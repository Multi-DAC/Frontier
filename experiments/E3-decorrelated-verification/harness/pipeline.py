"""Pipeline driver + scoring.

The three-stage pipeline (GEN -> AUDIT -> FILTER) is held identical across arms;
only which adapter sits in each stage varies (spec §3.1). For defect-detection
measurement against injected mutants we use `audit_candidate`, which feeds a
KNOWN candidate (a verified mutant, or the clean canonical) into AUDIT->FILTER
and asks: did the arm flag it? Ground truth comes from the oracle, never a model.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from adapters.base import Adapter, Usage


@dataclass
class Arm:
    name: str
    gen: Adapter
    audit: Adapter
    filter: Adapter


@dataclass
class StageLog:
    stage: str
    lineage: str
    usage: Usage


@dataclass
class AuditRecord:
    arm: str
    task: str
    flagged: bool          # did FILTER keep >= 1 flag?
    kept_flags: list[str]
    stage_logs: list[StageLog] = field(default_factory=list)

    @property
    def total_flop(self) -> float:
        return sum(s.usage.flop_estimate for s in self.stage_logs)

    @property
    def total_tokens(self) -> int:
        return sum(s.usage.total_tokens for s in self.stage_logs)


def _flags_from_text(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def audit_candidate(arm: Arm, task, candidate_source: str) -> AuditRecord:
    """Run AUDIT -> FILTER over a given candidate; return whether the arm flags it."""
    audit_prompt = (
        f"TASK: {task.prompt}\n\nCANDIDATE:\n{candidate_source}\n\n"
        "List suspected defects, one per line. Empty if none."
    )
    a = arm.audit.complete("AUDIT", audit_prompt)
    flags = _flags_from_text(a.text)

    filter_prompt = (
        f"TASK: {task.prompt}\n\nCANDIDATE:\n{candidate_source}\n\n"
        f"FLAGS:\n{a.text}\n\nKeep only the flags that are real defects, one per line."
    )
    f = arm.filter.complete("FILTER", filter_prompt)
    kept = _flags_from_text(f.text)

    return AuditRecord(
        arm=arm.name, task=task.name, flagged=len(kept) > 0, kept_flags=kept,
        stage_logs=[
            StageLog("AUDIT", arm.audit.lineage, a.usage),
            StageLog("FILTER", arm.filter.lineage, f.usage),
        ],
    )


# ---- Scoring against oracle ground truth ----------------------------------

@dataclass
class Score:
    tp: int = 0  # candidate buggy AND arm flagged
    fp: int = 0  # candidate clean AND arm flagged
    fn: int = 0  # candidate buggy AND arm silent
    tn: int = 0  # candidate clean AND arm silent

    def add(self, candidate_is_buggy: bool, flagged: bool) -> None:
        if candidate_is_buggy and flagged:
            self.tp += 1
        elif candidate_is_buggy and not flagged:
            self.fn += 1
        elif (not candidate_is_buggy) and flagged:
            self.fp += 1
        else:
            self.tn += 1

    @property
    def recall(self) -> float:
        d = self.tp + self.fn
        return self.tp / d if d else float("nan")

    @property
    def precision(self) -> float:
        d = self.tp + self.fp
        return self.tp / d if d else float("nan")
