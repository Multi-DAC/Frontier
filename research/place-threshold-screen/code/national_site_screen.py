"""NATIONAL SITE SCREEN -- "sites that meet all requirements, if Sandia is a bust."

Clayton, D196: "let's run analysis looking for sites that meet all requirements if
Sandia is a bust, although I'm certainly under the impression it is not."

THE REQUIREMENTS, restated with a gauge each. Layers 1-3 are the D137/D138 criteria.
Layer 4 is the one the D196 dossier found missing ("the criteria contained a driver
nobody measured"). Layer 5 is new tonight and it is the one that changes the search:

  R1 CONDUIT   -- an active Quaternary fault within 10 km            [USGS Qfaults]
  R2 DRIVER    -- PUBLISHED SLIP RATE on that fault                  [Qfaults slip_rate]
  R3 PIEZO     -- quartz-rich crystalline rock near surface          [Macrostrat map]
  R4 STRAIN    -- modern geodetic strain above the craton floor      [NGL MIDAS]
  R5 RESOLVABLE -- slip rate >= 1.0 mm/yr, i.e. ABOVE what a regional GPS network can
                   actually detect (~0.4-1.0 mm/yr, measured tonight at Albuquerque)

R5 is not a physics requirement. It is an INSTRUMENT requirement, and it exists because
of what the ABQ numbers turned out to say: Hubbell Spring's published slip rate is
0.2-1.0 mm/yr (mid 0.6) and last night's geodetic bound was ~1.0 mm/yr. The bound sits
ABOVE the expected signal. So the "creep null" never had the power to refute anything,
and a site search that ignores resolvability will keep producing pins that cannot be
decided by any instrument I own. A screen that cannot fail is not a screen.

STAGE 1 is a national attribute query for fast faults ONLY (>1 mm/yr), which is cheap
because it needs no geometry filter and returns a small set. Stages 2-4 run only on the
survivors, because lithology and strain are the expensive layers.
"""
import json, math, os, sys, urllib.request, urllib.parse, random
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lithology_probe import nearest_quartz_rich          # noqa: E402
from qfaults_pull import slip_mid, verts, hav_ll         # noqa: E402

random.seed(20260815)
EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/12/query"
FAST_CACHE = "work/qfaults_fast_national.geojson"
MIDAS_NA = "work/midas_NA_true.txt"
R_EARTH = 6371.0
CRATON_FLOOR_NSTRAIN = 8.0        # measured: Kansas craton control, D196 addendum
PAGE = 1000


# ---------------------------------------------------------------- stage 1: fast faults
def pull_fast():
    if os.path.exists(FAST_CACHE):
        return json.load(open(FAST_CACHE))
    where = ("slip_rate = 'Greater than 5.0 mm/yr' OR "
             "slip_rate = 'Between 5.0 and 1.0 mm/yr'")
    feats, off = [], 0
    while True:
        q = dict(where=where, outFields="fault_name,section_name,slip_rate,age,"
                                        "slip_sense,total_fault_length",
                 returnGeometry="true", outSR="4326", f="geojson",
                 resultOffset=off, resultRecordCount=PAGE)
        # POST, not GET: the GET form of this where-clause returns 403 (quotes in the
        # query string trip the server's filter). Same query, different verb.
        req = urllib.request.Request(EP, data=urllib.parse.urlencode(q).encode(),
                                     headers={"User-Agent": "Mozilla/5.0",
                                              "Content-Type":
                                                  "application/x-www-form-urlencoded"})
        d = json.load(urllib.request.urlopen(req, timeout=300))
        got = d.get("features", [])
        feats.extend(got)
        print(f"[stage1] +{len(got)} (total {len(feats)})", file=sys.stderr)
        if len(got) < PAGE:
            break
        off += PAGE
        if off > 60000:
            break
    out = {"type": "FeatureCollection", "features": feats}
    open(FAST_CACHE, "w").write(json.dumps(out))
    return out


def fault_nodes(fc, thin_km=25.0):
    """Collapse fast-fault vertices into candidate nodes >= thin_km apart, keeping the
    highest slip rate in each cluster. One node per ~25 km of fast fault."""
    pts = []
    for ft in fc["features"]:
        p = ft["properties"]
        sm = slip_mid(p.get("slip_rate"))
        if sm is None:
            continue
        vs = verts(ft)
        for c in vs[::max(1, len(vs)//4)]:
            pts.append({"lat": c[1], "lon": c[0], "slip": sm,
                        "fault_name": p.get("fault_name"),
                        "slip_rate_class": p.get("slip_rate"),
                        "age": p.get("age"), "sense": p.get("slip_sense")})
    pts.sort(key=lambda r: -r["slip"])
    keep = []
    for p in pts:
        if all(hav_ll(p["lat"], p["lon"], k["lat"], k["lon"]) >= thin_km for k in keep):
            keep.append(p)
    return keep


# ---------------------------------------------------------------- stage 2: strain
def load_midas(path):
    out = []
    for ln in open(path, encoding="utf-8", errors="replace"):
        f = ln.split()
        if len(f) < 27:
            continue
        try:
            lat = float(f[24]); lon = float(f[25])
            if lon > 180:
                lon -= 360.0
            if float(f[4]) < 3.0:
                continue
            out.append({"site": f[0], "ve": float(f[8])*1000, "vn": float(f[9])*1000,
                        "vu": float(f[10])*1000, "lat": lat, "lon": lon})
        except ValueError:
            continue
    return out


STA = load_midas(MIDAS_NA) if os.path.exists(MIDAS_NA) else []


def lstsq(A, y):
    n = len(A[0])
    M = [[sum(A[k][i]*A[k][j] for k in range(len(A))) for j in range(n)]
         + [sum(A[k][i]*y[k] for k in range(len(A)))] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[p][i]) < 1e-12:
            return None
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r == i:
                continue
            f = M[r][i]/M[i][i]
            for c in range(i, n+1):
                M[r][c] -= f*M[i][c]
    return [M[i][n]/M[i][i] for i in range(n)]


def _fit(group, lat0, lon0):
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
    exy = 0.5*(pe[2]+pn[1])
    gmax = math.hypot(pe[1]-pn[2], 2*exy)*1e3
    res = [math.hypot(ye[k]-(pe[0]+pe[1]*A[k][1]+pe[2]*A[k][2]),
                      yn[k]-(pn[0]+pn[1]*A[k][1]+pn[2]*A[k][2])) for k in range(len(group))]
    return gmax, res


def strain_at(lat, lon, r_km=50.0, nscram=400):
    grp = [s for s in STA if hav_ll(lat, lon, s["lat"], s["lon"]) <= r_km]
    if len(grp) < 5:
        return {"n": len(grp), "gmax_nstrain_yr": None,
                "verdict": "UNMEASURED -- <5 stations in radius"}
    # 3-sigma MAD trim, same as the D196 tensor run
    g = list(grp)
    for _ in range(4):
        f = _fit(g, lat, lon)
        if f is None:
            return {"n": len(grp), "gmax_nstrain_yr": None, "verdict": "FIT FAILED"}
        _, res = f
        med = sorted(res)[len(res)//2]
        mad = sorted(abs(x-med) for x in res)[len(res)//2] or 1e-9
        bad = [i for i, x in enumerate(res) if (x-med)/(1.4826*mad) > 3.0]
        if not bad or len(g)-len(bad) < 5:
            break
        for i in sorted(bad, reverse=True):
            g.pop(i)
    f = _fit(g, lat, lon)
    if f is None:
        return {"n": len(grp), "gmax_nstrain_yr": None, "verdict": "FIT FAILED"}
    gmax = f[0]
    vels = [(s["ve"], s["vn"]) for s in g]
    hits = draws = 0
    for _ in range(nscram):
        random.shuffle(vels)
        gg = [dict(s, ve=vels[i][0], vn=vels[i][1]) for i, s in enumerate(g)]
        ff = _fit(gg, lat, lon)
        if ff is None:
            continue
        draws += 1
        if ff[0] >= gmax:
            hits += 1
    p = (hits+1)/(draws+1)
    return {"n": len(grp), "n_kept": len(g), "gmax_nstrain_yr": round(gmax, 1),
            "p_scramble": round(p, 4),
            "above_craton_floor": bool(gmax > CRATON_FLOOR_NSTRAIN),
            "verdict": ("STRAINING" if (gmax > CRATON_FLOOR_NSTRAIN and p < 0.05)
                        else "not resolved above floor")}


# ---------------------------------------------------------------- scoring
def score(node, lith, strain):
    req = {}
    req["R1_conduit_active_fault"] = True                       # node IS on a fault
    req["R2_driver_published_slip"] = node["slip"] is not None
    tiers = lith.get("nearest", {})
    plut = tiers.get("TIER_PLUTONIC"); fab = tiers.get("TIER_FABRIC")
    near_km = min([t["ring_km"] for t in (plut, fab) if t], default=None)
    req["R3_piezo_quartz_rich_within_10km"] = bool(near_km is not None and near_km <= 10.0)
    req["R4_modern_strain"] = strain.get("verdict") == "STRAINING"
    req["R5_resolvable_slip_ge_1mm"] = bool(node["slip"] and node["slip"] >= 1.0)
    return {"requirements": req, "n_met": sum(1 for v in req.values() if v),
            "meets_all": all(req.values()),
            "nearest_quartz_km": near_km,
            "quartz_tier": ("TIER_PLUTONIC" if plut and (not fab or plut["ring_km"] <= fab["ring_km"])
                            else "TIER_FABRIC" if fab else None)}


if __name__ == "__main__":
    fc = pull_fast()
    print(f"[stage1] fast-fault features: {len(fc['features'])}", file=sys.stderr)
    nodes = fault_nodes(fc)
    print(f"[stage1] candidate nodes (>=25 km apart): {len(nodes)}", file=sys.stderr)
    LIMIT = int(os.environ.get("SCREEN_LIMIT", "45"))
    nodes = nodes[:LIMIT]
    results = []
    for i, nd in enumerate(nodes):
        st = strain_at(nd["lat"], nd["lon"])
        lith = nearest_quartz_rich(nd["lat"], nd["lon"])
        sc = score(nd, lith, st)
        row = {**nd, "strain": st, "lith_at_point": lith.get("at_point_unit"),
               "lith_at_point_tier": lith.get("at_point_tier"), **sc}
        results.append(row)
        print(f"[{i+1}/{len(nodes)}] {nd['fault_name'][:34]:<34} slip={nd['slip']:<4} "
              f"gmax={st.get('gmax_nstrain_yr')} q={sc['nearest_quartz_km']} "
              f"met={sc['n_met']}/5 {'*** ALL ***' if sc['meets_all'] else ''}",
              file=sys.stderr)
        sys.stderr.flush()
    results.sort(key=lambda r: (-r["n_met"], -(r["slip"] or 0)))
    out = {"stage1_fast_fault_features": len(fc["features"]),
           "candidate_nodes_screened": len(nodes),
           "meets_all_requirements": [r for r in results if r["meets_all"]],
           "all_results": results}
    print(json.dumps(out, indent=2))
    print(f"\nMEETS ALL 5: {len(out['meets_all_requirements'])}", file=sys.stderr)
    for r in out["meets_all_requirements"]:
        print(f"   {r['fault_name']}  {r['lat']:.3f},{r['lon']:.3f}  "
              f"slip={r['slip']} gmax={r['strain']['gmax_nstrain_yr']} "
              f"quartz={r['nearest_quartz_km']}km {r['quartz_tier']}", file=sys.stderr)
