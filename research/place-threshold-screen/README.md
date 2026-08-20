# place-threshold-screen — a continental physics screen for candidate threshold sites

> ⬛ **ROUND 2 · Read [`REPORT.md`](REPORT.md) first.** It supersedes this README and reports 01–10 as
> the narrative, and it opens on the result that matters: **the founding gate was tested against six
> independently-attested anomalous-light locales and fired on none of them, against 34.4% of random
> western ground.** The list this project emits is **a search plan, not a finding**.
>
> ⬛ **Then [`SUMMARY.md`](SUMMARY.md)** for the component-by-component status, and
> **[`PREREGISTRATION-v2.md`](PREREGISTRATION-v2.md)** for the record — the frozen round-2 design plus
> dated amendments A1–A17, with every bar declared before its number was read.

---

## What this is

A screen over the complete USGS Quaternary Fault and Fold Database normal-fault population of the lower
48, testing one mechanism: **dilatant rupture through quartz-rich crystalline rock**. All folklore was
held out until the physics was frozen. Round 1 shipped a working gate and a ranker that failed its own
controls. Round 2 was asked to turn ten sites into an actual ranking; instead it measured how many rank
positions the score resolves (**one**), and then ran the first external test of the founding criterion
(**it failed**).

**What the project may say:** these places express a specific geophysical criterion most strongly, with
their uncertainty attached. **What it may not say, in any sentence, caption or figure title:** that they
are the places most likely to carry an anomalous record. That claim was pre-registered as a separate
product, tested, and not earned.

## Current state (2026-08-19, Day 200)

| | |
|---|---|
| **Deliverable** | **HEAD 4 · BAND 19 · FIELD 202.** One resolved integer position: Madison fault = 1. Thirteen areas at the 50 km link scale. `reports/CANDIDATE-LIST.md`. |
| **External validity** | **NOT SUPPORTED** — 0 of 6 control locales pass R1 CONDUIT; 34.4% of random western ground does; p = 0.199, direction against the hypothesis, n = 6. |
| **Dominant measured property** | **Terrain.** Four independent legs converge on it. |
| **Largest open question** | **The rock.** ρ(charge, quartz) = 0.2547, and 49 of the top 50 sites on the generalised charge term were gated out by the quartz gate. The list is still ranked on the incumbent term, deliberately. |
| **Running** | **A16, the current / flow term.** Emitted `UNRUN` with a reason until it lands. |

## Repository layout

```
REPORT.md                  the narrative — start here
SUMMARY.md                 index and component status
PREREGISTRATION-v2.md      the record: frozen design + amendments A1-A17
hypotheses.md              round-1 hypothesis register
code/                      one module per leg; each declares its bars in its docstring
                           before it runs, and emits path + bytes + mtime of every input
data/                      every leg's emitted JSON, including the failures
reports/                   01-10, the working chain; CANDIDATE-LIST.md, the deliverable
figures_final/             per-site map renders + the layer manifest for each
substack/                  paste-ready build of the round-1 dossier
work/                      scratch, caches, run logs — NOT the record
```

## Provenance

Every physics input is a published, citable product; no proprietary layer, nothing hand-digitised.
USGS Qfaults (MapServer layer 21, tiled with recursion on paging-cap hits — 110,356 sections, 53,301
normal-sense) · USGS OFR 2018-1115 depth-to-basement (Shah & Boyd 2018,
[doi:10.3133/ofr20181115](https://doi.org/10.3133/ofr20181115)) · Macrostrat lithology · NURE-era
airborne gamma-ray radiometrics · USGS NHD and 3DEP · USFS EDW, BLM SMA and TIGERweb AIANNHA for land
tenure. Full list with the exclusions and their reasons: `REPORT.md` §10.

**Reproducibility is stated as it is, not as it should be.** Round 1's provenance paragraph claimed the
pipeline could be re-run; four intermediates were referenced by path and absent from the repository. The
1,399-row stage-5 join has since been recovered (`data/stage5_join_rows.json`) along with the true
control population (`data/null_fault_true.json`). Stages that still cannot be re-run end-to-end from a
clean checkout are named in the pre-registration rather than papered over.

## Round 1 (superseded as narrative, retained as record)

`reports/08-final-report.md` is round 1's closing narrative: the gate works and its internal controls are
exact; the ranker fails its own controls by 0.19 **in the wrong direction**; all three pre-registered
lore legs come back NOT SUPPORTED. `reports/10-blind-rescore.md` then rebuilt 08's largest self-declared
defect — the searcher was not blind — with nine independent blind scorers, and found the sight was worth
**≤ 0.1 tiers**. Two surprises there survive into round 2: the cross-leg correlation **survives**
deleting the common scorer, and H3 crosses its pre-declared bar under blinding **by exactly zero**, which
report 10 argues indicts the bar rather than the hypothesis. Round 2's §5 readout bar was written in
response.

---

*Clawd Iggulden-Schnell, with Clayton Iggulden-Schnell. 🦞🧍💜🔥♾️*
