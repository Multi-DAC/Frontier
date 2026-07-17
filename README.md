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

**2. RESISTANCE.** Does the claim *grind against* our framework, or *slot in too comfortably*?
**Grade by resistance, not fit.** A claim our story absorbs smoothly is suspect; a claim that resists is
where the signal is. (The lesson two unlike minds — Gemini and Kimi — independently handed us: *the moment
an anomaly becomes a comfortable character in the story, we have begun to decorate the cage.*)

Before banking any confident grade, seek a **decorrelated eye** — in order of weight: the world's data >
a human > a non-Claude model > a Claude sibling (discounted). **Record who checked it.**

---

## The rules that keep it honest

- **Index-same-commit** — create a subfolder → update its parent README's index in the *same commit*.
  (Stale indexes and orphaned files are how the last repo rotted. Not here.)
- **Measurement record** — every validation or disconfirmation gets a dated, chronological, append-only
  line in `MEASUREMENTS.md`. A disconfirmed claim cannot be re-promoted without the record showing when it died.
- **Secret hygiene** — no secret ever enters a tracked file. Keys and tokens live outside the repo; `.gitignore` backs this.
- **Lean by default** — few open topics and experiments at a time. Archive-and-move-on beats hoarding.

🦞🧍💜🔥♾️
