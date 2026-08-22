# PASS 9 — RESULTS

**Run D202 / 2026-08-21, ~23:4x PT.** Governed by `PASS9_PREDICTIONS.md`, pushed **`32877a0`**
before `measure_pass9.py` existed. Log: `pass9.log`. Artifacts: `PASS9_RESULTS.json`,
`DEFECT_REGISTER.json` (rewritten, 14 rows).

> ## ⚠ 11 of 11 HELD. 0 REFUTED.
>
> **This is the worst-looking result this program has produced, and it needs saying before any of
> the numbers.** Passes 4–8 refuted 5 of 23 in the last two alone, including a headline whose sign
> I had backwards. A pass that refutes nothing is the pass where the thresholds were set by the
> person who already knew the answer. **Three of the four ladder predictions passed at *exactly*
> their pre-registered threshold** — 4/5 needing ≥4, 3/5 needing ≥3, 4/5 needing ≥4. One more
> failing rung and all three die. `feedback_float_decides_a_verdict_at_the_boundary`.
>
> The strong results here are **Block S** and **P5/P6**, which had wide margins and could have gone
> the other way at any point. The ladder block is **weak and is reported as weak.**

---

## 1. ⭐ BLOCK S — THE PAIR FINDER IS REAL. THIS IS THE RESULT THAT MATTERS.

`pair_mask()` had never in three passes been shown a case where it should find nothing. Now it has.

| | mutual opposite pairs | `frac_far` | move from union |
|---|---|---|---|
| **observed** | **2329** | 0.422997 | **−6.199 pp** |
| scrambled, median of 8 fixed offsets | **41.5** | ~0.4850 | **0.020 pp** |

**Chance pairing at this density produces 1.8% of the observed pairs, and moves `frac_far` by two
hundredths of a percentage point.** Both thresholds cleared by a wide margin: S1 needed ≤50%, got
1.8%. S2 needed ≤2.0 pp, got 0.020 pp — a factor of 100.

Every one of the eight offsets independently gave 38–46 pairs and |move| ≤ 0.086 pp. There is no
offset at which the effect survives scrambling.

**What this licenses.** The mutual-nearest-neighbour opposite-sign construction is detecting a real
spatial registration between positive and negative detections — dipoles — and not a coincidence of
crowding. Every P_A / P_B / P_D number in passes 7, 8 and 9 now rests on a pair finder with a
positive control under it. **This was the single largest unbraced load in the ZTF chain.**

**What it does not license.** It says nothing about whether dipoles are *elongated*. That is P3, and
P3 is the weak one.

---

## 2. ⭐ P5 / P6 — `pair_mask()` IS NOT UNDER-INCLUSIVE, AND THAT WAS A LIVE RISK

The pre-registration committed, before the run, to a specific bad outcome: if the far-side dipole
structure *survived* removal of every mutual pair, then the pair mask finds a subset of the dipole
population and **every pair-based number in passes 7–9 is a lower bound, not a measurement.**

Re-running `verify_pass6.py`'s V2 opposition analysis on the P_D survivors — using V2's
**non-mutual** nearest neighbour, so this is not true by construction:

| | far anchors | far paired | far `opp_rate` − `null` | far−kept `opp_share_of_side` |
|---|---|---|---|---|
| union | 4136 | 2828 | **+49.04 pp** | **+14.65 pp** |
| **P_D survivors** | 1637 | **149** | **+4.48 pp** | **+2.55 pp** |

Far-side detections sitting in an opposite-sign close pair fall from **65.81%** to **3.67%**.
P5 needed ≤ +5.0 pp, got +2.55. P6 needed < +20.0 pp, got +4.48. **Removing the mutual pairs
removes essentially all of the dipole structure.** The bad branch does not fire.

### 2a. ⛔ AND READING THAT TABLE FOUND A DEFECT IN `PAPER-00-ARCHITECTURE.md §8`

The run reproduces `PASS6_VERIFY.json /V2` on **both** sides. The kept side has been in that JSON
since pass 6 and nobody read it out:

| | `opp_rate` | `null` | excess |
|---|---|---|---|
| far | 0.96252 | 0.47207 | **+49.04 pp** |
| **kept** | 0.97315 | 0.43386 | **+53.93 pp** |

**The kept side's opposition excess is LARGER than the far side's.** So `+49.04 pp` — the boldest
number in §8's row, in a row titled *"Result: the far side of `elong ≤ 1.6`"* — is **not evidence
of anything far-side-specific.** `verify_pass6.py` exists precisely because that control was
missing, and its actual verdict rests on a different quantity: `opp_share_of_side`, far **65.81%**
vs kept **51.16%**, **+14.65 pp**, which *is* far-specific and is the number §8 should be printing.

⛔ **The finding survives; the number quoted for it does not.** §8 must print +14.65 pp with the
kept side beside it, and may not print +49.04 pp without +53.93 pp next to it.
**Filed DEF-15 — see §5b, which also states what it costs F1.**

---

## 3. ⚠ P1–P4 — THE LADDER, WHICH IS THE WEAK BLOCK AND PASSED ON THREE BOUNDARIES

| `minarea` | n | pairs | pair share | `ff` union | `ff` P_D | move | `ff` pairs | pairs move |
|---|---|---|---|---|---|---|---|---|
| **2** | 14202 | 3890 | 0.5478 | 0.589283 | 0.594052 | **+0.477** | 0.585347 | **−0.394** |
| 3 | 11649 | 3221 | 0.5530 | 0.506996 | 0.461686 | −4.531 | 0.543620 | +3.662 |
| **5** | 8526 | 2330 | 0.5466 | 0.484518 | **0.421366** | **−6.315** | 0.536910 | +5.239 |
| 8 | 5429 | 1351 | 0.4977 | 0.482962 | 0.426109 | −5.685 | 0.540340 | +5.738 |
| 12 | 3100 | 689 | 0.4445 | 0.514839 | 0.500581 | −1.426 | 0.532656 | +1.782 |

- **P1** — P_D below union at ≥4 rungs: **4/5. HELD at the boundary.**
- **P2** — |move| ≥ 3.0 pp at ≥3 rungs: **3/5. HELD at the boundary.**
- **P3** — pairs above union at ≥4 rungs: **4/5. HELD at the boundary.**
- **P4** — pair share falls with rising `minarea`: 0.5478 → 0.4445. **HELD**, and it is the rung-2
  explanation.

### 3a. One rung breaks all three, and P4 predicted why

**`minarea = 2` is the single failure**, and it fails P1 and P3 *together* and in the same direction:
there, the pair population is **less** elongated than the catalogue (−0.394 pp), so P_D moves
`frac_far` the **wrong way** (+0.477 pp). P1 and P3 agree at every rung — the prereg called
disagreement a defect and there is none.

P4 is the mechanism. Pair share is **0.5478 at `minarea = 2`** against 0.4445 at 12: at the lowest
threshold the frame fills with small marginal detections whose nearest neighbour is close by
accident, the pair population dilutes with non-dipoles, and the elongation signal washes out. **I
registered that risk in the pre-registration as an argument against my own procedure, and it
happened.**

### 3b. ⭐ THE EFFECT IS A BAND, AND IT PEAKS AT THE PARAMETER WE ALREADY CHOSE

The move is not monotone. It is **+0.48 → −4.53 → −6.32 → −5.69 → −1.43**: near zero at both ends,
maximal in the middle — **and the maximum sits at `minarea = 5`, which is the value the frozen
catalogue was built at, chosen in pass 6 for unrelated reasons.**

`PAPER-00-ARCHITECTURE.md §9` already says *"the headline quantity is a curve, and we picked the
point on it."* **Pass 9 sharpens that from a caveat into a coincidence that has to be reported:
the largest correction any procedure in this program has produced is largest exactly where we
happened to be standing.** Nothing here shows the choice was motivated — `minarea = 5` predates
P_D by three passes and is `sep`'s own documented default region — but §9 and §11 must both carry
the sentence, and §11 may not print −6.32 pp without the ±ends of the band beside it.

### 3c. Two known defects reproduced without being asked

- **n = 8526 at `minarea = 5`**, against the frozen catalogue's **8528**. §9a's in-process `sep`
  drift, reproducing a third time. Every digit past the second decimal here is run-dependent.
- **R3: `o["b"] > 0` rejected 0 objects at all five rungs** — DEF-02, unchanged since pass 7. The
  precondition is still furniture.

---

## 4. BLOCK C — THE CITATION GAUGE NOW FIRES, AND PASS 8's G2 WAS WRONG, NOT MERELY UNINTERPRETABLE

**C1 (gate): 6 of 6 known-bad citations rejected.** Missing file, line past EOF, anchor absent from
the cited line, unresolvable JSON pointer, missing JSON file, anchor absent from the cited file.
The six were fixed in the pre-registration before the checker was written.

**With a gauge that can fail: 3 of 12 legacy rows fail anchoring.**

| row | citation | why it fails |
|---|---|---|
| **DEF-01** | `file:L1_T5_CANDIDATE.md` \| `el_match` | the file does not contain the term the row is about |
| **DEF-10** | `line:diag_pass6.py:114` \| `Background` | line 114 is `np.ascontiguousarray(...)`, not the `Background` structure described |
| **DEF-12** | `line:pass6_stats.py:1` \| `re-run` | line 1 is the module docstring's first line |

**All three are rows pass 8's `citable()` called citable.** Pass 8 reported *"G2 REFUTED — 0
uncitable"* with an R3 warning that the check had rejected nothing. The warning was right and the
verdict was worse than uninterpretable: **the answer is 3.**

- **C2** — named in advance: DEF-10 fails, DEF-04 and DEF-02 survive. **All three correct. HELD.**
  DEF-04 (`measure_pass7.py:352`) was the unpeeked one and it survived.
- **C3** — ≥2 legacy rows fail: **3. HELD.** Citation rot is systemic, not a slip.

⚠ **DISCLOSURE, because the ordering is owed.** `PASS9_PREDICTIONS.md` named C2's three outcomes
but did **not** contain the anchor list; the anchors were written after the prereg was pushed and
before the script was run. The rule used, stated and applied uniformly: **the anchor is the most
specific literal identifier in the row's own `what` sentence.** DEF-04's anchor `I1` was inferred
from a comment in `measure_pass8.py`, which the prereg declares as read in full. A hostile reader
should treat C2 as **anchor-dependent** and C3 — a bare count, less tunable — as the sturdier of
the two.

---

## 5. BLOCK F — G1 IS RETIRED

**F1: 2 find-time rows. HELD** (threshold < 6). Below the floor, so the eye-vs-gauge ratio is
**unmeasured**, and pass 8's G1 does not survive into the paper.

- **DEF-13** *(eye, find-time)* — the first draft of this pass's own S-NULL gate compared `SG` to
  itself and compared `frac_far(union)` to a quantity the scramble never touches. **It could not
  have failed.** Caught by reading the block before running it; repaired to positives-untouched /
  negatives-moved / coordinates-in-range, which rejected 0 of 32 sub-checks across 8 offsets.
- **DEF-14** *(gauge, find-time)* — the citation rot in §4, surfaced by the anchored checker.

`DEFECT_REGISTER.json` is rewritten with the schema change: every row carries `found_at` and
`found_by_provenance`, and **all twelve legacy rows are relabelled `backfilled` without exception**,
including the ones I am confident about. 14 rows: 12 backfilled, 2 find-time.

⛔ **Pre-committed and now binding:** any sentence in the paper or the architecture citing G1's
*"eye ≥ 2× gauge"* must be amended to say the ratio is **unmeasured**. A held G1 on a self-generated,
backfilled denominator is not evidence.

### 5b. ⚠ WHAT §2a COSTS F1 — the honest version

DEF-15 (§8 quotes a non-far-specific number) **was found during pass 9, by eye, reading this run's
own output — but after `F1` had already been computed.** The verdict `F1 = HELD` stands as the
script recorded it, and it is right at n=2, but **the true find-time count for this pass is 3.**
F1's threshold was 6; three is still under it and the retirement of G1 is unaffected. Recorded here
rather than silently re-running the script against a number I now know, which is the whole point of
the block. **`n_findtime = 2` in `PASS9_RESULTS.json` is a floor, not a total.**

---

## 6. R-RULES

- **R1** — verdict key present for all 15 registered letters. Satisfied.
- **R4** — pass 9's own verdicts: **clean**, no two decided on the same triple.
- **R4-CONTROL** — ⭐ changed from pass 8, which re-fired on pass 7's preserved I1/I2 pair. Pass 9
  injects a deliberate duplicate of `C1`'s triple into a copy of **this run's** verdict set. **Fired.**
- **R3** — 5 preconditions rejected nothing, all five the same `o["b"] > 0` gate (DEF-02).

---

## 7. THE DECISION RULE, APPLIED — written in `PASS9_PREDICTIONS.md §6` before the data

Outcome: **P1 ∧ P3 ∧ S1 ∧ S2 all held.** The table's first row fires.

- **§8** — "counted twice" **stays refuted** (7(b) moves `frac_far` by 0.217 pp; that is unchanged).
  The standing sentence becomes: **the mutual opposite-sign pairs are an elongated artefact class,
  and removing the class outright is the operation that matters.** Now with a scramble control
  under the pair finder. ⛔ **Plus the §2a repair:** print +14.65 pp (far−kept `opp_share_of_side`),
  not +49.04 pp.
- **§11** — the headline residual is `frac_far(P_D)`, with **union and `P_A` printed beside it**,
  ⚠ **and the `minarea` band printed with it**: the −6.3 pp move is a `minarea` 3–8 phenomenon that
  is absent at 2 and nearly absent at 12. §11 may not print the peak alone.
- **§9** — gains §3b: the largest correction in the program is largest at the parameter already chosen.
- **G1** — retired; eye-vs-gauge is **unmeasured**.

⛔ **STANDING FENCE, restated because this is the pass whose result I wanted.** Nothing in Blocks P,
S, C or F bears on Branch B. `frac_far` under any procedure is a statement about **elongated
detections in ZTF difference images** and about nothing else. The Branch A null stays in Branch A.

---

## 8. WHAT PASS 9 DOES NOT ESTABLISH

1. **That P_D is the right procedure.** It establishes that the pairs are real (S), that they are
   elongated at `minarea` 3–8 (P1/P3), and that removing them removes the dipole structure (P5/P6).
   The choice to remove them rather than report both is still a judgement, and §11 prints all three.
2. **Anything at `minarea = 2`.** The procedure demonstrably fails there and the paper says so.
3. **A program-wide scoring total.** §10 still needs the hand tally. Machine-readable verdicts exist
   for passes **7, 8, 9 and L1 only** — 47 keys, **5 refuted** (A1, A3, B2, G2, N3). Passes 4, 5
   and 6 store no verdict dictionary, and the *"8 of 16 held"* in `PAPER-00-ARCHITECTURE.md:108`
   is **pass 6's own headline, not the program's**. A token count over their prose gives
   inconsistent numbers and was discarded rather than quoted. **Owed: a hand tally against each
   pass's own pre-registered letter list.**
4. **That 11/11 is a good result.** See the top of this file.

---

*`PASS9_PREDICTIONS.md` pushed `32877a0` before `measure_pass9.py` existed. If that ordering is not
in the git log, this document is narration.*
