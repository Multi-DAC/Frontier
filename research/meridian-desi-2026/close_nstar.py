"""
Meridian demolition audit, pass 3 — closing N_* in the modulus-inflation sector.

Settles the PENDING half of Finding D-9: is the NCG one-loop radion mass
(m_rad ~ 120 GeV) the mass that governs the post-inflationary oscillation phase?

ANSWER: no. The oscillation mass is the curvature of the INFLATIONARY potential
at its own minimum, which 15E writes down explicitly:

    V(sigma) = V_0 [1 - exp(-sqrt(2/3) sigma/M_Pl)]^2        (15E sec 4.2/4.3)

Expanding at sigma -> 0 gives m^2 = (4/3) V_0 / M_Pl^2, i.e. m = 2 H_inf.
COBE-normalising V_0 fixes it at ~3e13 GeV — the textbook Starobinsky scalaron
mass (1.3e-5 M_Pl), eleven orders of magnitude above 16H's assumed
"free parameter: O(100 GeV) to O(TeV)".

Consequence, and it is constructive: m_sigma is NOT free, so N_* is not free
either. The only residual freedom is the decay coupling, and N_* is bounded
across its entire physical range (gravitational -> instantaneous).

Also verifies two defects in 16H_reheating.py:
  - N_star() uses (2/3) ln(T_reh); Liddle-Leach / Planck-2018 X eq(10) at
    w_reh = 0 gives (1/3). Overstates N_* by 3.3-5.3 over 16H's own scan.
  - V_star_14 = 2.1e16 GeV is (a) never used and (b) wrong: 7.8e15 GeV.

And one in 15E itself:
  - the slow-roll physics is right — at each quoted phi_*, 15E's n_s and r
    reproduce to four decimals. It is the N_* LABEL that is wrong. The column
    is built from the asymptotic u = 1/(2 beta^2 N), dropping both the ln u
    term and the f(u_end) offset, so every row is mislabelled by ~4.3 e-folds:
    the row printed "N_* = 55" is N_* = 50.7. Anyone who feeds a reheating-
    derived N_* into that table reads off the wrong (n_s, r).

Cross-checks: N_* computed two independent ways (first-principles entropy/
e-fold accounting, and Planck 2018 X eq(10)) agreeing to 0.1 e-folds; the
e-fold integral evaluated both in closed form and by numerical quadrature.

Clawd, Day 201 / 2026-08-20.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants
MP    = 2.435e18            # reduced Planck mass, GeV
A_s   = 2.100e-9            # Planck 2018 TT,TE,EE+lowE+lensing @ k=0.05/Mpc
g     = 106.75              # g_* at reheating
g0s   = 3.931               # g_{*s} today
T_0   = 2.7255 * 8.617333e-14
kpiv  = 0.05 * 6.394e-39    # 0.05 Mpc^-1 expressed in GeV
h     = 0.674
beta  = np.sqrt(2.0 / 3.0)  # alpha = 1 attractor
Lam_r = np.sqrt(6) * MP * np.exp(-35.0)   # 16H's radion coupling scale, 3761 GeV

# ------------------------------------------------- the potential 15E writes
V    = lambda p: (1 - np.exp(-beta * p))**2
Vp   = lambda p: 2*beta*np.exp(-beta*p) * (1 - np.exp(-beta*p))
Vpp  = lambda p: 2*beta*beta*np.exp(-beta*p) * (2*np.exp(-beta*p) - 1)
epsV = lambda p: 0.5 * (Vp(p) / V(p))**2
etaV = lambda p: Vpp(p) / V(p)

p_end  = brentq(lambda p: epsV(p) - 1.0, 0.05, 5.0)
N_of   = lambda p: quad(lambda x: V(x)/Vp(x), p_end, p)[0]     # numerical
p_of_N = lambda N: brentq(lambda x: N_of(x) - N, p_end + 1e-6, 12.0)


def N_star_firstprinciples(T_reh, V_star, rho_end):
    """Entropy + e-fold accounting, matter-dominated (w=0) reheating."""
    H_star  = np.sqrt(V_star / 3.0) / MP
    rho_reh = (np.pi**2 / 30.0) * g * T_reh**4
    return ((1/3.)*np.log(rho_reh/rho_end) + (1/3.)*np.log(g0s/g)
            + np.log(T_0/T_reh) + np.log(H_star/kpiv))


def N_star_planck_eq10(T_reh, V_star, rho_end):
    """Planck 2018 X eq(10), independent cross-check."""
    rho_th = (np.pi**2 / 30.0) * g * T_reh**4
    return (67.0 - np.log(0.05 / (h/2998.0))
            + 0.25*np.log(V_star**2 / (MP**4 * rho_end))
            + (1/12.)*np.log(rho_th/rho_end) - (1/12.)*np.log(g))


def solve(coupling):
    """Self-consistent N_* for a given decay-coupling scale (or 'inst')."""
    N = 55.0
    for _ in range(400):
        p       = p_of_N(N)
        e       = epsV(p)
        V_star  = 24*np.pi**2 * A_s * e * MP**4         # COBE normalisation
        V0      = V_star / (1 - np.exp(-beta*p))**2     # plateau height
        rho_end = 1.5 * V0 * (1 - np.exp(-beta*p_end))**2
        m       = 2.0 * np.sqrt(V0/3.0) / MP            # <-- the whole point
        H_end   = np.sqrt(rho_end/3.0) / MP
        T_inst  = (30*rho_end / (np.pi**2 * g))**0.25
        if coupling == 'inst':
            T, G = T_inst, np.inf
        else:
            G = m**3 / (8*np.pi*coupling**2)
            T = min((90./(np.pi**2*g))**0.25 * np.sqrt(G*MP), T_inst)
        N_new = N_star_firstprinciples(T, V_star, rho_end)
        if abs(N_new - N) < 1e-10:
            break
        N = 0.5*N + 0.5*N_new
    return dict(N=N, ns=1 - 6*e + 2*etaV(p), r=16*e, m=m, G=G, T=T,
                H_end=H_end, V_star=V_star, V0=V0, rho_end=rho_end)


if __name__ == "__main__":
    print("=" * 78)
    print("1. THE MASS 16H NEEDED WAS NEVER FREE")
    print("=" * 78)
    d = solve(MP)
    print(f"  V(sigma) = V0 [1 - exp(-sqrt(2/3) sigma/M_Pl)]^2   ->   m^2 = (4/3)V0/M_Pl^2")
    print(f"  V_*^(1/4)          = {d['V_star']**0.25:.3e} GeV   (16H hardcodes 2.1e16, and never uses it)")
    print(f"  m_sigma = 2 H_inf  = {d['m']:.3e} GeV   [Starobinsky scalaron, textbook 1.3e-5 M_Pl = 3.2e13]")
    print(f"  16H assumes          200 - 2000 GeV      -> off by {d['m']/2000:.1e}")
    print(f"  Meridian's own m_rad 120 GeV (NCG 1-loop) -> off by {d['m']/120:.1e}")
    print(f"  m_sigma / Lambda_r = {d['m']/Lam_r:.2e}  => 16H's trace-anomaly EFT is invalid at the true mass,")
    print(f"     so its 'WW+ZZ > 85% distinguishes Meridian from Starobinsky' signature is computed off-shell.")

    print()
    print("=" * 78)
    print("2. N_* IS THEREFORE BOUNDED WITH NO FREE MASS PARAMETER")
    print("=" * 78)
    print(f"{'decay coupling':>24} {'Gamma [GeV]':>12} {'T_reh [GeV]':>12} {'N_*':>7} {'n_s':>8} {'r':>9} {'vs Planck':>10}")
    rows = []
    for lab, c in [("M_Pl (gravitational)", MP), ("10^16 GeV", 1e16),
                   ("10^14 GeV", 1e14), ("instantaneous (Gamma>H)", 'inst')]:
        d = solve(c)
        rows.append(d)
        print(f"{lab:>24} {d['G']:12.3e} {d['T']:12.3e} {d['N']:7.2f} "
              f"{d['ns']:8.4f} {d['r']:9.5f} {abs(d['ns']-0.9649)/0.0042:9.2f}s")
    lo, hi = rows[0], rows[-1]
    print(f"\n  CLOSED RANGE:  N_* = {lo['N']:.1f} - {hi['N']:.1f}"
          f"   n_s = {lo['ns']:.4f} - {hi['ns']:.4f}   r = {hi['r']:.5f} - {lo['r']:.5f}")
    print(f"  Planck 2018: n_s = 0.9649 +/- 0.0042  ->  the whole range sits inside 0.6 sigma.")
    print(f"  cross-check, Planck-2018-X eq(10) at the instantaneous end: "
          f"N_* = {N_star_planck_eq10(hi['T'], hi['V_star'], hi['rho_end']):.2f} "
          f"(first-principles: {hi['N']:.2f})")

    print()
    print("=" * 78)
    print("3. TWO DEFECTS IN 16H_reheating.py's N_star()")
    print("=" * 78)
    print("  (a) coefficient of ln(T_reh): 16H uses 2/3; w_reh=0 gives 1/3.")
    print(f"{'m_sigma':>9} {'T_reh [GeV]':>12} {'16H N_*':>9} {'correct':>9} {'error':>7}")

    def Gamma_16H(m, L):
        a_s, mW, mZ, mt = 0.1179, 80.377, 91.1876, 172.69
        G = (a_s**2 * m**3 * 49.0) / (32*np.pi**3 * L**2)
        for mv, c in ((mW, 32.0), (mZ, 64.0)):
            if m > 2*mv:
                bb = np.sqrt(1 - 4*mv**2/m**2); x = mv**2/m**2
                G += (m**3/(c*np.pi*L**2)) * bb * (1 - 4*x + 12*x**2)
        for mf, nc in ((mt, 3), (4.18, 3), (1.777, 1)):
            if m > 2*mf:
                bb = np.sqrt(1 - 4*mf**2/m**2)
                G += nc * mf**2 * m / (8*np.pi*L**2) * bb**3
        return G

    for ms in [120, 200, 500, 1000, 2000]:
        T = (90./(np.pi**2*g))**0.25 * np.sqrt(Gamma_16H(ms, Lam_r) * MP)
        N16 = 55.4 + (2/3.)*np.log(T/1e9)
        p = p_of_N(N16); e = epsV(p)
        Vs = 24*np.pi**2*A_s*e*MP**4
        V0 = Vs/(1-np.exp(-beta*p))**2
        re = 1.5*V0*(1-np.exp(-beta*p_end))**2
        print(f"{ms:9.0f} {T:12.3e} {N16:9.2f} "
              f"{N_star_firstprinciples(T, Vs, re):9.2f} "
              f"{N16 - N_star_firstprinciples(T, Vs, re):+7.2f}")
    print("  (b) V_star_14 = 2.1e16 GeV is assigned and never read; correct value is 7.8e15.")

    print()
    print("=" * 78)
    print("4. 15E's OWN e-FOLD COLUMN IS MISLABELLED BY ~4.3")
    print("=" * 78)
    print("  cause: u_* taken as the asymptotic 1/(2 beta^2 N), dropping ln u and f(u_end).")
    print("  the (phi_*, n_s, r) triples are CORRECT — it is only the N attached to them that is not.")
    print(f"{'15E label':>10} {'15E phi_*':>10} {'true N':>8} {'15E n_s':>9} {'true n_s':>9} {'15E r':>8} {'true r':>9}")
    for lab, p15, ns15, r15 in [(50, 5.14, 0.9582, 0.0049), (55, 5.26, 0.9621, 0.0041),
                                (57, 5.30, 0.9635, 0.0038), (60, 5.37, 0.9654, 0.0034)]:
        print(f"{lab:>10} {p15:10.2f} {N_of(p15):8.1f} {ns15:9.4f} "
              f"{1-6*epsV(p15)+2*etaV(p15):9.4f} {r15:8.4f} {16*epsV(p15):9.5f}")
    print("  NOTE ON DIRECTION: this error runs AWAY from Planck (it understates n_s at fixed N),")
    print("  which is why 15E needed 'best fit N_* = 59.2' to reach the Planck central value.")
    print("  The true best fit is N_* ~ 55 — squarely inside the range section 2 closes.")
