#!/usr/bin/env python3
"""l1_detail_round2.py — along-trace L1 detail for the two areas that entered the
deliverable in round 2.

The eight round-1 areas print an L1 bullet carrying `quartz_frac = h/8 vertices —
N x <rock>`, `along X km of trace, N segments`. That detail comes from the
along-trace probe, and it is NOT in data/stage5_join_rows.json, which stores only
the leg's value. Centennial fault and Antelope Valley fault zone were never in the
round-1 dossier, so nothing on disk carries their version of it.

This runs the SAME callable the eight were measured with — remeasure_ten.measure()
over remeasure_ten.pull_exact_retry() — rather than retyping anything, and it does
it through the module's own discipline:

  1. Both declared controls go through the identical path FIRST and must reproduce
     their declared values exactly. Sandia 0.875 / Hubbell Spring 0.000. If the
     path has moved, nothing is written. (This is the check that killed the
     local-geometry shortcut in round 1: the negative control agreed down both
     paths and only the positive one caught it.)
  2. Each new site's freshly measured quartz_frac is asserted against the value
     data/stage5_join_rows.json already carries for it. A live re-pull that
     disagrees with the frozen join means the article would print two different
     numbers for the same leg, so it aborts rather than picking one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import remeasure_ten as R  # noqa: E402

WANT = ["Centennial fault", "Antelope Valley fault zone"]
CONTROLS = {"Sandia fault": 0.875, "Hubbell Spring fault": 0.0}
OUT = "data/l1_detail_round2.json"


QUALIFYING = ("TIER_PLUTONIC", "TIER_FABRIC")


def terms_of(rec):
    """The bullet's `7x granite, 1x no qualifying unit` breakdown, as the dossier builds it."""
    t = {}
    for p in rec["pts"]:
        k = p.get("term") or "no qualifying unit"
        t[k] = t.get(k, 0) + 1
    return sorted(t.items(), key=lambda kv: (-kv[1], kv[0]))


def split_terms(rec):
    """Terms split by whether the tier ladder counts them toward quartz_frac.

    The dossier's eight print `quartz_frac 0.875 = 7/8 vertices - 7x granite`, where
    the vertex count and the term list happen to coincide because every named rock at
    those sites qualified. That is not general. Centennial returns a rhyolite: a named
    rock, at a measured vertex, in TIER_VOLCANIC, which does NOT count toward the gate.
    Printing 5/8 there would inflate the gate reading by a vertex under a label that
    says quartz_frac. Split, so the bullet can say which is which.
    """
    q, nq = {}, {}
    for p in rec["pts"]:
        term, tier = p.get("term"), p.get("tier")
        if not term:
            nq["no qualifying unit"] = nq.get("no qualifying unit", 0) + 1
        elif tier in QUALIFYING:
            q[term] = q.get(term, 0) + 1
        else:
            nq[term] = nq.get(term, 0) + 1
    key = lambda d: sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))  # noqa: E731
    return key(q), key(nq), sum(q.values())


def main():
    stage5 = {r["fault_name"]: r
              for r in json.load(open("data/stage5_join_rows.json", encoding="utf-8"))["rows"]}

    out = {"controls": {}, "sites": {}}
    print("== controls through the path this run uses", file=sys.stderr)
    for nm, declared in CONTROLS.items():
        got = R.measure(nm, R.pull_exact_retry(nm))
        agree = got["quartz_frac"] is not None and abs(got["quartz_frac"] - declared) < 1e-9
        out["controls"][nm] = {"declared": declared, "measured": got["quartz_frac"],
                               "n_pts": got["n_pts"], "segments": got["segments"],
                               "agree": bool(agree)}
        print(f"   {nm:<24} declared {declared:<6} measured {got['quartz_frac']} "
              f"{'AGREE' if agree else 'DISAGREE'}", file=sys.stderr)
        if not agree:
            sys.exit(f"[abort] control {nm} does not reproduce; the probe has moved. "
                     "Nothing written.")
    out["controls_reproduce"] = True

    print("\n== the two round-2 sites", file=sys.stderr)
    for nm in WANT:
        r = R.measure(nm, R.pull_exact_retry(nm))
        frozen = stage5[nm]["legs"]["L1_lithology"]["value"]
        if r["quartz_frac"] is None or abs(r["quartz_frac"] - frozen) > 1e-9:
            sys.exit(f"[abort] {nm}: live probe reads quartz_frac {r['quartz_frac']}, "
                     f"stage5_join_rows.json carries {frozen}. The article would print "
                     "two different numbers for one leg.")
        hit = sum(1 for p in r["pts"] if p.get("term"))
        qual, nonqual, n_qual = split_terms(r)
        # the gate reading and the qualifying-vertex count must be the same statement
        if abs(n_qual / r["n_pts"] - r["quartz_frac"]) > 1e-9:
            sys.exit(f"[abort] {nm}: {n_qual}/{r['n_pts']} qualifying vertices does not "
                     f"reproduce quartz_frac {r['quartz_frac']}.")
        out["sites"][nm] = {
            "quartz_frac": r["quartz_frac"], "fabric_frac": r["fabric_frac"],
            "vertices_any_term": hit, "vertices_qualifying": n_qual, "n_pts": r["n_pts"],
            "traced_km": r["traced_km"], "segments": r["segments"],
            "terms": terms_of(r),
            "terms_qualifying": qual, "terms_not_qualifying": nonqual,
            "agrees_with_stage5": True,
        }
        print(f"   {nm:<30} frac={r['quartz_frac']} {n_qual}/{r['n_pts']} qualifying "
              f"({hit} named)  {r['traced_km']} km  {r['segments']} segs  "
              f"qual={qual} other={nonqual}", file=sys.stderr)

    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print(f"\nwrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
