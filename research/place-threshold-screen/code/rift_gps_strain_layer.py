"""Rio Grande rift portal pins -- GEODETIC STRAIN layer (NGL MIDAS, NA-fixed). Day 196.

WHY. The D196 seismicity layer (work/sandia_seismicity_layer.py) found all three
Albuquerque-rift pins indistinguishable from zero and from each other, while the
positive control (Socorro) outscored them 11-30x. That forked the programme:

  Fork 1 -- the piezo term does NOT need seismicity. Aseismic creep or the residual
           stress field of a locked fault supplies E without measurable earthquakes.
           Signature: a velocity GRADIENT across the trace with no seismicity.
  Fork 2 -- it does. Then the pin set scores a dead driver.

Earthquake counts cannot separate these. Geodesy can: creep is motion without
rupture, and MIDAS gives NA-fixed station velocities from public GNSS.

CONTROLS FIRST, AND BEFORE THE MEASUREMENT (standing discipline).
  METHOD-POS : San Andreas creeping section / Parkfield -- a documented aseismic
               creeping fault. The gradient detector MUST fire here or it is broken.
  METHOD-NEG : stable craton, central Kansas -- MUST come back flat. If Kansas shows
               a gradient, the detector is reading reference-frame noise as strain.
  RIFT-POS   : Socorro magma body -- documented ~2-3 mm/yr UPLIFT. Tests whether the
               rift has ANY live geodetic signal this network can see, in the vertical
               channel, independent of the horizontal gradient logic.

Data: http://geodesy.unr.edu/velocities/midas.NA.txt  (NA plate-fixed, IGS14-derived)
MIDAS cols: 1 site, 9 ve, 10 vn, 11 vu (m/yr), 12-14 sigmas, 25 lat, 26 lon.
"""
import math, sys, json, itertools

SRC = "work/midas_NA_true.txt"
R_EARTH = 6371.0

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
            out.append({
                "site": f[0], "t0": float(f[2]), "t1": float(f[3]), "dur": float(f[4]),
                "ve": float(f[8])*1000, "vn": float(f[9])*1000, "vu": float(f[10])*1000,
                "sve": float(f[11])*1000, "svn": float(f[12])*1000, "svu": float(f[13])*1000,
                "lat": lat, "lon": lon,
            })
        except ValueError:
            continue
    return out

STA = load()
print(f"[load] {len(STA)} MIDAS NA-fixed stations", file=sys.stderr)

SITES = [
    # name,                       lat,     lon,    role
    ("METHOD-POS Parkfield SAF",  35.90, -120.43, "creeping fault: detector MUST fire"),
    ("METHOD-NEG Kansas craton",  38.80,  -98.20, "stable: detector MUST stay flat"),
    ("RIFT-POS  Socorro magma",   34.10, -106.90, "documented uplift: vertical channel check"),
    ("PRIMARY   Hubbell Spring",  34.90, -106.53, "the pin under test"),
    ("SECONDARY Sandia W scarp",  35.10, -106.51, "best piezo, late-Q"),
    ("CONTROL   Tijeras corridor",35.17, -106.32, "blind control"),
    ("FLOOR     Bouguer low",     35.20, -106.72, "FLOOR-class: no piezo"),
]
RADII = [25.0, 50.0, 100.0]
MIN_DUR = 2.5   # yr; MIDAS velocities below this are not trustworthy


def near(lat, lon, r):
    return [s for s in STA if s["dur"] >= MIN_DUR and hav((lat, lon), (s["lat"], s["lon"])) <= r]


def gradient(group):
    """Largest 2-sigma-significant differential horizontal velocity per unit baseline.

    Returns (nanostrain/yr, pair, n_significant_pairs, n_pairs). Sigma is propagated
    from the two stations' MIDAS uncertainties in quadrature. A pair only counts if
    the differential exceeds 2x its own sigma -- so a noisy pair cannot manufacture a
    gradient, and a null here is a null with a stated floor, not an absence of data.
    """
    best = None; nsig = 0; npair = 0
    for a, b in itertools.combinations(group, 2):
        d = hav((a["lat"], a["lon"]), (b["lat"], b["lon"]))
        if d < 3.0:      # co-located monuments carry no strain information
            continue
        npair += 1
        dv = math.hypot(a["ve"]-b["ve"], a["vn"]-b["vn"])
        sd = math.hypot(a["sve"], b["sve"], a["svn"], b["svn"])
        sig = dv > 2*sd
        if sig: nsig += 1
        rate = dv / d * 1e6 / 1000.0      # mm/yr per km -> nanostrain/yr
        srate = sd / d * 1e6 / 1000.0
        if sig and (best is None or rate > best[0]):
            best = (rate, f"{a['site']}-{b['site']}", round(d,1), round(dv,3), round(sd,3), round(srate,1))
    return best, nsig, npair


rows = []
for name, lat, lon, role in SITES:
    row = {"site": name, "role": role, "by_radius": {}}
    for r in RADII:
        g = near(lat, lon, r)
        best, nsig, npair = gradient(g)
        vus = [s["vu"] for s in g]
        row["by_radius"][int(r)] = {
            "n_stations": len(g),
            "n_pairs": npair,
            "n_pairs_2sigma": nsig,
            "max_sig_gradient_nstrain_yr": None if best is None else round(best[0], 1),
            "gradient_pair": None if best is None else best[1],
            "pair_km": None if best is None else best[2],
            "pair_dv_mm_yr": None if best is None else best[3],
            "pair_sigma_mm_yr": None if best is None else best[4],
            "median_vu_mm_yr": None if not vus else round(sorted(vus)[len(vus)//2], 2),
            "stations": sorted(s["site"] for s in g),
        }
    rows.append(row)
    b = row["by_radius"][50]
    print(f"{name:28s} r=50km n={b['n_stations']:3d} sigpairs={b['n_pairs_2sigma']:3d}/"
          f"{b['n_pairs']:4d} grad={b['max_sig_gradient_nstrain_yr']} vu={b['median_vu_mm_yr']}",
          file=sys.stderr)

print(json.dumps(rows, indent=2))
