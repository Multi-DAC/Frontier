"""Mock adapter — validates the mechanical spine with zero model calls, zero cost.

It does NOT pretend to detect defects intelligently. Its only job is to exercise
the pipeline plumbing and the scoring math deterministically, so that everything
Gemini's design-review cannot touch (oracle, mutation, pipeline flow, TP/FP/FN
accounting) is proven correct before a single token is spent on a real lineage.

GEN returns a source we hand it (so the oracle has something concrete to judge).
AUDIT/FILTER emit flags according to a fixed policy passed in at construction,
letting the smoke test drive both "flags a bug" and "stays silent" branches.
"""
from __future__ import annotations

from .base import Adapter, Completion, Usage


class MockAdapter(Adapter):
    lineage = "mock"
    params = 0

    def __init__(self, gen_source: str = "", audit_flags: list[str] | None = None,
                 filter_keeps: bool = True):
        self.gen_source = gen_source
        self.audit_flags = audit_flags or []
        self.filter_keeps = filter_keeps

    def complete(self, stage: str, prompt: str, **kw) -> Completion:
        usage = Usage(prompt_tokens=len(prompt.split()), completion_tokens=1,
                      wall_seconds=0.0, params=self.params)
        if stage == "GEN":
            return Completion(self.gen_source, usage)
        if stage == "AUDIT":
            return Completion("\n".join(self.audit_flags), usage)
        if stage == "FILTER":
            kept = self.audit_flags if self.filter_keeps else []
            return Completion("\n".join(kept), usage)
        return Completion("", usage)
