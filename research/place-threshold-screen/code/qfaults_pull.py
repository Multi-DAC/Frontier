"""USGS Qfaults puller WITH PAGING, plus slip-rate extraction.

Why this file exists: the first ABQ pull returned exactly 2000 features. 2000 is the
ArcGIS maxRecordCount, not a fault count -- the query was silently truncated and I
nearly read a clipped sample as "the faults in the box". Everything downstream pages.

Second correction: the layer carries `slip_rate` and `total_fault_length` per section.
Both surveys so far have scored faults by Quaternary AGE CLASS (10^4-10^6 yr clock),
which is exactly the "driver nobody measured" the D196 dossier named. slip_rate is the
driver, published, per section, and it was one field away the whole time.
"""
import json, math, urllib.request, urllib.parse, os, sys, re
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/12/query"
R = 6371.0
PAGE = 1000


def hav_ll(lat1, lon1, lat2, lon2):
    la1, lo1, la2, lo2 = map(math.radians, (lat1, lon1, lat2, lon2))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))


def pull_bbox(lon0, lat0, lon1, lat1, cache=None):
    if cache and os.path.exists(cache):
        return json.load(open(cache))
    feats, off = [], 0
    while True:
        q = dict(where="1=1", geometry=f"{lon0},{lat0},{lon1},{lat1}",
                 geometryType="esriGeometryEnvelope", inSR="4326",
                 spatialRel="esriSpatialRelIntersects", outFields="*",
                 returnGeometry="true", outSR="4326", f="geojson",
                 resultOffset=off, resultRecordCount=PAGE)
        req = urllib.request.Request(EP + "?" + urllib.parse.urlencode(q),
                                     headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=180))
        got = d.get("features", [])
        feats.extend(got)
        if len(got) < PAGE:
            break
        off += PAGE
        if off > 40000:
            print("[warn] paging cap hit", file=sys.stderr)
            break
    out = {"type": "FeatureCollection", "features": feats}
    if cache:
        open(cache, "w").write(json.dumps(out))
    return out


SLIP_MID = {  # USGS Qfaults slip-rate categories -> representative mm/yr
    "greater than 5.0 mm/yr": 7.5,
    "between 5.0 and 1.0 mm/yr": 3.0,
    "between 1.0 and 0.2 mm/yr": 0.6,
    "less than 0.2 mm/yr": 0.1,
    "unspecified": None, "unknown": None,
}


def slip_mid(s):
    if not s:
        return None
    k = s.strip().lower()
    for pat, v in SLIP_MID.items():
        if pat in k:
            return v
    nums = [float(x) for x in re.findall(r"[\d.]+", k)]
    if "greater" in k and nums:
        return nums[0]*1.5
    if "less" in k and nums:
        return nums[0]/2
    if len(nums) >= 2:
        return (nums[0]+nums[1])/2
    return nums[0] if nums else None


def verts(ft):
    g = ft.get("geometry") or {}
    if g.get("type") == "LineString":
        return g["coordinates"]
    if g.get("type") == "MultiLineString":
        return [p for ln in g["coordinates"] for p in ln]
    return []


def nearest(lat, lon, fc, max_km=200.0):
    """Nearest Qfaults section to a point. Returns distance, name, age, slip-rate."""
    best = None
    for ft in fc.get("features", []):
        p = ft["properties"]
        for c in verts(ft):
            d = hav_ll(lat, lon, c[1], c[0])
            if best is None or d < best[0]:
                best = (d, p)
    if best is None or best[0] > max_km:
        return None
    d, p = best
    return {"dist_km": round(d, 2),
            "fault_name": p.get("fault_name"), "section": p.get("section_name"),
            "age": p.get("age"), "slip_rate_class": p.get("slip_rate"),
            "slip_rate_mm_yr": slip_mid(p.get("slip_rate")),
            "total_fault_length_km": p.get("total_fault_length"),
            "slip_sense": p.get("slip_sense")}


def best_driver(lat, lon, fc, r_km=25.0):
    """Highest published slip rate on any section within r_km -- the DRIVER layer,
    from the fault database rather than from an age class."""
    hits = []
    for ft in fc.get("features", []):
        p = ft["properties"]
        dmin = min((hav_ll(lat, lon, c[1], c[0]) for c in verts(ft)), default=1e9)
        if dmin <= r_km:
            sm = slip_mid(p.get("slip_rate"))
            hits.append({"dist_km": round(dmin, 2), "fault_name": p.get("fault_name"),
                         "slip_rate_class": p.get("slip_rate"), "slip_rate_mm_yr": sm,
                         "age": p.get("age")})
    rated = [h for h in hits if h["slip_rate_mm_yr"] is not None]
    rated.sort(key=lambda h: -h["slip_rate_mm_yr"])
    return {"n_sections_within_r": len(hits), "n_with_published_slip_rate": len(rated),
            "max_slip_rate_mm_yr": rated[0]["slip_rate_mm_yr"] if rated else None,
            "fastest": rated[0] if rated else None,
            "nearest": min(hits, key=lambda h: h["dist_km"]) if hits else None}


if __name__ == "__main__":
    fc = pull_bbox(-107.2, 34.2, -106.0, 35.6, "work/abq_qfaults_paged.geojson")
    fs = fc["features"]
    print(f"features (paged): {len(fs)}")
    names = {}
    for ft in fs:
        n = ft["properties"].get("fault_name") or "(unnamed)"
        names[n] = names.get(n, 0) + 1
    print(f"named faults: {len(names)}")
    hub = [n for n in names if "hubbell" in n.lower()]
    print("HUBBELL MATCHES:", hub)
    for n in sorted(names):
        print(f"   {names[n]:>5}  {n}")
    for tag, la, lo in (("Hubbell Spring pin", 34.90, -106.53),
                        ("Sandia W scarp", 35.10, -106.51),
                        ("Tijeras control", 35.06, -106.36)):
        print(f"\n== {tag}")
        print("   nearest:", json.dumps(nearest(la, lo, fc)))
        print("   driver :", json.dumps(best_driver(la, lo, fc)))
