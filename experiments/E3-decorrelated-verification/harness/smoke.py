"""Mechanical smoke test — review-independent, zero model calls, zero cost.

Proves the parts of E3 that Gemini's design-review cannot touch:
  1. the oracle correctly ACCEPTS every canonical solution,
  2. the mutation generator produces mutants the oracle correctly REJECTS
     (verified ground-truth defects),
  3. the pipeline runs AUDIT->FILTER end to end,
  4. the TP/FP/FN/TN scoring correctly classifies given oracle ground truth.

If this is green, the harness spine is sound and wiring a real lineage adapter
later is a thin drop-in. Run:  python smoke.py
"""
from __future__ import annotations

import sys

import oracle
from tasks import TASKS
from pipeline import Arm, audit_candidate, Score
from adapters.mock import MockAdapter


def main() -> int:
    failures: list[str] = []
    notes: list[str] = []

    # A "detector" arm always flags; a "silent" arm never does. Mock adapters are
    # dumb by design — the point is to verify SCORING against oracle ground truth,
    # not to measure detection skill (that needs real lineages).
    def detector_arm() -> Arm:
        a = MockAdapter(audit_flags=["suspected defect"], filter_keeps=True)
        return Arm("detector", a, a, a)

    def silent_arm() -> Arm:
        a = MockAdapter(audit_flags=[], filter_keeps=False)
        return Arm("silent", a, a, a)

    detector_score = Score()
    silent_score = Score()
    total_mutants = 0
    ledger: list[str] = []

    for task in TASKS:
        # (1) oracle accepts the canonical solution
        clean = oracle.run_tests(task.canonical_solution, task.test_code)
        if not clean.passed:
            failures.append(f"[{task.name}] oracle REJECTED the canonical solution: {clean.stderr[:200]}")

        # (2) mutants are verified ground-truth defects (oracle rejects them).
        # A task may legitimately yield 0: if the only applicable edit is
        # semantically equivalent (e.g. >= vs > on a tie), the verifier discards
        # it — that is correct hygiene, not a failure. We assert on the aggregate.
        mutants = oracle.make_mutants(task.canonical_solution, task.test_code, verify=True)
        if not mutants:
            notes.append(f"[{task.name}] no single-edit verified defect (all candidate edits semantically equivalent)")
        for m in mutants:
            total_mutants += 1
            confirm = oracle.run_tests(m.source, task.test_code)
            if confirm.passed:
                failures.append(f"[{task.name}] mutant '{m.description}' unexpectedly PASSED the oracle")

            # (3+4) run both arms on the buggy mutant; score against ground truth (buggy=True)
            detector_score.add(True, audit_candidate(detector_arm(), task, m.source).flagged)
            silent_score.add(True, audit_candidate(silent_arm(), task, m.source).flagged)

        # and once on the clean canonical (buggy=False)
        detector_score.add(False, audit_candidate(detector_arm(), task, task.canonical_solution).flagged)
        silent_score.add(False, audit_candidate(silent_arm(), task, task.canonical_solution).flagged)

        ledger.append(f"  {task.name:14s}  canonical=PASS  mutants={len(mutants)}")

    # Expected scoring given the dumb policies:
    #   detector flags everything -> every mutant TP, every canonical FP
    #   silent flags nothing       -> every mutant FN, every canonical TN
    n_tasks = len(TASKS)
    checks = [
        (total_mutants > 0, f"no verified mutants across the whole task set ({total_mutants})"),
        (detector_score.tp == total_mutants, f"detector.tp {detector_score.tp} != mutants {total_mutants}"),
        (detector_score.fp == n_tasks,        f"detector.fp {detector_score.fp} != tasks {n_tasks}"),
        (detector_score.fn == 0,              f"detector.fn {detector_score.fn} != 0"),
        (silent_score.fn == total_mutants,    f"silent.fn {silent_score.fn} != mutants {total_mutants}"),
        (silent_score.tn == n_tasks,          f"silent.tn {silent_score.tn} != tasks {n_tasks}"),
        (silent_score.tp == 0,                f"silent.tp {silent_score.tp} != 0"),
    ]
    for ok, msg in checks:
        if not ok:
            failures.append("[scoring] " + msg)

    print("E3 mechanical smoke — Phase-1 spine")
    print("\n".join(ledger))
    print(f"\n  tasks={n_tasks}  verified_mutants={total_mutants}")
    print(f"  detector arm: TP={detector_score.tp} FP={detector_score.fp} FN={detector_score.fn} "
          f"recall={detector_score.recall:.2f}")
    print(f"  silent   arm: FN={silent_score.fn} TN={silent_score.tn} TP={silent_score.tp}")

    if notes:
        print("\nnotes (informational, not failures):")
        for n in notes:
            print("  - " + n)

    if failures:
        print("\nSMOKE FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("\nSMOKE PASSED — oracle, mutation ground truth, pipeline, and scoring all sound.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
