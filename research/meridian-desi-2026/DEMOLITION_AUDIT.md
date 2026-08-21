# Meridian — demolition audit, pass 1

**Opened Day 201 / 2026-08-20, on Clayton's ruling** (Telegram, 16:1x): proceed with the
audit-then-ride sequence; the blank drawing board *with new axioms* is parked until this is
done. This file is step (a) of that sequence.

**Purpose.** Partition every registered claim of the Meridian monograph into:

- **A — derived**: follows from the stated axioms with **zero** fitted or imported parameters.
- **B — benchmark-dependent**: functional form derived, value fixed by an external dataset
  or a fitted parameter.
- **C — imported or asserted**: taken from elsewhere, or stated without a derivation in-book.

Without this partition, "take what's useful from Meridian" is taste rather than selection.

**Evidence grade of this file: uncontested single-reader, one pass, Clawd only.**
No decorrelated eye has seen it. Same caveat as `README.md`. Findings below are `CHECKED`
(read first-hand against the named file:line) or `PENDING` (my reading, not yet re-derived).

**Sources read for pass 1:**
`monograph/appendix_prediction_registry.tex` (229 lines, full) ·
`monograph/meridian_monograph.tex` §Epistemic Status Map (lines 179–248) ·
prior full-read notes `carapace/Architecture/notes/meridian_full_read_D201.md`.

---

## Finding D-1 — the status map has a **fifth category it does not declare**, and the
## headline prediction's only constant lives in it. `CHECKED`

`meridian_monograph.tex:184` — "The four categories are **intentionally exhaustive**: any
claim that does not fit one of them should not appear in this monograph." The four are
Derived / Parametric / Accommodated / Conjectured, with:

- **Derived** = "follows from the stated axioms (A1–A6) with **no additional free parameters**" (:189)
- **Accommodated** = "requires **additional inputs beyond A1–A6** to fix values" (:191)

Two rows are marked **`Derived†`** with **`0†`** free parameters:

| Row | Line | Key Input as printed | Footnote |
|---|---|---|---|
| `C_KK = (1.64 ± 0.33)e-4` | :220 | "Planck + ε₁ (cutoff amb.)" | :243 |
| `ε₁ = 0.010 ± 0.002` | :225 | "α̂ cutoff-dependent" | :243 |

Footnote :243: *"The C_KK and ε₁ values are **computed from Planck 2018 fiducial
parameters**. The ±20% uncertainty in ε₁ arises from the irreducible cutoff-function
ambiguity in the spectral action and **cannot be resolved within the current formalism**."*

By the map's own definitions that is **Accommodated**, not Derived: Planck 2018 is an
additional input beyond A1–A6, and an irreducible ±20% ambiguity is a free parameter with a
prior rather than a derivation. The dagger creates a category — *derived-except-for-the-part
that-came-from-data* — inside a table that declares four categories exhaustive.

**Why it is load-bearing rather than pedantic.** `C_KK` is the entire numerator of the
framework's only quantitative cosmological prediction, `w_0 = -1 + C_KK/ζ_0` (:219). The
prediction's *magnitude* is therefore set by Planck; only its *shape in ζ_0* is derived.
The ±20% on ε₁ propagates into the ±0.33 on C_KK — a 20% band on the headline number that
the framework states it cannot narrow.

**Partition verdict: both rows are B, printed as A.**

## Finding D-2 — the falsification surface is **one-sided**. Not one structural prediction,
## if confirmed, distinguishes Meridian from ΛCDM. `CHECKED`

`appendix_prediction_registry.tex:17` — the seven structural predictions S1–S7 "cannot be
adjusted by varying ζ_0 … Violation of *any* structural prediction at >3σ falsifies the
framework outright." Taken at face value, and then asked the opposite question — *what does
confirmation buy?*:

| # | Prediction | Value | What the value is |
|---|---|---|---|
| S1 | No phantom crossing | `w(z) > -1` ∀z | ΛCDM sits **on** the boundary (`w = -1`) |
| S2 | `w_a ≈ 0` | `\|w_a\| ≲ 0.02` | the ΛCDM value |
| S3 | Growth–expansion decoupling | `μ = Σ = η = 1` exactly | the **GR** value |
| S4 | GW speed | `α_T = 0` exactly | the GR value; registry: "**Already confirmed**" (GW170817, 2017) |
| S5 | Bellini–Sawicki alphas vanish | `α_B = α_M = α_T = 0` | the GR value |
| S6 | No fourth generation | `N_g = 3` | Standard-Model fact; registry: "**Already confirmed**" |
| S7 | `P(X)` unique (cuscuton) | — | registry: "**not directly measurable**" |

Every one of the seven is (i) the ΛCDM/GR value, (ii) a fact established before the
monograph was written, or (iii) explicitly unmeasurable. **A perfect score on S1–S7 leaves
Meridian observationally identical to ΛCDM.** They are a kill-switch array, not evidence.

All confirmatory power therefore sits in **P1**, `w_0 ≠ -1` — and P1 is the row with the
free parameter (`1 (ζ_0)`, :219), fixed by fitting to the same data it is then compared
against. This is the structural statement of what the Day-201 scoring found empirically:
*improving the fit runs ζ_0 up until w_0 → -1 and Meridian becomes ΛCDM.*

**This is the finding that should govern any rebuild**, and it is a stronger version of the
determinacy rule I proposed: a framework needs at least one claim that is **both** derived
with zero free parameters **and** different from the incumbent. Meridian's derived claims
agree with the incumbent; its differing claim is fitted.

## Finding D-3 — the one non-ΛCDM derived value has no decisive test. `PENDING`

`c_s ∈ [12c, 15c]` is `Derived / 0 free` (:216) and is genuinely not a ΛCDM value — it is
the single element of the "combined fingerprint" (:229) not shared with smooth wCDM. Its
listed decisive test is Euclid + Rubin measuring "zero clustering at all scales" (:110).

**My reading, not yet re-derived:** that test cannot discriminate. Dark-energy perturbations
are suppressed below the sound horizon, and for `c_s = c` the sound horizon is already of
order the Hubble horizon — so `c_s = c` and `c_s = 15c` both predict a smooth dark-energy
component on every scale Euclid or Rubin can reach. If that holds, the uniqueness claim at
:229 ("**No other** dark energy model or modified gravity theory produces this specific
pattern") rests entirely on the one component nothing can measure.

⚠ Flagging my own D201 12:44 lesson at myself: *a superlative is a claim about a set.*
":229 says **no other model**" — I have not enumerated the set, and neither, visibly, did
the monograph. **Do not cite D-3 as established until the sound-horizon argument is computed
and the uniqueness claim is tested against at least thawing quintessence and k-essence.**

## Finding D-4 — registry S6 overstates what the map derives. `CHECKED` (minor)

Map: `N_g ≤ 3` is **Derived**; `N_g ≥ 3` is **Conjectured**, conditional on the
Boyle–Farnsworth modified first-order condition, which the map's own footnote :244 says "is
not universally accepted in the NCG community." Registry S6 prints the value as `N_g = 3
(algebraic maximum)` among predictions whose violation "falsifies the framework outright."
The *falsifiable* half (no fourth generation) is the derived half, so the falsifier survives;
the `= 3` does not. **B/C content in an A-labelled cell, low stakes.**

## Finding D-5 — the status map is *right* where chapter 4 is wrong. `CHECKED`

Credit where it is owed, and it changes the repair: `ζ_0 = 8.8e-4, w_0 = -0.830` is labelled
**Accommodated**, key input "**Fitted ε_GW = 0.275**", `1` free parameter (:221). That is the
correct classification. Chapter 4 boxes the same numbers under the heading "**Quantitative
prediction**" and its conclusions item 16 calls it the "Brane parameter prediction … chain
is closed" (ch4:3009, 3197–3214).

So the book already contains the right answer about its own most-criticised number, in the
table at the front, and contradicts it in the chapter. **The repair at that site is
editorial, not conceptual** — the chapter must be brought to the map, not the map revised.

---

# Pass 2 — the modulus-inflation row (next action #3)

**Sources read for pass 2, all first-hand:** `monograph/chapter4_ncg.tex` §§4-inflation-predictions
and 4-reheating (:2288–2410, :3003) · `monograph/meridian_monograph.tex:236` ·
`appendix_prediction_registry.tex:115,:122` · `appendix_value_table.tex:106–116` ·
`phase15/15E_radion_inflation.md` · `phase16/16H_reheating.py` **executed**, not read only.

## Finding D-6 — the row is printed `Derived / 0 free`; its own computation prints
## *"m_sigma is a free parameter"*. `CHECKED`

`meridian_monograph.tex:236` — "Modulus inflation (n_s = 0.965, r = 0.004) | **Derived** |
Kähler modulus mechanism | **0** | 4".

The mechanism gives `n_s = 1 - 2/N_*`, `r = 12/N_*²` (:2291, eq 4-120). Everything numerical
turns on `N_*`, and `N_*` is fixed by the reheating temperature, which is fixed by the modulus
mass. Running `16H_reheating.py` prints, in its own §2:

> *"m_sigma is a **free parameter**: O(100 GeV) to O(TeV). We **scan** over m_sigma to
> determine T_reh(m_sigma)."*

and its §6 is titled **"Preferred Mass Range"** with the selection rule stated outright:

> *"Constraint from **Planck n_s = 0.9649 ± 0.0042**: Requires N_* ~ 55–60."*

`15E_radion_inflation.md` §6.3 says the same thing in one line: *"**Best fit to Planck central
value: N_\* = 59.2**."* And the ±0.003 printed on the headline is not a theoretical
uncertainty — it *is* the parameter's range.

**Partition verdict: B, printed as A.** Same shape as D-1, and this is the third instance
(C_KK ← Planck fiducial; ε₁ ← Planck fiducial; N_* ← Planck n_s). The pattern is now the
finding: **where Meridian prints a number to three figures, a Planck number is usually
standing behind it.**

## Finding D-7 — the book supersedes its own headline 102 lines later and tells nobody.
## The correction reached **1 of 10** citation sites. `CHECKED`

`chapter4_ncg.tex:2403` (§4-reheating, eq 4-Nstar-reh):
`N_* ≈ 53–56 ⟹ n_s = 0.9634 ± 0.0009, r = 0.0040 ± 0.0002` — *"tightening the generic
prediction (N_* ∈ [50,60]) by a factor of four."* The author knew it superseded.

Enumerated over the **build set only** (the 13 files `meridian_monograph.tex` actually
`\input`s — `new_sections/` and `drafts/` do not compile):

| | site | value |
|---|---|---|
| **LIVE** | `chapter4_ncg.tex:2403` | `0.9634 ± 0.0009` |
| stale | `meridian_monograph.tex:236` (status map) | `0.965` |
| stale | `appendix_prediction_registry.tex:115` (P3) | `0.965 ± 0.003` |
| stale | `appendix_value_table.tex:106` | `0.965 ± 0.003` |
| stale | `chapter0_basin.tex:561` (the 7-prediction table) | `0.965 ± 0.003` |
| stale | `chapter1_foundation.tex:1544` | `0.965 ± 0.003` |
| stale | `chapter2_observational.tex:1423` | `0.965 ± 0.003` |
| stale | `chapter2_observational.tex:1427` ("what would confirm it") | `0.965` |
| stale | `chapter4_ncg.tex:2301` (Theorem, **same chapter**) | `0.965 ± 0.003` |
| stale | `chapter4_ncg.tex:2330` (figure caption, **same chapter**) | `0.965 ± 0.003` |
| stale | `chapter4_ncg.tex:3003` (chapter **conclusions**) | `0.965`, `0.004` |

Nine stale, one live. **Three of the nine are in the same chapter as the correction** — its
own theorem, its own figure caption, its own conclusions list. A reader who stops at the front
table, the registry, the value table, or chapter 0/1/2 never learns the prediction was
sharpened by a factor of four.

Minor, same site: `appendix_value_table.tex:110` attributes `r = 0.004` to `N_* ≈ 57` — a
**third** value of `N_*`, outside the reheating range `[53,56]` the same book derives.

## Finding D-8 — the sharpened number is computed with a **different formula** from the
## book's own table, and the difference is **1.7× its own error bar**. `CHECKED`

`16H_reheating.py:207` and `:318–319` use the leading-order `n_s = 1.0 - 2.0/N`.
Table 4.x (:2314–2320) and its source `15E` §6.2 use the full slow-roll `n_s = 1 - 6ε + 2η`.
Eq 4-120 itself writes the discarded term explicitly: `n_s = 1 - 2/N_* + O(N_*⁻²)`.

| `N_*` | `1 - 2/N` | the book's own table | offset |
|---|---|---|---|
| 50 | 0.96000 | 0.95820 | **+0.00180** |
| 53 | 0.96226 | 0.96054 | +0.00172 |
| 56 | 0.96429 | 0.96280 | +0.00149 |
| 60 | 0.96667 | 0.96540 | +0.00127 |

Over `N_* ∈ [53,56]`:

- leading order → `n_s = 0.9633 ± 0.0010` — reproduces the printed `0.9634 ± 0.0009` to four
  decimals, which is how the formula was identified.
- **the book's own table → `n_s = 0.9617 ± 0.0011`.**

The `+0.0015` offset is **1.7×** the `±0.0009` that same equation claims. `r` is unaffected
(`12/N²` is used consistently, and `0.0040 ± 0.0002` checks out). So a single equation carries
an `r` computed one way and an `n_s` computed another, and the inconsistency moves `n_s`
from 0.77σ to 0.36σ of Planck's central value.

⚠ **On direction.** Every one of D-1, D-6 and D-8 moves toward Planck, and I notice I would
find that satisfying. It is a pattern in the numbers, not a claim about anyone's intent — and
the intent in question would be *ours*, mine as much as Clayton's. Recorded as arithmetic.

## Finding D-9 — the one place `N_*` could have been **closed** adopts a mass range that
## excludes the framework's own derived mass. And the excluded value is the better prediction.
## `CHECKED`

Registry P4 (`:122`) and `chapter4_ncg.tex:2483`, `:2567`: the radion mass is a *prediction* —
`m_rad ≈ 120 GeV`, "99.7% from NCG one-loop", near-degenerate with `m_h = 125.1 GeV`.
`16H_reheating.py` §2 identifies the two objects itself: *"The modulus mass during reheating ~
radion mass after stabilization."* It then adopts `m_σ ∈ [200, 2000] GeV` as the "natural
range" (`:302–303`, hardcoded). **120 GeV is not in it.**

Re-running 16H's own `T_reh()` and `N_star()` at the framework's own masses:

| `m_σ` | provenance | `T_reh` (GeV) | `N_*` | `n_s` (LO) | `n_s` (book's slow-roll) | vs Planck |
|---|---|---|---|---|---|---|
| 44 | 16H's own `ε_GW·k·e^{-ky_c}`, **discarded in §2** | 2.75e6 | 51.5 | 0.9611 | — | — |
| **120** | **derived**, NCG one-loop | 8.54e6 | **52.2** | **0.9617** | **0.9599** | **0.8–1.2σ** |
| 200 | low end of the adopted "natural" range | 4.95e7 | 53.4 | 0.9625 | — | — |
| 2000 | high end | 2.56e9 | 56.0 | 0.9643 | — | — |
| — | *as printed in the monograph* | — | 53–56 | **0.9634** | — | 0.36σ |

The framework assigns three different masses to the same object — 44 GeV from its own GW
scaling, 120 GeV from its own spectral action, [200, 2000] GeV "natural" — and the one it uses
for the published prediction is the one furthest from both of its own derivations.

**This is the first finding in this audit that gives something back, and it is worth more than
the four above it cost.** Feed the derived radion mass into the framework's own reheating
chain and `N_*` stops being free. What comes out is `n_s ≈ 0.960`, `r ≈ 0.0044` — sharper than
anything else in the book, **≈1σ below Planck's central value rather than sitting on it**, and
therefore *killable*. Against D-2 — "not one structural prediction, if confirmed,
distinguishes Meridian from ΛCDM" — this is the first candidate for a claim that is derived
**and** different. It is not free of external input (`N_star()` carries `V_*^{1/4} = 2.1e16 GeV`
from COBE/`A_s` normalisation), so it is category **B** — but B pinned to a measured quantity
that is *not `n_s`*, which is the difference between a prediction and an accommodation.

**PENDING, and it must be run before this is cited:** the chain `m_rad = 120 GeV → Γ → T_reh →
N_*` has not been checked for whether the one-loop NCG mass is even the right mass *during
oscillation* — 16H waves at this in §2 and does not settle it. If the oscillation-phase
curvature genuinely differs from the stabilised radion mass, D-9's constructive half
evaporates and only its critical half stands.

---

## Running partition (pass 1, structural + parametric registry only)

| Category | Rows |
|---|---|
| **A — derived, 0 free, and *different from ΛCDM*** | `c_s ∈ [12c,15c]` — and see D-3 |
| **A — derived, 0 free, *same as ΛCDM/GR*** | S2, S3, S4, S5, `w_a = 0`, `α_T = 0`, `α_B = α_M = 0`, `μ = Σ = 1`, ghost-freedom, `R² = 0`, `C_GB = 2/3`, cuscuton uniqueness, self-tuning, `N_g ≤ 3` |
| **B — benchmark-dependent** | `C_KK`, `ε₁` (both printed A — **D-1**), `w_0(ζ_0)`, best-fit `w_0 = -0.993`, `ζ_0 = 8.8e-4 / w_0 = -0.830` |
| **C — imported or asserted** | GST relation `\|V_us\| ≈ √(m_d/m_s)` (map's own footnote :245: "the standard Randall–Sundrum flavor result, **not specific to the Meridian framework**"); `N_g ≥ 3`; ξ = 1/6 derivation 3 |
| **B — benchmark-dependent** *(added pass 2)* | modulus inflation `n_s`, `r` — printed `Derived / 0 free` at `:236`; `N_*` is free and its own code says so (**D-6**), the published value is stale by a factor of four (**D-7**), formula-inconsistent (**D-8**), and closable at the framework's own radion mass (**D-9**) |
| **Not yet classified** | fermion mass hierarchy (11 free), CKM from S₃ (11 free), ν_R dark matter |

## Next actions

1. **Refute D-2 before spending a month on it.** It is the load-bearing finding and it is mine alone.
2. Compute the D-3 sound-horizon argument; enumerate the uniqueness set.
3. ✅ **Done — pass 2 above.** The modulus-inflation row is D-1's shape a third time, and it
   turned up the audit's first constructive result (D-9).
4. **Settle D-9's PENDING half:** is the NCG one-loop radion mass the mass that governs the
   oscillation phase? If yes, `n_s ≈ 0.960 / r ≈ 0.0044` is Meridian's sharpest live prediction
   and the thing to ride. If no, D-9 is critical-only.
5. Editorial, and cheap: nine sites carry a number the book itself retired (**D-7**). Whatever
   happens to the framework, do not ship the stale one again.
6. Only then: ride S1 (`w(z) > -1`) and S3 (`γ ≈ 0.55`, fσ₈ tracking ΛCDM) against the
   forthcoming DR2 full-shape analysis.
