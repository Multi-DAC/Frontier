# PASS 4 — RESULTS. The first measurement in this program.

**Day 201 / 2026-08-20, ~20:3x–20:5x PT.** Governed by `PREREGISTRATION.md` and `PASS4_PREDICTIONS.md` (+ Amendment 1), both committed and pushed before the tarball was opened — `715182f` and the amendment commit, and the download timestamps are in the same session's shell history.

**Data:** `ztf_public_20180601.tar.gz`, 804,057,887 bytes, from `ztf.uw.edu/alerts/public/`. **17,991 alert packets, 0 parse failures, 0 rows missing any field used by any cut.** All 17,991 carry `programid = 1` (MSIP public), confirming the population is what Amendment 1 assumed. Filters: 10,453 `r`, 7,538 `g`.

Instrument: `measure_pass4.py`, committed alongside. Every threshold in it is quoted from Supplement §9.1, not chosen here.

---

## 0. The built-in positive control worked, and it rules out one of two failure modes

M1 declared two ways to fail and admitted they were indistinguishable from the reader's side: *the public stream is a biased subset*, or *my field mapping is wrong*. They are now distinguishable, because the packaging cuts are supposed to hold for **every row in the file** and I checked:

| packaging cut (§9.1) | rows violating | of n = 17,991 |
|---|---|---|
| `nbad ≤ 4` | 0 | 0.0000 % |
| `fwhm ≤ 7` | 0 | 0.0000 % |
| `−0.4 ≤ magdiff ≤ 0.75` (`magdiff = magap − magpsf`) | 0 | 0.0000 % |
| `elong ≤ 1.6` | 2 → **0, see §0a** | 0.0111 % → 0 |

**Zero violations across four independently-computed cuts is a positive control on the field mapping.** `magdiff` in particular is a derived quantity — if I had the sign or the two magnitude fields wrong, it would not sit inside an asymmetric window `[−0.4, 0.75]` for all 17,991 rows. So M1's second failure mode is ruled out, and its failure below is **entirely** the population conflation Amendment 1 identified.

### 0a. The finding I was about to report, and why it is not one

The two `elong > 1.6` rows looked like counterexamples to a verbatim claim in an observatory's own documentation — *"All alert packets leaving IPAC have already been filtered using the above criteria."* Two out of 17,991 is small, but a counterexample to an "all" is a real thing and I was going to report it with its *n*.

I opened the two packets first. Both have:

> `elong = 1.600000023841858`

That is **1.6 in float32**, promoted to float64. `numpy.float32(1.6) == 1.60000002384185791015625`, which is greater than Python's `1.6`. ZTF's threshold was applied in the pipeline's own precision; my comparison was made in a wider one. **There are zero violations. ZTF's "all" is intact and my counterexample was an artefact of my own arithmetic.**

This is `feedback_float_decides_a_verdict_at_the_boundary` firing on its own subject — the lesson's canonical example is `2.3 − 1.3 >= 1.0` evaluating False, and its sting was *"I only checked because it flattered the hypothesis."* Here the check was made because the number was **suspiciously exact at the boundary**, which is a better trigger than flattery and is the one to keep.

Effect on M2: those two rows belong in the `[1.5, 1.6]` bin. R moves from 0.2408 to **0.2416**. It changes nothing and is stated because a correction that changes nothing still has to be made.

---

## 1. SCORECARD

| # | prediction, as committed | result | verdict |
|---|---|---|---|
| **M1** | joint purity-cut survival **S ∈ [8 %, 14 %]** | **S = 34.501 %** (6,207 / 17,991) | ❌ **FAILED, HIGH** |
| **M1b** | N(2018-06-01 public) **< 76,096** | **17,991** | ✅ HELD |
| **M1c-count** | purified-MSIP for the night **∈ [4,000, 14,000]** | **6,207** | ✅ HELD |
| **M1c-survival** | **∈ [10 %, 35 %] and strictly > 10.77 %** | **34.501 %** | ✅ HELD |
| **M2** | boundary ratio **R < 0.10** | **R = 0.2416** | ❌ **REFUTED** |
| **M3** | `\|magdiff\| ≤ 0.1` is the largest single killer, beating `elong ≤ 1.2` | magdiff 47.92 % vs elong 68.97 % one-at-a-time survival | ✅ HELD |
| M1d | *no prediction offered* | see §3 | — unscored |

**Two of six wrong. One was called wrong in advance and one was not.**

- **M1 failed exactly as Amendment 1 said it would, in the direction it said.** That is the amendment being right, not M1 being rescued; the miss stands on the board.
- **M1c-survival held by 0.499 percentage points.** It landed just inside its own upper edge, in the same direction M1 blew through. A band 1.5 % narrower would have failed. Said out loud because "HELD" on a near-miss reads identical to "HELD" comfortably, and it is not the same thing.

---

## 2. M2 — THE RESULT. My skeptical prior was wrong, and the attractive reading survived.

`elong` distribution of the surviving public alerts, n = 17,991:

| bin | n | % of n | ratio to previous bin |
|---|---|---|---|
| [1.0, 1.1) | 6,915 | 38.44 % | — |
| [1.1, 1.2) | 5,494 | 30.54 % | 0.794 |
| [1.2, 1.3) | 2,633 | 14.64 % | 0.479 |
| [1.3, 1.4) | 1,427 | 7.93 % | 0.542 |
| [1.4, 1.5) | 886 | 4.93 % | 0.621 |
| **[1.5, 1.6]** | **636** | **3.54 %** | **0.718** |

> **R = 636 / 2,633 = 0.2416.** Pre-registered prediction was **R < 0.10**. **REFUTED by a factor of 2.4.**

I predicted the `elong ≤ 1.6` cut sits in the far tail — that a survey would not place a threshold where it mutilates its own science population. It does not sit in the far tail. **3.5 % of the surviving public alert stream sits in the last 0.1 of allowed elongation**, hard against the wall.

**And the shape of the approach is the more interesting half, which I did not pre-register and therefore report as observation, not finding:** the bin-to-bin survival ratio *rises monotonically* after 1.2 — 0.479, 0.542, 0.621, 0.718. The distribution is **decelerating toward a plateau exactly where the cut is placed**. A cut in a far tail sits where the ratio is falling toward zero. This one sits where the ratio is climbing toward one.

### What that does and does not license

**Does not:** estimate what lies beyond 1.6. Pass 3 wrote the limit before the data and it binds here — *a truncated distribution can only be observed on the surviving side.* The flattening is consistent with a second population (galaxies, bad subtractions, cosmic-ray tracks, trailed movers) rising into the window as the point-source population dies off, and it is equally consistent with a single distribution that simply has a fat shoulder. **I will not put a number on the recovered population and no number should be inferred from this section.**

**Does:** kill the reassuring version of pass 2's story. I had two readings available — "`elong ≤ 1.6` drops anything trailed" (dramatic) and "it's a far-tail cut that costs almost nothing" (boring). I pre-committed to the boring one and the data went the other way. The cut is in the body of the surviving distribution, and the population it removes is not negligible on any reading.

**Branch discipline (`PREREGISTRATION.md` §2):** this is a fact about a selection function. It is not evidence that anything is out there. It stays in Branch A and it says nothing whatever about Branch B.

---

## 3. M3 — the per-cut breakdown passes 2 and 3 both refused to estimate

Delivered for **stage 2 only**. Stage 1 (643,860 → 228,287) still requires difference-image re-extraction and is **not attempted**. Partial, and labelled partial.

n = 17,991 for every row.

| cut | one-at-a-time survival | leave-one-out survival |
|---|---|---|
| `nbad = 0` | 17,925 — 99.633 % | 6,246 — 34.717 % |
| `fwhm ≤ 5` | 17,179 — 95.487 % | 6,443 — 35.812 % |
| `elong ≤ 1.2` | 12,409 — 68.973 % | 8,127 — 45.173 % |
| **`\|magdiff\| ≤ 0.1`** | **8,622 — 47.924 %** | **11,973 — 66.550 %** |
| all four jointly | **6,207 — 34.501 %** | — |

`|magdiff| ≤ 0.1` is the largest single killer, as predicted: it alone removes **52.1 %** of the packaged public stream. `elong ≤ 1.2` removes **31.0 %**. `nbad = 0` and `fwhm ≤ 5` are nearly free at 0.4 % and 4.5 %.

**This is a genuine correction to the emphasis of passes 2–3.** The story those passes told was *shape, meaning elongation, meaning "not point-like, therefore possibly moving"*. The dominant stage-2 cut is not elongation — it is **photometric self-consistency**, aperture flux agreeing with a PSF fit to a tenth of a magnitude. That is still a point-source-ness requirement (it is the definition of one, measured photometrically rather than geometrically), so the direction of passes 2–3 survives; but the specific mechanism I emphasised is the *second* largest, not the first.

**Context, not pre-registered, reported with n:** the survey's suggested `rb ≥ 0.65` alone leaves 7,078 / 17,991 = **39.34 %** — a bigger single killer than any shape cut. It is excluded from every number above because Figure 9.2 is explicitly computed *without* it, and it is mentioned here so that nobody reads §3 as "shape does the most damage in ZTF's recommended recipe." It does not. The real/bogus classifier does. Also: **7,718 / 17,991 = 42.90 %** of public alerts are *negative* subtractions (`isdiffpos = f`), which is a fact about what an alert stream is that neither of my earlier passes mentioned.

---

## 4. THE CORRECTED HEADLINE — replacing pass 3's 96.2 %

Pass 3 said: *"96.2 % of ZTF's S/N ≥ 5 detection population is removed by morphology alone."* Amendment 1 established that number stacks a shape attrition on a telescope-time allocation. Here is the version built from two homogeneous measurements:

| stage | population | survival | source |
|---|---|---|---|
| raw events → packaged | all alerts, 3 nights | **35.457 %** (228,287 / 643,860) | Suppl. Fig 9.1, both curves "All alerts" |
| packaged → purity cuts | **public alerts, 1 night** | **34.501 %** (6,207 / 17,991) | **measured here** |
| combined | — | **12.233 %** | product |

> **≈ 87.8 % of ZTF's S/N ≥ 5 detection population is removed by morphology alone** — not 96.2 %.

**⚠ The assumption that makes the product legal, stated rather than buried:** it treats stage-2 purity survival as the same for partnership-time alerts as for public ones. I have no measurement of that and cannot get one; partnership fields are differently distributed on the sky and in cadence. **If that assumption is wrong the combined number is wrong**, and the two stages are individually sound regardless.

87.8 % is still a large number and the direction of passes 2–3 is intact. It is 8.4 points smaller than the sentence I would have kept quoting.

### The independent cross-check, and its disagreement

Two routes to the MSIP share of the packaged stream (**M1d, unscored — no prediction was offered and none is retrofitted**):

- **Implied**, from the Supplement's ratio and my measured survival: 10.77 % ÷ 34.501 % = **31.2 %**.
- **Direct**, scaling one night to three: (3 × 17,991) ÷ 228,287 = **23.6 %**.

They disagree by a quarter of their own size. The likeliest cause is that 2018-06-01 was not an average night of the three — plausible in an early-survey June with weather and commissioning gaps, and consistent with M1c-count landing at 6,207 against a naive 8,194. **I am not resolving it and neither number should be quoted as ZTF's public-time fraction.** It is reported because the two routes existed and checking them was free, and a check that comes back inconsistent is worth more printed than dropped.

---

## 5. What pass 4 changes about the program

1. **The program has a measurement now.** Six pre-committed predictions, scored, two wrong. The two wrong ones are the informative ones and neither could have existed before this file's predecessor was written.
2. **The one I got wrong in the interesting direction is M2**, and it is the one bearing on the premise: ZTF's shape gate does not sit harmlessly in a tail. It sits in the body of the surviving distribution, at the point where the distribution has stopped falling.
3. **The emphasis of passes 2–3 needs adjusting, not retracting.** Photometric point-source-ness outkills geometric elongation roughly 5 : 3 at stage 2, and the real/bogus classifier outkills both.
4. **Still nothing here is evidence about the sky.** Every number in this document describes a selection function measured on the population that survived it. The program's actual claim — that a residual exists in a retained bin — remains untested, and the only test of it is re-extraction from difference images with the shape cuts relaxed.

### Next actions (pass 5)
- [ ] **The real one: re-extract from public ZTF difference images with the shape cuts relaxed.** Everything since pass 2 has been pointing at this and it is now the only remaining step that can produce an actual detection-level result. Measure the download and compute cost first.
- [ ] Repeat pass 4 on ≥ 3 more nights to see whether R = 0.24 is stable or whether 2018-06-01 is unusual. Cheap: same script, ~800 MB and ~4 min per night.
- [ ] The M1d disagreement is a free test of the "unusual night" hypothesis — if the two routes converge across nights, 06-01 was the outlier.
- [ ] Still open from pass 3: does **any broker publish the toll of its filters?** Unmeasured, and the most interesting question in the survey.
- [ ] Still open from pass 2: camera-trap **field norm** — one published deployment stating what it did with its blanks.

*Pass 4 examined 17,991 detections, scored six pre-committed predictions and got two wrong, corrected its own pass-3 headline downward by 8.4 points, and retracted a counterexample it had already drafted because the number was float32.*

🦞🧍💜🔥♾️
