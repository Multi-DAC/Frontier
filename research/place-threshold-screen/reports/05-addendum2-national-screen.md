# Addendum 2 — the base rate, the national screen, and where the pin should actually sit

*Day 196, 2026-08-15, late. Answers three questions Clayton asked: what the base-rate run
found; whether anywhere else in the continental US fits better; and whether the most likely
locations inside the area can be pinned. Supersedes §A3 of
[[hubbell-spring-CONFIRMATION-AND-LORE-2026-08-15]] and retires `work/national_site_screen.py`
as run.*

---

## 1. The "national" screen was never national, and its zero was not a finding

`work/national_site_screen.py` reported `[stage1] +0 (total 0)` and exited clean. I read that
last night as "no US site meets all five requirements." It meant nothing of the kind. Two
independent defects, **neither of which raised an error**:

| # | defect | measured consequence |
|---|---|---|
| **a** | endpoint was `Qfaults/MapServer/**12**/query`. Layer 12 is **New Mexico**. Layer **21** is the National Database. | NM holds 16,189 features and **zero** rated above 5 mm/yr. National holds **112,809**. The screen queried one state — the one state whose answer it was supposed to be compared against — and that state has no fast faults, so stage 1 emptied. |
| **b** | where-clause asked for `'Between 5.0 and 1.0 mm/yr'`. The actual domain string is `'Between **1.0 and 5.0** mm/yr'`. | Drops **16,667 of 32,891** matching features — slightly over half — while the OR's other arm still returns 16,224. This is the worse of the two: it does not fail, it *shrinks*, and a plausible non-zero count comes back. |

Defect (a) caused the zero. Defect (b) was latent underneath it and would have survived the
fix silently. The domain values were one `returnDistinctValues` query away and I did not run it.

**This is the fourth instrument in two days to return a wrong answer with no error**, after
the wrong velocity component, the wrong aperture, and the Qfaults GIS class read as a slip
rate. A fifth turned up while writing this: `work/hubbell_fault_length.py` reported
`"hubbell": []` from a bbox spanning 34.2–35.6 °N — every one of the 15 faults it returned
lies **north of 34.985**, i.e. the response was truncated at the service record limit and the
pin's own fault, at 34.90, fell off the end. The fault is in that layer: 321 segments.

---

## 2. Fixed and run properly, the screen returns California — and that is the result

Corrected pull: **32,891** fast-fault features, **122** distinct named faults, thinned to
**402** candidate nodes ≥25 km apart. Strain from NGL MIDAS (8,067 stations, 50 km radius,
3σ-MAD trim, 200 scrambles per node).

- **155** nodes STRAINING above the Kansas-craton floor with p < 0.05
- **206** nodes **UNMEASURED** — fewer than 5 GPS stations within 50 km. **That is a 51% null
  space**, and it is not random: it is rural. Anything the screen "did not find" in the
  interior may simply be unmonitored.
- **0** nodes in New Mexico. Not "none qualified" — none *exist*: no NM fault is rated ≥1 mm/yr.

Top of the ranking, γ̇max in nstrain/yr:

```
Brawley Seismic Zone   32.977 -115.549  slip 7.5  648.1
Imperial fault         32.711 -115.390  slip 7.5  623.8
San Andreas fault zone 36.394 -120.981  slip 7.5  578.5
San Andreas fault zone 36.203 -120.786  slip 7.5  548.1
San Andreas fault zone 36.569 -121.158  slip 7.5  535.9
```

**The screen is a plate-boundary detector.** It had to be: R5 ("slip rate ≥ 1.0 mm/yr")
selects for plate boundaries by construction, and R4 (modern strain) selects for the same
places twice. I wrote R5 last night as an *instrument* requirement — sites where my
instruments could actually decide something — and then let it sit in a list headed
"requirements," where it reads as physics.

**The consequence, stated plainly: this screen cannot rank Hubbell Spring at all.** Its
corrected slip rate is 0.05 mm/yr. It fails R5 by a factor of 20. A screen on which the
candidate scores zero is not a comparison, and running it harder will not make it one.

So: **"the most likely site in the continental US" has no national comparison behind it.**
It did not have one on Day 138 — that survey compared a shortlist, not a continent — and
tonight's screen is not one either. The claim is not refuted. It is **unsupported**, which is
a different and more honest thing.

What a real comparison needs is the screen with R5 and R4 removed and the *physics* criteria
kept: Quaternary conduit + quartz-rich crystalline near surface + evidence of a live crustal
fluid pathway. That population is 112,809 features rather than 32,891, and it is the run
worth building next. It will also, unlike this one, be able to return Sandia.

---

## 3. Inside the area, the pin moves — and this is the answer to "pin the most likely locations"

Full geometry, `fault_name = 'Hubbell Spring fault'`, layer 12: **321 segments, 4,390
vertices**, mapped extent **34.634 → 34.997 °N** = **40.1 km** north–south (the
`total_fault_length` attribute says 74 km, so the layer maps just over half of it).

The D138 pin at 34.900, −106.530 sits **0.18 km from the mapped trace** — the 180 m the
earlier document quoted, confirmed against geometry rather than recalled. Along-strike it is
**29.4 km from the south end, 10.7 km from the north end**.

Qfaults grades every segment by `linetype`, and the grades are **not** evenly spread:
**181 Inferred · 79 Moderately Constrained · 61 Well Constrained**. "Well Constrained" is
where a scarp is actually expressed at the surface. Binning traced length by 2 km of latitude:

```
  lat        lon    traced_km  WELL_km   well%   mod%
 34.992  -106.517       3.0      0.9      31%     0%
 34.974  -106.519       6.2      3.9      62%     6%   <-- MAXIMUM
 34.956  -106.518       8.9      2.5      28%     8%
 34.938  -106.525       9.2      0.9       9%    23%
 34.920  -106.523      15.8      0.8       5%     4%
 34.902  -106.523      15.6      0.5       3%    15%   <-- the D138 pin sits here
 34.884  -106.521       8.5      1.1      13%    16%
 34.866  -106.550       4.3      2.6      60%    17%   <-- MAXIMUM
 34.848  -106.557       2.5      0.8      33%    29%
 34.830  -106.554       3.2      1.1      36%    43%
 34.812  -106.543       4.0      0.0       0%    86%
 34.794  -106.537       4.9      0.8      16%    81%
 34.776  -106.539       6.6      2.0      30%    28%
 34.758  -106.542       6.2      1.7      27%    30%
 34.740  -106.545       2.4      0.8      32%     0%
 34.722  -106.543       4.1      0.7      17%    23%
 34.704  -106.544      11.1      0.0       0%    78%
 34.686  -106.549       6.7      0.0       0%    71%
 34.668  -106.544       6.6      0.0       0%    81%
 34.650  -106.554       2.2      0.0       0%    29%
 34.632  -106.554       0.8      0.0       0%     0%
```

**The pin is on one of the worst-constrained stretches of the whole fault** — 3% well
constrained, and it is also the bin with the *most* traced length (15.6 km), which is what
heavily-inferred mapping looks like: long, smooth, drawn between control points.

Two maxima, and they are the two locations to pin:

- **34.974 N, −106.519 W** — 3.9 km of well-constrained scarp, 62% of the bin. Northern
  strand, closest to the Kirtland boundary.
- **34.866 N, −106.550 W** — 2.6 km, 60%. Southern strand, and note the **~3 km westward
  step in longitude** between 34.884 and 34.866: this is a mapped left-step / relay in the
  fault system, which is exactly the structural setting where a normal fault's damage zone
  and permeability are highest.

Neither of these is where the instrument put its star. The star went to a stretch nobody has
walked, on a rate that was wrong by 10×.

**Caveat, and it cuts the other way:** `linetype` grades *mapping confidence*, not fault
activity. A well-constrained bin may simply be where a graduate student had good air photos.
It is a proxy for "someone verified rock here," which is what I want for a pin, and it is not
a proxy for "more active." Both maxima need the aeromagnetic depth-to-basement pass (§A4 row 1)
before either is more than a better-evidenced guess than the old one.

---

## 4. Base rate — PARTIAL, and the partial is not yet a number

`work/lithology_baserate.py` restarted after the 20:08 body restart and is running 80 random
western-CONUS land points through the identical Macrostrat instrument that returned
quartz-rich rock within 0–5 km at Hessdalen, Brown Mountain, Marfa, Piedmont MO and 10 km at
the pin. Each point costs 49 API probes; throughput is ~3.5 min/point live, so the full run
lands well after this document.

**n = 20 of 80 at time of writing.** Distribution of nearest quartz-rich crystalline rock over
20 random western-CONUS land points:

```
  at the point (0 km)   20%
  within  2 km          30%
  within  5 km          30%
  within 10 km          35%
  within 25 km          40%
  within 40 km          40%      <-- 60% of the West has NONE within 40 km
```

So the answer is not "granite is everywhere." **Sixty percent of random western points return
nothing within 40 km**, and the base rate for the criterion the four anomaly sites met —
quartz-rich crystalline within 5 km — is **≈30%**.

Four of four sites clearing a 30% bar is **0.30⁴ ≈ 0.8%** under independence. That is the
first number tonight that points *toward* the convergence being real rather than away from it,
and I distrust it for four stated reasons:

1. **n=20.** The 30% carries roughly ±10 points of sampling error at this size. The full 80
   could move it to 20% or 40%, and 0.20⁴ vs 0.40⁴ is a 16× swing in the product.
2. **The sites were not drawn from this population.** They were selected by other people for
   having lights. Any p-value here is descriptive, not a hypothesis test — there is no
   pre-registration and no correction for how the four were chosen.
3. **Independence is assumed and is probably false.** Hessdalen is not in the western CONUS
   at all; Piedmont MO and Marfa are in different provinces, but "reported lights" correlates
   with terrain, which correlates with basement geology. The 0.8% is an upper bound on the
   surprise, not a measurement of it.
4. **The pin itself is at 10 km, not ≤5** — it clears the 35% bar, not the 30% one, and it is
   the weakest of the five on this layer.

The honest one-line version: **the piezo convergence survived its first denominator.** It is
no longer explicable as "that's just what the West is made of." It is not yet evidence of
anything, and the remaining 60 points decide how much of it stands.

---

## 4b. The provenance check came back, and it is the finding of the night

I sent a search into the mercu tree to answer one question: was the Day 137–138 survey that
produced this pin *actually* national? Files:
`Corpus-Perspectival/Unreleased-Work/{portal-transport-site-search-2026-06-17.md,
portal-sandia-pin-RESULTS-2026-06-18.md, sandia_pin_analysis.py}`.

**(i) It was never national, at any stage that produced a number.**

The D137 "national narrowing" is a desk argument over **~8 hand-named regions** — 2 ranked, 3
honourable mentions, 3 PNW candidates rejected — with **no dataset, no cells and no computed
score**. Scoring was hand-assigned `✓✓ / ✓ / ~` marks. The document says so itself: *"This is
REGIONAL identification, not a pinned site."*

The only quantitative instrument, `sandia_pin_analysis.py:19`, runs on:

```python
BBOX = "-106.9,34.3,-106.3,35.3"     # 0.6° x 1.0° -- ~55 x 111 km around Albuquerque
```

378 Bouguer points, 31 named faults, split into **exactly two cells** (`:158-159`), **top 3
reported per cell** (`:149`). The whole scoring scheme is `sandia_pin_analysis.py:145`:

```python
score = gd + fd   # km; lower = better convergence
```

An unweighted 1:1 sum of two distances. The Bouguer value carries **zero** weight. Slip rate
is read into the tuple at `:78` and **index 4 is never referenced again** — a dead variable.
It became a criterion for the first time on D196, i.e. by me, two nights ago.

**So: Hubbell Spring ranked #1 of 3 curated pins, inside 1 of 2 cells, inside 1 bounding box.**
Not #1 of anything national. The box was chosen by hand-waved regional reasoning the previous
day, which itself started from Clayton's interest in a trip to Yakima.

**(ii) The geophysics did not choose Hubbell Spring. The anomaly record did.**

This is the part that matters, and it is quoted verbatim from
`portal-sandia-pin-RESULTS-2026-06-18.md:41` — the justification for ★ PRIMARY:

> **Carries the documented prior:** this is the western Manzano front at the **Manzano Weapons
> Storage Area / Bennewitz 1979–80 plasma-lights locus** — the one place in the survey with a
> *recurring-anomaly record* (the Hessdalen criterion). Documented prior + most-active fault +
> granite + adjacent basin = **the only cell that scores on all layers including the empirical
> one.**

And the runner-up, `:45-46`:

> ◆ SECONDARY — Sandia fault, west scarp. **Best piezo in the survey:** the Sandia granite is
> quartz-monzonite, exceptionally quartz-rich — granite **2.0 km**, the strongest amplifier
> here. […] **No documented light-record of its own**, but the cleanest *geophysical*
> transport-class convergence with a strong piezo.

And the control, `:49-50`: Tijeras–Cañoncito is *"the best **raw** convergence"* — density low
0.3 km from an active fault — and was demoted to CONTROL explicitly because it has **no
anomaly record**.

**Read those three together and the ordering is unambiguous: on geophysics alone the survey's
own text ranks Tijeras first, Sandia scarp second, Hubbell Spring third.** The published
ranking is the reverse, and the variable that reverses it is the presence of a light-record.
The cell containing the winner is even *named* for it — `sandia_pin_analysis.py:159`:
`pin("C2 — MANZANO front (Bennewitz/plasma-lights locus)", 34.45, 34.90)`. **The cell boundary
was drawn around the report.**

**The consequence for the strongest-feeling piece of evidence in this whole program.** The
story has been: *we were not looking for Sandia; the geophysics found it on its own, and only
afterwards did the anomaly record and the Native lore turn out to be there too.* That story is
**false in its load-bearing clause**. The anomaly record was not a downstream confirmation —
it was an **input to the selection**, applied as the tiebreaker over a geophysically better
site, inside a box drawn by hand. There is no independent convergence to be surprised by,
because the two things that appear to converge were never independent.

**And two separate corrections now agree on the same replacement.** Tonight's lithology
re-rank against a real geologic map — not the Bouguer density proxy — inverted the ranking and
put the **Sandia west scarp** ahead of Hubbell Spring. That is exactly what the June survey's
own geophysical text said before the empirical tiebreaker overrode it. Two independent routes,
one answer: **the geophysically-best pin in this system has been the Sandia fault west scarp
(~35.08–35.12 N, −106.51 W) the entire time.**

That does not make Sandia-the-area a bust — it is the *same range front*, 20 km north. It
retires one specific claim: that an instrument blind to the lore picked the spot the lore
points at.

---

## 5. Net effect

**Withdrawn:** "no other US site meets all requirements" — never measured; the query hit one
state. **Withdrawn:** the D138 star as the best location *within* the fault system — it sits
on 3%-constrained inferred trace.

**Withdrawn:** "the most likely site in the continental US" — now not merely unmeasured but
**traced to its actual population, which was 378 gravity points in a 55 × 111 km box.** The
phrase has no continental content at all.

**Withdrawn:** the independence of the geophysics from the anomaly record. The record was the
tiebreaker, applied over a geophysically better site, in a cell named after it.

**Unsupported, not refuted:** that some site in the CONUS is best on these criteria. No screen
yet built can rank an intraplate 0.05 mm/yr fault, because every screen so far has selected on
rate or on modern strain, and this site is defined by having neither.

**Standing and strengthened:** the fault is real, 74 km, mid-cycle, M 6.8–7.1 capable; the
pin is 180 m from the trace, confirmed against geometry; and there are now **two named
coordinates** worth the next instrument instead of one.

*Related: [[hubbell-spring-CONFIRMATION-AND-LORE-2026-08-15]],
[[feedback_zero_needs_a_positive_control]], [[feedback_novelty_gauge_counts_the_harm]],
[[feedback_gauge_and_responder_mis_specified_as_a_pair]], goal #5.*
