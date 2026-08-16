"""STAGE 5 -- the multi-criterion join over the whole population, with coverage as a
first-class output rather than an afterthought.

THE TRAP THIS FILE IS BUILT AROUND. "Find the sites that meet ALL requirements" is the
right question and the most dangerous possible query shape for this dataset, because the
legs do not have the same coverage:

    L1 lithology (quartz_frac)      1399/1399   100.0%
    L2 age_rank                     1399/1399   100.0%
    L4 junction density             1399/1399   100.0%   (computed, by construction)
    L3 published slip rate          1349/1399    96.4%
    L6 total_fault_length           1328/1399    94.9%
    L5 GPS strain                     23/1399     1.6%   <--

An AND across all six returns at most 23 sites, and the other 1,376 would be reported as
"did not meet the requirements" when the truth is "was never measured on that leg". That
is the same defect that produced the ten falsy zeros this morning, at population scale,
and it would be invisible in the output: a short list looks like a strict screen.

So the rule here is that a leg may only EXCLUDE a fault if that leg actually measured it.
Every fault carries a per-leg status of PASS / FAIL / UNMEASURED -- three values, never
two -- and the score records how many legs it was actually scored on, so a site scored on
3 of 4 is visibly not the same object as one scored on 4 of 4.

L5 is demoted to an ANNOTATION for the same reason: at 1.6% coverage it can PROMOTE a
site (a measured strain hit is real evidence) but it can never demote one, because absence
of a GPS strain measurement at a fault is a statement about the GPS network, not the fault.

LITHOLOGY IS A GATE, NOT A RANKER, and there are now two independent reasons:
  1. 241 of 1393 faults passed and Sandia ranked 42nd of them, with 20 faults at a perfect
     1.000. It does not discriminate at the top.
  2. Measured D197: quartz_frac carries sampling noise of order 1/N_SAMPLE = 0.125 from
     vertex ordering alone -- the Sandia trace reads 0.875 or 1.000 depending purely on
     the order the service returns its segments in. Ranking on a quantity with that much
     ordering noise at 8 points is ranking on the sampler.
So L1 gates at RESCUE_FRAC and contributes nothing to the score.

NAME NORMALISATION HAPPENS ONCE, HERE. The USGS attributes carry stray control characters
(a trailing U+000B on one fault, doubled internal spaces on two more). Mixing raw and
stripped spellings has now produced a silent failure three separate times in this pipeline:
it lost a measurement in stage 3, created a phantom duplicate row in stage 4B, and dropped
a fault out of my own coverage check while writing this file. Every dict that enters the
join goes through key_of(), and the join asserts no two raw keys collide when normalised.

WHAT IS STILL NOT IN THE SCORE: light-record, lore, sighting counts, facility proximity.
Those are the outcome variable. The rank is physics-only and the lore is held out.
"""
import json, math, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qfaults_pull import slip_mid                                    # noqa: E402

W = os.path.dirname(os.path.abspath(__file__))
LITH = os.path.join(W, "trace_lithology_full.json")
NODES = os.path.join(W, "transport_nodes_perfault.json")
STRAIN = os.path.join(W, "screen_strain_pass.json")
QF = os.path.join(W, "qfaults_normal_national.geojson")
OUT = os.path.join(W, "stage5_join.json")

RESCUE_FRAC = 0.25
JUNCTION_KM = 15.0
CTL = {"Sandia fault": ("POSITIVE", True), "Hubbell Spring fault": ("NEGATIVE", False)}
R = 6371.0

PASS, FAIL, UNMEASURED = "PASS", "FAIL", "UNMEASURED"


def key_of(name):
    """The one place a fault name becomes a key. See the header."""
    return " ".join((name or "").split())


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def load_normalised(path, subkey=None):
    d = json.load(open(path, encoding="utf-8"))
    src = d[subkey] if subkey else d
    out, seen = {}, defaultdict(list)
    for k, v in src.items():
        seen[key_of(k)].append(k)
        out[key_of(k)] = v
    clash = {k: v for k, v in seen.items() if len(v) > 1}
    if clash:
        sys.exit(f"[abort] {path}: normalising keys collides {clash}; "
                 "two distinct faults would merge into one row.")
    return out


def junction_index(cell=0.25):
    fc = json.load(open(QF, encoding="utf-8"))
    grid = defaultdict(set)
    for ft in fc["features"]:
        nm = key_of(ft["properties"].get("fault_name"))
        if not nm:
            continue
        g = ft.get("geometry") or {}
        parts = ([g["coordinates"]] if g.get("type") == "LineString"
                 else g.get("coordinates", []) if g.get("type") == "MultiLineString"
                 else [])
        for part in parts:
            for c in part:
                grid[(round(c[1] / cell), round(c[0] / cell))].add(
                    (nm, round(c[1], 3), round(c[0], 3)))
    return grid, cell


def neighbours(grid, cell, lat, lon, km=JUNCTION_KM):
    span = int(km / 111.0 / cell) + 1
    r0, c0 = round(lat / cell), round(lon / cell)
    names = set()
    for dr in range(-span, span + 1):
        for dc in range(-span, span + 1):
            for nm, la, lo in grid.get((r0 + dr, c0 + dc), ()):
                if hav(lat, lon, la, lo) <= km:
                    names.add(nm)
    return names


if __name__ == "__main__":
    lith = load_normalised(LITH, "done")
    nodes_raw = json.load(open(NODES, encoding="utf-8"))
    best = {}
    for n in nodes_raw["all"]:
        nm = key_of(n.get("fault_name"))
        if nm and nm not in best:
            best[nm] = n
    strain = defaultdict(list)
    for r in json.load(open(STRAIN, encoding="utf-8"))["all"]:
        nm = key_of(r.get("fault_name"))
        if nm:
            strain[nm].append(r)

    pop = sorted(best)
    N = len(pop)
    print(f"[pop] {N} named dilatant normal faults", file=sys.stderr)

    grid, cell = junction_index()
    print(f"[idx] {len(grid)} occupied cells", file=sys.stderr)

    rows = []
    for nm in pop:
        n = best[nm]
        L = lith.get(nm, {})
        legs, score, scored_on = {}, {}, 0

        # ---- L1 lithology: GATE ONLY. Three-valued.
        qf = L.get("quartz_frac")
        if L.get("off_frame"):
            legs["L1_lithology"] = {"status": UNMEASURED, "value": None,
                                    "why": "off-frame: " + L.get("off_frame_reason", "")}
        elif qf is None:
            legs["L1_lithology"] = {"status": UNMEASURED, "value": None,
                                    "why": L.get("error") or "no measurement"}
        else:
            legs["L1_lithology"] = {"status": PASS if qf >= RESCUE_FRAC else FAIL,
                                    "value": qf, "n_pts": L.get("n_pts"),
                                    "fabric_frac": L.get("fabric_frac")}

        # ---- L2 age / rupture recency: RANKER
        ar = n.get("age_rank")
        if ar is None:
            legs["L2_age"] = {"status": UNMEASURED, "value": None}
        else:
            legs["L2_age"] = {"status": PASS, "value": ar, "age": n.get("age")}
            score["age"] = min(1.0, ar / 5.0); scored_on += 1

        # ---- L3 published slip rate: RANKER. The DRIVER, not an age proxy.
        sr = slip_mid(n.get("slip_rate_class"))
        if sr is None:
            legs["L3_slip"] = {"status": UNMEASURED, "value": None,
                               "class": n.get("slip_rate_class")}
        else:
            legs["L3_slip"] = {"status": PASS, "value": sr,
                               "class": n.get("slip_rate_class")}
            # 0.1 -> 0, 7.5 -> 1 on a log scale; published categories are coarse.
            score["slip"] = min(1.0, max(0.0, (math.log10(sr) + 1.0) / 2.0))
            scored_on += 1

        # ---- L4 junction density: RANKER, 100% by construction
        lat, lon = n.get("lat"), n.get("lon")
        if lat is None or lon is None:
            legs["L4_junction"] = {"status": UNMEASURED, "value": None}
        else:
            nb = neighbours(grid, cell, lat, lon)
            legs["L4_junction"] = {"status": PASS, "value": len(nb),
                                   "systems": sorted(nb)[:8]}
            score["junction"] = min(1.0, max(0, len(nb) - 1) / 4.0); scored_on += 1

        # ---- L6 structural scale: RANKER
        tl = n.get("total_fault_length") or 0
        if tl <= 0:
            legs["L6_length"] = {"status": UNMEASURED, "value": None}
        else:
            legs["L6_length"] = {"status": PASS, "value": tl}
            score["length"] = min(1.0, math.log10(max(tl, 1)) / 2.5); scored_on += 1

        # ---- L5 GPS strain: ANNOTATION. May promote, never demote.
        # The strain layer carries its OWN three-valued verdict -- 'STRAINING' vs
        # 'not resolved above floor' -- so a measured non-detection is a real FAIL on
        # this leg and is kept as one, distinct from the 1,376 faults with no GPS node
        # at all. Flattening it to a number would have lost that distinction.
        sv = [r["strain"] for r in strain.get(nm, [])
              if isinstance(r.get("strain"), dict)
              and r["strain"].get("gmax_nstrain_yr") is not None]
        if not sv:
            legs["L5_strain"] = {"status": UNMEASURED, "value": None,
                                 "why": "no GPS strain node within the layer's footprint; "
                                        "a statement about the network, not the fault"}
        else:
            top = max(sv, key=lambda s: s["gmax_nstrain_yr"])
            hit = any(s.get("verdict") == "STRAINING" for s in sv)
            legs["L5_strain"] = {"status": PASS if hit else FAIL,
                                 "value": top["gmax_nstrain_yr"],
                                 "verdict": top.get("verdict"),
                                 "p_scramble": top.get("p_scramble"),
                                 "above_craton_floor": top.get("above_craton_floor"),
                                 "n_nodes": len(sv)}

        gated_out = legs["L1_lithology"]["status"] == FAIL
        # Two numbers, because one of them lies. `score` is the mean over the legs the
        # fault actually has; on its own it lets MISSING DATA BUY RANK -- a fault with no
        # published slip rate and no mapped length is averaged over only its two best
        # legs, and the first run of this file duly put three 2-of-4 faults above every
        # complete one. `floor` charges the missing legs as zero, which is the other
        # extreme and equally wrong on its own. Ranking is tiered on completeness first
        # (see below) so neither number has to carry the comparison by itself.
        total = round(sum(score.values()) / scored_on, 4) if scored_on else None
        floor = round(sum(score.values()) / 4.0, 4)
        rows.append({
            "fault_name": nm, "lat": lat, "lon": lon,
            "gate_L1": legs["L1_lithology"]["status"],
            "gated_out": gated_out,
            "score": total, "score_floor": floor,
            "scored_on_legs": scored_on, "of_legs": 4,
            "complete": scored_on == 4,
            "components": {k: round(v, 3) for k, v in score.items()},
            "strain_annotation": legs["L5_strain"]["value"],
            "legs": legs})

    # ---------------- coverage, reported before any ranking is read
    cov = {}
    for lg in ("L1_lithology", "L2_age", "L3_slip", "L4_junction", "L6_length",
               "L5_strain"):
        m = sum(1 for r in rows if r["legs"][lg]["status"] != UNMEASURED)
        cov[lg] = {"measured": m, "of": N, "pct": round(100 * m / N, 1)}

    survivors = [r for r in rows if r["gate_L1"] == PASS]
    unmeasured_gate = [r for r in rows if r["gate_L1"] == UNMEASURED]
    # Completeness FIRST, then score. A 4-of-4 fault and a 2-of-4 fault are not two
    # values of one quantity, they are two different states of knowledge, and averaging
    # them onto a single axis is what let missing data outrank measurement.
    survivors.sort(key=lambda r: (not r["complete"], -(r["score"] or 0),
                                  r["fault_name"]))
    complete = [r for r in survivors if r["complete"]]
    partial = [r for r in survivors if not r["complete"]]

    # ---------------- controls, by RANK not just by value
    ctl_out = {}
    for nm, (label, want_pass) in CTL.items():
        k = key_of(nm)
        r = next((x for x in rows if x["fault_name"] == k), None)
        got = r["gate_L1"] == PASS if r else None
        rank = next((i for i, x in enumerate(survivors, 1)
                     if x["fault_name"] == k), None)
        ctl_out[nm] = {"declared": label, "must_pass_gate": want_pass,
                       "passed_gate": got, "correct": got is want_pass,
                       "rank_among_survivors": rank, "of": len(survivors),
                       "score": r["score"] if r else None}
    ctl_ok = all(v["correct"] for v in ctl_out.values())

    out = {"population": N,
           "gate": {"leg": "L1_lithology", "threshold": RESCUE_FRAC,
                    "passed": len(survivors), "failed": N - len(survivors)
                    - len(unmeasured_gate), "unmeasured": len(unmeasured_gate)},
           "coverage": cov, "controls": ctl_out, "controls_valid": ctl_ok,
           "ranked_complete": len(complete), "ranked_partial": len(partial),
           "join_rule": "L1 gates (3-valued; UNMEASURED never excludes). L2/L3/L4/L6 "
                        "score, each fault scored only on the legs it has, denominator "
                        "recorded. Ranking is tiered on completeness FIRST so a "
                        "partially-measured fault cannot outrank a fully-measured one on "
                        "a mean taken over fewer legs. L5 (1.5% coverage) annotates only.",
           "rows": rows}
    json.dump(out, open(OUT, "w"), indent=1)

    print("\n== LEG COVERAGE", file=sys.stderr)
    for k, v in cov.items():
        flag = "  <-- ANNOTATION ONLY" if v["pct"] < 50 else ""
        print(f"   {k:<14} {v['measured']:5d}/{v['of']}  {v['pct']:5.1f}%{flag}",
              file=sys.stderr)
    print(f"\n== GATE L1 >= {RESCUE_FRAC}: {len(survivors)} pass, "
          f"{out['gate']['failed']} fail, {len(unmeasured_gate)} unmeasured "
          f"(unmeasured are NOT excluded, they are unranked)", file=sys.stderr)
    print("\n== CONTROLS", file=sys.stderr)
    for nm, v in ctl_out.items():
        print(f"   {nm:<24} {v['declared']:<9} gate={v['passed_gate']!s:<5} "
              f"{'OK' if v['correct'] else 'WRONG'}   rank "
              f"{v['rank_among_survivors']}/{v['of']}  score={v['score']}",
              file=sys.stderr)
    if not ctl_ok:
        sys.exit("[abort] controls failed the join; ranking not to be read.")

    def table(title, lst, k=25):
        print(f"\n== {title}", file=sys.stderr)
        print(f"{'#':>3} {'score':>6} {'legs':>4} {'age':>5} {'slip':>5} {'junc':>5} "
              f"{'len':>5} {'qtz':>5} {'strain':>8}  fault", file=sys.stderr)
        for i, r in enumerate(lst[:k], 1):
            c = r["components"]
            st = r["strain_annotation"]
            print(f"{i:>3} {r['score']:6.3f} {r['scored_on_legs']}/4 "
                  f"{c.get('age', 0):5.2f} {c.get('slip', 0):5.2f} "
                  f"{c.get('junction', 0):5.2f} {c.get('length', 0):5.2f} "
                  f"{r['legs']['L1_lithology']['value']:5.2f} "
                  f"{(f'{st:.2e}' if st is not None else '--'):>8}  "
                  f"{r['fault_name'][:44]}", file=sys.stderr)

    table(f"TOP 25 of {len(complete)} FULLY-MEASURED survivors "
          f"(physics only; lore held out)", complete)
    table(f"PARTIAL-COVERAGE survivors ({len(partial)}) -- scores NOT comparable to the "
          f"table above; fewer legs, smaller denominator", partial, 10)
    print(f"\n[stage5] {len(complete)} complete + {len(partial)} partial = "
          f"{len(survivors)} through the gate; wrote {OUT}", file=sys.stderr)
