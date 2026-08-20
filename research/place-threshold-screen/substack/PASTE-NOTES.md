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
| `POST.html` | 12,662 | 86 | 13 | the whole report, one post |
| `POST-part1.html` | 5,686 | 37 | 3 | the report **without** the ten site dossiers |
| `POST-part2.html` | 7,107 | 51 | 10 | the ten site dossiers alone |

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

- Ten areas in the western United States where the physics of anomalous places is
  most strongly expressed — screened from every mapped normal fault in the lower
  forty-eight, with the folklore held out of the arithmetic.
- A continental screen for the ground under the lights: 110,356 mapped sections,
  1,399 nodes, 242 through the gate, thirteen areas, ten printed.

If you publish it as two, part 2's title: **The Ground Under the Lights — the ten areas**.

## Round 2 — what changed in this build

The deliverable is **ten AREAS at the 50 km separation scale**, driven from
`data/candidate_list.json`. The round-1 article shipped ten *faults* at 100 km,
scraped out of `dossier.html` — which coupled the article's membership to a stale
artefact. It no longer does. Two areas are new (Centennial Valley, Antelope
Valley) and two dropped below the cut (Bear River, Teton).

Both new areas were measured through the same along-trace probe as the other
eight, with both declared controls run first and required to reproduce exactly
(`code/l1_detail_round2.py`), and their plates are built by the same
`site_figure.build()` as the rest (`code/plates_round2.py`). Neither has a lore
entry: they entered after the three experiments were frozen, and a sighted
post-hoc lookup is the contamination the pre-registration exists to prevent.

Register: confounds and controls are stated **once**, in the method section, and
the rest of the article presents findings.

## What is checked at build time

Every measurement quoted in the prose — score, gate reading, trace length,
segment count, junction count, mapped length, nearest place — against
`dossier.html` for the eight round-1 areas and against
`stage5_join_rows.json` + `l1_detail_round2.json` + the plate's own layers
manifest for the two round-2 ones. Plus: **membership and order of the ten**
against `candidate_list.json`, the cut gap and head gap recomputed, every
superlative in the prose recomputed across the ten, all lore tiers against the
frozen result files, and the headline programme figures against the summaries.
A typo fails the build rather than shipping.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
| 01 | `01_the-three-lore-legs-at-a-glance.jpg` | 57 KB | the three lore legs at a glance |
| 02 | `02_the-ten-areas-with-their-measured-terms.jpg` | 126 KB | the ten areas with their measured terms |
| 03 | `03_the-three-areas-immediately-below-the-cut.jpg` | 35 KB | the three areas immediately below the cut |
| 04 | `04_four-panel-geophysical-plate-for-madison-fau.jpg` | 275 KB | four-panel geophysical plate for Madison fault |
| 05 | `05_four-panel-geophysical-plate-for-round-valle.jpg` | 331 KB | four-panel geophysical plate for Round Valley fault |
| 06 | `06_four-panel-geophysical-plate-for-little-vall.jpg` | 355 KB | four-panel geophysical plate for Little Valley fault |
| 07 | `07_four-panel-geophysical-plate-for-centennial-.jpg` | 262 KB | four-panel geophysical plate for Centennial fault |
| 08 | `08_four-panel-geophysical-plate-for-antelope-va.jpg` | 354 KB | four-panel geophysical plate for Antelope Valley fault zone |
| 09 | `09_four-panel-geophysical-plate-for-helena-vall.jpg` | 245 KB | four-panel geophysical plate for Helena valley fault |
| 10 | `10_four-panel-geophysical-plate-for-red-rock-fa.jpg` | 247 KB | four-panel geophysical plate for Red Rock fault |
| 11 | `11_four-panel-geophysical-plate-for-sand-spring.jpg` | 325 KB | four-panel geophysical plate for Sand Springs Range fault |
| 12 | `12_four-panel-geophysical-plate-for-mosquito-fa.jpg` | 285 KB | four-panel geophysical plate for Mosquito fault |
| 13 | `13_four-panel-geophysical-plate-for-sandia-faul.jpg` | 237 KB | four-panel geophysical plate for Sandia fault |
