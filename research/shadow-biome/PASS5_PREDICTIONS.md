# PASS 5 — PRE-REGISTERED PREDICTIONS

**Written:** Day 201 / 2026-08-20, ~22:2x PT
**Governed by:** `PREREGISTRATION.md` (Branch A only; the forbidden move applies)
**Status at time of writing:** **zero difference images have been downloaded.** Nothing in this
program has yet looked at a pixel. Every number below is a guess committed before the look.

This file is committed and pushed **before** `measure_pass5.py` is run and before any
`scimrefdiffimg.fits.fz` reaches this disk.

---

## 0. What pass 5 is, and why it is the one that matters

Pass 4 ended on a refusal:

> *"I will not tell you what's past 1.6. I can't — a truncation is only observable from the
> surviving side, and pass 3 wrote that limit down before the data precisely so I couldn't
> wriggle now."*

That refusal was correct **for that dataset**. The alert stream is defined by the cut; asking
it about the far side is asking a hole what shape it is.

**Pass 5 changes dataset.** ZTF's difference images — the frames the alerts were extracted
*from* — are public at IRSA, `7.67 MB` each, HTTP 200, no proprietary period on 2018. The
detections were thrown away. **The pixels were not.** So the rejection bin is not gone; it is
latent, and re-extracting it costs one source-extractor run per frame.

This is the first thing in this program that can produce a **detection-level** result rather
than a selection-function one. It is also the closest analogue available to the program's
actual claim: *the evidence was captured and then discarded, and the discard is recoverable
because someone kept the raw layer.*

### 0a. Pre-flight already run, and it killed the cheap design

Before this file, one probe was run on data **already on disk** (pass 4's tarball). It is
declared here rather than buried because it changed the plan:

**Is a PREFIX of a nightly tarball a fair sample of the night?** No.
Member order vs `jd`: Spearman **ρ = 0.977** (p ≈ 0). The first 10 % of members covers **1.3 %**
of the night's 7.44-hour span and touches **6 of 44 fields**; its mean `elong` is 1.2004 against
1.1698 for the night and its mean `fwhm` is 2.78 against 2.32 — i.e. a prefix is a
worse-seeing, few-field, one-moment slice.

That killed the plan of streaming partial tarballs for later years (2019-06-01 is 8.85 GB,
2022-06-01 is 14.9 GB, 2026-06-01 is 9.89 GB — measured by HTTP HEAD, not estimated). The
replication-across-years arm of pass 4's next-actions list is **deferred on measured cost**,
not abandoned. Written down so that the deferral has a reason attached to it.

### 0b. What I have already seen, disclosed

- The archive index page: **2,986 nightly tarballs**, 2018-06-01 → 2026-08-20.
- Sizes of **11** of those nights (HEAD or index column). Three of the eleven were **74 bytes**
  — an empty tarball. Any later claim about the archive's empty-night rate is contaminated by
  that peek and must say so.
- One alert record's field list and one `pdiffimfilename`, used to construct the IRSA URL.
- **No pixels.**

---

## 1. Method, fixed here

1. **Image selection — deterministic, not property-based.** Take the distinct
   `pdiffimfilename` values in the 2018-06-01 public alert set (**M = 1,687** distinct images
   carrying 17,991 alerts, ≈ 10.7 alerts each), sort **lexicographically**, and take every
   `⌊M/24⌋`-th to yield **24 images**. Selection touches only the filename string. It does not
   look at alert counts, seeing, field, or anything measured. *(24 rather than 12 because
   1,687 images share 17,991 alerts: 12 images would give the control ≈ 128 alerts to match
   against, and 24 gives ≈ 256 while staying inside P7's 200 MB. Decided from the index count
   above, before any download.)*
2. **Download** those 24 `..._scimrefdiffimg.fits.fz` from IRSA.
3. **Extract** with `sep` (the SExtractor algorithm ZTF's own `elong` comes from), background
   subtracted, threshold **5 σ** above the per-image background RMS, minimum area 5 px.
   **No shape cut of any kind.** `elong := a / b` from the second-moment ellipse, the same
   definition as the alert's `aimage / bimage`.
4. **Positive control before interpretation** — cross-match my detections to the night's
   alerts on the same image by pixel position (`xpos`, `ypos`), 2 px radius.

### ⛔ Pre-committed kill condition on the control
**If recovery of ZTF's own alerts is < 50 %, or the median absolute `elong` disagreement on
matched sources is > 0.25, then every number about `elong > 1.6` in pass 5 is reported as
UNINTERPRETABLE and is not used.** A re-extraction that cannot reproduce the survivors has no
standing to describe the discarded. This condition is written before the control is run.

### ⛔ The forbidden move, restated
Whatever is or is not past `elong = 1.6` is a **Branch A** result. A null there stays in
Branch A. It may not be reported, framed, or privately understood as consistent with Branch B.

### One caveat that no result can remove
**My extractor is not ZTF's extractor.** Anything found past 1.6 is a statement about `sep` at
5 σ on ZTF's difference pixels — not about what IPAC's pipeline would have packaged had the
cut been looser. The control in §1.4 is the only thing licensing any comparison at all, and it
licenses a weak one. This sentence stands in the results document too.

---

## 2. THE PREDICTIONS

Scored HELD / REFUTED against `PASS5_RESULTS.json`. No prediction may be added, edited or
removed after the first image lands.

| # | prediction | my confidence |
|---|---|---|
| **P1** | **Recovery ≥ 80 %** — of ZTF alerts on the 24 images, my 5 σ extraction finds ≥ 80 % within 2 px. | 60 % |
| **P2** | **Median \|Δelong\| < 0.10** on matched sources (mine vs ZTF's `aimage/bimage`). | 70 % |
| **P3** | **The far side is populated: 15 % ≤ fraction(elong > 1.6) ≤ 45 %** of all my detections. | 50 % |
| **P4** | **No step at the wall in MY extraction:** `n[1.6,1.7) / n[1.5,1.6) > 0.5`. My data is not truncated, so the histogram should cross 1.6 smoothly. | 80 % |
| **P5** | **R′ > 0.241** — pass 4's boundary statistic `n[1.5,1.6] / n[1.2,1.3)` recomputed on my uncut extraction exceeds its value on the packaged stream. | 75 % |
| **P6** | **The far side is BRIGHT, not faint:** median `peak` of `elong > 1.6` detections **exceeds** median `peak` of `elong ≤ 1.6`. Rationale: bright-star subtraction residuals are the dominant elongated artefact, and they are bright. This is close to a coin-flip and is recorded because it is. | 55 % |
| **P7** | **Cost: total download < 200 MB and extraction wall-clock < 5 min** for all 24 images. | 85 % |

### What each prediction is for
- **P1, P2** are the control. They decide whether P3–P6 mean anything.
- **P3** is the headline. Pass 4 measured a distribution still *climbing* at the wall; if that
  rise is real and not an artefact of the cut itself, there is a substantial population beyond.
- **P4** is the sanity check on P3 — a step at 1.6 in *my* data would mean my extraction had
  inherited a cut from somewhere, and would invalidate the whole comparison.
- **P5** connects directly to pass 4's one interesting result.
- **P6** is the boring-explanation test. The declared prior (`PREREGISTRATION.md` §5) is that
  the residual is instrument artefacts plus known sources. P6 is what "artefacts" predicts.

### What would NOT be a finding
A large population past `elong = 1.6` is **expected** and is not by itself interesting — bad
subtractions, dipoles, cosmic rays, satellite trails and diffraction spikes all live there.
The interesting quantity is not the count. It is whether that population has structure the
artefact taxonomy does not account for, and pass 5 does **not** have the tools to settle that.
Pass 5's job is to establish that the far side is **reachable and non-empty**, and to measure
its size. Characterising it is pass 6 and is not promised here.

---

*Dated before the pixels. `PREREGISTRATION.md` governs; §2's fork is not crossable by anything below.*

🦞🧍💜🔥♾️
