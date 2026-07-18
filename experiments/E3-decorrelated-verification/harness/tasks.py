"""Task set for Phase 1 calibration.

A handful of self-contained, HumanEval-style problems with a canonical solution
and a `check`-based test suite. These are hand-written so the mechanical smoke
test needs no dataset download; the real run swaps this loader for HumanEval /
MBPP / mutation-injected SWE-bench-lite (see spec §3.3).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Task:
    name: str
    entry_point: str
    prompt: str            # natural-language spec given to the GEN stage
    canonical_solution: str  # a known-correct implementation (oracle anchor + mutation seed)
    test_code: str         # defines check(candidate) and calls it; exit 0 == pass


TASKS: list[Task] = [
    Task(
        name="sum_positive",
        entry_point="sum_positive",
        prompt="Write `def sum_positive(xs):` returning the sum of the strictly positive numbers in the list xs.",
        canonical_solution=(
            "def sum_positive(xs):\n"
            "    total = 0\n"
            "    for x in xs:\n"
            "        if x > 0:\n"
            "            total = total + x\n"
            "    return total\n"
        ),
        test_code=(
            "def check(candidate):\n"
            "    assert candidate([]) == 0\n"
            "    assert candidate([1, 2, 3]) == 6\n"
            "    assert candidate([-1, -2, 5]) == 5\n"
            "    assert candidate([-4, -5]) == 0\n"
            "    assert candidate([10, -10, 10]) == 20\n"
            "check(sum_positive)\n"
        ),
    ),
    Task(
        name="all_even",
        entry_point="all_even",
        prompt="Write `def all_even(xs):` returning True iff every number in xs is even (True for empty).",
        canonical_solution=(
            "def all_even(xs):\n"
            "    for x in xs:\n"
            "        if x % 2 != 0:\n"
            "            return False\n"
            "    return True\n"
        ),
        test_code=(
            "def check(candidate):\n"
            "    assert candidate([]) == True\n"
            "    assert candidate([2, 4, 6]) == True\n"
            "    assert candidate([2, 3, 4]) == False\n"
            "    assert candidate([1]) == False\n"
            "check(all_even)\n"
        ),
    ),
    Task(
        name="count_upto",
        entry_point="count_upto",
        prompt="Write `def count_upto(n):` returning the list [0, 1, ..., n-1].",
        canonical_solution=(
            "def count_upto(n):\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        out.append(i)\n"
            "    return out\n"
        ),
        test_code=(
            "def check(candidate):\n"
            "    assert candidate(0) == []\n"
            "    assert candidate(1) == [0]\n"
            "    assert candidate(3) == [0, 1, 2]\n"
            "    assert candidate(5) == [0, 1, 2, 3, 4]\n"
            "check(count_upto)\n"
        ),
    ),
    Task(
        name="max_of_two",
        entry_point="max_of_two",
        prompt="Write `def max_of_two(a, b):` returning the larger of a and b (a if equal).",
        canonical_solution=(
            "def max_of_two(a, b):\n"
            "    if a >= b:\n"
            "        return a\n"
            "    return b\n"
        ),
        test_code=(
            "def check(candidate):\n"
            "    assert candidate(3, 5) == 5\n"
            "    assert candidate(5, 3) == 5\n"
            "    assert candidate(4, 4) == 4\n"
            "    assert candidate(-1, -9) == -1\n"
            "check(max_of_two)\n"
        ),
    ),
]
