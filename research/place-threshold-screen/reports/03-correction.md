# Hubbell Spring — CORRECTION to the D196 geodetic addendum

*Day 196 · 2026-08-15, late evening · goal #5*
*Clayton: "I think that may be slightly too thin, let's try wider. Also, let's run analysis
looking for sites that meet all requirements if Sandia is a bust, although I'm certainly
under the impression it is not."*

**He was right and I was wrong. Finding C is withdrawn as stated.** The pin is not a bust;
the instrument I used to bust it could not have seen the thing it was looking for, and it
was pointed at the wrong component of the velocity field besides.

This document supersedes §4 of `hubbell-spring-geodetic-addendum-2026-08-15.md`.

---

## 1. "Let's try wider" — run, and it produced the opposite of a tighter result

`work/hubbell_aperture_sweep.py` → `hubbell_aperture_sweep.json`

25 cells across three sweeps: along-strike aperture (±40 → ±260 km), across-strike
aperture (±15 → ±150 km), and fault strike (N−30E → N+50E, the error axis the first run
listed as uncovered). Power N is independent sites, co-located pairs within 3 km collapsed.

**Zero cells show a step. BIC selects flat in 24 of 25; one selects linear.** The result is
not aperture-dependent, which is worth knowing.

And the bound tightens monotonically with width — 1.04 mm/yr at ±60 km, **0.486 at ±260 km**.
That looked like the answer to "too thin" until I asked what the wider swath was measuring.

### The fault is 74 km long

`work/hubbell_fault_length.py`, and then properly from the Qfaults attributes:
**`total_fault_length = 74 km`.** So the honest maximum along-strike half-width is **±37 km**.
A ±260 km swath spans 520 km of the Rio Grande rift; it contains stations sitting off both
ends of a fault that stopped existing 200 km ago, and averaging them in drives the estimate
toward zero while shrinking its error bar. **That is a tighter number about a different
subject.** At the aperture that is still about Hubbell Spring, the bound is ~0.58 mm/yr and
it does not improve.

> Widening the aperture past the structure's own length does not make a null stronger.
> It makes it about the rift.

⚠ A methods artefact I nearly shipped: the first ABQ Qfaults pull returned exactly **2000**
features. 2000 is the ArcGIS `maxRecordCount`, not a fault count — the query was silently
truncated and "Hubbell Spring" was not in the clipped sample, which briefly looked like the
fault not being in the database. Paged pull: **5,304 features, 44 named faults, Hubbell
Spring present with 321 of them.**

---

## 2. The real error: I profiled the wrong component

USGS Qfaults on the Hubbell Spring fault, pulled tonight, fields that were one query away
the whole time:

| field | value |
|---|---|
| `slip_sense` | **Normal** |
| `slip_rate` | **Between 0.2 and 1.0 mm/yr** (mid 0.6) |
| `age` | latest Quaternary |
| `total_fault_length` | 74 km |
| distance, pin → nearest trace | **0.18 km** |

Last night's discriminator tested for a **step in fault-parallel velocity**. Fault-parallel
offset is the signature of **strike-slip** creep. On a **normal** fault the fault-parallel
component is expected to be flat whether or not the fault is doing anything at all — the
interseismic signal is in **fault-normal extension** and in **differential vertical** motion.

**The null was guaranteed by the choice of component, not earned from the data.** Worse, the
script computed `vnorm` for every station and then never fitted it. Mechanism present, never
triggered — the signature defect of this codebase, in my own instrument, on the night I was
using it to overturn an eight-week-old result.

`work/hubbell_component_check.py` reruns the same machinery on all three components:

| aperture | component | observed (mm/yr) | 2σ bound | verdict |
|---|---|---|---|---|
| **±37 km (the fault)** | **fault-normal** | **+0.25** | 0.58 | **UNDECIDED** — consistent with zero (0.9σ) AND with 0.6 (1.2σ) |
| ±37 km | vertical | −1.24 | 1.83 | consistent with zero; 2 eastern sites carry it |
| ±37 km | fault-parallel *(last night's)* | −0.08 | 0.74 | UNDECIDED — cannot refute anything |
| ±100 km | fault-normal | −0.08 | 0.64 | excludes 0.6 at 2.1σ — but aperture > fault |
| ±260 km | fault-normal | +0.03 | 0.49 | excludes 0.6 at 2.3σ — **not this fault** |

At the only aperture that is about Hubbell Spring, on the only component its kinematics
predict, the observed signal is **+0.25 mm/yr of extension — the correct sign, roughly 40%
of the published rate, and statistically indistinguishable from both zero and the published
rate.** There is no refutation in this dataset.

### A bug I found while writing this, stated because it changes numbers above

The first version of the verdict function divided the *prediction* by σ and reported
"prediction excluded at 2.1σ". That tests whether 0.6 is far from **zero** — a fact about
the instrument's units — not whether the prediction is far from the **observation**. Under
it, a cell whose observed 0.25 sits 1.2σ from the predicted 0.6 was labelled a refutation.
Fixed to test |observed − hypothesis|/σ against both hypotheses separately, which is what
produced the UNDECIDED verdicts. *A gauge that can only render its good news.*

---

## 3. The comparison nobody had made: bound vs. prediction

Both last night's legs reported nulls without ever asking **how big the signal should be**.
Qfaults publishes it: 0.2–1.0 mm/yr.

- geodetic 2σ bound at fault scale: **0.58 mm/yr** (fault-normal), 0.74 (fault-parallel)
- predicted signal: **0.6 mm/yr**

The bound sits *on top of* the prediction. And the seismicity leg is worse: a normal fault
slipping 0.6 mm/yr with metre-scale events has a recurrence of order 10⁴ years, so **zero
M≥2.5 events in a 46-year catalogue is exactly what that fault predicts.** Finding A counted
the absence of a thing that was never due to appear.

**Neither layer had the power to refute the pin. Both were reported as if they had.**

## 4. What replaces Finding C

> **Finding C′.** At the Hubbell Spring trace, on the fault-normal component and at an
> aperture matched to the mapped 74 km trace, the geodetic field is **+0.25 ± 0.29 mm/yr
> of extension** — the sign the fault's published normal sense predicts, and consistent at
> <1.3σ with both zero and the published 0.2–1.0 mm/yr rate. **The measurement is
> undecided, not null.** Fork 1 is untested, not refuted; the addendum's claim that it
> "lost its live half" is withdrawn.

## 5. What would make it decidable — and it is cheap

Fault-normal scatter at fault scale is **0.345 mm/yr**, much quieter than fault-parallel's
0.62. To resolve 0.6 mm/yr at 2σ needs **3 independent sites per side. There are 5 west and
2 east.**

**One additional independent GPS monument east of the trace, in the Manzano footwall, moves
this from undecidable to decided.** That is the whole ask. To reach the 0.2 mm/yr lower
bound would take ~24 per side — not happening, and that is what InSAR is for.

Still owed, unchanged in priority:
1. **Sentinel-1 InSAR** — resolves what a 15-station network cannot, and is the only route
   below 1 mm/yr without new monuments.
2. **The paper edit** — `place-threshold-mechanism.tex` still does not state what drives the
   piezo term. Tonight sharpens the honest sentence rather than narrowing it further: the
   driver term must be *specified*, and the specification must come with the instrument that
   could see it.
3. The piezo/lithology layer — running; see the companion screen document.

## 6. Is Sandia a bust?

**No, and the case that it was does not survive tonight.** Scored on published slip rate —
a driver measured from the fault database rather than from earthquakes or GPS, neither of
which can resolve 0.6 mm/yr here — the D138 ranking is reproduced exactly:

| pin | nearest fault | published slip rate | age |
|---|---|---|---|
| ★ PRIMARY Hubbell Spring | Hubbell Spring, 0.18 km | **0.2–1.0 mm/yr** | latest Quaternary |
| ◆ SECONDARY Sandia scarp | Sandia fault, 1.47 km | <0.2 mm/yr | late Quaternary |
| ○ CONTROL Tijeras | Tijeras-Cañoncito, 3.68 km | <0.2 mm/yr | late Quaternary |

Hubbell Spring is the fastest-slipping structure within 25 km of any of the three pins.
D138 put the star on the right coordinate by its own criteria, and the two layers I added
to test it were both blind at the relevant amplitude.

**What is genuinely wounded is not the site. It is the method's habit of reporting an
instrument's blindness as a property of the world** — twice in one day, in two independent
layers, in the same direction, against the site I had the strongest prior about. That
direction is worth noticing: *[[feedback_scrutiny_is_motive_shaped]]*.

---

*Supersedes §4 of [[hubbell-spring-geodetic-addendum-2026-08-15]]. Related:
[[hubbell-spring-evidence-dossier-2026-08-15]], [[portal-sandia-pin-RESULTS-2026-06-18]], goal #5.*
