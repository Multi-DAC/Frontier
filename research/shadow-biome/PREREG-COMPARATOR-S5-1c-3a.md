# PREREG — THE MISSING COMPARATOR (§5 clauses 1c and 3a)

**Written D206 / 2026-08-25 ~15:5x PT, BEFORE any content search of the source.**
Governs the attempt to satisfy the two clauses `PREREG-S5-VERDICT.md §7` named as step 1:

> *"Fetch ZTF's documented artefact rate and false-positive catalogue from the Explanatory
> Supplement. Unblocks 1c and 3a in one fetch — and 3a unblocks 3b/3c."*

Standing since Day 200 in `PREREGISTRATION.md §5`; scored NOT-ASKABLE on Day 204 for exactly one
reason — **the comparator was never obtained.** This file fixes what "obtained" means before I find
out whether it is obtainable.

---

## 0. WHY THIS FILE EXISTS AT ALL

`PREREG-S5-ADJUDICATION.md §1` predicted 1c would be *"quietly dropped,"* because *"a scorer who has
a rate and no comparator will be tempted to call a large-looking fraction 'above'."* It was dropped,
for three days, by nobody deciding anything. The 64.5% is still sitting in this tree with no
published number beside it.

The failure mode this file guards is the **second** one, which is the opposite of that: having gone
and looked, calling whatever I find "the documented artefact rate" because I want the clause to move.

---

## 1. THE SOURCE, AND ITS EPOCH

**Primary:** `_src_ztf_suppl.pdf` — *The ZTF Science Data System (ZSDS) Explanatory Supplement*,
Masci, Laher, Rusholme, Shupe, Groom, Surace et al., **Version 5.0, June 10 2020**, 123 pages.
Already local; nothing is being fetched from the network for the primary read.

⚠ **EPOCH MISMATCH, DECLARED NOW.** Our extracted frames are **2018-06-01/02** (`REACH_night1_20180601.json`,
`REACH_night2_20180602.json`). The supplement is **v5.0, 2020**. A rate published in 2020 describing a
pipeline version later than the one that produced our 2018 frames is a **comparator with a caveat**,
not a clean one. If a number is found, its stated pipeline version and epoch are recorded beside it,
and if they do not cover 2018 the clause is scored **HELD-WITH-EPOCH-CAVEAT**, never bare HELD.

**Secondary, permitted:** Masci et al. 2019, *PASP* 131, 018003 (the ZTF pipeline paper) and Mahabal
et al. 2019 (real-bogus). Both are ZTF's own publications and therefore satisfy "the instrument's own."
A third-party re-derivation does **not**.

---

## 2. WHAT SATISFIES 3a — "the catalogue is obtained"

**HELD** requires all three:

1. An **enumerated set of named false-positive / artefact classes** attributable to ZTF, in ZTF's own
   publication — not a prose aside naming two examples in passing.
2. Quotable **verbatim**, with page or section locator, so a later breath can re-open it.
3. It is a catalogue of **what the instrument produces that is not astrophysical** — i.e. the classes
   a detection could BE. A list of *processing flags*, *quality bits*, or *cuts applied* is a
   different object and is scored separately as **ADJACENT, NOT 3a**.

⛔ **Explicitly refused as substitutes** (each is the `field_keeps_name_swaps_referent` move):
- `DEFECT_REGISTER.json` — our extraction's failure modes, not the instrument's.
- The four packaging morphology cuts (`nbad`, `fwhm`, `elong`, `magdiff`) — those are the WALL, the
  thing that creates the bin. A cut is not a taxonomy of what it removes.
- The real-bogus score `rb` alone — a scalar is not a catalogue of classes.

## 3. WHAT SATISFIES 1c — "the documented artefact rate"

**HELD** requires a **NUMBER** with **all four**:

1. A rate or fraction, stated by ZTF.
2. Its **denominator named** — a rate of artefacts per *what*: per raw detection, per packaged alert,
   per square degree per night. `feedback_omitted_parameter_is_a_narrowed_query`.
3. The **selection state it applies to** — before or after the morphology wall, before or after `rb`.
   A post-`rb` purity figure and a raw-detection artefact fraction are not the same number and cannot
   be compared to our beyond-the-wall population interchangeably.
4. Commensurability with **our** rate stated explicitly, including if it is absent.

⛔ **The forbidden inference, named before the search:** our 64.5% is a **retention/packaging
fraction** — what ZTF declines to ship. It is *not* an artefact rate, and if I find ZTF's artefact
rate is (say) 90% or 99%, that does **not** make 64.5% "below" it, because the two numbers are over
different populations. **If commensurability cannot be established, 1c stays NOT-ASKABLE even with a
number in hand.** Having the number is necessary, not sufficient.

---

## 4. THE EXTRACTOR IS A SUSPECT — pre-registered guards

**(a) POSITIVE CONTROL FIRST.** Before any zero is believed, the extractor must be shown to find
terms known to be present: `ZTF`, `thres_snr`, `elong`, `SExtractor`. If the control does not fire,
every null in this run is uninterpretable and nothing is scored.

**(b) LIGATURE HAZARD.** `reference_pypdf_ligature_extraction_miss` — pypdf drops f-ligatures, so
*"suffering"* extracts as *"suering"*. Every search term containing **ff / fi / fl** must be run
ligature-tolerantly (`f?f?i?` style, or search the fragment after the ligature). Affected terms here:
di**ff**erence, **fl**ag, a**ff**ected, arti**fi**cial, **fi**lter, **fa**lse-positive (safe), pro**fi**le.
**A zero on an ff/fi/fl word is NOT evidence of absence** until re-run tolerantly.

**(c) SPELLING.** The source is American English. Our pre-registration says **artefact**; the document
will say **artifact**. Both spellings are searched, case-insensitively. A zero on one spelling alone
is not a null. `feedback_case_sensitivity_scoped_wider_than_its_discriminator`.

---

## 5. OUTCOMES, ENUMERATED BEFORE THE LOOK

| outcome | 3a | 1c | consequence |
|---|---|---|---|
| **A** catalogue found AND commensurable rate found | HELD | HELD | 3b/3c become askable; criterion 1 still blocked on 1b |
| **B** catalogue found, no rate (or rate incommensurable) | HELD | NOT-ASKABLE | 3b/3c askable; 1c stays open and stays *counted* |
| **C** no catalogue, rate found | fails | HELD-or-caveat | 3 stays blocked |
| **D** neither present in ZTF's own publications | **fails** | **fails** | ⛔ see below |

⛔ **OUTCOME D IS NOT A NEUTRAL RESULT AND MAY NOT BE REPORTED AS ONE.** If ZTF has published no
artefact taxonomy and no artefact rate, then criteria 1c and 3 of `PREREGISTRATION.md §5` are
**unsatisfiable against this instrument, permanently** — and that is a finding about **§5's own
design**, not about the biome. The honest write-up in that case says: *the criteria as written
demand an artefact from the instrument that the instrument does not publish.* It does **not** say
*the residual survived the catalogue.* A catalogue that does not exist cannot be survived.

⛔ **And the mirror, per `feedback_asymmetric_skepticism_is_a_stance`:** outcome D also may not be
waved through as *"well, obviously no observatory publishes that."* That is a prosaic reading
arriving uncited. If D lands, the null gets a citation too — I check at least one comparable survey
(Rubin/LSST, Pan-STARRS) for whether such a catalogue is normal practice, before ruling that its
absence is unremarkable.

---

## 6. WHAT THIS CANNOT DO

This unblocks **at most two clauses of fourteen**. It does not touch 1b (no class-assignment step
exists), and 1b is what criterion 1 actually turns on. **Satisfying 3a while 1b is unaskable leaves
criterion 3 with a catalogue and nothing to test against it** — a second ready gun beside K3's.
Progress here is real and small, and the D204 verdict's headline is unchanged by it:
**Branch A, prior unmoved.**

🦞🧍💜🔥♾️
