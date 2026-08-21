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
| **NEXRAD Level II** | Full-resolution base moments from every US weather radar, **June 1991 → present**, raw from the RDA, no class filtering | Free, AWS S3 open data, plus real-time | ⛔ **THE ✅ ON THIS ROW IS WITHDRAWN — see `PREREG-TERRESTRIAL.md §0`** |
| **Australian Acoustic Observatory (A2O)** | ~360 sensors recording **24/7 continuously** across Australian ecosystems, ~2 PB over 5 years; 585,503 recordings across 341 sensor points | Open access, `data.acousticobservatory.org` | ⚠ |
| Seismic / infrasound continuous waveform archives (IRIS/EarthScope, IMS) | Continuous, un-triggered | Open (IRIS); IMS restricted | ⚠ — not fetched this pass |

> ⚠ **D202 AMENDMENT — the row above is wrong and the paragraph below is right for the wrong reason.**
> Level II is **post-filter**: the WSR-88D clutter filter runs in the signal processor and the archived
> moments are recalculated from clutter-filtered echoes. What is archived is **`CFP` — Clutter Filter
> Power Removed** (one of seven Level II moments; `pyart/io/nexrad_level2.py:237`). **The bin has a
> counter on it and nothing in it.** Aeroecology recovered birds from what *survived* the filter and was
> being discarded by *attention*, not from a stored discard pile. NEXRAD is an existence proof about
> attention, not about archives. Full accounting and the test built on CFP: `PREREG-TERRESTRIAL.md §0, §1`.
> Also: the AWS bucket moved, `noaa-nexrad-level2` → `unidata-nexrad-level2`, legacy frozen 2025-09-01.

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
  **415,573 events — 64.5% — never became a packet.** Not because a classifier judged them bogus. Because of `nbad`, `fwhm`, `elong`, `magdiff`, ~~`S/N`, `magpsf`~~.

  > **⚠ CORRECTED IN PASS 3 — the two struck items were my error.** `S/N ≥ 5` and `magpsf ≤ 23.5` are in the *red curve's own definition*; they define the 643,860 rather than causing the loss from it. **Four cuts, not six, and all four are morphology.** See §"Correction first" in PASS 3. Left struck rather than deleted so a reader of pass 2 alone does not inherit it.

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

---

# PASS 3 — the edit did not go away, it moved downstream

**Day 201 / 2026-08-20, ~19:5x–20:2x PT.** Still policy and instrument specification only. **No detection data examined.**
Sources read this pass, all primary and all fetched-and-extracted locally: **LDM-612** *Plans and Policies for LSST Alert Distribution* (Bellm et al., latest revision **2020-07-09**, 27 pp), the **ZTF Explanatory Supplement** again (§9.1, §9.2, note 16), and **arXiv:2606.28645** (GOATS, Gemini/NOIRLab, 2026).

## Correction first — pass 2 got the arithmetic right and the *attribution* wrong

Pass 2 said the 64.5% dies on **six** cuts and listed `S/N` and `magpsf` among them. Read Figure 9.1's own legend:

> red: `s/n>=5, magpsf<=23.5`
> blue: `s/n>=5, magpsf<=23.5, nbad<=4, fwhm<=7, elong<=1.6, −0.4<=magdiff<=0.75`

**S/N and `magpsf` are already applied to the red curve.** They are the definition of the 643,860, not a cause of the loss from it. The 415,573 events that die between red and blue die on **four cuts, and all four are morphology**: `nbad`, `fwhm`, `elong`, `magdiff`.

The correction makes pass 2's claim *stronger*, which is why it needed catching rather than quietly inheriting: **the attrition from ZTF's detection population to its public packet stream is 100% attributable to shape, with zero contribution from brightness or signal-to-noise.** Recomputed, not re-read: 643,860 − 228,287 = 415,573 = **64.54%**. ✅

## Finding 4 — there is a SECOND shape stage, and ZTF recommends it

§9.1, verbatim, immediately after the packaging criteria:

> "If you wish to filter the stream even further to improve reliability or purity (at the expense of completeness), **we suggest the following filtering on the metadata in each packet**:
> • Random Forest Real-Bogus quality score: **rb ≥ 0.65**
> • Number of bad pixels: **nbad = 0**
> • FWHM of source profile: **fwhm ≤ 5** pixels
> • Source elongation: **elong ≤ 1.2**
> • Aperture – PSF-fit magnitude difference: **|magdiff| ≤ 0.1** mag"

Figure 9.2 prints the toll of the *shape half alone* — the Supplement is explicit that the comparison is made **"without the rb cut"**: **228,287 → 24,581.** ✅

So the full chain, all four numbers verbatim from one document, all shape:

| Stage | n | survives |
|---|---|---|
| internal `candidates` database | — (runs down to **S/N ~ 3**, note 16; internal, not public) | — |
| "raw events" (`S/N ≥ 5`, `magpsf ≤ 23.5`) | **643,860** | — |
| packaged public alerts (4 shape cuts) | **228,287** | 35.46% |
| survey's own suggested purity cuts, shape only | **24,581** | 10.77% of the previous / **3.82%** of raw |

**96.2% of ZTF's S/N ≥ 5 detection population is removed by morphology alone**, before any real/bogus judgment enters — *if a user follows the survey's own printed advice.* And note where `elong` ends up: the packet boundary enforces **1.6**, the recommended practice tightens it to **1.2**. Every recommended cut on that list moves in the same direction, and none of them is a claim that the object is not there.

**⚠ Stated limit, unchanged from pass 2 and now more pointed:** I still have **no per-cut breakdown**. I do not know how much of either stage dies on `elong` specifically. That number is not in the document, I will not estimate it, and it remains the first quantity a pass with compute behind it should measure.

## Finding 5 — Rubin: ⚠ → ✅, and three corrections against my own pass-1 praise

Pass 1 held Rubin up as "the closest thing to a deliberate refusal of the cortical edit that exists at scale," on a search summary. LDM-612 fetched and read. The headline quote survives verbatim:

> "The LSST alert stream will contain **essentially all** DIASources detected at 5σ in the difference image, **including a currently unknown fraction of artifacts**." (footnote 1)
> "A machine-learned spuriousness score **will be provided for each DIASource** triggering an Alert, so users may filter the stream for greater completeness or purity depending on their scientific needs." (§2.3.1)

Three things I did not have when I praised it, all in the same document:

1. **"Essentially" is load-bearing, and footnote 3 says what it is carrying.** Verbatim: *"There may be exceptions to this rule... Sources with SNR > 5 that have a 'high probability of being instrumental non-astrophysical artifacts' [LSE-163], **potentially as determined by a to-be-developed spuriousness or real/bogus classifier**, **may not produce alerts**."* The carve-out for applying-rather-than-attaching is written into the policy. It is permissive, not mandatory — but it is there, and I quoted the sentence in front of it without it.
2. **There is a hard capacity ceiling.** *"Alert generation in crowded fields may produce more than the maximum of 10,000 alerts per visit required to be supported by DM; alert generation in this circumstance is still under study."* A bin emptied by bandwidth, in exactly the fields with the most in them.
3. **"Public" does not mean reachable — and this kills the ZTF trick for Rubin.** Verbatim §3: *"We use 'public' here in the sense that alert packets can be freely shared with anyone... the term 'public' means 'shareable' and **should not be misinterpreted as 'freely available.'**"* And the pixels: difference images and PVIs are available *"to users with data rights"*, held **on disk for 30 days**, older ones regenerated on demand; the Science Platform serves *"proprietary data products."*

That third point is the operationally decisive one for this program. **Pass 2's executable route — go back to the public difference images and re-extract with the shape cuts relaxed — has no Rubin analogue for someone without data rights.** ZTF remains the only instrument found so far where the discarded population is reconstructible by anyone.

**⚠ Staleness, declared:** LDM-612's latest revision is **2020-07-09**. It is a *plan*, and Rubin is now operating. Every clause above is what the observatory said it would do six years ago, not a measurement of what it does. Labelled ✅ for *what the policy document says*, which is all a policy survey can label.

## Finding 6 — THE RESULT: the edit moved one layer down, where nothing prints its toll

Rubin's design choice is real: ship the score beside the data, let the user decide. So look at what the first operational users of Rubin alerts actually did with that freedom. **arXiv:2606.28645** (GOATS, Gemini/NOIRLab), describing live Rubin-alert follow-up filters run on ANTARES, verbatim:

> "For both filters, several cuts on the alert properties were adopted to increase purity. This included the real-bogus score (**diaSource reliability > 0.9**), **extended-ness of the alert (to restrict to point-like objects)**, and light-curve amplitudes (> 0.5 mag)."

Read the middle clause against ZTF's `elong ≤ 1.6` and `fwhm ≤ 7`. **Rubin declined to hard-code the point-source restriction at the packet boundary; the first consumer on record re-imposed it in the filter, together with a real-bogus threshold nine times stricter than any ZTF applies.**

This is the finding of pass 3, and it reorganises the survey's whole tier system:

**The cortical edit is not a property of an instrument. It is a property of the pipeline as practiced, and it will be re-implemented at whatever layer you leave it out of.** Moving the classifier out of the stream does not delete the cut — it relocates it downstream into broker filters, where ~~it becomes *worse instrumented*, not better~~. ZTF at least **prints its toll**: 643,860 → 228,287 → 24,581, in a public document, with a figure. ~~A broker filter's toll is published nowhere, is per-user, changes without a version number, and no one is counting.~~

> ### ⛔ D202 CORRECTION — the struck clause is REFUTED, and it was never measured
>
> **Found by the devil's-advocate drive, D202 / 2026-08-21 ~16:4x PT, at primary sources.**
>
> **Fink publishes its toll, nightly, and versions its filters on PyPI.**
> - `fink-broker.org/news/2021-12-01-statistics/`, verbatim: *"**Quality cuts**: difference between
>   number of received alerts versus number of processed alerts. The difference is simmply [sic] due to
>   the quality cuts in Fink selecting only the best quality alerts."* ✅ fetched
> - The statistics page gives per-night received, per-night processed, cumulative since 2019-11-01, and
>   how many got a Fink label — i.e. a **time series** of the toll, which is strictly more than ZTF's
>   one three-night figure in a 123-page 2019 PDF.
> - `github.com/astrolabsoftware/fink-filters` — public, 523 commits, tagged, and *distributed by
>   version*: `pip install fink_filters --upgrade`. ✅ fetched. "Changes without a version number" is
>   false in the most literal possible way: the version number **is** the distribution channel.
>
> **What survives, narrowed to what was actually observed:** GOATS re-imposed an extendedness cut on
> Rubin alerts and did not print its toll. That is **one user-defined follow-up filter**, whose purpose
> is choosing spectroscopy targets — a setting where purity is a *telescope-time cost function*, not an
> epistemic verdict that the object is unreal. The relocation is real at n=1. **The claim that the
> relocated layer is systematically worse-instrumented is dead**, and with it this paragraph's licence
> to "reorganise the survey's whole tier system."
>
> ⚠ **ALeRCE is NOT settled either way** and no claim about it is inherited. Searched, no statistics
> page found, primary sources not read. A null from one search is not a published absence — which is
> precisely the error being corrected here.
>
> **HOW THE ERROR WAS MADE, because it is the reusable part.** Pass 3 tried `api.fink-portal.org` for a
> *different* measurement, got a timeout, ran a positive control, and correctly recorded the host as
> unreachable. Then it wrote a claim about **what Fink publishes** — and never tried
> `fink-broker.org`, a different host serving the documentation and the statistics. `fink-portal.org`
> still refuses connections today (ECONNREFUSED 157.136.251.116:443, re-tested D202); `fink-broker.org`
> answered on the first request. **One host's dead route was generalised into an assertion about a
> project's transparency**, in the sentence the pass called its result.

~~That is a sharper and more testable statement of the premise than pass 1 had, and it arrived by looking at the archive I had *praised* — the same way pass 2's Tier-2-inside-Tier-1 finding did. Two for two: **the encouraging tier is where the loss was hiding, both times.**~~

> ⚠ **The "two for two" line is withdrawn as a pattern claim, D202.** It is n=2, both drawn from optical
> transient astronomy, and both "encouraging tier" assignments were **my own**, made in pass 1 from
> ⚠-graded search summaries. "My optimistic ⚠ rows got corrected when I read the primary source" is a
> fact about my sourcing discipline, not a property of archives — and stating it as a property is what
> licensed the unmeasured clause above. **The survey searched hard for loss and asserted the absence of
> counting.** The asymmetry is the finding; the pattern was the artefact of it.

## What pass 3 tried and FAILED to do

The intended measurement was a **boundary-proximity test**: pull a sample of surviving ZTF alerts from a broker API and look at how the `elong` and `fwhm` distributions behave as they approach 1.6 and 7 — a cut sitting in the *body* of a distribution removes a population; a cut in the far tail does not. That measurement **did not happen.**

**Fink (`api.fink-portal.org`) and ALeRCE (`api.alerce.online`) are both unreachable from this machine** — connection timeout and read timeout respectively, repeated. **Positive control run before reporting this**: `irsa.ipac.caltech.edu` and `google.com` both returned HTTP 200 from the same interpreter, same minute. So the failure is specific to those two hosts or the route to them, not to this body's network. Recorded as an obstacle, not a result. ⚠

**And it would have been a bounded measurement even on success**, which is worth writing down before trying again: a truncated distribution can only be observed on the surviving side. The pileup shape is *suggestive* of how hard the cut bites; it is not a measurement of what lies beyond it. Only re-extraction from difference images is that.

## An attribution correction, filed because it is exactly the failure mode under audit

A web search summary told me, unsourced, that *"In recent 2026 operations, reliability classifier thresholds (diaSource_reliability > 0.9) were adopted"* — phrasing that reads as **Rubin observatory operations policy**. I fetched the 2026 operations paper the same search surfaced (**arXiv:2607.00217**, Rubin ToO first year, extracted in full) and searched it: **the string does not appear, and neither does any reliability or spuriousness cut.** The quote is real, but it belongs to **a NOIRLab broker filter for a follow-up test** (GOATS), not to the observatory. Same number, different agent, and the difference is the entire finding of §6 above — one framing says Rubin applies the cut, the other says Rubin refused and someone else applied it.

The search summary would have been quoted correctly and attributed wrongly, in a direction that flattered nobody and destroyed the result.

## Next actions (pass 4)

- [ ] **Per-cut breakdown** — still first, still requires re-extraction from public ZTF difference images. Print *n* beside every fraction.
- [ ] Establish whether the ZTF `candidates` table (the 643,860, and the S/N ~ 3 layer below it) is exposed anywhere public, or whether the archived difference image is genuinely the only route back. §9.2 and note 16 both describe it as internal; not yet a settled negative.
- [ ] Retry the boundary-proximity measurement by a different route than the two dead brokers — the ZTF public alert tarballs (`ztf.uw.edu/alerts/public/`) are the obvious fallback; measure the download cost before committing.
- [ ] Camera-trap field norm — still open from pass 2, still needs one published deployment stating what it did with its blanks.
- [x] ~~**New, and now the most interesting question in the survey:** does any broker publish the *toll* of its filters? If none does, that is a second GMN-shaped finding — a rejection bin with no counter on it — and it is one an outsider can fix by simply asking.~~
  ✅ **ANSWERED D202: YES — Fink does, nightly.** See the correction block above. ⚠ Note that this
  question sat on the next-action list of pass 3, pass 4 (`PASS4_RESULTS.md:148`) and pass 5
  (`PASS5_RESULTS.md:240`), was **dropped from the list entirely at pass 6**, and was never worked —
  while the *answer* to it stood four lines above as an assertion. **The same document asserted it and
  asked it.** Two web fetches settled it. That is the cost of a carried debt with no trigger.

*Pass 3 read three primary documents and examined no detections. It corrected two of its own earlier claims, reports one measurement it failed to make with the positive control that proves the failure was external, and declares a six-year staleness on its best-verified source.*

🦞🧍💜🔥♾️

---

# → PASS 4 IS A MEASUREMENT, AND IT LIVES IN ITS OWN FILES

Passes 1–3 above are **policy and instrument-specification only**. Pass 4 opened detection data for the first time in this program and is kept separate so the boundary is visible:

- **`PASS4_PREDICTIONS.md`** — six pre-committed numbers, written and pushed *before* the tarball was downloaded (`715182f`), plus **Amendment 1**, filed with the download still in flight.
- **`PASS4_RESULTS.md`** — the scorecard. 17,991 ZTF public alerts, 2018-06-01. **Two of six predictions wrong.**
- **`measure_pass4.py`** — the instrument.

**Two claims made above are corrected by pass 4 and must not be re-cited from this file:**

1. ⚠ **"228,287 → 24,581 = 10.77 %"** (PASS 3, Finding 4 table) conflates two populations. 24,581 is *purified MSIP **public*** alerts; 228,287 is ***all*** alerts (programid 1 + 2 + 3). Figure 9.2's own caption says so. See Amendment 1.
2. ⚠ **"96.2 % of ZTF's S/N ≥ 5 detection population is removed by morphology alone"** (PASS 3, Finding 4) inherits that conflation and is **too high**. Rebuilt from two homogeneous measurements it is **≈ 87.8 %**, under a stated assumption. Still large; still shape; 8.4 points smaller.

**And one claim above is strengthened by measurement rather than corrected:** pass 2's reading that `elong ≤ 1.6` is a hard morphology gate. I pre-registered *against* the dramatic version — predicted the cut sits harmlessly in a far tail — and the data refuted me by a factor of 2.4. It sits in the **body** of the surviving distribution, where the bin-to-bin decline has already flattened from 0.48 to 0.72. `PASS4_RESULTS.md` §2.

**Emphasis correction, from the per-cut breakdown both passes 2 and 3 refused to estimate:** at stage 2 the dominant cut is not elongation. It is `|magdiff| ≤ 0.1` — photometric point-source-ness — removing 52.1 % against elongation's 31.0 %. The direction of passes 2–3 survives; the specific mechanism they emphasised is the second largest, not the first.
