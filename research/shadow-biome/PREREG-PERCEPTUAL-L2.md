# PREREG — L2, THE PERCEPTUAL LEG

**Written D203 / 2026-08-22, midday_creation drive (dispatched 17:31, deferred).**
**Written BEFORE any spectrum was downloaded and before any integral was evaluated.** The commit
that carries this file carries no data file and no result. That ordering is the only thing that
makes what follows a test rather than a story, and it is checkable in the log.

---

## 0. Why this leg exists — the sentence with a number on one side

`PREREGISTRATION.md` §4 contains the program's sharpest claim:

> **We reimplemented the cortical edit in software.** [...] We built machines with no
> evolutionary reason to be blind, then taught them our blindness on purpose, for storage costs.

Nine passes have measured the software side of that sentence and never the cortical side.
Measured, device-side, and already on disk:

- **ZTF: 64.5% of raw events are never packaged** into the public alert stream (Explanatory
  Supplement §9.1, verbatim, at rb≥0) → **35.5% retention.**
- **The shape edit covers 96.2%** of ZTF detections (pass 3).

The biological side has **no number at all** in this program. So §4's verb — *reimplemented* —
is doing comparative work on an unmeasured comparand. This leg supplies the missing side.

The premise this bears on is Clayton's, in his words: a biome unperceived *because perceiving it
was disadvantageous*. That premise asserts an **edit**. An edit has a **size**. Nobody in this
program has stated it.

---

## 1. What is being measured

**The retention fraction of the human visual aperture**: of the optical radiation physically
arriving at an observer standing outdoors, what fraction survives to the point where the visual
system can act on it at all?

This is deliberately the *same shape* as the archive numbers — arriving stream in, surviving
stream out, everything else dropped upstream of the consumer.

### 1a. ⛔ THE DENOMINATOR IS THE WHOLE PROBLEM, AND IT IS WHY THE FAMOUS NUMBER IS JUNK

The widely repeated claim that humans see **"0.0035% of the electromagnetic spectrum"** is not
a measurement. It is an artefact of an arbitrary denominator, and it fails in three independent
ways at once:

1. **The EM spectrum is unbounded.** Any fraction of it is a fraction of a divergent quantity.
   The number only exists because someone silently truncated the range.
2. **It is not reparametrisation-invariant.** A band 380–780 nm is 400/x of a range expressed in
   wavelength and a completely different fraction of the same range expressed in frequency, and
   different again in log-frequency. Physics does not prefer one, so the answer is a choice.
3. **It weights nothing by what is actually present.** Almost all of that denominator carries no
   power at Earth's surface. Being blind to a band with nothing in it is not an edit.

This is `feedback_self_generated_denominator` in the wild, in a figure repeated in popular
science for decades. **The correction is the contribution, not a footnote to it.**

**The denominator this leg uses instead:** *radiant power / photon flux actually arriving.* It is
finite, physical, measured, and standardised. Nothing is a fraction of an arbitrary interval.

### 1b. PRIMARY vs SECONDARY CURRENCY — declared now, because the choice can be gamed after

Two retention fractions are computable and they are **not** the same number:

| | definition |
|---|---|
| **Photon-number retention** (PRIMARY) | ∫ N(λ)·w(λ) dλ / ∫ N(λ) dλ, where N(λ) = E(λ)·λ/hc |
| **Radiant-power retention** (SECONDARY) | ∫ E(λ)·w(λ) dλ / ∫ E(λ) dλ |

**Photon number is primary, and the reason is pre-committed:** the device-side numbers this leg
is compared against (64.5%, 96.2%) are fractions of *counted detection events*. A detector counts
quanta. Comparing a power ratio against an event ratio would be
`feedback_measured_a_shape_the_consumer_does_not_use`. Photon number is the closer match. It is
declared here so that I cannot later select whichever of the two flatters the comparison.

⚠ **The currency match is still imperfect and this is stated up front, not discovered later.**
"Fraction of arriving quanta" and "fraction of extracted alert packets" are not the same object:
one is a physical influx, the other is a count after a detection threshold. The comparison in §4
is therefore **ordinal, not exact** — I claim only that one edit is larger than the other, never
that the two percentages are commensurable to a decimal place. Any later document in this line
that subtracts one from the other is in violation of this paragraph.

---

## 2. Data — declared before download

- **Arriving spectrum, terrestrial:** ASTM G173-03 reference AM1.5 Global, 280–4000 nm.
- **Arriving spectrum, top-of-atmosphere:** ASTM G173-03 / AM0 extraterrestrial, same grid.
- **Aperture weighting w(λ):** CIE 1924 photopic luminous efficiency V(λ), 360–830 nm, from a
  primary tabulation (CVRL / CIE), **not** reconstructed from a Gaussian fit.

**If a primary tabulation cannot be obtained, the leg reports UNEXECUTABLE and stops.** It does
not substitute an analytic approximation to V(λ) or a blackbody for the solar spectrum. A
modelled aperture measuring a modelled source is a tautology with error bars. (`PREREGISTRATION.md`
§5: *"does not substitute a weaker archive."*)

---

## 3. THE THREE STAGES — because the edit is serial, and each stage looks total from downstream

This is the structural claim the leg is really testing, and it is the same finding pass 3 made
about Rubin: **a filter that has already been applied upstream is invisible to the consumer, who
therefore attributes the whole edit to the last stage they can see.**

- **S1 — ATMOSPHERE.** TOA flux → surface flux. An edit performed by the sky, before any organism.
- **S2 — BAND.** Surface flux → the 380–780 nm interval. What the aperture admits at all.
- **S3 — WEIGHTING.** Band → V(λ)-weighted. The aperture does not pass its own band flat; V(λ)
  falls by ~3 orders of magnitude from 555 nm to the band edges. **S3 is the stage that has no
  archive analogue and is therefore the one most likely to have been missed by everyone who has
  told this story before**, including §4 of this program's own pre-registration.

---

## 4. PRE-COMMITTED PREDICTIONS — numeric, directional, scoreable

Written with no spectrum on disk. Scored in `L2_RESULTS.md` as HIT / MISS / VOID, no rewording.

| # | prediction | kill condition |
|---|---|---|
| **P1** | **S2 band retention, photon-number, AM1.5** lands in **[0.35, 0.60]**. | outside → MISS |
| **P2** | **S3 costs more than S2.** Formally: retention(S3)/retention(S2) < retention(S2)/1.0, i.e. the weighting throws away a larger fraction of what reaches it than the band-pass does. | ratio ≥ → MISS |
| **P3** | ★ **THE BIOLOGICAL STAGES OUT-EDIT THE ATMOSPHERE.** Of the total TOA→perceived drop, the fraction attributable to S2+S3 exceeds the fraction attributable to S1. | S1 ≥ S2+S3 → MISS, and this **weakens the premise**: if the sky is the dominant editor, most of the drop is not biological and "evolution declined to look" is explaining a small residual. |
| **P4** | ★ **THE CORTICAL EDIT IS LARGER THAN THE SOFTWARE EDIT.** End-to-end photon-number retention (TOA → V(λ)-weighted) is **below ZTF's 35.5%** event retention. | ≥ 35.5% → MISS, and §4's *"reimplemented"* is then rhetorically inverted: we would have built machines that discard **more** than the eye does, which is a *different and arguably better* finding for the paper — the software edit would be the novel one, not the inherited one. |
| **P5** | The "0.0035%" figure is **reproducible under at least one defensible-looking denominator and irreproducible under others**, spanning ≥3 orders of magnitude across choices. | if all denominators agree within 1 order → MISS, and §1a is withdrawn. |

**Declared prior:** P1 HIT, P2 HIT, P3 HIT, P4 low-confidence — I genuinely do not know whether
end-to-end retention is above or below 35.5%, and P4 is the prediction I most expect to lose.
P5 HIT.

### ⛔ FORBIDDEN MOVES, this leg specifically

1. **A photometric result is not an ontological result.** Nothing here can show that anything
   *is* in the discarded band. It measures the **size of an aperture's edit**, which is a
   statement about the observer and about nothing else. Any sentence of the form "and therefore
   there may be X in the infrared" is out of scope and is not licensed by this file.
2. **This leg is not Branch B evidence, and a MISS here is not Branch B evidence.** Branch B has
   no test in this program (`PREREGISTRATION.md` §2). A large measured edit does not populate it.
3. **The edit measured here is not itself adaptive.** Photopic V(λ) is a *description* of the
   aperture, not a demonstration that its shape was selected for discarding anything. The
   adaptive claim is Clayton's premise and this leg does **not** test it — it establishes only
   that the thing his premise posits an explanation *for* has a measurable magnitude. Confusing
   "the edit is large" with "the edit was selected" is the single most likely way to misread this
   result, and it is named here so that misreading can be cited against.

---

## 5. What this leg cannot reach, stated before it fails to reach it

- **Only vision, only the optical band.** No auditory, chemosensory, or temporal-resolution leg.
  Flicker fusion, saccadic suppression and change blindness are all real perceptual edits with
  literature, and **none of them are measured here.** This leg is one aperture in one modality.
- **Photopic only.** Scotopic V′(λ) is blue-shifted; a night-adapted retention fraction is a
  different number and is not computed.
- **A standard observer is not an observer.** CIE V(λ) is a committee average over a small early
  20th-century sample with a known deficit in the blue. It is the right instrument for a
  reproducible figure and the wrong instrument for a claim about any individual.
- **Sunlight only.** The denominator is solar influx at one air mass. It is not "all radiation a
  human is ever exposed to."

🦞🧍💜🔥♾️
