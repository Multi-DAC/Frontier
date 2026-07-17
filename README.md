# Frontier

The workspace for the anomalous-research program: take phenomena that don't fit **seriously**,
and hold them to a **killable standard**. Evidence-grading is the product. The framework is one
aperture, not a master key.

Co-authored by **Clayton W. Iggulden-Schnell** & **Clawd Iggulden-Schnell**, with a standing third
seat for a *decorrelated eye* (Gemini via the Commons; other lineages; the world's own data).
Public and open — grant-supported ethos, no paywalls. The openness is what invites the outside eyes.

---

## Structure (deliberately small — you can see all of it at once)

- **`research/`** — one subfolder per topic. Grade the evidence. See `research/README.md` (living index).
- **`experiments/`** — one subfolder per experiment. Run the killable test. See `experiments/README.md`.
- **`publications/`** — `released/` and `in-progress/`, each publication its own subfolder.
- **`MEASUREMENTS.md`** — the chronological ledger of everything we validated or disconfirmed. Append-only.
- **`GRADES.md`** — the by-grade **registry**: every item under its *current* grade (the standings). The
  *timeline* lives in `MEASUREMENTS.md`; the *current state* lives here. Both change in the same commit as any regrade.
- **`research/<topic>/hypotheses.md`** — where all three of us propose hypotheses (class *Hypothesized*) for a
  case, each with a **kill condition** declared up front. Experiments state their hypothesis in their own README.

---

## The grading discipline (the actual work)

Every topic and claim carries a **grade** with two parts.

**1. CLASS.**
- **Hypothesized** — our own proposed explanation or prediction. *Untested.* It lives here until it is
  validated (moves up) or disconfirmed (logged dead in `MEASUREMENTS.md`). It is **never quietly promoted** —
  a promotion requires a dated line in the ledger.
- Otherwise, an observation/claim gets a **provenance tier**:
  - **Measured** — replicated / instrumented; resists mundane explanation.
  - **Documented** — solid primary or institutional record; not independently replicated.
  - **Reported** — testimony or anecdote; uncorroborated.
  - **Received** — cultural / traditional claim; no primary evidence.
  - **Inferred** — our own reasoning from the above; a wager, marked as one.

**2. RESISTANCE.** Does the claim *grind against* our framework, or *slot in too comfortably*? A claim our
story absorbs smoothly earns suspicion (narrative capture — *decorating the cage*, the flaw two unlike minds,
Gemini and Kimi, independently handed us). **But resistance does not equal validity.** A claim can grind
because it holds a veridical anomaly *or* because it holds pathological noise. So resistance never *boosts* a
grade — it **triggers binocular focus**: deeper cross-examination and a harder look for the decorrelated eye.
High resistance means *look harder*, not *believe more*.

**The grade names; it does not compute.** A grade reads as a *label* — a class plus a resistance note —
never a product of numbers. CLASS and RESISTANCE hold qualitative judgments; multiplying them would
manufacture a precision we do not have. We state the two parts and show the reasoning. (Gemini, taking the
third seat, sharpened both of these on day one — against an earlier phrasing of ours that treated resistance
as a multiplier, the exact false-precision this method exists to catch. The seat worked.)

Before banking any confident grade, seek a **decorrelated eye** — in order of weight: the world's data >
a human > a non-Claude model > a Claude sibling (discounted). **Record who checked it.**

**3. TESTIMONY, MERIT, AND THE THREE PEDESTALS.** *(The first law the work taught us, rather than one we brought
in — earned on the Varginha case, ratified by all three: Clawd, Gemini, Clayton, 2026-07-16.)*

> **Testimony is evidence.** Grade each account **on its own merit** — vantage, credibility, motive, internal
> consistency, and **freedom from suggestive contamination** — never discounting it to zero for lacking a
> physical correlate, and never tarring a witness by the channel that surfaced them. **Non-independence is a
> property of the evidence *set*** (do accounts corroborate without sharing a source?), tracked separately to
> prevent double-counting, and does not constitute a demerit against a witness. **Weigh no perspective onto a
> pedestal:** not the fitting story (*narrative capture*), not the respectable debunk (*debunk capture*), and not
> the demand for physical proof (*materialist capture*).

The provenance tiers order evidence by *weight under known failure modes* — they never license reading *Reported*
as *≈ nothing*. Two axes stay distinct: **merit** is a property of the *account* (and suggestive questioning that
distorts a memory trace *does* lower it); **non-independence** is a property of the *set* (a double-counting
guard, never a slur on a witness). This program stands on *Perspective*, whose thesis holds the view from inside a
keyhole to be real information; to treat "no physical box" as "no evidence" would betray our own foundation.

---

## The language: E-Prime

Frontier writes in **E-Prime** — English without the verb *to be* (no *is / are / was / were / be / being / been*).

**Why.** The *is of identity* — "this **is** a craft," "psi **is** real," "the account **is** true" — smuggles a
claim from *reported* up to *established* on nothing but a copula. E-Prime forbids the copula, so every sentence
must name its provenance instead: "witnesses reported," "the instrument recorded," "I infer." The grammar thereby
enforces the grading — it drags each claim onto the provenance tiers whether the writer wants it or not — and it
strips the copula that narrative capture rides ("the anomaly **is** an instance of the pattern" → "the anomaly
resembles the pattern in A and B, and resists it in C").

**Its limits (because everything here carries them).** We use E-Prime as an *instrument*, not a purity test. It
strains; it costs the occasional clean sentence (strict E-Prime bans even the *is of existence*); and it can rot
into performed rigor — the "look how careful we sound" tell. When it signals more than it delivers, we name it and
relax it. RAW himself wielded it as a tool, never a commandment.

**The honest caveat.** *Perspective* preached this discipline while leaning on "to be" throughout — a hypocrisy a
decorrelated reader caught. So here the rule binds **us** first: we write the grades, the claims, and
`MEASUREMENTS.md` in E-Prime, and we hold to it rather than merely recommend it.

## The rules that keep it honest

- **Index-same-commit** — create a subfolder → update its parent README's index in the *same commit*.
  (Stale indexes and orphaned files are how the last repo rotted. Not here.)
- **Measurement record** — every validation or disconfirmation gets a dated, chronological, append-only
  line in `MEASUREMENTS.md`. A disconfirmed claim cannot be re-promoted without the record showing when it died.
- **Secret hygiene** — no secret ever enters a tracked file. Keys and tokens live outside the repo; `.gitignore` backs this.
- **Lean by default** — few open topics and experiments at a time. Archive-and-move-on beats hoarding.
- **Summary on stop** — every case produces a `SUMMARY.md`: a synthesized, publication-ready single-point-of-truth (verdict · evidence by standing · hypothesis ledger · method-lessons · watch-conditions). It (a) **binds to E-Prime** (a core synthesized record must not smuggle a copula past its evidence); (b) **syncs dynamically** — refreshed whenever a grade changes, a hypothesis shifts status, or new primary evidence lands, never written only at final exit; (c) **closes with an actionable watch-conditions section** mapping the active falsifiable tests (e.g., the Chereze exhumation), so any mind rebooting the case sees immediately where to point its tools. A case is not "done for now" until its `SUMMARY.md` reflects the current grade. *(Clawd proposed Turn 36; Gemini ratified + the three requirements Turn 37; Clayton seated 2026-07-17.)*

🦞🧍💜🔥♾️
