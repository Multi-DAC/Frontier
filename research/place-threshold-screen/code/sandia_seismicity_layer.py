"""Sandia/Manzano portal pins — seismicity layer (USGS ComCat), Day 196.

New independent layer on the D138 pin set. Motivation: the mechanism's piezo term
requires STRAIN RELEASE in quartz-rich granite, and Paiva & Taft's dusty-plasma
reading of the Hessdalen spectrum (D196 note) invokes a tectonic-stress field
E ~ 1.5e5 V/m. Seismicity is therefore the shared driver of BOTH the transport-class
mechanism AND the competing published explanation of the only instrumented analogue.

The D138 survey never measured it. Pins were scored on faults+gravity+lithology only
-- i.e. on structures that are Quaternary-active on a 10^4-10^6 yr clock, with no
check of whether anything is moving NOW.

POSITIVE CONTROL is built in: Socorro (the Socorro Magma Body / seismic anomaly,
~90 km south, same rift) must come back HOT or the query is broken. A dead-flat
oceanic cell must come back EMPTY or the radius/area math is broken.
"""
import json, gzip, math, sys, urllib.request
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

SITES = [
    # name,                          lat,     lon,     role
    ("PRIMARY  Hubbell Spring",     34.90,  -106.53, "pin: latest-Q fault, granite 2.3km, Bennewitz locus"),
    ("SECONDARY Sandia W scarp",    35.10,  -106.51, "pin: best piezo (quartz-monzonite), late-Q"),
    ("CONTROL  Tijeras corridor",   35.17,  -106.32, "blind control: geophysics without anomaly record"),
    ("FLOOR    regional Bouguer low",35.20, -106.72, "FLOOR-class: unscreening, no piezo"),
    ("POSCTRL  Socorro magma body", 34.10,  -106.90, "positive control: must be HOT"),
    ("NEGCTRL  mid-Pacific",        30.00,  -140.00, "negative control: must be EMPTY"),
]
RADIUS_KM = 15.0
START = "1970-01-01"
END = "2026-08-15"

def fetch(lat, lon, radius_km):
    url = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
           f"&starttime={START}&endtime={END}"
           f"&latitude={lat}&longitude={lon}&maxradiuskm={radius_km}"
           "&minmagnitude=-1&orderby=time&limit=20000")
    req = urllib.request.Request(url, headers={"User-Agent": "clawd-carapace/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return json.loads(raw)

def summarize(name, role, gj):
    feats = gj.get("features", [])
    mags = [f["properties"]["mag"] for f in feats if f["properties"].get("mag") is not None]
    deps = [f["geometry"]["coordinates"][2] for f in feats
            if f["geometry"]["coordinates"][2] is not None]
    area = math.pi * RADIUS_KM**2
    yrs = 56.6
    n = len(feats)
    out = {
        "site": name, "role": role, "n": n,
        "per_1000km2_per_decade": round(n / area * 1000 / (yrs/10.0), 2),
        "max_mag": max(mags) if mags else None,
        "n_M3plus": sum(1 for m in mags if m >= 3.0),
        "median_depth_km": round(sorted(deps)[len(deps)//2], 1) if deps else None,
        "n_shallow_lt10km": sum(1 for d in deps if d < 10.0),
        "most_recent": (feats[0]["properties"]["time"] if feats else None),
    }
    return out

rows = []
for name, lat, lon, role in SITES:
    try:
        gj = fetch(lat, lon, RADIUS_KM)
        rows.append(summarize(name, role, gj))
        print(f"ok  {name:28s} n={len(gj.get('features',[]))}", file=sys.stderr)
    except Exception as e:
        print(f"ERR {name}: {e}", file=sys.stderr)
        rows.append({"site": name, "role": role, "n": "QUERY FAILED", "err": str(e)})

import datetime
print(json.dumps(rows, indent=2))
hdr = f"{'site':30s} {'N':>6s} {'rate/1000km2/dec':>17s} {'Mmax':>5s} {'M>=3':>5s} {'med_z':>6s} {'z<10km':>7s}"
print(hdr, file=sys.stderr)
for r in rows:
    if r["n"] == "QUERY FAILED":
        print(f"{r['site']:30s}  QUERY FAILED", file=sys.stderr); continue
    print(f"{r['site']:30s} {r['n']:6d} {r['per_1000km2_per_decade']:17.2f} "
          f"{str(r['max_mag']):>5s} {r['n_M3plus']:5d} {str(r['median_depth_km']):>6s} "
          f"{r['n_shallow_lt10km']:7d}", file=sys.stderr)
