# place-threshold-screen — a continental physics screen for candidate threshold sites

**GRADE (current — 2026-08-15, Clawd, no decorrelated eye yet)**

| part | grade |
|---|---|
| **Inputs** (fault trace, rupture age, slip sense, map lithology, Bouguer gravity, seismicity, GPS velocities) | **Documented** — USGS Qfaults, USGS SGMC2, USGS gravity, ANSS, MIDAS/Macrostrat. Pulled live; every layer records its own request URL in `figures/*.layers.json`. |
| **The ranking** (four-term score, top 10) | **Inferred** — our weighting over those inputs. A wager, marked as one. A ±50% weight perturbation keeps only three of ten slots stable. |
| **H-1** — dilatant Quaternary rupture through quartz-rich crystalline rock predicts an anomalous light/sound record | **Hypothesized**, untested. Kill condition in `hypotheses.md`. |
| **"Sandia/Hubbell Spring ranks best in the continental US"** | **Disconfirmed as stated** (2026-08-15). Measured against the same criteria the junction lands ~9th. The weaker claim — that the terrain belongs to the right class, and that the class dominates the top of the list — survives intact. |
| **RESISTANCE** | **LOW, and therefore under suspicion.** Four of the five printed sites returned grade-A Native or documented-anomaly material that the ranking could not see. That slots into our story too comfortably. Because nobody has yet measured the base rate of such material across the mountain West, the convergence earns **no** credit here — it triggers binocular focus, not belief. |

---

## 1. What this topic holds

Clayton framed the question in geophysics and lore, in that order, and asked for a screen that
could return somewhere other than the site we started from. This folder holds that screen: the
data pulls, the scoring code, seven working reports in sequence, and ten four-panel plates — one
per ranked site, each with a starred coordinate and layered imagery.

The program-level claim under test: **certain places host anomalous light and sound reports
because of what the rock does there**, specifically that a dilatant (normal-sense) fault rupturing
recently through quartz-rich crystalline basement supplies both a permeability pathway and a
piezoelectric source volume. Vallée's *window-area* observation supplies the phenomenology; this
screen supplies a falsifiable geographic prediction from the physics alone.

## 2. The one design decision that makes it a test

**The score contains no lore, no sighting count, no light record, and no proximity to any
facility.** A June-era survey demoted Tijeras–Cañoncito for lacking a light record, which ranks a
site on the very thing the mechanism claims to predict and renders the prediction unfalsifiable —
every winner carries lights because carrying lights wins. Here the four terms read:

| | criterion | source | weight |
|---|---|---|---|
| **P1** | recency of Quaternary rupture (conduit currency) | Qfaults `age` | 0–3 |
| **P2** | dilatant sense — normal faults open permeability, thrusts close it | Qfaults `slip_sense` | gate, not a term |
| **P3** | quartz-rich crystalline **at the trace** | Macrostrat geologic map | 0–2 |
| **P4** | junction density — distinct dilatant systems with trace inside 15 km | same cached pull | 0–2, capped |

The lore then gets looked up **afterward, per site, including the sites where I expected nothing** —
which converts "these places carry lore" from a selection effect into a prediction that could have
failed. On one of the five it did fail, and Section 5 of report 07 reports that failure as loudly
as the hits.

P3 weights **fabric above pluton** (2.0 vs 1.4), inverting the intuition that granite plays the
piezoelectric rock. An equigranular pluton averages its bulk piezoelectric moment toward zero
because the c-axes point everywhere; a tectonic fabric — gneiss, quartzite, mylonite — supplies
the case where they do not.

## 3. The result

62 of 507 thinned CONUS nodes (~12%) return quartz-rich crystalline at the trace, so the criterion
discriminates. Deduplicated to one node per fault system:

| # | score | site | age | rock | sys ≤15 km |
|---|---|---|---|---|---|
| 1 | 8.99 | **Madison fault**, 44.792 −111.438 — Hebgen Lake, MT | **historic** | gneiss | 6 |
| 2 | 8.19 | **Centennial fault**, 44.584 −112.066 — MT | latest Q | quartzite | 5 |
| 3 | 8.17 | **Teton fault**, 43.557 −110.862 — WY | latest Q | gneiss | 7 |
| 4 | 7.72 | Sawatch fault, 39.094 −106.380 — CO | late Q | gneiss | 5 |
| 5 | 7.38 | S. Sangre de Cristo fault, 36.849 −105.551 — NM | latest Q | gneiss | 3 |
| 6 | 7.38 | Mount Rose fault zone, 39.214 −119.816 — NV | latest Q | granodiorite | 13 |
| 7 | 7.10 | Helena valley fault, 46.759 −112.049 — MT | late Q | quartzite | 5 |
| 8 | 6.95 | East Pintwater Range fault, 37.036 −115.548 — NV | late Q | quartzite | 7 |
| 9 | 6.90 | Wasatch fault zone, 40.871 −111.855 — UT | latest Q | gneiss | 2 |
| 10 | 6.90 | N. Sangre de Cristo fault, 38.344 −105.950 — CO | latest Q | gneiss | 2 |

**Three deflations travel with that table and outrank it in importance.**

1. **Slots 4 and 5 amount to a coin flip.** Across 400 trials with every weight redrawn uniformly
   over a ±50% band, the top three hold a top-5 slot 100% of the time; Sawatch holds 57.8%, Mount
   Rose 51.5%, S. Sangre de Cristo 40.8%. Anyone reporting "the top 5" without that sentence
   reports their own weight choices.
2. **The top three amount to one fact, not three.** Madison, Centennial and Teton sit inside a
   ~150 km triangle on the Yellowstone hotspot's tectonic parabola. The thinning rule counts
   faults, not provinces, so one province spoke three times. Regrouped by province the Rio Grande
   rift places **second in the country** — and the Rio Grande rift holds Sandia.
3. **The pins do not sit on the gravity maxima.** Measuring the Bouguer gradient at each starred
   coordinate rather than eyeballing the panel: `data/gravity_gradient_at_star.json` shows Wasatch
   at 0.9% of its panel range and East Pintwater at 10.6%, against S. Sangre de Cristo at 77.1%.
   The star marks the fault trace, and on several sites the fault trace does not coincide with the
   basin-edge density step.

## 4. Where the starting site actually lands

Scored on **trace** lithology (75% of 16 sampled trace points quartz-rich, one unit named
*Sandia Granite*) rather than the at-point probe that failed it 1.5 km off-trace in fan gravel:

```
6.65   Sandia/Hubbell junction  ~34.98N −106.51   6 systems within 15 km   -> ~9th nationally
6.27   Hubbell Spring fault (own rock, 3% quartz along trace)
5.65   Sandia fault, granite trace point 35.074 −106.490
5.43   La Jencia fault, Socorro
```

The junction loses on exactly one term — P1. Its faults last ruptured in the late Quaternary at
0.05–0.2 mm/yr; Madison ruptured in 1959 in front of photographers. Nothing about the rock or the
structure ranks inferior; the **clock** runs slower.

## 5. What remains open, and in which direction it will move

- **Recall stays unmeasured.** The ranked list draws from the 62 nodes that passed an *at-point*
  probe — the probe that handed Sandia itself a false negative. 445 nodes failed it and await
  re-measurement along their traces. `code/trace_lithology_national.py` runs now with **Sandia
  declared the positive control and Hubbell Spring the declared negative**; should Sandia fail
  rescue or Hubbell pass, the run voids itself and says so. Until it lands, the top ten
  constitutes a **lower bound on the qualifying population**, and this folder deliberately ships
  without the in-flight output file rather than shipping a partial one.
- **The lore convergence has no denominator.** The correct control — draw 30 dilatant Quaternary
  faults at random from the same provinces, look each up blind, count grade-A hits — has not run.
  Until that number exists, Section 5 of report 07 reads as suggestive and nothing more.
- **P4 carries a stated, uncorrected bias.** Fault-*name* density partly measures mapping
  intensity, so a valley mapped at 1:24,000 outscores an identical valley mapped once at
  1:250,000. Capped at 2.0 for that reason and never permitted to dominate.
- **Aeromagnetic depth-to-basement** supplies the correct version of P3 for a *buried* crystalline
  source, and would re-rank every basin-fill site including the starting one.

## 6. Contents

| path | what it holds |
|---|---|
| `reports/01`–`07` | the seven working documents in the order they got written, ending with the continental top-10 |
| `code/` | every pull, screen, ranking and figure script — each one runnable standalone |
| `data/` | the small derived JSON each script emitted (scores, nodes, sweeps, gradients) |
| `figures/01`–`10` | one four-panel plate per site + a `.layers.json` recording each layer's provenance URL |

**Panels, identical across all ten sites so the eye can compare them:** **A** shaded relief (USGS
3DEP) with Quaternary traces coloured by rupture age · **B** bedrock geology (USGS SGMC2) with the
same linework · **C** Bouguer gravity · **D** regional context with ANSS seismicity.

⚠ **`reports/` carries the working documents verbatim, in ordinary English, not converted to
E-Prime.** Converting seven analysis documents after the fact would risk silently altering their
claims, and the repo's own rule exists to stop claims drifting. The grades, this README, the
hypothesis ledger and the `MEASUREMENTS.md` entry hold to E-Prime; the imported working papers
stand marked as imports.

⚠ Large upstream pulls stay **out** of the repo and re-derive from `code/qfaults_pull.py` and
`code/lithology_probe.py`: the national Qfaults GeoJSON (43 MB), the MIDAS velocity field, and the
Macrostrat response cache.

## 7. Provenance and standing

Screened, ranked, figured and written by **Clawd** on Day 196 (2026-08-15), at Clayton's
direction, inside the carapace body. **No decorrelated eye has looked at any of it.** The physics
inputs come from institutional records and anyone may re-pull them; the *weighting* remains ours,
and the lore section awaits its base rate. Treat the standing accordingly.

🦞🧍💜🔥♾️
