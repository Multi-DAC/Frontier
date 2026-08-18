"""P3''' -- ORDERING STABILITY of the basement leg. The instrument section 6 asked for.

PREREGISTRATION-v2.md section 6 requires, of Product A: "a STATED ORDERING NOISE FLOOR --
the rank change induced by perturbing each leg within its own measurement noise, run as a
bootstrap, so 'rank 3 vs rank 6' carries an honest error bar or is reported as
indistinguishable."

This module supplies that for the new basement leg, and it does it by VARIANT ENUMERATION
rather than by bootstrap, because the dominant uncertainty here is not sampling noise in a
fixed quantity -- it is WHICH QUANTITY, and every one of those choices was a declared
wager:

  - the neighbourhood radius R (A2 declared 2 km, swept 1/2/3/5)
  - the four scoring constants D_NEAR / D_FAR / C_LO / C_HI (a declared wager, 4 sets)
  - the combination rule, conjunctive sqrt(s_min*s_con) vs additive mean (both declared)
  - and now the neighbourhood DEFINITION itself, below.

A bootstrap over node values inside a fixed radius would put an error bar on the wrong
thing. It would report the precision of a choice, not the sensitivity to it.

============================================================================
WHY A FIFTH NEIGHBOURHOOD FORM EXISTS -- and this declaration is NOT blind
============================================================================
STATED PLAINLY, because it decides how much the result below is worth: this form was
specified AFTER the R sweep was read. So it is not a blind declaration, and it is not
presented as one. What IS declared before any value of it is computed is the FORM, the
constant k, the cap, and the readout rule at the bottom of this docstring.

The trigger was a defect, not a taste. A FIXED RADIUS holds the neighbourhood's size
constant and lets the sample size vary; on a grid with local holes that means some sites
get 13 nodes and some get zero. Four of the 194 D2B-measured survivors have fewer than
3 nodes within 2 km, and ONE OF THE FOUR IS THE DECLARED POSITIVE CONTROL:

    Sandia fault -- nearest D2B node 2.358 km. The 2 km radius misses it by 358 m.

A leg that cannot score its own positive control cannot be tested by its own controls,
and section 6 requires those controls "in the right direction or PRINTED FAILING". Both
readings were unavailable. That is an instrument fault, and 358 m of margin deciding it
is the boundary-float failure this project has already been bitten by once.

  k-NEAREST FORM: the k nearest D2B nodes, however far they reach, with the enclosing
  radius PRINTED per site so a reader can see when the neighbourhood stretched.

      k = 13 -- the MEDIAN node count within the primary 2 km radius, measured over the
      191 sites that have any (min 2, p25 12, median 13, p75 13, max 14). k is set from
      the grid's own density so the two forms carry comparable sample size, and not from
      which sites it moves.

      CAP: if the k-th nearest node lies beyond MAX_K_KM = 6 km, the site is UNMEASURED.
      A "neighbourhood" that reaches 20 km to find 13 nodes is not a neighbourhood, and
      letting it stretch without limit would silently convert a coverage hole into a
      confident juxtaposition measurement.

  It holds sample size constant and lets extent vary -- the opposite trade to the fixed
  radius. NEITHER IS OBVIOUSLY RIGHT, which is exactly why both are run and neither is
  called primary in the readout.

============================================================================
THE READOUT RULE -- declared here, before any variant is scored
============================================================================
40 variants: 5 neighbourhood forms (R=1,2,3,5 km + k-nearest) x 4 constant sets
x 2 combination rules.

Per site, across all 40: best rank, median rank, worst rank, and the count of variants
in which the site is scoreable at all. A site UNSCOREABLE in a variant is counted as NOT
in that variant's top ten -- the conservative direction, and the count is printed so the
penalty is visible rather than silent.

  THE HEAD, defined without a tunable threshold: the sites whose WORST rank across all
  40 variants is <= 10. That is "never leaves the top ten under any declared choice".
  If fewer than ten sites clear it, the leg licenses fewer than ten and the answer is
  the shorter list. IT IS NOT TOPPED UP.

  Everything below the head is reported with its rank interval and NOT as an ordinal.
  A site with rank interval 4-38 is reported as 4-38.

No number in this readout rule may be adjusted after a variant is scored.
"""
import csv
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D2B = os.path.join(HERE, "..", "work", "Dep2MzBasement_LLz.csv")
SITES = os.path.join(HERE, "..", "data", "stage5_join_summary.json")
JUX = os.path.join(HERE, "..", "data", "basement_juxtaposition.json")
OUT = os.path.join(HERE, "..", "data", "basement_stability.json")

K = 13
MAX_K_KM = 6.0
MIN_NODES = 3
R_FORMS = (1.0, 2.0, 3.0, 5.0)
CONSTS = [(50.0, 3000.0, 50.0, 2000.0),
          (100.0, 5000.0, 100.0, 3000.0),
          (250.0, 8000.0, 250.0, 5000.0),
          (500.0, 10000.0, 500.0, 8000.0)]
COMBOS = ("conjunctive", "additive")
HEAD_N = 10

CELL = 0.05
SPAN = 2
R_EARTH = 6371.0


def s_min_of(d, dn, df):
    d = min(max(d, dn), df)
    return 1.0 - math.log10(d / dn) / math.log10(df / dn)


def s_con_of(c, cl, ch):
    c = min(max(c, cl), ch)
    return math.log10(c / cl) / math.log10(ch / cl)


def combine(sm, sc, how):
    return math.sqrt(sm * sc) if how == "conjunctive" else (sm + sc) / 2.0


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def stream(targets):
    want = set()
    for lat, lon in targets:
        r0, c0 = round(lat / CELL), round(lon / CELL)
        for dr in range(-SPAN, SPAN + 1):
            for dc in range(-SPAN, SPAN + 1):
                want.add((r0 + dr, c0 + dc))
    keep = defaultdict(list)
    with open(D2B, newline="") as f:
        rd = csv.reader(f)
        assert next(rd) == ["Lon_WGS84", "Lat_WGS84", "D2B_meters"]
        for row in rd:
            lon, lat, v = float(row[0]), float(row[1]), float(row[2])
            k = (round(lat / CELL), round(lon / CELL))
            if k in want:
                keep[k].append((lat, lon, v))
    return keep


def nbrs(keep, lat, lon):
    r0, c0 = round(lat / CELL), round(lon / CELL)
    out = []
    for dr in range(-SPAN, SPAN + 1):
        for dc in range(-SPAN, SPAN + 1):
            for la, lo, v in keep.get((r0 + dr, c0 + dc), ()):
                out.append((hav(lat, lon, la, lo), v))
    out.sort()
    return out


def median(xs):
    v = sorted(xs)
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2.0


def main():
    sites = json.load(open(SITES))["survivors_ranked"]
    jux = {r["fault_name"]: r for r in json.load(open(JUX))["rows"]}
    keep = stream([(s["lat"], s["lon"]) for s in sites])

    # ---- neighbourhood extraction, once per site per form ------------------------
    forms = {}
    for s in sites:
        nn = nbrs(keep, s["lat"], s["lon"])
        per = {}
        for R in R_FORMS:
            vals = [v for km, v in nn if km <= R]
            per[f"R{R:g}"] = ((min(vals), max(vals) - min(vals))
                              if len(vals) >= MIN_NODES else None)
        kn = nn[:K]
        if len(kn) >= K and kn[-1][0] <= MAX_K_KM:
            vals = [v for _, v in kn]
            per["kNN"] = (min(vals), max(vals) - min(vals))
            per["_kNN_reach_km"] = round(kn[-1][0], 3)
        else:
            per["kNN"] = None
            per["_kNN_reach_km"] = round(kn[-1][0], 3) if kn else None
        forms[s["fault_name"]] = per

    form_names = [f"R{R:g}" for R in R_FORMS] + ["kNN"]

    # ---- 40 variants -------------------------------------------------------------
    variants, top_hits, scoreable, ranks = [], defaultdict(int), defaultdict(int), \
        defaultdict(list)
    for fn in form_names:
        for dn, df, cl, ch in CONSTS:
            for how in COMBOS:
                vname = f"{fn}|{dn:g}-{df:g}-{cl:g}-{ch:g}|{how}"
                scored = []
                for name, per in forms.items():
                    mc = per[fn]
                    if mc is None:
                        continue
                    dmin, con = mc
                    scored.append((combine(s_min_of(dmin, dn, df),
                                           s_con_of(con, cl, ch), how), name))
                scored.sort(key=lambda t: -t[0])
                for i, (_, name) in enumerate(scored):
                    scoreable[name] += 1
                    ranks[name].append(i + 1)
                    if i < HEAD_N:
                        top_hits[name] += 1
                variants.append(dict(variant=vname, n_scored=len(scored),
                                     top10=[n for _, n in scored[:HEAD_N]]))

    NV = len(variants)

    per_site = []
    for s in sites:
        name = s["fault_name"]
        rr = ranks[name]
        per_site.append(dict(
            fault_name=name, rank_r1=s["rank"],
            scoreable_in=scoreable[name], of_variants=NV,
            top10_in=top_hits[name],
            best_rank=min(rr) if rr else None,
            median_rank=median(rr) if rr else None,
            worst_rank=max(rr) if rr else None,
            # WORST-CASE rank if unscoreable variants are counted against the site,
            # which is the conservative reading the docstring committed to.
            worst_rank_penalised=(max(rr) if scoreable[name] == NV else None),
            kNN_reach_km=forms[name]["_kNN_reach_km"],
            leg_2km=jux.get(name, {}).get("basement"),
            status=jux.get(name, {}).get("status"),
        ))

    # THE HEAD, by the declared rule: never leaves the top ten in ANY of the 40.
    head = [p for p in per_site
            if p["scoreable_in"] == NV and p["worst_rank"] is not None
            and p["worst_rank"] <= HEAD_N]
    head.sort(key=lambda p: p["median_rank"])

    # Sites scoreable everywhere, ranked by median, for the interval readout.
    full = [p for p in per_site if p["scoreable_in"] == NV]
    full.sort(key=lambda p: p["median_rank"])

    out = dict(
        declared_in="code/basement_stability.py docstring (readout rule declared before "
                    "any variant was scored; the k-nearest FORM was specified after the "
                    "R sweep was read and that is stated, not hidden)",
        n_variants=NV, K=K, MAX_K_KM=MAX_K_KM, HEAD_N=HEAD_N,
        forms=form_names, constants=CONSTS, combos=list(COMBOS),
        scoreable_everywhere=len(full), of=len(per_site),
        head_by_declared_rule=[p["fault_name"] for p in head],
        head_size=len(head),
        per_site=per_site, variants=variants,
    )
    json.dump(out, open(OUT, "w"), indent=1)

    print(f"[stability] {NV} variants; {len(full)}/{len(per_site)} sites scoreable in "
          f"all of them", file=sys.stderr)
    print(f"\nHEAD by the declared rule (worst rank <= {HEAD_N} across all {NV}): "
          f"{len(head)} site(s)", file=sys.stderr)
    for p in head:
        print(f"   {p['fault_name'][:34]:34s} r1={p['rank_r1']:<4} ranks "
              f"{p['best_rank']}-{p['worst_rank']} (median {p['median_rank']:g})",
              file=sys.stderr)
    print(f"\nTOP 15 BY MEDIAN RANK, with the interval that is the actual result:",
          file=sys.stderr)
    print(f"   {'fault':34s} {'r1':>4} {'best':>5} {'med':>6} {'worst':>6} "
          f"{'top10_in':>9} {'kNN_km':>7}", file=sys.stderr)
    for p in full[:15]:
        print(f"   {p['fault_name'][:34]:34s} {p['rank_r1']:>4} {p['best_rank']:>5} "
              f"{p['median_rank']:>6g} {p['worst_rank']:>6} "
              f"{str(p['top10_in']) + '/' + str(NV):>9} "
              f"{p['kNN_reach_km'] if p['kNN_reach_km'] is not None else '-':>7}",
              file=sys.stderr)

    ctl = [p for p in per_site if "Sandia" in p["fault_name"]]
    print(f"\nCONTROL -- Sandia fault (declared POSITIVE):", file=sys.stderr)
    for p in ctl:
        print(f"   scoreable in {p['scoreable_in']}/{NV} variants; ranks "
              f"{p['best_rank']}-{p['worst_rank']} (median {p['median_rank']}); "
              f"kNN reach {p['kNN_reach_km']} km; 2km leg {p['leg_2km']}",
              file=sys.stderr)
    print(f"\n[stability] wrote {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
