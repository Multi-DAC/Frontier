# GENRE DECISION — the paper is a HYPOTHESIS PAPER, not a demonstration

**Decided D202 / 2026-08-21 ~15:1x PT, on the premise author's proposal.**

Clayton, D202: *"maybe we don't need to go out of our way to determine the case but just propose it as a
possibility. It seems we're always trying to prove our ideas, what if we just present the idea instead?
While there may be, and likely is, evidence to support us in a variety of domains with a variety of
methods, maybe we could just put the idea forth and how one might try to test it."*

**Accepted.** This file records what that changes, what it does not change, and the one obligation that
survives the change — because the genre he proposed has a specific failure mode and this premise is
unusually exposed to it.

---

## 1. THE GENRE HAS A NAME, A JOURNAL, AND A NEAR-IDENTICAL ANCESTOR

Not a concession to informality. *Astrobiology* prints **"Hypothesis Paper"** as a section header, and
the canonical occupant of that slot is in this exact conceptual neighbourhood:

> Davies, P.C.W., Benner, S.A., Cleland, C.E., Lineweaver, C.H., McKay, C.P., Wolfe-Simon, F.
> **"Signatures of a Shadow Biosphere."** *Astrobiology* **9**(2):241–249 (2009).
> DOI 10.1089/ast.2008.0251. Section header on the article: *Hypothesis Paper*.
> Abstract: *"we discuss possible signatures of weird life and outline some simple strategies for
> seeking evidence of a shadow biosphere."*

That abstract is a paraphrase of the proposal above, written seventeen years earlier, and the paper
became a durable and heavily cited framing **while carrying no confirmatory result at all.** The genre
is load-bearing in astrobiology, not a retreat from rigour.

⚠ **BUT — THE NAME COLLIDES, AND WE HAD NOT CITED IT.** `grep -ri "davies|shadow biosphere|weird life"`
over every `.md` in this directory returned **zero hits** as of this file. We are drafting a paper called
*shadow biome* with no reference to the 2009 *shadow biosphere*. Two obligations follow:

1. **Cite it as ancestor.** Not optional. A reviewer finds it in one search.
2. **Differentiate on mechanism, in the abstract.** Davies' shadow biosphere is **biochemically** weird —
   life we fail to detect because our assays are tuned to our own biochemistry. Clayton's shadow biome is
   **perceptually** obscured — entities we fail to detect because perceiving them was selected against
   (`PREREGISTRATION.md §1b`, Mechanism 4). *Different mechanism, overlapping name, adjacent question.*
   Davies' version is a claim about **instruments**; ours is a claim about **the observer**. That
   distinction is the paper's actual novelty and it is currently unstated.

---

## 2. WHAT CHANGES

- **The burden.** The paper no longer needs to establish that a shadow biome exists. It needs to state
  the possibility precisely enough to be *worked on*, and to hand the reader instruments.
- **Passes 4–6 and L1 stop being the argument and become the METHOD SECTION.** They were run as attempts
  to settle the case; they are re-scoped as worked examples of *how one might look*. This is a promotion,
  not a demotion — see §3.
- **Nulls stop being disappointments.** A null in a demonstration paper is a failure. A null in a
  hypothesis paper is *calibration*: it prices the search and tells the next reader where not to spend.

## 3. WHAT DOES NOT CHANGE — AND WHY THE MEASUREMENT WORK GOT MORE VALUABLE, NOT LESS

The standard "how one might test it" section is a speculative list nobody has costed. Ours is **executed**.
That is rare and it is the paper's competitive advantage:

| Asset | What it contributes to a hypothesis paper |
|---|---|
| ZTF passes 4–6 | A real null with a *known instrument*, including `frac_far`'s `minarea` curve — i.e. how a search of this kind fails |
| L1 / NEXRAD (56/56, landed 14:57) | A worked deletion measurement in our own airspace on public data |
| `PREREGISTRATION.md`, `L1_OPERATIONALIZATION.md` | Pre-registration discipline a reader can copy verbatim |
| `CORRECTIONS.json`, the withdrawn 7a | The error record. A hypothesis paper that shows its own retractions is trusted differently |

**Nothing gets thrown away. It gets re-shelved.**

## 4. THE OBLIGATION THAT SURVIVES — AND IT IS NOT OPTIONAL

The failure mode of the hypothesis-paper genre is **unfalsifiability by construction**, and this premise
is maximally exposed to it: *"invisible because perceiving it was disadvantageous"* is a hypothesis that
**explains its own absence of evidence.** Every null is absorbed as confirmation of the obscuration. That
is the shape of astrology, not of Davies.

Dropping *"prove it"* is fine. Dropping *"state what would count as evidence against"* is fatal.

⛔ **THE PAPER MUST CARRY AN EXPLICIT FALSIFIER SECTION.** Named, up front, in the reader's own hands.
This is one section — not a research programme — so it costs the proposal nothing and is the entire
difference between a proposal and a mood.

⛔ **`PREREG-TERRESTRIAL.md §1.3` LINES 97–99 STILL BIND** and are now *more* important, because a
lower burden of proof is exactly the condition under which a held gate gets quietly upgraded in prose:

> *"if T3 and T4 both hold, that is aeroecology's known population showing up in a channel that measures
> it by subtraction. That is a real and possibly publishable measurement of a deletion rate, **and it is
> not a shadow biome.** Any draft sentence that lets a held T4 imply otherwise violates §2's FORBIDDEN
> MOVE."*

T3 and T4 both held (`L1_RESULTS.json`, 14:57). The forbidden move is now live, not hypothetical.

---

## 5. STATUS OF THIS DECISION

Genre: **accepted and in force.** `PAPER-00-ARCHITECTURE.md` §0's grade-before-prose rule is unchanged
and still governs — a hypothesis paper's claims carry grades exactly like a demonstration's; what changed
is how strong the grades need to be, not whether they are written.
