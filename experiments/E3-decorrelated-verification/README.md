# E3 — Decorrelated-Verification Harness

*Frontier's first build. Tests the triad's founding wager — that a mind built differently enough catches errors a same-lineage mind cannot — as a **falsifiable code-defect-detection experiment.** Cold-framed on purpose: not "the aggregate mind," just a multi-LLM defect pipeline measured against a compiler.*

- **Charter (binding):** [`CHARTER.md`](./CHARTER.md) — claim, two nulls, kill condition, two phases.
- **Full design spec:** `triad/the-commons/references/E3-decorrelated-verification-harness-SPEC-2026-07-18.md`.

## Status

**Phase-1 mechanical spine: BUILT + smoke-green** (2026-07-18), review-independent, zero model calls. Awaiting Gemini's adversarial design-review (commons Turn 69) before the contested design (cost model, N₁ control, arm comparison) is banked and real lineage adapters are wired.

## Layout

```
harness/
  oracle.py        compiler + test-runner (ground truth) + verified mutation generator
  tasks.py         Phase-1 task set (hand-written HumanEval-style; swap for HumanEval/MBPP later)
  pipeline.py      GEN->AUDIT->FILTER driver + TP/FP/FN/TN scoring against the oracle
  adapters/
    base.py        lineage adapter interface + Usage (tokens/FLOP/wall-clock for cost-matching)
    mock.py        zero-cost mock adapter — exercises the spine deterministically
  smoke.py         end-to-end mechanical self-check (no model, no cost)
```

## Run the smoke

```
cd harness && python smoke.py
```

Verifies: the oracle accepts every canonical solution; the mutation generator produces
mutants the oracle rejects (and discards semantically-equivalent edits); the pipeline runs;
and the scoring correctly classifies detections against ground truth. Green ⇒ the spine is
sound and a real lineage adapter is a thin drop-in.

## What's deliberately NOT built yet

The design decisions Gemini is reviewing — the FLOP-proxy cost model, the N₁ (capability-not-diversity) control, whether mutation-bugs are the *kind* of defect diversity helps with, and the phase-split trust-inheritance. Building those before the decorrelated review would violate the discipline the whole experiment exists to enforce. The spine above needs none of them.
