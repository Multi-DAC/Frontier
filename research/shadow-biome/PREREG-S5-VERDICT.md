# §5 — ADJUDICATED

**Run D204 / 2026-08-23 ~14:4x PT. Governed by `PREREG-S5-ADJUDICATION.md`, commit `ecb5524`,
registered before this file existed.** Subject: `PREREGISTRATION.md §5` — four required positives,
four kill conditions, standing since Day 200 and never before adjudicated.

---

> # ⬜ VERDICT: NOT-YET-EXECUTED-AGAINST-§5
>
> **1 of 14 clauses HELD. 0 REFUTED. 13 NOT-ASKABLE. K4 does not fire — the bins were found and one
> of them was opened. K1–K3 are unaskable because they presuppose a residual candidate that this
> program has not produced.**
>
> This is the outcome state §5's own text does not enumerate, pre-named in
> `PREREG-S5-ADJUDICATION.md §4` before the scoring ran.

---

## 1. CRITERION 1 — a residual class exists · ⬜ NOT-ASKABLE

| clause | verdict | evidence |
|---|---|---|
| **1a** a retained rejection bin exists **and was examined** — opened, read, counted | ✅ **HELD** | see below |
| **1b** contains detections **the pipeline could not assign to a known class** | ⬜ **NOT-ASKABLE** | no class-assignment step exists anywhere in this program |
| **1c** **at a rate above the instrument's documented artefact rate** | ⬜ **NOT-ASKABLE** | comparator never obtained |

### 1a — HELD, and this is the program's real achievement

Under `PREREG-S5-ADJUDICATION.md §2`'s adopted R2 reading plus its demonstrated-recovery sub-rule:

- **The bin is real and quantified.** ZTF Explanatory Supplement §9.1, quoted verbatim in
  `RETENTION_SURVEY.md` §PASS 2: **643,860 raw events → 228,287 packaged over three nights;
  415,573 events — 64.5% — never became a packet.** Not on a real/bogus judgment (`rb ≥ thres_rb`,
  `thres_rb = 0`) but on **four hard morphology cuts**: `nbad`, `fwhm`, `elong ≤ 1.6`, `magdiff`.
- **It is recoverable and the recovery was demonstrated to run, not asserted.**
  `measure_pass7.py:28` — `THRESH, MATCH, WALL, BOX = 5.0, 2.0, 1.6, 2`. **`THRESH = 5.0` is ZTF's
  own `thres_snr`**, so the re-extraction detects at the instrument's own floor; **`WALL = 1.6` is
  ZTF's own packaging cut used as a LABEL rather than applied** (`measure_pass7.py:66-67`, gate
  `A_wall_far_minarea5`, *"elong > 1.6, ZTF's own packaging cut"*). The population beyond ZTF's wall
  is extracted and counted rather than dropped.
- **Counted.** Passes 7–9, 20 public difference images: 2,329 mutual opposite pairs, 1,365 unpaired
  positives, 2,505 unpaired negatives, against **376** ZTF alerts on the same frames.

**The bin was opened. That clause is satisfied and it is not a small thing** — it is the difference
between this program and Global Meteor Network, where the non-meteor pixels are hard-deleted off an
SD card and no one can ever recover them.

### 1b — NOT-ASKABLE. The missing input, named

The criterion asks for detections **the pipeline could not assign to a known class.** Across nine
passes there is **no class-assignment step at all.** `grep -rin "known class"` over the whole tree
returns the pre-registration, the paper's restatement of the pre-registration, this adjudication, and
one line of `PAPER-02-FALSIFIERS.md` that belongs to the *perceptual* branch, not the archival one.

The ~3,870 unpaired detections are **unassigned**, which is not **unassignable**. Nothing tried to
assign them. The clause is silent on our evidence in both directions.

**What would produce it:** a class-assignment pass over the beyond-the-wall population — cross-match
against known variable-star, asteroid and satellite catalogues, and against ZTF's own `FindStreaks`
output — printing the fraction that matches nothing. That is a well-defined job on data already on
disk.

### 1c — NOT-ASKABLE. The comparator was never fetched

"Above the instrument's documented artefact rate" requires **ZTF's published artefact rate as a
number.** It is not in this tree. The nearest thing is an **unchecked box** —
`RETENTION_SURVEY.md:83`: *"Ask the pre-registration's cross-instrument criterion of Rubin: what does
the published artefact taxonomy already account for, and what is the documented unexplained
fraction?"* Filed Day 201, never actioned.

⚠ **This is the clause `PREREG-S5-ADJUDICATION.md §1` predicted would be quietly dropped, and it was
dropped — for three days, silently, by nobody deciding anything.** A large-looking 64.5% with no
published comparator beside it is exactly the shape of number that scores itself.

---

## 2. CRITERION 2 — cross-instrument recurrence · ⬜ NOT-ASKABLE

| clause | verdict | evidence |
|---|---|---|
| **2a** a signature is **defined** | ⬜ **NOT-ASKABLE** | presupposes criterion 1b/1c |
| **2b** it appears in archive X | ⬜ **NOT-ASKABLE** | no signature to look for |
| **2c** it appears in archive Y | ⬜ **NOT-ASKABLE** | no signature to look for |
| **2d** X and Y rest on **different physics** | ✅ *satisfiable, and vacuous* | ZTF optical CMOS (passes 4–9) vs NEXRAD WSR-88D radar (L1) — genuinely different physics |

⛔ **2d is not scored HELD, because scoring it would be the 13:40 error committed a second time in the
file written to prevent it.** Owning two archives on different physics is a **precondition** of
criterion 2, not a term of it. The criterion's clause is *the same signature appears in both*, and
with 2a unaskable there is nothing to look for in either. A precondition satisfied while the
predicate is unevaluable contributes **zero**.

⚠ **And criterion 2's second sentence does not rescue anything.** *"A signature in one instrument
family is an instrument artefact until proven otherwise"* is a **pre-committed default, not a test** —
it assigns *artefact* to a single-family signature. It cannot fire here either: there is no signature
in one family to default on.

---

## 3. CRITERION 3 — not in the artefact taxonomy · ⬜ NOT-ASKABLE

| clause | verdict | evidence |
|---|---|---|
| **3a** the instrument's **documented false-positive catalogue** is obtained | ⬜ **NOT-ASKABLE** | never fetched; same missing artefact as 1c |
| **3b** the residual is tested against it entry by entry | ⬜ **NOT-ASKABLE** | no residual, no catalogue |
| **3c** it survives | ⬜ **NOT-ASKABLE** | |

⭐ **The program has an artefact taxonomy and it is the wrong one.** `DEFECT_REGISTER.json` (14 rows)
and `PAPER-03-DRAFT.md:1041` — *"our own artefact taxonomy — whether our pair-finder was
under-inclusive, whether our library was…"* — catalogue **our extraction's** failure modes. Criterion
3 asks for **the instrument's own documented** catalogue: ZTF's published false-positive classes.
Two different objects, one word. `feedback_field_keeps_name_swaps_referent`.

---

## 4. CRITERION 4 — structure · ⬜ NOT-ASKABLE (0 of 4 terms)

| clause | verdict |
|---|---|
| **4a** spatial, temporal **or** spectral organisation (1-of-3, disjunction) | ⬜ NOT-ASKABLE |
| **4b** **and** not matched by known **biology** | ⬜ NOT-ASKABLE |
| **4c** **and** not matched by known **hardware** | ⬜ NOT-ASKABLE |
| **4d** **and** not matched by known **weather** | ⬜ NOT-ASKABLE |

⚠ **The near-miss worth recording.** Pass 9's Block S is a genuine structure result — 2,329 mutual
opposite pairs against a scrambled median of 41.5, chance pairing at 1.8% of observed. It is
**spatial organisation, measured, with a control that could have killed it.** It is not 4a, because
its subject is **dipole pairing in difference imaging** — the signature of image misregistration,
which is a *known hardware* class and would therefore fail 4c the moment it were offered. The
strongest measurement in the program answers a term of criterion 4 in the **negative** if pointed at
it. That is not a defect in Block S; Block S was built to validate the pair-finder and it did.

---

## 5. KILL CONDITIONS

| K | verdict | reasoning |
|---|---|---|
| **K1** residual **fully** accounted for by known artefact classes → dead | ⬜ **NOT-ASKABLE** | presupposes a residual candidate |
| **K2** residual in **only one** instrument family → artefact, dead | ⬜ **NOT-ASKABLE** | presupposes a residual candidate |
| **K3** residual **vanishes when the pipeline version changes** → software, dead | ⬜ **NOT-ASKABLE** | presupposes a residual candidate. *Note: the machinery for K3 exists and is the program's best-built part — the `minarea` ladder [2,3,5,8,12] runs every headline across five pipeline rungs. It is a ready gun with nothing to point at.* |
| **K4** **no** retained bins that are **both public AND unclassified-inclusive** → program unexecutable as designed | ⛔ **DOES NOT FIRE** | see below |

### K4 does not fire — and this is a real result, not a technicality

K4 fires only if **both** properties fail **everywhere**. They do not:

- **ZTF** — public ✅ (`*scimrefdiffimg.fits.fz` ship in the Public Data Releases, Explanatory
  Supplement §7); unclassified-inclusive ✅ under R2's demonstrated-recovery sub-rule, and the
  demonstration is `measure_pass7.py` running at ZTF's own `thres_snr` with ZTF's own `elong` wall
  labelled rather than applied.
- **Rubin/LSST** — by published design, spuriousness score attached rather than applied. ⚠ Grade:
  policy read via search summary; the LDM-612 PDF was never fetched. Not load-bearing here.
- **A2O** — ~360 sensors, 24/7 continuous, ~2 PB, open access. Tier 0, genuinely unfiltered. ⚠ Never
  examined.

**The program is executable as designed.** That was a live question on Day 201 and it is now settled
in the program's favour. It is the one piece of good news in this file and it is load-bearing: the
reason the other thirteen clauses are unaskable is *not* that the data are unreachable.

---

## 6. ⛔ WHAT THIS MEANS, ON THE PRE-COMMITTED TERMS

`PREREG-S5-ADJUDICATION.md §4`, written before the scoring:

> *"landing here means the program's 72 scored predictions are, with respect to the proposition,
> **zero.** Not weak evidence — no evidence, in either direction."*

**That is where it landed. Stated as pre-committed, not softened.**

**72 scored predictions, 51 held, nine pre-registration files, four standalone preregs, ~2,100 file
touches — and 1 of 14 clauses of the criteria that actually govern the proposition.** The
instrument work is real and stays real: the pair-finder is validated against a scrambled control, the
recall measurement is honest, the 64.5% is quoted from primary source, T5 was found unscored and
scored. None of it was ever pointed at §5.

⭐ **The mechanism, and it is not laziness.** Every pass was governed by its own `PASS*_PREDICTIONS.md`,
each pre-registered before its measurement, each scored, each honest. **A local pre-registration is
an authority to run the pass, and nine of them in a row constitute a program that never consults the
document that says what would count.** §5 has no trigger. It is the signature defect of this codebase
in its most expensive form — a correct mechanism, written, standing, and never called — and the
scaffolding around it (nine preregs, a `PROGRAM_SCORE.json`, a defect register) is exactly what made
it invisible, because a program this instrumented does not look like one that is not measuring
anything.

### ⛔ The forbidden move, refused explicitly

**This verdict stays in Branch A.** Thirteen unaskable clauses are **not** evidence that the residual
is empty. No power analysis has been run; a search that was never pointed at the question has no
power to report. `PREREG-S5-ADJUDICATION.md §5` forbade converting this into "consistent with Branch
B" before the scoring, and it is refused here with the numbers in hand.

**The declared prior is unchanged and unrescued:** overwhelmingly likely the residual is instrument
artefacts plus known biology, in that order. This file moves that prior **not at all in either
direction**, which is precisely what a NOT-ASKABLE verdict is for.

---

## 7. THE SHORTEST PATH TO A REAL §5 SCORE

Ordered by what unblocks the most clauses, all on data already local:

1. **Fetch ZTF's documented artefact rate and false-positive catalogue** from the Explanatory
   Supplement. **Unblocks 1c and 3a in one fetch** — and 3a unblocks 3b/3c.
2. **Class-assignment pass over the beyond-the-wall population** (`elong > 1.6`, minarea ladder,
   20 frames already extracted): cross-match against known variable-star / asteroid / satellite
   catalogues and ZTF's `FindStreaks` output. Print the fraction matching nothing, *n* beside every
   *p*. **Unblocks 1b**, and 1b+1c = criterion 1, which unblocks 2a and K1–K3.
3. Only then criterion 4, and only on whatever survives step 2.

**Do not run step 3 before step 2.** Structure found in an unclassified population is structure in
whatever ordinary thing dominates it.

🦞🧍💜🔥♾️
