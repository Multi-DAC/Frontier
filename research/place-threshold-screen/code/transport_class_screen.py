"""TRANSPORT-CLASS SCREEN -- the national comparison with the INSTRUMENT gates removed.

Why this file exists. `work/national_site_screen.py` returned California, and the reason
is written into its own criteria list: R5 ("slip rate >= 1.0 mm/yr") and R4 ("modern
geodetic strain") are requirements of my INSTRUMENTS, not of the mechanism. Both select
plate boundaries by construction, and both score the Sandia-Manzano candidate at ZERO --
its measured rate is 0.05 mm/yr (Personius & Mahan 2003). A screen on which the candidate
cannot place is not a comparison. Addendum 2 sec. 2 named this run as the replacement.

So this screen keeps only criteria that are claims about the PHYSICS:

  P1 CONDUIT   -- a Quaternary fault, graded by recency of rupture       [Qfaults age]
  P2 DILATANT  -- extensional sense. A normal fault opens permeability as it slips;
                  a thrust closes it. This is a statement about fluid pathway, not
                  about how fast the fault moves.                        [Qfaults slip_sense]
  P3 PIEZO     -- quartz-rich crystalline rock AT or NEAR the surface trace
                                                                        [Macrostrat map]

and it deliberately does NOT gate on rate or on strain. Rate is carried as an ATTRIBUTE
so the ranking can be inspected against it, never as a filter.

⚠ P3 is the weak criterion and stays weak: bulk piezoelectricity in an equigranular
pluton averages toward zero (see lithology_probe's docstring). TIER_FABRIC and
TIER_PLUTONIC are reported separately for that reason and are not summed.

STAGING, because Macrostrat is the expensive layer and a base-rate run is already using
it: stage 1 is pure Qfaults attribute+geometry and runs immediately. Stage 2 is one
Macrostrat point query per node -- the STRONGEST form of P3 ("is the rock quartz-rich at
the trace") -- and only nodes that FAIL at-point earn the expensive ring probe in a later
pass. Stage 2 will not start while another Macrostrat client is running; see --wait-pid.
"""
import json, math, os, sys, time, urllib.request, urllib.parse

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/21/query"
CACHE = "work/qfaults_normal_national.geojson"
PAGE = 1000
R_EARTH = 6371.0

# Measured 2026-08-15 against the live service with returnDistinctValues, not recalled.
# NOTE the case pair: 'late Quaternary' (18,631) and 'Late Quaternary' (282) are DISTINCT
# strings in this field. Matching is done case-folded downstream for exactly that reason.
AGE_RANK = {
    "historic": 5,
    "latest quaternary": 4,          # <15 ka
    "late quaternary": 3,            # <130 ka
    "middle and late quaternary": 2,  # <750 ka
    "undifferentiated quaternary": 1,
    "class b": 0,
    "unspecified": 0,
}
# 'Normal' 54,158 ; 'Left lateral; Normal' 60 ; 'Unspecified; Normal' 31
DILATANT = ("normal",)


def hav(lat1, lon1, lat2, lon2):
    la1, lo1, la2, lo2 = map(math.radians, (lat1, lon1, lat2, lon2))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def post(**kw):
    kw.setdefault("f", "geojson")
    req = urllib.request.Request(
        EP, data=urllib.parse.urlencode(kw).encode(),
        headers={"User-Agent": "Mozilla/5.0",
                 "Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=600))


def pull_dilatant():
    """All Quaternary faults with an extensional component, national layer 21.

    Geometry is generalised at ~1 km (maxAllowableOffset) because this screen only needs
    node positions, and the ungeneralised pull is ~100 MB. The offset is recorded in the
    output so nobody later reads these vertices as mapped trace.
    """
    if os.path.exists(CACHE):
        fc = json.load(open(CACHE))
        print(f"[stage1] cache hit: {len(fc['features'])} features", file=sys.stderr)
        return fc
    where = ("slip_sense = 'Normal' OR slip_sense = 'Left lateral; Normal' "
             "OR slip_sense = 'Unspecified; Normal'")
    feats, off = [], 0
    while True:
        d = post(where=where,
                 outFields=("fault_name,section_name,fault_id,age,slip_rate,slip_sense,"
                            "linetype,total_fault_length,dip_direction,mapped_scale"),
                 returnGeometry="true", outSR="4326", maxAllowableOffset="0.01",
                 resultOffset=off, resultRecordCount=PAGE)
        got = d.get("features", [])
        feats.extend(got)
        print(f"[stage1] +{len(got)} (total {len(feats)})", file=sys.stderr)
        sys.stderr.flush()
        if len(got) < PAGE:
            break
        off += PAGE
        if off > 80000:
            print("[warn] paging cap", file=sys.stderr)
            break
    fc = {"type": "FeatureCollection", "maxAllowableOffset_deg": 0.01,
          "features": feats}
    open(CACHE, "w").write(json.dumps(fc))
    return fc


def verts(ft):
    g = ft.get("geometry") or {}
    if g.get("type") == "LineString":
        return g["coordinates"]
    if g.get("type") == "MultiLineString":
        return [c for part in g["coordinates"] for c in part]
    return []


def nodes_from(fc, thin_km=40.0, conus_only=True):
    """Collapse the fault population into candidate nodes >= thin_km apart.

    Sort key is age rank, NOT slip rate: rate is the gate this screen exists to remove.
    Ties break on mapped length, so a long well-known structure wins its cluster over a
    2 km splay -- which is a mapping-effort bias and is stated, not hidden.
    """
    pts = []
    for ft in fc["features"]:
        p = ft["properties"]
        vs = verts(ft)
        if not vs:
            continue
        rank = AGE_RANK.get((p.get("age") or "").strip().lower(), 0)
        step = max(1, len(vs) // 3)
        for c in vs[::step]:
            lon, lat = c[0], c[1]
            if conus_only and not (24.0 <= lat <= 49.5 and -125.5 <= lon <= -66.5):
                continue
            pts.append({"lat": round(lat, 5), "lon": round(lon, 5),
                        "age": p.get("age"), "age_rank": rank,
                        "slip_rate_class": p.get("slip_rate"),
                        "slip_sense": p.get("slip_sense"),
                        "fault_name": p.get("fault_name"),
                        "section_name": p.get("section_name"),
                        "linetype": p.get("linetype"),
                        "total_fault_length": p.get("total_fault_length") or 0})
    pts.sort(key=lambda r: (-r["age_rank"], -(r["total_fault_length"] or 0)))
    keep = []
    for p in pts:
        if all(hav(p["lat"], p["lon"], k["lat"], k["lon"]) >= thin_km for k in keep):
            keep.append(p)
    return keep


def wait_for_pid(pid, poll=60):
    """Block while another process is hitting Macrostrat. Pacing, not politeness: two
    clients on the same public API is how you earn a rate-limit that corrupts BOTH runs."""
    import subprocess
    while True:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue)"
                            f" {{'ALIVE'}} else {{'GONE'}}"],
                           capture_output=True, text=True)
        if "GONE" in r.stdout:
            return
        print(f"[stage2] waiting on pid {pid} ...", file=sys.stderr)
        sys.stderr.flush()
        time.sleep(poll)


if __name__ == "__main__":
    args = sys.argv[1:]
    thin = float(os.environ.get("THIN_KM", "40"))
    fc = pull_dilatant()
    nodes = nodes_from(fc, thin_km=thin)
    print(f"[stage1] dilatant Quaternary features: {len(fc['features'])}", file=sys.stderr)
    print(f"[stage1] candidate nodes >= {thin} km apart (CONUS): {len(nodes)}",
          file=sys.stderr)
    by_age = {}
    for n in nodes:
        by_age[n["age"]] = by_age.get(n["age"], 0) + 1
    for k, v in sorted(by_age.items(), key=lambda kv: -kv[1]):
        print(f"    {v:>5}  {k}", file=sys.stderr)
    out = {"population_features": len(fc["features"]), "thin_km": thin,
           "nodes": nodes, "age_histogram": by_age}
    json.dump(out, open("work/transport_nodes.json", "w"), indent=1)
    print("[stage1] wrote work/transport_nodes.json", file=sys.stderr)

    # Named pins that must be SCORED whether or not they win their 40 km cluster.
    # Hubbell Spring wins the Albuquerque cluster on age rank, which silently swallows the
    # Sandia fault west scarp 18 km north -- the pin that two independent corrections now
    # rank ABOVE it. A thinning rule that eats the leading candidate is a bucket derived
    # by subtraction; forcing them in keeps the comparison honest and marks them `forced`.
    FORCED = [
        (35.100, -106.510, "Sandia fault, west scarp (D196 lithology re-rank)"),
        (34.974, -106.519, "Hubbell Spring, NORTH scarp maximum (62% well-constrained)"),
        (34.866, -106.550, "Hubbell Spring, SOUTH scarp maximum (60%, relay step)"),
        (34.900, -106.530, "D138 original star (retired, kept as control)"),
        (35.060, -106.430, "Tijeras-Canoncito (June's best RAW convergence, demoted)"),
    ]
    for la, lo, why in FORCED:
        nodes.append({"lat": la, "lon": lo, "age": "forced-pin", "age_rank": -1,
                      "slip_rate_class": None, "slip_sense": "Normal",
                      "fault_name": why, "section_name": None, "linetype": None,
                      "total_fault_length": 0, "forced": True})

    if "--stage2" in args:
        wp = [a for a in args if a.startswith("--wait-pid=")]
        if wp:
            wait_for_pid(int(wp[0].split("=")[1]))
        from lithology_probe import unit_at, classify, _save  # noqa: E402
        scored = []
        for i, n in enumerate(nodes):
            us = unit_at(n["lat"], n["lon"])
            tier, term, name = classify(us)
            n2 = dict(n, at_point_tier=tier, at_point_term=term, at_point_unit=name)
            scored.append(n2)
            if (i + 1) % 25 == 0:
                _save()
                print(f"[stage2] {i+1}/{len(nodes)}", file=sys.stderr)
                sys.stderr.flush()
        _save()
        hits = [r for r in scored
                if r["at_point_tier"] in ("TIER_PLUTONIC", "TIER_FABRIC")]
        hits.sort(key=lambda r: (-r["age_rank"], -(r["total_fault_length"] or 0)))
        json.dump({"n_nodes": len(scored), "n_quartz_at_point": len(hits),
                   "hits": hits, "all": scored},
                  open("work/transport_screen_stage2.json", "w"), indent=1)
        print(f"[stage2] quartz-rich AT the trace: {len(hits)} / {len(scored)}",
              file=sys.stderr)
