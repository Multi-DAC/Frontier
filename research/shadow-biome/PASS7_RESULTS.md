# PASS 7 — RESULTS

**Run D202 / 2026-08-21 ~16:0x PT.** Governed by `PASS7_PREDICTIONS.md`, committed and pushed
(`da25f0c`) **before `measure_pass7.py` existed**. Artifacts: `PASS7_RESULTS.json`,
`PASS7_MISSES.json`, `PASS7_DIAG.json`, `pass7.log`.

> ## **9 of 12 held. A1 refuted, A3 refuted, B2 refuted — and the three refutations are worth more than the nine.**
> *(B3 is an identity control and is excluded from the total, per `PASS7_PREDICTIONS.md §3`.)*

---

## 1. ⭐ THE HEADLINE: I HAD THE SIGN OF THE ARTEFACT BACKWARDS

| quantity | value |
|---|---|
| `frac_far` union (`minarea=5`) | **0.484991** |
| `frac_far` **`sign=+1` only** | **0.548728** |
| `frac_far` **`sign=−1` only** | **0.436285** |

**A1 predicted single-sign `frac_far` would fall below the union. It rose — by 6.37 pp.**
**A3 predicted the negative side would be the more elongated one, by ≥3 pp. The positive side is
more elongated, by 11.24 pp.** Both refuted, both in the same direction, and that direction is the
opposite of the story the architecture has been carrying.

**The story that just died.** `PAPER-00-ARCHITECTURE.md §8` attributes the far side to
*"difference-image dipoles, counted twice by pass 5's `+data`/`-data` union"*, and A3's rationale
made that concrete: negative lobes are subtraction residuals sitting on bright-star wings, hence
extended, hence elongated, hence the far side is substantially an artefact of the negative pass.
**Measured: the negatives are the LESS elongated population.** Deleting them does not clean the far
side, it *concentrates* it.

⚠ **And it is robust across the whole `minarea` ladder** — A4's real content, beyond the span it
was written to test:

| `minarea` | `frac_far` union | `frac_far` `+only` | drop |
|---|---|---|---|
| 2 | 0.5893 | 0.6331 | **−4.383 pp** |
| 3 | 0.5070 | 0.5583 | **−5.133 pp** |
| 5 | 0.4845 | 0.5479 | **−6.337 pp** |
| 8 | 0.4830 | 0.5647 | **−8.172 pp** |
| 12 | 0.5148 | 0.6052 | **−9.031 pp** |

**Every rung negative.** A1 and A3 are not refuted at one parameter value; they are refuted at all
five, and the effect *grows monotonically with `minarea`*.

⚠ **A4 HELD at span 4.648 pp against a threshold of 5.0 — 0.35 pp of margin on a number I chose
arbitrarily.** It is recorded as held because that is what was pre-registered, and it is recorded
here as **nearly refuted** because a verdict decided in the third decimal of an arbitrary threshold
is not a robust verdict. **A4 also did not test the monotonicity above, which is the more
interesting structure and which no pre-registered prediction covers.** Post-hoc, and labelled.

---

## 2. ⛔ B2 REFUTED — AND BY MY OWN RULE THAT MAKES §1 UNINTERPRETABLE

| quantity | value |
|---|---|
| `frac_far` **pair-collapsed** | **0.482820** |
| \|collapsed − `+only`\| | **6.591 pp** (threshold 4.0) |

`PASS7_PREDICTIONS.md §3`: *"A B2 refutation makes A1/A2 and B1 **UNINTERPRETABLE** rather than
merely surprising."* **That fires. It is not renegotiated here.**

### 2a. The diagnosis — and it is not a rescue

`PASS7_DIAG.json` Q1, post-hoc and labelled as such:

| group | n | `frac_far` |
|---|---|---|
| positive, paired | 2329 | 0.5822 |
| positive, unpaired | 1365 | 0.4916 |
| negative, paired | 2329 | 0.4908 |
| **negative, unpaired** | **2505** | **0.3856** |

7(a) deletes **4834** negatives. 7(b) deletes **2329**. The difference is **2505 unpaired
negatives at `frac_far` 0.3856** — far below the catalogue's 0.4850. Deleting a big, low-elongation
population *raises* the remaining fraction. **That accounts for the 6.591 pp gap arithmetically.**

⭐ **What it accounts for is a defect in the architecture's plan, not in the measurement.**
`PAPER-00-ARCHITECTURE.md §11(a)` specifies pass 7(a) as *"single-sign extraction, `+data` only, no
union."* **That is not a de-doubling procedure.** It is a de-doubling *plus* the deletion of 2505
detections that are not dipole halves at all — negative-only residuals, which include real fading
sources. **The pre-registration's own control caught the architecture's plan being wrong**, which
is the entire reason B2 was written as an agreement test between two procedures rather than as a
result.

⛔ **B2 stays REFUTED.** The diagnosis is dated, post-hoc, and does not retro-fit the verdict.

### 2b. ⭐ The number that survives, and it is the one that matters

**7(b) is the de-doubling that does what the architecture meant.** Collapse 2329 mutual
opposite-sign pairs within 10 px — **27.3% of the catalogue removed** — and:

> **`frac_far`: 0.484991 → 0.482820. A move of 0.217 pp.**

**Dipole double-counting does not explain the far side.** It inflates the *count* and leaves the
*fraction* essentially where it was. `PAPER-00-ARCHITECTURE.md §8`'s parenthetical mechanism is
therefore **refuted as an explanation of `frac_far`** and must be restated as what it is: an
explanation of `n`.

⚠ Carried under B2's ruling: this sentence is **provisional** until the disagreement between the two
procedures is resolved by a measurement rather than by an account. The route is stated in §6.

---

## 3. C1–C4 — ALL FOUR HELD, AT `minarea=2`

376 alerts · **275 recovered (73.14%)** · 101 residual.

| class | n |
|---|---|
| RECOVERED | 275 |
| **UNEXTRACTED_DESPITE_FLUX** | **68** |
| BELOW_THRESHOLD | 31 |
| NEAR_MISS_RADIUS | 2 |

- **C1 HELD** — recovery reproduced `PASS6_DIAG.json`'s 0.7313829787 to **+0.000 pp**. See §5; this
  turned out to be a finding about the instrument rather than a formality.
- **C2 HELD** — `UNEXTRACTED_DESPITE_FLUX` is the largest residual class, 68 of 101 (67.3%).
- **C3 HELD** — median `magpsf` unrecovered − recovered = **+1.124 mag** (threshold 1.0). The
  boring answer, predicted as the boring answer: the residual is *faint things a threshold-limited
  extractor misses*.
- **C4 HELD** — residual misses appear in **20 of 20** frames. Not clustered, so not a per-frame
  registration fault; a detection-efficiency floor, which is the duller reading and the one
  registered.

⛔ **None of this licenses an object claim.** A miss is an absence *in our extractor* of something
**ZTF already alerted on**. `PREREGISTRATION.md §3`'s ceiling, unchanged.

---

## 4. ⭐ THE INSTRUMENT BLOCK — R2's GAUGE BEAT MY EYE, WHICH I PREDICTED AGAINST

**I1 HELD · I2 HELD.** I2 was written expecting to lose: *"every instrument defect in this program
so far was found by me, by hand, late."* The automatic gauge got there first this time.

**R2's rejection table — 6 preconditions rejected NOTHING:**

| precondition | in | rejected |
|---|---|---|
| `o["b"] > 0` @ `minarea=2` | 14202 | **0** |
| `o["b"] > 0` @ `minarea=3` | 11649 | **0** |
| `o["b"] > 0` @ `minarea=5` | 8526 | **0** |
| `o["b"] > 0` @ `minarea=8` | 5429 | **0** |
| `o["b"] > 0` @ `minarea=12` | 3100 | **0** |
| alert carries `x`/`y` | 376 | **0** |

⭐ **`ok = o["b"] > 0` is `measure_pass6.py:88` and `diag_pass6.py:127` — inherited code, applied to
every extraction in passes 6 and 7, and it has never rejected a single object.** It is the exact
shape of the L1 defect that generated this gauge (`el_match` True 8/8, `n_dropped: 0`), sitting in
the ZTF leg the whole time and never once looked at. It is benign — it guards a division by `b` that
never divides by zero — but *"benign"* is a conclusion available only after looking, and nobody had.

Likewise `NO_POSITION`: pass 6 carried a class for alerts without coordinates and **every alert has
coordinates**. A branch that has never executed.

### 4a. ⚠ AND I2's SCORING IS DEGENERATE — found by eye, by me, reading my own output

`measure_pass7.py:352-353` sets `V["I1"] = V["I2"] = gauge_found`. **They are the same boolean.**
So I2 can be refuted only when I1 is, and the case I2 was actually written to catch — *the gauge
finds something AND I had already spotted something by eye* — **cannot be expressed.**

⭐ **This is a scoring defect inside the fix for a scoring defect**, and it was found by exactly the
method I2 predicts against. The recursion is not a joke at my expense; it is the finding: **a gauge
that grades its own success renders only its good news.** I2's HELD above is therefore recorded as
**PROVISIONAL and structurally unable to have been otherwise**, and it may not be cited as evidence
that the gauge works.

**Repair, owed:** I1 and I2 need independent inputs — a defect register with a `found_by`
field (`gauge` / `eye`) written at find time, so the ordering is recorded rather than inferred.

---

## 5. ⭐ `sep` NON-DETERMINISM: THE MECHANISM IS SHARPER THAN §9a SAYS

C1 reproducing to **+0.000 pp** was the tell. Checked further: `measure_pass7.py`'s ladder
reproduced `PASS6_DIAG.json`'s counts at **all five rungs, exactly** — 14202 · 11649 · 8526 · 5429 ·
3100, and `frac_far` to four decimals at every rung — a day later, in a different process, from a
different script. That sits badly against `pass6_stats.py`'s docstring, the sole citation for
`PAPER-00-ARCHITECTURE.md §9/§9a`, which says `sep` *"does not return the same catalogue twice."*

**So it was measured** (`PASS7_DIAG.json` Q2), on the image the docstring names —
`687_zr_c14_o_q1`, which **is** in `diffimg/`:

| condition | object counts |
|---|---|
| **same process, 6 repeats** | 1014 · 1014 · 1015 · 1014 · 1016 · **1012** |
| **fresh process, 4 runs** | 1014 · 1014 · 1014 · **1014** |

> ⭐ **The variation is WITHIN a process across repeated calls. A fresh process reproduces exactly.**

The docstring's 1012–1016 is confirmed to the digit — **and it was measured in-process.** Both
observations are true and they are about different things. This explains the exact ladder
reproduction (fresh process, same call order) *and* the docstring's spread (repeated calls,
accumulating process state) with one mechanism.

**What it costs §9a.** §9a reports `PASS6_RESULTS.json` and `PASS6_DIAG.json` disagreeing by 0.047 pp
at the same `minarea` and attributes it to run-to-run non-determinism. On this evidence **fresh runs
of the same call sequence do not disagree**, so the 2-object measure-vs-diag delta more likely comes
from the **structural** difference between the two scripts — ~~`measure_pass6.py` computes the
background *inside* the sign loop, `diag_pass6.py` computes it once *outside*.~~

> ⛔ **STRUCK D202 ~16:4x BY PASS 8 §4b. THE STRUCK CLAUSE IS FALSE OF BOTH SCRIPTS.**
> **Both** compute `sep.Background` **inside** the sign loop (`measure_pass6.py:84-86`,
> `diag_pass6.py:115-117`). The real differences are (1) `measure_pass6.py` makes an extra
> `sep.Background(img)` call for `bkg0` *before* the loop, and (2) `diag_pass6.py` runs **five**
> `sep.extract` calls off one prepped array where `measure_pass6.py` runs one — and given N1/N2 that
> repetition *is* the variation mechanism. **The conclusion the clause was written to support
> survives** (`PASS8_NONDET.json`: the two structures differ by 4 objects, `measure`'s the higher
> `frac_far`, matching the published sign). The reason given for it did not. Entered as `DEF-10`.

⛔ **NOT YET TESTED, and §9a is not rewritten on this.** One image, ten extractions. The claim being
corrected is a section of the paper, and correcting it on n=1 would repeat the error that produced
it. **Owed:** run the same in-process/fresh-process contrast across all 20 images, and A/B the two
background structures directly on identical inputs.

> ✅ **PAID D202 ~16:3x — `PASS8_NONDET.json`, `PASS8_RESULTS.md §4`.** n=20, one process per image.
> In-process variation on **11 of 20** (registered as a minority, **refuted** — it is a majority);
> fresh-process spread **0 of 20**. The mechanism holds at n=20. ⭐ And the frozen catalogue inherits
> it: `PASS6_catalog.npz` **8528** (one process, 20 images) · pass-7 A4 **8526** · pass-8
> fresh-per-image **8524**.

⭐ **The one thing that stands now:** a re-run-and-diff gauge on this pipeline is worse than
`pass6_stats.py` thought. The docstring says such a gauge *"can pass a broken refactor and fail a
correct one."* If fresh runs reproduce exactly, then it **cannot fail a correct one** — it will
return identical every time and report success unconditionally. **A gauge that can only ever render
one verdict is furniture**, and this one has been standing in the room since pass 6.

---

## 6. WHAT PASS 7 CHANGES, AND WHAT IT IS OWED

**Changed:**
1. ⛔ `PAPER-00-ARCHITECTURE.md §8`'s dipole-doubling mechanism is refuted **as an explanation of
   `frac_far`** (§2b: 0.217 pp). It explains `n`. The section is amended, not deleted.
2. ⛔ §11(a)'s plan — *"single-sign extraction, `+data` only"* — is **the wrong operation** and is
   replaced by 7(b) pair-collapse. §2a.
3. The far side is **positive-dominated**, 0.5487 vs 0.4363, at every rung of the ladder. New, and
   the architecture had it backwards.
4. §9's instrument section gains R2's six unexercised preconditions and §5's sharpened mechanism.

**Owed:**
- **The B2 resolution.** A third procedure that is neither: collapse pairs *and* keep unpaired
  negatives, versus collapse pairs and drop them, reported as a pair. Until then §2b is provisional.
- **The §9a re-test** across 20 images, and the background-structure A/B. §5.
- **The I1/I2 independence repair.** §4a.
- ⚠ **A pre-registration for all three**, before the code, same as this one. The temptation is
  lower now than it was at 7(a) and that is exactly when the discipline gets dropped.

---

## 7. WHAT THIS DOES NOT BEAR ON

Branch A only, unchanged. `PREREGISTRATION.md §2`'s forbidden crossing is not approached by any
sentence above: **a far side that survives de-doubling is a statement about ZTF's `elong ≤ 1.6`
cut**, and about my extractor's disagreement with it. It is not a statement about a sky, a
population, or an unperceived anything. `PASS7_PREDICTIONS.md §2` narrowed this before the numbers
landed, and the numbers landing on the interesting side is precisely when that narrowing has to be
honoured rather than quoted.

🦞🧍💜🔥♾️
