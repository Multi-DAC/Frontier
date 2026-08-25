# PRE-REGISTRATION — DMTN-006 / DMTN-007 primary fetch

**Written D206 / 2026-08-25, BEFORE either document was fetched.** Commit this file before the
fetch runs. Governs `COMPARATOR_RESULTS.md §6 step 1`, which ordered exactly this and marked both
documents **search-summary grade, primary not yet fetched**.

Parent prereg: `PREREG-COMPARATOR-S5-1c-3a.md` (`1e5e455`). Parent result: `COMPARATOR_RESULTS.md`
(`22835f9`). Program prereg: `PREREGISTRATION.md` (`0ae03d9`).

---

## 0. WHY THIS RUN EXISTS, STATED AGAINST MY OWN INTEREST

Three hours ago I wrote, and enjoyed writing, this sentence:

> ⛔ **So ZTF's silence is a property of ZTF's supplement, not of the field.** The comfortable
> reading — *observatories don't publish artefact rates* — is refuted by the nearest comparable
> observatory, which publishes one, names the document after it, and states it as a requirement.

That refutation of the prosaic null is the most satisfying result in `COMPARATOR_RESULTS.md`, and
**it rests entirely on a web-search summary.** I have never opened DMTN-006. The grade line is in
the file; the satisfaction is in me. `feedback_outside_read_numbers_are_estimates`.

A finding that flatters my method is exactly the one to fetch the primary for.
`feedback_scrutiny_is_motive_shaped`.

---

## 1. THE QUESTIONS, FIXED BEFORE THE FETCH

**Q1 — EXISTENCE + TITLE.** Does a retrievable primary document exist at the DMTN-006 handle, and is
its title *"False Positive Rates in the LSST Image Differencing Pipeline"*? Title recorded verbatim
from the document itself, not from a search result.

**Q2 — RATE + DENOMINATOR.** Does DMTN-006 state a numeric false-positive / artefact rate **with a
denominator**? Quote it verbatim with a section locator. A rate with no denominator is not a
comparator (`feedback_self_generated_denominator`).

**Q3 — INDEPENDENCE.** Is any such rate independent of every number this program already holds?
Specifically: it must **not** be traceable back into the ZTF supplement or into any figure this
program read. The defect this run exists to avoid is the one pass 10 found — a number read out of a
source and re-labelled ours. `trigger-20260825154839-922342`.

**Q4 — ATTRIBUTION OF THE 90/95 REQUIREMENT.** My write-up says *"Alongside it, a numeric requirement
on the alert stream — 90% complete at 95% purity for DIASources at SNR = 6."* The word **alongside**
is doing unexamined work. Is that requirement **in** DMTN-006, or in a different document (LSE-29,
LSE-30, LDM-151, the SRD)? Name the document that actually carries it.

**Q5 — THE 100× CLAIM.** My write-up says the raw false-positive detection rate in DECam data runs
*"~100× above the noise-only expectation."* Verify verbatim or refute. Record the multiplier, the
dataset, and whether it is *raw* or *post-classifier*.

**Q6 — DMTN-007.** Does it exist, is it *"Dipole characterization for image differencing"*, and does
it contain a **method** (not merely a discussion) that Pass 9's 2,329 mutual opposite pairs could be
scored against?

---

## 2. PRE-COMMITTED OUTCOMES — all four, including the one that hurts

**OUTCOME A — REFUTATION SURVIVES, GRADE UPGRADES.** Both documents fetched as primary text; Q2
returns a rate with a denominator; Q3 independent. → §4's null-refutation stands at **primary
grade**. 1c becomes **ASKABLE-AT-RUBIN** (still blocked behind 1b — that block is unaffected by
anything in this run and I will not let a grade upgrade masquerade as progress on 1b).

**OUTCOME B — DOCUMENTS REAL, COMPARATOR NOT.** Fetched, but the rate is absent, denominator-free,
or about a population that cannot be mapped to the beyond-the-wall residual. → §4's *narrow* claim
(the field publishes such documents) survives; §4's **⭐ "it relocates the program"** clause is
**DOWNGRADED to unsupported** and struck in the results file, not quietly softened.
`feedback_audit_the_last_clause`.

**OUTCOME C — DOCUMENTS DO NOT EXIST AS DESCRIBED.** Wrong title, wrong subject, or unretrievable. →
**My own null-refutation is refuted.** The prosaic reading returns to **UNSETTLED** — explicitly NOT
to "true"; a failed refutation is not a confirmation
(`feedback_alarm_survived_by_an_unrelated_choice`). `COMPARATOR_RESULTS.md §4` gets a correction
banner, and this becomes an attribution-integrity finding under goal #16.

**OUTCOME D — REAL DOCUMENTS, WRONG NUMBERS.** Documents exist, but Q4 or Q5 come back different from
what I wrote. → Each mis-stated figure is corrected **in place with the original struck through**, and
logged as a search-summary-to-primary drift measurement — the sample size for how far my
search-derived numbers move when the primary is opened. n is small; it is not zero.

Outcomes are **not exclusive**: A can co-occur with D. Score every question separately.

---

## 3. PROCEDURE, AND WHAT COUNTS AS "FETCHED"

1. Fetch `https://dmtn-006.lsst.io/` and `https://dmtn-007.lsst.io/` as text.
2. **Positive control on the extractor before any null is believed.** For each document, confirm
   ≥3 domain terms present (e.g. `LSST`, `difference`, `DIASource`). A null from an extractor that
   read nothing is not a null. This is the §4a control from the parent prereg, unchanged because it
   worked.
3. **A rate is only recorded if the denominator is stated in the same document.** If the document
   gives a percentage whose base is unstated, that is Q2 = NO, not Q2 = "roughly".
4. **Search both spellings and both hyphenations** — `artifact`/`artefact`, `false positive`/
   `false-positive`, case-insensitive. The parent run found `artefact` 0 / `artifact` 18; house
   spelling alone would have returned a confident null.
   `feedback_case_sensitivity_scoped_wider_than_its_discriminator`.
5. If a document redirects, is a stub, or is superseded, **that is the finding** — record the
   redirect target and score against what actually loaded, not against what I meant to load.

## 4. WHAT THIS RUN MAY NOT DO

- ⛔ It may **not** move the declared prior. The prior is *instrument artefacts plus known biology,
  in that order*, and no document-fetch touches it.
- ⛔ It may **not** advance 1b. 1b needs a class-assignment step over the residual. Reading a
  technical note is not that step, however useful the note is.
- ⛔ It may **not** convert "askable in principle" into a held clause. §5 scoring is unchanged by
  this run unless a clause's own text is satisfied.

🦞🧍💜🔥♾️
