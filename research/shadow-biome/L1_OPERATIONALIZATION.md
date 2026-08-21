# L1 OPERATIONALIZATION — the degrees of freedom in T1–T4, pinned before the first measurement

**Written D202 / 2026-08-21, ~13:5x PT. Committed and pushed BEFORE `measure_l1.py` is run.**
Governed by `PREREG-TERRESTRIAL.md §1.2` (the ceiling), `§1.3` (T1–T5), and `L1_CONTROL.json:finding_C1`
(CFP is **detection-conditional** — a gate with no above-threshold return has no CFP value at all).

⛔ **STATE AT WRITING: exactly one volume scan has been decoded in this program** — the KHGX autumn
solar-noon control, `2024/10/16/KHGX/KHGX20241016_180650_V06`. The other 55 keys in `L1_SAMPLE.json`
have been *listed* (name, byte size, start time) and never fetched. No T1–T4 number exists.

---

## 0. Why this file exists

`PREREG-TERRESTRIAL.md §1.3` names four predictions and their refutation thresholds. It does **not** say
what "the non-stationary residual" *is* as an array of numbers. That is at least four free choices —
baseline estimator, difference statistic, grid, and the treatment of gates that are finite in one scan
and absent in the other — and every one of them can be tuned toward a held prediction after the fact.

The thresholds were fixed in advance. **Fixing a threshold on an unspecified statistic is not a
pre-registration**, so the statistic gets pinned here, on the same terms: written first, arbitrary where
arbitrariness is honest, and quoted afterwards whatever it says.

---

## 1. THE GRID — how two scans are made comparable

A volume scan's rays are not aligned across time; azimuth is a float that drifts. So each scan is reduced
to a fixed lattice:

- **Sweep selection**: the **FIRST CFP-bearing sweep** in the volume (`L1_CONTROL.json`'s adopted rule,
  forced by split cuts and SAILS — the Doppler half of each split cut carries no CFP). Its elevation is
  recorded per scan.
- **Azimuth**: 360 bins of 1.0°, bin *k* = [k, k+1). Cell value = **mean of the finite CFP values** of
  rays falling in that bin. A bin with no finite value is NaN, not zero.
- **Range**: gate index, after asserting `first_gate` and `gate_width` match between any two scans being
  compared. Comparison is truncated to the shorter gate count. A mismatch in gate geometry is recorded
  and that pair is **dropped, not resampled** — resampling a mismatch is how an instrument difference
  becomes a science result.
- **Range cap**: 460 km, the control's own max range.

Cell count is therefore 360 × N_gates, near-field (<50 km) being a small minority of cells. Every
statistic below is a **per-cell density**, never a total, so the near/far comparison in T3 is not decided
by cell count.

## 2. THE BASELINE — what "stationary" is measured against

Per **radar**, over that radar's **24 primary scans only** (partners are held out; they belong to T2):

> `baseline[cell] = median of the finite CFP values of that cell across the 24 scans`
> defined only where **≥ 12 of 24** scans are finite. Elsewhere the baseline is NaN.

Median, not mean, because a transient in one scan must not move the thing the transient is measured
against. The ≥50% support rule is the arbitrary one; it is chosen now.

⚠ **The baseline is contaminated by design.** It is built from the same scans whose residuals are taken
against it, including the dawn and dusk scans T4 compares. This makes T4 *conservative* — a real dawn
excess raises the baseline it is scored against — and it makes no difference to T3's near/far contrast,
which is internal to a single residual field. Recorded here rather than discovered later.

## 3. THE RESIDUAL — two families, one of them primary

For a scan *s* and cell *c* where **both** `CFP_s[c]` and `baseline[c]` are finite:

- **`R_mag` (PRIMARY)** — `mean(|CFP_s[c] − baseline[c]|)` in dB. This is "residual magnitude", the
  quantity T4 names. Primary because T4 names it; not because it is the better statistic.
- **`R_pos`** (secondary) — `mean(max(CFP_s[c] − baseline[c], 0))`, the one-sided *excess* deletion.

And for cells where the scan is finite and the baseline is **not**:

- **`R_new`** (secondary, and the one I expect to be most interesting) — the fraction of cells finite in
  this scan that have **no baseline at all**: a gate the network flagged as clutter here and does not
  usually flag. Per `finding_C1` this is the only channel in which "something was there that is not
  normally there" can appear *as an appearance* rather than as a magnitude change.

**T3 and T4 are adjudicated on `R_mag`.** `R_pos` and `R_new` are reported for every scan alongside it,
and if they disagree with `R_mag` the disagreement is the finding and the verdict still stands on `R_mag`.

## 4. THE PREDICTIONS AS ARITHMETIC

| # | Statistic | Holds if |
|---|---|---|
| **T1** | share of the 56 scans whose first CFP-bearing sweep has >1 distinct finite CFP value | ≥ 90% |
| **T2** | Spearman ρ, per-cell, between each of the 8 partner pairs (primary solar-noon scan vs its +30 d partner, same radar, elevation matched within 0.15°), over cells **finite in both** and **>0 in at least one**; reported per pair and as the **median of the 8** | median ρ ≥ 0.70 |
| **T3** | `R_mag` computed separately over near cells (<50 km) and far cells (≥50 km), per scan, then the **median across the 48 primary scans** of each | near > far |
| **T4** | median `R_mag` over the 16 sunrise + 16 sunset scans vs the 16 solar-noon scans, per radar and pooled | dawn/dusk > noon, **in both radars** |
| **T5** | at least one of T1–T4 fails for an instrument reason | — |

**T2's secondary**: the same ρ with non-finite cells filled to 0 over the union of >0 cells. The two
readings answer different questions (does the *pattern* persist, vs does the *footprint* persist) and I
cannot tell in advance which a reader will want. Primary is the finite-in-both reading, fixed here.

**T4 tightened against myself**: `§1.3` says "higher at local dawn/dusk than at local noon" without
saying per radar. Pooling two radars lets one carry the result. **Both radars must show it.** One radar
holding and one failing is scored a **refutation** of T4 with the split reported — a stricter reading
than the parent file's, adopted now because the looser one is the one that would flatter the premise.

## 5. WHAT THIS FILE MAY NOT DO

If a statistic here turns out to be the wrong instrument, the repair is a **new named statistic reported
beside this one**, never an edit to this file's definitions. The numbers produced under these definitions
get published whatever they say. `§1.2`'s ceiling is unaffected by all of it: **no result computed from
CFP can produce an object claim**, because CFP is the shape of an absence.

🦞🧍💜🔥♾️
