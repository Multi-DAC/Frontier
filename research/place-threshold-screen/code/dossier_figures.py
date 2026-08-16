"""Rebuild the four-panel plates for the FROZEN top-10 — the list the lore legs actually ran on.

WHY THIS EXISTS AND IS NOT `site_figure.py --top10`:

`site_figure.top_sites()` reads `work/site_rank.json`, which is the PARTIAL screen from
report 07 (Madison, Centennial, Teton, Sawatch, Sangre de Cristo...). The lore experiments
H1/H2/H3 were run against `work/top10_frozen_100km.json` — a different list, produced by a
different rule (L1 as a fifth scoring term + 100 km minimum separation, greedy from the top).
EIGHT OF TEN DIFFER. The plates committed to figures/ are therefore pictures of sites that
carry no lore evidence, under filenames that read like the candidate list.

That is the exact shape this repo keeps producing: a carrier whose name promises the current
subject and whose content is the previous one. So this driver takes the site list from the
frozen file, asserts the rendered manifest name against the frozen name for every site, and
writes into a SEPARATE directory rather than overwriting — the old plates stay legible as
what they are.

Output: work/figures_final/NN_slug.png + .layers.json, plus _manifest.json over all ten.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import site_figure  # noqa: E402

FROZEN = "work/top10_frozen_100km.json"
JOIN = "work/stage5_join.json"
LITH = "work/trace_lithology_full.json"
OUTDIR = "work/figures_final"


def rock_summary(lr):
    """What the 8 along-trace vertices actually hit — the quantity `quartz_frac` is built from.

    `at_point_term` only exists on rows that came through trace_lithology_survivors.json;
    for 8 of the frozen 10 it is absent and the panel rendered a bare '?'. The per-vertex
    `pts` are present on every row, so summarise those instead and SAY it is a trace
    summary rather than a point reading — a different quantity, honestly named.
    """
    pts = lr.get("pts") or []
    if not pts:
        return "?", "no per-vertex lithology on file"
    counts = {}
    for p in pts:
        counts[p.get("term") or "no qualifying unit"] = counts.get(
            p.get("term") or "no qualifying unit", 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    modal = ordered[0][0]
    detail = ", ".join(f"{v}× {k}" for k, v in ordered)
    return modal, f"{len(pts)} trace vertices: {detail}"


def load_sites():
    frozen = json.load(open(FROZEN))
    rows = {r["fault_name"]: r for r in json.load(open(JOIN))["rows"]}
    lith = json.load(open(LITH))["done"]

    sites = []
    for s in frozen["sites"]:
        name = s["fault"]
        row = rows.get(name) or {}
        lr = lith.get(name) or {}
        legs = row.get("legs", {})
        modal, detail = rock_summary(lr)
        sites.append({
            "fault_name": name,
            "lat": s["lat"],
            "lon": s["lon"],
            "rank": s["rank"],
            "score": {
                "total": round(s["score"], 3),
                "age": s["components"]["age"],
                "tier": s["L1"],
                "length": s["components"]["length"],
                "junction": s["components"]["junction"],
            },
            "at_point_term": modal,
            "at_point_unit": detail,
            "age": legs.get("L2_age", {}).get("age", "?"),
            "slip_rate_class": legs.get("L3_slip", {}).get("class", "?"),
            "n_systems_15km": legs.get("L4_junction", {}).get("value", "?"),
        })
    return sites


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    sites = load_sites()
    os.makedirs(OUTDIR, exist_ok=True)
    mans, failed = [], []
    for s in sites:
        if only and only.lower() not in s["fault_name"].lower():
            continue
        print(f"[{s['rank']:>2}] {s['score']['total']:5.3f} {s['fault_name']}", file=sys.stderr)
        try:
            _, m = site_figure.build(s, outdir=OUTDIR)
            # the assertion this file exists for
            assert m["name"] == s["fault_name"], f"manifest name {m['name']} != {s['fault_name']}"
            mans.append(m)
        except Exception as exc:                                    # noqa: BLE001
            print(f"  !! BUILD FAILED {type(exc).__name__}: {exc}", file=sys.stderr)
            failed.append({"fault": s["fault_name"], "error": f"{type(exc).__name__}: {exc}"})

    man = {"n": len(mans), "n_expected": len([s for s in sites if not only]),
           "failed": failed, "source_list": FROZEN, "sites": mans}
    with open(os.path.join(OUTDIR, "_manifest.json"), "w") as fh:
        json.dump(man, fh, indent=1)
    print(f"\nrendered {len(mans)} plates, {len(failed)} failed", file=sys.stderr)
    if failed:
        sys.exit(1)
