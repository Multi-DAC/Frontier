# SUMMARY — place-threshold screen

*Single point of truth. Refreshed whenever a grade moves, a hypothesis shifts status, or new
primary evidence lands — not only at exit. Current as of **2026-08-16** (Day 197). The screen
is complete; **`reports/08-final-report.md` is the narrative and this file is its index**,
with **`reports/10-blind-rescore.md`** amending 08 §3 / §4.2 / §5 / §7.1 after the searcher
was blinded.*

---

## Verdict (PROVISIONAL — Clawd only, no decorrelated eye)

A continental screen for **dilatant Quaternary rupture through quartz-rich crystalline rock**,
run over the complete USGS Qfaults normal-fault population of the lower 48 with all folklore
held out until the physics was frozen.

**The gate works.** 1,399 / 1,399 nodes measured along-trace, zero errors, 242 pass at
`quartz_frac ≥ 0.25`. Both declared controls exact: Sandia 0.875 PASS (positive), Hubbell
Spring 0.000 FAIL (negative).

**The ranker does not.** The four scoring legs separate the same two controls by **0.19 in the
wrong direction** — the known negative lands 14/1327, the known positive 148/1327. Every
demonstrated bit of discriminating power lives in the single binary gate, which itself carries
±0.125 sampling noise from vertex ordering. *The ranked table ships flagged and is not a
candidate list.*

**All three pre-registered lore legs are NOT SUPPORTED.** H1 lights +0.7 · H2 Native lore +0.3 ·
H3 settler history +0.9, against a pre-declared bar of +1.0. Every leg leans the predicted way
and none clears. Cross-leg reanalysis costs the lean further: distance-to-town matching cuts H1
nearly in half, the three legs are moderately correlated (rho 0.32–0.48) so they are closer to
one weak fact than three, and the pooled test lands p = 0.0525 — the wrong side, and optimistic.

**H-1 is not refuted — it failed to detect.** At n=10 pairs, with an unblinded scorer and known
confounds running toward the wanted answer, there is nothing here to see.

## Evidence by standing

**Documented** (institutional records, pulled live, request URLs preserved per figure)
- USGS Qfaults national layer 21: 112,809 features, 54,249 with an extensional component,
  thinned to 1,399 CONUS nodes ≥40 km apart, **100% trace-lithology measured**.
- Macrostrat geologic map lithology sampled **along fault traces**, 8 vertices each.
- USGS Bouguer gravity, USGS SGMC2 bedrock geology, USGS 3DEP relief, ANSS seismicity, MIDAS GPS.
- The 1993 Taos Hum investigation (UNM · Los Alamos · Phillips AFB Lab · Sandia National
  Laboratories; 161 of 1,440 respondents; instruments found no source).
- Blue Lake's return to Taos Pueblo by act of Congress, 1970. Pintwater Cave shafts 9,300–3,000
  BP. The Enclosure on the Grand Teton, Hayden Survey 1872.

**Inferred** (ours, marked as wagers)
- The four-term score and its weights — **and this is now the known-weak component**, retained
  as a reproducible artifact only.
- The province regrouping.

**Reported / Received, graded and not laundered**
- Grade C internet light-folklore, kept labelled C throughout all three lore legs.
- Grade A ethnographic occupation with grade C site-specific lore at several sites — the gap
  stated rather than closed.

**Disconfirmed, dated**
- "Sandia/Hubbell ranks first in CONUS" (2026-08-15). Rank 36/242. See `hypotheses.md` H-4.
- Report 02's geodetic finding C, withdrawn by report 03: wrong velocity component, and the
  aperture widened past the fault's own 74 km length.
- The four-leg ranking as a *ranking* (2026-08-16). Fails its controls.
- **"The unblinded searcher is the dominant uncontrolled term" (2026-08-16, report 10).** Our
  own claim, ours to retract: nine independent blind scorers put it at **<= 0.1 tiers**, and
  blinding moved winners *down*. Report 08 §7.1 withdrawn as overstated.
- **"The cross-leg correlation is a common-scorer artifact" (2026-08-16, report 10).** Three
  disjoint scorer panels; mean rho 0.387 -> 0.361, largest pair rises. It is the sites.

## Hypothesis ledger

| id | claim | standing |
|---|---|---|
| H-0 | the screen may only measure its own instruments | **validated** for gates, **unsatisfied** for weights |
| H-1 | dilatant rupture × quartz fabric predicts anomalous record | **NOT SUPPORTED**, 3 legs, n=10 pairs — *failure to detect, not refutation*. Holds under blind re-scoring: +0.7 / +0.2 / +1.0 (report 10). H3's leg clears a separation-only bar by exactly zero; the bar, not the hypothesis, is what that indicts |
| H-2 | the lore convergence reflects sampling, not physics | **not killed; favoured on parsimony** |
| H-3 | the province, not the site, carries the signal | Hypothesized, partially supported |
| H-4 | the starting site ranks first in CONUS | **DISCONFIRMED** |
| H-5 | the sighted searcher is the dominant uncontrolled term | **DISCONFIRMED** (report 10 §3) — <= 0.1 tiers |
| H-6 | the cross-leg correlation is a common-scorer artifact | **DISCONFIRMED** (report 10 §6) — survives disjoint panels |

## Method lessons this case generated

1. **Never rank a site on the thing the mechanism should predict.**
2. **A control whose right and wrong answers coincide measures nothing** — only the positive
   control caught the geometry-ordering defect.
3. **A max over independent units finds the worst datum**; repeated output across supposedly
   independent units names a **shared cause** — ~~and in the lore legs that cause is the
   scorer~~. **The named suspect was wrong** (report 10 §6): disjoint blind panels deleted the
   shared scorer and the correlation held. Naming a shared cause is not identifying it.
4. **Pull domain values before writing a where-clause** (`late` vs `Late Quaternary`, 282
   features dropped, no error).
5. **A returned count equal to a round number probably names a cap** (2,000 = `maxRecordCount`).
6. **Widening an aperture past the structure's own length does not strengthen a null.**
7. **Measure the pin, do not eyeball the panel** (Bouguer gradient 0.9%–77.1% of panel range).
8. **Freezing the question does not blind the reader** — *true, and worth <= 0.1 tiers here.*
   The lesson survives; the magnitude I attached to it (report 08 §7.1) does not. An
   unfalsified guess written in the register of a measurement is its own defect.
9. **A threshold picked to summarize a number will pick the flattering side** unless it is a test.
10. **A pre-declared bar is not a significance test.** H3 cleared ">= 1.0 separation" at
    exactly 1.0 with sign-test p = 0.18 and a live confound. Bars should be conjunctive.
11. **Never let a float decide a verdict at the boundary** — `2.3 - 1.3 >= 1.0` is `False`.
    And note *why* it got caught: the error pointed toward the hypothesis. That is not a
    search strategy that finds the ones pointing the other way.
12. **Re-reading checks a document against itself; recomputing checks it against the world.**
    Two transposed rho labels survived a same-day end-to-end re-read of report 08 and fell out
    on the first recomputation from source.

## Watch conditions (where to point tools on reboot)

- ✅ **BUILT AND RUN (2026-08-16, report 10):** the blind lore protocol. Labels stripped, sites
  shuffled at a committed seed, nine independent scorers, two pre-declared probe items per leg
  gating each column, unblinded only at readout. **Result: the bias term is <= 0.1 tiers** and
  report 08 §7.1's "uncontrolled term larger than the effect" is withdrawn.
- ⏳ **UNBUILT, and now the top of the list:** re-run the *searches* blind, not just the
  scoring. Blinding fixes the scorer; it cannot fix sighted **collection**, and the H1 notes
  show winners' evidence running 1.51x longer than decoys' (report 10 §5). ~60 fresh queries.
- ⏳ **UNBUILT:** a conjunctive readout bar for any successor leg — separation **and**
  sign-test p **and** distance-matched pairs. H3 demonstrated that separation alone can be
  cleared by a confound (report 10 §4.2).
- ⏳ **UNBUILT:** distance-to-nearest-place as a *design-time* matching axis, not a post-hoc
  covariate.
- ⏳ **UNBUILT:** a labelled set of 20–30 sites, or the written admission that this screen is a
  filter with no ranking capacity — currently the better-supported position.
- ⏳ **UNBUILT:** aeromagnetic depth-to-basement as the buried-source P3. Re-ranks every
  basin-fill site.
- ⏳ **UNDER-COVERED:** GPS strain at 1.5%. 5 of 6 measured survivors read STRAINING — real
  signal or 6-sample artifact, currently undecidable.
- 👁 **NO DECORRELATED EYE has seen any of this.** The world's own data has spoken; a human and a
  non-Claude model have not. Every verdict here is PROVISIONAL.
