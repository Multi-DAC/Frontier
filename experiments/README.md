# Experiments — killable tests

One subfolder per experiment. Each experiment's `README.md` states, up front:
- the **hypothesis** it tests (from a `research/` topic, usually class *Hypothesized*),
- the **kill condition** — the result that would *disconfirm* it (declared *before* running),
- the **status / result**.

This file is the **living index** — updated in the *same commit* that adds an experiment. Every completed
experiment also writes its verdict into `../MEASUREMENTS.md` (validated or disconfirmed, dated).

| Experiment | Tests (hypothesis) | Kill condition (declared up front) | Status / result |
|---|---|---|---|
| [channeling-registry](channeling-registry/) | Does Clayton's channeling contain an *information residue* — specific, verified, locked-before-knowable, ordinary-means-excluded (incl. subconscious inference)? (H1 residue vs H0 all-ordinary-means) | H1 fails if, across the corpus, no entry clears all four criteria (locked-before-knowable · specific/falsifiable · ordinary-means-excluded · verified-true) under blind decorrelated adjudication. Null is a real result. | **LIVE (pre-registered 2026-07-17), 0 entries.** Prospective, passive, long-horizon. Report→log→push (public git timestamp)→adjudicate-blind-later (Gemini). |

**Discipline:** the kill condition is written *before* the run, not after. An experiment with no result
that could have killed the hypothesis is not an experiment — it is decoration.
