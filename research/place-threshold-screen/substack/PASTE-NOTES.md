# Substack paste — The Ground Under the Lights

Built by `code/build_report.py` from `dossier.html` + `code/report_text.py`.
Rebuild any time either changes; **nothing in `substack/` is hand-edited.**

This is the *narrative* build. `code/build_substack.py` still exists and still
works — it reflows the internal dossier one-for-one. That one is the internal
artifact. This one is the article.

## Do this

1. Open the file you want in a browser (double-click it).
2. Click anywhere below the orange line, **Ctrl-A**, **Ctrl-C**.
3. New Substack post → click in the body → **Ctrl-V**.
4. **Check the images came through.** If any are missing: Ctrl-Z, paste again.
   The first paste dropping images is known behaviour (Day 139, *The Curvature
   of Good and Evil*); the second paste usually carries them.
5. Anything still missing → drag it in from `substack/assets/`, numbered in
   paste order.

## Three builds — pick one

| file | words | text KB | images | what |
|---|---|---|---|---|
| `POST.html` | 12,515 | 85 | 13 | the whole report, one post |
| `POST-part1.html` | 5,332 | 36 | 3 | the report **without** the ten site dossiers |
| `POST-part2.html` | 7,315 | 52 | 10 | the ten site dossiers alone |

**Gmail clips any email over 102 KB** with a *"[Message clipped]"* link. The web
version is never affected. `POST.html` goes over that; part 1 on its own does
not. So:

- **One post** → paste `POST.html`. Email readers get a clip link.
- **Two posts** → paste `POST-part1.html` today and `POST-part2.html` as the
  companion field guide. Part 1 already ends with a pointer to it, and part 2
  opens with a two-sentence recap so it stands alone.

## The title field — do NOT paste this, type it

**Title:** The Ground Under the Lights

**Subtitle** — pick one:

- A continental screen for the physics of anomalous places, with the folklore
  held out until the physics was frozen — and the null printed in full.
- Ten faults, four geophysical layers each, three pre-registered lore
  experiments, nine blind scorers, and a result that did not go our way.

If you publish it as two, part 2's title: **The Ground Under the Lights — the ten sites**.

## What this build does that the old one did not

| | old (`build_substack.py`) | this |
|---|---|---|
| structure | the internal dossier's | question → method → rigour → results → sites |
| lore | tier tables per site | **narrative prose per site**, tiers stated inline |
| framing | none — opens on a results table | opens on the observation and the conjecture |
| method | scattered through captions | its own section, plus a rigour section |
| tables | 3 imaged + 44 reflowed | 3 imaged, the rest written into the prose |
| numbers | rendered from data | rendered from data **and asserted against it** |

Every measurement quoted in the prose — score, gate reading, trace length,
segment count, junction count, mapped length, nearest place — is checked against
`dossier.html` and `data/top10_frozen_100km.json` at build time. A typo fails
the build rather than shipping.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
| 01 | `01_the-three-lore-legs-at-a-glance.jpg` | 57 KB | the three lore legs at a glance |
| 02 | `02_the-ten-with-their-five-scoring-terms.jpg` | 112 KB | the ten with their five scoring terms |
| 03 | `03_faults-suppressed-by-the-100-km-rule.jpg` | 86 KB | faults suppressed by the 100 km rule |
| 04 | `04_four-panel-geophysical-plate-for-madison-fau.jpg` | 275 KB | four-panel geophysical plate for Madison fault |
| 05 | `05_four-panel-geophysical-plate-for-round-valle.jpg` | 331 KB | four-panel geophysical plate for Round Valley fault |
| 06 | `06_four-panel-geophysical-plate-for-little-vall.jpg` | 355 KB | four-panel geophysical plate for Little Valley fault |
| 07 | `07_four-panel-geophysical-plate-for-helena-vall.jpg` | 245 KB | four-panel geophysical plate for Helena valley fault |
| 08 | `08_four-panel-geophysical-plate-for-red-rock-fa.jpg` | 247 KB | four-panel geophysical plate for Red Rock fault |
| 09 | `09_four-panel-geophysical-plate-for-sand-spring.jpg` | 325 KB | four-panel geophysical plate for Sand Springs Range fault |
| 10 | `10_four-panel-geophysical-plate-for-mosquito-fa.jpg` | 285 KB | four-panel geophysical plate for Mosquito fault |
| 11 | `11_four-panel-geophysical-plate-for-sandia-faul.jpg` | 237 KB | four-panel geophysical plate for Sandia fault |
| 12 | `12_four-panel-geophysical-plate-for-bear-river-.jpg` | 259 KB | four-panel geophysical plate for Bear River fault zone |
| 13 | `13_four-panel-geophysical-plate-for-teton-fault.jpg` | 311 KB | four-panel geophysical plate for Teton fault |
