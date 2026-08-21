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

🦞🧍💜🔥♾️
