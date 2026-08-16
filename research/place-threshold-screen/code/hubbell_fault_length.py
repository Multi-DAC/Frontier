"""How long is the Hubbell Spring fault, actually?

The aperture sweep tightens the creep bound from 1.04 to 0.49 mm/yr by widening the
swath along strike to +/-260 km. That is only a legitimate tightening IF the structure
being profiled is that long. If the mapped trace is 50 km, then a +/-260 km swath has
stopped measuring Hubbell Spring and started measuring the Rio Grande rift -- a tighter
number about a different subject.

So: measure the mapped trace length from USGS Qfaults and let it set the maximum
honest aperture. Reports every Quaternary fault in the box by length and by summed
strike-parallel extent, so the answer is not one hand-picked polyline.
"""
import json, math, urllib.request, urllib.parse, sys, os
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

BBOX = "-107.2,34.2,-106.0,35.6"
CACHE = "work/abq_qfaults.geojson"
EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/12/query"
R = 6371.0


def hav(p, q):
    la1, lo1, la2, lo2 = map(math.radians, (p[1], p[0], q[1], q[0]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))


if os.path.exists(CACHE):
    d = json.load(open(CACHE))
else:
    q = dict(where="1=1", geometry=BBOX, geometryType="esriGeometryEnvelope", inSR="4326",
             spatialRel="esriSpatialRelIntersects", outFields="*",
             returnGeometry="true", outSR="4326", f="geojson")
    req = urllib.request.Request(EP + "?" + urllib.parse.urlencode(q),
                                 headers={"User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    open(CACHE, "w").write(json.dumps(d))

byname = {}
for ft in d.get("features", []):
    pr = ft.get("properties", {})
    nm = pr.get("name") or pr.get("NAME") or pr.get("fault_name") or "(unnamed)"
    g = ft.get("geometry") or {}
    lines = []
    if g.get("type") == "LineString":
        lines = [g["coordinates"]]
    elif g.get("type") == "MultiLineString":
        lines = g["coordinates"]
    L = 0.0
    pts = []
    for ln in lines:
        for i in range(1, len(ln)):
            L += hav(ln[i-1], ln[i])
        pts.extend(ln)
    e = byname.setdefault(nm, {"len_km": 0.0, "pts": [],
                               "age": pr.get("age") or pr.get("AGE") or
                                      pr.get("recency") or pr.get("agecode")})
    e["len_km"] += L
    e["pts"].extend(pts)

rows = []
for nm, e in byname.items():
    if not e["pts"]:
        continue
    lats = [p[1] for p in e["pts"]]; lons = [p[0] for p in e["pts"]]
    # end-to-end extent of the mapped trace (not the summed wiggle)
    ext = hav((min(lons), min(lats)), (max(lons), max(lats)))
    rows.append({"name": nm, "traced_len_km": round(e["len_km"], 1),
                 "endpoint_extent_km": round(ext, 1),
                 "lat_range": [round(min(lats), 3), round(max(lats), 3)],
                 "age": e["age"], "n_vertices": len(e["pts"])})
rows.sort(key=lambda r: -r["endpoint_extent_km"])

hub = [r for r in rows if "hubbell" in r["name"].lower()]
out = {"bbox": BBOX, "n_named_faults": len(rows),
       "hubbell": hub, "longest_10": rows[:10]}
if hub:
    ext = max(r["endpoint_extent_km"] for r in hub)
    out["max_honest_along_strike_halfwidth_km"] = round(ext/2, 1)
    out["verdict"] = (f"Hubbell Spring mapped extent {ext:.1f} km -> a swath wider than "
                      f"+/-{ext/2:.1f} km along strike is no longer profiling this fault.")
print(json.dumps(out, indent=2))
print(json.dumps({k: out[k] for k in out if k != "longest_10"}, indent=2), file=sys.stderr)
