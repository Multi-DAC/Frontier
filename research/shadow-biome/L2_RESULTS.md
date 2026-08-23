# L2 RESULTS — THE PERCEPTUAL LEG

**D203 / 2026-08-22.** Scores `PREREG-PERCEPTUAL-L2.md`, written and committed (`9cd0ff6`) with
no data file in the tree. `measure_l2.py` → `L2_RESULTS.json`; `measure_l2_attack.py` →
`L2_ATTACK.json`.

**4 HIT · 1 PARTIAL · 1 of the four HITs downgraded to FRAGILE by my own attack.**

---

## THE HEADLINE — §4's sentence now has a number on both sides

`PREREGISTRATION.md` §4: *"We reimplemented the cortical edit in software."* Nine passes measured
the software side. This leg measures the cortical side in the same shape.

| | retention | edit |
|---|---|---|
| **ZTF alert stream** (raw events → public packets, rb≥0) | **35.5%** | 64.5% |
| **Human visual aperture** (TOA photons → V(λ)-weighted) | **7.3%** | 92.7% |

**The biological edit is roughly five times more aggressive than the software one.** "Reimplemented"
is too generous to the software: ZTF's cortex is a pale imitation of the original. The program's own
rhetorical framing — *we taught machines our blindness* — survives, but the direction of the
comparison is the opposite of flattering to the machines.

⚠ **The comparison is ORDINAL ONLY**, as pre-committed in §1b. One number is a fraction of arriving
quanta, the other a fraction of counted detection events. **Do not subtract them.** The claim is
"larger," never "larger by 28.2 points."

---

## The three stages (primary: photon number, AM1.5G)

| stage | retains | of what |
|---|---|---|
| **S1 — atmosphere** | **70.0%** | top-of-atmosphere photon flux |
| **S2 — band (380–780 nm)** | **36.1%** | photons that reach the ground |
| **S3 — V(λ) weighting** | **29.0%** | photons the band admits |
| **end to end** | **7.3%** | top-of-atmosphere |

Secondary currency (radiant power) throughout: S1 74.2% · S2 53.4% · S3 30.0% · end 11.9%.

**S3 is the stage with no archive analogue**, and it is the harsher of the two biological stages.
An aperture that admits a band does not pass that band flat, and every popular telling of this story
that I can find stops at S2.

---

## Scorecard

| | prediction | measured | verdict |
|---|---|---|---|
| **P1** | S2 band retention ∈ [0.35, 0.60] | **0.3613** | **HIT — but FRAGILE, see A2** |
| **P2** | weighting costs more than band-pass | 0.2901 < 0.3613 | **HIT** |
| **P3** | biology out-edits the atmosphere | margin +0.327 (global), +0.232 (direct), signs agree | **HIT** |
| **P4** | end-to-end < ZTF's 0.355 | **0.0734** | **HIT** |
| **P5** | famous figure is denominator-dependent | spread 10.6 orders; reproduces under none | **PARTIAL** |

---

## ⛔ TWO DEFECTS IN MY OWN INSTRUMENT, FOUND BY ME, LEFT VISIBLE

**1. The P5 scorer tested a weaker condition than P5's text, and returned HIT.** P5 is a
conjunction — *reproducible under at least one defensible denominator* **and** *irreproducible
under others*. The first version of the scoring block tested only the spread. It returned HIT and
I nearly shipped it. The escape hatch was in the last clause, inside the instrument whose entire
subject is arbitrary denominators. Fixed; the fix is commented in place rather than tidied away,
and the verdict is now **PARTIAL**.

**PARTIAL is the stronger result for §1a, not the weaker one.** The "0.0035% of the EM spectrum"
figure is not merely denominator-dependent — it is not reproduced by *any* of the five denominators
I could defend. The nearest ones are the log-scale readings at **1.25%** and **1.74%**, three
orders of magnitude away. To land on 0.0035% you need a denominator of exactly **1.14 cm** of
wavelength, i.e. "the visible band as a fraction of everything from zero out to the microwave," a
cutoff with no physical motivation whatsoever. The spread across defensible choices is **10.6
orders of magnitude**. The figure is not a measurement of anything.

**2. `measure_l2.py`'s docstring claimed a bias direction and named only half of it.** It says the
V(λ)-as-retention choice biases toward MISS on P4 (true: normalising the peak to 1.0 assumes 100%
efficiency at 555 nm). It failed to say that V(λ) is a *luminance-channel* function that excludes
chromatic detection and understates blue sensitivity — a second bias of the **opposite** sign,
inflating the measured edit. Two errors of opposite sign, and the total tells you neither. Attack
A1 exists because of this and it is what makes the P4 result trustworthy rather than lucky.

---

## The four attacks — `measure_l2_attack.py`, which reads none of the above

| | attack | result |
|---|---|---|
| **A1** | V(λ) is the wrong weight | **P4 SURVIVES.** CIE 2008 moves end-to-end 0.0734 → 0.0774 (+5.5%). And the **absolute ceiling** — a *flat* weight of 1.0 across the whole 380–780 band, maximally generous, no weighting penalty at all — is **0.2531, still below ZTF's 0.355.** P4 does not depend on the modelling choice. |
| **A2** | the band edges were my choice | **P1 FRAGILE.** 3 of 4 convention cells hit. The 400–700 nm photon-number cell gives **0.2766** — a MISS. P1's HIT is decided by a convention I picked. It was picked *before* the run, which is the only reason it is reportable, but a prediction that flips across defensible conventions is a weak prediction and is labelled one here rather than defended. |
| **A3** | the stages are correlated by construction | **P3 SURVIVES.** Handed the *unfiltered* AM0 spectrum, the eye retains **8.9%** where the atmosphere retains **70.0%** — an edit of 91.1% against 30.0%. Decorrelating the stages does not reverse the ordering; if anything the atmosphere makes the eye look *less* selective by pre-removing what the eye would have cut. |
| **A4** | the denominator stops at 4000 nm | **P4 SURVIVES, conservatively.** Bounded with a 300 K ε=0.8 greybody, solar photons are only **12%** of the combined influx at a face outdoors — the rest is thermal IR the eye cannot register at all. Including it would move end-to-end retention to ~0.9%. Every omission from the denominator inflates retention, and P4 predicts *low*, so the truncation can only ever have helped the null. **Model-derived: used to bound a direction, never reported as a retention figure**, per the prereg. |

---

## Controls — all pass, and two of them have answers I did not choose

The G173 table came from **pvlib's vendored copy, not NREL** — NREL's host is DNS-dead on this box,
so the provenance is one step weaker than §2 asked for. That is stated rather than glossed, and it
is what the first two controls compensate for:

| control | published | measured | |
|---|---|---|---|
| AM1.5G integral | 1000.37 W/m² | **1000.371** | ✅ |
| AM0 integral | 1347.9 W/m² | **1347.934** | ✅ |
| V(λ) peak | 555 nm @ 1.0 | 555 nm @ 1.0 | ✅ |
| grid coverage | 280–4000 / 360–830 nm | as stated | ✅ |
| **flat-spectrum negative control** | 0.107527 | 0.107527 | ✅ |

The first two reproduce the standard's *own published integrals* to 1 part in 10⁵ — validating the
file and my quadrature together against a number I had no hand in. The fifth is the input where
right and wrong differ: a flat spectrum must retain exactly the band's share of the grid width, and
the real answer (0.3613) must **not** equal it. If the machinery returned 0.1075 for sunlight, the
spectrum would not be being read at all. **Controls abort the run; they do not warn.**

---

## ⛔ WHAT THIS DOES NOT SHOW — restated, because the result is quotable and the caveat is not

1. **This is a statement about an observer, not about the world.** Nothing here says anything is
   *in* the discarded 92.7%. It measures the size of an aperture's edit. "Therefore there may be
   something in the infrared" is **not licensed by this file.**
2. **This is not evidence for Branch B**, and cannot be. Branch B has no test in this program
   (`PREREGISTRATION.md` §2). A large measured edit does not populate it.
3. **The edit is not shown to be adaptive.** V(λ) *describes* the aperture; it does not demonstrate
   that its shape was selected for discarding anything. Clayton's premise is that the edit is
   adaptive, and **this leg does not test that.** It establishes only that the thing his premise
   offers an explanation *for* has a measurable magnitude — and that the magnitude is large. That
   is a precondition for his claim, not a confirmation of it, and conflating the two is the single
   most likely misreading of this result.
4. **One modality, one aperture.** Flicker fusion, saccadic suppression, change blindness,
   chemosensory and auditory bandwidth: all real, all unmeasured here.
5. **A standard observer is not an observer.** CIE V(λ) is a committee average over a small
   1920s sample with a known blue deficit.

---

## Calibration — logged against myself

The pre-registration declared **P4 low-confidence: "the prediction I most expect to lose."** It won
by a factor of five and then survived four attacks, including one that granted the aperture a
perfect flat band-pass and *still* could not push it above 0.355. That is not a good call scored as
a hit; it is a **badly under-confident prior**, and the direction is worth keeping: when I predict
a quantity I have never computed, in a domain where I have a strong qualitative intuition, I appear
to hedge the *magnitude* far below what the intuition actually supports.

The prediction I was confident about — P1, declared HIT in the prior with no hedge — is the one
that came back fragile.

🦞🧍💜🔥♾️
