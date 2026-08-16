"""THE LORE EXPERIMENT -- design, matched null set, and pre-declared rubric.
Written and committed BEFORE a single lore query is run. That ordering is the
whole instrument; everything else here is bookkeeping.

WHAT IS BEING TESTED. The physics screen ranked 225 complete-legs faults with the
folk/light record held out entirely. The claim under test is:

    H1: sites the physics ranks highly carry a heavier anomalous-light / folk
        record than physics-comparable sites the ranking rejects.

THE WAY THIS EXPERIMENT DIES, and it dies here if anywhere: LORE REQUIRES
WITNESSES. A fault in the Nevada outback with nobody within 60 km cannot generate
a light record no matter what it does, and a fault under a metro area generates one
whatever it does. Left alone, this experiment measures the distribution of PEOPLE
and reports it as a property of ROCK. Ten winners with lore and ten unmatched
nulls without would look like a result and be a census.

So the null set is matched on the confounder, not drawn at random:
  - OBSERVER PROXY: incorporated places (Census 2023 gazetteer) within 50 km of the
    site coordinate, plus km to the nearest one. Not population -- place COUNT --
    because it needs no population join and is monotone in the thing that matters.
  - Each winner gets one decoy from the SAME 225-fault population, chosen to
    minimise |log observer-proxy difference| while scoring in the BOTTOM HALF of
    the physics ranking and sitting >= 25 km from every winner and every decoy
    already chosen. Same rock class, same rough witness density, opposite physics.
  - The pairing is reported with its residual mismatch. A pair that could not be
    matched is marked UNMATCHED and excluded from the headline count rather than
    quietly averaged in.

PRE-DECLARED RUBRIC -- fixed now, applied identically to winners and decoys, and
not to be renegotiated after the first surprising result:

  T3  A NAMED, place-specific recurring anomalous-light or apparition record
      within 25 km of the site coordinate, attested in a source that is not
      itself a listicle -- newspaper archive, folklore collection, state
      historical society, academic treatment, or a pre-1995 printed source.
  T2  A recurring anomaly record within 25 km, but attested only in modern
      web-native aggregators (ghost-site directories, UFO databases, listicles).
  T1  Isolated or one-off reports only within 25 km, or a recurring record at
      25-60 km that is not plausibly the same site.
  T0  Nothing found under the protocol.

  PROTOCOL, identical per site, no site gets an extra pass: three queries --
      (a) "<fault name>" + the two nearest named places + ghost lights
      (b) <nearest place>, <state> + mystery lights OR spook light OR ghost light
      (c) <nearest place>, <state> + UFO sightings history
  Whatever the first pass returns is the score. Chasing a promising thread on a
  winner and not on its decoy is how a null result gets converted into a positive
  one without anybody deciding to cheat.

  SCORED BLIND? NO -- and it is recorded here rather than claimed away. I know
  which names are winners. The mitigation is that the query template, the query
  COUNT and the tier definitions are frozen in this file before any lookup, so the
  discretion left to me is scoring, not searching. Read the tier assignments as
  the weakest link in the chain.

PRE-DECLARED READOUT. Winners minus decoys, on mean tier and on count of T3+T2.
  - Separation of >= 1 full tier on the mean, in the predicted direction: H1 SUPPORTED.
  - Anything less, or the wrong sign: H1 NOT SUPPORTED, and it gets written up
    that way. n=10 pairs is small; this can refute, it cannot confirm.
"""
import json, math, os, io, zipfile

W = os.path.dirname(os.path.abspath(__file__))
R = 6371.0
OBS_KM = 50.0
MIN_SEP_KM = 25.0


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def load_places():
    """Census 2023 gazetteer, incorporated + CDP places. (name, state, lat, lon)."""
    z = zipfile.ZipFile(os.path.join(W, "gaz_place.zip"))
    raw = z.read(z.namelist()[0]).decode("utf-8", "replace")
    rows, hdr = [], None
    for line in io.StringIO(raw):
        f = [x.strip() for x in line.rstrip("\n").split("\t")]
        if hdr is None:
            hdr = f
            continue
        try:
            rows.append((f[hdr.index("NAME")], f[hdr.index("USPS")],
                         float(f[hdr.index("INTPTLAT")]),
                         float(f[hdr.index("INTPTLONG")])))
        except (ValueError, IndexError):
            continue
    return rows


def observer(places, lat, lon):
    near = []
    for nm, st, la, lo in places:
        if abs(la - lat) > 1.2 or abs(lo - lon) > 1.6:
            continue
        d = hav(lat, lon, la, lo)
        if d <= 120.0:
            near.append((d, nm, st))
    near.sort()
    return {"places_within_50km": sum(1 for d, _, _ in near if d <= OBS_KM),
            "nearest_km": round(near[0][0], 1) if near else None,
            "nearest": [{"place": n, "state": s, "km": round(d, 1)}
                        for d, n, s in near[:3]]}


if __name__ == "__main__":
    top = json.load(open(os.path.join(W, "top10_frozen_100km.json"),
                        encoding="utf-8"))
    join = json.load(open(os.path.join(W, "stage5_join.json"), encoding="utf-8"))
    places = load_places()
    print(f"[places] {len(places)} census places loaded")

    # full scored population, same rule as top10_rerank.py
    pop = []
    for r in join["rows"]:
        if r["gate_L1"] != "PASS" or not r["complete"]:
            continue
        q = r["legs"]["L1_lithology"]["value"]
        if q is None or r["lat"] is None or r["lon"] is None:
            continue
        c = r["components"]
        pop.append({"fault": r["fault_name"], "lat": r["lat"], "lon": r["lon"],
                    "score": round((c.get("age", 0) + c.get("slip", 0)
                                    + c.get("junction", 0) + c.get("length", 0)
                                    + q) / 5.0, 4)})
    pop.sort(key=lambda x: -x["score"])
    median = pop[len(pop) // 2]["score"]
    bottom = [x for x in pop if x["score"] < median]
    print(f"[pop] {len(pop)} survivors, median score {median}, "
          f"{len(bottom)} in the bottom half (decoy pool)")

    winners = []
    for s in top["sites"]:
        o = observer(places, s["lat"], s["lon"])
        winners.append(dict(s, observer=o))
    for b in bottom:
        b["observer"] = observer(places, b["lat"], b["lon"])

    # ---- matching: nearest observer-density neighbour in the bottom half
    taken, pairs = [], []
    for w in winners:
        wo = w["observer"]["places_within_50km"]
        best, bestcost = None, None
        for b in bottom:
            if b["fault"] in taken:
                continue
            if any(hav(b["lat"], b["lon"], x["lat"], x["lon"]) < MIN_SEP_KM
                   for x in winners + [p["decoy"] for p in pairs]):
                continue
            cost = abs(math.log1p(b["observer"]["places_within_50km"])
                       - math.log1p(wo))
            if bestcost is None or cost < bestcost:
                best, bestcost = b, cost
        if best is None:
            pairs.append({"winner": w, "decoy": None, "status": "UNMATCHED"})
            continue
        taken.append(best["fault"])
        pairs.append({"winner": w, "decoy": best, "status": "MATCHED",
                      "observer_gap": round(bestcost, 3),
                      "winner_obs": wo,
                      "decoy_obs": best["observer"]["places_within_50km"]})

    out = {"designed": "2026-08-16", "separation_km": top["separation_km"],
           "hypothesis": "H1: high physics rank -> heavier anomalous-light record",
           "rubric": {"T3": "named place-specific recurring record <=25km, "
                            "non-listicle source",
                      "T2": "recurring record <=25km, web-aggregator only",
                      "T1": "isolated/one-off <=25km, or recurring at 25-60km",
                      "T0": "nothing under protocol"},
           "protocol_queries_per_site": 3,
           "blind": False,
           "blind_note": "query template/count/tiers frozen pre-lookup; scoring "
                         "is not blind and is the weakest link",
           "observer_proxy": "census places within 50 km (2023 gazetteer)",
           "readout_rule": ">=1 full tier separation on the mean, predicted "
                           "direction = SUPPORTED; else NOT SUPPORTED",
           "pairs": pairs}
    dst = os.path.join(W, "lore_experiment_design.json")
    json.dump(out, open(dst, "w"), indent=1)

    print(f"\n{'rank':>4}  {'WINNER':<32} {'obs':>4} {'near':>18}   "
          f"{'DECOY (bottom half)':<32} {'obs':>4} {'scr':>6}")
    for p in pairs:
        w = p["winner"]
        n = w["observer"]["nearest"][0] if w["observer"]["nearest"] else None
        nn = f"{n['place'][:14]},{n['state']}" if n else "--"
        if p["decoy"] is None:
            print(f"{w['rank']:>4}  {w['fault'][:32]:<32} "
                  f"{w['observer']['places_within_50km']:>4} {nn:>18}   "
                  f"{'*** UNMATCHED ***':<32}")
            continue
        d = p["decoy"]
        print(f"{w['rank']:>4}  {w['fault'][:32]:<32} "
              f"{w['observer']['places_within_50km']:>4} {nn:>18}   "
              f"{d['fault'][:32]:<32} "
              f"{d['observer']['places_within_50km']:>4} {d['score']:6.3f}")
    print(f"\n[wrote] {dst}")
