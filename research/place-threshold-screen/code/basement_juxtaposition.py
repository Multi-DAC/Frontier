"""P3'' -- BASEMENT JUXTAPOSITION. The A2 re-specification of the depth-to-basement leg.

WHY THIS FILE EXISTS. `basement_leg.py` sampled the NEAREST grid node and scored it.
PREREGISTRATION-v2.md amendment A2 retired that form after measuring what it was actually
ranking on: at Madison fault -- round 1's rank 1 -- depth-to-basement spans 0.6 m to
2,172 m inside a 2 km radius. The point sample returned 1,069 m. A number like that does
not measure the site; it measures which side of a range front the nearest node fell on.
Same defect as round 1's quartz_frac +/-0.125 vertex-ordering noise, new instrument.

THE TWO QUANTITIES, DECLARED FROM MECHANISM BEFORE THE JOIN TO SITE IDENTITY RUNS.
(A2 named this file as the place they are declared. They are written here against the
mechanism, not against a table of which sites they move.)

Report 08 asked for a leg expressing "a buried crystalline source with a permeable
pathway to the surface". That configuration has TWO necessary parts, and a point depth
expresses neither:

  (1) basement_min -- the SHALLOWEST basement depth within radius R.
      Does crystalline rock come near the surface anywhere in reach? Monotone DECREASING
      in depth, same log-linear form the point leg used and the same constants, so the
      re-specification cannot be confused with a re-tuning:

          s_min = 1 - log10(clip(Dmin, D_NEAR, D_FAR)/D_NEAR) / log10(D_FAR/D_NEAR)

      D_NEAR = 100 m, D_FAR = 5000 m -- unchanged from the point form. A DECLARED WAGER.

  (2) basement_contrast -- max minus min within the same R.
      Is there a structural juxtaposition: exposed crystalline against deep fill, which
      is what a dilatant range-front rupture IS? Monotone INCREASING, same log shape:

          s_con = log10(clip(C, C_LO, C_HI)/C_LO) / log10(C_HI/C_LO)

      C_LO = 100 m (below the grid's own local scatter -- no meaningful juxtaposition),
      C_HI = 3000 m (a full range front). ALSO A DECLARED WAGER, swept in ALTERNATES.

  The point value is DISCARDED as sampler-dependent. It is still computed here, but only
  to reproduce amendment A3's recorded figures, and it is written to the output under a
  key naming it retired so nothing downstream can pick it up by accident.

COMBINATION, and it is CONJUNCTIVE, which is a prediction and not a convenience:

      basement = sqrt(s_min * s_con)

  A geometric mean goes to zero if either part is absent, and that is the mechanism's
  claim: a source with no pathway does not couple, and a pathway with no source has
  nothing to couple. TWO PRE-DECLARED CONSEQUENCES, written before the values are joined
  so neither can be reported later as a discovery:

    - A UNIFORMLY EXPOSED crystalline block scores LOW on this leg despite basement at
      surface, because it has no juxtaposition. That is intended. It is also the single
      most likely way this leg is WRONG, and if the printed ten becomes implausible in
      that specific direction, the honest move is to report the additive form alongside,
      NOT to swap to it. Both forms are therefore computed and both are written out.
    - Deep uniform basin scores low on both parts. Also intended.

RADIUS. R = 2 km primary, swept over 1 / 2 / 3 / 5 km. 2 km is where A2 measured the
spread; it is the scale of a range-front damage zone, and it is wide enough that a
1 km-node grid gives several nodes without being wide enough to reach a second structure.

CONTRAST IS NEVER SCORED ZERO FOR WANT OF NODES. A contrast needs at least MIN_NODES
nodes inside R to mean anything; with fewer, contrast is UNMEASURED, a third value. One
node inside R would yield max == min == 0 m of contrast, which is indistinguishable in
the output from a genuinely flat neighbourhood and would push the site to the floor of a
conjunctive leg. That is the shape of round 1's "conflation scored as an absence".

THE 31 WITH NO BASEMENT VALUE (A1 / A1-RESULT). 27 of them carry essentially no sediment
and are scored `basement_min` INFERRED ~= 0. Their CONTRAST is unmeasurable -- there is no
basement grid there to take a max of. So the conjunctive leg is UNMEASURED for all 31,
and the structural asymmetry is stated rather than smoothed: THE SITES THE min-PART MOST
FAVOURS ARE EXACTLY THE SITES THE contrast-PART CANNOT SEE. A sediment-derived contrast
is computed for them as a clearly-separated ANNOTATION -- the two grids measure different
quantities (A1-RESULT's own caveat) and it is not folded into the leg.

WHAT THIS LEG IS NOT ALLOWED TO DO: physics criterion, Product A only. It carries no
claim about anomalous record. PREREGISTRATION-v2.md section 0.

This module also RE-DERIVES the figures amendments A1-RESULT, A2 and A3 state in prose,
and prints a PROSE CHECK against them. A correct compressed note expands into a wrong
sentence; recomputing beats re-reading.
"""
import csv
import hashlib
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D2B = os.path.join(HERE, "..", "work", "Dep2MzBasement_LLz.csv")
SED = os.path.join(HERE, "..", "work", "Sedthick_LLz.csv")
SITES = os.path.join(HERE, "..", "data", "stage5_join_summary.json")
OUT = os.path.join(HERE, "..", "data", "basement_juxtaposition.json")

D_NEAR, D_FAR = 100.0, 5000.0
C_LO, C_HI = 100.0, 3000.0
R_PRIMARY = 2.0
R_SWEEP = (1.0, 2.0, 3.0, 5.0)
MIN_NODES = 3
NODE_MAX_KM = 5.0              # a D2B estimate counts as present within this distance
SED_INFER_MAX_M = 200.0        # A1-RESULT's rule: sediment <= 200 m -> basement ~ 0, INFERRED

ALTERNATES = [(50.0, 3000.0, 50.0, 2000.0),
              (100.0, 5000.0, 100.0, 3000.0),
              (250.0, 8000.0, 250.0, 5000.0),
              (500.0, 10000.0, 500.0, 8000.0)]

# What the amendments say, in prose, so the recomputation can contradict them out loud.
PROSE = {
    "A1_measured": 194, "A1_total": 225, "A1_missing": 31,
    "A1_quartz_missing": 0.645, "A1_quartz_measured": 0.529,
    "A1R_sed_defined_of_31": 30, "A1R_sed_median_31": 1.4, "A1R_le50_31": 26,
    "A1R_sed_defined_of_194": 194, "A1R_sed_median_194": 3.4, "A1R_le50_194": 176,
    "A1R_inferred": 27, "A1R_stay_unmeasured": 4,
    "A2_ge4_nodes_2km": 190, "A2_spread_gt200": 76, "A2_spread_gt500": 37,
    "A2_median_spread": 141.8,
    "A2_madison_min": 0.6, "A2_madison_max": 2172.0,
    "A2_madison_point": 1069.0, "A2_madison_nbr_median": 648.0,
    "A3_sandia_point_m": 834.0, "A3_sandia_leg": 0.458,
    "A3_madison_point_m": 1069.0, "A3_madison_leg": 0.394,
    "A3_deeper_than_500": 22, "A3_median_depth": 64.0,
}
EXPECT_SHA_SED_PREFIX = "f79792c6"
CELL = 0.05        # ~5.5 km hash cell; +/-2 cells guarantees capture inside 5 km
R_EARTH = 6371.0


def s_min_of(depth_m, d_near=D_NEAR, d_far=D_FAR):
    d = min(max(depth_m, d_near), d_far)
    return 1.0 - math.log10(d / d_near) / math.log10(d_far / d_near)


def s_con_of(contrast_m, c_lo=C_LO, c_hi=C_HI):
    c = min(max(contrast_m, c_lo), c_hi)
    return math.log10(c / c_lo) / math.log10(c_hi / c_lo)


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def stream_near(path, targets, value_col, cell=CELL, span=2):
    """One streaming pass. Retains nodes in any cell within `span` of any target cell."""
    want = set()
    for lat, lon in targets:
        r0, c0 = round(lat / cell), round(lon / cell)
        for dr in range(-span, span + 1):
            for dc in range(-span, span + 1):
                want.add((r0 + dr, c0 + dc))
    keep = defaultdict(list)
    n = 0
    with open(path, newline="") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr == ["Lon_WGS84", "Lat_WGS84", value_col], hdr
        for row in rd:
            n += 1
            lon, lat, v = float(row[0]), float(row[1]), float(row[2])
            k = (round(lat / cell), round(lon / cell))
            if k in want:
                keep[k].append((lat, lon, v))
    print(f"[{value_col}] {n} nodes streamed, "
          f"{sum(len(v) for v in keep.values())} retained in {len(keep)} cells",
          file=sys.stderr)
    return keep


def neighbours(keep, lat, lon, radius_km, cell=CELL, span=2):
    """Every retained node within radius_km, as (km, value), nearest first."""
    r0, c0 = round(lat / cell), round(lon / cell)
    out = []
    for dr in range(-span, span + 1):
        for dc in range(-span, span + 1):
            for la, lo, v in keep.get((r0 + dr, c0 + dc), ()):
                km = hav(lat, lon, la, lo)
                if km <= radius_km:
                    out.append((km, v))
    out.sort()
    return out


def sha256_prefix(path, n=8):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:n], h.hexdigest()


def median(xs):
    v = sorted(xs)
    if not v:
        return None
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2.0


def pct(v, p):
    return v[min(len(v) - 1, int(p * len(v)))]


def main():
    src = json.load(open(SITES))
    sites = src["survivors_ranked"]
    targets = [(s["lat"], s["lon"]) for s in sites]

    sed_pref, sed_full = sha256_prefix(SED)
    print(f"[sed] sha256 {sed_pref}... (A1-RESULT states {EXPECT_SHA_SED_PREFIX})",
          file=sys.stderr)

    kb = stream_near(D2B, targets, "D2B_meters")
    ks = stream_near(SED, targets, "Sedthick_meters")

    rows = []
    for s in sites:
        lat, lon = s["lat"], s["lon"]
        r = dict(fault_name=s["fault_name"], rank_r1=s["rank"], lat=lat, lon=lon,
                 quartz_frac=s.get("quartz_frac"), score_r1=s.get("score"))

        # ---- per-radius basement neighbourhood -------------------------------------
        nb = {}
        for R in R_SWEEP:
            nn = neighbours(kb, lat, lon, R)
            vals = [v for _, v in nn]
            nb[R] = dict(n=len(vals),
                         dmin=round(min(vals), 1) if vals else None,
                         dmax=round(max(vals), 1) if vals else None,
                         dmed=round(median(vals), 1) if vals else None,
                         spread=round(max(vals) - min(vals), 1) if vals else None)
        r["basement_nbr"] = {f"{R:g}km": nb[R] for R in R_SWEEP}

        # ---- the RETIRED point form, kept only to reproduce A3 ----------------------
        nn_any = neighbours(kb, lat, lon, 6.0)
        if nn_any:
            r["RETIRED_point_d2b_m"] = round(nn_any[0][1], 1)
            r["RETIRED_point_node_km"] = round(nn_any[0][0], 3)
            r["RETIRED_point_leg"] = round(s_min_of(nn_any[0][1]), 4)
        else:
            r["RETIRED_point_d2b_m"] = None
            r["RETIRED_point_node_km"] = None
            r["RETIRED_point_leg"] = None

        # ---- sediment, point and neighbourhood -------------------------------------
        sn = neighbours(ks, lat, lon, R_PRIMARY)
        svals = [v for _, v in sn]
        r["sed_n_2km"] = len(svals)
        r["sed_point_m"] = round(sn[0][1], 2) if sn else None
        r["sed_min_2km_m"] = round(min(svals), 2) if svals else None
        r["sed_spread_2km_m"] = round(max(svals) - min(svals), 2) if svals else None

        # ---- status: A1-RESULT's population, which is NOT the leg's population -------
        # THREE DIFFERENT QUESTIONS, and the first version of this file collapsed the
        # first two. Kept apart by name so they cannot be again:
        #   status      -- does the D2B grid have ANY estimate here?  (A1's 194/31 split)
        #   basement_min-- is there a node inside R_PRIMARY to take a min over?
        #   contrast    -- are there >= MIN_NODES inside R_PRIMARY?
        # Collapsing status into the 2 km test moved 4 sites that DO have a basement
        # value (node at 2-5 km) into INFERRED, i.e. asserted "basement at surface" for
        # sites whose basement had in fact been measured. The prose check caught it.
        p = nb[R_PRIMARY]
        if r["RETIRED_point_d2b_m"] is not None and r["RETIRED_point_node_km"] <= NODE_MAX_KM:
            r["status"] = "PASS"
        elif r["sed_point_m"] is not None and r["sed_point_m"] <= SED_INFER_MAX_M:
            r["status"] = "INFERRED"
        else:
            r["status"] = "UNMEASURED"

        if p["n"] >= 1:
            r["basement_min_m"] = p["dmin"]
        elif r["status"] == "INFERRED":
            r["basement_min_m"] = 0.0
        else:
            r["basement_min_m"] = None
        r["basement_contrast_m"] = p["spread"] if p["n"] >= MIN_NODES else None

        if r["basement_min_m"] is None:
            r["s_min"] = None
        else:
            r["s_min"] = round(s_min_of(r["basement_min_m"]), 4)
        if r["basement_contrast_m"] is None:
            r["s_con"] = None
        else:
            r["s_con"] = round(s_con_of(r["basement_contrast_m"]), 4)

        if r["s_min"] is not None and r["s_con"] is not None:
            r["basement"] = round(math.sqrt(r["s_min"] * r["s_con"]), 4)
            r["basement_additive"] = round((r["s_min"] + r["s_con"]) / 2.0, 4)
            r["leg_status"] = "MEASURED"
            r["alternates"] = {
                f"{dn:g}_{df:g}_{cl:g}_{ch:g}":
                    round(math.sqrt(s_min_of(r["basement_min_m"], dn, df)
                                    * s_con_of(r["basement_contrast_m"], cl, ch)), 4)
                for dn, df, cl, ch in ALTERNATES}
            r["radius_sweep"] = {}
            for R in R_SWEEP:
                q = nb[R]
                if q["n"] >= MIN_NODES:
                    r["radius_sweep"][f"{R:g}km"] = round(
                        math.sqrt(s_min_of(q["dmin"]) * s_con_of(q["spread"])), 4)
                else:
                    r["radius_sweep"][f"{R:g}km"] = None
        else:
            r["basement"] = None
            r["basement_additive"] = None
            r["leg_status"] = ("UNMEASURED_NO_CONTRAST" if r["s_min"] is not None
                              else "UNMEASURED")
            r["alternates"] = None
            r["radius_sweep"] = None

        # ---- sediment-derived contrast, ANNOTATION ONLY, never folded in ------------
        r["ANNOT_sed_contrast_m"] = (r["sed_spread_2km_m"]
                                     if r["sed_n_2km"] >= MIN_NODES else None)
        rows.append(r)

    # ================= recomputation of the prose figures =========================
    # A1's population, by A1's own definition: does the D2B grid have an estimate here.
    point_meas = [r for r in rows if r["status"] == "PASS"]
    no_b = [r for r in rows if r["status"] != "PASS"]

    chk = {}
    chk["A1_measured"] = len(point_meas)
    chk["A1_missing"] = len(no_b)
    chk["A1_quartz_missing"] = round(
        sum(r["quartz_frac"] for r in no_b) / max(1, len(no_b)), 3)
    chk["A1_quartz_measured"] = round(
        sum(r["quartz_frac"] for r in point_meas) / max(1, len(point_meas)), 3)

    sed31 = [r["sed_point_m"] for r in no_b if r["sed_point_m"] is not None]
    sed194 = [r["sed_point_m"] for r in point_meas if r["sed_point_m"] is not None]
    chk["A1R_sed_defined_of_31"] = len(sed31)
    chk["A1R_sed_median_31"] = round(median(sed31), 1) if sed31 else None
    chk["A1R_le50_31"] = sum(1 for v in sed31 if v <= 50)
    chk["A1R_sed_defined_of_194"] = len(sed194)
    chk["A1R_sed_median_194"] = round(median(sed194), 1) if sed194 else None
    chk["A1R_le50_194"] = sum(1 for v in sed194 if v <= 50)
    chk["A1R_inferred"] = sum(1 for r in rows if r["status"] == "INFERRED")
    chk["A1R_stay_unmeasured"] = sum(1 for r in rows if r["status"] == "UNMEASURED")

    ge4 = [r for r in rows if r["basement_nbr"]["2km"]["n"] >= 4]
    spreads = [r["basement_nbr"]["2km"]["spread"] for r in ge4]
    chk["A2_ge4_nodes_2km"] = len(ge4)
    chk["A2_spread_gt200"] = sum(1 for v in spreads if v > 200)
    chk["A2_spread_gt500"] = sum(1 for v in spreads if v > 500)
    chk["A2_median_spread"] = round(median(spreads), 1) if spreads else None

    def by_name(frag):
        for r in rows:
            if frag.lower() in r["fault_name"].lower():
                return r
        return None

    mad, san = by_name("Madison"), by_name("Sandia")
    if mad:
        chk["A2_madison_min"] = mad["basement_nbr"]["2km"]["dmin"]
        chk["A2_madison_max"] = mad["basement_nbr"]["2km"]["dmax"]
        chk["A2_madison_point"] = mad["RETIRED_point_d2b_m"]
        chk["A2_madison_nbr_median"] = mad["basement_nbr"]["2km"]["dmed"]
        chk["A3_madison_point_m"] = mad["RETIRED_point_d2b_m"]
        chk["A3_madison_leg"] = mad["RETIRED_point_leg"]
    if san:
        chk["A3_sandia_point_m"] = san["RETIRED_point_d2b_m"]
        chk["A3_sandia_leg"] = san["RETIRED_point_leg"]
    pts = sorted(r["RETIRED_point_d2b_m"] for r in point_meas)
    chk["A3_deeper_than_500"] = sum(1 for v in pts if v > 500)
    chk["A3_median_depth"] = round(median(pts), 1) if pts else None
    chk["A1_total"] = len(rows)

    print("\n=== PROSE CHECK -- amendments A1/A1-RESULT/A2/A3 vs recomputation ===",
          file=sys.stderr)
    bad = []
    for k, said in PROSE.items():
        got = chk.get(k)
        if got is None:
            print(f"  ?  {k:26s} prose {said}  -- not recomputed", file=sys.stderr)
            continue
        ok = (abs(got - said) <= max(0.051, abs(said) * 0.02)
              if isinstance(said, float) else got == said)
        print(f"  {'OK ' if ok else 'XX '} {k:26s} prose {said}  recomputed {got}",
              file=sys.stderr)
        if not ok:
            bad.append((k, said, got))

    # ================= the leg's own degeneracy audit (section 2 discipline) ========
    meas = [r for r in rows if r["basement"] is not None]
    vv = sorted(r["basement"] for r in meas)
    top_decile = sorted(meas, key=lambda r: -r["basement"])[:max(1, len(meas) // 10)]

    audit = {
        "measured": len(meas), "of": len(rows),
        "median_convention": "even n -> mean of the two central values (the ad-hoc "
                             "Day-199 run used index-based v[n//2]; small differences "
                             "in A1R_sed_median_194 and A2_median_spread trace to this)",
        "status_counts": {k: sum(1 for r in rows if r["status"] == k)
                          for k in ("PASS", "INFERRED", "UNMEASURED")},
        "nodes_in_2km_ge1": sum(1 for r in rows
                                if r["basement_nbr"]["2km"]["n"] >= 1),
        "unmeasured_no_contrast": sum(1 for r in rows
                                      if r["leg_status"] == "UNMEASURED_NO_CONTRAST"),
        "value": {"min": vv[0], "p25": pct(vv, .25), "median": pct(vv, .5),
                  "p75": pct(vv, .75), "max": vv[-1],
                  "distinct": len(set(vv)),
                  "at_ceiling_1.0": sum(1 for v in vv if v >= 0.999),
                  "at_floor_0.0": sum(1 for v in vv if v <= 0.001)},
        "s_min": {"median": median([r["s_min"] for r in meas]),
                  "at_ceiling": sum(1 for r in meas if r["s_min"] >= 0.999),
                  "at_floor": sum(1 for r in meas if r["s_min"] <= 0.001)},
        "s_con": {"median": median([r["s_con"] for r in meas]),
                  "at_ceiling": sum(1 for r in meas if r["s_con"] >= 0.999),
                  "at_floor": sum(1 for r in meas if r["s_con"] <= 0.001)},
        "top_decile_s_min_ceiling": sum(1 for r in top_decile if r["s_min"] >= 0.999),
        "top_decile_s_con_ceiling": sum(1 for r in top_decile if r["s_con"] >= 0.999),
        "top_decile_n": len(top_decile),
    }

    out = {
        "declared_in": "code/basement_juxtaposition.py docstring; PREREGISTRATION-v2 A2",
        "sources": {
            "D2B": "USGS OFR 2018-1115 Dep2MzBasement_LLz.csv",
            "SED": "USGS OFR 2018-1115 Sedthick_LLz.csv",
            "sed_sha256": sed_full,
        },
        "form": {
            "s_min": "1 - log10(clip(Dmin,D_NEAR,D_FAR)/D_NEAR)/log10(D_FAR/D_NEAR)",
            "s_con": "log10(clip(C,C_LO,C_HI)/C_LO)/log10(C_HI/C_LO)",
            "basement": "sqrt(s_min * s_con)  -- CONJUNCTIVE, declared",
            "D_NEAR": D_NEAR, "D_FAR": D_FAR, "C_LO": C_LO, "C_HI": C_HI,
            "R_primary_km": R_PRIMARY, "MIN_NODES_for_contrast": MIN_NODES,
        },
        "prose_check": {"disagreements": [{"key": k, "prose": p, "recomputed": g}
                                         for k, p, g in bad],
                        "checked": len(PROSE)},
        "audit": audit,
        "rows": rows,
    }
    json.dump(out, open(OUT, "w"), indent=1)

    print(f"\n[leg] conjunctive form measured for {len(meas)}/{len(rows)} sites; "
          f"{audit['unmeasured_no_contrast']} have s_min but no contrast",
          file=sys.stderr)
    print(f"[leg] value min {vv[0]} / median {pct(vv, .5)} / max {vv[-1]}; "
          f"{audit['value']['distinct']} distinct; ceiling "
          f"{audit['value']['at_ceiling_1.0']} floor {audit['value']['at_floor_0.0']}",
          file=sys.stderr)
    print(f"[leg] top decile (n={audit['top_decile_n']}): s_min at ceiling "
          f"{audit['top_decile_s_min_ceiling']}, s_con at ceiling "
          f"{audit['top_decile_s_con_ceiling']}", file=sys.stderr)
    if bad:
        print(f"\n[PROSE CHECK FAILED] {len(bad)} amendment figure(s) disagree with the "
              f"recomputation. Fix the amendment, not the code.", file=sys.stderr)
    print(f"[leg] wrote {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
