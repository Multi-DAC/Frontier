"""Hubbell Spring creep profile -- WIDER. Day 196 evening, second pass.

Clayton: "I think that may be slightly too thin, let's try wider."

The first profile ran ONE aperture (along +/-60 km, normal +/-40 km, strike N10E) and
got 14 stations, 11 west / 3 east, and an honest bound of ~1.0 mm/yr on a creep step.
That is thin. This asks the same question across the aperture and strike space instead
of at one arbitrary point in it, and it reports the thing that actually matters:

    DOES THE BOUND EVER GET TIGHT ENOUGH TO MEAN ANYTHING?

Three sweeps:
  A. ALONG-STRIKE aperture  -- adds stations at the SAME fault-normal distances. This is
     the widening that helps: more samples of the same step, no new physics imported.
  B. ACROSS-STRIKE aperture -- adds stations far from the trace. Helps the mean, but
     imports basin-wide gradient into a statistic that assumes flat+step. Reported
     separately BECAUSE it is the seductive one.
  C. STRIKE angle           -- a stated weakness of the first run: "does not cover a
     large strike error". Swept -30..+50 deg. If a step appears only at one strike, that
     is a finding about the fit, not the fault, unless the strike is independently right.

Every cell reports n, split, scatter, 2-sigma minimum detectable step, the observed step,
and BIC model selection. A cell with <2 independent sites on a side reports NO bound --
it does not report a null. Co-located pairs (<3 km apart) are collapsed to ONE independent
site before any power number is computed; that correction is what took the first run's
bound from 0.845 to 0.998 mm/yr and it is applied everywhere here.
"""
import math, json, sys
from collections import defaultdict

SRC = "work/midas_NA_true.txt"
R_EARTH = 6371.0
LAT0, LON0 = 34.90, -106.53
MIN_DUR = 3.0
COLOC_KM = 3.0
CREEP_TEST = 1.0


def load():
    out = []
    for ln in open(SRC, encoding="utf-8", errors="replace"):
        f = ln.split()
        if len(f) < 27:
            continue
        try:
            lat = float(f[24]); lon = float(f[25])
            if lon > 180:
                lon -= 360.0
            out.append({"site": f[0], "dur": float(f[4]),
                        "ve": float(f[8])*1000, "vn": float(f[9])*1000, "vu": float(f[10])*1000,
                        "lat": lat, "lon": lon})
        except ValueError:
            continue
    return out


STATIONS = [s for s in load() if s["dur"] >= MIN_DUR]
KX = 111.320*math.cos(math.radians(LAT0))
KY = 110.574


def project(strike_deg):
    th = math.radians(strike_deg)
    pe, pn = math.sin(th), math.cos(th)
    ne, nn = math.cos(th), -math.sin(th)
    rows = []
    for s in STATIONS:
        dx = (s["lon"]-LON0)*KX
        dy = (s["lat"]-LAT0)*KY
        rows.append({"site": s["site"], "lat": s["lat"], "lon": s["lon"],
                     "along": dx*pe + dy*pn, "norm": dx*ne + dy*nn,
                     "vpar": s["ve"]*pe + s["vn"]*pn, "vu": s["vu"]})
    return rows


def independent_sites(rs):
    """Collapse co-located clusters (<COLOC_KM) to one. Returns cluster count only --
    the fit still uses every station; this is purely the honest N for the power number."""
    used = [False]*len(rs)
    clusters = 0
    for i in range(len(rs)):
        if used[i]:
            continue
        clusters += 1
        used[i] = True
        for j in range(i+1, len(rs)):
            if used[j]:
                continue
            d = math.hypot((rs[i]["lon"]-rs[j]["lon"])*KX, (rs[i]["lat"]-rs[j]["lat"])*KY)
            if d < COLOC_KM:
                used[j] = True
    return clusters


def bic_models(rs):
    if len(rs) < 6:
        return None
    x = [r["norm"] for r in rs]; y = [r["vpar"] for r in rs]
    n = len(x)
    def rss(pred): return sum((y[i]-pred[i])**2 for i in range(n))
    m0 = sum(y)/n
    r0 = rss([m0]*n)
    xb = sum(x)/n; yb = sum(y)/n
    sxx = sum((xi-xb)**2 for xi in x) or 1e-12
    b = sum((x[i]-xb)*(y[i]-yb) for i in range(n))/sxx
    a = yb-b*xb
    r1 = rss([a+b*xi for xi in x])
    A = [[1.0, xi, 1.0 if xi >= 0 else 0.0] for xi in x]
    M = [[sum(A[k][i]*A[k][j] for k in range(n)) for j in range(3)]
         + [sum(A[k][i]*y[k] for k in range(n))] for i in range(3)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r_: abs(M[r_][i]))
        M[i], M[p] = M[p], M[i]
        if abs(M[i][i]) < 1e-12:
            return None
        for r_ in range(3):
            if r_ == i:
                continue
            f = M[r_][i]/M[i][i]
            for c in range(i, 4):
                M[r_][c] -= f*M[i][c]
    p2 = [M[i][3]/M[i][i] for i in range(3)]
    r2 = rss([p2[0]+p2[1]*x[i]+p2[2]*A[i][2] for i in range(n)])
    def bic(r, k): return n*math.log(max(r, 1e-12)/n) + k*math.log(n)
    cand = [("M0_flat", bic(r0, 1)), ("M1_linear", bic(r1, 2)), ("M2_step", bic(r2, 3))]
    win = min(cand, key=lambda t: t[1])
    return {"winner": win[0], "dBIC_step_minus_best_other":
            round(bic(r2, 3) - min(bic(r0, 1), bic(r1, 2)), 2),
            "step_est_mm_yr": round(p2[2], 3)}


def cell(strike, along_hw, norm_hw, drop_nmab=True):
    rs = [r for r in project(strike)
          if abs(r["along"]) <= along_hw and abs(r["norm"]) <= norm_hw]
    if drop_nmab:
        rs = [r for r in rs if r["site"] != "NMAB"]
    out = {"strike_deg": strike, "along_hw_km": along_hw, "norm_hw_km": norm_hw,
           "n": len(rs)}
    if len(rs) < 4:
        out["verdict"] = "NO BOUND -- too few stations"
        return out
    west = [r for r in rs if r["norm"] < 0]
    east = [r for r in rs if r["norm"] >= 0]
    nw = independent_sites(west); ne_ = independent_sites(east)
    out.update({"n_west": len(west), "n_east": len(east),
                "indep_west": nw, "indep_east": ne_})
    vs = [r["vpar"] for r in rs]
    mean = sum(vs)/len(vs)
    sd = math.sqrt(sum((v-mean)**2 for v in vs)/(len(vs)-1))
    out["scatter_mm_yr"] = round(sd, 3)
    if nw >= 2 and ne_ >= 2:
        sem = sd*math.sqrt(1/nw + 1/ne_)
        mw = sum(r["vpar"] for r in west)/len(west)
        me = sum(r["vpar"] for r in east)/len(east)
        out["min_detect_step_2sig"] = round(2*sem, 3)
        out["observed_step_mm_yr"] = round(me-mw, 3)
        out["step_over_sigma"] = round((me-mw)/sem, 2) if sem else None
        out["detects_1mm_creep"] = bool(2*sem < CREEP_TEST)
        out["verdict"] = ("STEP" if abs(me-mw) > 2*sem else "NULL")
    else:
        out["min_detect_step_2sig"] = None
        out["verdict"] = "NO BOUND -- <2 independent sites on a side"
    m = bic_models(rs)
    if m:
        out["bic"] = m
    return out


res = {"note": "NMAB excluded throughout (aquifer compaction, defended in the addendum). "
               "Power N is INDEPENDENT SITES after collapsing <3 km pairs.",
       "baseline_first_run": cell(10.0, 60.0, 40.0)}

res["A_along_strike_sweep"] = [cell(10.0, hw, 40.0)
                               for hw in (40, 60, 80, 100, 130, 160, 200, 260)]
res["B_across_strike_sweep"] = [cell(10.0, 100.0, nw)
                                for nw in (15, 20, 30, 40, 60, 80, 110, 150)]
res["C_strike_sweep"] = [cell(st, 100.0, 40.0)
                         for st in (-30, -20, -10, 0, 10, 20, 30, 40, 50)]

# The question the sweep exists to answer.
bounded = [c for grp in ("A_along_strike_sweep", "B_across_strike_sweep", "C_strike_sweep")
           for c in res[grp] if c.get("min_detect_step_2sig")]
best = min(bounded, key=lambda c: c["min_detect_step_2sig"]) if bounded else None
res["tightest_bound_anywhere_in_sweep"] = best
res["any_cell_showing_a_step"] = [c for c in bounded if c["verdict"] == "STEP"]
res["cells_selecting_M2_step_by_BIC"] = [
    c for c in bounded if c.get("bic", {}).get("winner") == "M2_step"]

print(json.dumps(res, indent=2))
for k in ("A_along_strike_sweep", "B_across_strike_sweep", "C_strike_sweep"):
    print(f"\n== {k}", file=sys.stderr)
    for c in res[k]:
        print(f"  strike{c['strike_deg']:>5} along{c['along_hw_km']:>5} norm{c['norm_hw_km']:>5} "
              f"n={c['n']:>3} W/E={c.get('indep_west','-')}/{c.get('indep_east','-')} "
              f"sd={c.get('scatter_mm_yr','-'):>6} bound={c.get('min_detect_step_2sig')} "
              f"obs={c.get('observed_step_mm_yr')} {c['verdict']} "
              f"{c.get('bic',{}).get('winner','')}", file=sys.stderr)
print(f"\nTIGHTEST: {json.dumps(best)}", file=sys.stderr)
print(f"STEPS FOUND: {len(res['any_cell_showing_a_step'])}", file=sys.stderr)
