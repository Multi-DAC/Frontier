"""SECTION 14 — the noise floor the gravimetric bound was missing.

PAPER-00-ARCHITECTURE.md row 14 carries a computed number: a 350 g mass at 1 m is
2.34x a superconducting gravimeter's static floor. The row's own fence says that is
SENSITIVITY, NOT DETECTION, because the tidal / atmospheric / hydrological loading
terms were never computed. This computes them.

Everything here is either derived from constants in this file or quoted from a named
published measurement. No number is recalled. Units are carried explicitly, because
the whole failure mode of the original claim was a comparison against the wrong floor.

UNITS, stated once:
    1 Gal   = 1e-2  m/s^2
    1 uGal  = 1e-8  m/s^2
    1 nGal  = 1e-11 m/s^2
    1 nm/s^2 = 1e-9 m/s^2   =  100 nGal   =  0.1 uGal
"""
import json

G = 6.67430e-11          # CODATA 2018, m^3 kg^-1 s^-2
R_E = 6.371e6            # mean Earth radius, m
GM_MOON = 4.9028695e12   # m^3/s^2, DE440
GM_SUN = 1.32712440018e20
D_MOON = 3.844e8         # mean, m
D_SUN = 1.495978707e11   # 1 au, m

NM = 1e-9                # m/s^2 per nm/s^2
UGAL = 1e-8
NGAL = 1e-11


def in_(a, unit):
    return a / unit


def signal(mass_kg, r_m):
    """Newtonian attraction of a compact mass at distance r. No shielding assumed:
    an own-sector body still gravitates, which is the whole point of Branch B."""
    return G * mass_kg / r_m ** 2


def tide_amp(GM, d):
    """Peak radial tidal acceleration at the sub-body point, rigid Earth:
    dg = 2 G M R / d^3. The elastic response multiplies this by the gravimetric
    factor delta ~ 1.16 (Wahr-Dehant); we report both."""
    return 2 * GM * R_E / d ** 3


DELTA = 1.16             # gravimetric factor, degree-2, elastic Earth

out = {"units_note": "values reported in nm/s^2 and nGal; 1 nm/s^2 = 100 nGal"}

# ---- 1. THE SIGNAL, as row 14 states it -------------------------------------
sig = signal(0.350, 1.0)
out["signal_350g_at_1m"] = {"m_s2": sig, "nm_s2": in_(sig, NM), "nGal": in_(sig, NGAL)}

# ---- 2. THE EARTH, computed from first principles ---------------------------
tm, ts = tide_amp(GM_MOON, D_MOON), tide_amp(GM_SUN, D_SUN)
out["tide_rigid_lunar_nm_s2"] = in_(tm, NM)
out["tide_rigid_solar_nm_s2"] = in_(ts, NM)
out["tide_rigid_sum_nm_s2"] = in_(tm + ts, NM)
out["tide_elastic_sum_nm_s2"] = in_((tm + ts) * DELTA, NM)
out["tide_over_signal"] = (tm + ts) * DELTA / sig

# ---- 3. WHAT IS LEFT AFTER THE CORRECTIONS, from the literature -------------
# Every entry is a published, station-specific measurement. Source is carried WITH
# the number so a later reader cannot separate them.
CROSSLEY = ("Crossley, Murphy & Liang 2023, Geophys. J. Int. 232(2) 1031-1065, "
            "doi:10.1093/gji/ggac357 (SG at Apache Point Observatory, NM)")
ANTOKOLETZ = ("Antokoletz et al. 2024, Geophys. J. Int. 236(1) 88-98, "
              "doi:10.1093/gji/ggad371 (five European SG stations)")

floors = [
    dict(name="tidal-band residual noise, best case, narrowband",
         lo_uGal=0.017, hi_uGal=0.037, source=CROSSLEY,
         quote="residual noise 0.017-0.037 uGal (ETERNA, model AP1018mn, Series A-B)"),
    dict(name="mean error of fit after tidal + pressure correction, broadband",
         lo_uGal=1.5, hi_uGal=2.0, source=CROSSLEY,
         quote="the mean error of our fit remains between 1.5-2.0 uGal for our two data sets"),
    dict(name="departure of corrected residual from the hydrological model",
         lo_uGal=None, hi_uGal=4.0, source=CROSSLEY,
         quote="episodes in the corrected residuals that depart by up to 4 uGal from the "
               "hydrological models (after >90% of seasonal variance removed)"),
    dict(name="non-tidal ocean loading, coastal station Yebes",
         lo_uGal=0.2, hi_uGal=0.2, source=ANTOKOLETZ,
         quote="largest amplitude at Yebes (260 km from the Atlantic) with an RMS of 2 nm/s^2"),
    dict(name="inverted-barometer effect, most inland station Wettzell",
         lo_uGal=0.14, hi_uGal=0.14, source=ANTOKOLETZ,
         quote="the IB effect shows an RMS of 1.4 nm/s^2"),
]
for f in floors:
    hi = f["hi_uGal"] * UGAL
    f["hi_nm_s2"] = in_(hi, NM)
    f["hi_nGal"] = in_(hi, NGAL)
    f["floor_over_signal"] = hi / sig
    if f["lo_uGal"] is not None:
        f["lo_over_signal"] = f["lo_uGal"] * UGAL / sig
out["published_floors"] = floors

# ---- 4. THE INVERSION — what mass WOULD clear each floor at 1 m -------------
def mass_for(a, r=1.0):
    return a * r ** 2 / G

out["mass_to_clear_floor_kg_at_1m"] = {
    "best_narrowband_tidal_residual_0.017uGal": mass_for(0.017 * UGAL),
    "broadband_fit_error_1.5uGal": mass_for(1.5 * UGAL),
    "hydrological_departure_4uGal": mass_for(4.0 * UGAL),
}
# r^2 scaling, stated so the bound is not read as distance-free
out["mass_to_clear_best_floor_kg"] = {f"{r}m": mass_for(0.017 * UGAL, r) for r in (1, 3, 10, 30)}

# ---- 5. THE VERDICT ---------------------------------------------------------
best = 0.017 * UGAL
out["verdict"] = {
    "signal_nGal": in_(sig, NGAL),
    "best_published_residual_nGal": in_(best, NGAL),
    "signal_is_below_best_floor_by_factor": best / sig,
    "ruling": ("The 2.34x figure compared the signal to the instrument's STATIC RESOLUTION. "
               "Against the residual that survives tidal, atmospheric, ocean-loading and "
               "hydrological correction at the best-characterised SG site in the literature, "
               "the same signal is BELOW the floor. Row 14's own fence -- sensitivity, not "
               "detection -- is upheld, and the margin is now a number rather than a caveat."),
}

json.dump(out, open("GRAVIMETRIC_FLOOR.json", "w"), indent=1)

print(f"signal (350 g @ 1 m)          : {out['signal_350g_at_1m']['nGal']:.3f} nGal "
      f"= {out['signal_350g_at_1m']['nm_s2']:.5f} nm/s^2")
print(f"solid-earth tide (computed)   : {out['tide_elastic_sum_nm_s2']:.1f} nm/s^2 "
      f"= {out['tide_over_signal']:.3e} x the signal")
for f in floors:
    print(f"  floor: {f['name'][:52]:<52} {f['hi_nGal']:>9.0f} nGal  "
          f"= {f['floor_over_signal']:>8.1f} x signal   [{f['source'].split(',')[0]}]")
print(f"\nmass needed at 1 m to clear the BEST published residual: "
      f"{out['mass_to_clear_floor_kg_at_1m']['best_narrowband_tidal_residual_0.017uGal']:.2f} kg")
print(f"                          ... the broadband fit error   : "
      f"{out['mass_to_clear_floor_kg_at_1m']['broadband_fit_error_1.5uGal']:.1f} kg")
print(f"signal sits {out['verdict']['signal_is_below_best_floor_by_factor']:.1f}x BELOW the best floor")
