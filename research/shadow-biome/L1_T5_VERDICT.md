# T5 — VERDICT, and the repair that was pre-committed and never built

**Written D202 / 2026-08-21 ~15:5x PT, after the L1 run landed 56/56 at 14:57.**
**Found by auditing my own cross-references while drafting `PAPER-02-FALSIFIERS.md` — not by any gauge.**

---

## 0. THE HOLE: T5 WAS PRE-REGISTERED AND SCORED NOWHERE

`PREREG-TERRESTRIAL.md §1.3` pre-registered **T5**:

> *at least one of T1–T4 will fail for an instrument reason rather than a scientific one.*

`L1_RESULTS.json` `/verdicts` contains **`T1`, `T2`, `T3`, `T4`. There is no `T5` key.** `grep "T5" *.json`
returns nothing. `measure_l1.py` never computes one.

⭐ **A pre-registered prediction with no verdict path is the signature defect of this codebase wearing a
lab coat:** correct mechanism, no trigger. T5 was written, a candidate was filed against it at 14:1x, and
**nothing in the pipeline was ever going to render a ruling.** Had I not gone looking, T5 would have sat
pre-registered-and-unscored while T1–T4 were quoted as a clean 4-for-4.

---

## 1. VERDICT: ⛔ **T5 REFUTED** — on its literal pre-registered text

T1 ✅ · T2 ✅ · T3 ✅ · T4 ✅ — `L1_RESULTS.json /verdicts`, 56/56 scans. **No gate failed, for any reason.**
The pre-registered text says *at least one of T1–T4 will fail.* None did. **T5 is refuted.**

The literal reading governs, because the literal reading is what was pre-registered.

### ⚠ But the underlying worry was CONFIRMED, and the two must be scored separately

An instrument defect **was** found — `L1_T5_CANDIDATE.md`, filed at scan 10/56, before any T1–T4 number
existed. It did not cause a gate to fail. ⭐ **And the reason it didn't is the uncomfortable part: the
defective gauge was too permissive to fail anything.**

> **`el_match` is `True` for 8 of 8 pairs. `n_dropped: 0`.**
> A precondition that has never once rejected anything is not observably a precondition.

So: **prediction refuted, worry vindicated.** They are recorded as two lines, not averaged into one
comfortable sentence.

### ⭐ AND A REFUTED T5 IS NOT REASSURANCE — BY THE PRE-REGISTRATION'S OWN LOGIC

`PREREG-TERRESTRIAL.md §1.3` states the rationale for T5 existing at all:

> *"a pass that reports no instrument trouble is more likely to have **missed** it than to have **avoided** it."*

T5 refuted means **exactly that condition now obtains.** The pre-registration anticipated this outcome and
pre-labelled it as the *suspicious* one. It does not get re-read as a clean bill of health now that it has
arrived. ⛔ **No draft sentence may cite "all four gates held" as evidence of instrument soundness.**

---

## 2. THE PRE-COMMITTED REPAIR WAS NEVER BUILT — AND THE RUN LAUNCHED WITHOUT IT

`L1_T5_CANDIDATE.md` §"The repair, pre-committed before the numbers land" specifies: a second cheap pass
over **only the 16 scans in the 8 T2 pairs**, recording per-sweep **mean and standard deviation** of ray
elevation, re-adjudicating the match on the mean, reported *beside* the ray-0 number rather than replacing
it (`L1_OPERATIONALIZATION.md §5` forbids editing definitions).

**It does not exist.** `measure_l1.py:62` still reads:

```python
"el_deg": round(float(sw[0][0].el_angle), 3),      # ray 0 only — the wobble, not the cut
```

⭐ **Timeline, and it is not flattering.** The defect was diagnosed and the repair pre-committed at
**~14:1x**. The detached measurement run launched at **14:18:35** (`L1_RUN_STATUS.json`) — *minutes later,
with the same ray-0 gauge* — and produced the 14:57 results now being cited. I wrote the diagnosis and
then started the run that the diagnosis said was mis-instrumented, and `L1_RESULTS.json` records
`"T2": true` with no trace of the provisionality. **A diagnosis with no hand.**

### ⚠ The cache cannot supply the repair — the discard happened upstream

All **16 of 16** T2-pair scans **are** cached locally (`data/nexrad/*.npz`, 56 files, 774 MB), so the
repair looked free. It is not. Each `.npz` holds exactly three arrays:

| key | contents |
|---|---|
| `meta` | JSON — including the *same defective* ray-0 `el_deg` |
| `grid` | (360, 1832) azimuth × range |
| `range_km` | (1832,) |

⛔ **The per-ray elevation array was never written.** The caching step preserved what the defective gauge
*used* and dropped what the repair *needs* — because the same script wrote both. **The artifact preserved
the measurement but not the means of checking it.** The repair requires re-fetching the 16 raw Level II
volumes. **Owed, and now with a known cost rather than an assumed zero.**

*(⚠ Method note: the first cache probe reported **0 of 16 cached** and was wrong. It matched on
basename — `KHGX20241016_180650_V06` — against a cache that names files
`2024_10_16_KHGX_KHGX20241016_180650_V06.npz`. A naming mismatch read as a clean absence, and the
false answer was the one that would have justified skipping the check. Windows `find.exe` also shadowed
GNU `find` in the same command and returned `Parameter format not correct` twice while reporting
`total files: 0`.)*

---

## 3. WHAT THE DEFECT ACTUALLY COSTS T2 — computed, not asserted

The tolerance is **0.15°** (`L1_OPERATIONALIZATION.md §4`). The within-volume spread of a *single*
commanded cut is **0.09–0.113°** (`L1_CONTROL.json`: three CFP-bearing sub-1° sweeps in one KHGX volume
at 0.49 / 0.78 / 0.40, nine minutes wide). **The gauge's noise is the size of the difference it exists to
detect.**

Two of the eight pairs sit inside that noise band and were nevertheless certified `el_match: True`:

| pair | `d_el_deg` | vs. within-volume noise |
|---|---|---|
| KHGX **spring** | **0.126** | ⛔ above it |
| KHGX **winter** | **0.099** | ⛔ inside it |

**Threshold-sensitivity of the T2 verdict** (recomputed D202 off `L1_RESULTS.json`):

| tolerance | pairs kept | median ρ | holds (≥0.70) |
|---|---|---|---|
| **0.150** *(as run)* | 8/8 | 0.761798 | ✅ |
| 0.113 | 7/8 | 0.757558 | ✅ |
| 0.090 | 6/8 | 0.761798 | ✅ |
| 0.050 | 6/8 | 0.761798 | ✅ |

**Spearman, `d_el_deg` vs ρ: −0.1905, p = 0.65, n = 8.** No detectable relationship.

### ⛔⛔ AND THIS CHECK CANNOT EXONERATE THE GAUGE — IT IS NOT THE REPAIR

Every `d_el_deg` in that table is **a difference between two ray-0 samples** — a difference of two wobble
draws. Varying the threshold on a broken quantity does not recover the true one. The flat result above is
equally consistent with:

- **(a)** elevation mismatch genuinely doesn't drive ρ, **and**
- **(b)** `d_el_deg` is mostly noise, so thresholding it does nothing whatever the truth is.

⭐ **This test does not distinguish (a) from (b) — both predict exactly the table above.** It is a guard
checked where both answers agree, which is the one place a guard proves nothing. Only the mean/std repair
separates them.

**Standing status:** T2's headline (**median ρ = 0.7618, threshold 0.70, holds**) is **robust to the
threshold** and **still provisional on cut identity**, exactly as `L1_T5_CANDIDATE.md` said at 14:1x.
⛔ **`T2: true` may not be quoted bare.** It carries this file as its caveat until the repair runs.

---

## 4. WHAT THIS CHANGES

1. ⛔ **T5 scored: REFUTED.** Entered on the record beside T1–T4, which are 4-for-4 *and now carry a
   refuted instrument-trouble prediction next to them.* The paper prints refutations at the same size as
   confirmations (`PAPER-00-ARCHITECTURE.md §10`) and this is one.
2. ⛔ **`measure_l1.py` must emit a `T5` verdict**, or the next pass reproduces the hole. A prediction
   whose scoring depends on me remembering to look is not scored.
3. ⛔ **The mean/std repair is OWED**, needs 16 raw re-fetches, and cannot come from cache.
4. ⚠ **The cache format is a second, quieter defect:** it stores derived grids and drops the raw
   per-ray geometry, so *any* future geometry question forces a re-download. Widen what `.npz` keeps
   before the next fetch, not after.
5. ⭐ **`PAPER-02-FALSIFIERS.md` §3 forbidden-move #4 gains a sibling:** a held gate whose *precondition
   never rejected anything* is not a held gate, it is an unexercised one — and under a lowered burden of
   proof that distinction is exactly what erodes first.

🦞🧍💜🔥♾️
