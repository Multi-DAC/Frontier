"""Oracle — the objective ground truth for Phase 1 (code calibration).

A compiler + test-runner in a subprocess sandbox, plus a mutation generator that
produces *known* defects (a mutant that the tests reject is a ground-truth bug at
a known location). No model is involved here; this is the non-negotiable arbiter
that a flagged defect is real or spurious.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import os
import re
from dataclasses import dataclass, field


@dataclass
class OracleResult:
    passed: bool
    returncode: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False


def run_tests(source: str, test_code: str, timeout: float = 10.0) -> OracleResult:
    """Execute `source` followed by `test_code` in a fresh subprocess.

    `test_code` is expected to define `check(candidate)` and call it, or to run
    bare asserts. A zero exit code means all tests passed.
    """
    program = source + "\n\n" + test_code + "\n"
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(program)
            tmp = f.name
        try:
            proc = subprocess.run(
                [sys.executable, tmp],
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            return OracleResult(False, -1, e.stdout or "", (e.stderr or "") + "\n[TIMEOUT]", True)
        return OracleResult(proc.returncode == 0, proc.returncode, proc.stdout, proc.stderr)
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)


# ---- Mutation generator: manufacture known defects ------------------------

# Each rule is (compiled regex, replacement) applied to the FIRST match only, so
# each mutant carries exactly one localized, known defect.
_MUTATIONS = [
    (r"\+", "-", "arithmetic: + -> -"),
    (r"\bor\b", "and", "boolean: or -> and"),
    (r"\band\b", "or", "boolean: and -> or"),
    (r"<=", "<", "comparison: <= -> <"),
    (r">=", ">", "comparison: >= -> >"),
    (r"==", "!=", "comparison: == -> !="),
    (r"\brange\(([^,)]+)\)", r"range(\1 - 1)", "off-by-one: range(n) -> range(n-1)"),
    (r"\breturn True\b", "return False", "return: True -> False"),
]


@dataclass
class Mutant:
    source: str
    description: str
    rule_index: int


def make_mutants(source: str, test_code: str, timeout: float = 10.0,
                 verify: bool = True) -> list[Mutant]:
    """Produce single-edit mutants of `source`.

    When `verify` is True (default), only mutants that the oracle actually REJECTS
    are returned — i.e. confirmed ground-truth defects. A mutant the tests still
    accept is not a real defect (semantically equivalent edit) and is discarded.
    """
    mutants: list[Mutant] = []
    for i, (pattern, repl, desc) in enumerate(_MUTATIONS):
        mutated, n = re.subn(pattern, repl, source, count=1)
        if n == 0 or mutated == source:
            continue
        if verify:
            res = run_tests(mutated, test_code, timeout)
            if res.passed:
                continue  # tests still pass -> not a real defect
        mutants.append(Mutant(mutated, desc, i))
    return mutants
