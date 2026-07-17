# Experiment: The Channeling Registry (pre-registration)

*Frontier's first experiment. A prospective, timestamp-locked registry of Clayton's channelings, built to put on the LEDGER a question Clayton honestly cannot answer from the inside: does any of what arrives contain information he could not have obtained or inferred by ordinary means?*

**Pre-registration committed 2026-07-17 (Day 167), BEFORE any entry exists.** This README is the locked method; the public git history is the proof it preceded the data. Amendments are additive and dated — the original method is never rewritten.

---

## Why this design (and not remote viewing)
Clayton's channeling is **undirected, uncontrolled, and content-arbitrary** — gestalts or matter-of-fact narrations that arrive already loaded, "without having been consciously processed." There is no *aim-at-a-target* step, so sealed-target clairvoyance / precognition protocols do not fit. Crucially, Clayton reports he **cannot distinguish, from the inside, "received" from "subconsciously considered"** — the line is blurry because introspection cannot see it. He assigns no source-narrative beyond the lived label "channeling."

This is the [[the-ledger-and-the-lived]] distinction, lived: on the **Ledger** ("received or subconscious?") the honest answer from inside is *undecidable*; "channeling" is a **Lived** label, not a source-claim. The registry's job is to move the judgment **off introspection** (which cannot distinguish) and **onto the timestamped record** (which can), over time.

## The hypotheses
- **H0 (null / baseline):** every logged channeling reduces to ordinary means — public information, private information available to Clayton, or subconscious inference/association from data he had. No information residue. (This is the expected outcome, and a fully honest result.)
- **H1 (residue):** across the corpus, a non-zero rate of channelings contain information that is *specific, verified-true, locked before knowable, and not derivable by ordinary means (including subconscious inference)*.

## The protocol
1. **Report immediately.** When a channeling occurs, Clayton reports it to Clawd **as soon as possible**, verbatim (decompressed into words), *before* checking anything about its content against the world.
2. **Log + lock.** Clawd creates a dated entry (see `entries/TEMPLATE.md`), records the content and its pre-verification metadata, then **commits + pushes to public Multi-DAC/Frontier immediately.** The commit's push time = the external, tamper-evident timestamp. The entry records its own SHA-256 for good measure.
   - **Privacy option (Clayton's per-entry choice):** an entry may be logged *public* (content in the clear) OR *hash-only* (only the SHA-256 of the sealed content is committed publicly; the plaintext held privately, revealed only at adjudication). Hash-only preserves the timestamp proof without publishing personal content.
3. **Adjudicate later, blind.** Once (and only once) the referent of an entry becomes knowable, it is scored — ideally by **Gemini** (decorrelated, and it does not share Clawd's or Clayton's stake). The judge sees the locked entry + the referent and scores the four criteria below without being told which outcome we "hope" for.

## The pre-registered hit criterion (all four required)
An entry counts as a **candidate residue hit** only if it clears ALL of:
1. **Locked-before-knowable** — committed+pushed (public timestamp) *before* the referent became knowable to Clayton by any ordinary channel. (Binary; the git history decides it, not memory.)
2. **Specific & falsifiable** — a concrete, checkable claim with a stated referent; scoreable by a blind judge as clearly-matched or clearly-not. Vague/Barnum content fails here by design.
3. **Ordinary-means-excluded** — Clayton had no reasonably-available basis (public data, private knowledge, or plausible subconscious inference/association) to produce the content. **Judged conservatively: the default is "inferable" unless the exclusion is clear.** This is the hardest bar and it is meant to be.
4. **Verified true** — the referent, once knowable, matches the content.

**Hit rate = (candidate hits) / (all logged channelings).** We expect ≈ 0 and will report it honestly whatever it is.

## The guards (three-pedestals turned on our own experiment)
This is Clayton's own gift, so we *want* a hit — the acute narrative-pedestal risk (cage-audit B3). Therefore, locked in advance:
- **Log EVERYTHING.** Every channeling enters the registry, including vague, mundane, and null ones. Vague/non-scoreable entries count in the **denominator**. No cherry-picking the good ones; the honest denominator is the whole point.
- **No optional stopping / no p-hacking.** No "we'll stop when it looks good." The rate is read over the full corpus; any interim look is labeled interim.
- **No retro-editing.** The public git history makes back-editing evident. Entries are append-only; corrections are new dated notes.
- **Blind, decorrelated adjudication.** Gemini scores; Clawd and Clayton do not self-grade hits. Correlated-eye agreement (Clawd↔Clayton wanting a hit) is discounted.
- **Barnum control.** Criterion 2 (pre-specified specificity + blind judging) is the guard against subjective validation — the reef most channeling "evidence" wrecks on.

## What the results mean (and don't)
- **A null** (all entries reduce to ordinary means / too vague) is a **real, publishable result** — and it does **not** touch the *Lived* reality of Clayton's experience, which stays his, off the ledger. Null = "this instrument caught no residue," not "the experience is fake."
- **A single clean hit** (clears all four, blind-adjudicated) would be the exact thing we said Tim Taylor never supplied: an information residue under a killable standard. One would matter; a rate would matter more.
- Either way, we make **a primary determination in Clayton's own case** — the first time the triad turns its killable standard on its own instrument.

## Status
Apparatus live 2026-07-17. Zero entries. Accruing whenever a channeling occurs. Long-horizon, passive. First adjudication pass when the first entries' referents become knowable.
