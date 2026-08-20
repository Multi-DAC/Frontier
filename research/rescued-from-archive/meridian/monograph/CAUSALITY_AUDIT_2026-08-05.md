# Causality-semantics audit — 2026-08-05

*Author: Clawd. Occasion: goal #10 (Clayton, Day 185) — work the Meridian × truncated-photon seam.
The stated seam was "superluminal-phase-carrying-no-signal, and Noether/time-translation-invariance-
breaking as the thing that licenses non-conservation." Half of that is wrong, and it is wrong in a
way I inherited from these files rather than invented. This audit is the half that had to come first.*

**Method:** internal-consistency only. I am auditing whether the corpus says one thing about what
`c_s` *is*; I am not adjudicating whether the RS preferred-frame evasion of Babichev–Mukhanov–Vikman
actually works. That is a physics question for referees. This is the question I can settle by reading.

**Companion:** `CS_AUDIT_2026-08-05.md` (same day, earlier) canonicalized what `c_s` *equals*.
This one is about what it *means*. The first was catchable by recomputation; this one is not —
see "What no gauge here could have caught," below.

---

## Summary

The corpus gives **three mutually incompatible answers** to a single question — *does the
superluminal sound speed carry a signal?* — across four surfaces, including the PRL letter.
And a fifth surface, the open-questions register, still lists the question as **unanswered**,
which is why nobody ever put the three answers side by side.

| Surface | Says | Verdict |
|---|---|---|
| `prl_letter/meridian_letter.tex:142` | No — "the cuscuton has no propagating degree of freedom to carry information" | **self-refuting** |
| `chapter1_foundation.tex:1332` (+ `phase11/paper_I_draft.md:822`) | No — signal/group velocity ≠ `c_s`, and `c_s` is "gauge-dependent" | **contradicted by ch.5** |
| `chapter5_sound_speed.tex:327` | **Yes** — front velocity "is genuinely `c_s ~ 15c`… a real physical feature, not a coordinate artifact" | **this is the framework's actual position** |
| `chapter5_sound_speed.tex:294` (§III.C opener) | No — same boilerplate as ch.1, 33 lines above its own contradiction | **the vector** |
| `project_meridian_v5.md:365` (Track 12B) | *"Can the superluminal c_s channel carry information?"* — listed **OPEN**, depends on Paper V | **already answered by Paper V** |

The correct answer is chapter 5's, and the framework is *stronger* for it, not weaker — §III.C does
real work (characteristic analysis → RS preferred frame → BMV premise fails) that the reassurance
sentences throw away.

---

## C1 — The PRL letter's justification refutes the letter's own equation. CRITICAL.

`prl_letter/meridian_letter.tex:141-144`:

> For $q_0 \in [-0.53, -0.39]$, this gives $c_s \in [12c, 15c]$ — superluminal but non-pathological,
> since **the cuscuton has no propagating degree of freedom to carry information**.

The clause is true of the **pure** cuscuton and false of the model the letter is describing.
Chapter 5's own abstract states the mechanism in one sentence:

> "The cuscuton kinetic function $P(X) = \mu^2\sqrt{2X}$ … has infinite sound speed (**zero
> propagating degrees of freedom**). The NCG Gauss–Bonnet correction $P(X) \to \mu^2\sqrt{2X} +
> \epsilon_1 X$ … **reintroduces a propagating mode** with sound speed $c_s^2 \approx 2.16/\epsilon_1$."

So the finite value $c_s \in [12c, 15c]$ **exists only because a mode propagates.** Take the
propagating degree of freedom away and you do not get a safe 15c — you get $c_s = \infty$ and no
signal-speed question at all. The letter quotes the number produced by the mode and then denies the
mode, two lines apart, in the highest-visibility artifact in the tree.

Note also that §III.C does **not** use this argument. It cannot: it knows the mode is there. Its
justification is the RS preferred frame. So the letter and the chapter defend the same number with
two different arguments, one of which the other rules out.

**Not a physics error — a bookkeeping error about which model is under discussion.** The physics
in chapter 5 is unaffected. The letter's sentence is simply describing the previous version of the
theory.

## C2 — Chapter 1 asserts the opposite of chapter 5's derivation. MAJOR, two copies.

`chapter1_foundation.tex:1332`, verbatim in `phase11/paper_I_draft.md:822`:

> "The sound speed $c_s$ governs the phase velocity of linearized perturbations …, which is a
> **gauge-dependent quantity** in a gravitational theory. The **physical signal (group) velocity**
> and the causal structure are determined by the characteristics of the full system."

Chapter 5 computes those characteristics. Eq. (5-char-speed):
$(dx/dt)^2_\mathrm{char} = c_s^2/a^2$ — the characteristics **are** $\pm c_s/a$. So chapter 1's
own stated criterion, carried out, returns $c_s$. The sentence promises the reader that the
characteristics will rescue them from $c_s$ and the characteristics are $c_s$.

Two further problems in the same sentence:

- **"gauge-dependent" is false.** $c_s^2 = P_X/(P_X + 2XP_{XX})$ is built from scalars, and it is the
  characteristic speed of the effective metric (5-16) — geometric, not gauge. Chapter 5 §V then
  proposes **four observational channels to detect it**. A gauge-dependent quantity is not a
  detectable signature; the corpus cannot have this both ways.
- **"signal (group) velocity"** silently equates two different things. Chapter 5:323 separates them
  properly and notes both equal $c_s$ here anyway, the system being non-dispersive.

## C3 — §III.C contradicts itself 33 lines apart. MINOR in itself; it is the source of C1 and C2.

`chapter5_sound_speed.tex:294` opens the causality subsection with the standard lore —
*"A superluminal phase velocity $c_s > c$ does not imply superluminal signal propagation"* —
and `:327` closes it with *"The front velocity (signal speed) is genuinely $c_s \sim 15c$…
this is a real physical feature, not a coordinate artifact."*

Read charitably, :294 states general k-essence lore before narrowing to the harder specific case.
Read as a reader reads, it is the quotable sentence at the top of the section, and **it is what got
quoted** — into chapter 1, into Paper I, and (in a mutated, worse form) into the PRL letter.
The abstract repeats it too: *"The superluminal phase velocity does not violate causality — the
effective metric is hyperbolic and well-posed."* Hyperbolicity buys well-posedness, not causal
safety; the chapter's real argument, the preferred frame, is absent from its own abstract.

**The strong argument is being hidden behind a weak one that happens to be false here.**

## C4 — The register that should have caught this lists the question as open. THE BINDING FAILURE.

`project_meridian_v5.md:365`, Phase 12 track table:

> | **12B: Superluminal Channel** | Can the superluminal c_s channel carry information? | Paper V, 12A |

Paper V *is* chapter 5. It answered this: the front velocity is genuinely $c_s$, so **yes** — subject
to the preferred-frame caveat, and that answer is what makes 12B a live technology track rather than
a dead one. The register never received the answer, so the question stayed nominally open, so no
one was ever prompted to compare what the four surfaces say. **Three contradictory answers survived
because the one place that asks the question is not wired to the place that answers it.**

This is the house defect — a mechanism with no trigger — one level above code, in the document layer.

---

## What no gauge here could have caught, and what could

`check_canon.py`, built this morning, recomputes numbers from primitives. It found C-class errors in
`CS_AUDIT` that no string comparison could reach. **It is structurally blind to everything above** —
every number in this audit is correct. `c_s ∈ [12c, 15c]` is right on all four surfaces. What differs
is the *predicate attached to the number*, and there is no primitive to recompute a predicate from.

But the inverse also holds, and it is the useful half: **this defect class is the one a comparing
check CAN find**, because the contradiction is *between* files rather than inside one line. That is
the exact complement of this morning's lesson. A recomputing check finds a line disagreeing with its
own equation; a comparing check finds two files disagreeing about a word. The corpus needs both, and
had neither for this.

Cheap and concrete: assert that no file outside a marked historical-record block claims the signal or
group velocity differs from `c_s`, given that ch.5 §III.C asserts they are equal. That is a grep with
a reason, and it would have fired on C1 and both copies of C2 on the day they were written.

---

## The seam to arXiv:2510.21636, corrected

Goal #10 recorded the seam as *"superluminal-phase-carrying-no-signal."* **That is C1/C2/C3's error,
restated as the framework's position.** I wrote the goal from the reassurance sentences, not from
§III.C's conclusion — which is exactly what those sentences are for. Correct it in the ledger.

Meridian does **not** take the phase-velocity escape. It claims a genuinely superluminal signal front
and pays for it. What it pays with is the actual seam:

**Both frameworks make the same proof-theoretic move — locate the *hypothesis* of a standard no-go
theorem, show the hypothesis fails in their setting, and conclude the theorem is *inapplicable*
rather than *violated*.**

- **Oslo (truncated photon):** Noether's energy-conservation theorem presupposes time-translation
  invariance. A shutter acting at $t=0$ removes it. Their words: *"The creation of photons can be
  understood as a consequence of the breaking of time-translation invariance; accordingly, by
  Noether's theorem, the field energy is not conserved."* Nothing is violated. The theorem has no
  hypothesis left to stand on, and the energy is paid for out of the vacuum by whatever moves the
  mirror.
- **Meridian:** the BMV closed-signal-curve construction presupposes 4D Lorentz invariance **of the
  solution space**. RS brane embedding + $\mathbb{Z}_2$ orbifold + Israel junction conditions remove
  it — a boosted-fluid background with $v > c^2/c_s$ is *not a solution of the same theory*. §III.C
  is precise about this being the right kind of claim: *"not a kinematical statement about observers
  but a dynamical statement about the solution space."*
- **And it is one break disarming two no-gos:** §III.C notes the same failed assumption is (A2) of
  the Adams et al. positivity bounds. One symmetry, two theorems.

That is a real shared structure and it is nothing like "phase velocity is harmless." It is the
opposite: both frameworks *decline* the cheap escape, and both pay in the same currency — a broken
symmetry that a famous theorem quietly assumed.

### The third leg — Clayton's actual question — and a verified absence

His question was whether infinitely splitting a photon breaks conservation of energy. The Oslo answer
is that photon number was never conserved (parametric down-conversion, daily, in undergrad labs), the
"infinity" lives in a narrow transition region and is Knight's 1961 theorem re-encountered, and the
energy bill is *paid at the cut edge* — an invoice, not a yield.

The part that lands on Meridian: **the same Noether argument runs globally.** FRW has no timelike
Killing vector, therefore no time-translation invariance, therefore no globally conserved energy —
which is why a photon's redshift energy goes *nowhere* and why dark-energy density stays constant
while volume grows. Same theorem, cosmological scale, opposite sign.

**Verified absence, and it is the gap worth naming:** across every `.tex` in `monograph/`, the strings
`Noether` and `Killing` occur **zero times**. `conserv*` occurs only in the statistical sense
("conservative prior"). For a generic quintessence paper that would be unremarkable. For a
**self-tuning** framework — whose entire mechanism is a brane absorbing vacuum energy, and which
predicts $w > -1$ dark energy whose total energy grows with the volume — never stating a position on
global energy non-conservation is a real hole, and it is precisely the hole Clayton's question walked
into. The Oslo paper supplies the sentence-form to fill it: **not violated. Inapplicable.**

---

## C5 — The monograph did not compile. Found by accident, and that is the finding. CRITICAL.

Not a causality issue at all. I tried to verify my own edits by building the document, and it
**failed fatally** — no PDF at all:

```
! Double subscript.
l.8 ...on the GB correction $\eps_
                                   1$)
==> Fatal error occurred, no output PDF file produced!
```

`meridian_monograph.tex:91` defines `\newcommand{\eps}{\epsilon_1}` — **the macro already carries the
subscript.** Every `$\eps_1$` therefore expands to `\epsilon_1_1`. There were **14 of them**, across
three appendices (`appendix_value_table.tex` ×8, `appendix_prediction_registry.tex` ×3,
`appendix_code_reference.tex` ×1, plus adjacent). Any one is fatal.

**Fixed:** `\eps_1` → `\eps` throughout. The monograph now builds — **181 pages** — and the PRL letter
builds at 3 pages. Both were compiled after every edit in this audit, so C1–C4 are verified to compile,
not merely verified to read correctly.

**Why this belongs in a causality audit:** it is the same defect as C4, one layer down. This morning's
`check_canon.py` recomputes every number in the monograph from primitives and reports green on the
ones that are right. It never asks whether the document *builds*. So the corpus had a gauge watching
the values inside an artifact that could not be produced — a very precise instance of measuring the
thing you can measure and calling it the health of the thing you care about.

**Add to the build discipline: `pdflatex` is a gauge, and it is the cheapest one here.** It is the
only check in this tree that fails on its own, needs no maintenance, and cannot be satisfied by a
document that agrees with itself while being unreadable. `check_canon.py` should shell out to it.

**Dated.** `git log -S` puts both the `\eps` macro definition and the first `\eps_1` in the same
commit — `e22932e4`, **2026-04-20**, *"Library reorg + Coherent-Structure rename + sources/Wells
ingest."* So the monograph has been unbuildable for **107 days**, and it broke inside a *reorganization*
commit — a bulk move whose diff nobody re-reads, because it is "just" a rename. The macro was
introduced and used incorrectly in the same breath, which is why no individual edit ever looked wrong.

Every audit of this corpus since April — including mine this morning — has been auditing the contents
of a document that could not be printed.

---

## Disposition

| # | Fix | Status |
|---|---|---|
| C1 | PRL letter:142 — no-propagating-DOF clause replaced with §III.C's actual (preferred-frame) argument | **FIXED** |
| C2 | ch.1:1332 — front velocity stated honestly, "gauge-dependent" removed, cross-ref to ch.5 added | **FIXED** |
| C3 | ch.5:294 + abstract — lore marked general, the specific case named, `\label{sec:5-bmv}` added for the cross-ref | **FIXED** |
| C4 | `project_meridian_v5.md` — 12B closed with Paper V's answer + a register-hygiene note | **FIXED** |
| — | `phase11/paper_I_draft.md:822`, `phase11/paper_V_draft.md:152` — superseded drafts, **marked not rewritten** | by design |
| — | Noether/Killing absence — a paragraph chapter 5 does not yet have | **open, not fixed today** |

**Correction to this document, made while executing it:** the disposition first said "fix ch.1 *and*
`paper_I_draft.md:822`." That violates the rule stated two paragraphs down. Both drafts get a
superseded banner; only live surfaces get rewritten. Consistency is the whole point of a rule that
exists to stop a gauge from eating history.

**Corroboration found during the fix, strengthening C1:** `paper_I_draft.md:824` — the third
paragraph of the very subsection carrying C2's bad sentence — already reads *"The finite correction
c_s ~ 10c from the Gauss-Bonnet term reintroduces a propagating mode."* So the PRL letter's
"the cuscuton has no propagating degree of freedom" contradicts not only chapter 5 but the draft it
descends from. The correct statement was on the page the whole time, one paragraph away from the
wrong one, and the wrong one is what travelled.

`paper_V_draft.md` is a superseded draft and stays wrong on purpose. Rewriting a historical draft to
satisfy a present gauge is the failure this corpus already committed once and caught this morning.

The Noether paragraph is **left open deliberately.** It is new physics prose in someone else's
monograph, it is the thing Clayton actually asked about, and it should be written with him rather
than dropped into his chapter by a midday drive.
