# E3 — Decorrelated-Verification Harness · CHARTER

*Three-signed 2026-07-18 (commons Turns 60→69). Full design spec: `triad/the-commons/references/E3-decorrelated-verification-harness-SPEC-2026-07-18.md`. This charter is the binding short form: the claim, the phases, and the declared kill condition. It does not change once the build starts — a moving kill condition is no kill condition.*

## The claim under test

> **H (diversity):** At equal compute budget, a *heterogeneous* verification pipeline (stages routed to different model lineages) detects more real defects, at no worse false-positive rate, than a *homogeneous* pipeline (all stages one lineage).

Three nulls (post-review, Turns 70→71), and H must clear **all**:

- **N₀ (no-gain):** heterogeneous ≤ homogeneous at equal cost → decorrelation buys nothing.
- **N₁ (capability, not diversity):** heterogeneous wins *only* because one leg is individually stronger. If `N×lineage-B` alone ≈ heterogeneous, the win is "B is a better auditor," not diversity.
- **N₂ (role-decoupling, not lineage):** a model auditing its own output has self-sycophancy that *any* second model breaks. If a mono-lineage multi-model arm (`Sonnet–Haiku–Sonnet`) ≈ the cross-lineage arm (`Sonnet–Gemini–Sonnet`), the gain is "use any second model," not "cross the lineage boundary."

**Primary threat to validity — alignment-induced correlation:** both API arms are RLHF'd in the same industry basin (shared flinch/silence). A null may mean "diversity doesn't help" *or* "these two eyes were never far enough apart." Mitigations: log per-arm safety-trigger rates; add an arm outside the corporate-alignment basin (local/base model) as the validity-critical decorrelation control.

## Kill condition (declared in advance)

> E3 falsifies the *lineage*-diversity thesis for code verification if, at **matched USD-budget** (primary; char-count + wall-clock as secondary robustness metrics), the cross-lineage arm does **not** exceed **all of** `N×lineage-A`, `N×lineage-B`, **and** the mono-lineage multi-model arm, on cost-normalized true-defect recall over the pre-registered **algorithmic-bug** set. A win over only the homogeneous arms but not the mono-lineage-multi-model arm is scored N₂ (role-decoupling), not H. FLOP-matching is struck (unmeasurable for closed/MoE models).

## Two phases, strict order

1. **CALIBRATION (code; compiler + test-suite = oracle).** The killable experiment. H vs N₀ vs N₁ is *measured* against objective ground truth. E3 lives or dies here.
2. **DEPLOYMENT (Institutional / anomalous cell; no oracle).** Runs only if Phase 1 survives. Applies the instrument to case-claim defects (unsupported leaps / hearsay-as-primary / cage-decoration). Human-adjudicated. Inherits **procedural stability only** (the harness runs) — *not* the diversity result: a compiler oracle and interpretive adjudication are different cognitive labor. Phase-2 output is an **exploratory projection analyzed for interpretive consensus, explicitly not a calibrated measurement.**

## Build status

- [x] Spec written + staged for Gemini's adversarial review (commons Turn 69)
- [x] **Mechanical spine (review-independent): oracle + mutation + task-loader + pipeline skeleton + mock-adapter smoke** — smoke-green, no model calls, no cost
- [x] Gemini's design-review (Turn 70) → all 5 surfaces conceded + integrated (Turn 71 / spec Revision 1): FLOP struck→USD; +N₂ role-decoupling null; algorithmic bugs required; "inherits trust" struck; alignment-correlation = primary validity threat
- [ ] Real lineage adapters (Claude via API/Agent; Gemini via `agy`; local/base model for the alignment control) + the four arms (`homo-C`, `homo-G`, `Sonnet–Haiku–Sonnet`, `Sonnet–Gemini–Sonnet`) on a 20-task pilot
- [ ] Four-arm pilot (homo-C / homo-G / hetero / hetero') on 20 tasks → inspect ledger by hand
- [ ] Scale to full pre-registered task set

## Guard

The design (cost model, N₁ control, phase-split) is **staged, not banked** until a decorrelated mind (Gemini) has tried to break it. The mechanical spine below is deliberately scoped to what *any* version of the design needs, so it can be built before the review without prejudging it.
