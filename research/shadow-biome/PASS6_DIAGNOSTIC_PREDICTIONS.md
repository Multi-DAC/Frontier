# PASS 6 DIAGNOSTICS — D2

**Written and committed BEFORE `diag_pass6.py` was run.** These test hypotheses
that are **POST-HOC** — they were formed by looking at the pass-6 results. That
is stated plainly here and will be stated in the results document. A post-hoc
hypothesis is worth something only if it is committed to a number before it is
tested, which is what this file is for.

Governed by `PREREGISTRATION.md`. Runs on `PASS6_catalog.npz` and the 20 images
already on disk. Downloads nothing.

---

## What produced these hypotheses

`measure_pass6.py` (results `PASS6_RESULTS.json`) returned 4/8. Three results
generated the questions below:

1. **P2 refuted in the opposite direction.** I predicted the far side would be
   *collinear* with its neighbours (streaks): median `|delta| < 40 deg`. It came
   back at **62.77 deg** against a uniform expectation of 45, with the kept side
   at 53.39. The far side is strongly **ANTI**-collinear: elongation runs
   *perpendicular* to the direction to the nearest neighbour.
2. **The far side is more directionally concentrated but LESS axis-aligned.**
   Axial `R` far = 0.2335 vs kept = 0.1259, yet axis-aligned fraction far =
   0.2897 vs kept = 0.3017. There is a preferred direction and it is **not** the
   pixel grid. Per frame the axis-aligned fraction runs 0.131 to 0.679 — one
   frame is concentrated *away* from the axes, another *on* them.
3. **The control miss is not a threshold effect.** Of 153 unrecovered alerts,
   only 31 (20.26%) had local peak S/N < 5. **121 (79.1%) had >= 5 sigma of flux
   at the alert position and produced no detection within 5 px.** P7 refuted.

---

## D2a — DIPOLES

**Hypothesis.** The anti-collinearity is difference-image **dipole residuals**.
A star that subtracts imperfectly under small astrometric mis-registration
leaves a **positive lobe and a negative lobe** a few pixels apart. Each lobe is a
crescent whose long axis is **perpendicular** to the separation between them.
Pass 5 extracted `+data` and `-data` and unioned them, so both lobes are in the
catalogue as separate detections. That produces exactly the observed signature:
nearest neighbour close, **opposite sign**, elongation ~90 deg to the pair axis.

It also predicts the pass-5 sign split, which was **+3694 / -4834**.

Among far-side detections whose nearest neighbour lies within **10 px**:

> **D2a-1: PREDICT >= 65% have a nearest neighbour of OPPOSITE sign.**
> **D2a-2: PREDICT their median `|delta|` >= 70 deg** (vs 45 uniform).
> **D2a-3: PREDICT the opposite-sign close pairs are more anti-collinear than
> the same-sign close pairs, by >= 10 deg.**

D2a-3 is the one that matters: it is internally controlled. If close pairs are
anti-collinear *regardless* of sign, the mechanism is not dipoles and I say so.

**If D2a holds, it is a finding AGAINST my own headline** — a large share of the
far side would be one astrophysical object counted twice as two artefacts.

## D2b — MINAREA: is 48.50% a property of ZTF, or of a parameter I chose?

**Hypothesis.** 121 alerts with visible flux and no detection is a **`minarea=5`**
effect, not a threshold effect: a faint PSF can have a 5-sigma *peak* while
fewer than 5 connected pixels clear 5 sigma. My local-S/N test used the max
pixel in a 5x5 box, so such a source passes "flux is there" and fails `minarea`.

**Why this attacks the headline directly.** `minarea` is a **shape-dependent**
selection and I applied it while measuring a shape distribution. At fixed peak
S/N an elongated source spreads flux over more pixels above threshold than a
compact one, so `minarea=5` should admit elongated sources preferentially. If
so, **48.50% is inflated by my own extraction parameter.**

Re-extract all 20 images at `minarea` in {2, 3, 5, 8, 12}, everything else
identical. Backgrounds computed once per image per sign and reused.

> **D2b-1: PREDICT control recovery at `minarea=2` >= 80%** (vs 59.31% at 5).
> **D2b-2: PREDICT `frac_far` moves by >= 5 percentage points across the
> ladder** — i.e. the headline is a function of a parameter I picked.
> **D2b-3: PREDICT `frac_far` INCREASES monotonically with `minarea`.**

D2b-3 is the direction claim and it is the one I could most easily be wrong
about; the competing effect is that an elongated source at fixed *total flux*
has a lower peak and can drop below 5 sigma entirely. I am predicting the
first effect dominates. **The number, not the argument, decides.**

**Stated before the run:** if D2b-2 holds, then no pass-5 or pass-6 statement
about the *size* of the far side survives without a `minarea` qualifier
attached, and the results documents must be amended, not annotated.

## D2c — is the preferred direction FRAME-SPECIFIC?

**Hypothesis.** The excess concentration with no axis preference is per-frame
**trailing** — tracking drift during the exposure elongates everything in one
direction, which differs frame to frame and washes out when pooled.

> **D2c-1: PREDICT far-side axial `R` exceeds kept-side `R` in >= 15 of 20
> frames.**
> **D2c-2: PREDICT the circular spread of the 20 per-frame mean axial
> directions is >= 30 deg** — i.e. the direction is not a fixed instrument axis.

If D2c-2 is REFUTED and all 20 frames share one direction, the cause is fixed
optics or the detector grid, not tracking, and D2c's stated mechanism is wrong.

---

## Controls

`measure_pass6.py`'s C1/C2/C3 passed (R = 0.6695 / 0.0310 / 0.0000 deg) and
`diag_pass6.py` reuses the **same** `collinearity` and `axial_R` functions by
import, not by copy, so those controls carry.

One control is added because D2a needs it:

- **C4 (sign-pairing has a null):** the opposite-sign rate among close pairs is
  compared against the rate expected from that frame's own sign composition,
  not against 50%. Pass 5's global split was 43.3% positive, so a naive 50%
  null would manufacture the result. Required: D2a-1 is scored against the
  **per-frame composition-matched** expectation and reported as an excess over
  it, not as a raw rate.

## The forbidden move, still in force

Every branch of this is about ZTF difference images and instrument behaviour.
A null here stays in the device-detectable branch. If the far side is largely
dipoles and `minarea` artefacts, then ZTF's `elong <= 1.6` cut is a **good cut**,
and pass 5's headline shrinks or dies. That outcome gets written in the same
font as the other one.
