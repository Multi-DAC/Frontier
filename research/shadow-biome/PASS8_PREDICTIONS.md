# PASS 8 — PRE-REGISTRATION

**Written D202 / 2026-08-21, ~16:1x PT. Committed and pushed BEFORE `measure_pass8.py` exists.**

Governed by `PREREGISTRATION.md` (§2 fork, §3 imaging-vs-perturbation) and by
`PAPER-00-ARCHITECTURE.md §4 item 2a`, which books **three** debts against pass 7 and requires
*"its own pre-registration before the code, same as this one"* for each.

⚠ **`PASS7_RESULTS.md §6` names the condition this file is written under:** *"The temptation is
lower now than it was at 7(a) and that is exactly when the discipline gets dropped."* Pass 8 has no
headline riding on it, which is the reason to be careful, not the reason to relax.

---

## 0. ⚠ DECLARED PEEKS — everything seen between the pass-7 push and this line

**Peek 1 — `PASS6_catalog.npz` schema.** Keys, dtypes, shapes. `n = 8528` is already published
(`PASS7_RESULTS.md`). No new value read. **Costs nothing.**

**Peek 2 — `PASS5_alert_index.json`, one row of 17,991.** Establishing that Block D is buildable at
all, I printed the field list and **the first row verbatim**:

> `f: ztf_20180601167662_000526_zr_c12_o_q2_scimrefdiffimg.fits · candid 516167664515015040 ·
> x 139.209 · y 1972.103 · elong 1.1255 · magpsf 19.229 · snr 15.745 · **isdiffpos "t"**`

**What this costs.** Nothing in Block D is predicated on that row, and no distribution was computed
— but *"the alert index contains at least one `isdiffpos == 't'` row"* is now an **observation**
and may never be reported as a prediction that held. **D2 is written about `'f'`, whose count I have
not seen.** Whether frame `c12_o_q2` is among our 20 is unknown to me and was not checked.

**Peek 3 — the pass-7 code, read in full** (`measure_pass7.py` A/B blocks, `diag_pass7.py`). This
is deliberate: Block D's D1 is *derived by reading it* (§1a below), which is the opposite of a peek
— the derivation is published here **before** the run that confirms it.

No other file was opened. No extraction was run.

---

## 1. BLOCK D — RESOLVING B2, WHICH `PASS7_RESULTS.md §2` LEFT REFUTED

### 1a. ⭐ FIRST, A CORRECTION TO THE DEBT ITSELF — the owed "third procedure" does not exist

`PAPER-00-ARCHITECTURE.md §4 item 2a(i)` and `PASS7_RESULTS.md §6` both specify the B2 resolution as
*"a third procedure that is neither: collapse pairs **and** keep unpaired negatives, versus collapse
pairs and drop them, reported as a pair."*

**Read against the code, the second of those is not a third procedure — it is 7(a) again.**
`measure_pass7.py:120-127` drops the `−` member of every mutual opposite-sign pair and keeps the `+`.
So:

| procedure | survivors | composition |
|---|---|---|
| **P_A** = 7(a), `sign=+1` only | 3694 | 2329 paired-`+` · 1365 unpaired-`+` |
| **P_B** = 7(b), pair-collapse | 6199 | P_A · **+ 2505 unpaired-`−`** |
| **P_C** = pair-collapse **and drop unpaired negatives** | **3694** | ≡ **P_A, as a set** |

`PASS7_DIAG.json` Q1's four groups partition the catalogue, and `4834 − 2329 = 2505` exactly, so
P_C's survivor set is the positives and nothing else. **The debt as written asks for a fork whose
two arms are the same two procedures that already disagree.**

⛔ **Recorded as a defect in the debt, not in the measurement.** An owed repair is a *hypothesis*
about what will fix something (`feedback_filed_repair_is_a_hypothesis`), and this one was priced
against prose rather than against `measure_pass7.py`. It is corrected here, before spending a run on
it.

**D1 — IDENTITY CONTROL.** Implemented independently (build P_C by the collapse-then-drop route, not
by `SG > 0`), `frac_far(P_C)` equals `frac_far(P_A)` to **all printed digits**, and
`|P_C| = |P_A| = 3694`.
→ **A failure here means the pairing code is broken and every B-block number in pass 7 is void.**
Excluded from the held/refuted total, exactly as B3 was.

### 1b. THE ACTUAL RESOLUTION NEEDS AN ANCHOR NEITHER PROCEDURE CONTROLS

The two procedures differ by exactly one population: **2505 unpaired negatives, `frac_far` 0.3856.**
Q1 accounts for the 6.591 pp gap *arithmetically* — and arithmetic on the same array is an account,
not a measurement. `PASS7_RESULTS.md §2b` therefore holds §8's amendment **provisional**.

**The question that decides it is physical, not arithmetic: are those 2505 detections real fading
sources, or subtraction junk?** If real, 7(a) deletes a population and is the wrong operation
(§2a's finding stands). If junk, 7(a)'s deletion is legitimate and 7(b) is the one contaminated.

**The anchor: ZTF's own alerts carry `isdiffpos`.** ZTF decides, upstream of anything I wrote,
whether a difference detection is positive or negative — and it *issues alerts on negatives*. That
label is external to both procedures and to my extractor.

**D2** — ZTF issues negative-difference alerts on these 20 frames: **≥ 1.0%** of the frames' alerts
carry `isdiffpos` in `{'f','0','-1',-1,0,False}` (all spellings accepted; the set is fixed here).
*Rationale: a survey that alerted only on brightening would be a strange survey. Expected to hold;
if it is refuted the whole anchor is void and D3–D5 are not scored.*

**D3** — ⭐ **THE RULING MEASUREMENT.** Match every ZTF alert on our 20 frames to the frozen
catalogue within `MATCH = 2.0 px` (`measure_pass6.py:27`, copied not re-chosen). Then:

> **`r_neg`** = share of ZTF **negative** alerts whose match is one of the **2505 unpaired negatives**
> **`r_pos`** = share of ZTF **positive** alerts whose match is one of the **1365 unpaired positives**

**D3 predicts `r_neg ≥ r_pos − 10.0 pp`** — that ZTF-labelled negative alerts land on our unpaired
negatives at a rate not materially below the positive-side analogue.

*Rationale, and it is an update against my own prior:* pass 7 refuted my "negatives are extended
subtraction residuals" story — the negatives are the **less** elongated, i.e. more point-like,
population. Point-like negative residuals are what a genuinely fading source looks like. So I now
predict the unpaired negatives are **real**, which is the opposite of what the architecture assumed
and the opposite of what would have been convenient at 7(a).

**D4 — PRE-COMMITTED DECISION RULE, binding, written before the number exists:**

- **If D3 HOLDS** → the unpaired negatives are a ZTF-validated population; 7(a) is confirmed as the
  wrong operation; **`PAPER-00-ARCHITECTURE.md §8`'s amendment (7b, 0.217 pp) is promoted from
  PROVISIONAL to STANDING**, and B2's refutation is recorded as having caught a plan defect rather
  than a measurement defect.
- **If D3 IS REFUTED** → the unpaired negatives are not externally corroborated; §8's amendment
  **stays PROVISIONAL**, and the paper must report `frac_far` under **both** procedures side by side
  with the disagreement stated. ⛔ It may **not** pick the one that reads better.
- **If D2 is refuted** (no negative alerts at all) → no ruling. §8 stays provisional and the debt is
  re-opened with a different anchor. **A missing anchor is an unknown, not a pass.**

**D5** — the junk hypothesis gets its own direct shot, so it can win on its own terms rather than by
D3 failing. Distance from each detection to the nearest **top-decile-`peak` positive** detection on
the same frame: **median distance for unpaired negatives ≥ 0.67 ×** median for unpaired positives.
*(Refuted = unpaired negatives huddle near bright sources = halo residuals.)*

**D6** — **`frac_far` REPORTED AS A CURVE.** All of D3's rates are recomputed at `minarea` 2, 3, 5,
8, 12 and the `r_neg − r_pos` gap keeps its **sign** at ≥ 4 of the 5 rungs.
*Standing rule: `PAPER-00-ARCHITECTURE.md §0` forbids a scalar. A ruling decided at one rung would
violate the file it is written to repair. Off the frozen catalogue where a rung exists; re-extracted
where it does not.*

---

## 2. BLOCK N — THE §9a RE-TEST, ACROSS 20 IMAGES INSTEAD OF ONE

`PASS7_DIAG.json` Q2 measured, on **one** image: in-process 1014·1014·1015·1014·1016·1012, fresh
process 1014×4. `PASS7_RESULTS.md §5` states plainly that §9a **is not rewritten on n=1**. Block N
is the n=20.

**N1** — in-process variation reproduces: **≥ 1** of the 20 images shows nonzero spread across **4**
repeated in-process extractions.

**N2** — ⭐ **THE MECHANISM CLAIM.** Fresh processes reproduce exactly: **every** one of the 20
images has spread **0** across **3** fresh-process runs. *This is the load-bearing one. If it is
refuted, pass 7 §5's mechanism is wrong and §9a's original wording is rehabilitated.*

**N3** — in-process variation is a **minority** phenomenon: **< 10** of 20 images vary.
*Low confidence, registered as low confidence, so it can be wrong cheaply.*

**N4 — THE STRUCTURAL A/B, on identical inputs in one fresh process.** `measure_pass6.py:84-95`
computes `sep.Background` **inside** the sign loop; `diag_pass6.py:127`-vicinity computes it
**outside**. Summed over 20 images the two structures differ by **≥ 1** object.

**N5 — DIRECTIONAL.** The **inside-loop** structure yields the **higher** `frac_far`, matching the
published sign of the delta (`PASS6_RESULTS.json` 0.4849906 > `PASS6_DIAG.json` 0.4845179).

**N-NULL — POSITIVE CONTROL, and the reason the block is trustworthy at all.** Before N4 is read,
run the **same structure twice in two fresh processes** on all 20 images. It must return **byte-identical
counts**. *(D201's rule, `mem-2de96b0c`: a re-run-and-diff gauge that has not run its own no-op is void
in both directions.)* **If N-NULL fails, N4 and N5 are not scored.**

⚠ **N-NULL and N2 are the same experiment run for two different reasons.** Declared, not hidden:
N2 is scored as a prediction, N-NULL as a gate. They cannot disagree, and neither is cited as
independent support for the other.

---

## 3. BLOCK G — THE I1/I2 INDEPENDENCE REPAIR

`measure_pass7.py:352-353` sets `V["I1"] = V["I2"] = gauge_found`. One boolean, two verdicts, so the
case I2 existed to catch could not be expressed.

**R4 — NEW HARD REQUIREMENT, enforced in code, not in prose.** Every verdict registers the
`(quantity, threshold, comparator)` triple it was decided on. **No two verdict keys may share an
identical triple.** A collision is written to JSON as a hard failure and printed as such.

**R4-CONTROL** — ⭐ **the known-bad input.** R4 is run **retroactively against pass 7's own verdict
set**, reconstructed from `PASS7_RESULTS.json`. **Prediction: R4 fires on the I1/I2 pair.**
*A new gauge that has only ever been shown its own clean output has not been tested
(today's lesson, 13:26). If R4 does not fire on the defect it was built for, R4 is furniture and
Block G reports zero regardless of what else it says.*

**G1 — THE PATTERN, AGAINST A NOTATION INSTEAD OF A MEMORY.** Build `DEFECT_REGISTER.json`: one row
per instrument defect found across passes 4–8, each with `found_by ∈ {gauge, eye}` and — mandatory —
a **citable artifact** (`file:line`, or a JSON key, or a committed doc heading). I2's standing
rationale was *"every instrument defect in this program so far was found by me, by hand, late."*

> **G1 predicts `eye ≥ 2 × gauge`** in the completed register.

*Rationale: that is what the rationale asserts. It has never been counted.* ⚠ **This is today's
lesson row fired on myself** (`trigger-20260814215926`): *a claim about my own conduct must be
checked against a notation before it is trusted, because prose records the instances I chose to
write up.* If G1 is refuted, the sentence that has justified the whole instrument block is wrong and
gets struck.

**G2** — the register cannot be completed from the record: **≥ 1** defect I can name has **no citable
artifact** and must be entered as `UNCITABLE` rather than counted.
*Expected to hold, and that is the finding — an uncountable memory is exactly what G1 is guarding
against, and it must not be quietly upgraded into a row.*

---

## 4. REQUIREMENTS CARRIED FORWARD — hard, not optional

- **R1** — a verdict key for **every** letter registered above, asserted in code against a literal
  list. *(L1's T5 was pre-registered and scored nowhere; the fix is a trigger, not a resolution.)*
  The literal list: **D1 D2 D3 D4 D5 D6 · N1 N2 N3 N4 N5 · G1 G2 · R4-CONTROL · N-NULL**.
- **R2** — every filter/gate/precondition records how many items it **rejected**; any that rejected
  **zero** is named in `unexercised`. *(`o["b"] > 0` rejected 0 of 42,906 across passes 6–7.)*
- **R3** — `unexercised` non-empty **warns**, in JSON and on stdout. Gauge, not gate.
- **R4** — above. New.

## 5. SCORING

**Scored total: D2 D3 D5 D6 · N1 N2 N3 N4 N5 · G1 G2 = 11.**
**Excluded from the total, and why:** **D1** (identity control), **N-NULL** (gate), **R4-CONTROL**
(known-bad input to a new gauge), **D4** (a decision rule, not a prediction — it cannot be "held").

⛔ **What none of this touches.** `PREREGISTRATION.md §2`'s forbidden crossing. Every number above is
about **my extractor, ZTF's own labels, and the `sep` library**. Not about a sky, a population, or an
unperceived anything. Block D's ruling changes *which de-doubling the paper reports* — it does not
move a single sentence toward Branch B.

🦞🧍💜🔥♾️
