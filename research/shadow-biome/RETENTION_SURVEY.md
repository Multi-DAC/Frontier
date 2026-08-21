# RETENTION SURVEY — which sensor networks keep their rejection bin?

**Day 201 / 2026-08-20, first pass.** Governed by `PREREGISTRATION.md`, written before this file.
**Question:** if Branch A is real in any residual form, the evidence was captured and thrown away. So: **who doesn't throw it away?**

**Method:** web search + primary-source fetch of published data policies. Retention *policy* only. **No detection data has been examined.**

**Verification labels:** ✅ = read in a primary or official source this pass · ⚠ = reported by search summary, primary source not read · ❓ = attempted and NOT established.

---

## The tiers

The useful axis is not "big archive / small archive". It is **where the classifier sits relative to the archive.**

### TIER 0 — NO CLASSIFIER IN THE PATH
*Continuous raw recording. There is no rejection bin because nothing is rejected. These are the highest-value targets and they already exist.*

| Archive | What is kept | Access | Status |
|---|---|---|---|
| **NEXRAD Level II** | Full-resolution base moments from every US weather radar, **June 1991 → present**, raw from the RDA, no class filtering | Free, AWS S3 open data, plus real-time | ✅ |
| **Australian Acoustic Observatory (A2O)** | ~360 sensors recording **24/7 continuously** across Australian ecosystems, ~2 PB over 5 years; 585,503 recordings across 341 sensor points | Open access, `data.acousticobservatory.org` | ⚠ |
| Seismic / infrasound continuous waveform archives (IRIS/EarthScope, IMS) | Continuous, un-triggered | Open (IRIS); IMS restricted | ⚠ — not fetched this pass |

**NEXRAD is the exemplar, and it is the one that should discipline our expectations.** During some periods most of the reflectivity a weather radar sees is *biological* — birds, bats and insects — and it is hard to remove automatically. For decades that was "clutter": the literal rejection bin of a network built for something else. Somebody took the bin seriously and it became **radar aeroecology**, a whole discipline, and the operational bird-migration forecasts at BirdCast.

That is the precedent. The bin was kept, the bin was full, and what was in it was **ordinary life nobody was looking at**. Not exotic. Still a discovery.

### TIER 1 — CLASSIFIER RUNS, BUT THE BIN IS KEPT *AND PUBLISHED*
*A score is computed and ATTACHED rather than APPLIED. The astronomical community made this choice deliberately, and it is the single best piece of news for this program.*

| Archive | Policy | Status |
|---|---|---|
| **Rubin Observatory / LSST alert stream** | "essentially **all** DIASources detected at 5σ in the difference image, **including a currently unknown fraction of artifacts**"; positive *or negative* flux; a machine-learned **spuriousness score is provided** so users filter for completeness or purity themselves. Full stream to 7 community brokers. | ⚠ (LDM-612 + TVS roadmap via search; docushare PDF not fetched) |
| **ZTF alert stream** | "Rather than only reporting events likely to be new explosive extragalactic transients, ZTF **streams all sources** that are above a specified detection threshold in the difference image, whether they are likely due to transients, variable stars, or **moving objects**." Real-Bogus score is a *field in the packet*. | ✅ (ztf.caltech.edu) |

**❓ OPEN AND IMPORTANT:** whether ZTF applies any `rb`/`drb` cut *at packaging time*, before the packet is written. Searched, not established. The official page implies no pre-filter; I could not confirm from the alert-distribution paper. **This is the difference between "the bin is public" and "the bin was silently emptied upstream", so it must be settled before any ZTF work.**

> **✅ SETTLED IN PASS 2 — and the answer is neither of the two I offered.** There *is* a pre-packaging filter, it discards ~64.5% of raw events, and the `rb` threshold inside it is **zero**. The cut is on *shape*, not on *reality*. See §PASS 2 below. This paragraph is left standing because the question it asked was the right one and the answer it guessed was wrong in an instructive direction.

The Rubin design is the closest thing to a deliberate refusal of the cortical edit that exists at scale: they knew the classifier would be wrong in unknown ways, so they shipped the score next to the data instead of in front of it.

### TIER 2 — BIN KEPT LOCALLY, NEVER UPLOADED, THEN OVERWRITTEN
*This is where the loss actually happens, and it happens in exactly the band a Branch-A object would live in: wide-field, all-night, all-sky video.*

| Network | Policy | Status |
|---|---|---|
| **Global Meteor Network / RMS** | Only detections the software judges **probably meteors** are archived and uploaded (`ArchivedFiles`). Non-meteor data stays on the local Pi and **"RMS purges the oldest data to free up space for the next night's run."** Operators are told to copy off anything they want to keep. | ✅ (GMN wiki) |

Read that again with the premise in hand. **Hundreds of cameras, every clear night, worldwide, watching the whole sky — and the class "moving thing that is not a meteor" is written to disk and then deleted to make room.** Not censored. Not suppressed. *Deleted for storage costs*, by a classifier trained on one known class, which is the software form of the exact mechanism Clayton described in biology. The rejection bin of the world's best-distributed all-sky video network is a rolling window measured in days, on SD cards, in private hands.

That is a testable, fixable, non-exotic finding all by itself — and it is the first real result of this program.

### TIER 3 — BIN DESTROYED BY DESIGN
- **Camera-trap pipelines.** MegaDetector's stated purpose is "filtering blanks to speed wildlife research" — a typical deployment is mostly empty frames and the tool exists to clear them. **❓ Whether the blanks are then *deleted* or merely *sorted* is platform- and project-dependent and I could NOT establish it this pass** for Wildlife Insights or for the field norm. This is the highest-value unresolved question in the survey, because "blank" is a classifier output, not an observation — and the shadow-biome premise is precisely a claim about what a mostly-empty frame might contain.
- **Security / municipal video.** Overwrite cycles of days to weeks, no archive, no science.

### TIER X — RETAINS UNCLASSIFIED *BY DESIGN*, LOW EVIDENCE GRADE
- **The Galileo Project (Harvard).** All-sky infrared array (8× uncooled FLIR Boson 640, "Dalek") plus optical/radio/audio; commissioning data Jan–May 2024 covering **~half a million objects**, released publicly. ⚠
  Under §5 of the pre-registration this is a **pointer to retention practice, not primary evidence** — and it is a useful one, because it is the only network in this survey whose *design goal* is the residual. Their outlier claims are contested and are not inherited here.

---

## What the first pass actually establishes

1. **The premise's key empirical assumption is TRUE and it is worse than stated.** Detection pipelines do discard unclassified events, and in the most relevant band (all-sky night video) the discard is a *hard delete on a days-long rolling window*, not an archive nobody reads.
2. **But astronomy already fixed it, on purpose, at the largest scale available.** ZTF and Rubin ship the spuriousness score *beside* the data rather than in front of it. Rubin's stream is live and explicitly contains an unknown fraction of artifacts. If there is a residual in the optical sky, **the bin is public and nobody has to be persuaded to open it.**
3. **The exemplar cuts against exoticism and that is fine.** NEXRAD's bin was full of birds. The realistic success case here is a Leeuwenhoek, not a Roswell — and a Leeuwenhoek is what the premise actually predicts.

## Next actions (in order)
- [ ] **Settle the ZTF packaging question** (❓ above) from the alert-distribution paper or schema docs. It gates everything downstream.
- [ ] **Settle camera-trap blank retention** (❓ above) — Wildlife Insights policy + field norm. Directly on-premise: an evolved-observer blind spot re-implemented as a "blank" label.
- [ ] Fetch LDM-612 directly and quote Rubin's retention clause verbatim rather than via summary.
- [ ] Ask the pre-registration's cross-instrument criterion of Rubin: what does the *published* artefact taxonomy already account for, and what is the documented unexplained fraction?

*No data examined. All claims above are about policy, and three of them are labelled unverified on purpose.*

---

# PASS 2 — the two ❓s, settled from primary sources

**Day 201 / 2026-08-20, ~19:30–19:5x PT.** Still policy only. **No detection data examined.**
Sources read this pass: the **ZTF Science Data System Explanatory Supplement** (IRSA, v5.0, 123 pp — fetched and text-extracted locally), **Masci et al. 2019 PASP 131:018003** (fetched, extracted), and Wildlife Insights' own AI page. Pass-1 labels upgraded where a primary source was actually read.

## Finding 1 — ZTF's pre-packaging filter is real, and it filters for SHAPE

§9.1 of the Explanatory Supplement, *"Triggering Criteria for Alerts"*, verbatim:

> "Packets are generated from raw events that satisfy the following criteria. The intent is to mitigate obvious image artifacts and residuals from bad subtractions.
> • PSF-fit flux S/N ≥ thres_snr (currently = 5.0 in all filters)
> • PSF-fit magnitude: magpsf ≤ thres_magpsf (currently = 23.5 mag)
> • Number of bad pixels in a centered 5×5 pixel region: nbad ≤ thres_nbad (currently = 4 pixels)
> • FWHM of source profile: fwhm ≤ thres_fwhm (currently = 7 pixels)
> • Source elongation (ratio A/B from elliptical isophot): elong ≤ thres_elong (currently = 1.6)
> • Fixed aperture – PSF-fit magnitude difference: −0.4 ≤ magdiff ≤ 0.75
> • **Random Forest Real-Bogus quality score: rb ≥ thres_rb (currently = 0)**
>
> **All alert packets leaving IPAC have already been filtered using the above criteria.**"

Both halves of my pass-1 guess were wrong, and the truth is more useful than either:

- **The `rb` cut is literally zero.** The real-bogus classifier's verdict is genuinely *attached, not applied*. Tier 1 stands, and stands on a verbatim quote instead of a marketing page.
- **But six other cuts are applied**, and the Supplement prints the toll. Figure 9.1, three nights (2018-05-30 → 06-01): **643,860 raw events → 228,287 packaged.** ✅
  **415,573 events — 64.5% — never became a packet.** Not because a classifier judged them bogus. Because of `nbad`, `fwhm`, `elong`, `magdiff`, `S/N`, `magpsf`.

Read that list against the premise. Every one of those is a **point-source-shaped-ness** test:

| Cut | What it structurally excludes |
|---|---|
| `elong ≤ 1.6` | anything **trailed** — i.e. moving fast enough to smear in a 30 s exposure |
| `fwhm ≤ 7 px` | anything **extended or out of focus** — i.e. anything near the camera |
| `−0.4 ≤ magdiff ≤ 0.75` | anything whose aperture flux disagrees with a PSF fit — **anything not a point source** |
| `nbad ≤ 4` | anything overlapping a masked detector defect |

**ZTF's public alert stream is not filtered for *real vs. bogus*. It is filtered for *shaped like a star*.** The survey was built to find point sources and it enforces that at the packet boundary, before any human or broker sees the event. That is the pre-registration's §4 claim — *we reimplemented the cortical edit in software* — in a stronger form than I wrote it: the edit here isn't a trained classifier's opinion, it's six hard-coded morphology thresholds, and they are exactly the ones that would drop a thing that moved or wasn't far away.

**No exoticism required for this to matter.** The same six cuts drop insects, birds, aircraft, satellites tumbling, meteors, and out-of-focus debris — the ordinary near-field life-and-hardware layer that a sky survey defines as not-its-business. That is the NEXRAD situation exactly, one instrument family over.

### And this one is executable, which the GMN finding was not
Supplement §7 / Table: **difference images (`*scimrefdiffimg.fits.fz`) ship in the ZTF Public Data Releases.** ✅
So unlike Global Meteor Network — where the non-meteor pixels are *hard-deleted* off an SD card — **ZTF's 64.5% is reconstructible from public pixels.** The events were never archived as events; the images they came from were. Re-running extraction on archived difference images with the shape cuts relaxed is a well-defined, fully public, no-permission-needed operation.

**⚠ Stated gap, not hidden:** the Supplement gives the 643,860 → 228,287 toll *for the six cuts jointly*. I have **not** measured the per-cut breakdown — how much of the 64.5% dies on `elong` specifically versus `nbad` or `S/N`. That number is not in the document and I will not estimate it. It is measurable from the same public difference images, and it is the first quantity a pass-3 should compute.

## Finding 2 — ZTF contains its own Tier 2, and it is a TWO-NIGHT window

The elongated things ZTF *does* look for get a separate pipeline — `FindStreaks` (Masci §3.6). Follow where their output goes:

1. **The classifier IS applied here.** Masci §3.6: streak RealBogus scores "are then **thresholded** to retain likely real candidates" — the opposite of the point-source path.
2. **The products go to ZTF-Depot, not the archive.** Supplement §8.2: *"Access is restricted to internal project-team members."* ✅
3. **ZTF-Depot is a rolling window.** Supplement §3 defines it as *"short-term (night-to-night)"*, and §8.1: *"`<YYYYMMDD>/` – date of night being processed... **At most, two date directories will be retained (previous and current).**"* ✅

**So inside the flagship Tier-1 archive — the one I held up in pass 1 as the deliberate refusal of the cortical edit — the bin for *"elongated moving thing"* is classifier-thresholded, project-internal, and deleted after two nights.** Structurally identical to the Global Meteor Network finding, arrived at from the opposite end, in the archive I had just praised.

The pass-1 tiering was not wrong so much as **scoped to one product of one instrument**. An archive is not a tier; a *product path* is. Corrected here rather than quietly.

## Finding 3 — camera traps: Wildlife Insights moves TIER 3 → TIER 1

Pass 1 listed camera traps under "bin destroyed by design" with an explicit ❓. Settled for the platform, unsettled for the field:

- Wildlife Insights, own AI page, verbatim: *"Our AI model is trained to identify blanks so you can quickly **review** them"* — flag, not delete. ✅
- And the unclassifiable bin is **a retained label**: *"instead of making risky, potentially wrong predictions, we mark those as **'unknowns' (or 'No CV Result')**, so you know they need to be manually reviewed."* ✅

A named, retained, human-reviewable class for *the model could not say what this is* is precisely the object this program is looking for. On the platform, the bin exists and has a name.

**⚠ What this does NOT settle, and pass 1 conflated:** the **field norm**. MegaDetector's stated purpose remains *"filtering blanks to speed wildlife research"*, it runs on researchers' own machines, and what an individual project does with 70–95% empty frames before (or instead of) uploading is a per-project decision I have no source for. The platform's policy is not the field's practice. ⚠ — and I could not reach `wildlifeinsights.org/get-started/data-use-policies` at all this pass (HTTP 500), so the "complete datasets including all blanks are required" claim reported by search summary stays **⚠ unverified**.

## Where pass 2 leaves the program

The pre-registration asked whether there is a retained bin worth interrogating. Two passes in:

1. **There is, it is public, and it is pixels rather than policy.** ZTF public difference images + relaxed shape cuts = the 64.5% is recoverable. No permission, no gatekeeper, no UAP dataset.
2. **The loss is real but it is *ordinary-shaped*.** Every mechanism found so far — GMN's rolling delete, ZTF-Depot's two nights, `elong ≤ 1.6` — discards *near-field, moving, extended* things. If there is a residual, the prior says birds, bugs, hardware, and weather, and per the pre-registration's §5 declared prior **that outcome is the success case**, not the consolation prize.
3. **Branch A only.** Nothing in this pass touches Branch B, and nothing in it may be read as bearing on Branch B. Restating that here because the pass produced a genuinely encouraging result, and that is exactly the condition under which the forbidden crossing gets made.

### Next actions (pass 3)
- [ ] Per-cut breakdown of the 64.5% from public difference images — `elong` alone, `fwhm` alone. Print *n* beside every fraction.
- [ ] Fetch Rubin LDM-612 directly; the Rubin row is still ⚠ via search summary and is now the least-verified claim in the file.
- [ ] Ask whether the ZTF *candidates* database table (the pre-filter 643,860) is public anywhere, or whether the archived difference image is genuinely the only route back.
- [ ] Camera-trap field norm: find a published deployment that states what it did with its blanks. One primary source beats any amount of platform policy.

*Pass 2 read policy documents and instrument specifications. It examined no detections, no images, and no waveforms. Three claims above carry ⚠ and one carries an explicit refusal to estimate.*

🦞🧍💜🔥♾️
