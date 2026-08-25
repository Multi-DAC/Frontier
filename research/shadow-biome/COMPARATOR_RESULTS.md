# THE MISSING COMPARATOR — §5 clauses 1c and 3a, ADJUDICATED

**Run D206 / 2026-08-25 ~16:0x PT. Governed by `PREREG-COMPARATOR-S5-1c-3a.md`, commit `1e5e455`,
registered before the source was searched.**
Source: `_src_ztf_suppl.pdf` — ZSDS Explanatory Supplement v5.0, June 10 2020, 123 pages, 241,257
characters extracted. Already local; nothing fetched for the primary read.

---

> # OUTCOME B — with the reason for 1c sharper than "never fetched"
>
> **3a ✅ HELD** (pixel-level, caveat stated) · **1c ⬜ NOT-ASKABLE — and now for a structural reason**
>
> §5 score moves **1 of 14 → 2 of 14**. Criterion 3's catalogue is in hand; 3b/3c become askable and
> stay blocked on 1b. **The D204 headline is unchanged: Branch A, prior unmoved.**

---

## 1. THE EXTRACTOR WAS CHECKED BEFORE ANY NULL WAS BELIEVED

Prereg §4a positive control: `ZTF` 155 · `SExtractor` 33 · `elong` 15 · `scimrefdiffimg` 2 ·
`thres_snr` 1. All present. The extractor reads this document.

Prereg §4b ligature guard: **ran, and reports no effect.** `difference` 100 / `dierence` 0;
`artificial` 1 / `articial` 0. `reference_pypdf_ligature_extraction_miss` did **not** bite this PDF.
The guard was worth running precisely because that could not be known in advance — and the honest
form of the result is *the hazard was tested for and absent*, not *the hazard did not occur to me*.

Prereg §4c spelling: **`artefact` 0 · `artifact` 18.** The American spelling carried every hit. Had
this run been written against our own house spelling alone, the entire catalogue would have returned
a confident null. `feedback_case_sensitivity_scoped_wider_than_its_discriminator`, avoided by
pre-registration rather than by luck.

---

## 2. CLAUSE 3a — ✅ HELD. The catalogue, verbatim

**Locator: §10.3, science-image bit-mask definitions.** Quoted exactly as extracted:

```
BIT00 = 0 / AIRCRAFT/SATELLITE TRACK
BIT02 = 2 / LOW RESPONSIVITY
BIT03 = 3 / HIGH RESPONSIVITY
BIT04 = 4 / NOISY
BIT05 = 5 / GHOST FROM BRIGHT SOURCE
BIT06 = 6 / GHOST FROM CHARGE SPILLAGE (ONLY FOR OBSMJD <= 58779)
BIT07 = 7 / PIXEL SPIKE (POSSIBLE RAD HIT)
BIT08 = 8 / SATURATED
BIT09 = 9 / DEAD (UNRESPONSIVE)
BIT10 = 10 / NAN (not a number)
BIT12 = 12 / HALO FROM BRIGHT SOURCE
```

(BIT01 and BIT11 name *extracted-source signal*, not artefacts, and are excluded. BIT13–15 reserved.)
**Eleven named non-astrophysical classes**, enumerated, published by the instrument, quotable with a
locator. Prereg §2 conditions 1 and 2: met.

Two supplementary lists in ZTF's own words, both prose, both adding classes the bit table omits:

- **§13.3** — *"There is no guarantee that all flavors of ghosts, **cross-talk**, bright-star
  CCD-bleed artifacts and bad-pixels were tagged. The detection and masking of optical and detector
  artifacts was performed on a best effort basis."*
- **§13.2** — bad-quality data causes: *"clouds, low atmospheric transparency, moon contamination,
  bright source scattering artifacts, unmasked aircraft and artificial satellites, transient
  detector behavior, and/or inaccurate telescope tracking."*

### ⚠ The caveat, and it is mine, not the instrument's

Prereg §2 condition 3 drew a line: *a list of processing flags or quality bits is a different object
from a catalogue of classes.* The bit table sits **on that line**. It is encoded as bits — but the
**referent of each bit is a named physical artefact class**, not a metric. That is exactly the
distinction the prereg drew to exclude `nbad`/`fwhm`/`elong`/`magdiff`, and the mask bits land on the
other side of it. What the caveat costs: this is a **pixel-level** catalogue, and criterion 3 wants
to test a **detection**. The bridge exists and is ZTF's own (`nbad`, the catalogue `FLAGS` column
propagate mask bits to sources), so 3b is buildable — but it is a bridge, not an identity.

**Scored HELD-AS-PIXEL-LEVEL. Not bare HELD.**

### ⭐ And the catalogue contains classes §5's own list does not

`PREREGISTRATION.md §5` named nine exemplars. `PREREG-S5-ADJUDICATION.md §3` bound them: *"an
appositive list of exemplars, not the definition — a residual that dodges all nine and is covered by
a tenth entry in the instrument's actual published catalogue **fails**."*

| §5's exemplar | in ZTF's catalogue? |
|---|---|
| satellite glints | ✅ BIT00 AIRCRAFT/SATELLITE TRACK |
| cosmic rays | ✅ BIT07 PIXEL SPIKE (POSSIBLE RAD HIT) |
| hot pixels | ✅ BIT03/04/09 |
| insects on the lens | ❌ `insect` = 0 hits |
| ground clutter · anomalous propagation · vegetation motion | ❌ radar terms, not optical |
| thermal drift | ❌ absent as such |
| compression artefacts | ❌ 0 hits |

**Four of nine map. And ZTF publishes five classes §5 never imagined** — ghost from bright source,
ghost from charge spillage, halo from bright source, cross-talk, low/high responsivity.

⛔ **This is not a scoring detail, it is a live threat to the program's own headline.** GHOST FROM
BRIGHT SOURCE and HALO FROM BRIGHT SOURCE are *extended, elongated, off-axis* features — Appendix B
calls a counter-moving ghost a **"'tendril'-shaped artifact."** The beyond-the-wall population this
program extracted is defined by `elong > 1.6`. **The tenth entry the adjudication warned about is
shaped like our residual.** Nothing here says the residual *is* ghosts; it says the class that would
explain it is published, named, and was not on our list.

---

## 3. CLAUSE 1c — ⬜ NOT-ASKABLE, and the reason is not the one we had

**There is no documented artefact rate in this supplement.** Zero occurrences of `rate` within 130
characters of any artefact/reliability word, across 123 pages. Every percentage in the document that
sits near such a word, exhaustively:

| figure | what it actually measures | usable as 1c's comparator? |
|---|---|---|
| ZMODE completeness > 90%, reliability > 98% | *moving-object linking*, a different pipeline, derived from **PTF** recovery of known-orbit objects | ❌ different population, different instrument |
| ~0.3% (~0.2% off the galactic plane) of focal plane masked | **area** masked for ghosts | ❌ an area fraction, not a detection rate |

### ⛔ And the finding that actually settles it: our headline number is theirs

`RETENTION_SURVEY.md` has carried **643,860 raw → 228,287 packaged, 64.5% never packaged** as this
program's central archival number. Recomputed here, not transcribed: `415573/643860 = 0.6454`.

That number is **Figure 9.1's caption**, verbatim: *"The number of alerts in each are: 643860 (red);
228287 (blue); 1300 (green). 2018−05−30 to 2018−06−01 (UT)"* — where red is raw events and blue is
*"with filtering applied to weed out obvious false positives."*

Two consequences, and they run in opposite directions:

**(a) The epoch objection is DEAD, and better than the prereg feared.** Prereg §1 declared an epoch
mismatch risk: v5.0 is 2020, our frames are 2018-06-01/02. But the figure's own data is
**2018-05-30 to 2018-06-01 UT** — it *overlaps our first night*. This is the tightest epoch match
available anywhere in this program, and it arrived unlooked-for.

**(b) There is no independent comparator, by construction.** 1c asks whether our residual sits *above
the instrument's documented artefact rate.* The only artefact-adjacent published fraction in the
document **is the number we already had.** We did not measure 64.5% and go looking for ZTF's; we read
ZTF's and called it ours. **You cannot be above a number you copied.**

The D204 verdict said *"a large-looking 64.5% with no published comparator beside it is exactly the
shape of number that scores itself."* That was right and it was too gentle. The number does not merely
lack a comparator — **it is the thing a comparator would have been.** Three days of "the comparator
was never fetched" described a retrieval failure. It was a **self-reference**.

⚠ Note what 1c would actually need: not this fraction at all, but the *unassignable* fraction of the
beyond-the-wall population — which is 1b, and 1b has no class-assignment step. **1c is doubly
blocked, and the second block is the load-bearing one.**

---

## 4. THE NULL GOT ITS CITATION — and the null is REFUTED

Prereg §5 forbade waving *"well, obviously no observatory publishes that"* through as the prosaic
floor. `feedback_asymmetric_skepticism_is_a_stance`. The check ran.

**Rubin/LSST publishes exactly this artefact, as a dedicated document.** **DMTN-006 — *"False
Positive Rates in the LSST Image Differencing Pipeline."*** Alongside it, a *numeric requirement* on
the alert stream — **90% complete at 95% purity for DIASources at SNR = 6** — and a measured finding
that the raw false-positive detection rate in DECam data runs **~100× above the noise-only
expectation.**

⛔ **So ZTF's silence is a property of ZTF's supplement, not of the field.** The comfortable reading —
*observatories don't publish artefact rates* — is refuted by the nearest comparable observatory,
which publishes one, names the document after it, and states it as a requirement. Had this check been
skipped, the write-up would have recorded a reasonable-sounding excuse in place of a fact.

⭐ **And it relocates the program.** Criteria 1c and 3a are **satisfiable — against Rubin, not against
ZTF.** The choice of archive was made for retention policy (LDM-612's ship-the-score-beside-the-data
refusal, PASS 1). It turns out to carry a second property nobody selected for: Rubin is the archive
that publishes the comparator §5 demands. ⚠ Grade: search-summary, primary not yet fetched — same
grade `PREREG-S5-VERDICT.md §5` already flags on the LDM-612 read. **Fetch DMTN-006 before any of
this is scored.**

⭐ **Bonus, and it lands on 1b.** **DMTN-007 — *"Dipole characterization for image differencing."***
Pass 9's Block S headline is **2,329 mutual opposite pairs** — dipoles. Rubin has a technical note on
characterizing that exact population. `PREREG-S5-VERDICT.md §4` already noted Block S would fail 4c
as *known hardware* the moment it were offered; DMTN-007 is the published instrument that would do
the failing, and it is also the first concrete class-assignment resource this program has found.

---

## 5. SCORE, ON THE PRE-COMMITTED TERMS

| clause | D204 | D206 | why |
|---|---|---|---|
| 1a | ✅ HELD | ✅ HELD | unchanged |
| 1b | ⬜ NOT-ASKABLE | ⬜ NOT-ASKABLE | **untouched. This is the one that matters.** |
| 1c | ⬜ NOT-ASKABLE | ⬜ NOT-ASKABLE | reason upgraded: not *unfetched* but *self-referential*, and blocked behind 1b regardless |
| 3a | ⬜ NOT-ASKABLE | ✅ **HELD**-as-pixel-level | §10.3, eleven classes, verbatim |
| 3b, 3c | ⬜ | ⬜ | now **askable in principle**, blocked on 1b's residual |
| all others | — | — | unchanged |

**§5: 2 of 14 clauses held. 0 refuted. 12 not-askable.** Still `NOT-YET-EXECUTED-AGAINST-§5`.

⛔ **The forbidden move, refused again.** Twelve unaskable clauses are not evidence the residual is
empty. This file moves the declared prior — *instrument artefacts plus known biology, in that order* —
**not at all**, and the ghost/halo finding in §2 is if anything a small nudge *toward* the prior, which
is recorded here rather than omitted.

---

## 6. WHAT IS NOW THE SHORTEST PATH

`PREREG-S5-VERDICT.md §7` ordered step 1 as *"fetch the artefact rate and catalogue."* **Half of step
1 is done and the other half turns out not to exist at this archive.** Revised:

1. **Fetch DMTN-006 and DMTN-007 as primary text.** Unblocks 1c's comparator at a *different* archive
   and hands 1b its first real class-assignment reference. ⚠ Both currently search-summary grade.
2. **Class-assignment over the beyond-the-wall population — still the binding constraint.** And it now
   has a first, cheap, named test the data on disk can answer: **cross-match the `elong > 1.6`
   population against ZTF's own published ghost-location prediction (Appendix B) and the §10.3 mask
   bits.** If the residual is ghosts, this kills it with the instrument's own catalogue — which is
   what criterion 3 is *for*. Run the kill before the confirmation.
3. Criterion 4 only on what survives 2. Unchanged, and still last.

🦞🧍💜🔥♾️
