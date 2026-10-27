---
name: "teenread"
description: "Teenread: a newspaper-style HTML page of exciting, age-appropriate reads for a curious 13-year-old (science, space, animals, geography, history, world news, teen achievers). Use for Teenread, teen news, teen reads, or any work in the Teen Reads folder."
---

# Teenread

Produce a source-linked, newspaper-style page of the most exciting, trustworthy and age-appropriate reads from around the world for a curious 13-year-old girl. Each story shows a headline and a short crux; clicking it expands a rich, detailed read that explains the story in plain words, says why it is cool, and ends with a question to think about.

## Home folders
- Local working copy: the user's **Teen Reads** folder (`/Users/Bejoy Jacob/Claude Projects/Teen Reads`). Whenever a task touches that folder, follow this skill. Files there:
  - `Teenread.html` - the latest edition, with the "Fetch latest reads" button.
  - `YYYY-MM-DD-teenread.html` - one dated edition per day.
  - `make-refresh-key.html` - locks a GitHub token with the Teenread password into `refresh-key.json`.
  - `github-repo/` - the published site, its own GitHub repo `BejoyKa/teenread`, served at `https://bejoyka.github.io/teenread/`. Everything for Teenread lives here, separate from Daily Tech Dose. `index.html` is today's edition, `archive/` holds every dated edition plus `archive/index.html`, `scripts/template.html` is the page shell, `scripts/generate.py` builds an edition with the Claude API, `.github/workflows/teenread-refresh.yml` runs it when the Fetch button is pressed, and `refresh-key.json` holds the token locked with Teenread's own password (never the Daily Tech Dose one).
- Story markup always sits between `<!--CONTENT START-->` and `<!--CONTENT END-->`. When updating a page, replace only what sits between those markers plus the date in `<title>` and the masthead, keeping the buttons, CSS and script intact.
- Before building, check the newest dated edition to find the last edition date (Workflow step 1), match its structure, and avoid repeating its stories.

## Reader
A bright, curious 13-year-old girl. She likes big "whoa" facts, mysteries, animals, space, inventions, people (especially girls and young people) doing remarkable things, and stories from every corner of the world. Write for her: clear, lively, never babyish, never condescending.

## Scope
1. **Space & Sky** - missions, launches, telescopes, planets, stars, things to see in the night sky this week.
2. **Science & Discovery** - new findings in physics, chemistry, biology, the human body, inventions and cool tech (robots, materials, clever engineering).
3. **Amazing Animals & Nature** - new species, animal behaviour, oceans, plants, conservation wins.
4. **Planet Earth & Geography** - volcanoes, oceans, ice, landscapes, climate science explained calmly, places around the world.
5. **History & Mysteries** - archaeology, fossils and dinosaurs, solved (or unsolved) puzzles from the past, forgotten people in history.
6. **Around the World** - positive or fascinating world news: culture, records, architecture, festivals, good-news progress, from Asia, Africa, Europe, the Americas, the Middle East and Oceania.
7. **Young Changemakers & Creators** - teens and kids winning science fairs, photography and writing prizes, inventing, leading; also women and girls in science, art and history; great new books for teens.

## Content safety (strict)
- Age-appropriate only. No graphic violence, crime, war casualties, disasters told for shock, self-harm, adult content, gossip, or partisan politics. Hard topics (climate, extinction) are fine when explained calmly with what people are doing about them.
- Prefer trustworthy sources: NASA, ESA, JAXA, Science News Explores, Smithsonian, National Geographic, BBC, NPR, Reuters, AP, CBC, ScienceDaily, Space.com, EarthSky, university and museum press releases, DOGOnews, TIME for Kids. No tabloids or clickbait.
- Never invent facts, figures, quotes, ages or names. Label anything unconfirmed "Reported". Say clearly when a study is early (for example a preprint) or a claim is a test, not a product.

## Workflow
1. Set the window: from the last edition's date to today (default last 24 hours if there is none), but never more than the last 5 days.
2. Run parallel web searches per scope area, with global angles. Include month and year in queries. Good hunting grounds: Smithsonian Smart News, Science News Explores, ScienceDaily (space, animals, fossils, strange & offbeat), Space.com, EarthSky, DOGOnews, Positive News, NASA/ESA news, Society for Science.
3. Verify each story on the source page; confirm its publication date falls in the window. A recent article about an older study is fine if the article itself is in the window; say when the study came out.
4. Select 12-18 stories (up to about 22 when the window spans several days) by "wow factor + learning value"; balance subjects and regions; aim for at least one story about a girl or woman doing something remarkable. Skip empty sections.
5. Choose the lead story: the single most exciting read, ideally one a teen can relate to.
6. Build the page (below). Save `YYYY-MM-DD-teenread.html` and `Teenread.html` in the Teen Reads folder, update the site copy (`github-repo/index.html`, `github-repo/archive/`), present the page, and give a 2-3 line chat summary.

## Page design (strict)
The same simple, traditional newspaper layout as Daily Tech Dose. Black text on a light warm-white background. No colours, gradients, images, or emojis.

- **No pictures**: the page has no images or character art anywhere; text and rules only.

- **Masthead**: centered serif title "Teenread", a small tagline "Big ideas for curious minds", date and coverage window beneath, thin black rules above and below. "Archives" link at top left, "Fetch latest reads" button at top right.
- **Layout**: a lead story at the top (larger headline), then stories in a 2-3 column grid on desktop (single column on mobile), grouped under small-caps section headings in this order: Space & Sky, Science & Discovery, Amazing Animals & Nature, Planet Earth & Geography, History & Mysteries, Around the World, Young Changemakers & Creators, Did You Know? Thin black rules between sections and stories.
- **Collapsed story**: small uppercase meta line (source · date), bold serif headline, a 2-3 line crux, and a "Read more" label.
- **Expanded story** (use `<details>/<summary>`): unlike Daily Tech Dose, this is a rich, exciting read of about 250-400 words, built from short sub-sections with `<h4>` headings, for example:
  - **What happened** (or Some background / Who was she?) - the story told like a story, with any hard word explained in plain language.
  - **The numbers** - a `<ul class="facts">` list of 3-6 key facts and figures (sizes, ages, dates, speeds), with everyday comparisons where helpful.
  - **How do they know?** or **The science behind it** - how scientists worked it out, the method or the mechanism, in kid-friendly terms.
  - Then `<p class="cool"><strong>Why it's cool:</strong> ...</p>` connecting it to her world, and `<p class="think"><strong>Think about it:</strong> ...</p>` with one open question that makes her imagine, predict or decide. Both are required on every story.
  - End with a "Read source" link.
  - Background explanations may use well-established general knowledge, but every story-specific fact must come from the source.
- **Collapse**: the page shell adds a "Collapse" button at the end of each expanded story, and the "Read more" label switches to "Collapse" while a story is open. Do not write these into the story markup.
- **Did You Know?**: a short `<div class="watch"><ul>` list of 4-6 quick facts or things to look out for (sky events, exhibitions, mission dates) drawn from this edition's sources.
- **Type**: serif (Georgia, "Times New Roman") for headlines and body; system sans-serif only for small meta labels. Body 16-17px, line-height 1.5, max width about 1100px.
- **Colors**: text `#1a1a1a`, background `#faf9f5`, rules `#1a1a1a`. Nothing else.
- One self-contained HTML file with inline CSS; no external assets.

### Skeleton
```html
<!--CONTENT START-->
<article class="lead"><details><summary><p class="meta">Source · Date</p><h3>Lead headline</h3><p class="crux">Crux.</p><p class="more">Read more</p></summary>
 <div class="detail">
  <h4>What happened</h4><p>...</p>
  <h4>The numbers</h4><ul class="facts"><li>...</li></ul>
  <h4>The science behind it</h4><p>...</p>
  <p class="cool"><strong>Why it's cool:</strong> ...</p>
  <p class="think"><strong>Think about it:</strong> ...</p>
  <p><a href="URL">Read source</a></p>
 </div></details></article>
<h2>Space &amp; Sky</h2>
<div class="grid">
 <article><details><summary><p class="meta">Source · Date</p><h3>Headline</h3><p class="crux">Crux.</p><p class="more">Read more</p></summary>
  <div class="detail">(same structure as the lead)</div></details></article>
</div>
<h2>Did You Know?</h2>
<div class="watch"><ul><li>...</li></ul></div>
<!--CONTENT END-->
```

## Rules
Every story has a working source link and date. Paraphrase; never copy article text. Keep the crux to 2-3 lines; let the expanded read be rich (250-400 words) but always clear and broken into short sections. Escape ampersands as `&amp;`. If a section has no good stories, omit it.
