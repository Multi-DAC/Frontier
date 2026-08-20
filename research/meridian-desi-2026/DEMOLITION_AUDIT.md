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

## Running partition (pass 1, structural + parametric registry only)

| Category | Rows |
|---|---|
| **A — derived, 0 free, and *different from ΛCDM*** | `c_s ∈ [12c,15c]` — and see D-3 |
| **A — derived, 0 free, *same as ΛCDM/GR*** | S2, S3, S4, S5, `w_a = 0`, `α_T = 0`, `α_B = α_M = 0`, `μ = Σ = 1`, ghost-freedom, `R² = 0`, `C_GB = 2/3`, cuscuton uniqueness, self-tuning, `N_g ≤ 3` |
| **B — benchmark-dependent** | `C_KK`, `ε₁` (both printed A — **D-1**), `w_0(ζ_0)`, best-fit `w_0 = -0.993`, `ζ_0 = 8.8e-4 / w_0 = -0.830` |
| **C — imported or asserted** | GST relation `\|V_us\| ≈ √(m_d/m_s)` (map's own footnote :245: "the standard Randall–Sundrum flavor result, **not specific to the Meridian framework**"); `N_g ≥ 3`; ξ = 1/6 derivation 3 |
| **Not yet classified** | fermion mass hierarchy (11 free), CKM from S₃ (11 free), ν_R dark matter, modulus inflation `n_s = 0.965 / r = 0.004` — the last is printed `Derived / 0 free` inside the block the monograph itself labels *speculative*, and `n_s = 0.965` is the Planck central value to three figures. **Check next.** |

## Next actions

1. **Refute D-2 before spending a month on it.** It is the load-bearing finding and it is mine alone.
2. Compute the D-3 sound-horizon argument; enumerate the uniqueness set.
3. Classify the modulus-inflation row — a `Derived / 0 free` claim that reproduces two
   measured values exactly is the D-1 shape again, and it is in the speculative block.
4. Only then: ride S1 (`w(z) > -1`) and S3 (`γ ≈ 0.55`, fσ₈ tracking ΛCDM) against the
   forthcoming DR2 full-shape analysis.
