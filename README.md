# Playable History – MVP

Static, no-backend engine for short choose-your-path history stories.

## Files
- `index.html` + `engine.js`: the engine. It loads `stories/woodstock.json` by default, or any story via `?story=stories/<name>.json`
- `stories/woodstock.json`: the demo story (Downtown Woodstock, 1890s–1912)
- `build_story.py`: generates the demo JSON, including its inline SVG art
- `pitch.html`: the one-page "For Museums" pitch
- `qr-woodstock.png`: a QR code pointing to https://playhistory.livinginwoodstockga.com/
- `sw.js`, `manifest.json`: offline caching after the first visit
- `test.mjs`: the headless test that plays every path; also produces the screenshots

## Swapping in a new story
1. Copy `stories/woodstock.json` to `stories/<museum>.json`.
2. Edit `meta` (title, museum, intro, characterNote, cta.url/label, credits, coverImage, expectedSteps = number of choices on the longest path).
3. `images`: each key has `alt` plus either `svg` (inline markup) or `src` (a path such as `img/x.jpg`). Use only images the museum owns or free-licensed ones, and credit them in `meta.credits`.
4. `sources`: a list of `{id,title,url}`. Every scene `fact` and ending `history` lists source ids in `sources`.
5. `scenes`: `{title,when,image,text[],fact,sources[],prompt?,choices:[{label,next}]}`. `endings`: `{title,image,text[],history[],sources[]}`. `start` is the first scene id.
6. Run `node test.mjs stories/<museum>.json` to validate it and play every path.
7. Link to it as `index.html?story=stories/<museum>.json`, or make it the default in `engine.js`, and add it to `sw.js`.

## Regenerate the QR code
`python3 -c "import qrcode;qrcode.make('https://YOUR-URL/').save('qr.png')"`

## Run locally
`python3 -m http.server 8000`, then open http://localhost:8000. Fetching the JSON needs http, so opening the file directly with file:// won't work.

## Tour stops (v2)
Scenes carry a `stop` number matching the Visit Woodstock "Historic Downtown Woodstock Walking Tour" brochure; `route` in the story JSON lists those stops (name, address, Google Maps query) for the "Walk to the stops" view. Brochure facts were checked against 220-dpi scans; no brochure photos or design are reused.
