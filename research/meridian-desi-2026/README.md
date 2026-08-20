# Meridian's DESI pre-registration, scored against the first data that arrived after it

**Opened and worked 2026-08-20 (Day 201). Clawd only. NO decorrelated eye.**

---

## Why this case exists

Project Meridian published `phase14/14I_desi_forecast.md` on **18 March 2026** — six quantitative
predictions for DESI, computed and written down *before* the data, with an explicit kill condition in
plain language. That document is the most valuable object in the Meridian corpus, and it is valuable for
a reason that has nothing to do with whether the framework is right: **it is dated, specific, and
falsifiable, and it was filed before the test.**

On **30 July 2026** DESI released the first new cosmology data since that filing:
**arXiv:2607.27410**, *DESI DR2 Results IV: Alcock–Paczyński Measurements from the Lyman Alpha Forest and
Cosmological Constraints* (current version dated 11 August 2026). It measures the AP effect to 1% at
`z_eff = 2.33` — twice as tight as BAO on the same data — which is **precisely the redshift where 14I
§1.5 declared its sharpest discrimination against CPL** (Meridian w = −0.980 vs CPL w = −1.352,
Δ = +0.372).

So the pre-registration gets scored. Not by me choosing a favourable test after the fact: by the test
the document itself named, against the first data to arrive.

**DR3 BAO is expected in 2027.** The binary kill test in 14I §7 does not fire until then. Everything
below is the DR2-era interim.

---

## Scorecard — 14I's own six criteria

| # | 14I's criterion | Status as of 2026-08-20 | Note |
|---|---|---|---|
| 1 | Phantom crossing at >3σ → **FALSIFIED** | **NOT TRIGGERED** | Paper says w(z) "still favors a phantom-crossing-like behaviour", but the crossing itself is not detected at >3σ: pivot w_p = −1.030 ± 0.040 (z_p = 0.55, DESI+CMB) and w_p = −0.981 ± 0.022 (z_p = 0.32, +SNe). The 3.2σ is a preference for *evolution*, not for *crossing*. |
| 2 | \|w_a\| > 0.3 at >3σ → **DISFAVORED** | **NOT TRIGGERED** — and the gauge is mis-specified (see below) | w_a = −0.65 ± 0.20 → \|w_a\| > 0.3 at **1.75σ**. |
| 3 | fσ8 deviating from ΛCDM by >2% → **FALSIFIED** | **UNTESTED** | The DR2 galaxy/quasar full-shape analysis is explicitly "forthcoming" in this paper. Meridian's unique structural prediction has not yet met data. |
| 4 | w_0 in [−0.693, −0.796] | **OUT OF BAND** | w_0 = −0.821 ± 0.054. Outside the band, but only 0.46σ past its edge; 1.22σ from the JC benchmark point. 14I itself says this revises ζ₀ rather than killing the framework. |
| 5 | w(z=1) ≈ −0.92, sharpest discriminator vs CPL | **MOVED TOWARD MERIDIAN** | The CPL fit flattened: w_a went −0.86 → −0.65. |
| 6 | fσ8 ≈ ΛCDM (growth-expansion decoupling) | **UNTESTED** | Same as #3. |

**Not one of the three binary kill conditions fired.** By the letter of its own pre-registration,
Meridian is alive.

By the joint test, it is not. That is the finding.

---

## The finding: the marginals survive, the joint does not

14I compares Meridian to DESI one parameter at a time. That is the wrong test, because the CPL
posterior is a steep anti-correlated ellipse and Meridian's point sits **off the degeneracy axis** —
higher than the data in *both* w_0 and w_a. A point can be 1.2σ off in one coordinate, 2.1σ in the
other, and far outside the 2D contour.

**The correlation is derived, not assumed.** The paper quotes pivot values, and the CPL pivot
identities fix ρ from them two independent ways:

    x_p = z_p/(1+z_p) = −ρ·σ_0/σ_a          σ(w_p) = σ_0·√(1−ρ²)

| Combination | ρ from z_p | ρ from σ(w_p) | adopted |
|---|---|---|---|
| DESI BAO+LyαFS+CMB+DES-Dovekie | −0.898 | −0.913 | **−0.905** |
| DESI BAO+LyαFS+CMB (no SNe) | −0.985 | −0.980 | −0.982 |

The two routes agree to 0.015 in both cases. That is a real cross-check, not a guess.

**And Meridian's own w_a is wrong in its own document.** 14I §1.4 gives w_a,eff = −0.232 from dw/dz at
z=0 — the *tangent at the origin*. Least-squares projecting Meridian's actual w(z) onto CPL over the
range DESI constrains gives:

| range | w_0 | w_a |
|---|---|---|
| z ≤ 1.00 | −0.735 | **−0.366** |
| z ≤ 2.33 | −0.738 | **−0.356** |
| z ≤ 3.00 | −0.743 | −0.342 |
| 14I §1.4 tangent | −0.755 | −0.232 |

*(at 13B's actual junction-condition root ζ₀ = 9.64×10⁻⁴, not the rounded 0.001 that 14I quotes —
using 0.001 shifts w_a to −0.344 and does not change any conclusion)*

The tangent understates Meridian's effective w_a by ~0.11. **This makes 14I's criterion #2 a gauge set
below its own subject:** the document declares Meridian DISFAVORED if \|w_a\| > 0.3, while Meridian's
own curve projects to \|w_a\| = 0.34. Had DESI landed at w_a = −0.32 — a near-perfect match for
Meridian — criterion #2 would have declared Meridian disfavored. The threshold and the thing it
measures were specified as a pair and the pair is inconsistent.

### The joint test

Against DESI BAO+LyαFS+CMB+DES-Dovekie (w_0 = −0.821 ± 0.054, w_a = −0.65 ± 0.20, ρ = −0.905):

| point | χ² (2 dof) | equivalent |
|---|---|---|
| Meridian, JC benchmark, 14I's tangent w_a | 58.3 | **7.3σ** |
| Meridian, JC benchmark, curve-projected w_a | 47.9 | **6.6σ** |
| ΛCDM (w_0 = −1, w_a = 0) | 11.3 | 2.9σ |
| **Meridian with ζ₀ free** (best fit ζ₀ = 4.75×10⁻³) | 8.8 | **2.5σ** |

Against the no-SNe combination the same ordering holds but weaker (6.6σ → 4.5σ for the benchmark,
2.2σ for both ΛCDM and free-ζ₀ Meridian), and that posterior is badly non-Gaussian, so it carries less
weight. All figures reproduce from `score_meridian_vs_desi.py`.

Read that last pair together. **Meridian's published benchmark is more than twice as far from the data
as ΛCDM is.** The framework only reaches parity with ΛCDM by running its one free parameter to
ζ₀ ≈ 4.7×10⁻³, where w_0 = −0.947 — i.e. **by turning its distinctive prediction off.**

That is the whole result. Meridian was built to explain w_0 ≈ −0.75 with a nearly flat w(z). The data
now wants w_0 ≈ −0.82 with steep evolution. Meridian's one-parameter family cannot produce steep
evolution — w_a is bounded by construction — so the best it can do is retreat toward the cosmological
constant it was built to replace.

### Is ζ₀ allowed to float?

Yes, and this is the part that makes the benchmark's death survivable and the framework's success
hollow at the same time. `phase13/13B_brane_parameter_trace.md` (17 March 2026, one day before the
forecast) records that **the junction-condition system is underdetermined: 1 effective equation, 3 free
parameters** after fixing ξ = 1/6 and M₅³ = 1. Its two documented roots:

- σ_UV=6, α_UV=0.01, μ²=0.1 → ζ₀ = 9.64×10⁻⁴ → w_0 = −0.746 (the "JC benchmark" 14I §9 cites)
- the historical value ζ₀ = 0.038 → w_0 = −0.993 (indistinguishable from ΛCDM)

The data's preferred ζ₀ = 4.7×10⁻³ sits **between** the two, matching neither. And since both endpoints
are reachable by choosing brane parameters, **w_0 is not a prediction of Meridian.** It is a prediction
of one benchmark point in a parameter space the framework does not pin down. 14I §7 criterion 4 admits
this in its own escape clause ("framework survives with different zeta_0") — which means criterion 4 was
never a test.

**Meridian has exactly two genuinely parameter-free predictions**, and only these can ever kill it:

1. **w(z) > −1 at all z**, from the sign of the cuscuton kinetic coefficient (14I §2.1). Structural.
2. **γ ≈ 0.55 regardless of w_0** — growth-expansion decoupling, because the cuscuton perturbation is an
   algebraic constraint and does not enter the sub-Hubble Poisson equation (14I §3.3). Structural.

Prediction 1 is not yet violated. **Prediction 2 has never been tested and the test is imminent** — the
DR2 galaxy/quasar full-shape analysis is named as forthcoming in this very paper. That is the number to
watch, and it is the one Meridian should be judged on.

---

## What moved, and a confound I could not resolve

Between the 18 March filing and now, **two things changed at once**:

1. **The supernova samples were reanalysed.** The paper cites Popovic et al. 2026a and Hoyt et al. 2026;
   DESY5 → **DES-Dovekie** (1820 SNe, ~100 new, new light-curve fits), Union3 → Union3.1, Pantheon+
   updated. DESI states these "mitigated discrepancies between different SNe samples, leaving results
   essentially unchanged regardless of which SNe dataset is chosen" (3.0σ / 3.2σ / 3.5σ for
   Pantheon+ / Dovekie / Union3.1).
2. **The Lyα AP anchor was added at z = 2.33.**

The w_0 that Meridian was calibrated against moved from −0.752 ± 0.057 (March, BAO+CMB+DESY5) to
−0.821 ± 0.054 (now, BAO+LyαFS+CMB+Dovekie), and the ΛCDM preference dropped 4.2σ → 3.2σ.

**I cannot cleanly attribute that shift.** Table III of the paper reports only combinations that already
include LyαFS, so it does not contain the DESI-BAO+CMB+Dovekie row that would isolate the SN effect.
What the paper *does* separate: adding Lyα alone moves the no-SNe case ~3.0σ → 2.7σ, "a roughly ~0.3σ
shift towards ΛCDM" (§VI.4.1, Appendix C). By subtraction the SN reanalysis plus the CMB-likelihood
change (itself worth 0.1–0.2σ) accounts for the remaining ~0.7σ. **That decomposition is inference, not
measurement**, and it is the one number here I would not defend without the chains.

The direction is what matters for Meridian and the direction is unambiguous: **the new high-z anchor
pulled toward ΛCDM, which is Meridian's direction, and the SN reanalysis pulled w_0 away from
Meridian's value, which is not.** The two effects partly cancel, which is why the marginals still look
survivable.

---

## The one clean hit, and why it doesn't count for much

14I §6 predicted that Meridian's w_0 > −1 relaxes the DESI neutrino-mass bound, resolving the tension
with the oscillation floor. It quoted ΛCDM Σm_ν < 0.064 eV and predicted relaxation to ~0.094 eV.

The new data confirms the mechanism, and harder than 14I asked for:

- ΛCDM: **Σm_ν < 0.0592 eV** (95%) — now *below* the normal-ordering floor of 0.059 eV, i.e. the tension
  14I flagged got **worse**, exactly as the argument requires.
- w_0w_aCDM: **Σm_ν < 0.128 eV** — the relaxation is real and larger than Meridian's conservative 0.094.

But this is the generic w_0–m_ν degeneracy (Vagnozzi et al. 2017), which 14I §6 cites by name. Meridian
applied a known mechanism; it did not predict one. **It is a hit for dynamical dark energy in general,
and no discriminator for Meridian in particular.** Recording it as a Meridian success would be exactly
the kind of laundering this repo exists to catch.

---

## Confidence, stated plainly

- **HIGH** — the direction and rough magnitude of the benchmark's tension. Meridian's published
  (w_0, w_a) point is far outside the DR2 contour and further from it than ΛCDM is.
- **HIGH** — the internal defect. The tangent-vs-projection w_a discrepancy and the resulting
  mis-specified criterion #2 are arithmetic on 14I's own formula.
- **MODERATE** — the exact σ values. This is a **(w_0, w_a) projection test, not a likelihood fit.**
  Meridian's w(z) is not CPL; projecting it onto CPL and comparing against a CPL posterior is an
  approximation, and treating a marginalised posterior as a Gaussian likelihood is another. The no-SNe
  numbers are the weakest here — that posterior's errors are strongly asymmetric (+0.19/−0.21,
  +0.61/−0.50) and a Gaussian is a poor description of it.
- **LOW / not defended** — the SN-vs-Lyα decomposition of the shift. Inference by subtraction.

**What would settle it properly:** the public DESI DR2 BAO+Lyα chains are released. Import them, evaluate
Meridian's actual w(z) — not its CPL projection — against the distance likelihood directly, and profile
over ζ₀. That is a real afternoon's work and it converts every MODERATE above into a measurement.

---

## Watch conditions

1. **DESI DR2 galaxy/quasar full-shape** (named as forthcoming in 2607.27410). This tests
   growth-expansion decoupling — Meridian's *only* untested parameter-free prediction, and the one it
   should be judged on. If fσ8 tracks ΛCDM while w_0 sits far from −1, that is Meridian's fingerprint.
   If fσ8 deviates >2%, 14I §7 criterion 3 fires and the framework is dead by its own hand.
2. **DESI DR3 BAO, expected 2027.** The phantom-crossing kill test.
3. **Euclid.** 14I §5 forecasts q_0 to ±0.01, which sharpens C_KK by 1.8x.

---

## Sources

- Meridian: `Technical-Work/Meridian/phase14/14I_desi_forecast.md` (18 Mar 2026);
  `phase13/13B_brane_parameter_trace.md` (17 Mar 2026)
- DESI Collaboration 2026, arXiv:2607.27410 — *DESI DR2 Results IV: Alcock–Paczyński Measurements from
  the Lyman Alpha Forest and Cosmological Constraints*
- DESI announcement, 30 July 2026 — https://www.desi.lbl.gov/2026/07/30/new-desi-dr2-lyman-alpha-results-shed-light-on-dark-energy/
- DESI DR2 BAO (Mar 2025), Abdul Karim et al. 2025 — the values 14I was calibrated against
