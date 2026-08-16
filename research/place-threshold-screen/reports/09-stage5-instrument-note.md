# Stage 5 — the ten closed, the join built, and the join fails its own controls

*Day 197 · 2026-08-16 · carapace · work/remeasure_ten.py, work/stage5_join.py*

## 1. The ten falsy-zeros were three different things

| # | class | what it actually was |
|---|-------|----------------------|
| 8 | network | genuinely unmeasured — but **half were never transient** |
| 1 | phantom duplicate | the fault **was** measured; a second row silently resolved to zero |
| 1 | out of population | `Left lateral` fault inside a `Normal`-only screen |

**The 403s are a WAF rule on the `where` clause, deterministic per name.** Measured, not
inferred:

```
LIKE '%House Range%'                      OK, 91 features
LIKE '%House Range (west side) fault%'    403
LIKE '%Salt%Cache%'                       OK, 37 features
LIKE '%Salt and Cache Valleys faults%'    403
```

It is **not** "parentheses" and **not** "the word *and*" — 35 names containing `(` and 19
containing ` and ` measured fine overnight and still return 200 on retest. The trigger is
substring-level (`Salt and` passes, `t and C` does not; `Range (` passes, `Range (w` does
not) — the shape of a SQLi signature list. A retry loop can never clear it; the fix is a
literal ladder plus a client-side exact match.

**The phantom ran opposite to how I first read it.** The USGS attribute for *Wah Wah
Mountains (south end near Lund) fault* carries a trailing **U+000B**. Stage 3 took the name
raw and measured it correctly — 23 segments, 154.6 km, 8 points, `quartz_frac` 0.0, an
honest zero. Stage 4B then checked done-ness on the **stripped** name (`trace_lithology_full.py:86`)
while writing rows under the **raw** one (`:96`), so the clean spelling never matched, got
measured again, and this time the exact filter compared the service's tabbed attribute
against a clean `==` and dropped all 23 segments — silently, as 0.0. Ghost deleted,
survivor reconfirmed independently (AGREE). That mismatch also explains `done` carrying
1401 rows for a 1399-fault population.

**Tijeras-Cañoncito is off-frame, not refuted.** `slip_sense = Left lateral`; the entire
population is the normal-fault national pull. The name carried in the file was a label I
wrote, not a USGS attribute, so no exact match was ever possible. Marked `off_frame`.

**Lithology leg now 1399/1399, zero errors, 242 pass, controls 0.875 / 0.000 exact.**

## 2. A control killed the first fix

The obvious repair was to source geometry from the local layer-21 pull already on disk and
skip the network entirely. Run through the controls first, it read:

```
Sandia fault          declared 0.875   local geometry 1.000   DISAGREE
Hubbell Spring fault  declared 0.000   local geometry 0.000   agree
```

Same layer, same fault, same probe — the local file concatenates segments in a different
**order**, and `trace_points` samples every `(len//8)`-th vertex. Different order, different
eight vertices. Both readings are honest; they are not the *same* reading, so they are not
mergeable.

The **negative** control agreed down both paths and on its own would have passed the swap
through. 0.0 is 0.0 everywhere; a control whose right and wrong answers coincide measures
nothing. Only the positive control could see it.

Consequence, recorded: **`quartz_frac` carries sampling noise of order `1/N_SAMPLE` = 0.125
from vertex ordering alone.** A second, independent reason the layer filters and cannot rank.

## 3. The join is built around coverage, because the legs are wildly unequal

```
L1 lithology     1399/1399   100.0%
L2 age_rank      1399/1399   100.0%
L4 junction      1399/1399   100.0%   (computed)
L3 slip rate     1349/1399    96.4%
L6 length        1328/1399    94.9%
L5 GPS strain      21/1399     1.5%   <-- annotation only
```

"Sites that meet **all** requirements" is the right question and the most dangerous query
shape this dataset admits: an AND across all six legs returns ~21 sites and reports 1,376
**unmeasured** faults as *failed requirements*. Same defect as the ten falsy zeros, at
population scale, and invisible in the output — a short list looks like a strict screen.

Rules, therefore: a leg may only **exclude** a fault it actually measured. Every fault
carries `PASS / FAIL / UNMEASURED` — three values, never two. L5 may **promote** a site and
never demote one, because a missing GPS node is a fact about the network, not the fault.

**The first run of the scorer reproduced the same bug one more time:** the score was a mean
over available legs, so three faults scored on 2 of 4 legs outranked every fully-measured
site — missing data buying rank. Now tiered on completeness first (225 complete, 17 partial,
reported separately and explicitly not comparable).

## 4. The result that matters, and it is negative

```
                        score    rank ignoring the gate
Hubbell Spring  NEGATIVE  0.734        14 / 1327
Sandia fault    POSITIVE  0.545       148 / 1327
```

**The four scoring legs separate the two controls by 0.19 in the wrong direction.** Age,
slip rate, junction density and structural scale — the entire ranking apparatus — put the
known negative near the top and the known positive in the middle of the pack. Every bit of
discriminating power in this screen currently lives in the single lithology gate, and that
gate is binary with ±0.125 of sampling noise on the quantity behind it.

So the top-25 table is **not evidence** and must not ship as a candidate list. What it is:
the first version of this screen whose population is complete (1399/1399) and whose
calibration can actually speak. Before today the gate leg had ten holes in it, so the
controls had nothing to say.

**Open, in order:**
1. The ranker needs legs that discriminate the controls. Junction density is the one that
   survived Addendum 3's deflation at Sandia and it is currently saturated (1.00 for both
   controls) — a saturated carrier passes every reachability test and carries no bits.
2. `n=2` controls cannot validate a ranker. Needs a larger labelled set, or the honest
   admission that this screen is a filter with no ranking capacity at all.
3. GPS strain at 1.5% is the leg most worth widening — 5 of 6 measured survivors read
   STRAINING.
