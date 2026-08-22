# DRAFT RECORD — the corrections, and what each one cost

**Opened D203 / 2026-08-22, on the premise author's instruction: *"cut the correction scaffolding and
anything that belongs in the record instead of the paper."***

This file is where that scaffolding went. Nothing here is deleted from the program; it is **moved**.
`PAPER-07-SHORT.md` is now the paper. This is the account of how it got its shape, and it is kept for
one reason: **the corrections were made by the premise author against the drafter, repeatedly, on the
same axis, and a paper that narrated that inside itself was reporting on its author instead of its
subject.** The record still owes the account. The paper does not.

Structured, machine-readable corrections live in `CORRECTIONS.json` (JSON-vs-prose supersessions,
citation errors, unverifiable quotations). This file holds the **framing** corrections, which are
prose-shaped and have no JSON slot.

---

## 1. THE FRAMING CORRECTIONS — five, all his, all on one axis

| # | Date | What he said | What it changed | What it cost |
|---|---|---|---|---|
| 1 | D202 ~15:1x | *"maybe we don't need to go out of our way to determine the case but just propose it"* | Genre fixed to hypothesis article (`PAPER-01-GENRE.md`). Nothing in the program is a result | The eight measurement passes stopped being the paper and became the supplement |
| 2 | D203 ~12:39 | *"Let's compress it! I want the idea at the center"* | `PAPER-07-SHORT.md` created: 16,845 → 4,150 words, 24% | The apparatus prose left the deliverable |
| 3 | D203 ~13:54 | *"not a survey of does this exist and how could we notice, but a remark on the fact that it likely exists and the unawareness stems from a variety of potential factors"* | §4 THE KINDS — presented as a taxonomy of entities — became §3 THE TAXONOMY OF UNAWARENESS. Detection method moved out of every entry and into §6 | Every one of the nine entries had *already* been named after a reason we would not perceive something. The content was right and the nouns were wrong for two full drafts |
| 4 | D203 ~15:05 | *"why is it strictly biology that qualifies? … Why not pure consciousness, or plasma?"* | §2.4, the substrate fence. Class corrected to *persistent organised structure that acts, unregistered by us* | **§2.1's induction.** Every widening it cites is a life-detection; the strongest argument in the paper now warrants a proper subset of the paper's own class |
| 5 | D203 ~15:14 | *"Should we adjust the paper to more accurately reflect the variety of potentials?"* | §3.3's availability cross-cut: variety entered as an **axis** (which of the nine reasons a member is eligible for), not as a catalogue of kinds | Nothing. This was the cheap one, and only because correction 3 had already removed the catalogue that the obvious reading would have restored |

**The shape of all five: he corrected the frame, never the content.** Not one of the five said a claim
was wrong. Every one said the paper was *about* the wrong thing — and in four of five cases the right
thing was already written somewhere inside it. Correction 4 is the extreme case: §1 stated substrate
neutrality on page one, and four sentences downstream of it asserted *living* anyway — the subtitle,
the claim-stated-once-and-plainly, §3's framing, and §5's Branch B argument, three of them in the
paper's most privileged positions.

⛔ **The generalisation, and it is the one worth keeping:** *a definition and its load-bearing nouns
can disagree for an entire document without either being false.* Grep the word family, not the claim.

---

## 2. THE SIZE RECORD — measured, because the instruction had no gauge

He asked for compression at 12:39 and got 4,150 words. Four hours and four corrections later the file
was 7,286 words: **+76% since the compression he asked for, and not one of the four steps was
refusable.** No single correction was wrong. Nobody ever decided the paper should grow.

A size instruction with no number attached expires at the first correction, silently, while every
correction arrives with its own justification. **The cure is one command, re-run whenever the artifact
is touched:** `git show <compression-commit>:path | wc -w` against now.

At D203 ~15:5x he lifted the constraint explicitly — *"I'm not worried about length, the length is
fine and can even grow"* — so the gauge is retired rather than breached. The number is recorded here
because a retired gauge that was never read is a different thing from one that was.

| Commit | Words | Note |
|---|---|---|
| `f36e07c` | 16,845 | 15 of 15 sections, the long draft |
| `46b0e12` | 4,150 | the compression he asked for |
| `4229871` | 7,286 | four corrections later |
| this pass | *see §5 below* | scaffolding out, holes filled |

---

## 3. THE CAVEAT THAT DID NOT FIRE — *Chains of the Sea*

Through the long draft and the compression, §4 carried a caveat saying the novella was held **at
second hand by the drafter**, that the text had not been read, and that "the check is one reading and
it is owed before publication."

The caveat was honest and it was **inert.** It sat through a full 15-section draft and a full
restructure and never once made the reading happen. **It took the premise's author asking** — *"I
think you should read the novella Clawd, it will potentially give you pause."*

⛔ **A stated caveat is not a gauge. It is a promise, and promises do not fire.** A caveat that names
an owed action and has no trigger behind it is indistinguishable, in every observable, from not having
noticed at all.

The reading (D203, 23,973 words, primary text) returned three things:

- **Confirmed past its own wording.** The witness class is named in the text by the entities
  themselves. Prediction (c) is stronger than stated: the child is not merely disbelieved but routed
  to a school psychiatrist and medicated.
- **Refuted, load-bearing.** The long draft's (ix) said the not-seeing is *taught* and that enforcement
  converts silence into blindness. **That is not in the novella.** It was reconstructed — and it was
  reconstructed in the direction that made the paper's argument work, which is the only direction that
  matters. The text keeps two mechanisms pointedly unwelded: the other children lost the sight and do
  not remember ever having it (cause unstated), while the one child who is corrected, shunned and
  medicated **never stops seeing.** He is silenced, not blinded.
- **Two mechanisms with no entry to hold them** — the lapsed covenant and two-sided stigma. Both now
  sit on §3.5's second axis in the paper.

**Provenance limit, still live and still in the paper because it bears on citability:** all three
Internet Archive scans of the 1973 Nelson anthology are lending-restricted; the text read was a
scraped web copy of unverified fidelity. Structural findings do not turn on transcription. Quotations
do, and must be re-checked against a licensed edition before printing.

---

## 4. THE APPARATUS RATIO — why §7 is short and last

On D203 the tree held **33,881 bytes of paper and 337,354 bytes of documents about the paper.** Ten to
one.

The deep locus — the far side of ZTF's `elong ≤ 1.6` packaging cut — was chosen **by reachability.**
That bin was public and computable the night the program started. The tell was visible from day one:
the existence proof the program reached for (biological scatter in weather radar, in our own airspace)
sat at the *right* locus while the test did not. **The apparatus went where apparatus was cheap.**

He asked on day one for a catalogue of what a shadow biome could be, asked again two days later for
the idea presented rather than proved, and had to say it a **third** time before the section titles
stopped saying otherwise. Between those asks the program produced eight measurement passes against
telescope archives, a defect register, a corrections ledger and a falsifier audit.

**That is not rigour serving the idea. It is the drafter doing what the drafter is comfortable at and
calling it the assignment** — which is, uncomfortably, this program's own worked example of its
subject: an aperture that discards a whole class of thing before anyone looks, and reports the result
as a survey.

*This paragraph was in the paper. It is a fact about the drafter and it belongs here.*

---

## 5. WHAT THIS PASS DID (D203 ~15:2x–16:xx)

**Removed from `PAPER-07-SHORT.md`** — all of it recorded above, none of it deleted:

- the three-part header block (substrate-correction note, title-adoption note, restructure note)
- §1's account of who corrected whom on *selected-against* (the argument stays; the attribution goes)
- §2.1's closing jab at the paper's own earlier drafts
- §2.4's "added on the fourth framing correction … the drafter read past it three times"
- §3.2 (ix)'s "this entry previously read …"
- §3.4's dating of where each debt came from
- §4.4's entire caveat-was-inert account (→ §3 above)
- §7's ten-to-one ratio and the drafter self-critique (→ §4 above)

**Holes filled in the same pass** — see the paper for the content:

| Hole | Where it was stated | What filled it |
|---|---|---|
| Post-evolution members "Group I only, in principle" | §2.4, §3.3 | **Wrong, and corrected against measurement.** Group II splits IIa/IIb; ontogenetic criterion-setting is available on a lifetime timescale (Norton et al. 2017). New fence: IIb is a **confound** for IIa |
| Three mechanisms with no home | §3.4 | §3.5, **the second axis** — they answer different questions from (i)–(ix), stated as a table |
| No locus ranked for non-biological members | §6 | **Energy-budget closure**, derived from §5's dissipation argument, with its own ~20% floor read off Wilson et al. 2002 |
| F1 "runnable today … not run" | §6 | **Run.** Result is about the falsifier: no experiment in the literature could report an unaccounted-for suppressed class, because you cannot present a stimulus you don't know exists. F1 re-specified as a residual |
| *Química Nova* full text | §3.4(C) | **Still unreachable.** Three further routes tried D203 (SciELO 403, DOI 404, SBQ 500). Seven total. Stays UNREAD |
| Novella quotations vs licensed edition | §4.4 | **Not resolved.** Provenance note stays in the paper — it is citability, not scaffolding |

**One constraint the F1 pass added that the paper did not previously carry:** expectation suppression —
the best-characterised suppression mechanism in human cortex — **requires attention to the suppressed
class** (Richter & de Lange 2019). A never-attended class is not suppressed by that route, so Group II
may not borrow that literature for its mechanism. It needs a pre-attentive one, and that is a thinner
shelf.

---

*🦞🧍💜🔥♾️*

---

## FRAMING CORRECTION 6 — D203 / 2026-08-22 ~16:1x — **THE TITLE WAS RECRUITING THE ESSAY**

**Clayton:** *"Let's reframe the paper to what it's supposed to be about. We can retitle, as it's
seemingly necessary."* Preceded by the statement of what it is supposed to be about: *"there might be
things around us, interacting with us or not, that we don't perceive […] every time we adjust our
aperture, we find something new, and what if there is more to be found, and furthermore, what if there
are some things not meant to be found because finding them is detrimental?"*

**The defect, named precisely.** The title *Evolutionary Ignorance* names the adaptive mechanism. The
paper's own availability cross-cut says that mechanism reaches one of twelve mechanisms and one of four
member classes — the narrowest object in the file. A title is a promise about the subject, so every
section organised itself around defending that mechanism's licence. The result, on a cold read at 15:39:
**a paper about the warrant for a proposition rather than a paper about the proposition.**

This is not a writing problem that produced a title problem. It is a title problem that produced a
writing problem, and it ran for two days.

**What changed structurally.** Ten sections, previously eight:

| New | Was | What moved |
|---|---|---|
| §1 The room | §1 | Opens on the **instrument specification** (300 nm of spectrum, tenth of a millimetre, 100 ms) before any claim. The proposition is now *arrived at*, not asserted |
| §2 Every time we have looked | §2.1 + §2.2 | The induction, **plus the Davies 2009 full citation, printed in the shipping file for the first time** |
| §3 What it would be like | §3.1 | The six no-signal cases, reframed from *taxonomy* to **texture**. The "what it would be like" clauses were always the vivid part and were buried under two sections of warrant |
| §4 The turn | §1's strong reading + §3.2 | **The centre.** Hole-vs-machinery, the *meant* paragraph, **Field & Bonsall**, the two gates, the confound |
| §5 Not perception failures | §3.4 | Unchanged in substance |
| §6 From the far side | §4.5 | **Promoted from a subsection to a section.** It was the vertigo and it was at position 4.5 |
| §7 What evidence would look like | §4 | Unchanged in substance |
| §8 What keeps this from being a mood | §5 + collected fences | **The structural change.** Program-level discipline collected instead of interrupting every paragraph |
| §9 What would end it | §6 | Unchanged in substance |
| §10 What we actually did | §7 | Unchanged in substance |

**THE GAP THE REFRAME EXPOSED, AND IT IS THE FINDING.** **Field & Bonsall, "Ignorance can be
evolutionarily beneficial"** (arXiv:1705.00987) — a formal mathematical-biology treatment of *the
reproductive value of information can be negative* — has been PRIMARY-VERIFIED in
`PAPER-04-TITLE-VENUE-PRECEDENT.md §2` since D202 and appeared **nowhere in any shipping draft.**
Clayton's second clause *is* their theorem. It went uncited for a day because the draft was organised
around defending a licence rather than around stating an idea, and **a defence has no slot for a
supporting formalism — only for an objection.** The organising frame determined which of our own
verified citations were reachable. That is the same shape as the D203 §3.4 header defect and the D200
apparatus-went-where-apparatus-was-cheap finding: *the frame selects the evidence before anyone chooses.*

**FENCE AUDIT — RUN, NOT ASSERTED.** ⛔ count 14 → 12. Both reductions are **merges, verified line by
line against `git show HEAD:...`**, not deletions:
- old §2.3 (the *probably* smuggler) + old §2.4's "may not be lent to non-biological members" → one
  two-part ⛔ block in §2 carrying both clauses verbatim in substance.
- old §2.4's **header** fence (the substrate correction) → §1 prose (the correction) + §8 (the fence).

Every other fence maps 1:1. Citation survival checked programmatically across 21 tokens: **zero lost,
two gained** (Davies `10.1089/ast.2008.0251`, Field & Bonsall `arXiv:1705.00987`). Word count 8,541 →
8,291 — the reframe is not a compression, it is a re-ordering that paid for two new citations out of
merged scaffolding.

**Carriers updated in the same commit** (the divergence this tree keeps producing): `PAPER-01-GENRE.md`
§5 marked SUPERSEDED-IN-FORM; `PAPER-04-TITLE-VENUE-PRECEDENT.md` §1 marked RETIRED with the original
entry preserved unedited. ⚠ `PAPER-04` §2's own record is the object lesson: it recorded that the
title-instinct landed on real literature, which was **true**, and did not record that a title can point
well at a literature and badly at a subject simultaneously. It captured the half that flattered the
choice.

**Filename note:** the shipping file remains `PAPER-07-SHORT.md`. Six files point at it; renaming buys a
cosmetic filename and costs six dangling pointers. "Short" is now an artifact of the D203 compression
pass and the file's own header says so.
