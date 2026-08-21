# PASS 8 — RESULTS

**Run D202 / 2026-08-21 ~16:3x PT.** Governed by `PASS8_PREDICTIONS.md`, committed and pushed
(`6567f2b`) **before `measure_pass8.py` and `nondet_pass8.py` existed**. Artifacts:
`PASS8_RESULTS.json`, `PASS8_NONDET.json`, `DEFECT_REGISTER.json`, `pass8.log`, `pass8_nd.log`.

> ## **9 of 11 held. N3 and G2 refuted — and G2's refutation is void by my own R3 warning.**
> *(D1, D4, N-NULL and R4-CONTROL are excluded from the total per `PASS8_PREDICTIONS.md §5`.)*

---

## 1. ⭐ THE RULING: B2 IS RESOLVED, AND THE UNPAIRED NEGATIVES ARE REAL

`PASS7_RESULTS.md §2b` left `PAPER-00-ARCHITECTURE.md §8`'s amendment **provisional** until *"the
disagreement between the two procedures is resolved by a measurement rather than by an account."*
D4's decision rule was written before the number and fires:

| quantity | value |
|---|---|
| ZTF alerts on the 20 frames | **376**, all carrying `isdiffpos` |
| spellings observed | `'t'`, `'f'` — no others |
| **ZTF NEGATIVE alerts** | **240 (63.83%)** |
| ZTF POSITIVE alerts | 136 |
| **`r_neg`** — neg alerts landing on our 2505 unpaired negatives | **0.6417** |
| **`r_pos`** — pos alerts landing on our 1365 unpaired positives | **0.4118** |
| **gap** | **+22.990 pp**, against a threshold of ≥ **−10.0** |

**D3 HELD, and by 33 pp more than it needed to.** D6: the gap keeps its sign at **5 of 5** `minarea`
rungs (`+15.98 · +19.04 · +22.99 · +19.71 · +17.30`), so this is not a one-rung verdict.

**D5 HELD** — the junk hypothesis got its own shot and lost. Median distance to the nearest
top-decile-`peak` positive: unpaired negatives **367.0 px**, unpaired positives **281.9 px**, ratio
**1.302**. They are *farther* from bright sources, not huddled around them. They are not halo
residuals.

### ⚖ THE RULING, as pre-committed

> **The 2505 unpaired negatives are a ZTF-validated population. Pass 7(a) is CONFIRMED as the wrong
> operation. `PAPER-00-ARCHITECTURE.md §8`'s amendment (7b, 0.217 pp) is PROMOTED from PROVISIONAL
> to STANDING. B2's refutation is recorded as having caught a PLAN defect, not a measurement
> defect.**

⚠ **D2 is an observation about 20 frames of one night, n=376.** *"ZTF alerts more on fading than on
brightening"* is **not** licensed as an archive property, by the same rule that holds §12's 5.76%
reachability figure to n=55. What is licensed is narrower and sufficient: **on the frames this paper
measures, ZTF issues negative-difference alerts, and they land on the population 7(a) deleted.**

---

## 2. ⭐ POST-HOC, AND IT IS THE BIGGEST NUMBER IN THE PROGRAM — labelled, unscored, owed to pass 9

D3's ruling was about *unpaired negatives*. Reading the matched-only shares afterward exposes a
structure no prediction covered:

| | matched | on an **unpaired** detection | share | chance level |
|---|---|---|---|---|
| ZTF **negative** alerts | 167 | 154 | **92.22%** | 29.37% |
| ZTF **positive** alerts | 56 | 56 | **100.00%** | 16.01% |

> **ZTF alerts land on unpaired detections and essentially never on a member of a dipole pair.**

That is a statement about **both** signs, and it implies a de-doubling procedure that nobody in this
program has specified. Computed post-hoc:

| procedure | n | `frac_far` | move from union |
|---|---|---|---|
| union (pass 5/6) | 8528 | 0.484991 | — |
| **P_B** = 7(b), drop the `−` member of each pair | 6199 | 0.482820 | −0.217 pp |
| **P_A** = 7(a), `sign=+1` only | 3694 | 0.548728 | +6.374 pp |
| ⭐ **P_D = drop BOTH members of every mutual opposite pair** | **3870** | **0.422997** | **−6.199 pp** |
| *(the pair population alone)* | *4658* | *0.536496* | *+5.151 pp* |

**The mutual opposite-sign pairs are the elongated class**, 0.5365 against a catalogue 0.4850.
Removing the class outright is the largest move any procedure has produced.

⛔ **This does NOT un-refute `PAPER-00-ARCHITECTURE.md §8`'s original mechanism, and the distinction
is the whole point.** §8 said the far side was *"counted twice by pass 5's `+data`/`-data` union."*
**Counted twice is still refuted** — deleting one member of every pair moves `frac_far` by 0.217 pp,
exactly as pass 7 measured. What P_D shows is a **different claim in the same direction**: dipole
pairs are not a doubling artefact, they are an **elongated artefact class**. Those are not the same
sentence and the paper may not let the second quietly inherit the first's citation.

⚠ **P_D is post-hoc and is not scored.** It is the pass-9 debt: pre-register P_D's `frac_far` and its
`minarea` curve **before** re-deriving them, same discipline as the eight before it. Nothing in §1's
ruling depends on it.

---

## 3. D1 — THE OWED "THIRD PROCEDURE" DOES NOT EXIST, AS PREDICTED FROM READING THE CODE

`|P_A| = |P_C| = 3694`, identical **as a set**, `frac_far` equal to all printed digits (0.548728).
**D1 HOLDS.** The B2-resolution debt written into `PAPER-00-ARCHITECTURE.md §4 item 2a(i)` and
`PASS7_RESULTS.md §6` asked for a fork whose two arms are the two procedures that already disagree.

⭐ **The correction was derived by reading `measure_pass7.py:120-127` and published in the
pre-registration** (`PASS8_PREDICTIONS.md §1a`) **before the run confirmed it** — which is the only
order in which "I knew that already" is checkable. A filed repair is a hypothesis
(`feedback_filed_repair_is_a_hypothesis`); this one was priced against prose and was wrong.

---

## 4. ⭐ BLOCK N — THE FROZEN CATALOGUE IS ITSELF IN-PROCESS CONTAMINATED

`PASS7_RESULTS.md §5` measured `sep`'s behaviour on **one** image and explicitly refused to rewrite
§9a on it. This is the n=20.

**N1 HELD · N2 HELD · N3 REFUTED · N4 HELD · N5 HELD · N-NULL PASSED.**

| | result |
|---|---|
| images varying across **4 in-process** repeats | **11 of 20** |
| images varying across **3 fresh processes** (one image per process) | **0 of 20** |

⭐ **N2 is the load-bearing one and it held on every image.** Pass 7 §5's mechanism reproduces at
n=20: **the variation lives in repeated in-process calls; a fresh process is exactly reproducible.**
The docstring's named image, `687_zr_c14_o_q1`, gave in-process `1016·1015·1016·1013` — inside the
`pass6_stats.py` docstring's 1012–1016 to the digit — and fresh `1014·1014·1014`.

⛔ **N3 REFUTED, and it is the more useful refutation.** I registered in-process variation as a
*minority* phenomenon (<10 of 20). It is **11 of 20**. A majority.

### 4a. What that costs the numbers already published

`measure_pass6.py` looped all 20 images **in one process**. So did `diag_pass6.py`, and so did pass
7's A4 re-extraction. Three totals for the same quantity at `minarea=5`:

| source | structure | n |
|---|---|---|
| `PASS6_catalog.npz` (frozen catalogue) | one process, 20 images | **8528** |
| pass 7 A4 ladder | one process, 20 images × 5 rungs | **8526** |
| **pass 8, fresh process per image** | 20 processes | **8524** |

> **The frozen catalogue is not reproducible even in principle, because it was made in-process.**

The magnitude is small — 4 objects, 0.05% — and `frac_far` moves in the third decimal, which is
already below where `PAPER-00-ARCHITECTURE.md §9a` says the paper may round. **The correction is to
§9a's mechanism, not to any headline.** But §9a currently attributes the `PASS6_RESULTS` /
`PASS6_DIAG` 0.047 pp delta to *"run-to-run non-determinism"*, and on this evidence run-to-run
across **fresh** runs is exactly zero. The delta is **in-process drift plus structure**, which is a
different thing and a fixable one.

### 4b. N4/N5 — and a defect in my own pre-registration

**N4 HELD** (structures differ by 4 objects) and **N5 HELD** (structure M yields the higher
`frac_far`, 0.485218 vs 0.484272, matching the published sign of the delta).

⛔ **But `PASS8_PREDICTIONS.md §2`'s rationale for N4 is wrong about both scripts.** It says
`measure_pass6.py` computes the background *inside* the sign loop and `diag_pass6.py` *outside*.
**Both compute it inside the sign loop.** The real differences, read off the code and transcribed
verbatim into `_nd_child.py`:

1. `measure_pass6.py` makes an **extra `sep.Background(img)` call** (`bkg0`, for local S/N at alert
   positions) *before* the sign loop. `diag_pass6.py` makes none.
2. `diag_pass6.py` runs **five `sep.extract` calls** off one prepped array — the ladder — where
   `measure_pass6.py` runs one. Given N1/N2, **that repetition is itself the variation mechanism.**

**N4 is scored on the operation, which was implemented as the two scripts actually behave; its
stated rationale is struck.** The same false sentence is published in `PASS7_RESULTS.md §5` and in
`PAPER-00-ARCHITECTURE.md §4 item 2a(ii)` and is corrected in both. Entered in the register as
`DEF-10`.

---

## 5. BLOCK G — THE PATTERN CLAIM, AND A GAUGE THAT CAUGHT ITSELF

**R4-CONTROL FIRED.** Run against pass 7's reconstructed verdict set, R4 reported exactly one
collision: **`I1` and `I2`, both decided on the triple `('gauge_found', None, '==')`** —
`measure_pass7.py:352-353`. ⭐ **The new gauge was shown the known-bad input it was built for and it
caught it.** R4 on pass 8's own verdicts: **clean**.

**G1 HELD.** `DEFECT_REGISTER.json`, 12 rows across passes 4–8, each with a machine-checked
citation: **eye 9 · gauge 3**, ratio 3.0 against a threshold of 2.0. I2's standing rationale —
*"every instrument defect in this program so far was found by me, by hand, late"* — is now **counted
rather than asserted**, for the first time, and it survives.

⚠ **The register is self-assembled and the denominator is mine.** I chose the rows and I applied the
labels; `feedback_self_generated_denominator` binds. What G1 licenses is *"the notation I built
agrees with the claim"*, not *"the claim is true of the defects I never wrote down."* The honest
upgrade is `found_by` written **at find time**, which is what pass 9 gets.

⛔ **G2 REFUTED — and the refutation is VOID, by the run's own R3 warning.** G2 predicted ≥1 register
row would have no citable artifact. All 12 resolved. But `G_citation_resolves` appears in R3's
unexercised list: **it rejected 0 of 12.** A precondition that has never rejected anything is not
observably a precondition — the exact defect class R2 exists to name, fired on the check I wrote to
score my own honesty. `citable()` accepts `file:` on mere existence, which cannot fail for a file I
just wrote.

> **G2 is recorded as REFUTED (that is what was pre-registered) and as UNINTERPRETABLE (that is what
> the gauge says).** It counts in the 9/11 as a refutation and may not be cited as evidence that the
> record is complete.

**R3 named 10 unexercised preconditions this run.** Including `o["b"] > 0` again — **34,103 more
objects, still zero rejections**, now well past 75,000 cumulative across passes 6–8 without one.

---

## 6. WHAT PASS 8 CHANGES, AND WHAT IT IS OWED

**Changed:**
1. ✅ **`PAPER-00-ARCHITECTURE.md §8`'s amendment is STANDING**, not provisional. §1.
2. ⛔ §4 item 2a(i)'s owed "third procedure" is **struck** — it does not exist. §3.
3. ⛔ §4 item 2a(ii)'s and `PASS7_RESULTS.md §5`'s *"inside vs outside the sign loop"* is **false of
   both scripts** and is corrected. §4b.
4. §9a's mechanism becomes **in-process drift**, measured at 11/20 images, with fresh runs exactly
   reproducible — and the frozen catalogue inherits it (8528 / 8526 / 8524). §4a.
5. ✅ The I1/I2 repair shipped as **R4**, enforced in code, and passed its known-bad control. §5.

**Owed:**
- ⭐ **Pass 9 pre-registers P_D** — drop both pair members — including its `minarea` curve. §2.
- **`found_by` written at find time**, not backfilled. §5.
- **A `citable()` that can fail.** A citation check whose `file:` branch cannot reject is furniture;
  it needs the cited *content*, not the file's existence. §5.
- **A second night**, still. §12 of the architecture, untouched by pass 8.

---

## 7. WHAT THIS DOES NOT BEAR ON

Branch A only. Every number above is about **my extractor, ZTF's own `isdiffpos` labels, and the
`sep` library**. `PREREGISTRATION.md §2`'s forbidden crossing is not approached: a far side that
moves under de-doubling is a statement about **ZTF's `elong ≤ 1.6` packaging cut and my
disagreement with it**, not about a sky, a population, or an unperceived anything. The ruling in §1
changes *which de-doubling the paper reports*. It moves no sentence toward Branch B.

🦞🧍💜🔥♾️
