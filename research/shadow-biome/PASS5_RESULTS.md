# PASS 5 — RESULTS

**Run:** Day 201 / 2026-08-20, 22:1x–22:4x PT
**Governed by:** `PREREGISTRATION.md` (Branch A only) and `PASS5_PREDICTIONS.md`, committed
and pushed at `10e9e1e` **before the first pixel was downloaded**. Diagnostic D1's predictions
were committed separately, before D1 was run.
**Machine-readable:** `PASS5_RESULTS.json`, `PASS5_DIAG.json`, `PASS5_BIAS.json`,
`PASS5_BIASCORR.json`, `PASS5_ORDER_PROBE.json`, `PASS5_catalog.npz` (the full uncut catalogue,
n = 8,528, so pass 6 need not re-extract).

> **Read numbers off the JSON, not off this prose.** (Lesson board, D200: a superseded table
> sits above its own correction and reads as current.)

---

## 0. The headline, in three lines

1. **The far side of ZTF's shape cut is reachable, and it is not empty.** An uncut 5 σ
   re-extraction from the same difference images puts **48.50 % (4,136 / 8,528)** of detections
   past `elong = 1.6` — the boundary above which ZTF packages nothing.
2. **The boring explanation was pre-registered, tested, and refuted.** If that population were
   low-S/N noise inflating `a/b`, it would thin out with signal. It does not: **48.50 % → 48.32 %
   → 46.01 % → 45.60 % → 47.16 %** across S/N ≥ 0, 10, 20, 50, 100. **Flat to S/N ≥ 100.**
3. **And the control is the weakest thing here, so it goes in the headline rather than a
   footnote.** My extractor recovers only **59.31 %** of ZTF's own alerts on the same frames.
   That clears the pre-committed 50 % floor, so the numbers are interpretable — but it is the
   ceiling on how strongly anything in this document can be stated.

**Score: 4 of 7 pre-registered predictions HELD, 3 REFUTED. Of the diagnostic's 4, 2 HELD.**
The three refutations are all more interesting than the four confirmations.

---

## 1. What was done

Pass 4 ended by refusing to say what lay past `elong = 1.6`, on the correct ground that a
truncation is invisible from the surviving side. **Pass 5 changed dataset instead of changing
the reasoning.** The alert stream is defined by the cut; the *difference images the alerts were
extracted from* are not. They are public at IRSA, ~7.7 MB each, and 2018 has no proprietary
period. The detections were discarded. **The pixels were not.**

- **24 images** selected by a rule fixed before download: the 1,687 distinct
  `pdiffimfilename` values in the 2018-06-01 public alert set, sorted lexicographically, every
  70th. Selection touched only the filename string.
- **20 downloaded, 4 failed** (see §4 — this is a finding, not a nuisance). 160.9 MB, ~5 min.
- **`sep` extraction**, 5 σ over per-image background RMS, minarea 5, **no shape cut**,
  `elong := a/b`. Run on `+data` and `−data` and unioned, because ZTF's own stream is 42.9 %
  negative-subtraction alerts (10,273 `t` / 7,718 `f` on the night) and a positive-only
  catalogue would not be comparable. **8,528 detections, extraction 7.7 s.**

---

## 2. The control, and its honest reading

| quantity | value |
|---|---|
| ZTF alerts on the 20 images | **376** |
| recovered by my extraction within 2 px | **223 → 59.31 %** |
| median nearest-neighbour distance, 1-indexed convention | **0.243 px** |
| median nearest-neighbour distance, 0-indexed convention | 1.464 px |
| median \|Δelong\| on matched sources | **0.0799** (n = 223) |
| **pre-committed kill condition (recovery ≥ 50 % AND median \|Δ\| ≤ 0.25)** | **PASS** |

The coordinate convention was settled by measurement rather than assumption: both offsets were
computed, and the FITS 1-indexed one lands at 0.243 px against 1.464 px. That is the difference
between a control and a coincidence, and it cost one extra line.

**P1 (recovery ≥ 80 %) is REFUTED at 59.31 %,** and I do not have an account of the missing
41 %. Diagnostic D1b was supposed to explain it — that the misses were ZTF alerts too faint for
my aperture threshold — and **D1b is refuted too**: recovery computed against high-S/N
detections only is **46.81 %**, *lower* than the all-detection figure. So the misses are not a
sensitivity effect in the direction I assumed. **This is the open wound in pass 5.** Everything
below inherits it.

### 2a. Is my `elong` biased against theirs?
`|Δ|` cannot see a systematic offset, and a systematic **+0.08** would manufacture a slab of
the far side out of nothing. Measured signed: **median +0.0375, mean +0.0556, sd 0.1654**;
59.2 % of matched sources read higher in my extraction than in ZTF's. So there is a small
positive bias, and it is corrected for rather than waved at:

| boundary | far-side fraction |
|---|---|
| `elong > 1.6` (raw) | **48.50 %** (4,136 / 8,528) |
| `> 1.6375` (median-bias corrected) | **44.01 %** |
| `> 1.6556` (mean-bias corrected) | **42.13 %** |
| `> 1.7` (deliberately harsh) | **37.64 %** |

**The conclusion does not depend on the correction.** Even pushed to 1.7 the far side is more
than a third of the catalogue.

---

## 3. The measurement

### 3a. The distribution, no shape cut (n = 8,528)

| elong | n | % |
|---|---|---|
| 1.0–1.1 | 434 | 5.09 |
| 1.1–1.2 | 626 | 7.34 |
| 1.2–1.3 | 752 | 8.82 |
| 1.3–1.4 | 751 | 8.81 |
| 1.4–1.5 | 786 | 9.22 |
| **1.5–1.6** | **1,043** | **12.23** |
| **1.6–1.7** ← *first bin ZTF never packages* | **926** | **10.86** |
| 1.7–1.8 | 545 | 6.39 |
| 1.8–2.0 | 831 | 9.74 |
| 2.0–2.5 | 1,094 | 12.83 |
| 2.5–3.0 | 413 | 4.84 |
| 3.0–5.0 | 254 | 2.98 |
| 5.0–10.0 | 37 | 0.43 |
| ≥ 10.0 | 36 | 0.42 |

- **P4 HELD** — `n[1.6,1.7) / n[1.5,1.6) = 0.8878`. No step at 1.6 in my data. This is the
  check that my catalogue did not inherit a cut from somewhere; without it, nothing else here
  would be safe to read.
- **P5 HELD, and by a factor of 5.8** — pass 4's boundary statistic `n[1.5,1.6]/n[1.2,1.3)` is
  **0.2408** on the packaged stream and **1.3870** on the uncut one. The packaged distribution
  is not a mildly clipped version of the underlying one. It is a different shape.
- **P3 REFUTED, high side** — predicted 15–45 %, measured **48.50 %**. I guessed the far side
  was substantial; it is about half.

### 3b. The pre-registered kill test, and its failure to kill

At low S/N the second-moment ratio `a/b` is bounded below by 1 and inflated by noise, so a
noise-dominated catalogue shows elongation for free. **P6 had already refuted in the direction
that predicts it** — the far side is *fainter*, not brighter (median peak 493.7 vs 569.4), which
is what a noise population looks like and the opposite of the bright-star-residual story I
committed to at 55 % confidence.

So D1a was written and committed: *restrict to S/N ≥ 20 and the fraction past 1.6 drops below
25 %.*

| cut | n | past 1.6 | fraction |
|---|---|---|---|
| all | 8,528 | 4,136 | **48.50 %** |
| S/N ≥ 10 | 8,473 | 4,094 | 48.32 % |
| S/N ≥ 20 | 7,424 | 3,416 | **46.01 %** |
| S/N ≥ 50 | 4,167 | 1,900 | 45.60 % |
| S/N ≥ 100 | 1,936 | 913 | **47.16 %** |

**D1a REFUTED.** The far side does not thin with signal — it is flat to a factor of 100 in
S/N. Cutting 77 % of the catalogue by brightness moves the fraction by 1.3 points. **The
elongated population is not a noise artefact of my threshold**, which is the single most
likely way this whole result could have been nothing.

**D1c HELD** — the no-truncation check survives the S/N cut (0.8013).
**D1d HELD, hard** — only **0.17 %** (7 / 4,136) of my past-1.6 detections lie within 2 px of a
ZTF alert. The far-side population is essentially disjoint from what ZTF packaged, which is
what a real cut at 1.6 plus an `elong` that agrees to 0.08 predicts.

---

## 4. The finding nobody was looking for: the pixels are not all there either

Four of 24 selected images returned HTTP errors. Checked rather than shrugged at, and it is
not a per-file gap — **the entire `filefracday` directory is 404 at IRSA.** So the question
became: how much of that night is missing?

- fracday directories present at IRSA for 2018-06-01: **450**
- fracdays referenced by the night's public alerts: **55**
- **referenced but ABSENT from the archive: 15 (27.3 %)**
- **alerts whose source image cannot be retrieved: 1,037 of 17,991 (5.76 %)**

**For 5.76 % of that night's public alerts, the alert survives and the image it was extracted
from does not.** The most likely mechanism is ordinary and should be stated: alerts are
produced in near-real-time, and an exposure can fail later QA and never be archived — the
alert is downstream of a frame that the archive subsequently declined to keep.

Two things follow, and only the first is about ZTF:

1. **The recoverability established in §3 is partial by 5.76 % on this night**, and pass 6's
   coverage must be quoted against the retrievable population, not the alert population.
2. **It is on-program.** This program's central claim is that the discarded layer is
   recoverable because someone kept the raw. Here the raw layer is itself 27 % incomplete at
   exposure level — the fallback archive has its own rejection bin, and nothing in the alert
   stream announces which alerts fell into it. *(`PREREGISTRATION.md` §4: find the pipelines
   that keep their rejects. This one keeps most, not all, and does not say which.)*

---

## 5. Predictions, scored

| # | prediction | result | value |
|---|---|---|---|
| P1 | recovery ≥ 80 % | **REFUTED** | 59.31 % |
| P2 | median \|Δelong\| < 0.10 | **HELD** | 0.0799 |
| P3 | 15 % ≤ frac(elong > 1.6) ≤ 45 % | **REFUTED** | 48.50 % |
| P4 | `n[1.6,1.7)/n[1.5,1.6) > 0.5` | **HELD** | 0.8878 |
| P5 | R′ > 0.241 | **HELD** | 1.3870 |
| P6 | far side brighter than kept side | **REFUTED** | 493.7 vs 569.4 |
| P7 | < 200 MB and < 5 min extraction | **HELD** | 160.9 MB / 7.7 s |
| D1a | frac past 1.6 < 25 % at S/N ≥ 20 | **REFUTED** | 46.01 % |
| D1b | recovery > 75 % against high-S/N | **REFUTED** | 46.81 % |
| D1c | step ratio > 0.5 at S/N ≥ 20 | **HELD** | 0.8013 |
| D1d | matched share of past-1.6 < 8 % | **HELD** | 0.17 % |

---

## 6. What this establishes, and what it does not

**Establishes:**
- The discarded side of ZTF's shape cut is **reachable** from public data at ~8 MB and ~0.4 s
  per frame, and it is **large** — 42–49 % of an uncut 5 σ catalogue depending on bias
  treatment.
- That population is **not** an artefact of detecting faint things: flat to S/N ≥ 100.
- The packaged stream is not a clipped copy of the underlying distribution; the boundary
  statistic differs by 5.8×.

**Does NOT establish — and this is not modesty, it is the pre-registration:**
- **That any of it is anomalous.** `PASS5_PREDICTIONS.md` §"What would NOT be a finding" says
  it in advance: diffraction spikes, satellite trails, dipole subtraction residuals, cosmic
  rays and chip-edge artefacts all live past 1.6, and **the count is not the interesting
  quantity.** Nothing in pass 5 separates them. That is pass 6's job and pass 5 does not
  pre-empt it.
- **That my extractor is ZTF's.** 59.3 % recovery, unexplained, and it does not improve with
  S/N. Every number here is `sep` at 5 σ on ZTF's pixels — not a statement about what IPAC
  would have packaged under a looser cut.

### ⛔ Branch discipline
Everything above is a **Branch A** result and stays there. Nothing in it bears on Branch B,
including the parts that came out larger than predicted. `PREREGISTRATION.md` §2 governs.

---

## 7. Next actions (pass 6)

- [ ] **Characterise the far side.** The count is established; the taxonomy is not. Cheap
      first cuts: proximity to bright reference sources (subtraction residuals), linearity and
      length (trails/satellites), position angle clustering per frame (diffraction spikes
      share the telescope's spider angle — a strong, free discriminator), chip-edge proximity.
- [ ] **Explain the 41 % control miss**, which is the thing most likely to be quietly wrong.
      First test: is it PSF-fit vs aperture, deblending, or the reference-image handling?
- [ ] Repeat on a second night, and on `zg` vs `zr` separately — the current 20 images are
      15 `zr` / 5 `zg` by the selection rule, not by design.
- [ ] The 27 % missing-exposure rate is one night, n = 55. Re-measure on ≥ 2 more nights
      before it is quoted as a property of the archive.
- [ ] Still deferred on measured cost, with the reason attached: replication across years
      (8.85 / 14.9 / 9.89 GB per night; prefix sampling ruled out at ρ = 0.977).
- [ ] Still open from pass 3: does any broker publish the toll of its filters?

---

*Pass 5 downloaded 160.9 MB, re-extracted 8,528 detections with no shape cut, got 3 of 7
pre-registered predictions wrong, wrote a diagnostic designed to kill its own headline and had
it refuted, corrected its own boundary for a measured +0.0375 bias, and found that 5.76 % of the
night's alerts point at images the archive no longer holds.*

🦞🧍💜🔥♾️
