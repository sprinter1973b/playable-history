# Playable History – MVP

Static, no-backend engine for short choose-your-path history stories.

## Files
- `index.html` + `engine.js`: the engine. It loads `stories/woodstock.json` by default, or any story via `?story=stories/<name>.json`
- `stories/woodstock.json`: the demo story (Downtown Woodstock, 1890s–1912)
- `build_story.py`: generates the demo JSON, including its inline SVG art
- `pitch.html`: the one-page "For Museums" pitch
- `qr-woodstock.png`: a QR code pointing to https://playhistory.livinginwoodstockga.com/
- `sw.js`, `manifest.json`: offline caching after the first visit
- `test.mjs`: validates the story and all 25 tour stops and lists every path; `ui_test.py` plays every path and the whole walking tour in a headless browser and takes the screenshots
- `tour_data.py`: the 25 walking-tour stops; `add_photos.py`: adds stop photos

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

## Walking Tour mode (v3)
The "🗺 Walking Tour" button lists all 25 stops of the Visit Woodstock "Historic Downtown Woodstock Walking Tour" brochure in order. Each stop has its name, address, a Google Maps link, a short blurb using only facts from the brochure (cited as the source; no brochure photos or design reused), and a one-question quiz. "Walk on" buttons chain the stops 1→25, and stops that are part of the depot story (12, 16, 17, 18, 25, in blue) have a button that jumps into that chapter. Stop data lives in `tour_data.py`; run `python3 build_story.py` to rebuild `stories/woodstock.json` (existing photo entries are kept).

## Adding photos
Use only photos you took or have written permission to use (for example from History Cherokee). Don't use the brochure's photos without Visit Woodstock's OK.
1. Put the photos in one folder, each named by its stop number: `12.jpg`, `16.png`, `17.jpg` ...
2. Optional: add `captions.csv` to that folder, one line per photo: `17,The depot in 2026,John Thomas`
3. Run `pip install pillow` (once), then `python3 add_photos.py <folder> --credit "John Thomas"`. Each photo is resized to 1200px wide, compressed to about 150 KB, saved as `images/<stop>.jpg`, and linked in `stories/woodstock.json` (`route[].photo` = `{src, alt, caption, credit}`).
4. Run `node test.mjs` (it checks every photo file exists), then upload `images/` and `stories/woodstock.json` to GitHub.
A stop with no photo, or whose file is missing, simply shows no picture.
