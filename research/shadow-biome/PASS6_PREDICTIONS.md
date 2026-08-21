# PASS 6 — PRE-REGISTERED PREDICTIONS

**Written and committed BEFORE `measure_pass6.py` was run and before any pass-6
number existed.** Governed by `PREREGISTRATION.md`. Every threshold in the
measurement script is copied from this file, not chosen while looking at output.

Day 201 / 2026-08-20, ~23:0x local.

---

## 0. What pass 5 left, stated so pass 6 cannot quietly move the target

Pass 5 established, on 20 ZTF difference images from 2018-06-01, 8,528
detections, no shape cut:

- **48.50%** of detections lie past ZTF's `elong <= 1.6` packaging cut.
- That fraction is **flat to S/N >= 100** — so it is not a low-S/N noise skirt.
- `R' = 1.3870` against 0.2408 on the packaged alert stream.
- The far side is **fainter**, not brighter (median peak 493.7 vs 569.4) —
  which refuted P6 of pass 5.

Pass 5 established **REACHABLE + LARGE + NOT-NOISE**. It established **nothing
about anomaly**, and `PASS5_PREDICTIONS.md` said the count was not the
interesting quantity before the data existed.

**The obvious hostile reading of pass 5, which pass 6 exists to test:** the far
side is instrumental — bleed trails off saturated stars, satellite and asteroid
streaks, cosmic rays, bad columns, subtraction residuals along the detector
grid. All of these are elongated. All of these are exactly what a shape cut at
1.6 is *for*. If that reading is right, ZTF's cut is a good cut, the far side is
junk, and the interesting quantity is zero.

**This pass is built to make that reading win if it can.** The three shape tests
below all have the sign that would kill the result set as their predicted
direction.

## 0.1 The forbidden move, restated

In writing since `0ae03d9`: **a null in the device-detectable branch STAYS in
that branch.** If pass 6 says the far side is instrumental, that is a null about
ZTF difference images. It may not be reframed as "consistent with" the
undetectable branch. It may not be reframed at all.

---

## 1. Fixed parameters — copied into the script, not chosen at runtime

| name | value | why |
|---|---|---|
| images | the 20 already in `diffimg/` | no download; identical set to pass 5 |
| `THRESH_SIG` | 5.0 | pass 5 §1.3, unchanged |
| `MINAREA` | 5 | pass 5 §1.3, unchanged |
| `MATCH_PX` | 2.0 | pass 5 §1.4, unchanged |
| wall | elong > 1.6 = "far side", <= 1.6 = "kept side" | ZTF's own cut |
| axis window | +/- 10 deg of 0 deg or 90 deg in PIXEL coords | chance rate = 40/180 = **22.22%** |
| bright percentile | 95th percentile of `peak` within a frame | defines "bright source" |
| neighbour radius | 100 px | for the collinearity test |
| S/N | `peak / bkg.globalrms`, as in `diag_pass5.py` | same instrument as pass 5 |

**Why effect sizes and not p-values.** At n ~ 4,000 a Rayleigh test returns a
vanishing p for a resultant length R of 0.03. Every test below is therefore
scored on a **pre-committed effect size**, and every one is scored **against the
kept side measured the same way**, so that any bias my own extractor has —
including pixel-grid quantisation of `theta` for near-minimum-area objects —
is present on both sides of the comparison and cancels.

**Angles are axial, not vectorial.** An elongation direction is defined mod
180 deg. All circular statistics are computed on **2*theta**, which is the only
correct treatment; a Rayleigh test on raw theta is meaningless here.

---

## 2. THE SHAPE TESTS — is the far side instrumental?

### P1 — axis alignment (bleed trails, bad columns, grid residuals)
Fraction of far-side detections with `theta` within +/-10 deg of the pixel axes.
Chance = 22.22%.

> **PREDICT: far side is between 22% and 40%, AND exceeds the kept side by
> >= 5 percentage points.**

Reasoning stated in advance: ZTF's P48 is a **Schmidt** — no secondary spider,
so no classic four-pronged diffraction spikes. But saturated stars bleed along
**columns**, and difference imaging leaves grid-aligned residuals. I expect a
real axis excess and I expect it to be a minority. If the far side comes back
**above 40%** the instrumental reading wins outright. If it comes back at chance
with **no** excess over the kept side, my stated mechanism is wrong and I say so.

### P2 — streak collinearity (satellites, asteroids, cosmic rays)
For each detection, the angle to its nearest same-side neighbour within 100 px,
compared against its own `theta`. A streak fragmented into several detections
has its elongation **pointing along the chain**. Statistic: median `|delta|`,
folded to [0, 90]. Uniform expectation = **45 deg**.

> **PREDICT: far-side median |delta| < 40 deg, AND at least 3 deg below the
> kept-side median.**

This is the test I trust most: it is immune to pixel-grid quantisation, because
grid quantisation aligns `theta` to axes without aligning it to a *neighbour
direction*.

### P3 — bright-source proximity (spikes, halos, saturation residuals)
Median distance from each detection to the nearest bright (>= 95th pct `peak`)
detection in the same frame, far side vs kept side.

> **PREDICT: ratio (far / kept) < 0.90 — the far side sits closer to bright
> things.**

### P4 — per-frame heterogeneity
Far-side fraction computed per frame; report the interquartile range.

> **PREDICT: IQR > 0.10.** A single uniform astrophysical population should not
> swing frame to frame; seeing, tracking error, moon and star density should.

---

## 3. THE 41% — explain pass 5's own flagged weakness

Pass 5 recovered **223 of 376** of ZTF's own alerts (59.31%) and gave **no
account** of the missing 41%. It was flagged in the handoff as the thing most
likely to be quietly wrong. Every unrecovered alert is now classified.

### P5 — the misses are faint
> **PREDICT: median `magpsf` of unrecovered exceeds recovered by >= 0.5 mag.**

### P6 — the misses are not a geometry bug
> **PREDICT: < 10% of unrecovered alerts are out of image bounds or land on a
> masked/non-finite pixel.**

If this is REFUTED the coordinate convention is wrong and **pass 5's control,
and therefore every pass-5 number, is in question.** This is the prediction
whose failure costs the most, which is why it is stated.

### P7 — the misses are my threshold, not my matcher
Local peak S/N in a 5x5 box at the alert position on my background-subtracted
image.
> **PREDICT: >= 60% of unrecovered alerts have local peak S/N < 5.0** — i.e.
> they are below the threshold I chose, not mismatched by the 2 px radius.

### P8 — recovery is high where it should be
> **PREDICT: recovery in the brightest `magpsf` tercile >= 80%.**

**The consequence, stated now so it cannot be constructed later.** If P5, P7 and
P8 all hold, my extractor's completeness **falls with faintness** — and pass 5
already measured the far side as **fainter** than the kept side. Then 48.50% is
a **floor, not a ceiling**, and the honest correction moves my headline number
*up*. I am writing that down before I know the answer specifically because it
flatters the result, and a flattering inference constructed after the fact is
worth nothing.

---

## 4. CONTROLS — the tests must be shown able to return both answers

A gauge that has only ever rendered one verdict is furniture. Each runs on
synthetic data with a known answer, and **all three must pass or Section 2 is
reported as UNINTERPRETABLE.**

- **C1 (can detect alignment):** n=1000 angles from a von Mises on 2*theta at
  kappa=2. Require resultant `R > 0.30`.
- **C2 (does not false-alarm):** n=1000 uniform angles. Require `R < 0.10`.
- **C3 (can detect collinearity):** 200 points on a straight line, each with
  `theta` along that line, run through the *actual* P2 code path. Require
  median `|delta| < 10 deg`.

C3 in particular is run through the same function that scores P2 — not a
reimplementation — so it tests the instrument rather than a copy of it.

---

## 5. What pass 6 cannot say, whatever it returns

- Nothing about **RA/Dec** or sky position; this is all pixel-frame.
- Nothing about ZTF's **packaging** decision. Every number is `sep` at 5 sigma
  on ZTF's pixels, not a statement about what IPAC would have alerted on.
- Nothing about **anomaly**, in either direction. A far side that is 100%
  instrumental means ZTF's cut is well-chosen. A far side that is not
  instrumental means there is an unexamined population, and "unexamined" is
  the entire claim — no more.
- One night, 20 images, 15 zr / 5 zg by the selection rule rather than by
  design. Replication across years is deferred on **measured** cost
  (2019: 8.85 GB, 2022: 14.9 GB, 2026: 9.89 GB by HTTP HEAD) and prefix
  sampling is ruled out (member-order vs jd Spearman rho = 0.977).
