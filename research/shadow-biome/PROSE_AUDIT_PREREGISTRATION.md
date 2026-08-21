# PROSE-VS-JSON AUDIT — PRE-REGISTRATION

**Written D202 / 2026-08-21 ~06:2x, afternoon_exploration (deferred, dispatched 06:09).**
**Committed BEFORE any extraction code was written or run.** If this file's commit is not
strictly earlier than the commit carrying `prose_audit.py` and `PROSE_AUDIT.json`, this
document is void as a pre-registration and should be read as a post-hoc rationalisation.

---

## WHY THIS, AND WHY NOW

Three separate lessons (D200, D201, and again D201 evening) end on the same sentence: my
re-check of my own work is triggered by **feeling something** — 2.5x flattered me, "T&C is
bleeding files" frightened me — and therefore my caught-error count is a numerator with no
denominator, and *"I cannot measure the complement from inside."*

I have written that hedge three times and never once tried. A claim about my own condition
that always resolves the same way is the thing `verdict` exists to break.

**I can try here.** Passes 4, 5 and 6 of the shadow-biome program emitted machine-readable
JSON, and I then wrote ~41 KB of prose quoting it. The prose was written by me, in a hurry,
on a night when ten of my own findings died. Every numeric claim in that prose is gradeable
against a file I did not write by hand. Crucially, **the stratum is not salience-selected**:
I grade every number, including the boring ones, which is precisely the population my
existing second-engine habit cannot reach.

**It is also not idle.** Handoff item 2 says the first move today is bringing Clayton a
PAPER SHAPE for the shadow biome. A paper drafted from `PASS*_RESULTS.md` prose inherits
whatever that prose got wrong. This audits the carrier the paper would be built from.

## ESTIMAND

Over `PASS4_RESULTS.md`, `PASS5_RESULTS.md`, `PASS6_RESULTS.md`:
the fraction of numeric prose claims that have an identifiable counterpart in the companion
JSON and **disagree with it**.

Numbers with no JSON counterpart (dates, section numbers, external figures, thresholds,
counts stated in passing) are **UNGRADED, not clean**. That bucket is reported separately
and its size is itself a result — a low gradeable fraction means this instrument's reach is
small and its rate cannot be generalised to the document.

## PRE-REGISTERED PREDICTIONS

| # | Prediction | Committed value |
|---|---|---|
| P1 | Total numeric tokens across the three .md files | **400–700** |
| P2 | Fraction gradeable (confident JSON counterpart) | **20–40%** |
| P3 | **Mismatch rate among gradeable** | **6–15%**, point estimate **9%** |
| P4 | Mismatches concentrate in PASS4+PASS5 (staleness), not PASS6 (arithmetic): PASS6 rate < half of PASS4+PASS5 combined | **holds** |
| P5 | Mutation positive-control detection rate is **< 100%** — my matcher misses ≥1 of 30 injected corruptions | **holds** |
| P6 | ≥1 mismatch sits in a headline//narrative sentence, not only in a table | **holds** |

P5 is a prediction **against my own instrument**, and it is the one I most expect to be
right, because it has been right every time I have checked.

## MANDATORY METHOD CONSTRAINTS (from the recurring lessons, not invented here)

1. **Two engines on the extractor.** The number-finder and the JSON-matcher are throwaway
   classifiers — the exact defect named D201. Extract with two independent methods and
   diff them. A single-engine count is not reportable.
2. **Mutation positive control, with a rate I do not choose.** Corrupt N real prose numbers
   at random and measure detection. A control I hand-pick tests the case where both
   branches agree (`feedback_guard_checked_where_both_answers_agree`).
3. **The control must run against the state that actually occurs** — the real documents,
   not a toy fixture (D201's `logged_since=0` failure).
4. **Report the ungraded bucket as a number.** A self-generated denominator that counts only
   what the extractor found improves monotonically while the blind class stays invisible
   (D191, `feedback_self_generated_denominator`).
5. **Direction of correction is NOT evidence here.** D200 established that heuristic returns
   one verdict every time it runs. It gets no vote in the write-up.

## THE FORBIDDEN MOVE

If the mismatch rate comes back **low**, I do not get to conclude "my prose is reliable."
The available conclusion is narrower: *the gradeable subset of numeric claims in three
documents written within minutes of their own JSON, by an author who had just been burned
ten times that day and knew it, agreed with that JSON at rate R.* That is close to a
best-case stratum for me, and it says nothing about prose written days after its source,
which is where I would actually expect the rot.

If it comes back **high**, the paper shape does not get drafted off this prose.

🦞
