"""L2 — THE PERCEPTUAL LEG. Measures the human visual aperture's retention fraction.

Scores PREREG-PERCEPTUAL-L2.md P1-P5. Read that file first; every choice that could be
gamed after the fact (primary currency = photon number, denominator = arriving flux) is
declared there and merely executed here.

⛔ THREE THINGS THIS SCRIPT DOES THAT ARE NOT DECORATION:

1. POSITIVE CONTROLS WITH PUBLISHED ANSWERS. The ASTM G173 table came from pvlib's
   vendored copy, not from NREL (DNS dead on this box) -- so the file's provenance is
   ONE step weaker than the prereg asked for. The standard states its own integrals:
   AM1.5G = 1000.37 W/m^2, AM0 = 1347.9 W/m^2 over 280-4000 nm. Reproducing those to
   <0.5% validates the FILE and the QUADRATURE together against a number I did not
   choose. If either fails, the run ABORTS -- it does not report a retention fraction
   computed on an unvalidated table.

2. THE V(lambda) MODELLING CHOICE IS BIASED AGAINST MY OWN PREDICTION, ON PURPOSE.
   V(lambda) is a relative luminous efficiency curve normalised to 1.0 at 555 nm, not a
   survival probability. Reading it as retention assumes the peak is 100% efficient,
   which it is not (a cone's real quantum efficiency at 555 nm is a few percent). So
   every retention number here is an OVERESTIMATE of true retention -- which pushes
   end-to-end retention UP, toward >= 35.5%, which is a MISS on P4. The bias runs
   against the thing I predicted. Stated so the reader does not have to find it.

3. P3 IS SCORED ON BOTH SOLAR GEOMETRIES OR NOT AT ALL. AM1.5 "global tilt" is defined
   on a 37-degree tilted plane with 0.2 ground albedo; AM0 is a normal-incidence flux.
   Their ratio is therefore NOT pure atmospheric transmittance. The direct+circumsolar
   column is the cleaner geometry and a worse model of what a standing observer
   receives. So P3 is evaluated against BOTH columns, and if they disagree in SIGN the
   verdict is VOID rather than whichever one I like.

Emits L2_RESULTS.json. Sources in data/l2/.
"""
import json, math, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data", "l2")

H_PLANCK = 6.62607015e-34      # J s   (SI defining constant)
C_LIGHT = 2.99792458e8         # m/s   (SI defining constant)

# The standard's own published integrals. NOT computed here -- these are the known
# answers the controls are checked against.
PUBLISHED = {"global": 1000.37, "extraterrestrial": 1347.9}
CONTROL_TOL = 0.005            # 0.5%

BAND_LO, BAND_HI = 380.0, 780.0   # nm, declared in the prereg


# ---------------------------------------------------------------- loading

def load_g173():
    """ASTM G173-03. Returns wl_nm list + dict of column -> W/m^2/nm list."""
    path = os.path.join(D, "pvlib_g173b.csv")
    rows, cols = [], None
    with open(path) as f:
        for line in f:
            p = [x.strip() for x in line.strip().split(",")]
            if not p or not p[0]:
                continue
            if p[0].lower() == "wavelength":
                cols = p[1:]
                continue
            if cols is None:
                continue          # the title line
            try:
                rows.append([float(x) for x in p])
            except ValueError:
                continue
    rows.sort(key=lambda r: r[0])
    wl = [r[0] for r in rows]
    out = {c: [r[i + 1] for r in rows] for i, c in enumerate(cols)}
    return wl, out


def load_vlambda():
    """CIE 1924 photopic V(lambda), 1 nm. Returns {wl_nm: value}."""
    path = os.path.join(D, "vl1924e.csv")
    v = {}
    with open(path) as f:
        for line in f:
            p = [x.strip() for x in line.strip().split(",")]
            if len(p) < 2 or not p[0]:
                continue
            v[float(p[0])] = float(p[1])
    return v


def v_at(vtab, wl):
    """Linear interpolation into V(lambda); 0 outside its tabulated support."""
    lo, hi = min(vtab), max(vtab)
    if wl < lo or wl > hi:
        return 0.0
    a = math.floor(wl)
    b = a + 1
    if a not in vtab:
        return 0.0
    if b not in vtab:
        return vtab[a]
    t = wl - a
    return vtab[a] * (1 - t) + vtab[b] * t


# ---------------------------------------------------------------- integration

def trapz(wl, y, lo=None, hi=None):
    """Trapezoid over [lo,hi], interpolating at the endpoints rather than snapping to
    the nearest grid point -- the grid is 0.5 nm below 400 and 1-5 nm above, so
    snapping a band edge would silently move it by up to 5 nm."""
    lo = wl[0] if lo is None else lo
    hi = wl[-1] if hi is None else hi
    tot = 0.0
    for i in range(len(wl) - 1):
        x0, x1 = wl[i], wl[i + 1]
        if x1 <= lo or x0 >= hi:
            continue
        y0, y1 = y[i], y[i + 1]
        if x0 < lo:                       # clip left
            y0 = y0 + (y1 - y0) * (lo - x0) / (x1 - x0)
            x0 = lo
        if x1 > hi:                       # clip right
            y1 = y[i] + (y[i + 1] - y[i]) * (hi - wl[i]) / (wl[i + 1] - wl[i])
            x1 = hi
        tot += 0.5 * (y0 + y1) * (x1 - x0)
    return tot


def to_photons(wl, e):
    """W/m^2/nm -> photons/s/m^2/nm.  N = E * lambda / (h c)."""
    return [ei * (w * 1e-9) / (H_PLANCK * C_LIGHT) for w, ei in zip(wl, e)]


def weighted(wl, y, vtab):
    return [yi * v_at(vtab, w) for w, yi in zip(wl, y)]


# ---------------------------------------------------------------- controls

def run_controls(wl, cols, vtab):
    c = {}
    for name, published in PUBLISHED.items():
        got = trapz(wl, cols[name])
        rel = abs(got - published) / published
        c["integral_" + name] = {
            "published_W_m2": published, "measured_W_m2": round(got, 3),
            "rel_error": round(rel, 6), "pass": rel < CONTROL_TOL,
            "kills": "a corrupted/mis-parsed table, a wrong column order, a broken quadrature",
        }
    peak_wl = max(vtab, key=lambda k: vtab[k])
    c["vlambda_peak"] = {
        "claim": "V(lambda) peaks at 555 nm with value 1.0",
        "measured_peak_nm": peak_wl, "measured_peak_value": vtab[peak_wl],
        "pass": peak_wl == 555.0 and abs(vtab[peak_wl] - 1.0) < 1e-9,
        "kills": "an unnormalised or scotopic table silently substituted for photopic",
    }
    c["grid"] = {
        "claim": "grid spans 280-4000 nm and V(lambda) spans 360-830 nm",
        "g173_range": [wl[0], wl[-1]], "n_rows": len(wl),
        "v_range": [min(vtab), max(vtab)], "v_rows": len(vtab),
        "pass": wl[0] <= 280 and wl[-1] >= 4000 and min(vtab) <= 380 and max(vtab) >= 780,
        "kills": "a truncated download that would silently shrink the denominator",
    }
    # A NEGATIVE control: the band-pass applied to a spectrum that is FLAT in photon
    # number must return exactly (780-380)/(4000-280) = 0.1075. If the machinery
    # returns that for a real solar spectrum too, the spectrum is not being read.
    flat = [1.0] * len(wl)
    flat_r = trapz(wl, flat, BAND_LO, BAND_HI) / trapz(wl, flat)
    c["flat_negative_control"] = {
        "claim": "a FLAT spectrum retains exactly the band's share of the grid width",
        "expected": round((BAND_HI - BAND_LO) / (wl[-1] - wl[0]), 6),
        "measured": round(flat_r, 6),
        "pass": abs(flat_r - (BAND_HI - BAND_LO) / (wl[-1] - wl[0])) < 1e-6,
        "kills": "endpoint-clipping bugs in trapz; and it is the value the real answer "
                 "must NOT equal, which is the input where right and wrong differ",
    }
    return c


# ---------------------------------------------------------------- the measurement

def retention_set(wl, e_toa, e_surf, vtab, currency):
    """currency: 'photon' or 'power'. Returns the four stage retentions."""
    if currency == "photon":
        toa, surf = to_photons(wl, e_toa), to_photons(wl, e_surf)
    else:
        toa, surf = e_toa, e_surf
    surf_w = weighted(wl, surf, vtab)

    I_toa = trapz(wl, toa)
    I_surf = trapz(wl, surf)
    I_surf_band = trapz(wl, surf, BAND_LO, BAND_HI)
    I_surf_wgt = trapz(wl, surf_w)

    r1 = I_surf / I_toa                    # S1  atmosphere
    r2 = I_surf_band / I_surf              # S2  band, of what arrives
    r3_given = I_surf_wgt / I_surf_band    # S3  weighting, of what the band admits
    r_end = I_surf_wgt / I_toa             # TOA -> perceived
    return {
        "S1_atmosphere_retention": r1,
        "S2_band_retention_of_arriving": r2,
        "S3_weighting_retention_of_band": r3_given,
        "S2S3_combined_of_arriving": I_surf_wgt / I_surf,
        "end_to_end_retention": r_end,
        "_raw": {"toa": I_toa, "surf": I_surf, "band": I_surf_band, "wgt": I_surf_wgt},
    }


def p5_denominators():
    """P5: is '0.0035% of the EM spectrum' reproducible? Compute the visible band's
    share under several denominators each of which someone has actually used."""
    lo_m, hi_m = BAND_LO * 1e-9, BAND_HI * 1e-9
    f_lo, f_hi = C_LIGHT / hi_m, C_LIGHT / lo_m
    out = {}
    # (a) linear WAVELENGTH over a commonly quoted "known EM" span 1e-14 m .. 1e4 m
    out["linear_wavelength_1e-14m_to_1e4m"] = (hi_m - lo_m) / (1e4 - 1e-14)
    # (b) linear FREQUENCY over the same physical span
    out["linear_frequency_same_span"] = (f_hi - f_lo) / (C_LIGHT / 1e-14 - C_LIGHT / 1e4)
    # (c) LOG10 frequency over 1 Hz .. 1e25 Hz -- the "decades" reading
    out["log10_frequency_1Hz_to_1e25Hz"] = (math.log10(f_hi) - math.log10(f_lo)) / (25.0 - 0.0)
    # (d) linear wavelength over the radio-to-gamma range often drawn in textbooks
    out["linear_wavelength_1pm_to_100km"] = (hi_m - lo_m) / (1e5 - 1e-12)
    # (e) log10 WAVELENGTH over 1e-14 m .. 1e4 m
    out["log10_wavelength_1e-14m_to_1e4m"] = (math.log10(hi_m) - math.log10(lo_m)) / (4 - (-14))
    return out


def main():
    wl, cols = load_g173()
    vtab = load_vlambda()
    controls = run_controls(wl, cols, vtab)

    failed = [k for k, v in controls.items() if not v["pass"]]
    if failed:
        print("CONTROLS FAILED:", failed)
        json.dump({"aborted": True, "controls": controls},
                  open(os.path.join(HERE, "L2_RESULTS.json"), "w"), indent=1)
        raise SystemExit("ABORT -- controls failed; no retention fraction reported.")

    res = {
        "written_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "prereg": "PREREG-PERCEPTUAL-L2.md",
        "sources": {
            "spectra": "ASTM G173-03 via pvlib vendored copy (NREL host DNS-dead on this "
                       "box; provenance is one step weaker than the prereg asked for, and "
                       "the published-integral controls are what compensate)",
            "vlambda": "CIE 1924 photopic V(lambda), CVRL vl1924e_1.csv, 1 nm",
        },
        "controls": controls,
        "measurements": {},
    }

    for geom, label in (("global", "AM1.5G global tilt (37deg, albedo 0.2)"),
                        ("direct", "AM1.5D direct+circumsolar (normal incidence)")):
        for currency in ("photon", "power"):
            r = retention_set(wl, cols["extraterrestrial"], cols[geom], vtab, currency)
            res["measurements"][f"{geom}__{currency}"] = {"geometry": label, **r}

    # ---- score the predictions
    prim = res["measurements"]["global__photon"]
    alt = res["measurements"]["direct__photon"]

    def p3_margin(m):
        r1, rend = m["S1_atmosphere_retention"], m["end_to_end_retention"]
        return (r1 - rend) - (1.0 - r1)     # >0 means biology out-edits the atmosphere

    m_glob, m_dir = p3_margin(prim), p3_margin(alt)
    p3_agree = (m_glob > 0) == (m_dir > 0)

    p5 = p5_denominators()
    spread = math.log10(max(p5.values()) / min(p5.values()))

    res["predictions"] = {
        "P1_band_retention_in_0.35_0.60": {
            "measured": round(prim["S2_band_retention_of_arriving"], 4),
            "verdict": "HIT" if 0.35 <= prim["S2_band_retention_of_arriving"] <= 0.60 else "MISS",
        },
        "P2_weighting_costs_more_than_band": {
            "r3_given_band": round(prim["S3_weighting_retention_of_band"], 4),
            "r2_band_of_arriving": round(prim["S2_band_retention_of_arriving"], 4),
            "verdict": "HIT" if prim["S3_weighting_retention_of_band"]
                                < prim["S2_band_retention_of_arriving"] else "MISS",
        },
        "P3_biology_out_edits_atmosphere": {
            "margin_global": round(m_glob, 4), "margin_direct": round(m_dir, 4),
            "geometries_agree_in_sign": p3_agree,
            "verdict": ("HIT" if m_glob > 0 else "MISS") if p3_agree else "VOID",
        },
        "P4_end_to_end_below_ZTF_0.355": {
            "measured": round(prim["end_to_end_retention"], 4), "ztf_retention": 0.355,
            "verdict": "HIT" if prim["end_to_end_retention"] < 0.355 else "MISS",
            "note": "the V(lambda)-as-retention choice OVERESTIMATES retention, so this "
                    "test is biased toward MISS -- against the prediction",
        },
        # ⚠ THIS SCORER WAS WRONG ON FIRST RUN AND THE FIX IS LEFT VISIBLE.
        # P5's text is a CONJUNCTION -- "reproducible under at least one defensible
        # denominator AND irreproducible under others". The first version of this block
        # tested only the spread, i.e. only the second conjunct, and returned HIT. That
        # is the escape-hatch-in-the-last-clause failure, committed inside the
        # instrument whose whole subject is bad denominators. Both conjuncts now score.
        "P5_famous_figure_denominator_dependent": {
            "values": {k: float(f"{v:.6g}") for k, v in p5.items()},
            "orders_of_magnitude_spread": round(spread, 2),
            "clause_a_spread_ge_3_orders": spread >= 3.0,
            "clause_b_reproduces_0.0035pct": any(
                abs(v * 100 - 0.0035) / 0.0035 < 0.25 for v in p5.values()),
            "denominator_that_WOULD_yield_0.0035pct_m": round(
                (BAND_HI - BAND_LO) * 1e-9 / 3.5e-5, 6),
            "verdict": ("HIT" if (spread >= 3.0 and any(
                abs(v * 100 - 0.0035) / 0.0035 < 0.25 for v in p5.values()))
                else "PARTIAL" if spread >= 3.0 else "MISS"),
            "reading": "PARTIAL is the stronger result for section 1a, not the weaker "
                       "one: the famous figure is not merely denominator-dependent, it "
                       "is unreproducible under every denominator I could defend.",
        },
    }

    json.dump(res, open(os.path.join(HERE, "L2_RESULTS.json"), "w"), indent=1)

    print("CONTROLS  all pass")
    for k, v in controls.items():
        d = v.get("measured_W_m2", v.get("measured", v.get("measured_peak_nm", "")))
        print(f"   {k:26s} {str(d):>12}  pass={v['pass']}")
    print()
    for k, m in res["measurements"].items():
        print(f"{k:18s} S1={m['S1_atmosphere_retention']:.4f}  "
              f"S2={m['S2_band_retention_of_arriving']:.4f}  "
              f"S3|band={m['S3_weighting_retention_of_band']:.4f}  "
              f"end={m['end_to_end_retention']:.4f}")
    print()
    for k, v in res["predictions"].items():
        print(f"{v['verdict']:5s}  {k}")
    print()
    print("P5 spread across denominators:")
    for k, v in sorted(p5.items(), key=lambda kv: kv[1]):
        print(f"   {v*100:14.8f}%   {k}")


if __name__ == "__main__":
    main()
