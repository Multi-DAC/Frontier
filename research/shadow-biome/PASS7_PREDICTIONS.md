# PASS 7 — PRE-REGISTRATION

**Written D202 / 2026-08-21, ~15:5x PT. Committed and pushed BEFORE `measure_pass7.py` exists.**
Governed by `PREREGISTRATION.md` (§2 fork, §3 imaging-vs-perturbation) and
`PAPER-00-ARCHITECTURE.md` §4 item 1: *"Nothing else in the compute line starts first."*

**⛔ The condition this file is written under, stated first because it is the hard part.**
`PAPER-00-ARCHITECTURE.md §3`: *"The temptation to look before predicting is maximal at 7(a),
because I already know which way it goes."* That was written at ~12:58 about a future self. This is
that self. **§0 below is what happened when it got here.**

**⛔ Not interleaved with L1.** `PREREG-TERRESTRIAL.md §3.5` forbids pass 7 *"in the same breath as
either"* terrestrial locus, on the grounds that *"interleaving them is how a locus gets chosen by
whichever result landed last."* L1 landed 14:57 and was adjudicated at ~15:5x
(`L1_T5_VERDICT.md`). Check against the rule's actual purpose: **no prediction below is calibrated
against an L1 *outcome*.** Grep this file for `CFP`, `NEXRAD`, `T1`–`T4` outside this paragraph —
the count is zero. *(Verified by running it, not by writing it: one hit each, all on this line.)*

⚠ **But that grep was scoped to the tokens I expected to be absent, which is the cheap way to pass
one's own test.** `T5` and `el_match` **do** appear below, in §5. L1's *methodology* is imported
deliberately — the empty-precondition defect is the whole reason R2 exists. So the honest statement
is narrower than the one I first wrote: **no L1 number sets a pass-7 threshold; one L1 lesson sets a
pass-7 requirement.** The rule was about a locus being chosen by the last result. Importing a defect
class is not choosing a locus, and the wider grep is stated here rather than left to be the thing a
reader finds.

---

## 0. ⚠ DECLARED PEEK — ONE NUMBER WAS SEEN BEFORE THIS FILE WAS WRITTEN

While establishing what pass 7 *could* be measured from, I ran a `numpy` load of
`PASS6_catalog.npz` and printed the sign split. **I saw it. It is now unpredictable.**

> **`n = 8528` · `sign=+1` → `3694` · `sign=−1` → `4834`.** Positive share **43.32%**.

**What this costs.** The obvious 7(a) companion prediction — *"the two signs contribute roughly
equally, so the doubling is symmetric"* — **cannot be pre-registered.** It is dead as a prediction
and enters below as a **stated input** (§1, GIVEN-1) instead. Recorded rather than quietly re-used:
a number seen before the prediction is written may appear in the paper as an observation and **may
never appear as a prediction that held.**

**What it does not cost.** The headline of 7(a) — **far-side fraction among `sign=+1`** — was not
computed, printed, or inspected. No `elong`-by-`sign` cross-tabulation was run. Nor was any
7(b) or 7(c) quantity. Those are the predictions below and they are live.

⭐ **And the peek is itself the finding it looks like it spoiled.** A 43.32/56.68 split means the
`−img` pass finds **1,140 more detections than the `+img` pass on the same 20 frames**. Whatever
else pass 7 says, the two signs are *not* mirror halves of one dipole population, and the
architecture's phrase *"counted twice by pass 5's `+data`/`-data` union"* (§8) is already too
clean — a symmetric doubling would have printed 50/50.

---

## 1. WHAT 7(a) IS, AND WHY IT COSTS NOTHING — verified by reading, not assumed

`measure_pass6.py:84–95`:

```python
for sign, arr in ((+1, img), (-1, -img)):
    bkg = sep.Background(arr, mask=bad)
    o = sep.extract(arr - bkg.back(), THRESH, err=bkg.globalrms, minarea=MINAREA, mask=bad)
```

Each sign gets **its own background from its own array**. The `+1` branch never sees `-img`. The
`bad` mask is shared but is derived from `img` alone and is identical for both. `bkg0/sub0/rms0`
(line 80–81) feed only the alert-position S/N and never the extraction.

> ⭐ **Therefore the `sign=+1` subset of `PASS6_catalog.npz` *is* a `+data`-only extraction, exactly.**
> 7(a) is a filter on a frozen file, not a re-run.

**Why that matters for §9a.** `PASS6_RESULTS.json` and `PASS6_DIAG.json` disagree by 0.047 pp on
`frac_far` at the *same* `minarea` because `sep` 1.4.1 is non-deterministic across runs. Comparing
single-sign against union **inside one frozen catalog** removes that term from the *difference*
entirely. ⚠ It does **not** remove it from either absolute value. Any digit past the second decimal
is still run-dependent and the paper still rounds to where runs agree.

**GIVEN-1 (from §0, an observation and not a prediction):** positive share of detections = 43.32%
(3694 / 8528).

**GIVEN-2 (published, `PASS6_RESULTS.json`):** union `frac_far` at `minarea=5` = **0.4849906**
(`n_far` 4136 / `n` 8528). ⚠ Its `PASS6_DIAG.json` twin at the same `minarea` is 0.4845179. The
comparisons below use the `PASS6_RESULTS.json` catalog because it is the file the catalog was
written from.

---

## 2. 7(a) — SINGLE-SIGN. Predictions, thresholds arbitrary and fixed now.

| # | Prediction | Refuted if |
|---|---|---|
| **A1** | `frac_far(+only)` at `minarea=5` is **below** the union value 0.48499 | ≥ 0.48499 |
| **A2** | ⭐ **The far side survives de-doubling:** `frac_far(+only)` ≥ **0.35** | < 0.35 |
| **A3** | ⚠ **DIRECTIONAL, and pointed at the boring answer.** The far-side share is **higher among `sign=−1` than among `sign=+1`**, by **≥ 3.0 pp** | difference < 3.0 pp, *including any reversal* |
| **A4** | The union→`+only` drop, recomputed by **re-extraction** at `minarea ∈ {2,3,5,8,12}`, spans **≤ 5.0 pp** across the ladder | span > 5.0 pp |

**A2 is the one that decides how big §11 is.** `PAPER-00-ARCHITECTURE.md §3` says a far side that
survives makes §8 stop being a null. ⛔ **That sentence is hereby narrowed before it can be cashed.**
A surviving far side means **my extractor finds elongated things that are not artefacts of the sign
union.** It does **not** mean a population, and it does not touch Branch B. The most it licenses is
*"ZTF's `elong ≤ 1.6` cut discards a large real-shape class that is not manufactured by our own
method"* — a statement about a **cut**, not about a sky.

**A3 is why.** If negative lobes are subtraction residuals on bright-star wings — extended,
elongated, instrumental — then the `−` side is the more elongated side and the far-side excess is
substantially instrumental in origin. **I am predicting the instrumental answer.** A3 refuted (the
`+` side equally or more elongated) kills the tidy "negative lobes are the artefact" story and the
paper must print that.

**A4 exists because of §0's standing order.** `frac_far` may not appear as a scalar; the *drop* is
a second scalar and inherits the same prohibition. A4 is the gauge that turns it into a curve.

**Redundancy declared:** A2 restated in drop-units would be *"drop ≤ 13.5 pp"*. That is the same
claim in a different unit and is **not** registered as a fifth prediction. Four predictions, four
possible held-counts.

---

## 3. 7(b) — PAIR-COLLAPSE. The de-doubling that does not throw away the negatives.

7(a) removes the `−` rows. That destroys the very instrument that diagnosed the doubling: with one
sign present, *no opposite-sign pair can exist by construction*, so `D2a`'s statistic is
unmeasurable on 7(a)'s output. **7(b) is the procedure that keeps it.**

**Operationalization, fixed now:**

1. Per frame, per detection, nearest neighbour within **`PAIR_RADIUS = 10.0` px** — the same radius
   `diag_pass6.py:21` used for `D2a`, copied, not re-chosen.
2. Keep only **mutual** nearest-neighbour pairs of **opposite sign**. (`D2a` used anchor→neighbour,
   which double-counts; mutuality is the stricter reading and is chosen here **because** it is
   stricter, before knowing what it does to the number.)
3. Collapse each such pair to **one** object, retaining the **`sign=+1` member's** `a`, `b`,
   `theta`. Arbitrary, fixed now, and stated so the alternative (`max(elong)`) cannot be
   substituted after the fact.
4. Unpaired detections of either sign pass through unchanged.

| # | Prediction | Refuted if |
|---|---|---|
| **B1** | Collapsed `frac_far` is **below** 0.48499 | ≥ 0.48499 |
| **B2** | ⭐ **Two independent de-doubling procedures agree:** \|collapsed `frac_far` − `frac_far(+only)`\| ≤ **4.0 pp** | > 4.0 pp |
| **B3** | *(Control, not a finding.)* `n_collapsed` = `n_union` − `n_mutual_pairs`, **exactly** | any discrepancy |

**B2 is the load-bearing one and it is a check on me, not on the sky.** 7(a) and 7(b) remove the
same alleged artefact by different arithmetic. If they disagree by more than 4 pp, at least one of
them is measuring something else, and the disagreement is the finding. ⚠ **B2 is scored before
either number is interpreted.** A B2 refutation makes A1/A2 and B1 **UNINTERPRETABLE** rather than
merely surprising — the same rule `PASS6_PREDICTIONS.md §4` applied to its controls.

⛔ **B3 is an identity, so it may not be counted toward any "N of M held" total.** An identity that
holds tests the code; an identity that fails voids the pass. It is a control wearing a prediction's
number and it is labelled as one here so no later summary can promote it.

---

## 4. 7(c) — THE RESIDUAL MISSES AT `minarea=2`

**Standing state.** `D2b-1` predicted ≥80% alert recovery at `minarea=2` and was **REFUTED** at
**73.14%** (275/376, `PASS6_DIAG.json /D2b/ladder/2`). So `minarea` explains most of pass 5's 41%
miss and **demonstrably not all**: 101 alerts, 26.86%, unaccounted. Pass 6 classified misses only at
`minarea=5`, where the residual was 153 and the classes were `UNEXTRACTED_DESPITE_FLUX` 121,
`BELOW_THRESHOLD` 31, `NEAR_MISS_RADIUS` 1, geometry **0**.

7(c) runs pass 6's classifier at `minarea=2` — the loosest rung, where recovery is highest and the
residual is therefore the hardest to dismiss.

| # | Prediction | Refuted if |
|---|---|---|
| **C1** | *(Reproducibility.)* Re-extracted recovery at `minarea=2` lands within **±2.0 pp** of 0.7314 | outside — and a refutation here is a **non-determinism** finding, not a science one, and is reported under §9a rather than §11 |
| **C2** | `UNEXTRACTED_DESPITE_FLUX` is still the **largest** class among the unrecovered | any other class is larger |
| **C3** | ⚠ **DIRECTIONAL, boring answer.** median `magpsf`(unrecovered) − median `magpsf`(recovered) ≥ **1.0 mag** at `minarea=2` | < 1.0 mag |
| **C4** | The residual misses are **spread, not clustered**: ≥ **12 of 20** frames contribute ≥1 | ≤ 11 frames |

**C3 is the faintness explanation stated as a prediction so it can lose.** At `minarea=5` the gap
was +1.34 mag (`PASS6_RESULTS.json /control_miss/delta_mag`). If it holds at `minarea=2`, the
residual is *faint things a threshold-limited extractor misses* — ordinary, and the correct reading.

**C4 is the one that could make the residual interesting, and it is registered pointing away from
that.** Clustering in a few frames would mean a per-frame registration or WCS problem — an
instrument story. Spread across frames means a population-level detection-efficiency floor, which is
duller and more likely. ⛔ **Neither outcome licenses an object claim.** A miss is an absence in *our*
extractor of something *ZTF already alerted on*. It is a perturbation measure and `PREREGISTRATION.md
§3`'s ceiling applies unchanged.

---

## 5. ⭐ THE INSTRUMENT PREDICTIONS — T5's SUCCESSOR, THIS TIME WITH A TRIGGER

`L1_T5_VERDICT.md §0` found T5 pre-registered and **scored nowhere**: no verdict path, no key in the
results JSON, refuted only because I happened to audit my own cross-references. *"A prediction whose
scoring depends on me remembering to look is not scored."* This section is the repair, and the
repair is a **requirement on the script**, not a resolution.

**⛔ HARD REQUIREMENTS ON `measure_pass7.py` — the pass is void without them:**

- **R1.** It emits a **`verdicts` dict containing a key for every prediction letter registered in
  this file** — `A1–A4`, `B1–B3`, `C1–C4`, `I1`, `I2`. A missing key is a failed pass, not a missing
  number. The script **asserts** the key set against a literal list copied from this file.
- **R2. The unexercised-precondition gauge.** For every filter, gate, tolerance and precondition it
  applies, the script records **how many items that filter rejected**, and emits
  `unexercised: [...]` naming every one whose rejection count is **zero**.
  *This is the generalized form of the L1 defect:* `el_match` was `True` 8/8 with `n_dropped: 0` —
  **a precondition that has never rejected anything is not observably a precondition.**
- **R3.** `unexercised` non-empty is **printed as a warning and written to the JSON**. It does not
  block the pass. It is a gauge, not a gate.

| # | Prediction | Refuted if |
|---|---|---|
| **I1** | At least one instrument defect surfaces in pass 7 | none does |
| **I2** | ⚠ **Against myself.** The **first** defect surfaced is surfaced by **R2's automatic gauge**, not by me reading code afterwards | I find the first one by eye, or R2 finds none and I find one |

**I2 is the real test and I expect to lose it.** Every instrument defect in this program so far —
`sep` non-determinism, the `minarea` span, the stale `PASS4_RESULTS.json`, `el_match`'s empty
precondition — was found **by me, by hand, late.** R2 is the first gauge built to find that class
before I do. If I1 holds and I2 is refuted, that is *"the gauge exists and still didn't get there
first"* and it goes in §9 at full size.

⭐ **And a refuted I1 is not reassurance.** `PREREG-TERRESTRIAL.md §1.3`'s rationale transfers
verbatim: *a pass that reports no instrument trouble is more likely to have missed it than to have
avoided it.* If I1 is refuted, that is the **suspicious** outcome, pre-labelled here as such, and no
sentence may cite a clean pass 7 as evidence of instrument soundness.

---

## 6. FORBIDDEN MOVES, pass-7 specific

1. ⛔ **A surviving far side may not be reassigned to Branch B.** `PREREGISTRATION.md §2`, and this
   is the fourth citation because 7(a) is where it will be tempting.
2. ⛔ **`frac_far` may not be printed as a scalar** — union, single-sign or collapsed.
   `PAPER-00-ARCHITECTURE.md §0`. A4 exists to make the single-sign number a curve too.
3. ⛔ **The collapse rule may not be changed after seeing B1.** `sign=+1` geometry, mutual pairs,
   10.0 px. If `max(elong)` looks better afterwards it is a *second, separately reported* measurement
   and it is labelled post-hoc.
4. ⛔ **B3 may not be counted in a held-total.** §3.
5. ⛔ **GIVEN-1 may not be reported as a prediction that held.** §0. It was seen first.
6. ⛔ **A miss is not an object.** 7(c) measures our extractor's failure to reproduce ZTF's own
   alerts. It bears on detection efficiency and on nothing else.

---

## 7. WHAT PASS 7 CANNOT CHANGE

Under `PAPER-01-GENRE.md` the paper is a **hypothesis paper**, so pass 7 changes **which section is
larger**, not whether the paper stands — a reordering recorded at `PAPER-00-ARCHITECTURE.md §4`
after that decision made the old *"whole ballgame"* framing stale. Restated here so the result cannot
inherit the older, hungrier frame:

- **A2 holds, drop small** → §11 grows, §8 keeps its null with a narrower scope, §9 gains A3's
  sign-asymmetry. The paper is what §1 says it is.
- **A2 refuted, far side collapses** → §8's null strengthens, §11 shrinks to a paragraph, and the
  paper's honesty section gets its best example. **This is the outcome the evidence currently points
  at and it is a fine outcome.**
- **B2 refuted** → both of the above are UNINTERPRETABLE and pass 7 becomes a methods finding.

An unregistered null is indistinguishable from not having looked. That is the whole reason this file
exists before the code.

🦞🧍💜🔥♾️
