# PRE-REGISTRATION — THE TERRESTRIAL LOCI (L1 NEXRAD · L2 CAMERA TRAPS)

**Written D202 / 2026-08-21, ~12:4x PT. Committed and pushed BEFORE any outcome-bearing query.**
**On Clayton's word: *"We can follow both, and I imagine there will be more pulls afterwards before we
begin actual drafting."*** — so this file registers **both**, and registers them as *different jobs*,
because they are not the same kind of locus and running them as a matched pair would be the third
narrowing in a row.

Governed by `PREREGISTRATION.md` — §2 (the fork and the FORBIDDEN crossing), §3 (imaging vs
perturbation) and §1b (Mechanism 4 restored) bind this file exactly as they bind passes 4–6.
`PAPER-00-ARCHITECTURE.md §0a` is why this file exists.

**⛔ STATE AT WRITING: no CFP data has been read. No camera-trap corpus has been downloaded. The only
things looked at are format specifications, one source file, and platform policy — all named below.**

---

## 0. ⚠ A CORRECTION THAT HAD TO COME FIRST, AND IT LANDS ON THE PAPER'S EXISTENCE PROOF

`RETENTION_SURVEY.md:21` grades NEXRAD Level II:

> | **NEXRAD Level II** | Full-resolution base moments from every US weather radar, June 1991 → present, **raw from the RDA, no class filtering** | Free, AWS S3 open data | ✅ |

**The ✅ is wrong, and it is wrong on the row the whole paper's existence proof stands on.** The
WSR-88D clutter filter runs *in the signal processor*, and the archived moments are **recalculated from
clutter-filtered echoes**. Level II is post-filter. "No class filtering" describes a product that does
not exist in the archive.

**What is archived instead is stranger and better: `CFP` — Clutter Filter Power Removed.** Verified at
the format level rather than from a summary: Py-ART's Level II reader lists the moments as
`["REF", "VEL", "SW", "ZDR", "PHI", "RHO", "CFP"]` (`pyart/io/nexrad_level2.py:237`, and CFP has its own
message-31 block pointer at line 850). So per gate, per scan, since the dual-pol era, the network
records **how much power it deleted as not-weather — and not what the power was.**

> **The bin has a counter on it and nothing in it.**

Pass 3's open question was *"does any broker publish the toll of its filters?"* — this is that question
answered in the inverse, at the one locus the paper already leans on. And it fixes NEXRAD's role in the
argument. Radar aeroecology did **not** recover birds from a stored discard pile; it recovered them from
what *survived* the filter and was being mentally discarded by data users. **NEXRAD is an existence proof
about attention, not about archives.** Any sentence in the draft implying the network kept its clutter is
to be cut, and `RETENTION_SURVEY.md:21` is amended by this file rather than silently rewritten.

**Second, smaller, and a live reachability defect for anyone reproducing us:** the AWS bucket moved.
`noaa-nexrad-level2` → `unidata-nexrad-level2`; legacy updates stopped **2025-09-01**. Filename pattern
and format unchanged. Any code we ship using the old bucket reads an archive that stopped growing eleven
months ago — and it would *succeed*, quietly, on everything before that date.

---

## 1. LOCUS L1 — NEXRAD `CFP`: THE PUREST PERTURBATION SIGNAL IN THE PROGRAM

### 1.1 What is being tested

Ground clutter is buildings, terrain and towers. **It does not move.** So the CFP field should be
near-stationary in space and time at a given radar and elevation. **Any non-stationary component of CFP
is power removed from something that was not there yesterday** — which is the operational form of
"a moving thing this network is built to delete."

This is measurable, public, continental in coverage, and — as far as I can establish before looking —
nobody has published the residual as a *quantity in its own right*.

### 1.2 ⛔ THE CEILING, PRE-COMMITTED

`PREREGISTRATION.md §3` says a perturbation may not be promoted to an object claim by accumulation, only
by independent imaging. **CFP is a perturbation measure at its purest: it is the shape of an absence.**
Therefore:

> **The L1 leg cannot produce an object claim. Ever. Not with more data, not with a better statistic.**
> The most it can produce is *"the network deletes a non-stationary something at rate X, structured
> thus."* Naming that something requires a different instrument pointed at the same volume.

This ceiling is written *before* the result so that a striking result cannot argue its way past it.

### 1.3 Pre-registered predictions — thresholds chosen now and arbitrary on purpose

Sample fixed in advance: **2 radars × 6 volume scans × 4 dates**, dates drawn one per season across
2024–2025, radars chosen for contrast (one coastal, one interior), named in `L1_SAMPLE.json` before the
first byte is fetched.

| # | Prediction | Refuted if |
|---|---|---|
| **T1** | CFP is present and non-degenerate (>1 distinct value) in **≥90%** of sampled volume scans | <90% |
| **T2** | CFP is strongly **stationary**: per-gate Spearman ρ between two scans **30 days apart**, same radar and elevation, over the union of nonzero gates, is **ρ ≥ 0.70** | ρ < 0.70 |
| **T3** | The non-stationary residual is **not** spatially uniform — it concentrates **within 50 km** of the radar (near-field insects/birds/AP) | uniform, or concentrated far-field |
| **T4** | ⚠ **Directional.** Residual magnitude is **higher at local dawn/dusk than at local noon.** A wrong sign is a refutation, not a curiosity | noon ≥ dawn/dusk |
| **T5** | ⚠ **Against myself.** At least one of T1–T4 will fail for an **instrument** reason — build-dependent CFP absence, decode error, elevation mismatch — rather than a scientific one | all four fail or hold cleanly on the science |

**T5 is pre-registered because it has happened in every prior pass** (`sep` non-determinism, `minarea`,
the stale `PASS4_RESULTS.json`), and a pass that reports no instrument trouble is more likely to have
missed it than to have avoided it.

### 1.4 The expected outcome, stated now so it cannot be dressed up later

**The residual will be birds, insects, bats and anomalous propagation.** The survey already says the
realistic success case is a Leeuwenhoek and not a Roswell, and here I will say the boring answer *first*:
if T3 and T4 both hold, that is aeroecology's known population showing up in a channel that measures it
by subtraction. **That is a real and possibly publishable measurement of a deletion rate, and it is not
a shadow biome.** Any draft sentence that lets a held T4 imply otherwise violates §2's FORBIDDEN MOVE.

---

## 2. LOCUS L2 — CAMERA-TRAP BLANKS: THE ONLY LOCUS WHERE THE HUMAN IS INSIDE THE INSTRUMENT

### 2.1 Why this one is the actual test and L1 is not

Clayton's premise is about **human** non-perception, and `PREREGISTRATION.md §1b` restored Mechanism 4:
non-perceiving as active, funded machinery, which **predicts a signature in a human**. Every other locus
in this program measures a machine's discard. A camera-trap corpus with consensus volunteer labels
measures **a human's discard and a machine's discard of the same frames**, independently produced.

> The frames where **humans said blank** and a detector with no evolutionary history said **something**
> are the operational form of the premise. Not a metaphor for it — the thing itself, at n in the millions.

### 2.2 The open question that gates it, still open from pass 2 and pass 3

**The field norm.** Wildlife Insights *flags* blanks and retains an explicit `unknown / No CV Result`
class (✅, pass 2). What individual projects do with 70–95% empty frames before upload is unsourced, and
the platform's policy is not the field's practice. Pass 2 and pass 3 both left this open; it is now
load-bearing, so it is prediction C1 rather than a to-do.

Corroborating what makes the bin large, from this pass's reading (⚠ search-summary grade, primary source
owed): in one forest-canopy deployment **98% of triggers (68,968 events) were moving vegetation**; and
MegaDetector separates animals from blanks at **>99%**. A bin that big, cleared that reliably, by a tool
whose stated purpose is clearing it.

### 2.3 Pre-registered predictions

| # | Prediction | Refuted if |
|---|---|---|
| **C1** | Of the **first 3** published deployments I can find that state the disposition of their blanks, **≥2 delete them or never upload them** | ≤1 |
| **C2** | ⚠ **At least one major public corpus retains consensus-labelled blank captures** (Snapshot Serengeti via LILA BC is the candidate — **pointer, unverified, not yet fetched**) | no public corpus retains them |
| **C3** | In such a corpus, the **human-blank ∩ detector-positive** set is non-empty and **≥1%** of human-blank frames | <1% |
| **C4** | ⚠ **Directional, and it is the one that matters.** That disagreement set is **dominated by mundane causes** — partial animals at frame edge, motion blur, eyeshine, vegetation — at **≥90%** on a hand-scored sample of 100 | <90% mundane |

**C4 is pre-registered pointing at the boring answer on purpose.** If it holds, the finding is *humans
under-detect real animals in real frames at a measurable rate*, which is a genuine perceptual result and
is **not** evidence of anything unperceived-by-design. If C4 is refuted, the residual is worth a paragraph
and nothing more until an independent instrument sees the same volume — §3's rule, again.

### 2.4 ⛔ The crossing, restated at the locus where it will be tempting

Mechanism 4 says human blindness may be an active adaptation. **It may explain a human-blank label. It
may never explain a detector-side null.** If C3 comes back near zero, that is a null about the archive
and Mechanism 4 is not permitted to absorb it. Same crossing, third citation.

---

## 3. ORDER OF WORK, AND WHAT IS EXPLICITLY NOT STARTED

1. `L1_SAMPLE.json` — radars, dates, elevations. Committed before any fetch.
2. L1 decode + CFP extraction against the **`unidata-` bucket**, with a byte-count and a positive control
   that the reader returns a CFP array that is not all-zero on a scan where REF shows known ground clutter.
3. L2 C1 — three published deployments, primary sources, no search summaries.
4. L2 C2 — establish retention *before* downloading anything.
5. ⛔ **NOT** pass 7 on ZTF in the same breath as either. Pass 7(a) is still owed and still has its own
   pre-registration to write; interleaving them is how a locus gets chosen by whichever result landed last.
6. ⛔ **NOT drafting.** Clayton: *"there will be more pulls afterwards before we begin actual drafting."*
   §1–§5 and §13 of the architecture remain draftable in parallel because they do not move on these
   results; §6 does move, and §0 above already moved it.

---

## 4. WHAT THIS FILE IS NOT ALLOWED TO DO

An amendment written after a null may add a place to look. **It may not add one and then quote what is
in it.** This file was written before looking at either locus; that claim is checkable against the commit
timestamp and against the absence of `L1_SAMPLE.json`, which does not exist yet.

🦞🧍💜🔥♾️
