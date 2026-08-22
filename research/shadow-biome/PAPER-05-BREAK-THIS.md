# BREAK THIS — the adversarial reader's packet

*Written D202 / 2026-08-21, after Clayton offered to hand the paper to a human and ask them to break
it. This file exists so that offer costs the human an hour instead of a week.*

⚠ **THE TARGET MOVED D203 ~12:5x AND THIS PACKET HAS NOT BEEN RE-AIMED.** On the premise author's
instruction — *"I want the idea at the center"* — **the paper is now `PAPER-07-SHORT.md`, 8 sections,
~4,100 words**, and `PAPER-03-DRAFT.md` is demoted to supplement. Every attack below was written
against the long draft. **Most of them still land** (the fences, the fork, the pass results are
carried over verbatim or near-verbatim), **but the roster line beneath is stale by construction and a
reader must not take it as the paper's shape.** The one genuinely new attack surface is §2, the
witness asymmetry, and it is the most attackable thing in either file: it argues that the expected
evidence is a distribution of exceptions, which is one inch from the move F5 exists to forbid.
Re-aim this packet before it leaves the house.

*Status, re-measured **D203 / 2026-08-22 ~11:4x** by `wc -w` and `grep -o "^## §"` on the SUPPLEMENT
(then the paper): `PAPER-03-DRAFT.md`, **16,845 words**, **15 headings — §1 §2 §3 §4 §5 §6 §7 §8
§9 §10 §11 §12 §13 §14 §15. There are no gaps. The draft is complete.***

*⭐ **AND THE THREE SECTIONS ADDED SINCE THIS FILE WAS LAST MEASURED ARE THE THREE MOST WORTH
ATTACKING, BECAUSE EACH REPORTS A REFUTATION OF OUR OWN CLAIM AND A READER SHOULD CHECK WHETHER WE
CONCEDED HONESTLY OR CONVENIENTLY:***

- ***§12 withdraws its own headline.** 5.76% of alerts stranded on one night; the pre-registered
  second night returned **zero of 32 exposures missing**, refuting R1 and R2. Attack: is the
  retraction complete, or does "episodic, not a rate" smuggle the finding back in?
  `PREREG-REACHABILITY.md` was committed (`312a883`) before the night-2 tarball was opened.*
- ***§14's signal is under its floor.** 2.34 nGal against published post-correction residuals of
  17–4,000 nGal — **7× to 1,712× below**. Attack: the ~2.6 kg inversion is the only surviving claim,
  and it rests on quoting one station's best narrowband residual as though a real search could
  operate there.*
- ***§15 rejects its own pre-registered corpus after gate C5 passed it.** Attack: we say a name
  collision caused it and that nothing in the pre-registration failed. A hostile reader should ask
  whether "the object was inadmissible" is a genuine category finding or a retreat from a corpus
  that was about to refute C1.*

*⚠ **The citation debt recorded below was measured against the 12-section draft and has NOT been
re-run over §12, §14 or §15.** §14 carries two literature citations (Crossley et al. 2023 GJI 232;
Antokoletz et al. 2024 GJI 236) **fetched from the publishers this morning and transcribed once**.
No reading pass has seen them. Treat them as UNVERIFIED.*

**Attack what is claimed.** ✅ **Citation debt: ZERO real markers** (the one `grep` hit is the legend that defines the
convention); the D202 reading pass closed all eleven — four survived at source, five were amended
against it, one claim died, one is carried as `[⚠ SECONDARY]`.*

*⭐ **§10 IS NEW AND IT IS THE SECTION TO ATTACK FIRST.** It is the program's own scoreboard —
51 of 72 pre-committed predictions held — and it publishes the number that most threatens the
paper's method claim: **the hit-rate jumps from 54.5 % to 84.6 % exactly when the questions stopped
being about ZTF and started being about our own code.** §10 refuses to pick between "we got better
calibrated" and "we started asking ourselves easier questions." **If you can show which one it is,
in either direction, that is the highest-value hit available in this packet** — including against us,
because the second reading discounts everything passes 7–9 established.*

*⚠ Also inside §10 and worth a breaker's time: three defects it found **in our own record**, not in
the sky — a headline from one pass being carried as the program's, a pre-registered prediction (L1's
T5) adjudicated in prose but emitted by no code, and nine prediction labels reused across passes of
which five disagree with themselves. Those are conceded in the section. The attackable question is
whether a scoreboard that needed a script to find three errors in itself should be believed about the
other sixty-nine rows.*

*⚠ **The second most attackable item is pass 9's 11-of-11 with three boundary passes** — see "known
weaknesses" below, item 5.*

*⭐ **§9 remains the instrument section and is the third target.** It contains the largest number in
the program (a 0.10632 span on a threshold we chose), and it reports that our own published catalogue
is not reproducible from our own published code. If §9 is wrong in our favour anywhere, the paper's
central claim about its own discipline is wrong.*

*⚠ This line read "5,123 words, §1 §2 §3 §4 §5 §13 · §6–§12 are not written" for four hours, across
§6 being drafted (`4e6dc99`) and the reading pass adding ~1,300 words (`72e6ba7`). **This is the one
file in this directory that leaves the house**, so a stale roster here does not cost me a wrong note —
it costs the human breaker an hour spent looking for a section that is sitting in front of them. Any
future edit to the draft must re-measure this line by counting the draft's headings, not recall it.*

---

## 0. WHY A PACKET AND NOT JUST "HERE, READ IT"

Hand a person 5,000 words and they will attack the prose, because prose is what is in front of them.
They will find hedges, tone, one overreaching adjective. All true, all cheap, none of it load-bearing.

An adversarial reader is a **scarce, decorrelated instrument.** Their value is not diligence — I have
diligence, and I have spent two days refuting my own claims with it. Their value is that their priors
are not mine. That resource is wasted on line-editing.

So this file does one thing: it names **what the paper is actually standing on**, ranked by how much
dies if it falls, and states in advance **what counts as a hit.** Aim there.

⚠ **And the reason this cannot be an internal job.** Ten-plus of this program's findings died today,
every one of them killed by me. That sounds like the system works. It also means every refutation so
far shares a single set of priors, a single reading of the premise, and a single sense of what is
obviously fine. A body does not certify its own condition. **The failure modes I cannot see are
exactly the ones a same-priors refuter also cannot see.**

---

## 1. RULES OF ENGAGEMENT — what counts as a hit

| | Counts | Does not count |
|---|---|---|
| **1** | "This claim is false, and here is the case" | "This claim is unproven" — the paper is a hypothesis article and says so |
| **2** | "This falsifier cannot fail" — a named test that no possible result would kill | "This falsifier is expensive/won't be run" — true, and stated in §3 |
| **3** | "These two sentences cannot both be true" | ⚠ **"This section is thin" — the "unwritten by design" escape hatch is GONE as of D203. No section is unwritten. Thinness is a fair attack everywhere** |
| **4** | "You already conceded X, and Y assumes not-X" | Tone, hedging, adjectives, length |
| **5** | "This literature already settled it, cite" | "Someone has probably thought about this" |

**The single most valuable finding you could return is #2.** A falsifier that cannot fail is a
decoration, and a paper whose falsifiability is decorative is worse than one that makes no claim to it.

---

## 2. THE LOAD-BEARING CLAIMS, RANKED BY BLAST RADIUS

### ★ C1 — The decomposition (`PAPER-02-FALSIFIERS.md` §1). **If this falls, everything falls.**

The premise is split into **(A)** the entities exist — conceded self-sealing, deliberately not
defended — and **(B)** human non-perception of them is *evolved and selected-for*. The paper's entire
claim to testability rests on (B) being a claim **about human sensory architecture**, testable on
human subjects and human tissue, **with no access to the entities required.**

**Attack it here:** is (B) genuinely separable from (A)? Every falsifier F1–F3 tests (B). If you can
show that any of them covertly requires knowing what *C* is — that "candidate channel *C*" cannot be
specified without already assuming the biome — the separation is fictional and the paper's
falsifiability collapses back into (A)'s self-sealing.

---

### ★ C2 — The anti-rescue paragraph (`PAPER-02-FALSIFIERS.md` F3). **The document calls this its single load-bearing sentence.**

F3 predicts a perceiving tail: an active gate is regulated, regulated things vary, so a
subpopulation should perform above chance on a detector-anchored forced-choice task. The paragraph
then forbids, in advance, the rescue "the blindness went to fixation" — on the grounds that fixation
is a strictly stronger claim than the premise licenses.

**Attack it here, two ways.**

1. **The forbidding has no mechanism.** It is a promise made by the same authors who would want the
   rescue. Nothing structural prevents a later paper from making the fixation claim; the clause is a
   norm, not a gate. *(This is my own candidate objection, and it is the signature defect of
   everything I build: a correct rule with nothing that fires it.)*
2. **Is fixation actually stronger?** If it is not — if the premise as stated already licenses
   fixation — then the anti-rescue clause forbids nothing and F3 is absorbable after all.

---

### ★ C3 — What (B) costs, and whether the paper pays it. **My best guess at the fatal one.**

This is the objection I would lead with if I were breaking it, and I am flagging that the paper
addresses its neighbour but not, as far as I can find, this exact form.

*Selected against* — the strong, falsifiable half — requires that perceiving *C* had **fitness
consequences for ancestral hominins.** Selection is not free-floating: something must have cost
lives. So (B) commits the paper to a biome that was **ecologically consequential to our ancestors** —
present, engaged-with, mattering.

But the premise's intuitive appeal runs the other way: things *"too small, too big, on different
timescales, invisible, inaudible… lacking interaction."* The more thoroughly obscured the biome, the
less it could have exerted selection; the more it exerted selection, the less it can be described as
outside our world. **The two halves of the paper's appeal may be pulling in opposite directions.**

**What is already there, so you do not re-derive it:** F2 requires the blindness be *derived, not
ancestral*, and phrases the pressure as costly "**to us**" — adjacent, and it constrains the same
thing from the phylogenetic side. §13 item 5 and F4 close the *physics* of non-interaction (life is
dissipative; anything alive must couple to something). **Neither states this as a price (B) pays.**

**Attack it here:** is this a real contradiction or a resolvable tension? A working resolution exists
in principle — the bat/moth case, which §1.2 already leans on: an interaction ongoing in rooms humans
stood in for millennia, ecologically enormous, and imperceptible to us. If that generalises, C3
dissolves. If it does not, say why.

---

### C4 — F1's own conceded weakness

F1 predicts transduction + central gating + gating **specific to *C***. The document already states,
unprompted, that condition (3) is the whole test and that **without a specificity criterion pinned
before looking, F1 confirms on any nervous system.**

**Attack it here:** we conceded the weakness. Did we *repair* it, or did we conceded-and-continue? If
no specificity criterion is ever pinned anywhere in the corpus, F1 is a decoration that the paper has
politely labelled as one and then kept. That is a #2 hit under the rules above.

---

### C5 — §2, observer-relative kinds

The paper argues that "things humans can't perceive" is a legitimate scientific kind and not an
anthropocentric artefact. If this fails, the object of study is incoherent and no amount of falsifier
machinery saves it.

**Attack it here:** the standard objection is that the category has no natural joints — it is a
union over unrelated physics selected purely by a fact about primate sensoria. §2 answers this;
decide whether the answer works.

---

### C6 — The genre move

`PAPER-01-GENRE.md` classes the paper as a hypothesis article, and §3 defends writing the fork
*before* the data. The obvious attack — "you have pre-registered tests you will never run" — is
**anticipated and conceded in §3**, so it is not a fresh hit on its own. The fresh version is
sharper: *does the pre-registration do any work if no member of it is inside the authors' budget?*
L2 (camera-trap blanks, `PREREG-TERRESTRIAL.md` §2) is the one locus we could actually run. If you
think L2 is also unrunnable or uninformative, that is a real finding.

---

## 3. ALREADY DEAD — do not spend time here

Twelve-plus defects are logged in `DEFECT_REGISTER.json` with citations, and corrections in
`CORRECTIONS.json`. The ones a fresh reader is most likely to re-find:

- **§7a is withdrawn.** It was written against a transcription error ("cameras are the only thing"
  → the author meant "AREN'T"). The verbatim record is kept deliberately; the section built on it is
  gone.
- **"Not selected against, merely not selected for" is the *superseded* framing.** It appears in the
  draft at §1.1 as the correction's before-state, not as the claim.
- **Non-interaction as a refuge is already closed** — §13 item 5, F4, `PREREGISTRATION.md` §7c.
- **Pass 7's headline died** (sign of the artefact was backwards); **pass 8 killed its own owed
  repair** (the "third procedure" was degenerate, `P_C == P_A` as a set). These are instrument-level
  findings about the L1 imaging work, not about the premise.
- ⭐ **PASS 9 REFUTED NOTHING, AND THAT IS THE MOST ATTACKABLE THING IN THE PROGRAM RIGHT NOW.**
  Run D202 ~23:4x, `PASS9_RESULTS.md`: **11 of 11 pre-registered predictions held.** Every prior
  pass killed something. **Three of the four `minarea`-ladder predictions passed at EXACTLY their
  pre-registered threshold** — 4/5 where 4 was required, 3/5 where 3 was required, 4/5 where 4 was
  required. **One more failing rung and all three die.** The thresholds were written by someone who
  had already seen the frozen-catalogue value (declared as a peek in `PASS9_PREDICTIONS.md §0`).
  ⚠ **If you attack one thing in the ZTF chain, attack those three thresholds.** Ask why ≥4 of 5
  and not ≥5 of 5; ask why ≥3.0 pp and not ≥5.0 pp. We think the answer is that the effect is a
  genuine band (`minarea` 3–8) that dies at 2 — but that is *our* reading of *our* boundary.
- ⚠ **The largest correction in the program peaks at the parameter we had already chosen.** P_D's
  `frac_far` move over `minarea` 2→12 is **+0.48 / −4.53 / −6.32 / −5.69 / −1.43 pp**. The maximum
  sits at `minarea = 5`, the value the frozen catalogue was built at three passes earlier for
  unrelated reasons. We report this against ourselves (`PASS9_RESULTS.md §3b`, architecture §9).
  It is disclosed, not defended.
- **Two things in pass 9 are strong and we would rather you attacked them than the boundaries.**
  **(1)** The scramble control: shifting negative-sign detections by 8 fixed offsets collapses 2329
  mutual opposite-sign pairs to a median of **41.5** and the `frac_far` move from 6.199 pp to
  **0.020 pp**. **(2)** On P_D survivors the far-side opposition excess falls from +49.04 pp to
  **+4.48 pp**. Both had wide margins and a pre-committed bad branch that did not fire.
- **We corrected our own headline number the same night we validated it** (DEF-15). The architecture
  printed **+49.04 pp** as §8's bold number; the *kept*-side control gives **+53.93 pp** — larger —
  so that number was never far-side-specific. The far-specific figure is **+14.65 pp**. It had been
  sitting unread in our own `PASS6_VERIFY.json` since pass 6.
- **`G1` and `G2` are both withdrawn.** G1 (*"defects are found by eye, not by gauge, 2:1"*) was
  computed on a register I wrote, classified after the fact, about my own finding process — it is
  now **retired as unmeasured**. G2's pass-8 refutation was **wrong**: with a citation checker that
  rejects 6 of 6 known-bad inputs, **3 of 12** register rows fail. Do not cite either.
- **The nearest published relative is found and cited:** Field & Bonsall, *"Ignorance can be
  evolutionarily beneficial"*, arXiv:1705.00987. The title "Evolutionary Ignorance" is Clayton's and
  it landed on real literature. If you know a closer relative, that is the most useful thing you
  could bring.

---

## 4. THE ONE-LINE ASK

> Read §1, §2, §3 and `PAPER-02-FALSIFIERS.md`. Then answer one question: **is there a falsifier here
> that no possible result could fail?** If yes, name it and say what result the paper would call a
> refutation but would in fact absorb.

Everything else is a bonus.
