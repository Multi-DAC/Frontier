# PASS 9 — PRE-REGISTRATION

**Written D202 / 2026-08-21, ~23:2x PT. Committed and pushed BEFORE `measure_pass9.py` exists.**

Opened on Clayton's ruling: *"I say we run it, and I'm fine with that being a successor. I'd
rather have it be ready and complete the full paper at once instead of having to redraft after the
final pass."* That settles both open forks — **pass 9 runs before §11 is drafted**, and **§15 ships
as a pre-registered successor, not as a result.**

Governed by `PREREGISTRATION.md` (§2 fork, §3 imaging-vs-perturbation) and by
`PAPER-00-ARCHITECTURE.md §4 item 2b`, which books **three** debts against pass 8, each requiring
*"its own pre-registration before the code"*:

- **(i)** ⭐ **P_D** — drop **both** members of every mutual opposite pair — with its `minarea`
  curve. Currently post-hoc at `frac_far` 0.422997.
- **(ii)** `found_by` written **at find time** rather than backfilled, because
  `DEFECT_REGISTER.json`'s denominator is mine.
- **(iii)** a `citable()` that **can fail** — pass 8's rejected **0 of 12**, which is why G2's
  refutation is uninterpretable by the run's own R3 warning.

This pass adds a fourth block that nobody booked, and it is the one most likely to hurt:

- **(iv)** ⭐ **BLOCK S — a scramble control on the pair finder.** Passes 7, 8 and now 9 all rest on
  `pair_mask()`, and **it has never been shown a case where it should find nothing.** Every number
  in the P_A/P_B/P_D family inherits that. `feedback_zero_needs_a_positive_control`.

⚠ **The condition this file is written under.** Pass 8 warned that the temptation drops when no
headline rides on the pass. Pass 9 is the opposite case: **P_D is the largest move any procedure in
this program has produced (−6.20 pp) and I like it.** That is the dangerous condition, not the safe
one. Block S exists because I like P_D.

---

## 0. ⚠ DECLARED PEEKS — everything seen between the pass-8 push and this line

**Peek 1 — `PASS8_RESULTS.md §1–§4`, read in full.** All of P_D's post-hoc numbers are known to me:
`P_D` n=3870, `frac_far` 0.422997, move −6.199 pp; the pair population alone n=4658,
`frac_far` 0.536496; `P_A` 3694/0.548728; `P_B` 6199/0.482820; union 8528/0.484991.
**Consequence: the frozen-catalogue value of P_D is an OBSERVATION and is not scored.** It appears
below only as **P0**, a reproduction control, on the same footing as pass 8's D1.

**Peek 2 — `measure_pass8.py`, read in full**, including `pair_mask()`, `citable()` and the
register. Deliberate: Blocks C and S are *derived by reading it*, and the derivation is published
here before the run.

**Peek 3 — `verify_pass6.py` in full, and `PASS6_VERIFY.json` `/V2` verbatim**, both sides:

> `far`: anchors 4136 · paired 2828 · paired_share 0.68375 · opp_rate 0.96252 · null 0.47207 ·
> med_delta 77.872° · opp_share_of_side 0.65812
> `kept`: anchors 4392 · paired 2309 · paired_share 0.52573 · opp_rate 0.97315 · null 0.43386 ·
> med_delta 69.799° · opp_share_of_side 0.51161

**What this costs.** P5 below re-runs that analysis **on the P_D survivors**, which I have not
computed. The *union* baselines are known; the *survivor* values are not. P5 is scored against
survivor values only, and the union numbers above may never be reported as a prediction that held.

**Peek 4 — two of the three `line:` citations in the register, read verbatim.**
`diag_pass6.py:114` is `img = np.ascontiguousarray(hdu.data.astype(np.float32))`.
`pass6_stats.py:1` is `"""Shared circular/spatial statistics for pass 6.`
⛔ **This directly informs C2 and I am not pretending otherwise.** C2 is therefore written in the
strongest form a peeked prediction can take: **it names which row it expects to fail, in advance,
and which two it expects to survive.** A bare "≥1 of 12 fails" would have been unfalsifiable given
what I have already seen. **`measure_pass7.py:352` was NOT opened** — DEF-04 is unpeeked and is the
honest half of C2.

**Peek 5 — `PASS6_catalog.npz` key list and dtypes.** No values read beyond `n = 8528`, published.

No other file was opened. No extraction was run. `measure_pass9.py` does not exist.

---

## 1. BLOCK P — P_D, PRE-REGISTERED

### 1a. What P_D is, stated so the code cannot drift from it

`pair_mask()` marks detection *i* paired iff its nearest neighbour *j* on the same frame is within
`PAIR_RADIUS = 10.0` px, the relation is **mutual** (`nn[j] == i`), and `sign[i] * sign[j] < 0`.

| procedure | rule | n (frozen) |
|---|---|---|
| union | everything pass 5/6 extracted | 8528 |
| `P_A` = 7(a) | `sign > 0` only | 3694 |
| `P_B` = 7(b) | drop the `−` member of each mutual opposite pair | 6199 |
| ⭐ `P_D` | drop **both** members of every mutual opposite pair | 3870 |

**P0 — REPRODUCTION CONTROL.** An independently written `P_D` (build it as `~paired`, not by
negating pass 8's `drop` array) gives `|P_D| = 3870` and `frac_far = 0.422997` to all printed
digits.
→ **A failure here means `PASS8_RESULTS.md §2`'s table is void and pass 9 stops.**
**EXCLUDED from the held/refuted total**, exactly as D1 and B3 were.

### 1b. The ladder — the part that is actually unknown

The frozen catalogue is one point on a `minarea` curve, and `PAPER-00-ARCHITECTURE.md §9` already
establishes that a single point on that curve is not even a fixed number. P_D has never been
computed anywhere but at `minarea = 5`. Re-extraction over `MINAREA_LADDER = [2, 3, 5, 8, 12]`,
20 images, same constants as passes 6–8 (`THRESH 5.0`, `WALL 1.6`, `PAIR_RADIUS 10.0`).

- **P1** — `frac_far(P_D) < frac_far(union)` at **≥ 4 of 5** rungs.
  *Why it could fail:* at `minarea = 2` the catalogue fills with small marginal detections whose
  nearest neighbour is close by accident; the pair population may stop being the elongated class.

- **P2** — the move `|frac_far(P_D) − frac_far(union)|` is **≥ 3.0 pp at ≥ 3 of 5** rungs.
  *This is the prediction that P_D is a real effect and not a `minarea = 5` accident.* Sign alone
  is cheap; magnitude is what §11 would have to print.

- **P3** — `frac_far(pair members only) > frac_far(union)` at **≥ 4 of 5** rungs.
  *The claim under test is "the pairs are the elongated class."* P1 and P3 are the same fact from
  two sides and **must agree**; a rung where one holds and the other does not is a defect, reported.

- **P4** — **pair share rises as `minarea` falls**: `pair_share(minarea=2) > pair_share(minarea=12)`,
  where `pair_share = n_paired / n`. *Predicts that some of the pairing is density-driven
  coincidence* — which, if true, is an argument against P_D that I am registering **before** the
  scramble control can make it for me.

### 1c. P5 — the one that can void every pair-based number in passes 7–9

`PASS6_VERIFY.json /V2` measures, per side of the `elong = 1.6` wall, the share of detections
sitting in an **opposite-sign close pair by nearest-neighbour** (not necessarily mutual). On the
union: far **0.65812**, kept **0.51161**, far-minus-kept **+14.65 pp** — the number
`PAPER-00-ARCHITECTURE.md §8` rests on.

**P_D removes the mutual pairs. Re-run V2 on the survivors.** Because V2's pairing is
*non-mutual*, survivors can still have an opposite-sign neighbour within 10 px, so this is **not**
true by construction.

- **P5** — on P_D survivors, far-minus-kept `opp_share_of_side` falls to **≤ +5.0 pp**
  (from +14.65 pp).
- **P6** — on P_D survivors, the opposition excess `opp_rate − null` on the **far** side falls
  **below +20.0 pp** (from +49.04 pp).

⛔ **Pre-committed reading if P5 or P6 is REFUTED:** the far-side dipole structure survives removal
of every mutual opposite pair, which means `pair_mask()` is **under-inclusive** — it is finding a
subset of the dipole population, not the population. In that case **every P_A/P_B/P_D number in
passes 7, 8 and 9 is a lower bound on the artefact, not a measurement of it**, and the paper must
say so in §11 in those words.

---

## 2. ⭐ BLOCK S — THE SCRAMBLE CONTROL THE PAIR FINDER HAS NEVER HAD

`pair_mask()` has only ever been shown real data, where it always finds pairs. A gauge shown only
the case it is expected to fire on has not been tested (`feedback_gauge_can_only_render_its_good_news`).

**The scramble, specified so it cannot be tuned afterwards.** Within each frame, translate every
`sign < 0` detection by a fixed offset `(dx, dy)`, wrapping each coordinate into the observed
`[min, max]` range of that frame's detections. Positives are untouched. **Eight fixed offsets**,
no RNG anywhere: `(±40, 0)`, `(0, ±40)`, `(+40, +40)`, `(+40, −40)`, `(−40, +40)`, `(−40, −40)`.
40 px is 4× `PAIR_RADIUS`. Report the **median** over the eight.

This destroys the physical registration of a dipole while preserving n, the sign composition, the
per-frame density and the clustering of each sign separately.

- **S-NULL — GATE, excluded from the total.** Every scramble preserves `n` exactly, preserves the
  multiset of signs exactly, and preserves `frac_far(union)` exactly (elongation is not moved).
  → **If S-NULL fails the scramble is not a scramble and Block S reports nothing.**

- **S1** — median scrambled mutual-opposite-pair count is **≤ 50%** of the observed 2329.
  *If it is not, most "pairs" are chance coincidence at this density and P_D is deleting a
  spatially-defined arbitrary subset.*

- **S2** — median `|frac_far(P_D_scrambled) − frac_far(union)|` is **≤ 2.0 pp**, against the
  observed 6.199 pp.
  *S1 is about how many pairs chance produces; S2 is about whether chance pairs are elongated.
  S2 is the one that matters — a chance-pair population should be a fair sample of the catalogue
  and move `frac_far` by roughly nothing.*

⛔ **Pre-committed reading if S2 is REFUTED** (chance pairs also move `frac_far` by ≥ 2 pp): the
mutual-nearest-neighbour construction **selects elongated detections by geometry alone**, and P_D's
−6.20 pp is at least partly an artefact of the pair *finder* rather than of the dipole *population*.
§11 then reports the union and states P_D as unexplained. **This is the outcome I am betting
against, which is exactly why it is written down first.**

---

## 3. BLOCK C — A `citable()` THAT CAN FAIL  (pass-8 debt iii)

Pass 8's `citable()` checks that a `file:` exists, that a `line:` file has at least that many lines,
and that a `json:` pointer resolves. It **rejected 0 of 12** — R3 flagged it, and G2's refutation is
uninterpretable in consequence.

**The strengthening: every citation is ANCHORED.** Each register row carries `anchor`, a literal
substring, and a `line:` or `file:` cite resolves only if the cited location **contains** it. A
line-number citation into a file that is still being edited rots silently; anchoring is the gauge
that fails on its own.

- **C1 — POSITIVE CONTROL, GATE, excluded from the total.** The strengthened `citable()` is run
  against **six** hand-built known-bad citations, fixed here:
  `file:NO_SUCH_FILE.md` · `line:measure_pass8.py:999999` ·
  `line:measure_pass8.py:1|ZZZ_NOT_IN_THIS_LINE` · `json:PASS8_RESULTS.json:/no/such/pointer` ·
  `json:NO_SUCH_FILE.json:/D1` · `file:PASS8_RESULTS.md|ZZZ_NOT_IN_THIS_FILE`.
  → **It must reject 6 of 6.** Rejecting fewer means Block C reports nothing and G2 stays
  uninterpretable for a second pass running.

- **C2 — the named prediction.** Under anchoring, **`DEF-10` fails** (its cite `line:diag_pass6.py:114`
  points at an `ascontiguousarray` line, not at the `Background`/`bkg0` structure the row
  describes), and **`DEF-04` (`line:measure_pass7.py:352`, unpeeked) and `DEF-02`
  (`json:PASS7_RESULTS.json:/I/unexercised`) both survive.**
  Scored as: **all three named outcomes correct.** Two of three is a refutation.

- **C3** — **≥ 2 of the 12 legacy rows fail anchoring**, i.e. DEF-10 is not alone.
  *Predicts that citation rot is systemic in this register and not a single slip.*

---

## 4. BLOCK F — `found_by` AT FIND TIME  (pass-8 debt ii)

Pass 8's G1 (*eye ≥ 2 × gauge*) is computed over a register **I** wrote, classified **after** the
fact, by **me**, about **my own** finding process. `feedback_self_generated_denominator`.

The repair is not a better backfill. It is a schema change: from pass 9 onward every row carries
`found_at` (the pass that found it) and `found_by_provenance ∈ {find-time, backfilled}`, and the
twelve legacy rows are **relabelled `backfilled` without exception**, including the ones I am
confident about.

- **F1** — pass 9 produces **fewer than 6** find-time rows.
  → therefore **G1 is UNDERPOWERED on find-time rows and is RETIRED, not re-scored.**
  ⛔ **Pre-committed:** if F1 holds, `PAPER-00-ARCHITECTURE.md` and any draft sentence citing G1
  must be amended to say the eye-vs-gauge ratio is **unmeasured**, not that it is 2:1. The pass-8
  G1 verdict does not survive into the paper either way — a held G1 on a backfilled denominator is
  not evidence, and this is the pass that says so.
  *Why it could fail:* Blocks P, S and C are three new gauges pointed at old code. Six find-time
  defects is not an absurd yield.

---

## 5. RUN RULES, CARRIED FORWARD UNCHANGED

- **R1** — a verdict key exists for every registered letter, asserted against a literal list:
  `[P0, P1, P2, P3, P4, P5, P6, S-NULL, S1, S2, C1, C2, C3, F1, R4-CONTROL]`.
- **R2** — every gate records its rejections; zero-rejection gates are named in an R3 warning.
- **R4** — no two verdicts share a `(quantity, threshold, comparator)` triple.
- **R4-CONTROL** — ⭐ **changed from pass 8.** Pass 8 ran R4 against pass 7's known-bad I1/I2 pair.
  That input is now permanently available and re-firing on it proves nothing new. Pass 9 instead
  **injects a deliberate duplicate triple into a copy of pass 9's own verdict set** and requires R4
  to fire on it. A gauge must be tested against *this* run's shape, not a preserved historical one.
  **EXCLUDED from the total.**
- **EXCLUDED from the held/refuted total:** `P0`, `S-NULL`, `C1`, `R4-CONTROL`. Everything else is
  scored. **11 scored predictions: P1 P2 P3 P4 P5 P6 S1 S2 C2 C3 F1.**

---

## 6. WHAT PASS 9 DOES TO THE PAPER — the decision rule, written before the data

| outcome | §8 | §11 |
|---|---|---|
| **P1 ∧ P3 ∧ S1 ∧ S2 hold** | "counted twice" stays refuted; the standing sentence is *the mutual opposite-sign pairs are an elongated artefact class* | headline residual is `frac_far(P_D)`, with union and `P_A` printed beside it and the spread stated |
| **S2 refuted** | unchanged | union is the headline; P_D is reported **as unexplained**, with the scramble number printed next to it |
| **P1 refuted on the ladder** | unchanged | P_D is a `minarea = 5` result and is reported only at `minarea = 5`, labelled |
| **P5 or P6 refuted** | ⛔ amended: `pair_mask()` is under-inclusive | every pair-based number in passes 7–9 is stated as **a lower bound on the artefact**, in those words |
| **F1 holds** | — | G1 is retired; the eye-vs-gauge ratio is reported as **unmeasured** |

⛔ **STANDING FENCE, unchanged and restated because this is the pass with a result I want:** a null
in the device-detectable branch **stays** in the device-detectable branch and may never be reframed
as "consistent with" the undetectable branch (`PREREGISTRATION.md §2`). Nothing in Block P, S, C or
F bears on Branch B. `frac_far` under any procedure is a statement about **elongated detections in
ZTF difference images** and about nothing else.

---

*Written before `measure_pass9.py` exists. If the file's git timestamp does not precede the
script's, this document is worthless and should be read as narration.*
