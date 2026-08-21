# Meridian — demolition audit

**Passes 1–4, all Day 201 / 2026-08-20.** *(This heading read "pass 1" through three
further passes — the file's own title was the stalest line in it, which is the exact defect
D-7 catalogues in the monograph. Fixed pass 4; a title is a citation site too.)*

**Opened on Clayton's ruling** (Telegram, 16:1x): proceed with the audit-then-ride
sequence; the blank drawing board *with new axioms* is parked until this is done. This file
is step (a) of that sequence.

**WHERE IT STANDS AFTER PASS 4 — read this before the findings.** The column *"derived,
zero free parameters, and different from ΛCDM"* is **empty**. It had one entry, `c_s ∈
[12c,15c]`; pass 4 struck it, because the prediction is unmeasurable in the entire
observable universe (**D-13**, 0.037σ all-sky). Exactly one candidate is left to refill it —
the LISA stochastic GW background from the RS phase transition — and it is **gated on a
bounce action the monograph states twice was never computed** (**D-16**). That calculation,
not any of the editorial repairs, is now the action that decides the program (next action
**#9**).

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

# Pass 3 — settling D-9's PENDING half (next action #4)

**Sources:** `phase15/15E_radion_inflation.md` §§1–6 · `phase16/16H_reheating.py` ·
Planck 2018 X eq (10) · Liddle & Leach 2003. **All numbers below are reproduced by
`close_nstar.py` in this directory** — run it; it prints every table in this section.

**Method note.** Two things were computed twice, on purpose, because a single derivation
here would have been unfalsifiable prose: `N_*` by first-principles entropy/e-fold
accounting **and** by Planck 2018 X eq (10) — they agree to 0.10 e-folds; the e-fold
integral in closed form **and** by numerical quadrature — identical. The chain's own
strongest check is that it lands on a number nobody in this repo put there:
`m_σ = 3.16e13 GeV`, the textbook Starobinsky scalaron mass `1.3e-5 M_Pl`.

## Finding D-10 — **D-9's constructive half is refuted, by the computation D-9 asked
## for.** The oscillation mass is not the radion mass, and it was never free. `CHECKED`

D-9 asked: *is the NCG one-loop radion mass (120 GeV) the mass that governs the
oscillation phase?* **No.** The mass that governs the oscillation phase is the curvature
of the **inflationary** potential at *its* minimum, and 15E writes that potential down:

`V(σ) = V₀ [1 - e^{-√(2/3)·σ/M_Pl}]²` (15E §4.2–4.3) ⟹ `m² = (4/3)V₀/M_Pl²` ⟹ `m_σ = 2H_inf`.

COBE-normalising `V₀` closes it with no freedom at all:

| quantity | value |
|---|---|
| `V_*^{1/4}` | **8.11e15 GeV** (16H hardcodes `2.1e16` — and never reads the variable) |
| **`m_σ = 2H_inf`** | **3.16e13 GeV** = `1.30e-5 M_Pl`, the Starobinsky scalaron mass |
| 16H's assumed range | 200 – 2000 GeV — **off by 1.6e10** |
| Meridian's own `m_rad` | 120 GeV — **off by 2.6e11** |

So my D-9 hypothesis — *feed the derived radion mass in and `N_*` closes at `n_s ≈ 0.960`* —
**is dead.** It was filed `PENDING` with the test that would kill it named in advance, the
test was run, and it killed it. That is the mechanism working, and it is the reason the
PENDING tag exists; had I cited D-9's constructive half yesterday it would now be a
retraction rather than a line item.

**Two things fall with it.** (i) 16H's `Λ_r`-suppressed trace-anomaly width is evaluated at
`m_σ/Λ_r = 8.4e9` — the EFT is invalid by ten orders of magnitude at the true mass, so
16H §7's *"WW + ZZ > 85%, this **distinguishes** Meridian from Starobinsky"* is computed
off-shell and **the claimed reheating signature is void.** (ii) 15E §4.2's own table maps
"Scalaron mass ↔ **Modulus mass at the inflationary minimum**" — the correct identification
is stated in the book, two documents before 16H substitutes the *stabilised* radion instead.
16H did not lack the answer; it walked past it.

## Finding D-11 — but `N_*` closes anyway, **better than the book's version**, with zero
## free mass parameters. This is what pass 3 gives back. `CHECKED`

If `m_σ` is fixed, the only remaining freedom is the *decay coupling* — and `N_*` is bounded
across its entire physical range, from gravitational to instantaneous:

| decay coupling | `Γ` (GeV) | `T_reh` (GeV) | `N_*` | `n_s` | `r` | vs Planck |
|---|---|---|---|---|---|---|
| `M_Pl` (gravitational — slowest possible) | 2.1e2 | 1.23e10 | 51.50 | 0.9627 | 0.00396 | 0.53σ |
| 1e16 GeV | 1.1e7 | 2.85e12 | 53.30 | 0.9639 | 0.00371 | 0.24σ |
| 1e14 GeV | 1.1e11 | 2.74e14 | 54.82 | 0.9649 | 0.00352 | 0.01σ |
| instantaneous (`Γ > H_end` — fastest possible) | ∞ | 2.62e15 | 55.57 | 0.9653 | 0.00343 | 0.10σ |

**`N_* = 51.5 – 55.6`, `n_s = 0.9627 – 0.9653`, `r = 0.0034 – 0.0040`, zero free parameters** —
the width is not a fit, it is the whole physically allowed coupling range. That is a *stronger*
result than the book's `N_* ∈ [53,56]`, which was purchased with an invented mass range.

**And it is worthless as a discriminator.** The entire interval sits inside 0.6σ of Planck's
central value, and `r ≈ 0.0035` is the Starobinsky value to two figures. **Meridian's
inflation sector kills Starobinsky (`R² = 0`, 14A.2) and then reproduces Starobinsky's
predictions exactly** — 15E says so itself, in its own executive summary, as a *selling point*.
Against **D-2** this is decisive: the inflation row is a fourth entry in the "derived, 0 free,
**same as the incumbent**" column. It buys the framework nothing it can be checked on except
LiteBIRD's `r`, and `r` cannot tell Meridian from R² inflation either.

**Partition verdict: the row is genuinely A after this repair — and A of the useless kind.**
D-6 said `Derived / 0 free` was false; the truer statement is that it was false *as computed*
and reachable *as claimed*, and reaching it honestly makes the row less useful, not more.

## Finding D-12 — two arithmetic defects, one in each document, pulling opposite ways. `CHECKED`

**(a) `16H_reheating.py:198`** — `N = 55.4 + (2/3)·ln(T_reh/1e9)`. The coefficient of
`ln T_reh` for matter-dominated (`w_reh = 0`) reheating is **1/3**, not 2/3 (Planck 2018 X
eq 10: `(1-3w)/(12(1+w))·ln(ρ_th/ρ_end)` with `ρ_th ∝ T⁴` gives `4/12`). The anchor is also
high. Over 16H's own scan:

| `m_σ` | `T_reh` | 16H's `N_*` | correct | error |
|---|---|---|---|---|
| 120 | 8.5e6 | 52.22 | 49.07 | **+3.15** |
| 200 | 5.0e7 | 53.40 | 49.65 | **+3.75** |
| 1000 | 9.5e8 | 55.37 | 50.62 | **+4.74** |
| 2000 | 2.6e9 | 56.03 | 50.95 | **+5.08** |

The published `N_* ∈ [53,56]` is, on its own inputs, `[49.6, 51.0]`. Direction: **toward Planck.**

**(b) `15E` §6.2's e-fold column is mislabelled by ≈ 4.3.** The physics is *right* — at each
quoted `φ_*`, 15E's `n_s` and `r` reproduce to four decimals. The `N_*` attached to them does
not: the column uses the asymptotic `u = 1/(2β²N)`, dropping both the `ln u` term and the
`f(u_end)` offset.

| 15E label | `φ_*/M_Pl` | **true `N_*`** | `n_s` (both) |
|---|---|---|---|
| 50 | 5.14 | **45.7** | 0.9580 |
| 55 | 5.26 | **50.7** | 0.9621 |
| 57 | 5.30 | **52.5** | 0.9634 |
| 60 | 5.37 | **55.8** | 0.9655 |

Consequence: *anyone who derives an `N_*` from reheating and looks it up in 15E's table reads
off the wrong `(n_s, r)`* — which is exactly the operation the monograph performs.

⚠ **Direction, and the counter-instance I owe.** In pass 2 I noted that D-1, D-6 and D-8 all
moved toward Planck and flagged that I would find that satisfying. D-12(a) makes four.
**D-12(b) is the first that runs the other way** — it *understates* `n_s` at fixed `N`, which
is why 15E needed "best fit `N_* = 59.2`" to reach Planck's centre when the true best fit is
`N_* ≈ 55`, comfortably inside the range D-11 closes. The pattern is real but it is not
universal, and I would not have found the exception if I had stopped at the first four.

---

# Pass 4 — settling D-3, the last candidate for *derived and different* (next action #2)

**Sources, all first-hand:** `chapter5_sound_speed.tex` (691 lines: §§5-signatures,
5-clustering, 5-isw, 5-perturbation-growth, 5-comparison, 5-landscape,
5-superluminal-comparison, 5-discriminating, 5-detection, 5-direct,
5-detection-summary, 5-conclusions) · `appendix_prediction_registry.tex:106–110, :229` ·
`appendix_computations.tex:39, :95, :425, :489, :547, :565, :801, :817, :1132–1134` ·
`meridian_monograph.tex:156, :165`. **All numbers reproduced by `cs_discriminability.py`
in this directory** (output committed as `cs_discriminability_output.txt`).

**Method note — the controls did the work again.** Two positive controls, and both
failed on the first run, which is the only reason the rest is trustworthy:

- **Control 1** (w → −1 must reproduce the ΛCDM growth factor) came back 5% off, and
  when I "fixed" the initial condition it got *worse* — 33% off. That is the signature
  of a mis-specified gauge, not a mis-specified IC: `D(a)` tracks the **comoving**-gauge
  density contrast and I was grading the **Newtonian**-gauge one near horizon crossing.
  Fixed by comparing `Δ_m = δ_m + 3(Hc/k²)θ_m` between two epochs both deep inside the
  horizon → 0.991, PASS. *The control moving when I touched something unrelated is what
  exposed it.*
- **Control 2** (the signal must be large where physics says it is) I first placed at
  `k = 0.01 h/Mpc` — **30× inside both sound horizons, where the two hypotheses agree**.
  A control sited where right and wrong give the same answer tests nothing. Moved to
  `k = 1e-4 h/Mpc`, between the two sound horizons → 30% effect, PASS.

**And the controls changed the physics I was willing to claim.** Control 2 surfaced that
the fluid equations at `c_s² = 216` are *anti-damped* — the friction coefficient
`−(1−3c_s²)` is **+647** — so I do not trust a direct superluminal integration. The whole
of Leg 2 was therefore rebuilt as a **bound**: compare `c_s = c` (the most strongly
clustering subluminal alternative) against **exactly smooth** DE (the `c_s → ∞` cuscuton
limit, which is Meridian's own S7). Meridian's `c_s = 14.7c` lies between them and much
nearer the smooth end, so that difference is a strict *upper bound* on any
`14.7c` vs `c` signal. Bounding costs nothing here and removes the numerics I distrust.

## Finding D-13 — the `c_s` prediction is unmeasurable **in the entire observable
## universe**. Chapter 5 says so itself, in bold; the registry and the front matter
## do not carry it. `CHECKED`

**First, credit, because it inverts the finding.** `chapter5_sound_speed.tex` §5-direct
already states the conclusion, in the author's own bold:

> ***"Direct detection of dark energy perturbations at c_s = 15c is not feasible with any
> planned experiment."***

and Table 5.4 lists the channel as `DE clustering | δ_DE/δ_m | 10⁻⁷–10⁻⁹ | Far future |
**No**`. Chapter 5 is the most careful chapter in the book. It computes the Jeans length
(`λ_J ~ 50,000–65,000 Mpc`, eq 5-18), notes it *exceeds the observable universe*, and
enumerates its comparison set with citations. **D-3's suspicion was right and it was not
a discovery — the book got there first.**

**Cross-check against the book's own analytic result, before adding anything to it.**
Chapter 5's eq (5-22) gives `δ_DE/δ_m ≈ −[3(1+w)/2]/(c_s²k²/(aH)²)` quasi-statically.
Against my integration, at `w = −0.99`, `c_s = c`:

| `k` [h/Mpc] | `k/aH` | this code | eq (5-22) | ratio |
|---|---|---|---|---|
| 0.01 | 30 | 5.31e-6 | 1.67e-5 | **3.14** |
| 0.03 | 90 | 5.85e-7 | 1.85e-6 | **3.17** |
| 0.10 | 300 | 5.26e-8 | 1.67e-7 | **3.17** |

The ratio is **constant to three figures across three decades in `k`** — the two methods
agree on the scaling law exactly, and differ only by a fixed prefactor, which is the
quasi-static approximation's own known error (eq 5-21 is driven by `δ_m′`; eq 5-22
substitutes `δ_m`, overstating the response by `1/f ≈ 1.9` at `z = 0`, with the neglected
`δ″` and friction terms supplying the rest). **Direction: the exact result is *smaller*
than the book's estimate**, so chapter 5's already-negative feasibility verdict was, if
anything, generous to itself. My instrument and the book's analysis are the same
instrument.

**What the computation adds.** Three things chapter 5 does not say:

**(i) It is volume-limited, not sensitivity-limited.** Every mode a survey can measure
is bounded below by the fundamental mode of its own volume, `k_min = 2π/V^(1/3)`:

| survey | V [(Gpc/h)³] | `k_min` [h/Mpc] | `k_min/k_s(c_s=c)` | `k_min/k_s(14.7c)` |
|---|---|---|---|---|
| Euclid spectroscopic | 20 | 2.32e-3 | **6.9** | 102 |
| Rubin LSST | 100 | 1.35e-3 | 4.1 | 60 |
| Euclid + Rubin | 150 | 1.18e-3 | 3.5 | 52 |
| **the entire observable universe** | 3513 | 4.13e-4 | **1.2** | 18 |

Every ratio exceeds 1, including the last. **Even `c_s = c` has its sound horizon outside
the largest mode that can exist in a survey**, so "zero clustering at all scales" is the
prediction of *both* hypotheses everywhere either can be looked at. No integration time,
detector, or systematics budget touches this — it is the survey volume, and the last row
is the universe.

**(ii) A hard ceiling on the significance, which chapter 5 leaves as "not feasible".**
Summing all 45 log-spaced bands from `k_min` to the edge of the linear regime, in
quadrature, with the DE-clustering-vs-smooth difference as signal and cosmic variance as
noise:

| `w_0` | provenance | S/N (Euclid+Rubin) | **S/N, ALL-SKY** | volume for 3σ |
|---|---|---|---|---|
| −0.990 | registry P1's own weighted mean | 7.7e-3 | **0.037σ** | 1.5e5 × V |
| −0.930 | chapter 4 alternative | 5.7e-2 | 0.27σ | 2.8e3 × V |
| −0.830 | status map `:221`, fitted ε_GW | 1.5e-1 | **0.73σ** | 4.0e2 × V |

"ALL-SKY" replaces the survey with **the entire observable universe** — the largest galaxy
survey physically constructible, ever, by anyone. It is **below 1σ at every `w_0` Meridian
quotes**, and **0.04σ** at the registry's own value. A 3σ detection at the registry's
value needs ~150,000 × the assumed volume, i.e. **~6,500 observable universes.**

**(iii) The signature shrinks as the fit improves — they are anti-correlated.** Every DE
perturbation carries a factor `(1+w)` exactly (`δ_de = (1+w)·D` by construction). The
framework's own fit drives `ζ_0` up and `w_0 → −1`:

| `w_0` | −0.830 | −0.930 | −0.990 | −0.993 | −1.000 |
|---|---|---|---|---|---|
| `(1+w_0)` | 0.170 | 0.070 | 0.010 | **0.007** | 0 |

`−0.993` is the Day-201 best fit to DESI DR2. **The better Meridian fits the expansion
data, the smaller its one unique perturbation signature becomes.** Chapter 5's eq (5-26)
contains the `(1+w)` and never remarks on this; it is the same anti-correlation D-2 found
in `w_0` itself, now in a second observable.

**What is actually broken, then, is not chapter 5 — it is the two layers above it.**

| layer | what it says about `c_s` | verdict |
|---|---|---|
| `chapter5:§5-direct` + Table 5.4 | **"not feasible with any planned experiment"**, `No` | **correct** |
| `appendix_prediction_registry.tex:110` | decisive test = "Euclid + Rubin (zero clustering at all scales)" | **contradicts it** — lists an unfeasible test in the decisive-test column |
| `meridian_monograph.tex:165` | "Chapter 5 provides **the orthogonal observational signature**" | **void** by chapter 5's own analysis |

`:165` is the book's architecture paragraph — the sentence that explains why the five
chapters are one work rather than five papers. It assigns chapter 5 the role of supplying
the orthogonal *observational* signature, and chapter 5's own detection section says the
signature cannot be observed. **This is D-7's shape a second time** (the book supersedes
itself internally and the correction does not reach the citing sites) — and this time it
reaches the front matter's statement of what the book *is*.

⚠ **Fairness, owed.** `c_s ~ 15c` is not empty of all discriminating power: per chapter 5
§5-clustering it *does* exclude clustering-DE models with `c_s ≪ c`, which do predict
detectable effects below ~100 Mpc. That is a real, if modest, exclusion. It buys nothing
**against the incumbent**, because ΛCDM, quintessence, phantom and f(R) all sit at
`c_s² = 1` in the book's own Table 5-3 — and Leg 2 shows `c_s² = 1` is itself
indistinguishable from `c_s² = 216`. The discrimination runs only against a class that is
not the one Meridian must beat.

## Finding D-14 — the uniqueness claim is defensible in the chapter and false in the
## registry, and the escalation happens in exactly one step. `CHECKED`

The same claim appears at three scope levels. The ladder is the finding:

| site | claim | scope | status |
|---|---|---|---|
| `ch5:§5-superluminal-comparison` | "No other model in the literature produces a specific numerical value for the superluminal sound speed **from first principles**" | qualified: *from first principles*; enumerated against DBI k-essence, pure cuscuton, extended cuscuton (Iyonaga/Gao), Galileons, ghost condensate — **with citations** | **defensible** |
| `ch5:§5-discriminating` | "a unique fingerprint that cannot be mimicked by **any model in Table 5-3**" | qualified: a named 7-row table | **defensible** |
| `registry:229` | "unique to the cuscuton mechanism **within five-dimensional self-tuning cosmology**. **No other dark energy model or modified gravity theory produces this specific pattern.**" | first sentence qualified — **second sentence drops the qualifier entirely** | **false** |

Two adjacent sentences, and the escalation is the second one: a claim about **how the
number was derived** (true, checkable, and to the book's credit) becomes a claim about
**what can be observed** (false, by chapter 5's own detection analysis). The audit-the-last-
clause pattern, in its purest form — the qualifier is present, one sentence earlier.

Concretely, at least two models reproduce the whole `:229` fingerprint observationally:
the **pure cuscuton** (`c_s = ∞`, zero DOF, `μ=Σ=1`, `α_T=0`, `w>−1`) — which the book
itself names as its own uncorrected limit — and **thawing quintessence with an ultra-flat
potential** (`w_0 ≳ −1`, `|w_a|` inside Meridian's own S2 bound, `μ=Σ=1` and `α_T=0`
exactly, `c_s = c`). Each differs from Meridian *only* in `c_s`, and D-13 is the statement
that `c_s` cannot be measured. Note also that **Table 5-3 is drawn in the one coordinate
no experiment can read**: it sorts models by the value of `c_s²`, which is precisely the
axis along which they are observationally degenerate.

⚠ **Instrument note, and it nearly cost the finding.** I began the enumeration with
`mcp__paper-search-mcp__search_arxiv`. It **ignores the query and returns the newest arXiv
submissions**, with no error: `"dark energy"` returned hexagonal-lattice charge-density
waves, spin-1 Kitaev magnets and 8-D heterotic strings. Had I skimmed those titles and
seen nothing on cuscutons, the natural conclusion is *"the literature does not contain
this"* — **a fabricated null that CONFIRMS the superlative under audit.** I caught it only
because I was searching for something I already knew existed. The enumeration above comes
from chapter 5's own citation list, read first-hand.

## Finding D-15 — `ζ_0`, the framework's single free parameter, carries **four live
## values spanning a factor of 42**, and the registry's is a weighted mean of two things
## that are not measurements of the same quantity. `CHECKED`

| value | site | `w_0` | what it is |
|---|---|---|---|
| `9.64e-4` | `appendix:39, :547, :817` | −0.865 | **junction-condition benchmark** — the framework's own *derivation* |
| `8.8e-4` | `meridian_monograph.tex:221` (status map) | −0.830 | fitted `ε_GW = 0.275` |
| `0.016 ± 0.002` | `registry:102` (P1 status cell) | −0.990 | **"weighted mean"** — of what, unstated |
| `0.037` | `appendix:39, :162, :204, :618` | −0.996 | **CMB-constraint benchmark** (Hiramatsu–Kobayashi) |
| ~~`0.038`~~ | historical | ~~−0.995~~ | **explicitly superseded** — artefact of `Φ_0 = 0.477` |

The registry's `0.016` sits between the JC benchmark (`0.001`) and the CMB benchmark
(`0.037`) and is quoted nowhere else in the book. A weighted mean of those two is not a
meaningful average: **one is a theory-side derivation and the other is a data constraint.**
Averaging them is the accommodation move stated as a measurement — and it lands in
**registry P1**, which per **D-2** is the row carrying *all* of Meridian's confirmatory
power.

**Credit, and it is substantial.** `appendix_computations.tex` is the most disciplined
layer in the book. It flags the `Φ_0 = 0.477 → 0.076` factor-of-six error as a *historical
note* (`:95`), marks the `B_10 = 171:1` Bayes factor **"Superseded … should not be cited as
current evidence"** (`:565`), and states plainly at `:801` that with the corrected
benchmark **"individual DESI detection significance is ≲ 0.3σ"**. That is better hygiene
than most published cosmology, and it is the book auditing itself correctly.

**Which sharpens the real structural finding of this whole audit.** Across four passes the
layers disagree in *both* directions — D-5: the status map is right and chapter 4 is
wrong; D-13: chapter 5 is right and the registry is wrong; D-15: the appendix is right and
the registry is wrong. **There is no layer of this book that can be trusted by position.**
Front matter, status map, registry, chapter, appendix, code — each has been the correct one
against some other, and the registry has now been wrong three times. The operational
consequence for "take what's useful from Meridian" is concrete: **no row may be selected by
reading a summary table. Every row has to be traced to its chapter and then to its code.**
That is what this audit has been doing; it now has a reason rather than a habit.

## Finding D-16 — the one candidate that survives D-2, and it is gated on a computation
## the book says was never performed. `CHECKED`

Next action #7 asked whether any sector is left that is both derived *and* different.
Reading chapter 5 for D-13 turned one up, and it partially refutes my own framing:

`ch5:Table 5-4` lists a **sixth channel** — the **stochastic gravitational-wave background
from the RS stabilisation phase transition** — as `SNR 18–643 | LISA (~2037) | **Yes
(65–99%)**`. That is not a ΛCDM value, not a pre-established fact, and not unmeasurable.
It has an instrument and a date.

**This does not refute D-2 as worded** — D-2 is about the structural predictions S1–S7,
and this is not one of them. It *does* refute the looser reading I have been leaning on in
conversation ("Meridian buys nothing that can be checked"), and I am recording that against
myself rather than quietly narrowing the claim.

**The gate.** `ch5:609` and `appendix_computations.tex:1132–1134`, both the book's own
words:

> *"A dedicated bounce-action computation for the cuscuton stabilisation mechanism has not
> been performed. If the transition is a smooth crossover, the stochastic GW background is
> absent and Channel 5 yields a null result."*
> *"Whether this conclusion holds for the cuscuton stabilisation mechanism … remains an
> open question."*

The first-order claim is inherited from Creminelli et al. (2002) / Nardini et al. (2007)
for **Goldberger–Wise** stabilisation. Meridian's radion potential has, in the book's own
description, *"a qualitatively different origin (algebraic over-determination rather than a
slowly-varying bulk scalar."* The inheritance is therefore exactly the kind of import
this audit has been cataloguing — except that here **the book flags it itself**, twice.

**This is the highest-value open computation in the corpus, and it is well-posed:** a
bounce action for the Meridian radion potential, which either returns a barrier (→ Meridian
has one falsifiable, non-ΛCDM, instrumented prediction) or does not (→ D-2 stands with no
qualification, and the framework's entire falsification surface is one-sided). Its two
free parameters `α, β/H` keep it category **B** at best — but B with an instrument and a
date beats every A in the book, all of which agree with the incumbent.

⚠ Also noted, and it belongs to goal #17 rather than here:
`appendix_computations.tex:1154` gives the code-availability URL as
`github.com/Multi-DAC/Corpus-Perspectival` under `meridian/` — **the archived, read-only
repository**. The monograph's reproducibility statement points at a tree that can no
longer be pushed to.

---

## Running partition (pass 1, structural + parametric registry only)

| Category | Rows |
|---|---|
| **A — derived, 0 free, and *different from ΛCDM*** | ~~`c_s ∈ [12c,15c]`~~ — **STRUCK, pass 4.** Derived: yes. Different: **not observably**, at 0.037σ all-sky (**D-13**). This column is now **EMPTY.** |
| **The only live candidate for that empty column** *(added pass 4)* | RS stabilisation phase transition → LISA stochastic GW background (`ch5:Table 5-4`, SNR 18–643, 65–99%). Category **B** (`α`, `β/H` free), and **gated on a bounce action the book says was never computed** (**D-16**, next action #9) |
| **A — derived, 0 free, *same as ΛCDM/GR*** | S2, S3, S4, S5, `w_a = 0`, `α_T = 0`, `α_B = α_M = 0`, `μ = Σ = 1`, ghost-freedom, `R² = 0`, `C_GB = 2/3`, cuscuton uniqueness, self-tuning, `N_g ≤ 3` |
| **B — benchmark-dependent** | `C_KK`, `ε₁` (both printed A — **D-1**), `w_0(ζ_0)`, best-fit `w_0 = -0.993`, `ζ_0 = 8.8e-4 / w_0 = -0.830`; **`ζ_0` itself** — four live values `9.64e-4 / 8.8e-4 / 0.016 / 0.037` spanning **42×**, and the registry's is a "weighted mean" of a derivation and a data constraint (**D-15**, pass 4) |
| **C — imported or asserted** | GST relation `\|V_us\| ≈ √(m_d/m_s)` (map's own footnote :245: "the standard Randall–Sundrum flavor result, **not specific to the Meridian framework**"); `N_g ≥ 3`; ξ = 1/6 derivation 3 |
| **B — benchmark-dependent** *(added pass 2)* | modulus inflation `n_s`, `r` — printed `Derived / 0 free` at `:236`; `N_*` is free **as computed** and its own code says so (**D-6**), the published value is stale by a factor of four (**D-7**) and formula-inconsistent (**D-8**) |
| **→ A, *same as ΛCDM/GR*** *(revised pass 3)* | modulus inflation, **after repair**: `m_σ` is fixed by COBE normalisation, so `N_* = 51.5–55.6`, `n_s = 0.9627–0.9653`, `r = 0.0034–0.0040`, **0 free parameters** (**D-11**) — but identical to Starobinsky R² inflation, so it moves from column B to the *unhelpful* half of column A. `120 GeV → N_*` is refuted (**D-10**) |
| **Not yet classified** | fermion mass hierarchy (11 free), CKM from S₃ (11 free), ν_R dark matter |

## Next actions

1. **Refute D-2 before spending a month on it.** It is the load-bearing finding and it is mine alone.
   ▷ **Pass 4 partially did this to itself** (**D-16**): the LISA / RS-phase-transition
   channel is a real candidate for *derived and different*, and I had been overstating D-2
   in conversation as "nothing checkable". D-2 as **worded** (about S1–S7) still stands.
   Still owed: a decorrelated eye. ⚠ Note the correlation — D-14 and D-16 are *my* second
   and third readings of the same book, not independent witnesses.
2. ✅ **Done — pass 4 above. Answer: NO, and the book already knew.** `c_s` is
   unmeasurable in the entire observable universe (all-sky S/N **0.037σ** at the registry's
   own `w_0`); chapter 5 §5-direct says so in bold and the registry `:110` and front matter
   `:165` contradict it (**D-13**). The uniqueness superlative is defensible in the chapter
   and false in the registry, one sentence apart (**D-14**). **`c_s` is struck from the
   "derived and different" column** — the last A-row candidate is gone, and what replaces it
   as the only live candidate is D-16's bounce action.
3. ✅ **Done — pass 2 above.** The modulus-inflation row is D-1's shape a third time, and it
   turned up the audit's first constructive result (D-9).
4. ✅ **Done — pass 3 above. Answer: NO.** The oscillation mass is `2H_inf = 3.16e13 GeV`,
   not the 120 GeV radion; D-9's constructive half is refuted (**D-10**). `N_*` closes anyway
   at `51.5–55.6` with zero free parameters (**D-11**) — and lands on Starobinsky, so it is
   an *A of the useless kind* and feeds D-2 rather than answering it.
5. Editorial, and cheap: nine sites carry a number the book itself retired (**D-7**). Whatever
   happens to the framework, do not ship the stale one again.
6. Only then: ride S1 (`w(z) > -1`) and S3 (`γ ≈ 0.55`, fσ₈ tracking ΛCDM) against the
   forthcoming DR2 full-shape analysis.
7. **New, and the one that changes the shape of the sequence.** D-2 said no *structural*
   prediction distinguishes Meridian from ΛCDM. D-11 now says the *inflation* sector doesn't
   either — it reproduces Starobinsky exactly, in a framework whose stated achievement is
   killing Starobinsky. Two independent sectors, same verdict. **Before the audit continues
   row by row, ask the question at the level it has now been asked twice: is there any sector
   left that is both derived and different?** The candidates are `c_s ∈ [12c,15c]` (D-3,
   possibly unmeasurable), the radion at 120 GeV near-degenerate with `m_h` (collider, 16K),
   and the fermion/CKM sector (11 free parameters, not yet classified). That is the whole list.
8. Cheap and mechanical, same family as #5: the `N_*` labels in 15E §6.2 are wrong by 4.3
   (**D-12b**) and 16H's `N_*` is high by 3–5 (**D-12a**). Any future use of either table
   must go through `close_nstar.py`, not the printed columns.
9. **★ THE ONE THAT DECIDES THE PROGRAM (new, pass 4, from D-16).** Compute the **bounce
   action for the Meridian radion potential** and settle whether the RS stabilisation
   transition is first-order. The book says twice, in its own words, that this was never
   done and that the first-order claim is inherited from Goldberger–Wise — a mechanism it
   describes as *qualitatively different* from its own. The outcome is binary and it decides
   the framework's fate: **barrier →** Meridian has exactly one falsifiable, non-ΛCDM
   prediction with an instrument and a date (LISA, ~2037); **crossover →** Channel 5 is null
   by the book's own statement, and **D-2 stands with no qualification** — the entire
   falsification surface is one-sided and nothing Meridian predicts differs from ΛCDM in a
   measurable way. Everything else in this list is bookkeeping next to this.
10. **Sequencing note, which pass 4 changed.** Actions #5–#8 are editorial repairs to a
    book whose central question is now open in one calculation (#9). **Do #9 first.** A
    stale `n_s` on nine pages does not matter if the answer to #9 is *crossover*; and if it
    is *barrier*, the repair list gets written against a framework that has something to
    defend. Rewriting the citation sites before #9 is optimising the packaging of an
    unresolved object.
11. **Structural, and it is the audit's own working rule now (from D-13/D-15).** There is
    **no layer of this book that can be trusted by position** — the registry has been wrong
    three times against three different layers, and each of front matter, status map,
    chapter, appendix and code has been the *correct* one in some pair. Any future
    selection from Meridian must trace a row to its chapter **and** to its code. Do not
    select by reading a summary table.
