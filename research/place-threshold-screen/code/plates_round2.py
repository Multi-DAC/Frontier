#!/usr/bin/env python3
"""plates_round2.py — build four-panel plates for the two areas that entered the
deliverable in round 2 and therefore have no plate from the round-1 dossier run.

Centennial fault and Antelope Valley fault zone are HEAD/BAND members in
data/candidate_list.json but were not in data/top10_frozen_100km.json, so
figures_final/ has nothing for them. Every other area in the round-2 ten is
represented by a member that already has a plate.

The site dicts are assembled from data/stage5_join_rows.json — the same join the
rest of the pipeline reads — and NOT retyped. The one derived quantity is the
5-term composite (the 4 scoring components plus the L1 quartz reading), which is
what candidate_list.py ranks on and what the round-1 frozen scores already are;
stage5's own `score` field is the 4-term version and would print a different
number under the same label. Asserted against candidate_list.json below rather
than trusted.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lithology_probe  # noqa: E402
import site_figure  # noqa: E402

WANT = {
    "Centennial fault": 4,               # rank shown on the plate = area rank in the ten
    "Antelope Valley fault zone": 5,
}
# NOT under work/ — that whole tree is gitignored, and a figure the article needs
# that only exists in an ignored directory does not exist for the article's purposes.
OUTDIR = "figures_round2"


def five_term(row):
    c = row["components"]
    q = row["legs"]["L1_lithology"]["value"]
    return round((c["age"] + c["slip"] + c["junction"] + c["length"] + q) / 5, 4)


def main():
    rows = {r["fault_name"]: r
            for r in json.load(open("data/stage5_join_rows.json", encoding="utf-8"))["rows"]}
    areas = {a["best_scoring"]: a
             for a in json.load(open("data/candidate_list.json", encoding="utf-8"))["areas"]}

    built = []
    for name, rank in WANT.items():
        r = rows[name]
        total = five_term(r)
        declared = areas[name]["best_score"]
        if abs(total - declared) > 5e-4:
            raise SystemExit(
                f"{name}: recomputed 5-term {total} != candidate_list {declared}. "
                "The plate would print a score the deliverable does not use.")

        # Panel B's footer prints the bedrock AT the starred node. The eight round-1
        # plates carry it, so these two must too or "built identically at every site"
        # stops being true. Re-probed through lithology_probe itself — same endpoint,
        # same tier ladder, same classify() — rather than retyped from any cache.
        tier, term, unit = lithology_probe.classify(
            lithology_probe.unit_at(r["lat"], r["lon"]))

        c, legs = r["components"], r["legs"]
        site = dict(
            fault_name=name,
            lat=r["lat"], lon=r["lon"],
            rank=rank,
            score=dict(total=total, age=c["age"], tier=legs["L1_lithology"]["value"],
                       length=c["length"], junction=c["junction"]),
            age=legs["L2_age"]["age"],
            slip_rate_class=legs["L3_slip"]["class"],
            n_systems_15km=legs["L4_junction"]["value"],
            at_point_term=term,
            at_point_unit=unit,
        )
        if term is None:
            raise SystemExit(f"{name}: bedrock at node did not classify; panel B would "
                             f"print '?' where the other eight plates print a rock.")
        print(f"[{rank}] {total}  {name}  ({r['lat']}, {r['lon']})", file=sys.stderr)
        out, man = site_figure.build(site, outdir=OUTDIR)
        bad = [k for k, v in man["layers"].items() if v["status"] != "PRESENT"]
        built.append(dict(name=name, rank=rank, score=total, output=out,
                          layers_failed=bad, layers_n=len(man["layers"])))

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "_manifest.json"), "w") as fh:
        json.dump({"n": len(built), "n_expected": len(WANT), "sites": built}, fh, indent=1)

    for b in built:
        flag = f"  !! MISSING LAYERS: {b['layers_failed']}" if b["layers_failed"] else ""
        print(f"{b['name']:32s} -> {b['output']}{flag}")
    if any(b["layers_failed"] for b in built):
        # A plate with a dead panel is a plate that says less than the other eight,
        # under a caption claiming all four panels are built identically. Loud.
        sys.exit(3)


if __name__ == "__main__":
    main()
