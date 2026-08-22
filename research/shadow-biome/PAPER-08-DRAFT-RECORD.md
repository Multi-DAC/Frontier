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
