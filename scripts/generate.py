"""Generate today's Teenread edition with the Claude API.

Reads prompt/SKILL.md (the editorial rules), asks Claude to research the news
with the server-side web search tool, and writes:
  index.html                           latest edition (what you read every day)
  archive/YYYY-MM-DD-teenread.html    dated copy
  archive/index.html                   list of past editions

Environment:
  ANTHROPIC_API_KEY   required
  CLAUDE_MODEL        optional, default claude-opus-5-5
  MAX_SEARCHES        optional, default 30
  TZ_NAME             optional, default America/Toronto
  MAX_LOOKBACK_DAYS   optional, default 5 (longest coverage window after a gap)
"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import anthropic

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
TEMPLATE = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")
SKILL = (ROOT / "prompt" / "SKILL.md").read_text(encoding="utf-8")

MODEL = os.environ.get("CLAUDE_MODEL") or "claude-opus-5-5"
MAX_SEARCHES = int(os.environ.get("MAX_SEARCHES") or 30)
MAX_LOOKBACK_DAYS = int(os.environ.get("MAX_LOOKBACK_DAYS") or 5)
TZ = ZoneInfo(os.environ.get("TZ_NAME") or "America/Toronto")
# Newest first; falls back to the basic version if the model doesn't support the newer one.
SEARCH_TOOLS = ["web_search_20260209", "web_search_20250305"]

START, END = "<!--CONTENT START-->", "<!--CONTENT END-->"
ARCHIVE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-teenread\.html$")


def editions() -> list[dt.date]:
    out = []
    for p in ARCHIVE.glob("*-teenread.html"):
        m = ARCHIVE_RE.search(p.name)
        if m:
            out.append(dt.date.fromisoformat(m.group(1)))
    return sorted(out)


def extract_content(page: str) -> str:
    return page[page.index(START) + len(START): page.index(END)].strip()


def build_prompt(today: dt.date, since: dt.date, previous: str | None) -> tuple[str, str, str]:
    system = (
        "You are the editor of Teenread, a daily newspaper of exciting, age-appropriate reads for a "
        "curious 13-year-old girl. Follow these editorial rules exactly.\n\n"
        + SKILL
        + "\n\n## Output contract for this run (overrides the save/present steps above)\n"
        "- The page shell (head, CSS, masthead, footer) already exists. Output ONLY the story "
        f"markup, wrapped exactly between {START} and {END}.\n"
        "- Use the same structure and class names as the example: one <article class=\"lead\"> "
        "first, then <h2> sections each followed by <div class=\"grid\"> of <article> items, "
        "each with <details><summary> (meta, h3, crux, <p class=\"more\">Read more</p>) and "
        "<div class=\"detail\">, ending with a Did You Know? section (<div class=\"watch\"><ul>).\n"
        "- Each <div class=\"detail\"> is a rich 250-400 word read using <h4> sub-heads (What happened, "
        "The numbers as <ul class=\"facts\">, How do they know? or The science behind it), then "
        "<p class=\"cool\"><strong>Why it's cool:</strong> ...</p>, then "
        "<p class=\"think\"><strong>Think about it:</strong> ...</p>, then the Read source link. "
        "No industry-impact paragraph. Do not add a Collapse button; the page adds it.\n"
        "- Escape ampersands as &amp;. No <script>, <style>, images, or inline styles.\n"
        "- Every story must have a real source URL you found in search results this run.\n"
        "- Do not write anything before the start marker or after the end marker."
    )
    window = (
        f"{since:%b %-d}–{today:%b %-d, %Y}" if since != today else f"{today:%b %-d, %Y}"
    )
    user = (
        f"Today is {today:%A, %B %-d, %Y}. Build today's edition covering news published "
        f"from {since:%B %-d, %Y} through today ({window}). Search widely first, verify dates, "
        "then write the markup."
    )
    if (today - since).days > 1:
        user += (
            f" This edition spans {(today - since).days} days, so pick the 12-22 most exciting "
            "stories across the whole window, not just today's."
        )
    if previous:
        user += (
            "\n\nHere is the previous edition's markup. Match its structure and tone, and do "
            "NOT repeat its stories unless there is a material new development (then say what "
            f"changed):\n\n{previous}"
        )
    return system, user, window


def call_claude(system: str, user: str) -> str:
    client = anthropic.Anthropic()
    last_err = None
    for tool_type in SEARCH_TOOLS:
        messages = [{"role": "user", "content": user}]
        so_far: list = []  # assistant blocks accumulated across pause_turn
        try:
            for _ in range(8):  # continue through pause_turn
                with client.messages.stream(
                    model=MODEL,
                    max_tokens=48000,
                    system=system,
                    messages=messages,
                    tools=[{"type": tool_type, "name": "web_search", "max_uses": MAX_SEARCHES}],
                ) as stream:
                    msg = stream.get_final_message()
                print(f"[{tool_type}] stop={msg.stop_reason} usage={msg.usage}", file=sys.stderr)
                so_far.extend(msg.content)
                if msg.stop_reason == "pause_turn":
                    messages = [
                        {"role": "user", "content": user},
                        {"role": "assistant", "content": so_far},
                    ]
                    continue
                if msg.stop_reason == "max_tokens":
                    raise RuntimeError("Hit max_tokens before finishing the edition")
                text = "".join(b.text for b in so_far if b.type == "text")
                return text
            raise RuntimeError("Too many pause_turn continuations")
        except anthropic.BadRequestError as e:  # e.g. tool version unsupported by model
            last_err = e
            print(f"{tool_type} rejected, trying next: {e}", file=sys.stderr)
    raise RuntimeError(f"All web search tool versions failed: {last_err}")


def validate(content: str) -> str:
    if START not in content or END not in content:
        raise ValueError("Response is missing the content markers")
    body = content[content.index(START) + len(START): content.rindex(END)].strip()
    body = re.sub(r"<script\b.*?</script>", "", body, flags=re.S | re.I)
    body = re.sub(r"<style\b.*?</style>", "", body, flags=re.S | re.I)
    articles = body.count("<article")
    if articles < 6:
        raise ValueError(f"Only {articles} stories; refusing to publish a thin edition")
    if 'class="lead"' not in body:
        raise ValueError("No lead story")
    if body.count("href=\"http") < articles:
        raise ValueError("Some stories are missing source links")
    return body


def render(content: str, today: dt.date, window: str, archive_href: str) -> str:
    now = dt.datetime.now(TZ)
    return (
        TEMPLATE.replace("{{CONTENT}}", content)
        .replace("{{DATE_LINE}}", f"{today:%A, %B %-d, %Y} &nbsp;·&nbsp; Coverage: {window}")
        .replace("{{DATE_SHORT}}", f"{today:%B %-d, %Y}")
        .replace("{{GENERATED}}", f"{now:%b %-d, %Y %-I:%M %p %Z}")
        .replace('href="archive/"', f'href="{archive_href}"')
    )


def write_archive_index() -> None:
    items = "\n".join(
        f'  <li><a href="{d.isoformat()}-teenread.html">{d:%A, %B %-d, %Y}</a></li>'
        for d in reversed(editions())
    )
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Teenread — Past editions</title>
<style>
body{{background:#faf9f5;color:#1a1a1a;font-family:Georgia,"Times New Roman",serif;margin:0;padding:0 24px 60px;line-height:1.6;font-size:17px}}
.wrap{{max-width:700px;margin:0 auto}}
h1{{text-align:center;font-size:44px;margin:28px 0 0;padding:18px 0 12px;border-top:4px double #1a1a1a;border-bottom:1px solid #1a1a1a}}
a{{color:#1a1a1a}} ul{{padding-left:20px}} li{{margin:8px 0}}
p{{text-align:center;font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase}}
</style></head>
<body><div class="wrap">
<h1>Past editions</h1>
<p><a href="../">Back to today's edition</a></p>
<ul>
{items}
</ul>
</div></body></html>
"""
    (ARCHIVE / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    today = dt.datetime.now(TZ).date()
    ARCHIVE.mkdir(exist_ok=True)
    past = [d for d in editions() if d < today]
    # Cover everything since the last edition, but never more than MAX_LOOKBACK_DAYS:
    # refresh the next day -> news since yesterday's edition; after a long gap -> the last 5 days.
    since = (past[-1] if past else today - dt.timedelta(days=1))
    since = max(since, today - dt.timedelta(days=MAX_LOOKBACK_DAYS))
    previous = None
    if past:
        previous = extract_content(
            (ARCHIVE / f"{past[-1].isoformat()}-teenread.html").read_text(encoding="utf-8")
        )

    system, user, window = build_prompt(today, since, previous)
    content = validate(call_claude(system, user))

    (ROOT / "index.html").write_text(render(content, today, window, "archive/"), encoding="utf-8")
    (ARCHIVE / f"{today.isoformat()}-teenread.html").write_text(
        render(content, today, window, "./"), encoding="utf-8"
    )
    write_archive_index()
    print(f"Published edition for {today} ({content.count('<article')} stories)")


if __name__ == "__main__":
    main()
