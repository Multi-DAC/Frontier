"""Rio Grande rift pins -- GEODETIC STRAIN, tensor fit. Day 196. Supersedes the
max-pair detector in rift_gps_strain_layer.py, which was REFUTED by its own output:
all four Albuquerque cells returned the identical 830 nstrain/yr because one station
(NMAB: vn = +5.2 mm/yr against a regional 2.0, vu = -3.0 mm/yr) sat inside every
radius. Horizontal anomaly plus subsidence is the signature of aquifer compaction --
Albuquerque basin groundwater withdrawal -- not of fault creep. A max-pair statistic
finds the worst monument in the cell, by construction.

METHOD. Fit a uniform velocity-gradient tensor to each cell by least squares:
    ve = a + L11*dx + L12*dy
    vn = b + L21*dx + L22*dy
  exx = L11, eyy = L22, exy = (L12+L21)/2, and the reported scalar is the maximum
  shear strain rate  gmax = sqrt((exx-eyy)^2 + 4*exy^2)  in nanostrain/yr.
An outlier inflates the residual rather than dictating the answer, and outliers are
then rejected explicitly at 3x MAD and NAMED in the output -- a fit with no deaths is
a fit to distrust.

SIGNIFICANCE. Scramble null: reassign the observed velocity vectors to the observed
station positions at random, 2000x, refit, and ask how often noise alone produces a
gmax this large. This destroys spatial coherence while preserving the exact velocity
scatter, so it tests the one thing at issue -- whether the field has STRUCTURE across
the fault -- and it needs no faith in MIDAS's formal sigmas, which are what fooled the
first detector.

CONTROLS, BEFORE THE MEASUREMENT.
  METHOD-POS Parkfield SAF  -- documented creep. MUST come back large and p<0.01.
  METHOD-NEG Kansas craton  -- stable. MUST come back small and p>0.05.
  RIFT-POS   Socorro        -- documented uplift; vertical channel, independent check.
Rift extension across the whole Rio Grande rift is order 1 mm/yr over ~100 km, i.e.
~10 nstrain/yr TOTAL. Anything the pins show above ~50 nstrain/yr is a monument
problem, not tectonics, and the null hypothesis of this run is that the pins are flat.
"""
import math, sys, json, random

random.seed(20260815)
SRC = "work/midas_NA_true.txt"
R_EARTH = 6371.0
MIN_DUR = 3.0
NSCRAM = 2000


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def load():
    out = []
    for ln in open(SRC, encoding="utf-8", errors="replace"):
        f = ln.split()
        if len(f) < 27:
            continue
        try:
            lat = float(f[24]); lon = float(f[25])
            if lon > 180: lon -= 360.0
            out.append({"site": f[0], "dur": float(f[4]),
                        "ve": float(f[8])*1000, "vn": float(f[9])*1000, "vu": float(f[10])*1000,
                        "lat": lat, "lon": lon})
        except ValueError:
            continue
    return out


STA = load()


def lstsq(A, y):
    """Normal equations with Gaussian elimination. n unknowns, tiny system."""
    n = len(A[0])
    M = [[sum(A[k][i]*A[k][j] for k in range(len(A))) for j in range(n)]
         + [sum(A[k][i]*y[k] for k in range(len(A)))] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[p][i]) < 1e-12:
            return None
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r == i: continue
            f = M[r][i]/M[i][i]
            for c in range(i, n+1):
                M[r][c] -= f*M[i][c]
    return [M[i][n]/M[i][i] for i in range(n)]


def fit(group, lat0, lon0):
    """Returns (gmax nstrain/yr, dilatation nstrain/yr, rms residual mm/yr, params)."""
    if len(group) < 4:
        return None
    kx = 111.320*math.cos(math.radians(lat0)); ky = 110.574
    A, ye, yn = [], [], []
    for s in group:
        A.append([1.0, (s["lon"]-lon0)*kx, (s["lat"]-lat0)*ky])
        ye.append(s["ve"]); yn.append(s["vn"])
    pe = lstsq(A, ye); pn = lstsq(A, yn)
    if pe is None or pn is None:
        return None
    exx, exy1 = pe[1], pe[2]
    eyx, eyy = pn[1], pn[2]
    exy = 0.5*(exy1+eyx)
    gmax = math.hypot(exx-eyy, 2*exy) * 1e3      # (mm/yr)/km -> nanostrain/yr
    dil = (exx+eyy) * 1e3
    res = []
    for k, s in enumerate(group):
        re_ = ye[k] - (pe[0]+pe[1]*A[k][1]+pe[2]*A[k][2])
        rn_ = yn[k] - (pn[0]+pn[1]*A[k][1]+pn[2]*A[k][2])
        res.append(math.hypot(re_, rn_))
    rms = math.sqrt(sum(r*r for r in res)/len(res))
    return gmax, dil, rms, res


def robust_fit(group, lat0, lon0):
    killed = []
    g = list(group)
    for _ in range(6):
        f = fit(g, lat0, lon0)
        if f is None:
            return None, killed
        _, _, _, res = f
        med = sorted(res)[len(res)//2]
        mad = sorted(abs(r-med) for r in res)[len(res)//2] or 1e-9
        bad = [i for i, r in enumerate(res) if (r-med)/(1.4826*mad) > 3.0]
        if not bad or len(g)-len(bad) < 5:
            return f, killed
        for i in sorted(bad, reverse=True):
            killed.append({"site": g[i]["site"], "resid_mm_yr": round(res[i], 2),
                           "vn": round(g[i]["vn"], 2), "vu": round(g[i]["vu"], 2)})
            g.pop(i)
    return fit(g, lat0, lon0), killed


def scramble_p(group, lat0, lon0, observed):
    vels = [(s["ve"], s["vn"]) for s in group]
    hits = 0; draws = 0
    for _ in range(NSCRAM):
        random.shuffle(vels)
        gg = [dict(s, ve=vels[i][0], vn=vels[i][1]) for i, s in enumerate(group)]
        f = fit(gg, lat0, lon0)
        if f is None: continue
        draws += 1
        if f[0] >= observed: hits += 1
    return (hits+1)/(draws+1), draws


SITES = [
    ("METHOD-POS Parkfield SAF",  35.90, -120.43),
    ("METHOD-NEG Kansas craton",  38.80,  -98.20),
    ("RIFT-POS  Socorro magma",   34.10, -106.90),
    ("PRIMARY   Hubbell Spring",  34.90, -106.53),
    ("SECONDARY Sandia W scarp",  35.10, -106.51),
    ("CONTROL   Tijeras corridor",35.17, -106.32),
    ("FLOOR     Bouguer low",     35.20, -106.72),
]
RADII = [50.0, 100.0]

rows = []
for name, lat, lon in SITES:
    row = {"site": name, "lat": lat, "lon": lon, "by_radius": {}}
    for r in RADII:
        g = [s for s in STA if s["dur"] >= MIN_DUR and hav((lat, lon), (s["lat"], s["lon"])) <= r]
        f, killed = robust_fit(g, lat, lon)
        if f is None:
            row["by_radius"][int(r)] = {"n_stations": len(g), "verdict": "TOO FEW STATIONS"}
            print(f"{name:28s} r={int(r):3d} n={len(g):3d}  TOO FEW", file=sys.stderr)
            continue
        gmax, dil, rms, _ = f
        kept = len(g) - len(killed)
        p, draws = scramble_p([s for s in g if s["site"] not in {k['site'] for k in killed}],
                              lat, lon, gmax)
        vus = sorted(s["vu"] for s in g)
        row["by_radius"][int(r)] = {
            "n_stations": len(g), "n_kept": kept,
            "outliers_rejected": killed,
            "gmax_nanostrain_yr": round(gmax, 1),
            "dilatation_nanostrain_yr": round(dil, 1),
            "rms_resid_mm_yr": round(rms, 3),
            "scramble_p": round(p, 4), "scramble_draws": draws,
            "median_vu_mm_yr": round(vus[len(vus)//2], 2) if vus else None,
        }
        print(f"{name:28s} r={int(r):3d} n={len(g):3d} kept={kept:3d} killed={len(killed)} "
              f"gmax={gmax:8.1f} dil={dil:8.1f} rms={rms:.2f} p={p:.4f} vu={row['by_radius'][int(r)]['median_vu_mm_yr']}",
              file=sys.stderr)
    rows.append(row)

print(json.dumps(rows, indent=2))
