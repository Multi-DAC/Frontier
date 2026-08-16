#!/usr/bin/env python
"""Socorro cell — the D138 four-layer pin method, run on the cell D138 never surveyed.

WHY THIS CELL. The D196 seismicity layer found all three Albuquerque-rift pins
(Hubbell Spring, Sandia scarp, Tijeras) statistically indistinguishable from zero at
completeness-safe magnitudes (M>=2.5, post-1980), while the Socorro cell -- included
only as a POSITIVE CONTROL to prove the query worked -- returned 19-30 events in the
same window. The mechanism's piezo term needs strain release NOW; the D138 survey
scored faults on a Quaternary (10^4-10^6 yr) clock and never checked the modern rate.
So the control outscored the pins on the one layer nobody had measured, and the honest
response is to run the pins' own instrument on it rather than to argue.

SAME METHOD, DELIBERATELY. Identical scoring to sandia_pin_analysis.py (D138) so the
numbers are comparable: USGS Qfaults + CONUS Bouguer grid, granite proxied by high
Bouguer, pin = local Bouguer minimum minimizing (granite_km + active_fault_km).
The granite-by-density proxy is CRUDE and is carried over ONLY for comparability.
"""
import json, math, os, gzip, urllib.request, urllib.parse, sys
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

SRC = r"C:\Users\mercu\clawd\repo-staging\Corpus-Perspectival\Unreleased-Work"
LON0, LON1, LAT0, LAT1 = -107.4, -106.4, 33.6, 34.6
BBOX = f"{LON0},{LAT0},{LON1},{LAT1}"
CACHE = "socorro_qfaults.geojson"
EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/12/query"


def pull():
    q = dict(where="1=1", geometry=BBOX, geometryType="esriGeometryEnvelope", inSR="4326",
             spatialRel="esriSpatialRelIntersects", outFields="*",
             returnGeometry="true", outSR="4326", f="geojson")
    req = urllib.request.Request(EP + "?" + urllib.parse.urlencode(q),
                                 headers={"User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    open(CACHE, "w").write(json.dumps(d))
    return d


def hav(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def load_bouguer():
    pts = []
    with gzip.open(os.path.join(SRC, "bouguer.xyz.gz"), "rt") as f:
        for line in f:
            p = line.split()
            if len(p) < 3:
                continue
            lo, la, mg = float(p[0]), float(p[1]), float(p[2])
            if LON0 <= lo <= LON1 and LAT0 <= la <= LAT1:
                pts.append((la, lo, mg))
    return pts


def local_minima(pts, radius_km=9.0):
    mins = []
    for i, (la, lo, mg) in enumerate(pts):
        if all(not (hav((la, lo), (la2, lo2)) <= radius_km and mg2 < mg)
               for j, (la2, lo2, mg2) in enumerate(pts) if i != j):
            mins.append((la, lo, mg))
    return mins


def fault_vertices(d):
    out = []
    for ft in d["features"]:
        p = ft["properties"]
        name = p.get("fault_name") or p.get("name") or ""
        age = p.get("age") or p.get("recency") or ""
        dip = p.get("dip_direction") or p.get("dip") or ""
        c = (ft.get("geometry") or {}).get("coordinates", [])
        if not c:
            continue
        pts = [v for ln in c for v in ln] if isinstance(c[0][0], list) else c
        out.extend((v[1], v[0], name, age, "", dip) for v in pts)
    return out


def main():
    d = json.load(open(CACHE)) if os.path.exists(CACHE) else pull()
    bg = load_bouguer()
    mgs = [m for _, _, m in bg]
    print("=" * 78)
    print("SOCORRO CELL — D138 four-layer pin method (the cell D138 did not survey)")
    print("=" * 78)
    print(f"Bouguer points in bbox: {len(bg)}  range {min(mgs):.1f} to {max(mgs):.1f} mGal")
    basin = min(bg, key=lambda t: t[2]); hi = max(bg, key=lambda t: t[2])
    print(f"REGIONAL LOW  (max unscreening): {basin[0]:.4f}, {basin[1]:.4f}  {basin[2]:.1f} mGal")
    print(f"REGIONAL HIGH (piezo/range core): {hi[0]:.4f}, {hi[1]:.4f}  {hi[2]:.1f} mGal")

    mins = sorted(local_minima(bg), key=lambda t: t[2])
    print(f"\nLOCAL Bouguer MINIMA (omega_pin localization sites): {len(mins)}")
    for la, lo, mg in mins[:8]:
        print(f"   {la:.4f}, {lo:.4f}   {mg:.1f} mGal")

    fv = fault_vertices(d)
    names = sorted(set(v[2] for v in fv if v[2]))
    print(f"\nNM Quaternary faults in bbox: {len(fv)} vertices / {len(names)} named")
    for nm in names:
        s = next(v for v in fv if v[2] == nm)
        print(f"   - {nm}  (age='{s[3]}')")

    # granite proxy: densest quartile of the local grid (same rule shape as D138)
    thresh = sorted(mgs)[int(0.75 * len(mgs))]
    dense = [(la, lo) for la, lo, mg in bg if mg > thresh]
    print(f"\n[granite proxy] densest-quartile threshold = {thresh:.1f} mGal, {len(dense)} pts")

    def gdist(p): return min(hav(p, q) for q in dense)
    ACTIVE = [v for v in fv if "late" in (v[3] or "").lower()]
    print(f"[conduit] late/latest-Quaternary vertices: {len(ACTIVE)}")
    if not ACTIVE:
        print("   !! NO late-Quaternary faults in this cell — layer 4 FAILS here.")
    def fdist(p): return min(hav((v[0], v[1]), p) for v in ACTIVE) if ACTIVE else float("nan")

    scored = []
    for la, lo, mg in mins:
        gd, fd = gdist((la, lo)), fdist((la, lo))
        scored.append((gd + fd, la, lo, mg, gd, fd))
    scored.sort(key=lambda t: (math.isnan(t[0]), t[0]))
    print("\nSOCORRO CELL — ranked by granite+fault convergence at a density low")
    for score, la, lo, mg, gd, fd in scored[:5]:
        nf = min(ACTIVE, key=lambda v: hav((v[0], v[1]), (la, lo)))[2] if ACTIVE else "n/a"
        print(f"   {la:.4f}, {lo:.4f}  {mg:.0f}mGal | granite {gd:.1f}km | "
              f"active-fault {fd:.1f}km ('{nf}') | conv {score:.1f}")

    # Where does the seismicity actually sit, and where is the Zamora arroyo?
    print("\nREFERENCE POINTS")
    for nm, la, lo in [("Socorro town", 34.0584, -106.8914),
                       ("seismicity centroid probe (POSCTRL)", 34.10, -106.90),
                       ("Zamora arroyo (APPROX, 'S of Socorro' — coords NOT verified)", 34.03, -106.89)]:
        nlo = min(mins, key=lambda m: hav((m[0], m[1]), (la, lo)))
        print(f"   {nm:58s} {la:.4f},{lo:.4f} | granite {gdist((la,lo)):.1f}km | "
              f"active-fault {fdist((la,lo)):.1f}km | nearest low {nlo[2]:.0f}mGal @ {hav((nlo[0],nlo[1]),(la,lo)):.1f}km")


if __name__ == "__main__":
    main()
