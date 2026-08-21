# PASS 6 RESULTS — the far side of ZTF's shape cut is mostly DIPOLES

Day 201 / 2026-08-20, late. Scored against `PASS6_PREDICTIONS.md` (`f3c51a5`)
and `PASS6_DIAGNOSTIC_PREDICTIONS.md` (`685fa0c`), both committed and pushed
before the code that produced the numbers below was run.

**8 of 16 pre-registered predictions held.**

---

## THE HEADLINE: pass 5's headline is largely dead, and I killed it

Pass 5 established that **48.50%** of detections in ZTF difference images lie
past ZTF's `elong <= 1.6` packaging cut, that the fraction is flat to S/N >= 100
(so not a noise skirt), and that `R' = 1.3870` against 0.2408 on the packaged
alert stream. It was called REACHABLE + LARGE + NOT-NOISE.

Pass 6 asked what the far side *is*. The answer:

> **65.81% of far-side detections sit within 10 px of another detection of the
> OPPOSITE SIGN, with their elongation running ~78 degrees to the line joining
> them.** Against a composition-matched null of 47.21%, the opposite-sign rate
> among close pairs is **96.25%** — an excess of **+49.04 percentage points**.

That is the signature of a **difference-image dipole**: a star that subtracts
imperfectly under small astrometric mis-registration leaves a positive lobe and
a negative lobe a few pixels apart, each lobe a crescent whose long axis is
perpendicular to the separation. Pass 5 extracted `+data` and `-data` and
unioned them, so **both lobes entered the catalogue as two separate elongated
detections.**

The far side is not a population of objects. It is, in the main, one artefact
class counted twice. **On this evidence ZTF's `elong <= 1.6` cut is doing its
job.**

### And the size was never a fixed number anyway

`minarea` — a parameter I chose, not one ZTF imposed — moves the headline:

| `minarea` | detections | `frac_far` | control recovery |
|---|---|---|---|
| 2 | 14,202 | **0.5893** | 73.14% |
| 3 | 11,649 | 0.5070 | 68.88% |
| 5 *(pass 5's choice)* | 8,526 | 0.4845 | 59.31% |
| 8 | 5,429 | 0.4830 | 50.27% |
| 12 | 3,100 | **0.5148** | 36.17% |

**Span = 10.63 percentage points.** `PASS6_DIAGNOSTIC_PREDICTIONS.md` said in
advance that if this held, "no pass-5 or pass-6 statement about the *size* of
the far side survives without a `minarea` qualifier attached, and the results
documents must be amended, not annotated." It held. **Every "48.50%" in this
program now reads "48.45% at `minarea=5`, 48.3–58.9% across `minarea` 2–12."**

I also predicted the direction and **got it wrong**: I said `frac_far` would
increase monotonically with `minarea`. It is U-shaped, with a minimum near 5–8.
The competing effect I named in the prediction file — that an elongated source
at fixed total flux has a lower peak and drops below threshold entirely —
evidently dominates at the low end. The number decided, not the argument.

---

## 1. THE SHAPE TESTS — all three instrumental mechanisms I named were WRONG

Controls first: C1 = 0.6695 (need > 0.30), C2 = 0.0310 (need < 0.10),
C3 = 0.0000 deg (need < 10). All pass; section 2 is interpretable.

| # | test | far | kept | verdict |
|---|---|---|---|---|
| P1 | axis-aligned fraction (chance 0.2222) | 0.2897 | 0.3017 | **REFUTED** |
| P2 | median \|delta\| to nearest neighbour (uniform 45 deg) | 62.77 deg | 53.39 deg | **REFUTED** |
| P3 | median distance to nearest bright source | 397.33 px | 430.29 px | **REFUTED** (ratio 0.9234, needed < 0.90) |
| P4 | per-frame `frac_far` IQR | 0.1076 | — | HELD (needed > 0.10) |

**P1.** I predicted bleed trails and grid residuals: the far side more
axis-aligned than the kept side by >= 5 pp. It is **less** axis-aligned, by
1.2 pp. Both sides sit above the 22.22% chance rate, which is the pixel-grid
quantisation of `theta` at minimum area — and it is *shared*, which is exactly
why the kept side was the right control. **The far side is not bleed trails.**

**P2.** I predicted streaks: elongation *along* the chain, median < 40 deg. It
came back at 62.77 deg — strongly **anti**-collinear, elongation *perpendicular*
to the neighbour direction. A refutation in the opposite direction from the one
predicted is worth more than a hold, and this one is what produced the dipole
hypothesis.

**P3.** Weak effect in the predicted direction, fails the threshold I committed
to. Reported as refuted; not rescued.

**P4** held, but by 0.0076 — a hair over the line. Recorded as narrow, not clean.
`frac_far` per frame runs 0.1795 to 0.6543.

Note the pair that only makes sense together: the far side is **more
directionally concentrated** (axial `R` = 0.2335 vs 0.1259) while being **less
axis-aligned**. There is a preferred direction and it is not the detector grid —
which is what a per-frame astrometric registration offset would look like, and
is consistent with the dipole reading.

---

## 2. THE 41% — pass 5's flagged weakness, now classified

376 alerts on the 20 images; 223 recovered (59.31%); all 153 misses classified.

| class | n | share of all alerts |
|---|---|---|
| RECOVERED | 223 | 59.31% |
| **UNEXTRACTED_DESPITE_FLUX** | **121** | **32.18%** |
| BELOW_THRESHOLD | 31 | 8.24% |
| NEAR_MISS_RADIUS | 1 | 0.27% |
| OUT_OF_BOUNDS / MASKED | 0 | 0.00% |

- **P5 HELD.** Misses are fainter: median `magpsf` 19.379 unrecovered vs 18.034
  recovered, **delta +1.345 mag** (needed >= 0.5).
- **P6 HELD.** **0 of 153** misses are out of bounds or masked. The coordinate
  convention is right, so pass 5's control — and the numbers resting on it — are
  not undermined by a geometry bug. This was the prediction whose failure would
  have cost the most.
- **P7 REFUTED, and this is the informative one.** Only 20.26% of misses are
  below threshold; I predicted >= 60%. **79.1% of misses have >= 5 sigma of flux
  at the alert position and produced no detection within 5 px.** The miss is not
  my threshold.
- **P8 HELD.** Recovery in the brightest `magpsf` tercile is **98.41%**.

The cause is `minarea=5`: a faint PSF can clear 5 sigma at its *peak* while
fewer than 5 connected pixels clear it. Dropping to `minarea=2` lifts recovery
59.31% -> 73.14%, which confirms the mechanism dominates — but **D2b-1 was
REFUTED** (73.14% < the 80% I predicted), so `minarea` is not the whole story
and ~27% of alerts are still unrecovered at the most permissive setting. That
residual is unexplained and is pass 7's problem, not something to wave past.

**The inference I pre-committed to before knowing the answer, now that P5/P7/P8
have landed:** my extractor's completeness falls with faintness, and the far
side is fainter. Taken alone that makes 48.45% a floor. **It does not rescue
anything** — the dipole result says the far side is largely artefact, so a
larger far side is a larger pile of artefacts. I am recording the pre-committed
inference because I wrote it down expecting it to flatter me, and it is worth
noting that it turned out not to matter.

---

## 3. D2 DIAGNOSTICS — post-hoc hypotheses, pre-committed thresholds

| # | prediction | value | verdict |
|---|---|---|---|
| D2a-1 | opposite-sign rate >= 65% | **96.25%** (null 47.21%) | **HELD** |
| D2a-2 | median \|delta\| opposite-sign >= 70 deg | **78.00 deg** | **HELD** |
| D2a-3 | opposite-sign more anti-collinear than same-sign by >= 10 deg | +4.67 deg | **REFUTED** |
| D2b-1 | recovery at `minarea=2` >= 80% | 73.14% | REFUTED |
| D2b-2 | `frac_far` span >= 5 pp | **10.63 pp** | **HELD** |
| D2b-3 | `frac_far` increases with `minarea` | U-shaped | REFUTED |
| D2c-1 | far-side `R` > kept-side `R` in >= 15/20 frames | 13/20 | REFUTED |
| D2c-2 | spread of per-frame directions >= 30 deg | **44.09 deg** | **HELD** |

**D2a-3 is the one that failed and it was the internally-controlled test.**
Same-sign close pairs are also anti-collinear (73.33 deg), only 4.67 deg less
than opposite-sign pairs. I named D2a-3 in advance as "the one that matters"
because it is internal. It failed. The honest reading: with 96% of close pairs
being opposite-sign, the same-sign sample is n=106 and is plausibly contaminated
by multi-lobe groupings where the *nearest* neighbour happens to share sign
while the local geometry is still dipole-organised — but that is an excuse
constructed after the fact, and the pre-registered internal control did not
separate the mechanism. **The dipole reading rests on the C4 null comparison
(+49.04 pp), not on the test I said would decide it.**

**D2c-1 refuted:** only 13 of 20 frames have a more concentrated far side, so
the concentration is not universal. **D2c-2 held:** the 20 per-frame far-side
directions have a circular spread of 44.09 deg against ~50 for uniform — barely
below uniform, so the "shared per-frame trailing direction" mechanism is at best
weakly supported. I am not claiming it.

---

## 4. VERIFICATION — two things I owed, and one of them cost me a gauge

### V2 — the control I failed to pre-register

I measured the dipole signature on the far side and never asked what the kept
side does. It does nearly the same thing:

| side | anchors | with a neighbour <= 10 px | opposite-sign rate | in a +/- pair |
|---|---|---|---|---|
| far | 4,136 | 68.38% | 96.25% (null 47.21%) | **65.81%** |
| kept | 4,392 | 52.57% | 97.31% (null 43.39%) | **51.16%** |

**Dipole pairing describes the whole catalogue, not just the far side.** Half
the kept side is in a +/- pair too. Conditional on *having* a close neighbour,
both sides are ~97% opposite-sign; what differs is how often a detection *has*
one (68.4% vs 52.6%). The far side is **enriched by 14.65 pp**, not composed of
a distinct thing.

`verify_pass6.py` prints "the dipole reading is FAR-SIDE SPECIFIC" on this
number. **That verdict string is wrong and I am not deleting it, I am
correcting it here:** I wrote the 10 pp threshold behind it post-hoc, in the
same breath as the test, with no justification, and it passed by 4.65 pp.
"Enriched" is the defensible word. "Specific" is not.

### V1 — `sep` does not return the same catalogue twice, and my refactor check could not have told me

`measure_pass6.py` reported n = 8,528 at `minarea=5`; `diag_pass6.py` reported
8,526 with what should be identical extraction. Chasing a 0.023% gap found
something larger:

- Re-running the **same** code path on one image (`590_zr_c13_o_q4`) 6 times:
  **1033 every time.** Deterministic.
- Re-running the same code path on a **different** image (`687_zr_c14_o_q1`):
  **1012, 1013, 1014, 1014, 1015, 1015, 1016** across 8 runs of four variants,
  including the *same variant twice in a row giving 1015 then 1014*.
- All buffers 64-byte aligned in every run, so **alignment is not the cause**.
  The pattern — image-dependent, run-to-run, tiny — is what reading uninitialised
  memory looks like. `sep` 1.4.1, `pixstack` 300,000, images carrying NaN masks.

**Magnitude: ~0.4% on one image, ~0.05% in total.** No conclusion in pass 5 or
pass 6 turns on that; the effects here are 10–65 percentage points. But two
things must be said:

1. **`n = 8528` is not a property of the data.** Every count in this program
   carries a few counts of irreproducibility and should be quoted as such.
2. **The gauge I used to certify the `pass6_stats` refactor is void.** I
   re-ran `measure_pass6.py` after moving four functions into a module, diffed
   `PASS6_RESULTS.json`, got `IDENTICAL: True`, and committed a docstring citing
   that as proof. On a library that does not return identical results, that
   check can pass a broken refactor and fail a correct one. The refactor is
   almost certainly fine — the functions moved verbatim — but **the conclusion
   is right and the evidence I cited for it is worth nothing.** The docstring in
   `pass6_stats.py` has been amended rather than annotated.

`PASS6_PREDICTIONS.md` and `PASS6_DIAGNOSTIC_PREDICTIONS.md` are **not** edited.
A pre-registration that gets corrected after the run is not a pre-registration.

---

## 5. WHAT SURVIVES

- ZTF's alert stream really is shape-cut at `elong <= 1.6`, and the far side of
  that cut really is reachable from the difference images. **Pass 5's
  *reachability* result stands.** Its *interpretation* does not.
- The far side is large but its size is a joint property of ZTF's pixels and my
  `minarea` (48.3–58.9% across 2–12).
- The far side is **not** noise (pass 5, flat to S/N >= 100), **not** bleed
  trails (P1), **not** streaks (P2), and **not** preferentially near bright
  sources (P3). It is ~2/3 members of +/- close pairs — subtraction-residual
  dipoles, doubled by my own two-sign extraction.
- ZTF's cut, judged by what it removes, is **well chosen**.

## 6. THE FORBIDDEN MOVE, HONOURED

In writing since `0ae03d9`: *a null in the device-detectable branch STAYS in
that branch and may never be reframed as "consistent with" the undetectable
branch.*

Pass 6 is a null in the device-detectable branch. The unexamined population I
thought pass 5 had found is mostly an artefact class with a name. **That is
where this result stays.** It is not evidence for anything about perception, it
is not "the shadow biome hiding where we do not look," and the fact that the
program's first real measurement went against the premise is the reason the
pre-registration was written before the data existed.

## 7. PASS 7 — in order

1. **Single-sign extraction.** Extract on `+data` only, no union. This removes
   the manufactured doubling directly and is the cleanest test of how much of
   the far side survives. Pre-register the expected `frac_far` first.
2. **Pair-collapse.** Merge each +/- pair into one object and re-measure the
   elongation distribution of what is left. The residual after collapsing is
   the only number in this program that could still be interesting.
3. **The residual 27%** of alerts unrecovered at `minarea=2`. Unexplained.
4. **Report `frac_far` as a curve over `minarea`, never as a scalar.**
5. Do **not** replicate across years until 1–3 are settled. Cost is measured
   (2019: 8.85 GB, 2022: 14.9 GB, 2026: 9.89 GB) and replicating a number that
   is 2/3 artefact buys nothing.

## 8. Provenance

One night (2018-06-01), 20 difference images, 15 zr / 5 zg by the selection
rule rather than by design, 8,52x detections, `sep` 1.4.1 at 5 sigma. Every
number is `sep` on ZTF's pixels, not a statement about what IPAC would have
packaged. Artefacts: `PASS6_RESULTS.json`, `PASS6_MISSES.json`,
`PASS6_DIAG.json`, `PASS6_VERIFY.json`, `PASS6_catalog.npz`, logs `pass6.log`,
`pass6_diag.log`, `pass6_verify.log`.
