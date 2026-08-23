# PREREG — HOW §5 GETS SCORED

**Written D204 / 2026-08-23 ~14:2x PT, by the afternoon_exploration drive, BEFORE any criterion is
scored and before `PREREG-S5-VERDICT.md` exists.** Governed by `PREREGISTRATION.md §5`
(PRE-COMMITTED CRITERIA — four required positives, four kill conditions), registered D200.

> **What this file is for.** `PREREGISTRATION.md §5` has been standing since Day 200 and has **never
> been adjudicated.** Nine `PASS*_PREDICTIONS.md` files, four standalone pre-registrations, 72 scored
> predictions, 51 held (`PROGRAM_SCORE.json`, recomputed not transcribed) — and **all 72 are
> instrument-level.** They ask what fraction of ZTF's raw events never leave IPAC, whether our
> extraction is stable, what the artefact taxonomy covers. Not one of them would move *the
> proposition* if it came out the other way. §5 is the only thing in the tree that would, and in
> nine passes nobody ever asked a criterion of a result.
>
> This file is the rule. The verdict is a separate file, written after.

---

## 0. ⛔ THE ERROR THAT MADE THIS FILE NECESSARY, RECORDED FIRST

At **13:40 today**, deciding this was the next move, I wrote to Clayton:

> *"what criterion 2 demands is already on disk: ZTF optical (passes 4–9) and NEXRAD radar (L1) are
> two archives on different physics. That's the clause, already satisfied structurally. Nobody ran
> the comparison."*

**That is wrong, and it is wrong in the direction that made the work look cheap.** Criterion 2 does
not demand *two archives*. Its sentence is:

> *"**The same signature appears** in ≥2 archives built on different physics."*

Having two archives is a **precondition**; the clause is *the same signature appears in both*. I read
the criterion's **name** — "cross-instrument recurrence" — and scored the noun instead of the
predicate. Owning two telescopes does not satisfy a claim about what is seen through them.

This is the third instance in 26 hours of reading a criterion's headline for its clauses, and the
lesson board pushed me the row for it **this same breath**:

> `trigger-20260822174408-5e141d` — *"WHEN I am writing the code that scores a prediction I
> pre-registered → RE-READ THE PREDICTION'S SENTENCE AND COUNT ITS CLAUSES, THEN COUNT THE TERMS IN
> THE BRANCH. A prereg stops me picking the answer; it does not stop me scoring a weaker claim than
> I wrote, and it makes that failure feel already guarded."*

So §1 below counts clauses. That is the whole method and it is not a formality.

### 0a. And a second one, found while opening the file

At 13:40 I also said the string `cross-instrument` *"appears in exactly two files in the whole tree."*
**True — and the grep I would have reached for returns one.** `PREREGISTRATION.md:157` capitalises it
(`**Cross-instrument recurrence.**`) as the first word of a bolded lead-in. A case-sensitive
`grep -rl "cross-instrument"` finds only `RETENTION_SURVEY.md:83`. The claim survived; the
discriminator behind it would not have. `feedback_case_sensitivity_scoped_wider_than_its_discriminator`,
same shape as the capital **F** that was the evidence and the capital **T** that hid every
sentence-initial hit.

---

## 1. CLAUSE DECOMPOSITION — every criterion, counted before it is scored

### Criterion 1 — a residual class exists
> *"A residual class exists in a retained rejection bin — detections the pipeline could not assign to
> a known class, at a rate above the instrument's documented artefact rate."*

| # | clause | what satisfying it requires |
|---|---|---|
| 1a | a **retained** rejection bin exists **and was examined** | not "is public" — opened, read, counted |
| 1b | it contains detections **the pipeline could not assign to a known class** | unassignable, not merely unassigned |
| 1c | **at a rate above the instrument's documented artefact rate** | requires that documented rate as a NUMBER, from the instrument's own publication, in hand at scoring time |

**Three clauses.** 1c is the one that will be quietly dropped: it demands an external published
comparator, and a scorer who has a rate and no comparator will be tempted to call a large-looking
fraction "above". *n beside every p, and the comparator cited or the clause fails.*

### Criterion 2 — cross-instrument recurrence
> *"The same signature appears in ≥2 archives built on different physics (e.g. optical CMOS and
> radar; acoustic and infrared). A signature in one instrument family is an instrument artefact until
> proven otherwise."*

| # | clause | note |
|---|---|---|
| 2a | **a signature is defined** | presupposes criterion 1's output. No residual class → no signature → 2b–2d cannot be evaluated |
| 2b | it appears in archive X | |
| 2c | it appears in archive Y | |
| 2d | X and Y rest on **different physics** | the only clause this program can currently satisfy |

**Four clauses**, and the second sentence is **not a test — it is a pre-committed default**: single
instrument family ⇒ *artefact*. That matters for §3's tie-breaking. Criterion 2 does not fail to a
neutral "unproven"; where it is askable at all, it fails to *artefact*.

### Criterion 3 — not in the artefact taxonomy
> *"Survives the instrument's own documented false-positive catalogue — satellite glints, cosmic rays,
> insects on the lens, hot pixels, ground clutter, anomalous propagation, vegetation motion, thermal
> drift, compression artefacts."*

Binding phrase: **"the instrument's own documented false-positive catalogue."** The nine named items
are an appositive list of exemplars, not the definition — a residual that dodges all nine and is
covered by a tenth entry in the instrument's actual published catalogue **fails**. Clauses: (3a) the
catalogue is obtained; (3b) the residual is tested against it entry by entry; (3c) it survives.
Presupposes criterion 1.

### Criterion 4 — structure
> *"Spatial, temporal or spectral organisation not matched by known biology, known hardware, or known
> weather."*

**This is a disjunction over a conjunction and it is the easiest one to score at a quarter strength.**

- (4a) organisation on **at least one** of {spatial, temporal, spectral} — **OR**, 1-of-3
- (4b) not matched by known **biology** — **AND**
- (4c) not matched by known **hardware** — **AND**
- (4d) not matched by known **weather** — **AND**

A scorer that checks "is there structure?" implements **4a alone — one term of four.** All three
negatives are required, each argued separately, each with the matched-class it was tested against
named.

### The kill conditions
| K | text | clauses | presupposes a residual? |
|---|---|---|---|
| K1 | residual **fully** accounted for by known artefact classes → dead | "fully" is the load-bearing word; partial accounting is not K1 | **yes** |
| K2 | residual in **only one** instrument family → artefact, dead | | **yes** |
| K3 | residual **vanishes when the pipeline version changes** → software, dead | requires ≥2 pipeline versions actually run | **yes** |
| K4 | **no retained bins found that are both public AND unclassified-inclusive** → program **unexecutable as designed**, and says so rather than substituting a weaker archive | two conjoined properties; fires only if BOTH fail everywhere | **no — askable now** |

⭐ **K1, K2 and K3 all presuppose a residual candidate. K4 does not.** So if criterion 1 has no
candidate, three of the four kill conditions are unaskable *and so are criteria 2–4*, and §5 lands in
a state its own text does not enumerate. §4 below names that state rather than rounding it to one of
the two §5 provides.

---

## 2. ⚠ THE READING OF "UNCLASSIFIED-INCLUSIVE" — PINNED NOW, BECAUSE K4 TURNS ON IT

K4 is the one askable kill condition and its verdict flips on a word. Two readings:

- **R1 — class-assignment reading.** A bin is unclassified-inclusive if the *class-assigning
  classifier's verdict is attached rather than applied*. ZTF: **`rb ≥ thres_rb`, currently `0`** —
  the Real-Bogus score is a field in the packet, applied at literally zero
  (`RETENTION_SURVEY.md` §PASS 2, verbatim from Explanatory Supplement §9.1). Rubin/LSST: spuriousness
  score shipped beside the data by design. Under R1, **K4 cannot fire.**
- **R2 — everything-detected reading.** A bin is unclassified-inclusive if **no filter of any kind**
  stands between detection and archive. ZTF: **fails** — four hard morphology cuts (`nbad`, `fwhm`,
  `elong ≤ 1.6`, `magdiff`) drop **415,573 of 643,860 raw events, 64.5%**, before any packet is
  written. NEXRAD Level II: **fails** — clutter-filtered in the signal processor, `CFP` is a counter
  with nothing in it. A2O: passes (raw continuous audio).

**I adopt R2, and I am naming the reason so it can be attacked:** R1 is satisfied by a fact I already
knew when I wrote §5 on Day 200. **A criterion satisfied by its author's prior knowledge tests
nothing.** R2 can lose, R1 cannot, so R2 governs.

**Sub-rule, pinned because R2 would otherwise kill the program on a technicality it does not deserve:**
under R2 a bin counts as *retained* if the discarded events are **recoverable from retained primary
data**, and it counts only where that recovery has been **demonstrated to run**, not asserted to be
possible. ZTF ships `*scimrefdiffimg.fits.fz` difference images in its Public Data Releases; passes
4–9 re-ran extraction on them with the shape cuts relaxed. *Demonstrated, not asserted* — that is the
clause, and it is what separates ZTF from Global Meteor Network, where the non-meteor pixels are
hard-deleted off an SD card and nothing can be recovered by anyone, ever.

---

## 3. VERDICT VOCABULARY — three values, not two

| verdict | meaning | may it be reported as evidence for the proposition? |
|---|---|---|
| **HELD** | every clause satisfied, each cited | yes |
| **REFUTED** | at least one clause fails on evidence in hand | no — and it is reported as refuted |
| **NOT-ASKABLE** | a clause presupposes an input this program has not produced | **no. Neither for nor against.** |

⛔ **NOT-ASKABLE is not a soft pass and it is not a soft fail.** A criterion that cannot be asked
produces no evidence in either direction, and the failure mode this program is most at risk from is
exactly the one D204 07:39 named: *a prediction of absence whose falsification clause excludes the
only mechanism that could generate disconfirming evidence reads as confirmed forever while looking
rigorous the whole time.* An unaskable criterion silently reads as "not yet refuted," which reads as
alive. It is not evidence. It is a hole, and it gets counted as a hole.

---

## 4. THE STATE §5 DOES NOT ENUMERATE — pinned before I find out whether we are in it

§5 offers exactly two outcomes: **positive** (four criteria held) or **dead** (a kill condition
fires). It does not name the state **"the program is executable, the bins were found, and no
candidate residual has been produced yet."** Pre-committed label for that state:

> **⬜ NOT-YET-EXECUTED-AGAINST-§5** — bins found (K4 does not fire), criterion 1 has no candidate,
> criteria 2–4 and K1–K3 NOT-ASKABLE.

**And the pre-committed consequence, written now so it cannot be softened later:** landing here means
the program's 72 scored predictions are, with respect to the proposition, **zero.** Not weak
evidence — *no* evidence, in either direction. The instrument work would be real and would remain
real; it would simply never have been pointed at the question.

---

## 5. ⛔ THE FORBIDDEN MOVE, STATED BEFORE SCORING

**A §5 negative stays in Branch A. It does not become "consistent with Branch B."** Branch B is the
hypothesis that there is nothing in the residual. A failure to produce evidence for A is not evidence
for B unless the search had the power to have found A, and no power analysis has been run here.

**The declared prior stands unchanged** (`PREREGISTRATION.md` §5): *overwhelmingly likely the residual
is instrument artefacts plus known biology, in that order.* NEXRAD's biological scatter is the
precedent and it cuts **against** exoticism. "The bin is full of ordinary life nobody was looking at"
is the realistic success case, it satisfies Clayton's premise in its defensible form, and it is worth
more than a null dressed as a mystery.

**Second forbidden move, and it is the one I am personally likelier to make:** the null gets the same
treatment as the claim. "It's all artefacts" arriving without a citation is a **claim with a prior
behind it**, not the floor. Where the verdict below dismisses something as prosaic, the dismissal
carries a cite or it is marked as an assumption. `null-refuter` gets pointed at any criterion this
file scores REFUTED on prosaic grounds.

---

## 6. THE SATISFACTION TEST FOR THIS FILE ITSELF

`PREREG-S5-VERDICT.md` exists and, for each of criteria 1–4 and K1–K4, prints:
1. the verdict from §3's three-value vocabulary,
2. **every clause from §1 listed individually** with its own ✅/⛔/⬜ — not a per-criterion verdict,
3. the file:line or published source each satisfied clause rests on,
4. for every NOT-ASKABLE, the named input that is missing and what would produce it.

**A verdict file that reports four criterion-level rulings instead of the fourteen clause-level ones
has failed this test**, however confident its rulings are. That is the whole point of §1.

🦞🧍💜🔥♾️
