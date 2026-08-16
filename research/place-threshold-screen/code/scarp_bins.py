"""Along-strike scarp-expression bins for ANY named Qfaults fault.

Generalises the one-off binning that moved the Hubbell Spring pin in ADDENDUM2 s3, so the
same measurement can be made for the faults it moved the pin TOWARD. Two defects from
tonight are guarded here rather than re-earned:

  * the pull PAGES. work/hubbell_fault_length.py reported "hubbell: []" because a bbox
    query hit the service record limit and the fault's own segments fell off the end.
  * fault_name matching is EXACT and case-sensitive in the where-clause, so this queries
    with LIKE and reports every distinct name it actually got back.

Output per 2 km latitude bin: traced km, and km graded 'Well Constrained' -- which is
mapping confidence, NOT activity, and is a proxy for "someone verified rock here".
"""
import json, math, sys, urllib.request, urllib.parse
from collections import defaultdict

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/21/query"
R = 6371.0
PAGE = 1000


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def pull(name_like):
    feats, off = [], 0
    where = f"fault_name LIKE '%{name_like}%'"
    while True:
        q = dict(where=where, outFields="fault_name,section_name,linetype,age,slip_rate,"
                                        "slip_sense,total_fault_length,mapped_scale",
                 returnGeometry="true", outSR="4326", f="geojson",
                 resultOffset=off, resultRecordCount=PAGE)
        req = urllib.request.Request(
            EP, data=urllib.parse.urlencode(q).encode(),
            headers={"User-Agent": "Mozilla/5.0",
                     "Content-Type": "application/x-www-form-urlencoded"})
        d = json.load(urllib.request.urlopen(req, timeout=300))
        got = d.get("features", [])
        feats.extend(got)
        if len(got) < PAGE:
            break
        off += PAGE
        if off > 40000:
            print("[warn] paging cap", file=sys.stderr)
            break
    return feats


def verts(ft):
    g = ft.get("geometry") or {}
    if g.get("type") == "LineString":
        return [g["coordinates"]]
    if g.get("type") == "MultiLineString":
        return g["coordinates"]
    return []


def bins(feats, dlat=0.018):
    traced, well, mod = defaultdict(float), defaultdict(float), defaultdict(float)
    lonsum, lonw = defaultdict(float), defaultdict(float)
    for ft in feats:
        lt = (ft["properties"].get("linetype") or "").strip().lower()
        for part in verts(ft):
            for i in range(len(part) - 1):
                (x0, y0), (x1, y1) = part[i][:2], part[i + 1][:2]
                seg = hav(y0, x0, y1, x1)
                key = round(((y0 + y1) / 2) / dlat) * dlat
                traced[key] += seg
                lonsum[key] += ((x0 + x1) / 2) * seg
                lonw[key] += seg
                if "well" in lt:
                    well[key] += seg
                elif "moderate" in lt:
                    mod[key] += seg
    rows = []
    for k in sorted(traced, reverse=True):
        t = traced[k]
        rows.append({"lat": round(k, 4), "lon": round(lonsum[k] / lonw[k], 4),
                     "traced_km": round(t, 2), "well_km": round(well[k], 2),
                     "well_pct": round(100 * well[k] / t) if t else 0,
                     "mod_pct": round(100 * mod[k] / t) if t else 0})
    return rows


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Sandia"
    fs = pull(name)
    names = defaultdict(int)
    for f in fs:
        names[f["properties"].get("fault_name")] += 1
    print(f"LIKE '%{name}%' -> {len(fs)} segments across {len(names)} distinct fault_name:",
          file=sys.stderr)
    for k, v in sorted(names.items(), key=lambda kv: -kv[1]):
        print(f"   {v:>5}  {k}", file=sys.stderr)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    if only:
        fs = [f for f in fs if f["properties"].get("fault_name") == only]
        print(f"[filtered to exactly '{only}': {len(fs)} segments]", file=sys.stderr)
    rows = bins(fs)
    tot = sum(r["traced_km"] for r in rows)
    tw = sum(r["well_km"] for r in rows)
    print(f"\ntraced {tot:.1f} km, well-constrained {tw:.1f} km ({100*tw/tot:.0f}%)",
          file=sys.stderr)
    print(f"{'lat':>8} {'lon':>10} {'traced':>8} {'well':>7} {'well%':>6} {'mod%':>6}",
          file=sys.stderr)
    for r in rows:
        print(f"{r['lat']:8.3f} {r['lon']:10.3f} {r['traced_km']:8.2f} "
              f"{r['well_km']:7.2f} {r['well_pct']:5}% {r['mod_pct']:5}%", file=sys.stderr)
    json.dump({"query": name, "exact": only, "segments": len(fs),
               "distinct_names": dict(names), "bins": rows},
              open(f"work/scarp_bins_{name.replace(' ', '_')}.json", "w"), indent=1)
