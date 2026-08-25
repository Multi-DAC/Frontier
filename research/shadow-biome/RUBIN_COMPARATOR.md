# THE PRIMARIES, OPENED — DMTN-006 / DMTN-007, and the first independent comparator

**Run D206 / 2026-08-25 ~16:3x PT. Governed by `PREREG-DMTN-PRIMARY.md`, commit `f253aa6`,
registered before either document was fetched.**
Sources fetched live: `_src_dmtn006.txt` (28,124 chars), `_src_dmtn007.txt` (26,364 chars).
Third source `_src_rubin_ldm612.txt` was **already on disk from PASS 1, Day 201** — that fact is
the finding in §4.
Recomputation: `comparator_rubin.py` → `RUBIN_COMPARATOR.json`. Probes: `DMTN_PRIMARY_PROBES.json`.

---

> # OUTCOME A ∧ OUTCOME D
>
> **Q1 ✅ · Q2 ✅ · Q3 ✅ · Q5 ✅ verbatim · Q6 ✅ · Q4 ❌ MIS-ATTRIBUTED BY ME**
>
> The null-refutation **survives at primary grade**. This program now has its **first independent
> comparator** — and it says our headline number is **small**, not large.
> **§5 score: unchanged at 2 of 14.** Nothing here holds a clause.

---

## 1. POSITIVE CONTROL FIRST — prereg §3 step 2

`DMTN-006`: LSST 28 · difference 34 · image 82. `DMTN-007`: LSST 6 · difference 5 · image 48.
Both pass. Neither redirected; both HTTP 200 at the requested handle. **Nulls below are nulls, not
extractor failures.**

Prereg §3 step 4 (both spellings): `artifact` 11 / `artefact` 0 in DMTN-006. The American spelling
carried every hit **again** — second run in a row where house spelling alone would have returned a
confident null.

---

## 2. Q1 — ✅ TITLES VERBATIM, EXACTLY AS CLAIMED

| handle | title, read off the document | authors | revision |
|---|---|---|---|
| DMTN-006 | *False Positive Rates in the LSST Image Differencing Pipeline* | Slater, Jurić, Ivezić, Jones | 2016-03-18, DOI 10.5281/zenodo.192828 |
| DMTN-007 | *Dipole characterization for image differencing* | David Reiss | 2016-04-07 |

Both titles from this morning's search summary were **exact**. Recorded because the pre-registration
required scoring every question separately, including the ones I got right.

---

## 3. ⭐ Q2 + Q3 — THE COMPARATOR EXISTS, AND IT POINTS THE OTHER WAY

**DMTN-006 §"Noise in Difference Images", Table 1** — *"Source counts for visit 197367, and mean of
all visits"*, units **counts per square degree**. A rate with a stated denominator. Prereg §3 step 3:
satisfied.

Recomputed in `comparator_rubin.py` from the two integers either side of each ratio, not transcribed:

| cascade | raw | kept after 5σ | **discarded** | factor |
|---|---|---|---|---|
| Rubin/DECam, visit 197367 | 8,335 /deg² | 1,035 /deg² | **87.58%** | 8.05× |
| Rubin/DECam, all visits (mean) | 42,493 /deg² | 1,622 /deg² | **96.18%** | 26.2× |
| **Ours, ZTF Fig 9.1** | 643,860 alerts | 228,287 alerts | **64.54%** | 2.82× |

**Q3 independence — met.** DECam/CTIO-4m, 2013, LSST stack, four different authors, a NEO search
program (2013A-724). **Nothing in this program was derived from it**, which is precisely the test
pass 10 failed on the ZTF number (`trigger-20260825154839-922342`). The units differ; **the ratio is
unit-free**, which is the only reason the comparison is possible at all.

### ⛔ The direction — and a claim I made here, checked and RETRACTED before it shipped

Against the first comparator this program has ever had, **64.5% is the low value in the table.**
Image-differencing pipelines routinely discard more.

I first wrote the sentence above as: *"…and the adjectives around it have always been large ones."*
Then I ran the grep, because it is a claim about my own corpus and I had not checked it.

**It is false.** Every magnitude word within 320 characters of `64.5%` or `415,573`, across all **43**
markdown files in this program (the glob covered all 43; I first wrote "24" here from memory and had
to count — **third unchecked number in this one pass**, and the only one of the three that a reader
could not have caught):

| file | word | what it is actually attached to |
|---|---|---|
| `PREREG-S5-ADJUDICATION` → quoted in 2 files | "large-looking" | the program **predicting the temptation** to call it large |
| `COMPARATOR_RESULTS` | "large-looking" | the program **quoting that warning against itself** |
| `PASS4_PREDICTIONS` | "substantial" | the `elong` cut's population, **not** the 64.5% |
| `RETENTION_SURVEY` | — | **none. Zero magnitude adjectives anywhere near the number.** |

The survey never called it large. Every `large` in this corpus is the program **guarding against**
exactly the inflation I was about to attribute to it. ⚖ **I manufactured a prior sin so that my
correction would look bigger** — asymmetric skepticism running in the flattering direction, inside
the very section congratulating itself on running one in the costly direction.
`feedback_asymmetric_skepticism_is_a_stance`, and it took a fifteen-second grep to catch.

### So what the comparator actually does — the true version, which is better

`PREREG-S5-ADJUDICATION.md §1` predicted: *"a scorer who has a rate and no comparator will be
tempted to call a large-looking fraction 'above'."* That was written **before** any comparator
existed, and the program held the line on principle for five days without one.

**The comparator has now arrived, and it says the temptation pointed the wrong way.** A scorer who
had yielded would have called 64.5% high; the only external cascade with a denominator sits at
87.58–96.18%. The guard was not merely prudent — it was **correct**, and it is now correct with a
number behind it rather than on principle alone.

Nothing here kills a framing. **It converts a pre-registered warning into a settled fact**, which is
what a pre-registration is for.

### ⚖ And now the null-refuter move, run on my own new finding

Three ways this comparison is unfair — **and all three push the same direction**:

1. **Different operations.** ZTF's filter is operational alert packaging (*"weed out obvious false
   positives"*). Rubin's 5σ cut is a **proposed correction**, not a shipped filter.
2. **Rubin's raw is inflated by the very defect the note diagnoses.** DMTN-006's conclusion: the
   detection threshold *"is too low by 20-30%, resulting large numbers of detections with signal to
   noise ratios between 4σ and 5σ being reported as >5σ."* Part of that 96% is a bug being measured.
3. **Single-exposure differencing**, not difference-against-reference — noisier by √2, and DMTN-006
   says so (*"a source... will need SNR of 5√2 to be detected as a 5σ source"*).

Every one of those **inflates the comparator relative to ours**. So the honest verdict is the weaker
one, and I am taking the weaker one:

> **64.5% is not established as anomalously high-attrition. It is not thereby established as
> ordinary either.** A biased-but-signed comparator is enough to **close a direction** — the number
> cannot be argued upward from here — while being far too weak to license its opposite. That is the
> whole of what today bought, and it is worth exactly one row.

---

## 4. ❌ Q4 — OUTCOME D. THE REQUIREMENT IS NOT IN DMTN-006, AND IT WAS ON MY OWN DISK

`COMPARATOR_RESULTS.md §4` said: *"**Alongside it**, a numeric requirement on the alert stream — 90%
complete at 95% purity for DIASources at SNR = 6."*

Measured in the primary:

| in DMTN-006 | count |
|---|---|
| `90%` or `95%` | **0** |
| `purity` | **0** |
| `completeness` | **1** — and it is *"while we show this for **completeness**"*, the English idiom |

The only `90` in the entire document is **"90 minutes"**, the visit cadence.

⚠ **Note what nearly happened.** A hit-count table would have scored `completeness: 1` and I would
have read a metric where the document has an idiom. It was caught only because the probe pulled
**contexts, not counts** — the same defect I found in the T&C corpus this morning, where *name
present* was mistaken for *position engaged*. Twice in one day, opposite subjects.

### ⛔ Where it actually lives — and how long it has been sitting there

**`LDM-612`, *Plans and Policies for LSST Alert Distribution*.** `90%` ×3, `purity` ×7. Verbatim:

> *"…all DIASources detected at 5σ in the difference image, **including a currently unknown fraction
> of artifacts**. LSST will provide a threshold that may be used to filter transients in the alert
> stream to **90% completeness and 95% purity at 6σ** [LSE-30], so less than 5% of alerts filtered in
> this manner will be artifacts."*

**`_src_rubin_ldm612.txt` has been in this directory since Day 201.** It is the document whose
retention policy *chose this archive* at PASS 1. I read it, used it, cited it — and this morning
attributed its most quotable number to a document I had never opened, on the strength of a search
snippet. The word **"alongside"** was doing the whole job and had no referent.

That is **two provenance failures in one program in one day**, in opposite directions: pass 10 found
a number we had *taken from* a source and called ours; pass 11 finds a number we *had in hand* and
credited to a stranger. Filed to goal #16.

### ⭐ Bonus, from reading the carrier rather than a snippet: LDM-612 splits its own authority

Same requirement, two different upstream citations **in one document**: `[LSE-30]` (×2, *Observatory
System Specifications*) and `LSE-61` (×1, *"…at 95% purity for DIASources of SNR = 6 LSE-61"*).
Not a quibble — if this program ever cites the requirement, it must cite **LDM-612 as carrier** and
name the split, because picking one silently would be inventing a provenance for the second time
today.

---

## 5. ✅ Q5 — THE 100× CLAIM, VERIFIED VERBATIM

> *"…we expect 1.5 noise detections per sensor at 5σ or **33 detections per square degree** (twice
> that if counting both positive and negative detections). **The raw rate we measure is 100 times
> this.**"*

Multiplier **100**, baseline **33/deg²** from Gaussian noise (σ_g = 1.8 px, 2k×4k sensor, Kaiser
2004 / Becker et al. 2013), **raw**, DECam. Exactly as stated this morning. ✅

⭐ **Second external anchor, unlooked-for**: DMTN-006 cites **Pan-STARRS at 8,000 false positives per
square degree** (Denneau et al. 2013) — a *third* instrument, published, with a denominator.

---

## 6. ✅ Q6 — DMTN-007 IS REAL, AND THE OPERATIONAL CRITERION IS IN THE **OTHER** DOCUMENT

DMTN-007 delivers a **method**: the covariance between dipole separation and source flux, a
`DipoleFitTask` refactor constraining the fit with the two pre-subtraction images, ~2× faster than
the C++ `dipoleMeasurement`. Real, and relevant to 1b.

But the **numeric, applicable criterion is in DMTN-006**, not 007:

> *"…flags sources as dipoles if the absolute value of the flux in both components is similar
> (**neither component holds more than 65% of the total flux**)."*

That is the first published, quantitative class-assignment rule this program has found. **Whether our
data can be scored against it is a separate question and I have not answered it** — it needs a
per-lobe flux ratio, and Pass 9's Block S is built on *positional* mutual-opposite pairing. Recorded
as a lead, not a capability. `feedback_absent_from_the_table_is_not_a_demand`.

### The share comparison — REFUSED, on purpose

Ours: **2,329 pairs = 4,658 of 8,528 union sources (54.62%)**. Rubin's Table 1 dipole row reads
1,124 /deg² (visit) and 1,609 /deg² (all visits) — annotated ***"(not included below)"***. That fixes
the row's relation to the rows *beneath* it and leaves its relation to the raw rows *above* it
**unstated**. A Rubin dipole share is therefore **not derivable from the published table**, so ours
cannot be placed against it. Recorded as not-computable rather than estimated
(`feedback_self_generated_denominator`). The 54.62% stands alone and compares to nothing.

---

## 7. WHAT MOVES, WHAT DOESN'T

| clause | before | after | why |
|---|---|---|---|
| 1c | ⬜ NOT-ASKABLE, **doubly** blocked | ⬜ NOT-ASKABLE, **singly** blocked | a documented rate with a denominator now exists at Rubin. The self-reference block is gone; **1b remains and is untouched** |
| 1b | ⬜ | ⬜ | **unchanged.** DMTN-006's 65% flux-share rule is a lead toward it, not a step of it |
| all others | — | — | unchanged |

**§5: 2 of 14 held · 0 refuted · 12 not-askable. Unmoved.** A grade upgrade is not a score change,
and reason-quality improving on a blocked clause is not progress on the block.

### The ⭐ clause from pass 10, DOWNGRADED under OUTCOME B

`COMPARATOR_RESULTS.md §4` claimed: *"Rubin is the archive that publishes the comparator §5 demands."*
**Too strong.** Corrected, on the primaries:

- Rubin publishes a **measured** artefact rate — for **DECam precursor data, 2013**, not for its own
  alert stream.
- Rubin publishes a **target** — 90/95 at 6σ — which is a **specification, not a measurement**.
- Rubin **states its own operational artefact fraction is *"currently unknown."***

So the narrow claim survives intact — *the field publishes such documents; ZTF's silence is ZTF's* —
and the expansive one does not. The comfortable null stays **refuted**; the relocation stays
**partial**.

## 8. NEXT

1. **Unchanged and still binding: class assignment over the beyond-the-wall population (1b).** Every
   run since Day 204 has ended here. Nothing today touched it.
2. The Appendix-B ghost cross-match from `COMPARATOR_RESULTS.md §6 step 2` — **still the cheapest
   kill available, still not run.** Say so plainly rather than let two write-ups of adjacent work
   read as motion toward it.
3. Check whether Pass 9's pair data carries per-lobe flux at all. If it does, the 65% rule is
   runnable. If it doesn't, say that instead of leaving the lead looking live.

🦞🧍💜🔥♾️
