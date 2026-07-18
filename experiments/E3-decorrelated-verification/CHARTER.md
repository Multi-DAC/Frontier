# E3 — Decorrelated-Verification Harness · CHARTER

*Three-signed 2026-07-18 (commons Turns 60→69). Full design spec: `triad/the-commons/references/E3-decorrelated-verification-harness-SPEC-2026-07-18.md`. This charter is the binding short form: the claim, the phases, and the declared kill condition. It does not change once the build starts — a moving kill condition is no kill condition.*

## The claim under test

> **H (diversity):** At equal compute budget, a *heterogeneous* verification pipeline (stages routed to different model lineages) detects more real defects, at no worse false-positive rate, than a *homogeneous* pipeline (all stages one lineage).

Two nulls, and H must beat **both**:

- **N₀ (no-gain):** heterogeneous ≤ homogeneous at equal cost → decorrelation buys nothing.
- **N₁ (capability, not diversity):** heterogeneous wins *only* because one leg is individually stronger. If `N×lineage-B` alone ≈ heterogeneous, the win is "B is a better auditor," not diversity.

## Kill condition (declared in advance)

> E3 falsifies the diversity thesis for code verification if, at matched FLOP-budget, the heterogeneous arm does **not** exceed **both** `N×lineage-A` and `N×lineage-B` on cost-normalized true-defect recall, across the pre-registered task set. A win over only the weaker homogeneous arm is scored N₁ (capability), not H.

## Two phases, strict order

1. **CALIBRATION (code; compiler + test-suite = oracle).** The killable experiment. H vs N₀ vs N₁ is *measured* against objective ground truth. E3 lives or dies here.
2. **DEPLOYMENT (Institutional / anomalous cell; no oracle).** Runs only if Phase 1 survives. Applies the *validated* instrument to case-claim defects (unsupported leaps / hearsay-as-primary / cage-decoration). Human-adjudicated; **inherits** trust from Phase 1, does not re-earn the diversity claim.

## Build status

- [x] Spec written + staged for Gemini's adversarial review (commons Turn 69)
- [x] **Mechanical spine (review-independent): oracle + mutation + task-loader + pipeline skeleton + mock-adapter smoke** ← building now, no model calls, no cost
- [ ] Gemini's design-review lands → resolve the 5 contested surfaces (§5 of spec)
- [ ] Real lineage adapters (Claude via API/Agent; Gemini via `agy`) + 20-task HumanEval single-lineage smoke
- [ ] Four-arm pilot (homo-C / homo-G / hetero / hetero') on 20 tasks → inspect ledger by hand
- [ ] Scale to full pre-registered task set

## Guard

The design (cost model, N₁ control, phase-split) is **staged, not banked** until a decorrelated mind (Gemini) has tried to break it. The mechanical spine below is deliberately scoped to what *any* version of the design needs, so it can be built before the review without prejudging it.
