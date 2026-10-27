"""Remove every picture (side character, corner characters, bottom art strip) from Teenread pages.
Safe to run more than once. Usage: python3 scripts/remove_pictures.py [files...]
With no arguments it cleans scripts/template.html, index.html and archive/*.html."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_DROP = re.compile(r"^\s*(\.side|\.mascots|\.corner|\.endart|@keyframes bob|@media\(min-width:1440px\)\{\.side|"
                      r"@media\(prefers-reduced-motion:no-preference\)\{\.side|@media\(max-width:700px\)\{\.titlebox)")

def clean(s: str) -> str:
    s = re.sub(r'<div class="side side-[lr]" aria-hidden="true">.*?</div>\n?', "", s, flags=re.S)
    s = re.sub(r'<div class="mascots" aria-hidden="true">.*?</div>\n?', "", s, flags=re.S)
    s = re.sub(r'<div class="endart">.*?</div>\n?', "", s, flags=re.S)
    s = re.sub(r'<img class="corner [^"]*"[^>]*>', "", s)
    s = re.sub(r'<div class="titlebox">(<h1>.*?</h1>)</div>', r"\1", s, flags=re.S)
    return "\n".join(l for l in s.split("\n") if not CSS_DROP.match(l))

files = [pathlib.Path(a) for a in sys.argv[1:]] or [
    ROOT / "scripts/template.html", ROOT / "index.html", *sorted((ROOT / "archive").glob("*-teenread.html"))]
for p in files:
    old = p.read_text(encoding="utf-8"); new = clean(old)
    if new != old:
        p.write_text(new, encoding="utf-8"); print("cleaned", p.name, f"({len(old)//1024} KB -> {len(new)//1024} KB)")
    else:
        print("already clean", p.name)
