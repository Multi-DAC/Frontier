"""Re-pull USGS Qfaults across the whole western grid extent, tiled and cached.

WHY: two reasons, and the second is the one that matters.

(1) D8. PREREGISTRATION-v2.md section 8 says round 2 does not ship while
    `qfaults_normal_national.geojson` is referenced by path and absent from disk. This
    regenerates that input from the live service with a recorded manifest.

(2) A6 needs a fault-distance measurement at coordinates that are NOT in the screen's
    own population -- the frozen positive-control locales and the seeded null. The
    screen's node list cannot answer "how far is the nearest Quaternary normal fault
    from an arbitrary point"; only the fault geometry can.

This file acquires RAW DATA ONLY. It reads no site identity, computes no score, and is
deliberately separable from `positive_control.py`, which carries the declaration and is
committed before anything is scored.

TILED because the ArcGIS layer silently truncates at maxRecordCount and the puller's own
docstring records that lesson. Each tile is paged to exhaustion and cached by name, so a
re-run is free and a partial run is resumable.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qfaults_pull  # noqa: E402
from qfaults_pull import pull_bbox  # noqa: E402

# ---------------------------------------------------------------------------
# THE LAYER, AND WHY IT IS NAMED HERE RATHER THAN INHERITED.
#
# `qfaults_pull.EP` points at MapServer LAYER 12. Layer 12 is NEW MEXICO. The service's
# layer list is per-state -- 0 Individual States, 2 Arizona, 3-5 California, 8 Idaho,
# 10 Montana, 11 Nevada, 12 NEW MEXICO, ..., 21 NATIONAL DATABASE. Layer 12 was the
# right choice for the Albuquerque work this module's parent was written for, and it is
# silently wrong for anything national.
#
# THE FIRST RUN OF THIS FILE INHERITED IT AND PULLED 16,189 SECTIONS -- a plausible,
# non-empty, entirely New Mexican answer. What caught it was ONLY that the run is TILED
# and prints per-tile counts: Nevada returned 0, California returned 0, Idaho returned 0.
# A single-bbox pull would have returned the same 16,189 features with nothing to read
# them against, and the fault-distance measurement downstream would have been a
# measurement of New Mexico wearing a national label.
#
# `dossier_html.py:529` already states "layer 21, complete national pull" for the 1,399
# CONUS node population, and the survivors do span MT/NV/WA/CA, so THE PUBLISHED
# POPULATION IS NOT AFFECTED. What is affected is `national_site_screen.py:39`, which
# also carries layer 12 and writes its stage-1 cache to a file named
# `qfaults_fast_national.geojson`. That cache is absent from disk (a D8 casualty), so
# what it contained cannot now be read -- recorded as an open question, not a verdict.
# ---------------------------------------------------------------------------
LAYER = 21
qfaults_pull.EP = ("https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/"
                   f"MapServer/{LAYER}/query")

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..", "work", f"qfaults_tiles_L{LAYER}")
OUT = os.path.join(HERE, "..", "work", "qfaults_west.geojson")

# The Shah & Boyd (2018) grid extent, rounded outward by a degree so a fault just
# outside the grid can still be the nearest fault to a point just inside it.
LON0, LON1 = -126.0, -101.0
LAT0, LAT1 = 28.0, 50.0
STEP = 5.0


def tiles():
    lon = LON0
    while lon < LON1:
        lat = LAT0
        while lat < LAT1:
            yield (lon, lat, min(lon + STEP, LON1), min(lat + STEP, LAT1))
            lat += STEP
        lon += STEP


def main():
    os.makedirs(WORK, exist_ok=True)
    seen, feats = set(), []
    for i, (lo0, la0, lo1, la1) in enumerate(tiles()):
        cache = os.path.join(WORK, f"t_{lo0:.0f}_{la0:.0f}.geojson")
        fc = pull_bbox(lo0, la0, lo1, la1, cache=cache)
        n = len(fc.get("features", []))
        new = 0
        for ft in fc["features"]:
            # tiles overlap at their shared edge; dedupe on the service's own object id
            oid = (ft.get("id")
                   or ft["properties"].get("objectid")
                   or ft["properties"].get("OBJECTID")
                   or json.dumps(ft["geometry"], sort_keys=True))
            if oid in seen:
                continue
            seen.add(oid)
            feats.append(ft)
            new += 1
        print(f"[{i:2d}] {lo0:7.1f},{la0:5.1f} -> {n:5d} features, {new:5d} new "
              f"(running {len(feats)})", flush=True)

    # ---- POSITIVE CONTROL ON THE PULL ITSELF ---------------------------------
    # A zero needs a positive control. Nevada and California are the two densest
    # Quaternary normal-fault provinces in the country; a national pull that returns
    # nothing in either has failed, and failed QUIETLY, which is the only way this
    # particular mistake ever presents. Fails loudly rather than writing the file.
    probes = {"Nevada (Basin and Range)": (-119.0, 38.0, -115.0, 41.0),
              "California (eastern Sierra)": (-120.0, 36.0, -117.0, 38.5),
              "Idaho/Montana (Lost River, Beaverhead)": (-115.0, 43.5, -111.0, 46.0)}
    print("\n  PULL POSITIVE CONTROL -- features falling inside known-dense boxes:")
    bad = []
    for label, (lo0, la0, lo1, la1) in probes.items():
        n = 0
        for ft in feats:
            for c in (ft.get("geometry") or {}).get("coordinates", []) or []:
                pts = [c] if isinstance(c[0], (int, float)) else c
                if any(lo0 <= p[0] <= lo1 and la0 <= p[1] <= la1 for p in pts):
                    n += 1
                    break
        print(f"    {n:6d}  {label}")
        if n == 0:
            bad.append(label)
    if bad:
        print(f"\n  FAILED: zero features in {bad}. This is the layer-12 signature. "
              f"NOT writing {OUT}.", file=sys.stderr)
        raise SystemExit(2)

    out = {"type": "FeatureCollection", "features": feats}
    with open(OUT, "w") as f:
        json.dump(out, f)
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16]
    print(f"\nWROTE {OUT}")
    print(f"  features : {len(feats)}")
    print(f"  sha256   : {h}")

    senses = {}
    ages = {}
    for ft in feats:
        p = ft["properties"]
        senses[p.get("slip_sense")] = senses.get(p.get("slip_sense"), 0) + 1
        ages[p.get("age")] = ages.get(p.get("age"), 0) + 1
    print("\n  slip_sense census (this is the NORMAL filter's raw material):")
    for k, v in sorted(senses.items(), key=lambda kv: -kv[1]):
        print(f"    {v:6d}  {k}")
    print("\n  age census:")
    for k, v in sorted(ages.items(), key=lambda kv: -kv[1]):
        print(f"    {v:6d}  {k}")


if __name__ == "__main__":
    main()
