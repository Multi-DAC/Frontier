"""Does the D196 seismicity ordering survive (a) catalog completeness and (b) Poisson noise?

n=1 vs n=4 is a difference I do not get to call a result without checking both.
"""
import json, math, sys, urllib.request
from math import lgamma, exp, log
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

SITES = [
    ("PRIMARY  Hubbell Spring",   34.90, -106.53),
    ("SECONDARY Sandia W scarp",  35.10, -106.51),
    ("CONTROL  Tijeras corridor", 35.17, -106.32),
    ("FLOOR    Bouguer low",      35.20, -106.72),
    ("POSCTRL  Socorro",          34.10, -106.90),
]

def fetch(lat, lon, r_km, minmag):
    url = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
           f"&starttime=1980-01-01&endtime=2026-08-15"
           f"&latitude={lat}&longitude={lon}&maxradiuskm={r_km}"
           f"&minmagnitude={minmag}&limit=20000")
    req = urllib.request.Request(url, headers={"User-Agent": "clawd-carapace/1.0"})
    with urllib.request.urlopen(req, timeout=120) as rq:
        return json.loads(rq.read())

def poisson_cdf(k, lam):
    return sum(exp(-lam + i*log(lam) - lgamma(i+1)) for i in range(k+1)) if lam > 0 else 1.0

# 1. Completeness proxy: magnitude histogram over the whole rift bbox.
#    If the catalog rolls over well above M2, small-N site counts are detection-limited.
gj = fetch(35.0, -106.6, 120, -1)
mags = sorted(f["properties"]["mag"] for f in gj["features"]
              if f["properties"].get("mag") is not None)
hist = {}
for m in mags:
    b = round(math.floor(m*2)/2, 1)
    hist[b] = hist.get(b, 0) + 1
print("REGIONAL MAGNITUDE HISTOGRAM (120 km of 35.0,-106.6; 1980-2026), N=%d" % len(mags))
for b in sorted(hist):
    print(f"  M {b:5.1f}  {hist[b]:5d}  {'#'*min(60, hist[b])}")
peak = max(hist, key=lambda b: hist[b])
print(f"  -> histogram peaks at M{peak}; catalog is NOT complete below roughly that.\n")

# 2. Site counts at three magnitude floors and two radii.
print("SITE COUNTS BY (radius, minmag)")
grid = [(15, 2.5), (25, 2.5), (25, 3.0), (40, 3.0)]
counts = {}
for name, lat, lon in SITES:
    row = []
    for r_km, mm in grid:
        n = len(fetch(lat, lon, r_km, mm)["features"])
        row.append(n)
    counts[name] = row
    print(f"  {name:28s} " + "  ".join(f"r{r}/M{mm}={n:3d}" for (r, mm), n in zip(grid, row)))

# 3. Poisson: is PRIMARY's deficit vs SECONDARY distinguishable from noise?
print("\nPOISSON CHECK  (H0: same rate; is PRIMARY's count low by chance?)")
for i, (r_km, mm) in enumerate(grid):
    k1 = counts["PRIMARY  Hubbell Spring"][i]
    k2 = counts["SECONDARY Sandia W scarp"][i]
    if k1 + k2 == 0:
        print(f"  r{r_km}/M{mm}: both zero - no information"); continue
    # binomial test, equal areas => p=0.5 under H0
    n, k = k1 + k2, k1
    p = sum(math.comb(n, j) for j in range(0, k+1)) / 2**n
    print(f"  r{r_km}/M{mm}: PRIMARY={k1} SECONDARY={k2}  one-sided p={p:.3f}"
          f"  {'-> NOT significant' if p > 0.05 else '-> significant'}")
