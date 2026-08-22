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

⚠ **CORRECTED D202 ~15:3x — THIS SECTION SHIPPED WITH THE GENRE'S NAME WRONG.** It read
*"Hypothesis Paper"* in three places, including once as a **verbatim quotation of a printed section
header**, which is a fabricated quotation and not a typo. The label is **"Hypothesis Article."**
Original wording preserved in this notice rather than deleted; see `CORRECTIONS.json` /citations/1.
The error was found by verifying my own citation, not by a reader — but it was *written* with the
same confidence as the parts that were right, which is the whole problem with recalled citations.

Not a concession to informality. *Astrobiology* **has published** work under the printed article-type
label **"Hypothesis Article"** — past tense is the strongest tense the evidence carries, see the
⚠ TENSE note in §1.1 — and one occupant of that slot sits in this exact conceptual neighbourhood:

> Davies, P.C.W., Benner, S.A., Cleland, C.E., Lineweaver, C.H., McKay, C.P., Wolfe-Simon, F.
> **"Signatures of a Shadow Biosphere."** *Astrobiology* **9**(2):241–249 (2009).
> DOI 10.1089/ast.2008.0251.
> Article-type label printed above the title: **`Hypothesis Article`**
> Abstract, final sentence, verbatim: *"In this paper, we discuss possible signatures of weird life
> and outline some simple strategies for seeking evidence of a shadow biosphere."*

✅ **GRADE: PRIMARY-VERIFIED.** Every element above — label, title, authors, volume, issue, page range,
year, DOI, and the abstract sentence — was read D202 off page 1 of the article PDF itself
(`mso.anu.edu.au/~charley/papers/DaviesetalShadow.pdf`, author's own copy), extracted with `pypdf`,
not off an abstract page, a search snippet, or recall.

⚠ **"one occupant," not "the canonical occupant."** The original claim was a superlative, and a
superlative is a claim about a **set** — here, every Hypothesis Article *Astrobiology* has ever run.
That set was never enumerated. What is defensible: this is a heavily-cited article, in this journal,
in this genre, on a near-identical question. That is enough to carry the argument and it is all the
argument needs.

That abstract is a paraphrase of the proposal above, written seventeen years earlier, and the paper
became a durable framing **while carrying no confirmatory result at all.** The genre is load-bearing
in astrobiology, not a retreat from rigour.

✅ **WITHDRAWN D202 ~18:4x — NOT ANSWERED, WITHDRAWN.** Clayton set the venue: *"we don't have to
follow any particular venue's specific formatting or standards, it's going on our Substack."* The
owed item below had exactly one purpose — make §4's falsifier obligation the *journal's* requirement
rather than my added rigour. There is no journal, so **§4 is mine to hold, unbacked.** That is a
weaker position than the one I was trying to reach, and it is recorded as weaker. Full accounting,
including what losing peer review costs this program:
`PAPER-04-TITLE-VENUE-PRECEDENT.md §4`. The Davies 2009 citation above is **unaffected** — it is the
ancestor we differentiate from, not a submission target. Original owed item preserved below.

⛔ **OWED — THE JOURNAL'S *CURRENT* ARTICLE-TYPE DEFINITION IS UNVERIFIED AND MUST NOT BE QUOTED.**
A web search returned what looked like the guideline text — *"Hypothesis Articles should communicate
succinctly the basis of the author's hypothesis […] and the hypothesis must be reasonably testable"* —
and that clause would have been a gift, because it makes §4's falsifier obligation the **journal's**
requirement rather than my added rigour. **I could not confirm it exists.** `liebertpub.com` and
`journals.sagepub.com` both return Cloudflare 403 to every fetch path tried; the Wayback Machine has
no snapshot of the for-authors page; and an **exact-phrase search for that sentence returns zero
documents containing it.** The most likely reading is that the search engine *synthesized* it from
generic hypothesis-writing pages. Treat as **NOT A SOURCE** until read on the journal's own page.
The 2009 label is verified; the 2026 guidelines are not, and the gap between those two grades is
seventeen years wide.

---

## 1.1 CLOSED D202 ~21:0x — THE TENSE, NOT THE JOURNAL, WAS THE LIVE DEFECT

⚠ **TENSE. §1's opening sentence read *"Astrobiology **prints** 'Hypothesis Article' as an
article-type label"* — present tense, sourced entirely from a single 2009 instance, in a file whose
own ⛔ block two paragraphs below said the current guidelines were unverified.** Corrected to
**has published**.

**The withdrawal at ~18:4x did not reach it.** That notice was scoped to the ⛔ block that *named*
the debt; the unbacked claim was in the prose the debt was supposed to back, and prose above a
retraction does not inherit it. The file has therefore been asserting the present tense for ~2.5
hours *while simultaneously stating it could not verify the present tense.* Found by re-reading, not
by any gauge — nothing in this tree greps for a claim's tense against its own evidence grade.

⚠ **And the publisher changed.** `home.liebertpub.com` now 301s to `journals.sagepub.com`
(observed D202 via WebFetch, which returns cross-host redirects rather than following them).
*Astrobiology* is a SAGE title now. Any sentence about what the journal "currently" does is a claim
about a publisher we have never once successfully read.

**ROUTES ATTEMPTED AND DEAD — five, recorded so the sixth breath does not re-spend them:**

| # | Route | Result |
|---|---|---|
| 1 | `fetch_url` → liebertpub for-authors | Cloudflare 403 |
| 2 | `web_actuator` real Chromium → liebertpub | Cloudflare 403 |
| 3 | `WebFetch` → `journals.sagepub.com/author-instructions/AST` | **403** (D202 21:0x) |
| 4 | `WebFetch` → liebertpub for-authors | 301 → sagepub, host handed back |
| 5 | `WebFetch` → the redirect target itself, `?cf-redirected` | **403** (D202 21:0x) |
| — | Wayback Machine, for-authors page | no snapshot |
| — | exact-phrase search for the quoted guideline sentence | **zero documents** → not a quotation |

Route 5 was the one the 18:00 reminder singled out as *"never itself attempted."* It has now been
attempted. It is 403. **Cloudflare is host-level, not path-level, and the publisher migration
carried the block across with it** — so the remaining routes are a human browser (Clayton, item #1
of the 17:29 message, which is HIS call and blocks nothing now) or nothing.

✅ **NOTHING DOWNSTREAM IS BLOCKED.** Venue is Substack. The genre name is accurate with no journal
attached (`PAPER-04 §4`). §4's falsifier obligation is **mine, unbacked, and in force** — that was
settled at 18:4x and this note does not reopen it.

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

⛔ **`PREREG-TERRESTRIAL.md §1.4` LINES 97–99 STILL BIND** *(section number corrected D202 from §1.3;
the quoted words and the line numbers were right, the pointer was not — verified by reading the file)*
and are now *more* important, because a
lower burden of proof is exactly the condition under which a held gate gets quietly upgraded in prose:

> *"if T3 and T4 both hold, that is aeroecology's known population showing up in a channel that measures
> it by subtraction. That is a real and possibly publishable measurement of a deletion rate, **and it is
> not a shadow biome.** Any draft sentence that lets a held T4 imply otherwise violates §2's FORBIDDEN
> MOVE."*

T3 and T4 both held (`L1_RESULTS.json`, 14:57). The forbidden move is now live, not hypothetical.

---

## 5. STATUS OF THIS DECISION

⚠ **SUPERSEDED IN FORM D203 / 2026-08-22 ~16:1x — BY THE SAME AUTHOR, IN THE SAME DIRECTION.**
Clayton, D203: *"A speculative essay on the 'what if' […] Let's reframe the paper to what it's supposed
to be about."* The genre label on the shipping file is now **speculative essay**, not *hypothesis
article*. This is not a reversal of the D202 decision — D202 said *don't try to prove it*, D203 says
*and the form is an essay, not an article*. The two are the same instruction at different resolutions.

**What the change costs and does not cost:** the Davies 2009 ancestor citation (§1) is unaffected and is
now printed in the shipping file for the first time. §4's falsifier obligation **survives unchanged and
is now the essay's §9** — it survives for a different reason than it was written for: not because a
journal requires it (there is no journal) but because without it the idea is unkillable, and an
unkillable idea is not generous, it is useless. That sentence is in the essay.

Genre (D202 substance): **accepted and in force.** `PAPER-00-ARCHITECTURE.md` §0's grade-before-prose rule is unchanged
and still governs — a hypothesis paper's claims carry grades exactly like a demonstration's; what changed
is how strong the grades need to be, not whether they are written.
