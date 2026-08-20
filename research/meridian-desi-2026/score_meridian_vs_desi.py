"""Score Meridian's 14I pre-registration (18 Mar 2026) against DESI arXiv:2607.27410.

Every number in README.md comes out of this file. Run it to reproduce.

The correlation rho is NOT assumed: it is recovered from the paper's own quoted
pivot values, two independent ways, via the CPL pivot identities.
"""
import numpy as np
from scipy.stats import chi2

# --- Meridian parameters, from 14I section 9 --------------------------------
C_KK = 2.454e-4          # +/- 0.827e-4
OM, ODE = 0.315, 0.685   # Planck 2018

def w_mer(z, zeta):
    """Meridian w(z) = -1 + 2*kappa_0 / [Omega_DE * E^2(z)]   (14I eq. 1.1)"""
    k0 = C_KK * ODE / (2 * zeta)
    return -1 + 2 * k0 / (ODE * (OM * (1 + z) ** 3 + ODE))

def cpl_project(zeta, zmax=2.33):
    """Least-squares CPL (w0, wa) that best mimics Meridian's w(z) over [0, zmax].

    This is NOT 14I section 1.4's w_a,eff = -0.232, which is the dw/dz tangent at
    z=0 and understates the effective wa by ~0.11 over the range DESI constrains.
    """
    z = np.linspace(0, zmax, 400)
    x = z / (1 + z)
    A = np.vstack([np.ones_like(x), x]).T
    return np.linalg.lstsq(A, w_mer(z, zeta), rcond=None)[0]

# --- rho recovered from the paper's pivot values ----------------------------
# CPL: Var(w0 + x*wa) minimised at x_p = -rho*s0/sa, with sigma(w_p) = s0*sqrt(1-rho^2)
def rho_from_pivot(s0, sa, zp, swp):
    xp = zp / (1 + zp)
    return -xp * sa / s0, -np.sqrt(max(0.0, 1 - (swp / s0) ** 2))

COMBOS = {
    # label: (mean, sigma, zp, sigma_wp)   -- all from arXiv:2607.27410 section VI.4.1
    "DESI BAO+LyaFS+CMB+DES-Dovekie": ((-0.821, -0.65), (0.054, 0.20), 0.32, 0.022),
    "DESI BAO+LyaFS+CMB (no SNe)   ": ((-0.54, -1.39), (0.20, 0.555), 0.55, 0.040),
}

def nsigma(point, mu, s, rho):
    C = np.array([[s[0] ** 2, rho * s[0] * s[1]], [rho * s[0] * s[1], s[1] ** 2]])
    d = np.asarray(point) - np.asarray(mu)
    c2 = float(d @ np.linalg.inv(C) @ d)
    return c2, float(np.sqrt(chi2.isf(max(chi2.sf(c2, 2), 1e-300), 1)))

if __name__ == "__main__":
    ZETA_JC = 9.64e-4        # 13B: the only root of the junction conditions at the stated brane params
    ZETA_ALT = 0.038         # 13B: the historical value, reachable with different brane params

    print("== rho recovered from the paper's own pivot numbers ==")
    rhos = {}
    for lab, (mu, s, zp, swp) in COMBOS.items():
        ra, rb = rho_from_pivot(s[0], s[1], zp, swp)
        rhos[lab] = (ra + rb) / 2
        print(f"  {lab}  rho(z_p)={ra:+.3f}  rho(sigma_wp)={rb:+.3f}  -> adopt {rhos[lab]:+.3f}")

    print("\n== Meridian's CPL projection vs its own tangent ==")
    for zmax in (1.0, 2.33, 3.0):
        w0, wa = cpl_project(ZETA_JC, zmax)
        print(f"  z <= {zmax:4.2f}: w0={w0:.3f}  wa={wa:+.3f}")
    print("  14I s1.4 tangent : w0=-0.755  wa=-0.232   <-- understates |wa| by ~0.11")
    print("  14I s7 criterion 2 disfavours Meridian if |wa| > 0.3 -- BELOW its own 0.344")

    print("\n== joint (w0, wa) test ==")
    for lab, (mu, s, _, _) in COMBOS.items():
        rho = rhos[lab]
        print(f"  -- {lab} (rho={rho:+.3f})")
        for tag, p in (
            ("Meridian JC, 14I tangent wa ", (-0.755, -0.232)),
            ("Meridian JC, projected wa   ", tuple(cpl_project(ZETA_JC))),
            ("LCDM                        ", (-1.0, 0.0)),
        ):
            c2, sg = nsigma(p, mu, s, rho)
            print(f"       {tag} chi2={c2:6.1f}  {sg:.1f} sigma")
        zs = np.logspace(-4, -0.5, 4000)
        c2b, zb = min((nsigma(tuple(cpl_project(z)), mu, s, rho)[0], z) for z in zs)
        w0b, wab = cpl_project(zb)
        _, sgb = nsigma((w0b, wab), mu, s, rho)
        print(f"       Meridian, zeta0 FREE         chi2={c2b:6.1f}  {sgb:.1f} sigma"
              f"   (zeta0={zb:.2e} -> w0={w0b:.3f}, wa={wab:+.3f})")

    print("\n== 13B's two roots ==")
    for z0 in (ZETA_JC, ZETA_ALT):
        print(f"  zeta0={z0:.3e} -> w0={w_mer(0.0, z0):.3f}")
