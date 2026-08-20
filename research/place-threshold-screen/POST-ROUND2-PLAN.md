# Rebuilding the Substack Post as the final report — round 2

*Opened Day 201 / 2026-08-20, on Clayton's instruction: the Post — not `REPORT.md` — is the
final deliverable. `REPORT.md` is a methods-and-audit document; the Post is the article, and it
should look like the dossier. The Post presents **the top ten areas**. It presents findings; it
does not relitigate itself paragraph by paragraph.*

---

## 1 · What the Post currently is, and why it is stale

`substack/POST.html` was built **2026-08-18** by `code/build_report.py` from `dossier.html` +
`code/report_text.py`. Nothing in `substack/` is hand-edited — the article is authored in
`report_text.py` and assembled. That contract stands; the rebuild edits `report_text.py`.

It is stale in three separate ways, and they are not the same fix:

1. **Membership.** It ships the **100 km** frozen ten. Round 2's deliverable is built at **50 km**.
2. **Evidence.** It predates A6–A17 entirely — the external test, rank resolution, the terrain
   confound, the charge term, radiometrics, water, flow. All of round 2.
3. **Unit.** It presents ten *faults*. Clayton asked for ten *areas*, which is the coarser and
   more honest object, and which round 2 already computed.

## 2 · THE DEFECT FOUND WHILE SCOPING THIS — two frozen tens, not one

`data/top10_frozen.json` and `data/top10_frozen_100km.json` both carry `"frozen": "2026-08-16"`.
They are **different lists**:

| | `top10_frozen.json` (50 km) | `top10_frozen_100km.json` (100 km) |
|---|---|---|
| shared | Madison · Round Valley · Little Valley · Helena valley · Red Rock · Sand Springs Range · Mosquito | *(same seven)* |
| **differs** | **Centennial · Antelope Valley · Fish Lake Valley** | **Sandia · Bear River · Teton** |

- `build_report.py:620` reads the **100 km** file → the published article's ten.
- `candidate_list.py:72` sets `SEP_KM = 50.0`, docstring *"the frozen list's own separation rule"*
  → true of the **50 km** file, not of the one the article shipped.

**So the published Post and the current deliverable disagree about three of ten sites, and no
artefact anywhere states which fork it is on.** `figures_final/` records the 100 km membership
only by accident — it has ten plates and they are that ten.

**A claim I nearly filed and did not, because it was wrong.** The 100 km file's `control` field
reads *"50 km rebuild reproduced top10_frozen.json exactly before this list was generated."* Next
to two files that visibly disagree that reads as a false reproducibility claim. It is not: it says
a 50 km *re-run* reproduced the 50 km *file* — determinism — and that is true. Resolve the
referent before scoring the sentence.

Load-bearing consequence: Madison ↔ Centennial is **54.77 km** (measured, and
`candidate_list.py:340` already knew: *"Centennial sits 54.8 km from Madison"*). Centennial is a
head site **only** under the 50 km rule. Under 100 km it merges into the Hebgen Lake area. That is
a real fork in the deliverable and the article must name the scale it chose.

## 3 · The deliverable: ten areas

Areas are single-linkage clusters of the 23 head+band structures at 50 km
(`data/candidate_list.json → areas`, 13 of them). Ordered by their best-scoring member:

| # | area | best-scoring member | score | extent | structures | plate |
|---|---|---|---|---|---|---|
| 1 | Hebgen Lake, MT | Madison fault | 0.8370 | 13.7 km | 4 | `figures_final/01` |
| 2 | Sierra front / Walker Lane, CA | Round Valley fault | 0.7324 | **115.1 km** | 7 | `figures_final/02` |
| 3 | Carson Range, NV | Little Valley fault | 0.7112 | 11.8 km | 2 | `figures_final/03` |
| 4 | Centennial Valley, MT | Centennial fault | 0.6812 | 0 | 1 | **NEW** `work/figures_round2/04` |
| 5 | Antelope Valley, CA/NV | Antelope Valley fz | 0.6244 | 0 | 1 | **NEW** `work/figures_round2/05` |
| 6 | Helena Valley, MT | Helena valley fault | 0.6240 | 0 | 1 | `figures_final/04` |
| 7 | Red Rock Valley, MT | Red Rock fault | 0.6168 | 0 | 1 | `figures_final/05` |
| 8 | Sand Springs Range, NV | Sand Springs Range fault | 0.6160 | 0 | 1 | `figures_final/06` |
| 9 | Mosquito Range, CO | Mosquito fault | 0.6134 | 0 | 1 | `figures_final/07` |
| 10 | Sandia Mountains, NM | Sandia fault | 0.6108 | 0 | 1 | `figures_final/08` |

**Below the line, printed rather than cut:** Bear River fz 0.6064 · Teton fault 0.6016 ·
S. Sangre de Cristo 0.5936. **The #10/#11 gap is 0.0044 of composite score against an instrument
step of 0.025** — one L1 vertex. The tenth line runs through the middle of a band, so the band is
printed. That is a finding about resolution, stated once, not a hedge repeated.

**Three tiers, and this is the article's spine because it is the strongest positive the ranking
ever produced:**

- **Position 1 is resolved.** Madison / Hebgen Lake is the **only integer position** the whole
  project resolves (`candidate_list.json → resolved_positions`).
- **A head of four**, P(top ten) = 1.000, never gated out: Madison · Round Valley · Little Valley ·
  Centennial. Internal order **not** resolved (Round Valley > Little Valley holds in 66.7% of draws).
- **Six more** that belong on the list and that the score cannot order.

## 4 · Ordering areas by best-scoring member is a NEW operation

`REPORT.md` §3 orders areas by *nothing* — it prints head-containing areas first, then the rest
alphabetically, and says explicitly that member count never orders them. Ranking the 13 by
`best_score` and cutting at 10 is introduced here for the article. It must be stated as the rule it
is, with the 0.0044 cut named. It is defensible; it is not inherited.

## 5 · What is DONE

- ✅ Two new four-panel plates, all 5 layers present, no failed panels:
  `code/plates_round2.py` → `work/figures_round2/`. Same `site_figure.build()` as the other eight,
  so "built identically at every site" stays true.
- ✅ `work/qfaults_normal_national.geojson` rebuilt from the corrected round-2 national pull
  (`work/qfaults_west.geojson`), filtered on `slip_sense` containing *normal*: **53,301 of 110,356**
  — asserted in the script against the count `REPORT.md` §10 states, not eyeballed. The old path was
  simply absent and `site_figure` died on it.
- ✅ Panel-B bedrock-at-node re-probed through `lithology_probe` itself, not retyped:
  Centennial **TIER_FABRIC / quartzite / Frontier Formation** — which *reproduces the cached
  stage-2 value exactly*, a free control on the lookup. Antelope Valley **TIER_VOLCANIC /
  rhyolite**, unit *"Cretaceous marine rocks (in part nonmarine), unit 2 (West Walker River)"*.
- ✅ `report_text.py` DECK rewritten to the round-2 deliverable.

## 6 · What is LEFT

1. **`report_text.py` prose.** Framing keeps. Then: METHOD to round-2 numbers (110,356 sections /
   53,301 normal / 1,399 nodes / **242 gate passes** / **225 ranked-complete + 17 partial** — those
   are two different quantities and the old text conflates them); RESULT sections rebuilt as
   findings — external test (A6), resolution (A7), terrain (A8/A12/A14/A16), rock (A13/A15), lore
   (H1–H3) compressed; the ten areas; closing recast from confession to recommendation.
2. **`build_report.py` refactor — the real work.** `parse_sites()` scrapes the ten sites out of
   `dossier.html` and hard-fails on `len(sites) != 10`. That couples membership to a stale artefact.
   Drive membership from `candidate_list.json → areas` instead, render measurements from
   `stage5_join_rows.json`, and take plates from `figures_final/` or `work/figures_round2/`.
3. **`near_km`** (nearest census place) for Centennial and Antelope Valley — the per-site header
   line prints it and `CHECK` has it only for the round-1 ten.
4. **The lore gap, which must be stated and must NOT be filled.** H1/H2/H3 and the nine blind
   scorers ran on the **100 km** ten plus matched decoys. Centennial and Antelope Valley were never
   scored. Looking them up now, sighted, post hoc, is precisely the contamination the
   pre-registration exists to prevent. Those two areas get **"The ground"** and no **"The record"**,
   with the reason printed. The absence is the honest artefact.
5. Correct `candidate_list.py:85-87`'s docstring — *"the frozen list's own separation rule"* is
   ambiguous across two files that disagree — and add the fork to `REPORT.md` §3.

## 7 · The one thing to raise with Clayton

He asked for *"the top 10 most likely areas for anomalous phenomena."* `REPORT.md` §1 records that
exact claim as **Product B**, pre-registered as a separate product, tested, and **not earned** — and
A6 is the test that took it. The article therefore ships the strongest version that is *true*:
**these are the ten areas where the physics we can measure is most strongly expressed, and this is
where we would send an instrument.** That is a recommendation, it is ours, it is defensible, and it
is what he asked for. The A6 result is printed as a finding in its own right — it is the most
important number the project produced — rather than as a disclaimer attached to every sentence.
