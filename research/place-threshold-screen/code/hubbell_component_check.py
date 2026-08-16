"""Hubbell Spring -- THE COMPONENT CHECK. The one that should have run first.

USGS Qfaults, pulled tonight, on the Hubbell Spring fault:

    slip_sense = "Normal"     slip_rate = "Between 0.2 and 1.0 mm/yr"   length = 74 km

Last night's discriminator (hubbell_creep_profile.py) tested for a step in FAULT-PARALLEL
velocity. Fault-parallel offset is the signature of STRIKE-SLIP creep. On a pure normal
fault the fault-parallel component is expected to be flat whether or not the fault is
doing anything at all -- so the null it returned was guaranteed by the choice of
component, not earned by the data. The script even computed `vnorm` per station and then
never fitted it.

This runs the same machinery on the components the fault's own kinematics predict:

    FAULT-NORMAL (extension across the trace)  -- the horizontal signature of normal slip
    VERTICAL     (footwall up / hanging wall down) -- the other half of it

and it compares each bound against a PREDICTED value rather than against zero, because
the second thing Qfaults handed over is a number to predict with: 0.2-1.0 mm/yr, mid 0.6.

That comparison is the whole point. A bound of 1.0 mm/yr on an expected signal of 0.6
mm/yr is not a null result. It is a POWER FAILURE, and reporting it as a refutation --
which is what I did last night -- inverts the finding.
"""
import math, json, sys

SRC = "work/midas_NA_true.txt"
LAT0, LON0 = 34.90, -106.53
STRIKE = 10.0
MIN_DUR = 3.0
COLOC_KM = 3.0
PREDICTED_SLIP_MM_YR = 0.6          # Qfaults mid of "Between 0.2 and 1.0 mm/yr"
PREDICTED_RANGE = (0.2, 1.0)
FAULT_LENGTH_KM = 74.0              # Qfaults total_fault_length
KX = 111.320*math.cos(math.radians(LAT0)); KY = 110.574


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
            if float(f[4]) < MIN_DUR:
                continue
            out.append({"site": f[0], "ve": float(f[8])*1000, "vn": float(f[9])*1000,
                        "vu": float(f[10])*1000, "lat": lat, "lon": lon})
        except ValueError:
            continue
    return out


def swath(along_hw, norm_hw, strike=STRIKE, drop_nmab=True):
    th = math.radians(strike)
    pe, pn = math.sin(th), math.cos(th)
    ne, nn = math.cos(th), -math.sin(th)
    rows = []
    for s in load():
        if drop_nmab and s["site"] == "NMAB":
            continue
        dx = (s["lon"]-LON0)*KX; dy = (s["lat"]-LAT0)*KY
        a = dx*pe + dy*pn
        n = dx*ne + dy*nn
        if abs(a) > along_hw or abs(n) > norm_hw:
            continue
        rows.append({"site": s["site"], "lat": s["lat"], "lon": s["lon"],
                     "along": a, "norm": n,
                     "vpar": s["ve"]*pe + s["vn"]*pn,
                     "vnorm": s["ve"]*ne + s["vn"]*nn,
                     "vu": s["vu"]})
    return rows


def indep(rs):
    used = [False]*len(rs); c = 0
    for i in range(len(rs)):
        if used[i]:
            continue
        c += 1; used[i] = True
        for j in range(i+1, len(rs)):
            if not used[j] and math.hypot((rs[i]["lon"]-rs[j]["lon"])*KX,
                                          (rs[i]["lat"]-rs[j]["lat"])*KY) < COLOC_KM:
                used[j] = True
    return c


def component_test(rows, key, label):
    west = [r for r in rows if r["norm"] < 0]
    east = [r for r in rows if r["norm"] >= 0]
    nw, ne_ = indep(west), indep(east)
    vs = [r[key] for r in rows]
    if len(vs) < 4:
        return {"component": label, "verdict": "NO BOUND -- too few stations"}
    m = sum(vs)/len(vs)
    sd = math.sqrt(sum((v-m)**2 for v in vs)/(len(vs)-1))
    out = {"component": label, "n": len(rows), "indep_west": nw, "indep_east": ne_,
           "scatter_mm_yr": round(sd, 3)}
    if nw < 2 or ne_ < 2:
        out["verdict"] = "NO BOUND -- <2 independent sites on a side"
        return out
    sem = sd*math.sqrt(1/nw + 1/ne_)
    mw = sum(r[key] for r in west)/len(west)
    me = sum(r[key] for r in east)/len(east)
    diff = me - mw
    # TWO hypotheses, each tested against the OBSERVATION -- not against each other and
    # not against zero-by-default. The first version of this function divided the
    # prediction by sigma, which tests "is 0.6 far from zero", a question about the
    # instrument's units rather than about the fault. It reported "prediction excluded"
    # for a cell where observed 0.25 sits 1.2 sigma from the predicted 0.6.
    z_null = abs(diff - 0.0)/sem if sem else float("inf")
    z_pred = abs(diff - PREDICTED_SLIP_MM_YR)/sem if sem else float("inf")
    excl_null = z_null > 2.0
    excl_pred = z_pred > 2.0
    out.update({"observed_diff_mm_yr": round(diff, 3),
                "sigma_mm_yr": round(sem, 3),
                "min_detect_2sig": round(2*sem, 3),
                "predicted_mm_yr": PREDICTED_SLIP_MM_YR,
                "z_vs_zero": round(z_null, 2),
                "z_vs_prediction": round(z_pred, 2),
                "excludes_zero": bool(excl_null),
                "excludes_prediction": bool(excl_pred),
                "CAN_THE_INSTRUMENT_SEPARATE_THEM":
                    bool(2*sem < PREDICTED_SLIP_MM_YR)})
    if not excl_null and not excl_pred:
        out["verdict"] = (f"UNDECIDED -- observed {diff:+.2f} is consistent with BOTH zero "
                          f"({z_null:.1f}s) and the published {PREDICTED_SLIP_MM_YR} "
                          f"({z_pred:.1f}s). No refutation is available here.")
    elif excl_pred and not excl_null:
        out["verdict"] = (f"REFUTES PUBLISHED RATE -- observed {diff:+.2f} excludes "
                          f"{PREDICTED_SLIP_MM_YR} at {z_pred:.1f}s, consistent with zero")
    elif excl_null and not excl_pred:
        out["verdict"] = (f"SUPPORTS PUBLISHED RATE -- observed {diff:+.2f} excludes zero "
                          f"at {z_null:.1f}s, consistent with {PREDICTED_SLIP_MM_YR}")
    else:
        out["verdict"] = (f"observed {diff:+.2f} excludes BOTH zero ({z_null:.1f}s) and "
                          f"{PREDICTED_SLIP_MM_YR} ({z_pred:.1f}s) -- something else")
    return out


def stations_needed(sd, target, split=0.5):
    """Independent sites per side needed for a 2-sigma detection of `target`."""
    for n in range(2, 400):
        nw = max(2, int(n*split)); ne_ = max(2, n-nw)
        if 2*sd*math.sqrt(1/nw + 1/ne_) < target:
            return {"total_indep_sites": n, "west": nw, "east": ne_}
    return None


APERTURES = [("fault-scale (+/-37 km = half the mapped 74 km trace)", 37.0, 40.0),
             ("last night's run (+/-60 km)", 60.0, 40.0),
             ("wide (+/-100 km)", 100.0, 40.0),
             ("rift-scale (+/-260 km -- NO LONGER THIS FAULT)", 260.0, 40.0)]

res = {"fault_facts_from_qfaults": {
           "slip_sense": "Normal", "slip_rate_class": "Between 0.2 and 1.0 mm/yr",
           "slip_rate_mid_mm_yr": PREDICTED_SLIP_MM_YR,
           "slip_rate_range_mm_yr": list(PREDICTED_RANGE),
           "total_fault_length_km": FAULT_LENGTH_KM,
           "max_honest_along_strike_halfwidth_km": FAULT_LENGTH_KM/2},
       "why_this_reruns": ("last night profiled FAULT-PARALLEL velocity; a normal fault's "
                           "interseismic signal is in FAULT-NORMAL and VERTICAL"),
       "apertures": []}

for label, ahw, nhw in APERTURES:
    rows = swath(ahw, nhw)
    blk = {"aperture": label, "along_hw_km": ahw, "norm_hw_km": nhw, "n": len(rows),
           "components": [component_test(rows, k, lab) for k, lab in
                          (("vnorm", "FAULT-NORMAL (extension) <- the right one"),
                           ("vu", "VERTICAL (footwall/hanging wall)"),
                           ("vpar", "fault-parallel (last night's, wrong for normal slip)"))]}
    res["apertures"].append(blk)

rows37 = swath(37.0, 40.0)
for key, lab in (("vnorm", "fault-normal"), ("vu", "vertical")):
    vs = [r[key] for r in rows37]
    m = sum(vs)/len(vs)
    sd = math.sqrt(sum((v-m)**2 for v in vs)/(len(vs)-1))
    res.setdefault("what_would_be_needed", {})[lab] = {
        "scatter_mm_yr": round(sd, 3),
        "to_detect_0.6_mm_yr": stations_needed(sd, PREDICTED_SLIP_MM_YR),
        "to_detect_0.2_mm_yr_lower_bound": stations_needed(sd, PREDICTED_RANGE[0]),
        "currently_have": {"indep_west": indep([r for r in rows37 if r["norm"] < 0]),
                           "indep_east": indep([r for r in rows37 if r["norm"] >= 0])}}

print(json.dumps(res, indent=2))
for blk in res["apertures"]:
    print(f"\n== {blk['aperture']}  n={blk['n']}", file=sys.stderr)
    for c in blk["components"]:
        print(f"   {c['component'][:52]:<52} obs={c.get('observed_diff_mm_yr')} "
              f"2sig={c.get('min_detect_2sig')} :: {c.get('verdict')}", file=sys.stderr)
print("\n== WHAT WOULD BE NEEDED", file=sys.stderr)
print(json.dumps(res["what_would_be_needed"], indent=2), file=sys.stderr)
