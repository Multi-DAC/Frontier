"""RANK the physics-only screen's survivors, and add the one criterion the screen lacked.

Input: work/transport_screen_stage2.json -- 62 of 507 CONUS dilatant-Quaternary nodes whose
rock is quartz-rich AT the trace point.

What this adds, and why it is a physics criterion rather than an instrument one:

  P4 JUNCTION -- how many DISTINCT dilatant fault systems have mapped trace within 15 km.
                 A fault intersection is a permeability maximum: two conjugate damage zones
                 sharing a volume is the standard structural control on geothermal upflow,
                 and it is the property that survived Addendum 3's deflation at Sandia (the
                 ~34.98N result was 'where the Hubbell system runs into the Sandia system').
                 Counted from the SAME cached national pull, so no new network call and no
                 new population.

  ⚠ P4 has a known bias and it is not corrected: fault-name density is partly a mapping
  artefact. A Basin-and-Range valley mapped at 1:24,000 by a 1990s NEHRP grant reports more
  distinct names than an equivalent structure mapped once at 1:250,000. So P4 is reported
  as its own column and capped, never allowed to dominate the sum.

WHAT IS DELIBERATELY NOT IN THE SCORE: any light-record, lore, sighting count, or
proximity to a facility. Those are the OUTCOME variable. June's survey demoted
Tijeras-Canoncito for having no light-record and thereby ranked the candidate on the thing
the mechanism is supposed to PREDICT -- which makes the prediction unfalsifiable. Here the
rank is physics-only and the lore is looked up afterward, held out, per site, including for
sites where I expect to find nothing.

TIER WEIGHTING: TIER_FABRIC > TIER_PLUTONIC, from lithology_probe's own docstring -- bulk
piezoelectric moment in an equigranular pluton averages toward zero because the c-axes are
randomly oriented; a tectonic fabric (gneiss, schist, mylonite) is the case where they are
not. This inverts the intuitive ordering ('granite is the piezo rock') on purpose.
"""
import json, math, os, sys
from collections import defaultdict

R = 6371.0
CACHE = "work/qfaults_normal_national.geojson"


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def load_index(cell=0.25):
    """Grid-hash every vertex of the national dilatant pull by fault_name."""
    fc = json.load(open(CACHE))
    grid = defaultdict(set)
    for ft in fc["features"]:
        nm = (ft["properties"].get("fault_name") or "").strip()
        if not nm:
            continue
        g = ft.get("geometry") or {}
        parts = ([g["coordinates"]] if g.get("type") == "LineString"
                 else g.get("coordinates", []) if g.get("type") == "MultiLineString"
                 else [])
        for part in parts:
            for c in part:
                lon, lat = c[0], c[1]
                grid[(round(lat / cell), round(lon / cell))].add((nm, round(lat, 3),
                                                                 round(lon, 3)))
    return grid, cell


def neighbours(grid, cell, lat, lon, km=15.0):
    span = int(km / 111.0 / cell) + 1
    r0, c0 = round(lat / cell), round(lon / cell)
    names = set()
    for dr in range(-span, span + 1):
        for dc in range(-span, span + 1):
            for nm, la, lo in grid.get((r0 + dr, c0 + dc), ()):
                if hav(lat, lon, la, lo) <= km:
                    names.add(nm)
    return names


TIER_W = {"TIER_FABRIC": 2.0, "TIER_PLUTONIC": 1.4}


def score(n, njunc):
    """0-10ish. Every term is stated; nothing is fitted to make a favourite win."""
    s_age = n["age_rank"] / 5.0 * 3.0            # 0-3   recency of rupture
    s_tier = TIER_W.get(n["at_point_tier"], 0)   # 0-2   piezo plausibility of the rock
    L = n.get("total_fault_length") or 0
    s_len = min(2.0, math.log10(max(L, 1)) )     # 0-2   structural scale (log km)
    s_junc = min(2.0, 0.5 * max(0, njunc - 1))   # 0-2   capped junction density
    return dict(age=round(s_age, 2), tier=round(s_tier, 2), length=round(s_len, 2),
                junction=round(s_junc, 2),
                total=round(s_age + s_tier + s_len + s_junc, 2))


if __name__ == "__main__":
    d = json.load(open("work/transport_screen_stage2.json"))
    grid, cell = load_index()
    print(f"[idx] {len(grid)} occupied cells", file=sys.stderr)
    rows = []
    for n in d["hits"]:
        nb = neighbours(grid, cell, n["lat"], n["lon"])
        sc = score(n, len(nb))
        rows.append(dict(n, n_systems_15km=len(nb),
                         systems_15km=sorted(nb)[:8], score=sc))
    rows.sort(key=lambda r: -r["score"]["total"])
    json.dump({"n": len(rows), "criteria": "P1 age, P2 dilatant (gate), P3 quartz at trace,"
                                           " P4 junction density; NO lore, NO light-record",
               "rows": rows}, open("work/site_rank.json", "w"), indent=1)
    print(f"{'#':>3} {'score':>6} {'age':>4} {'tier':>4} {'len':>4} {'junc':>4} "
          f"{'lat':>8} {'lon':>9}  fault", file=sys.stderr)
    for i, r in enumerate(rows[:25], 1):
        s = r["score"]
        print(f"{i:>3} {s['total']:6.2f} {s['age']:4.1f} {s['tier']:4.1f} {s['length']:4.1f} "
              f"{s['junction']:4.1f} {r['lat']:8.3f} {r['lon']:9.3f}  "
              f"{r['fault_name']} [{r['at_point_term']}] ({r['n_systems_15km']} sys)",
              file=sys.stderr)
