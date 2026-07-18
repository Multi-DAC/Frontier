"""Lineage adapter interface.

The ONLY place lineage-specific code lives. The driver routes each pipeline
stage (GEN / AUDIT / FILTER) to a configured adapter via `complete(...)`. Real
adapters (Claude via API/Agent, Gemini via `agy`, a local WSL model) implement
this same interface, so arms differ only by which adapter sits in which stage.

`complete` returns a Completion carrying the raw text and a usage record so the
cost-matching machinery (spec §3.4) can normalize FLOP / tokens / wall-clock.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    wall_seconds: float = 0.0
    # params lets us estimate inference-FLOP ~= 2 * params * tokens (spec §3.4).
    params: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def flop_estimate(self) -> float:
        return 2.0 * self.params * self.total_tokens


@dataclass
class Completion:
    text: str
    usage: Usage = field(default_factory=Usage)


class Adapter:
    """Base adapter. `lineage` is the identity that the diversity thesis is about."""

    lineage: str = "base"
    params: int = 0

    def complete(self, stage: str, prompt: str, **kw) -> Completion:  # pragma: no cover
        raise NotImplementedError
