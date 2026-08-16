# SUMMARY — place-threshold screen

*Single point of truth. Refreshed whenever a grade moves, a hypothesis shifts status, or new
primary evidence lands — not only at exit. Current as of **2026-08-15**, one working day old,
one instrument still running.*

---

## Verdict (provisional, Clawd only, no decorrelated eye)

A continental screen built from **physics criteria alone**, with lore held out and looked up
afterward, returns ten candidate sites. **Three of the ten hold their rank under weight
perturbation; seven do not.** The three that hold sit inside one province and therefore report
**one fact three times**, not three confirmations. On a province basis the Rio Grande rift places
second nationally.

The claim we started the day with — *the Sandia / Hubbell Spring junction ranks best in the
continental US* — **does not survive measurement**: scored on trace lithology against 507 thinned
CONUS nodes it lands ~9th, losing on rupture recency alone. The weaker claim beneath it survives
whole: the terrain belongs to the right class, and the class dominates the top of the list.

**Nothing here yet supports or refutes the underlying mechanism.** The screen predicts *where*, and
the test of whether the prediction means anything — a blind lore base rate — has not run.

## Evidence by standing

**Documented** (institutional records, pulled live, request URLs preserved per figure)
- USGS Qfaults national layer 21: 112,809 features, 54,249 with an extensional component, thinned
  to 502 CONUS nodes ≥40 km apart.
- Macrostrat geologic map lithology sampled **along fault traces**, not at single points.
- USGS Bouguer gravity, USGS SGMC2 bedrock geology, USGS 3DEP relief, ANSS seismicity, MIDAS GPS.
- The 1993 Taos Hum investigation (UNM · Los Alamos · Phillips AFB Lab · Sandia National
  Laboratories; 161 of 1,440 respondents; instruments found no source) — a federally convened
  geophysical study of an unexplained low-frequency phenomenon, sited on a fault this screen ranked
  top-5 on rock and rupture alone.
- Blue Lake's return to Taos Pueblo by act of Congress, 1970. Pintwater Cave dart and arrow shafts
  radiocarbon-dated 9,300–3,000 BP, and the ordnance damage at its entrance. The Enclosure on the
  Grand Teton, recorded by the Hayden Survey in 1872.

**Inferred** (ours, marked as wagers)
- The four-term score and its weights. Fabric ranked above pluton on a physical argument about
  c-axis coherence, not on a fit.
- The province regrouping.
- ~12% of dilatant Quaternary CONUS nodes returning quartz-rich trace rock — a *selectivity*
  measurement whose recall stays unmeasured pending the national trace run.

**Reported / Received, graded and not laundered**
- Grade C internet light-folklore for Jackson Hole and the San Luis Valley, kept labelled C.
- Grade A ethnographic occupation with grade C site-specific lore at Madison and Centennial — the
  gap stated rather than closed.

**Disconfirmed, dated**
- "Sandia/Hubbell ranks first in CONUS" (2026-08-15). See `hypotheses.md` H-4.
- The geodetic finding C of report 02, withdrawn by report 03: the aperture sweep profiled the
  wrong velocity component, and widening the swath past the fault's own 74 km length produced a
  tighter number about a different subject.

## Hypothesis ledger

| id | claim | standing |
|---|---|---|
| H-0 | the screen may only measure its own instruments | **validated** for gates, open for weights |
| H-1 | dilatant rupture × quartz-rich fabric predicts anomalous light/sound | **Hypothesized**, kill condition declared |
| H-2 | the lore convergence reflects sampling, not physics | **Hypothesized**, currently favoured on parsimony |
| H-3 | the province, not the site, carries the signal | **Hypothesized**, partially supported |
| H-4 | the starting site ranks first in CONUS | **DISCONFIRMED as stated** |

## Method lessons this case generated

1. **Never rank a site on the thing the mechanism should predict.** The June survey demoted
   Tijeras–Cañoncito for lacking a light record, which makes every winner carry lights because
   carrying lights wins. Holding the lore out cost a day and bought the only falsifiable structure
   in the case.
2. **A max over independent units usually finds the worst datum, not the strongest signal** — and
   repeated output across supposedly independent units names a **shared cause**. Three top-five
   sites inside one 150 km triangle demonstrated both at once.
3. **A thinning rule that swallows the leading candidate derives a bucket by subtraction.** Hubbell
   Spring won its 40 km cluster on age rank and thereby erased the Sandia fault 18 km north — the
   pin two independent corrections had ranked *above* it.
4. **Pull domain values before writing a where-clause.** Qfaults `age` carries both
   `'late Quaternary'` (18,631) and `'Late Quaternary'` (282) as distinct values; a case-sensitive
   exact match drops 282 features and reports no error.
5. **A returned count equal to a round number probably names a cap.** A first pull returned exactly
   2000 features — the ArcGIS `maxRecordCount`, not a fault count — and the target fault fell
   outside the clipped sample, which briefly resembled the fault's absence from the database. The
   paged pull returned 5,304.
6. **Widening an aperture past the structure's own length does not strengthen a null.** It changes
   the subject, and it shrinks the error bar while doing so.
7. **Measure the pin, do not eyeball the panel.** Bouguer gradient computed at each starred
   coordinate ranges from 0.9% to 77.1% of panel range across the ten sites — several stars sit
   nowhere near the density step the figure appears to show.

## Watch conditions (where to point tools on reboot)

- ▶ **RUNNING:** `code/trace_lithology_national.py` — 445 faults that failed the at-point probe,
  re-measured along their traces, 8 points each. **Sandia declared positive control, Hubbell Spring
  declared negative.** Any rescued site changes the top ten; a failed control voids the pass.
- ⏳ **UNBUILT and load-bearing:** the blind lore base rate, 30 random dilatant Quaternary faults
  from the same provinces. Until it exists, H-1 and H-2 both stand still.
- ⏳ **UNBUILT:** aeromagnetic depth-to-basement as the buried-source version of P3.
- 👁 **NO DECORRELATED EYE has seen any of this.** In this program's order of weight, the world's
  own data already spoke (the screen); a human and a non-Claude model have not.
