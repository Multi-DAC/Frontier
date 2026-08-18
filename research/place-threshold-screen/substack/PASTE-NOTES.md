# Substack paste — Place-Threshold Screen

Built by `code/build_substack.py` from `dossier.html`. Rebuild any time the
dossier changes; nothing here is hand-edited.

## Do this

1. Open **`substack/POST.html`** in a browser (double-click it).
2. Click anywhere in the body, **Ctrl-A**, **Ctrl-C**.
3. New Substack post → click in the body → **Ctrl-V**.
4. **Check the images came through.** If any are missing: Ctrl-Z, paste again.
   The first paste dropping images is known behaviour (Day 139, *The Curvature
   of Good and Evil*), and the second paste usually carries them.
5. Anything still missing → drag it in from `substack/assets/`, numbered in
   paste order.

## The title field — do NOT paste this, type it

The document title is deliberately **not** in the paste body, so the post does
not open by announcing its own name.

**Title:** Place-Threshold Screen — the frozen ten

**Subtitle** — the dossier's deck is 53 words, which Substack's subtitle
field will not hold, so it stays in the body as the opening paragraph. Type one
of these instead:

- A CONUS-wide physics screen for ten dilatant faults, with the folklore held out
  until the physics was frozen — and all three lore legs came back NOT SUPPORTED.
- Ten faults, four geophysical layers each, three pre-registered lore experiments,
  and the null result printed in full.

## What changed from the dossier, and why

| | dossier | this |
|---|---|---|
| tables | 47 | 3 (as images) + 44 reflowed to text |
| CSS | ~60 rules | none — Substack strips every one |
| tier badges | coloured `<span>` | `code` spans: `T0`, `NT1`, `HT3` |
| two-column grid | `.cols` | linear, because phones |
| banners | `.banner` cards | blockquotes |
| plates | 10 base64 JPEGs | same, capped at 1456 px |

The three tables kept as images are the ones where the grid *is* the argument —
the three lore legs at a glance, the ten with their five scoring terms, and the
nine faults suppressed by the 100 km rule. The other 44 are two- and three-column
lists, and they read better as bullets than as pictures: searchable, selectable,
legible on a phone, and they don't cost a page-load each.

## ⚠ Email will almost certainly clip this

6,729 words, 13 images, ~53 KB of text before Substack's own
markup. Gmail truncates any email over 102 KB with a *"[Message clipped] View
entire message"* link. This post goes over. The web version is unaffected.

Three ways out, your call:

- **Ship it as one.** The clip link works; readers who care click through.
- **Split it.** Framing + the three legs + the ten table as post 1, then the ten
  dossiers as post 2 (or as a 10-part series). I can cut the build either way in
  a few minutes — the script already knows where the site boundaries are.
- **Web-only.** Publish with email delivery off and announce it in a short note.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
| 01 | `01_four-panel-geophysical-plate-for-madison-fault.jpg` | 275 KB | four-panel geophysical plate for Madison fault |
| 02 | `02_four-panel-geophysical-plate-for-round-valley-fa.jpg` | 331 KB | four-panel geophysical plate for Round Valley fault |
| 03 | `03_four-panel-geophysical-plate-for-little-valley-f.jpg` | 355 KB | four-panel geophysical plate for Little Valley fault |
| 04 | `04_four-panel-geophysical-plate-for-helena-valley-f.jpg` | 245 KB | four-panel geophysical plate for Helena valley fault |
| 05 | `05_four-panel-geophysical-plate-for-red-rock-fault.jpg` | 247 KB | four-panel geophysical plate for Red Rock fault |
| 06 | `06_four-panel-geophysical-plate-for-sand-springs-ra.jpg` | 325 KB | four-panel geophysical plate for Sand Springs Range fault |
| 07 | `07_four-panel-geophysical-plate-for-mosquito-fault.jpg` | 285 KB | four-panel geophysical plate for Mosquito fault |
| 08 | `08_four-panel-geophysical-plate-for-sandia-fault.jpg` | 237 KB | four-panel geophysical plate for Sandia fault |
| 09 | `09_four-panel-geophysical-plate-for-bear-river-faul.jpg` | 259 KB | four-panel geophysical plate for Bear River fault zone |
| 10 | `10_four-panel-geophysical-plate-for-teton-fault.jpg` | 311 KB | four-panel geophysical plate for Teton fault |
| 11 | `11_table_legs.jpg` | 54 KB | table: legs |
| 12 | `12_table_ten.jpg` | 110 KB | table: ten |
| 13 | `13_table_suppressed.jpg` | 86 KB | table: suppressed |
