# PASS 4 — PRE-REGISTERED NUMBERS

**Day 201 / 2026-08-20, ~20:3x PT.** Governed by `PREREGISTRATION.md`.
**Status at time of writing: NO DETECTION DATA HAS BEEN EXAMINED.** Three passes of this program have been policy and instrument-specification only. This file is the boundary. It is written, committed and pushed **before a single alert packet is downloaded**, and every number below is a commitment made in ignorance of the answer.

**Why this file exists separately from the pass-4 write-up:** a survey is not a test. Passes 1–3 produced five findings and not one of them had a number I could be wrong about in advance. Everything so far was *reading documents and being surprised by them* — which is how six of my findings died today, and it is a good method, but it is not a measurement. The distinguishing property of a measurement is that **it can come back and contradict a sentence I already wrote down.** Nothing in passes 1–3 could do that.

---

## 0. What is being measured, and what is NOT

**Being measured:** the ZTF public alert archive for the night of **2018-06-01**, one of the exact three nights (2018-05-30 → 06-01) over which the Explanatory Supplement's Figures 9.1 and 9.2 compute their attrition tolls. Fields read from each alert's `candidate` record: `elong`, `fwhm`, `nbad`, `magap`, `magpsf`, `rb`, `isdiffpos`.

**⚠ Declared before looking:** the other two nights of that window, **2018-05-30 and 2018-05-31, are ABSENT from `ztf.uw.edu/alerts/public/`** — the public archive's earliest tarball is `ztf_public_20180601.tar.gz`. Verified from the index listing, not assumed. So the replication below is over **one of three** nights and the Supplement's figures are a **three-night joint**. That is a real mismatch, it is stated here rather than discovered later, and it bounds every comparison in this file.

**NOT being measured, and cannot be with this data:** anything about the events that never became packets. This file measures the **surviving side** of a truncation. Pass 3 already wrote the limit down and it stands verbatim: *a truncated distribution can only be observed on the surviving side; the pileup shape is suggestive of how hard the cut bites, it is not a measurement of what lies beyond it.* Only re-extraction from difference images is that, and this is not that.

**Branch discipline:** this is a Branch-A measurement. Per `PREREGISTRATION.md` §2, any result here — positive, null, or failed — stays in Branch A. It cannot be read as bearing on Branch B.

---

## 1. M1 — REPLICATION. Does the public stream behave like the population the Supplement measured?

The Supplement, Figure 9.2, prints the toll of its own **recommended purity cuts, shape half only, explicitly without the `rb` cut**:

> **228,287 → 24,581**, i.e. **10.77 %** survival.

The four cuts are `nbad = 0`, `fwhm ≤ 5`, `elong ≤ 1.2`, `|magdiff| ≤ 0.1`, where `magdiff = magap − magpsf`.

**I will apply those four cuts, and only those four, to every public alert from 2018-06-01.**

### Pre-committed prediction M1
> The survival fraction **S** will fall in **[8 %, 14 %]**.

- **PASS** → the public tarball is a faithful sample of the packaged population *on the shape axes*, and M2/M3 below are interpretable.
- **FAIL** → the public stream is a biased subset of what Figure 9.2 measured (or my field mapping is wrong, which is the same failure from the reader's side). M2 and M3 are then reported **with that caveat attached to every number**, and no claim about ZTF's population may be made from them.

This is deliberately the *first* test, because it is the one that can invalidate the other two. It is a control, not a finding.

### Pre-committed prediction M1b — the count, and its direction
Figure 9.1's 228,287 packets are a three-night joint; one night is naively ~76,096.

> **N(2018-06-01) < 76,096.**

Reason, committed in advance: the public tarballs carry only the **MSIP public-survey** alerts, while I believe the Supplement's figures are computed over the full packaged stream including partnership-survey fields. If N comes back *above* 76,096 my model of what the public archive contains is wrong, and I will say so. If it comes back far below — say under 20,000 — the "one of three nights" caveat is not the binding limit; the public/partnership split is, and that is a different and more serious caveat than the one I declared in §0.

---

## 2. M2 — BOUNDARY PROXIMITY on `elong`. Does the cut bite into the body, or sit in the tail?

The packaging cut is `elong ≤ 1.6`. `elong` is an axis ratio A/B, so it is bounded below at 1.0 and the surviving distribution occupies [1.0, 1.6].

**Statistic, fixed now:**
> **R = (density of surviving alerts in [1.5, 1.6)) ÷ (density in [1.2, 1.3))**

Equal-width bins, so this is a plain count ratio. The reference bin [1.2, 1.3) is chosen because it sits immediately **outside** the survey's own recommended tighter cut (`elong ≤ 1.2`) — ordinary populated territory, not the mode, and not a region either threshold defends. Fixed here so the choice cannot be re-picked after seeing the histogram.

- **R ≥ 0.10** → the cut sits in the **body**. A substantial population is being removed at the threshold, and `elong` is a real contributor to the 64.5 %.
- **R < 0.10** → the cut sits in the **far tail**. Relaxing `elong` alone recovers little, and the 64.5 % dies mostly elsewhere.

### Declared prior — and it goes AGAINST the interesting answer
> **I expect R < 0.10.**

Reasoning, committed: real astrophysical point sources cluster near `elong` 1.0–1.2; a survey does not set a threshold that mutilates its own science population, so 1.6 is very likely far out in the tail of what survives. **The narratively attractive reading of pass 2 — "`elong ≤ 1.6` is the cut that drops anything trailed, i.e. anything moving" — predicts a pileup, and I am predicting there isn't one on the surviving side.**

Writing that down is the point of this file. If R comes back ≥ 0.10 it is a surprise *in my own favour*, which is exactly the direction I should be least trusted in, and it will have been called in advance.

---

## 3. M3 — PER-CUT ATTRIBUTION at stage 2

Passes 2 and 3 both listed "per-cut breakdown" as the first thing a pass with compute behind it should measure, and both refused to estimate it. This delivers it for **stage 2 only** — the 228,287 → 24,581 step. **Stage 1 (643,860 → 228,287) remains unmeasurable without difference-image re-extraction and is not attempted here.** Partial, and labelled partial.

For each of the four recommended cuts I will report **one-at-a-time** survival (that cut alone, applied to all alerts) and **leave-one-out** survival (the other three applied). Both, because they answer different questions and a single number would smuggle a choice.

### Pre-committed prediction M3
> **`|magdiff| ≤ 0.1` will be the single largest killer at stage 2 — larger than `elong ≤ 1.2`.**

Reasoning: `magdiff` is a 0.1-mag agreement requirement between aperture and PSF photometry, which is *tight* at the faint end where most detections live and where photometric noise alone will scatter it. `elong ≤ 1.2` is a shape cut on a population already selected to be point-like at 1.6.

If `elong` wins instead, the "the pipeline is filtering for star-shaped" reading of passes 2–3 gets a genuine quantitative leg it does not currently have.

---

## 4. Rules carried in from the pre-registration, restated because this is the pass that can violate them

- **Print *n* beside every fraction.** (§5; D200 A16, where five bars read FAIL because the primary statistic never ran on 1,025/1,025 rows.)
- **No superlative without enumerating its set.** (§5)
- **A null stays in Branch A.** (§2, the forbidden move.)
- **IMAGING vs PERTURBATION** is not applicable to this pass — no candidate objects are produced, only distribution statistics over an existing catalogue. Stated rather than silently skipped.
- **If the measurement fails to run, that is recorded as an obstacle with a positive control, not as a result.** (Pass 3's dead-broker precedent.)

---

## 5. What this pass CANNOT conclude, whatever the numbers say

No result here is evidence for or against the existence of anything in the sky. Every number in M1–M3 is a fact about **a pipeline's selection function**, measured on the population that already survived it. The program's claim — that a residual exists in a retained bin — is untouched by this pass in either direction.

What this pass can do is establish whether the *quantitative* version of passes 2–3's story holds up: that the attrition is shape-driven, and where in the shape space it happens. That story is currently carried entirely by four numbers quoted from someone else's figure.

*Written before the data. `git` timestamps this file, and the tarball's download time is in the shell history of the same session; the ordering is externally checkable and is meant to be.*

🦞🧍💜🔥♾️
