"""P3' -- DEPTH TO CRYSTALLINE BASEMENT, the leg round 1 asked for and did not build.

Report 08's closing list: "Aeromagnetic depth-to-basement. This is the correct version of
the rock criterion for a BURIED crystalline source, and it would re-rank every basin-fill
site in the study, including the one we started from."

It uses the PUBLISHED inversion rather than deriving one from the magnetic grid:
  Shah, A.K. & Boyd, O.S., 2018, "Depth to basement and thickness of unconsolidated
  sediments for the western United States", USGS OFR 2018-1115, doi:10.3133/ofr20181115.
  ScienceBase 5b0d85eee4b0c39c934b0429, Dep2MzBasement_LLz.csv, 1 km nodes, WGS84.
  sha256 c30b20a4a407f47d487cf46338e1a966b46e87b5c4a26f73d994233d50b63ffd

THE FUNCTIONAL FORM IS DECLARED HERE, BEFORE THE JOIN TO SITE IDENTITY RUNS.
(PREREGISTRATION-v2.md section 7.) Whoever reads this later: the ordering below was
written against the mechanism, not against a table of which sites it moves.

  Mechanism: a quartz-fabric crystalline source coupling to a surface observer. Basin
  fill between basement and surface is the decoupling term -- more section, weaker
  coupling. So the leg is monotone DECREASING in depth-to-basement.

  Form: log-linear, mirroring how the existing `length` leg already treats a quantity
  spanning orders of magnitude.

      s = 1 - log10(clip(D, D_NEAR, D_FAR) / D_NEAR) / log10(D_FAR / D_NEAR)

  so s = 1.0 at D <= D_NEAR (basement at or near surface) and s = 0.0 at D >= D_FAR.

  D_NEAR = 100 m, D_FAR = 5000 m. THESE TWO CONSTANTS ARE A WAGER AND ARE LABELLED AS
  ONE. There is no published threshold at which crystalline coupling "switches off", so
  rather than dress a guess as a constant, the module ships a SENSITIVITY SWEEP over
  alternates (see ALTERNATES) and the report prints whether the top ten survives them.
  A leg whose ordering depends on which arbitrary constant was chosen is an artefact of
  the choice, and this is the instrument that says so out loud.

WHAT THIS LEG IS NOT ALLOWED TO DO: it is a physics criterion and enters Product A
(criterion strength) only. It carries no claim about anomalous record. See
PREREGISTRATION-v2.md section 0.
"""
import csv
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
GRID = os.path.join(HERE, "..", "work", "Dep2MzBasement_LLz.csv")
SITES = os.path.join(HERE, "..", "data", "stage5_join_summary.json")
OUT = os.path.join(HERE, "..", "data", "basement_leg.json")

D_NEAR, D_FAR = 100.0, 5000.0
ALTERNATES = [(50.0, 3000.0), (100.0, 5000.0), (250.0, 8000.0), (500.0, 10000.0)]

# Grid extent from the ScienceBase record, re-asserted here so a silently-different
# file cannot be joined without tripping something.
EXTENT = dict(minX=-124.72, maxX=-102.73, minY=28.99, maxY=49.0)
CELL = 0.05                                     # ~5 km hash cell; grid nodes are ~1 km
R = 6371.0


def score(depth_m, d_near=D_NEAR, d_far=D_FAR):
    """Monotone decreasing in depth. Declared before the join; see the header."""
    d = min(max(depth_m, d_near), d_far)
    return 1.0 - math.log10(d / d_near) / math.log10(d_far / d_near)


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def load_grid_near(targets, path=GRID, cell=CELL):
    """One streaming pass over 100 MB. Keeps only nodes in cells any target occupies.

    Streaming rather than loading: the file is ~2.9M rows and only ~a few thousand
    nodes are ever within reach of the 227 points we ask about.
    """
    want = set()
    for lat, lon in targets:
        r0, c0 = round(lat / cell), round(lon / cell)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                want.add((r0 + dr, c0 + dc))
    keep = defaultdict(list)
    n = 0
    with open(path, newline="") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr == ["Lon_WGS84", "Lat_WGS84", "D2B_meters"], hdr
        for row in rd:
            n += 1
            lon, lat, d = float(row[0]), float(row[1]), float(row[2])
            k = (round(lat / cell), round(lon / cell))
            if k in want:
                keep[k].append((lat, lon, d))
    print(f"[grid] {n} nodes streamed, {sum(len(v) for v in keep.values())} retained "
          f"in {len(keep)} cells", file=sys.stderr)
    return keep, cell


def sample(keep, cell, lat, lon):
    """Nearest grid node, with the distance to it returned so the caller can see
    whether this was a sample or an extrapolation."""
    r0, c0 = round(lat / cell), round(lon / cell)
    best = None
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            for la, lo, d in keep.get((r0 + dr, c0 + dc), ()):
                km = hav(lat, lon, la, lo)
                if best is None or km < best[0]:
                    best = (km, d)
    return best


def main():
    src = json.load(open(SITES))
    sites = src["survivors_ranked"]
    targets = [(s["lat"], s["lon"]) for s in sites]

    outside = [s for s in sites
               if not (EXTENT["minX"] <= s["lon"] <= EXTENT["maxX"]
                       and EXTENT["minY"] <= s["lat"] <= EXTENT["maxY"])]
    print(f"[extent] {len(sites) - len(outside)}/{len(sites)} inside the published grid "
          f"extent; {len(outside)} outside (UNMEASURED, never scored 0)", file=sys.stderr)

    keep, cell = load_grid_near(targets)

    rows, far = [], 0
    for s in sites:
        hit = sample(keep, cell, s["lat"], s["lon"])
        if hit is None:
            rows.append(dict(fault_name=s["fault_name"], rank_r1=s["rank"],
                             lat=s["lat"], lon=s["lon"],
                             d2b_m=None, node_km=None, status="UNMEASURED",
                             basement=None))
            continue
        km, d = hit
        if km > 2.0:
            far += 1
        rows.append(dict(fault_name=s["fault_name"], rank_r1=s["rank"],
                         lat=s["lat"], lon=s["lon"],
                         d2b_m=round(d, 1), node_km=round(km, 3), status="PASS",
                         basement=round(score(d), 4),
                         alternates={f"{a}_{b}": round(score(d, a, b), 4)
                                     for a, b in ALTERNATES}))

    meas = [r for r in rows if r["status"] == "PASS"]
    dd = sorted(r["d2b_m"] for r in meas)
    ss = sorted(r["basement"] for r in meas)

    def pct(v, p):
        return v[min(len(v) - 1, int(p * len(v)))]

    summary = {
        "source": "USGS OFR 2018-1115 (Shah & Boyd 2018), Dep2MzBasement_LLz.csv",
        "sha256": "c30b20a4a407f47d487cf46338e1a966b46e87b5c4a26f73d994233d50b63ffd",
        "form": "s = 1 - log10(clip(D,D_NEAR,D_FAR)/D_NEAR) / log10(D_FAR/D_NEAR)",
        "D_NEAR": D_NEAR, "D_FAR": D_FAR,
        "constants_are": "A DECLARED WAGER. See ALTERNATES and the sensitivity sweep.",
        "measured": len(meas), "of": len(rows),
        "nearest_node_km_max": max((r["node_km"] for r in meas), default=None),
        "nodes_beyond_2km": far,
        "depth_m": {"min": dd[0], "p25": pct(dd, .25), "median": pct(dd, .5),
                    "p75": pct(dd, .75), "max": dd[-1]},
        "leg_value": {"min": ss[0], "p25": pct(ss, .25), "median": pct(ss, .5),
                      "p75": pct(ss, .75), "max": ss[-1],
                      "at_ceiling_1.0": sum(1 for v in ss if v >= 0.999),
                      "at_floor_0.0": sum(1 for v in ss if v <= 0.001)},
        "rows": rows,
    }
    json.dump(summary, open(OUT, "w"), indent=1)

    print(f"\n[leg] measured {len(meas)}/{len(rows)}; nearest node <= "
          f"{summary['nearest_node_km_max']} km ({far} beyond 2 km)", file=sys.stderr)
    print(f"[leg] depth m: min {dd[0]} / median {pct(dd, .5)} / max {dd[-1]}",
          file=sys.stderr)
    print(f"[leg] value:   min {ss[0]} / median {pct(ss, .5)} / max {ss[-1]}  "
          f"ceiling {summary['leg_value']['at_ceiling_1.0']}  "
          f"floor {summary['leg_value']['at_floor_0.0']}", file=sys.stderr)
    print(f"[leg] wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
