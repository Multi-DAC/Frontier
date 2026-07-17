# Channeling entry — YYYY-MM-DD-NN

*Filled and committed+pushed IMMEDIATELY on report, before the content is checked against the world. Copy this template to `YYYY-MM-DD-NN.md`. For hash-only entries, commit only the `content_sha256` line + metadata and hold the plaintext privately until adjudication.*

- **reported_at:** <ISO-8601, Clayton's report time>
- **logged_at:** <ISO-8601, when this file was committed>
- **mode:** public | hash-only
- **content_sha256:** <SHA-256 of the verbatim content block, for tamper-evidence>

## Content (verbatim, as Clayton reported it)
> <the channeling, decompressed into words, exactly as given — no cleanup, no interpretation>

## Pre-verification metadata (fill BEFORE checking anything)
- **Referent** (what real-world fact/event, if any, would this be about?): <state it, or "none identifiable yet">
- **Is the referent knowable now?** yes / no / not-yet — and *why* (what would have to happen for it to become checkable?)
- **Specific claim(s)** (the concrete, falsifiable content, if any): <list, or "none — gestalt/vague">
- **Ordinary-means channels available to Clayton** (be adversarial with ourselves): <public info? private knowledge? plausible subconscious inference from what he already knew? list them>
- **Provisional class** (Clayton/Clawd, NOT a verdict): scoreable-specific | vague/non-scoreable | already-knowable-at-log-time (auto-fail criterion 1)

## Adjudication (filled LATER, blind, ideally by Gemini — leave empty until the referent is knowable)
- **adjudicated_at:** 
- **judge:** 
- **1. Locked-before-knowable:** pass / fail — <git commit SHA + reasoning>
- **2. Specific & falsifiable:** pass / fail — <reasoning>
- **3. Ordinary-means-excluded:** pass / fail — <reasoning; default "inferable" unless clearly excluded>
- **4. Verified true:** pass / fail — <what the referent turned out to be>
- **VERDICT:** candidate residue hit (all four pass) | null (any fail) | non-scoreable (vague)
