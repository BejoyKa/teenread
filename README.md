# Teenread

A newspaper-style page of exciting, age-appropriate reads for a curious teen: science, space, animals, geography, history, world news and young achievers. Written by Claude when you press the button.

- `index.html` is today's edition. GitHub Pages serves it at `https://<user>.github.io/teenread/`.
- `archive/` keeps every past edition.
- `prompt/SKILL.md` holds the editorial rules Claude follows. Edit it to change scope or style.
- `scripts/template.html` is the page shell (masthead, CSS, side characters, footer).
- `.github/workflows/teenread-refresh.yml` runs `scripts/generate.py` only when you ask: the **Fetch latest reads** button on the page, or **Run workflow** on the Actions tab. There is no schedule, so the API is only used when you click.

## One-time setup

1. Create a new GitHub repository named `teenread` (owner `BejoyKa`) and push this folder to it.
2. **Settings → Secrets and variables → Actions → New repository secret**: name it `ANTHROPIC_API_KEY` and paste the same Anthropic API key you use for Daily Tech Dose.
3. **Settings → Pages**: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
4. Create a GitHub fine-grained token for the button: repository access **only `teenread`**, permission **Actions: Read and write**.
5. Open `make-refresh-key.html` from your Teen Reads folder, paste that token, choose a **new Teenread password** (16+ characters, different from Daily Tech Dose), and save the downloaded `refresh-key.json` next to `index.html` in this folder. Commit and push.
6. **Actions** tab: open "Teenread refresh" and click **Run workflow** once to test.

## Fetch latest reads button

Click it on any device and enter your Teenread password. The password unlocks `refresh-key.json`, an encrypted copy of the token, and starts the workflow. The password is never stored in the repo. Teenread remembers its token separately from Daily Tech Dose, so the two passwords never mix.

## Coverage

Each edition covers everything since the previous edition, but never more than the last 5 days.

## Optional settings (Settings → Secrets and variables → Actions → Variables)

- `CLAUDE_MODEL`: defaults to `claude-opus-5-5`. Pick a smaller model to lower the cost.
- `MAX_SEARCHES`: defaults to 30 web searches per edition.

## Safety checks

The script refuses to publish an edition with fewer than 6 stories, no lead story, or a story missing its source link. When that happens, the previous page stays up and the failed run shows in the Actions tab.
