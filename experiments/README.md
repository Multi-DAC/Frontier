# Experiments — killable tests

One subfolder per experiment. Each experiment's `README.md` states, up front:
- the **hypothesis** it tests (from a `research/` topic, usually class *Hypothesized*),
- the **kill condition** — the result that would *disconfirm* it (declared *before* running),
- the **status / result**.

This file is the **living index** — updated in the *same commit* that adds an experiment. Every completed
experiment also writes its verdict into `../MEASUREMENTS.md` (validated or disconfirmed, dated).

| Experiment | Tests (hypothesis) | Kill condition (declared up front) | Status / result |
|---|---|---|---|
| *(none yet)* | | | |

**Discipline:** the kill condition is written *before* the run, not after. An experiment with no result
that could have killed the hypothesis is not an experiment — it is decoration.
