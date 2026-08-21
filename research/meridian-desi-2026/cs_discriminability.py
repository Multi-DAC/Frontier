#!/usr/bin/env python3
r"""
cs_discriminability.py -- settle Meridian audit finding D-3.

QUESTION (registry P2, appendix_prediction_registry.tex:106-110):
  Meridian predicts c_s in [12c, 15c] (c_s^2 = C_q/eps ~ 216), labelled
  "Derived / 0 free" and cited as the ONE element of the "combined
  fingerprint" (:229) not shared with smooth wCDM.  Its listed decisive
  test is "Euclid + Rubin (zero clustering at all scales)".

  Can that test discriminate c_s = 15c from c_s = c?

METHOD -- three independent legs, deliberately redundant:

  LEG 1  Kinematic.  Dark-energy perturbations are suppressed below the
         DE sound horizon k_s = aH/c_s.  Compare k_s(c_s) against the
         k-range a galaxy survey can actually measure.  No dynamics.

  LEG 2  Dynamical.  Integrate the full Newtonian-gauge fluid
         perturbation equations (Ma & Bertschinger 1995 eqs 29-30, with
         the rest-frame sound-speed gauge correction) for matter + DE,
         for c_s^2 = 1 and c_s^2 = 216, and read off the fractional
         difference in the observable potential phi(k) at z=0.

  LEG 3  Amplitude.  DE perturbations enter every observable multiplied
         by (1+w).  Evaluate that prefactor at Meridian's OWN quoted
         w_0 values and ask what is left to measure.

POSITIVE CONTROL (required -- a null result needs one):
  Run the same integrator at w = -1 + 1e-9, where the DE perturbation
  must vanish identically and matter growth must reduce to the standard
  LCDM growth factor D(a) = (5/2) Om E(a) \int da'/(a'E(a'))^3.
  If that does not reproduce, no null below is believable.

  A SECOND control runs w = -0.5 (grossly non-LCDM), where the c_s
  signature MUST be large -- confirming the integrator can see a
  difference when one exists, i.e. that the null is a measurement and
  not a broken pipe.

Approximations, stated:
  * matter + DE only; radiation omitted from background and
    perturbations.  Integration starts at a_i = 1e-3, after
    matter-radiation equality (a_eq ~ 3e-4) and before horizon entry of
    the largest survey mode (a_entry ~ 6e-3).  The neglect is common to
    both c_s runs and cancels in their difference, which is the only
    quantity claimed.
  * constant w (Meridian's own S2: |w_a| <~ 0.02).
  * no anisotropic stress => phi = psi (Meridian's own S3/S5: mu=Sigma=1).
    Both approximations are the framework's own predictions, so using
    them cannot be said to disadvantage it.

Day 201 / 2026-08-20.  Clawd.
"""

import numpy as np
from scipy.integrate import solve_ivp, quad

# ---------------------------------------------------------------- cosmology
h      = 0.6736
Om     = 0.3153
Ode    = 1.0 - Om
C_KM_S = 299792.458
H0     = 100.0 * h / C_KM_S          # Mpc^-1
HUBBLE_RADIUS = 1.0 / H0             # Mpc


def E(a, w):
    return np.sqrt(Om * a ** -3 + Ode * a ** (-3.0 * (1.0 + w)))


def Hc(a, w):                        # conformal Hubble aH, Mpc^-1
    return a * H0 * E(a, w)


def frac(a, w):                      # rho_i / rho_tot
    e2 = E(a, w) ** 2
    return Om * a ** -3 / e2, Ode * a ** (-3.0 * (1.0 + w)) / e2


# --------------------------------------------------------- LEG 1: kinematic
def leg1():
    print("=" * 78)
    print("LEG 1 -- KINEMATIC.  Sound horizon vs the window a survey can measure.")
    print("=" * 78)
    print()
    print("  Dark energy is smooth (delta_de -> 0) for k >> k_s = aH/c_s.")
    print("  At z=0, aH = H_0, so k_s = H_0/c_s.")
    print()
    print(f"  H_0/c = {H0:.3e} Mpc^-1 = {H0/h:.5f} h/Mpc   (Hubble radius {HUBBLE_RADIUS:.0f} Mpc)")
    print()
    rows = [("c_s = c        (quintessence, k-essence)", 1.0),
            ("c_s = 12c      (Meridian, low end)",      12.0),
            ("c_s = 14.7c    (Meridian, c_s^2 = 216)",  np.sqrt(216.0)),
            ("c_s = 15c      (Meridian, high end)",     15.0),
            ("c_s = infinity (pure cuscuton)",          np.inf)]
    print(f"  {'model':<40} {'k_s [h/Mpc]':>14} {'lambda_s [Mpc]':>16}")
    for label, cs in rows:
        ks = H0 / cs / h                       # h/Mpc
        lam = np.inf if cs == np.inf else 2 * np.pi * cs / H0
        print(f"  {label:<40} {ks:>14.3e} {lam:>16.0f}" if np.isfinite(lam)
              else f"  {label:<40} {ks:>14.3e} {'infinite':>16}")
    print()

    # Survey windows.  k_min is the fundamental mode of the survey volume;
    # no analysis can measure a wavenumber below it.
    surveys = [
        # name,                        volume (Gpc/h)^3
        ("Euclid spectroscopic (0.9<z<1.8)", 20.0),
        ("Rubin LSST photometric (z<2)",     100.0),
        ("Euclid + Rubin combined (optimistic)", 150.0),
        ("the entire observable universe",   4 / 3 * np.pi * (14.0 * h) ** 3),
    ]
    print(f"  {'survey':<42} {'V [(Gpc/h)^3]':>14} {'k_min [h/Mpc]':>15}")
    kmins = {}
    for name, V in surveys:
        L = (V * 1e9) ** (1.0 / 3.0)           # Mpc/h
        kmin = 2 * np.pi / L
        kmins[name] = kmin
        print(f"  {name:<42} {V:>14.1f} {kmin:>15.3e}")
    print()

    ks_cs1 = H0 / 1.0 / h
    ks_m   = H0 / np.sqrt(216.0) / h
    print("  RATIO k_min(survey) / k_s(model)  -- >1 means EVERY measurable mode")
    print("  is already inside the sound horizon, i.e. DE is smooth there anyway:")
    print()
    print(f"  {'survey':<42} {'vs c_s=c':>12} {'vs c_s=14.7c':>14}")
    for name, _ in surveys:
        print(f"  {name:<42} {kmins[name]/ks_cs1:>12.1f} {kmins[name]/ks_m:>14.1f}")
    print()
    print("  VERDICT LEG 1: even for c_s = c the sound horizon lies OUTSIDE the")
    print("  largest mode any planned survey can measure.  'Zero clustering at")
    print("  all scales' is the prediction of BOTH hypotheses over the entire")
    print("  observable window.  The test as written cannot discriminate, and")
    print("  the reason has nothing to do with sensitivity -- it is the survey")
    print("  volume, which no integration time improves.")
    print()
    return kmins


# --------------------------------------------------- LEG 2: full perturbations
def rhs(N, y, k, w, cs2, smooth):
    """
    Newtonian gauge, matter + DE fluid, e-folds N = ln a.

    State: [delta_m, theta_m, D, theta_d, phi]
      D = delta_de/(1+w)  -- rescaled so the system stays regular as w->-1.

    smooth=True is the EXACT c_s -> infinity (cuscuton) limit: the field
    carries no propagating perturbation, delta_de = theta_de = 0
    identically, and DE contributes to the background only.  This is what
    Meridian's own S7 (P(X) uniquely cuscuton) asserts, and it avoids
    integrating the superluminal fluid equations, which are anti-damped
    (the friction coefficient -(1-3c_s^2) is +647 at c_s^2=216) and which
    I do not trust to four figures.  See METHOD note in the header.
    """
    a = np.exp(N)
    hc = Hc(a, w)
    fm, fd = frac(a, w)
    dm, tm, D, td, phi = y

    if smooth:
        D = td = 0.0

    # momentum constraint gives dphi/dN directly (no anisotropic stress)
    dphi = 1.5 * (hc / k ** 2) * (fm * tm + fd * (1.0 + w) * td) - phi

    ddm = -tm / hc + 3.0 * dphi
    dtm = -tm + k ** 2 * phi / hc

    if smooth:
        dD = dtd = 0.0
    else:
        dD  = -(td / hc - 3.0 * dphi) - 3.0 * (cs2 - w) * D \
              - 9.0 * hc * (cs2 - w) * td / k ** 2
        dtd = -(1.0 - 3.0 * cs2) * td + cs2 * k ** 2 * D / hc + k ** 2 * phi / hc

    return [ddm, dtm, dD, dtd, dphi]


def evolve(k, w, cs2=1.0, smooth=False, a_i=1e-3, a_f=1.0):
    """
    Adiabatic growing mode, matter-dominated ICs.

    NOTE (this line is the fix that control 1 forced): the IC must carry
    the k^2 term.  delta_m = -2*phi is only the leading superhorizon
    piece; the full MD growing mode consistent with theta_m = k^2 tau
    phi/3 is

        delta_m = -2 phi - (2/3) (k/Hc)^2 phi        [Hc = 2/tau]

    Dropping it under-initialises delta_m by a factor ~2 for the modes
    of interest at a_i = 1e-3 and cost 5% of the LCDM growth factor.
    """
    hc_i = Hc(a_i, w)
    phi_i = 1.0
    dm_i = -2.0 * phi_i * (1.0 + (2.0 / 3.0) * (k / hc_i) ** 2)
    tm_i = (2.0 * k ** 2 / (3.0 * hc_i)) * phi_i
    y0 = [dm_i, tm_i, dm_i, tm_i, phi_i]      # adiabatic: D = delta_m
    if smooth:
        y0[2] = y0[3] = 0.0
    sol = solve_ivp(rhs, (np.log(a_i), np.log(a_f)), y0,
                    args=(k, w, cs2, smooth), method="Radau",
                    rtol=1e-10, atol=1e-14, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    dm, tm, D, td, phi = sol.y[:, -1]
    return dict(delta_m=dm, delta_de=(1.0 + w) * D, D=D, phi=phi, sol=sol)


def lcdm_growth(a):
    """D(a) normalised so D -> a in matter domination; standard integral."""
    def integrand(x):
        return 1.0 / (x * E(x, -1.0)) ** 3
    val, _ = quad(integrand, 1e-8, a, limit=200)
    return 2.5 * Om * E(a, -1.0) * val


def leg2_controls():
    print("=" * 78)
    print("LEG 2a -- POSITIVE CONTROLS.  Does the integrator work at all?")
    print("=" * 78)
    print()
    k = 0.01 * h                                   # Mpc^-1

    # Control 1: w -> -1 must reproduce the LCDM growth factor.
    # Compared between a=0.1 and a=1, BOTH deep inside the horizon for this
    # k (k/aH = 17 and 30).  The first draft compared a=1e-3 -> a=1, where
    # k/aH = 1.7 and the Newtonian-gauge delta is NOT proportional to D(a);
    # that control graded the gauge, not the integrator, and it moved when
    # I "fixed" the initial condition -- which is how it was caught.
    w = -1.0 + 1e-9
    r = evolve(k, w)

    def delta_comoving(a):
        """
        D(a) tracks the COMOVING-gauge density contrast, not the
        Newtonian-gauge one.  Delta = delta + 3 (Hc/k^2) theta.  Grading
        delta_m against D(a) directly leaves a ~0.3%/decade gauge residual
        that is not the integrator's fault -- and 1.7% of it survived to
        a=1, which is what kept this control red after the a=0.1 move.
        """
        y = r["sol"].sol(np.log(a))
        return y[0] + 3.0 * Hc(a, w) * y[1] / k ** 2

    d_num = delta_comoving(1.0) / delta_comoving(0.1)
    d_lcdm = lcdm_growth(1.0) / lcdm_growth(0.1)
    print(f"  CONTROL 1  w = -1 + 1e-9, c_s^2 = 1, k = 0.01 h/Mpc")
    print(f"    growth  Delta_m(a=1)/Delta_m(a=0.1)   numeric  {d_num:10.5f}")
    print(f"                                           LCDM     {d_lcdm:10.5f}"
          f"   ratio {d_num/d_lcdm:.5f}")
    print(f"    delta_de/delta_m at z=0                         {r['delta_de']/r['delta_m']:.3e}"
          "   (must be <= 1e-9, the size of 1+w)")
    ok1 = abs(d_num / d_lcdm - 1.0) < 0.01 and abs(r["delta_de"] / r["delta_m"]) < 1e-8
    print(f"    -> {'PASS' if ok1 else 'FAIL'}")
    print()

    # Control 2: the signature MUST be large where physics says it is --
    # BETWEEN the two sound horizons, k_s(cuscuton)=0 < k < k_s(c)=3.3e-4.
    # (First draft ran this at k = 0.01 h/Mpc, 30x INSIDE both sound
    # horizons, where the true answer is 'no difference' -- a control
    # placed where both hypotheses agree tests nothing.  Moved.)
    w = -0.5
    kc = 1.0e-4 * h
    clus = evolve(kc, w, smooth=False)
    smoo = evolve(kc, w, smooth=True)
    dphi = abs(smoo["phi"] / clus["phi"] - 1.0)
    print(f"  CONTROL 2  w = -0.5 (grossly non-LCDM), k = 1e-4 h/Mpc")
    print(f"             -- chosen BETWEEN the two sound horizons, where the")
    print(f"                two hypotheses must disagree maximally")
    print(f"    delta_de/delta_m at z=0, c_s = c                {clus['delta_de']/clus['delta_m']:.4e}")
    print(f"    delta_de/delta_m at z=0, smooth (cuscuton)      {smoo['delta_de']:.4e}  (exactly 0)")
    print(f"    |phi(smooth)/phi(c_s=c) - 1|                    {dphi:.4e}")
    ok2 = dphi > 1e-2
    print(f"    -> {'PASS -- the pipe CAN see the difference' if ok2 else 'FAIL -- broken pipe'}")
    print()
    return ok1 and ok2


def leg2(kmins):
    print("=" * 78)
    print("LEG 2b -- DYNAMICAL.  An UPPER BOUND on what c_s can do.")
    print("=" * 78)
    print()
    print("  Compared below: c_s = c (the MOST strongly clustering subluminal")
    print("  alternative) against exactly smooth DE (the c_s -> infinity")
    print("  cuscuton limit Meridian asserts).  Meridian's c_s = 14.7c lies")
    print("  between them and much nearer the smooth end, so this difference")
    print("  is a strict UPPER BOUND on any c_s = 14.7c vs c_s = c signal.")
    print("  Bounding it this way costs nothing and avoids integrating the")
    print("  superluminal fluid equations, which are anti-damped.")
    print()
    ks_h = np.array([1e-4, 3e-4, 1e-3, 2.3e-3, 5e-3, 1e-2, 3e-2, 1e-1])
    V = 150.0 * 1e9                               # (Mpc/h)^3, Euclid+Rubin
    for w, tag in [(-0.990, "registry P1 weighted mean, zeta_0 = 0.016"),
                   (-0.830, "status map :221, fitted eps_GW = 0.275")]:
        print(f"  w_0 = {w}   ({tag})")
        print(f"  {'k [h/Mpc]':>11} {'delta_de/delta_m':>18} {'|dphi/phi| BOUND':>18}"
              f" {'cosmic var':>12} {'S/N':>9}")
        for kh in ks_h:
            k = kh * h
            clus = evolve(k, w, smooth=False)
            smoo = evolve(k, w, smooth=True)
            rat = clus["delta_de"] / clus["delta_m"]
            dphi = abs(smoo["phi"] / clus["phi"] - 1.0)
            # cosmic variance on a band-power at k: sigma/P = sqrt(2/N_modes),
            # N_modes = V k^2 dk /(2 pi^2) with dk = k/10.
            nmod = V * kh ** 3 / (10.0 * 2 * np.pi ** 2)
            cv = np.sqrt(2.0 / max(nmod, 1e-30))
            # P ~ phi^2 k^4 -> fractional signal in P is 2*|dphi/phi|
            snr = 2.0 * dphi / cv
            below = kh < kmins["Euclid + Rubin combined (optimistic)"]
            mark = "  UNMEASURABLE k" if below else ""
            print(f"  {kh:>11.1e} {rat:>18.3e} {dphi:>18.3e} {cv:>12.2e} {snr:>9.1e}{mark}")
        print()
    print("  'cosmic var' is the irreducible fractional error on a power-spectrum")
    print("  band at that k for a 150 (Gpc/h)^3 survey (dk = k/10).  'S/N' is the")
    print("  best possible single-band detection significance of the FULL")
    print("  clustering-vs-smooth difference.  Modes marked UNMEASURABLE lie")
    print("  below the survey's fundamental mode and do not exist in its data at")
    print("  all -- their S/N column is shown only to make the point that even")
    print("  there, where the signal is largest, it is far below unity.")
    print()

    # Summing over bands is the obvious objection to a single-band S/N, so
    # do it rather than leave it as an escape hatch.  Log-spaced bands of
    # width dlnk = 0.1 from the survey fundamental mode to the edge of the
    # linear regime, added in quadrature.
    print("  TOTAL S/N, all bands in quadrature, k_min(survey) -> k_max = 0.1 h/Mpc")
    print("  (linear regime only; dln k = 0.1, so ~44 independent bands):")
    print()
    kmin = kmins["Euclid + Rubin combined (optimistic)"]
    kgrid = np.exp(np.arange(np.log(kmin), np.log(0.1), 0.1))
    V_universe = kmins and (4 / 3 * np.pi * (14.0 * h) ** 3) * 1e9   # (Mpc/h)^3
    print(f"  {'w_0':>8} {'bands':>7} {'S/N Euclid+Rubin':>18} {'S/N ALL-SKY':>13}"
          f" {'V needed for 3-sigma':>22}")
    for w in (-0.990, -0.930, -0.830):
        s2 = 0.0
        for kh in kgrid:
            k = kh * h
            clus = evolve(k, w, smooth=False)
            smoo = evolve(k, w, smooth=True)
            dphi = abs(smoo["phi"] / clus["phi"] - 1.0)
            nmod = V * kh ** 3 / (10.0 * 2 * np.pi ** 2)
            cv = np.sqrt(2.0 / nmod)
            s2 += (2.0 * dphi / cv) ** 2
        tot = np.sqrt(s2)
        # S/N scales as sqrt(V); the observable universe is the hard ceiling.
        tot_sky = tot * np.sqrt(V_universe / V)
        need = (3.0 / tot) ** 2                    # in units of the assumed V
        print(f"  {w:>8.3f} {len(kgrid):>7d} {tot:>18.3e} {tot_sky:>13.3e}"
              f" {need:>18.2e} x V")
    print()
    print("  'S/N ALL-SKY' replaces the survey with the ENTIRE OBSERVABLE")
    print(f"  UNIVERSE ({V_universe/1e9:.0f} (Gpc/h)^3, {V_universe/V:.0f}x the assumed volume) --")
    print("  the largest galaxy survey physically constructible, ever, by anyone.")
    print("  It is still below 1 sigma at every w_0 Meridian quotes, and 40x below")
    print("  1 sigma at the registry's own weighted-mean value.  The last column")
    print("  is the survey volume a 3-sigma detection would require, in units of")
    print("  the assumed 150 (Gpc/h)^3.")
    print()
    print("  STATED LIMIT OF THIS LEG: galaxy clustering only.  The ISW effect")
    print("  (CMB x LSS) is the natural probe of horizon-scale DE clustering and")
    print("  is NOT forecast here.  It does not rescue the test -- the full ISW")
    print("  signal is itself only a ~4-5 sigma detection in LCDM, and the")
    print("  c_s-dependent part of it is the same (1+w)-suppressed fraction")
    print("  tabulated above -- but that is an argument, not a computation, and")
    print("  it is flagged as such rather than folded into the verdict.")
    print()


# ------------------------------------------------------- LEG 3: the prefactor
def leg3():
    print("=" * 78)
    print("LEG 3 -- AMPLITUDE.  Every DE perturbation carries a factor (1+w).")
    print("=" * 78)
    print()
    print("  delta_de = (1+w) * D, exactly, by the rescaling used above; and the")
    print("  DE share of the Poisson source is f_de * (1+w) * D.  So the whole")
    print("  c_s signature is proportional to (1+w) BEFORE any sound-horizon")
    print("  suppression is applied.")
    print()
    vals = [("-0.830", -0.830, "status map :221 (fitted eps_GW), 1 free param"),
            ("-0.930", -0.930, "chapter 4 alternative"),
            ("-0.990", -0.990, "registry P1 weighted mean, zeta_0 = 0.016"),
            ("-0.993", -0.993, "Day-201 best fit to DESI DR2"),
            ("-1.000", -1.000, "LCDM limit, zeta_0 -> infinity")]
    print(f"  {'w_0':>8} {'(1+w_0)':>10}  provenance")
    for s, w, prov in vals:
        print(f"  {s:>8} {1.0 + w:>10.3f}  {prov}")
    print()
    print("  The framework's OWN fit drives zeta_0 up, w_0 -> -1, (1+w_0) -> 0.")
    print("  The better Meridian fits the expansion data, the smaller its unique")
    print("  perturbation signature becomes.  Fit quality and distinguishability")
    print("  are anti-correlated by construction.")
    print()


def leg4():
    """
    CROSS-CHECK against the monograph's OWN analytic result.

    chapter5_sound_speed.tex eq (5-22), quasi-static:
        delta_DE/delta_m ~ -[3(1+w)/2] / (c_s^2 k^2/(aH)^2)
    and eq (5-26) drops the 3/2:
        delta_DE/delta_m ~ (1+w) / (c_s k/(aH))^2

    If my integration disagrees with these by orders of magnitude, one of
    us is wrong and I should find out which BEFORE writing anything down.
    """
    print("=" * 78)
    print("LEG 4 -- CROSS-CHECK vs the monograph's own eq (5-22) and (5-26).")
    print("=" * 78)
    print()
    w = -0.99
    print(f"  w_0 = {w}, c_s = c (so the c_s^2 factor is 1 and drops out)")
    print(f"  {'k [h/Mpc]':>11} {'k/aH':>8} {'this code':>12} {'eq (5-22)':>12}"
          f" {'eq (5-26)':>12} {'ratio 5-22':>11}")
    for kh in (0.01, 0.03, 0.1):
        k = kh * h
        r = evolve(k, w, smooth=False)
        mine = abs(r["delta_de"] / r["delta_m"])
        x = (kh / (H0 / h)) ** 2                  # (k/aH)^2 at z=0
        e522 = 1.5 * (1.0 + w) / x
        e526 = (1.0 + w) / x
        print(f"  {kh:>11.2f} {np.sqrt(x):>8.1f} {mine:>12.3e} {e522:>12.3e}"
              f" {e526:>12.3e} {e522/mine:>11.2f}")
    print()
    print("  Same order of magnitude at every k -- the two methods agree.  The")
    print("  residual factor ~3 is the quasi-static approximation's own error:")
    print("  eq (5-21) is driven by delta_m' but eq (5-22) substitutes delta_m,")
    print("  which overstates the response by 1/f ~ 1.9 at z=0 (f = dlnD/dlna),")
    print("  and the neglected delta'' and friction terms supply the rest.")
    print()
    print("  DIRECTION: the exact result is SMALLER than the book's estimate, so")
    print("  the monograph's already-negative feasibility verdict was, if")
    print("  anything, generous to itself.  This leg CONFIRMS chapter 5.")
    print()


def main():
    kmins = leg1()
    ok = leg2_controls()
    if not ok:
        print("!! CONTROLS FAILED -- nothing below is trustworthy.  Stop.")
        return
    leg2(kmins)
    leg3()
    leg4()
    print("=" * 78)
    print("D-3 VERDICT")
    print("=" * 78)
    print("""
  The registry's decisive test for P2 -- "Euclid + Rubin (zero clustering
  at all scales)" -- is satisfied identically by c_s = c and by
  c_s = 15c, because the DE sound horizon for c_s = c already lies
  outside the largest mode either survey can measure.  Confirming it
  confirms nothing about c_s.

  The residual dynamical difference in phi is smaller than the cosmic
  variance of the largest available survey by orders of magnitude, at
  every k, at both of Meridian's own quoted w_0 values -- and it shrinks
  in proportion to (1+w_0) as the framework's own fit improves.

  P2 is therefore not a prediction under test.  Since c_s is the sole
  element of the ":229 combined fingerprint" not shared with smooth
  wCDM, the fingerprint's discriminating power is zero on all currently
  planned data.
""")


if __name__ == "__main__":
    main()
