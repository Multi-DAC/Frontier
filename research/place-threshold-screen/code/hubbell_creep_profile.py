"""Hubbell Spring -- fault-normal creep profile. Day 196. THE discriminator.

The disc-fit (rift_gps_strain_tensor.py) measures strain averaged over a 50 km circle.
Fault creep is not that shape: it is a STEP in fault-parallel velocity localized within
a few km of the trace. A disc fit averages a step into a gentle ramp and cannot tell
the two apart. So this asks the question in the shape the answer would have.

Hubbell Spring is a west-dipping normal fault on the east side of the basin, striking
~N10E near the pin. Fault-parallel = N10E, fault-normal = N100E.

MODELS COMPARED on fault-parallel velocity v vs across-strike distance x:
   M0  v = c                     (nothing)
   M1  v = c + m*x               (distributed shear -- what a disc fit would see)
   M2  v = c + m*x + s*H(x)      (creep: a STEP at the trace, Fork 1's signature)
Selection by BIC, because M2 always fits at least as well and N is small.

THE POWER QUESTION IS ASKED FIRST AND IT IS ALLOWED TO END THE RUN. Before any model
is fitted, this reports how many stations sit within 20 km of the trace on EACH side
and the scatter of the field. If a step of the size creep would produce cannot be
distinguished from zero at this station density, the honest output is NOT a null --
it is "this network cannot answer", and the run says so and names what can.
"""
import math, sys, json, random

random.seed(20260815)
SRC = "work/midas_NA_true.txt"
R_EARTH = 6371.0
LAT0, LON0 = 34.90, -106.53
STRIKE_DEG = 10.0          # fault-parallel azimuth, degrees east of north
HALFWIDTH_KM = 60.0        # along-strike extent of the swath
MAXNORM_KM = 40.0          # across-strike half-width
MIN_DUR = 3.0
CREEP_TEST_MM_YR = 1.0     # a creep rate worth detecting, for the power calculation


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R_EARTH*math.asin(math.sqrt(h))


def load():
    out = []
    for ln in open(SRC, encoding="utf-8", errors="replace"):
        f = ln.split()
        if len(f) < 27: continue
        try:
            lat = float(f[24]); lon = float(f[25])
            if lon > 180: lon -= 360.0
            out.append({"site": f[0], "dur": float(f[4]),
                        "ve": float(f[8])*1000, "vn": float(f[9])*1000, "vu": float(f[10])*1000,
                        "lat": lat, "lon": lon})
        except ValueError:
            continue
    return out


kx = 111.320*math.cos(math.radians(LAT0)); ky = 110.574
th = math.radians(STRIKE_DEG)
# unit vectors: along-strike (p) and fault-normal (n), in east/north components
pe, pn = math.sin(th), math.cos(th)
ne, nn = math.cos(th), -math.sin(th)

rows = []
for s in load():
    if s["dur"] < MIN_DUR: continue
    dx = (s["lon"]-LON0)*kx; dy = (s["lat"]-LAT0)*ky
    along = dx*pe + dy*pn
    norm = dx*ne + dy*nn
    if abs(along) > HALFWIDTH_KM or abs(norm) > MAXNORM_KM: continue
    rows.append({"site": s["site"], "along": along, "norm": norm,
                 "vpar": s["ve"]*pe + s["vn"]*pn, "vnorm": s["ve"]*ne + s["vn"]*nn,
                 "vu": s["vu"]})

# NMAB is excluded by name and the reason is stated: vn +5.2 mm/yr with vu -3.0 mm/yr,
# i.e. horizontal anomaly WITH subsidence = Albuquerque-basin aquifer compaction, a
# documented process. Excluding it is a claim; the run reports the answer BOTH ways.
def report(rs, tag):
    west = [r for r in rs if r["norm"] < 0]; east = [r for r in rs if r["norm"] >= 0]
    vs = [r["vpar"] for r in rs]
    mean = sum(vs)/len(vs)
    sd = math.sqrt(sum((v-mean)**2 for v in vs)/(len(vs)-1)) if len(vs) > 1 else float("nan")
    out = {"tag": tag, "n": len(rs), "n_west": len(west), "n_east": len(east),
           "scatter_vpar_mm_yr": round(sd, 3),
           "n_within_20km_west": sum(1 for r in west if r["norm"] > -20),
           "n_within_20km_east": sum(1 for r in east if r["norm"] < 20)}
    # power: smallest detectable step at 2 sigma given this scatter and split
    if len(west) >= 2 and len(east) >= 2:
        sem = sd*math.sqrt(1/len(west) + 1/len(east))
        out["min_detectable_step_2sig_mm_yr"] = round(2*sem, 3)
        out["can_detect_1mm_yr_creep"] = bool(2*sem < CREEP_TEST_MM_YR)
        mw = sum(r["vpar"] for r in west)/len(west)
        me = sum(r["vpar"] for r in east)/len(east)
        out["observed_step_mm_yr"] = round(me-mw, 3)
        out["observed_step_over_sigma"] = round((me-mw)/sem, 2) if sem else None
    else:
        out["min_detectable_step_2sig_mm_yr"] = None
        out["can_detect_1mm_yr_creep"] = False
    return out


def bic_models(rs):
    if len(rs) < 6: return None
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
    # M2: linear + step at x=0, solved by least squares on 3 columns
    A = [[1.0, xi, 1.0 if xi >= 0 else 0.0] for xi in x]
    M = [[sum(A[k][i]*A[k][j] for k in range(n)) for j in range(3)]
         + [sum(A[k][i]*y[k] for k in range(n))] for i in range(3)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r_: abs(M[r_][i]))
        M[i], M[p] = M[p], M[i]
        if abs(M[i][i]) < 1e-12: return None
        for r_ in range(3):
            if r_ == i: continue
            f = M[r_][i]/M[i][i]
            for c in range(i, 4): M[r_][c] -= f*M[i][c]
    p2 = [M[i][3]/M[i][i] for i in range(3)]
    r2 = rss([p2[0]+p2[1]*x[i]+p2[2]*A[i][2] for i in range(n)])
    def bic(r, k): return n*math.log(max(r, 1e-12)/n) + k*math.log(n)
    return {"BIC_M0_flat": round(bic(r0, 1), 2),
            "BIC_M1_linear": round(bic(r1, 2), 2),
            "BIC_M2_step": round(bic(r2, 3), 2),
            "step_estimate_mm_yr": round(p2[2], 3),
            "linear_slope_mm_yr_per_km": round(p2[1], 4),
            "winner": min([("M0 flat", bic(r0,1)), ("M1 linear", bic(r1,2)),
                           ("M2 step (creep)", bic(r2,3))], key=lambda t: t[1])[0]}


out = {"swath": {"strike_deg": STRIKE_DEG, "along_halfwidth_km": HALFWIDTH_KM,
                 "normal_halfwidth_km": MAXNORM_KM, "min_duration_yr": MIN_DUR},
       "stations": sorted([{k: (round(v,3) if isinstance(v,float) else v)
                            for k,v in r.items()} for r in rows], key=lambda r: r["norm"])}
with_nmab = report(rows, "ALL STATIONS")
no_nmab = report([r for r in rows if r["site"] != "NMAB"], "NMAB EXCLUDED (aquifer)")
out["power_and_step"] = [with_nmab, no_nmab]
out["models_all"] = bic_models(rows)
out["models_no_nmab"] = bic_models([r for r in rows if r["site"] != "NMAB"])

for r in out["power_and_step"]:
    print(json.dumps(r), file=sys.stderr)
print(json.dumps(out["models_all"]), file=sys.stderr)
print(json.dumps(out["models_no_nmab"]), file=sys.stderr)
print(json.dumps(out, indent=2))
