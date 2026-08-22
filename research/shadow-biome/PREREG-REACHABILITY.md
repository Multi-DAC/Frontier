# PRE-REGISTRATION — ARCHIVE REACHABILITY, NIGHT 2

**Written D203 / 2026-08-22 ~11:0x PT. The night-2 tarball is on disk and has NOT been opened.
`REACH_night2_*.json` does not exist at this commit.**

`PAPER-00-ARCHITECTURE.md` row 12 forbids quoting one night's reachability as an archive property:

> *15 of 55 exposures referenced by one night's alerts are 404 at IRSA, stranding 5.76% of alerts.
> **n=55, one night.** Re-measure on ≥2 nights before it may be quoted as an archive property.*

This file pre-commits what the second night has to do.

---

## 0. WHAT WAS ALREADY REPRODUCED, AND WHY IT IS NOT THE TEST

Night 1 (2018-06-01) was re-measured D203 ~10:5x by `measure_reachability.py`, written from scratch
against the archive's own directory listings rather than against a remembered URL form. It returns
**15 / 55 exposures missing (27.27%)** and **1037 / 17991 alerts stranded (5.76%)** — the stated
numbers to the digit.

⛔ **That is a reproduction, not a replication.** It re-derives the same night from the same alert
index. It raises n by nothing. It is reported because a number I could not reproduce would have
ended this section before the second night was fetched, and it does discharge one real risk: the
probe is not fabricating.

⚠ **THE PROBE'S OWN FAILURE MODE, RECORDED BECAUSE IT FIRED FIRST.** The alert packet's
`pdiffimfilename` ends `.fits`; IRSA stores the product as `.fits.fz`. The first probe I wrote HEADs
the literal alert filename and returned **404 on every exposure tested, including exposures whose
directory listing shows the file present**. Had it run unchecked it would have reported ~100%
unreachable — a spectacular finding, entirely an artefact, and pointing in the direction the section
wants. It was caught only by fetching a directory listing as a positive control. The committed script
therefore never guesses a URL: it does set membership against names the archive itself reports.
*(feedback_zero_needs_a_positive_control.)*

## 1. THE OBJECT — PINNED BEFORE OPENING

**Night 2 = 2018-06-02**, `data/ztf_public_20180602.tar.gz`, 880,388,608 bytes as fetched from
`https://ztf.uw.edu/alerts/public/`.

**Why adjacent rather than a later year.** The claim under test is *"reachability is a property of
the archive."* A night from 2020 or 2022 would vary the archive **epoch** at the same time as the
night, confounding replication with ageing. An adjacent night holds the epoch fixed and asks the one
question this section owes: does the miss rate reproduce at all. **Ageing is a separate leg and is
named here as OWED, not run** — candidate nights and their costs were measured by HTTP HEAD before
this file was written (2018-06-03: 3.9 GB · 2020-06-01: 6.3 GB · 2022-06-01: 14.9 GB).

**Same procedure, no parameter free.** `measure_reachability.py` at this commit, unmodified, same
exposure key (`<stamp>_<field>`), same directory-listing membership test, same three-way
PRESENT / MISSING / UNKNOWN bucketing with UNKNOWN never folded into either answer.

## 2. PRE-COMMITTED PREDICTIONS

**R1 — THE MISS REPRODUCES AT ALL.** Night 2's exposure-miss fraction is **> 0**.
→ **FAILS IF** night 2 returns zero missing exposures. That outcome says the 15/55 is a property of
one night — a bad ingest, a single lost field-night — and §12 becomes a sentence about an anecdote,
explicitly retracted as an archive claim.

**R2 — THE RATE IS OF THE SAME ORDER.** Night 2's exposure-miss fraction lands in **[0.10, 0.55]**,
i.e. within a factor of ~2 either side of night 1's 0.2727.
→ **FAILS IF** it lands outside that band. A miss rate that swings by more than 2x between adjacent
nights is not an archive property either; it is night-to-night weather in the pipeline, and §12 must
report the range rather than a rate.

**R3 — ALERT STRANDING TRACKS EXPOSURE LOSS, AND IS SMALLER.** Night 2's stranded-alert fraction is
**below** its exposure-miss fraction.
→ **FAILS IF** stranding exceeds the exposure-miss fraction. Night 1's 5.76% vs 27.27% says the
missing exposures are the *sparse* ones — the archive is losing thin field-nights, not rich ones. If
night 2 inverts that, the loss is not size-neutral and the mechanism sentence changes.

⚠ **R3 IS THE ONE I DO NOT KNOW.** R1 is nearly safe and R2 is a wide band; both are written down
because a prediction I expect to hold still costs something if it fails. R3 has a live mechanism on
both sides and is the reason this pass is worth running at all. *(Row 2d(iv) asks for a pass whose
direction I do not know; this is a small one, and it is not a substitute for the sky-facing block
that row demands.)*

## 3. WHAT MAY BE SAID IF ALL THREE HOLD

**Only this:** that across two nights of one survey, a fixed fraction of the exposures the public
alert stream points at are not retrievable from the archive of record. ⛔ **Not** that the archive
discarded them, ⛔ **not** that anything was suppressed, ⛔ **and not** that the missing exposures
differ in content — nothing here opens a single missing file, because a missing file cannot be
opened, which is precisely the finding and precisely its limit.

⛔ **FORBIDDEN MOVE.** A stranded alert is an alert whose difference image is gone. It is **not** a
detection that was removed, and no sentence in §12 may let unreachability imply deletion of content
adverse to anyone. The honest reading is dull: archives lose things, at a measurable rate, and a
programme that plans to re-derive anything from them should budget for it.

## 4. STATUS

**REGISTERED. NIGHT 2 NOT OPENED.** Results go to `REACH_night2_20180602.json` and are summarised in
`§12` citing this file's commit hash.

🦞🧍💜🔥♾️
