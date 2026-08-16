"""LORE EXPERIMENT -- scoring and readout. Rubric applied AS FROZEN, not renegotiated.

ONE DISCRIMINATOR HAD TO BE MADE EXPLICIT DURING SCORING, and it is recorded here
rather than buried: the T3 definition turns on "a NAMED, place-specific recurring
record". Several sites returned a recurring regional sighting HISTORY (Lake Tahoe,
Albuquerque) with real newspaper attestation but no named phenomenon; several
returned a NAMED light (Diamond City Light, Yellow Creek, Santa Fe's Spook Lane)
attested only by a tour operator or a folklore blog. Both are T2 under the rule as
written, and the rule was applied that way to WINNERS AND DECOYS ALIKE -- including
where it cost the known-positive. Sandia's Kirtland AFB 1957 case is a named
INCIDENT, not a named recurring light, so Sandia scores T2 like everything else.
That is the tell that the rubric was not bent toward the result I expected.

Result: T3 was awarded ZERO times in 20 sites. See the readout for what that means
about the instrument, which is the larger finding here.
"""
import json, math, os
from itertools import combinations

W = os.path.dirname(os.path.abspath(__file__))

# tier, and the single most load-bearing thing the protocol returned
SCORES = {
    # ---- WINNERS (physics top 10, 100 km separation)
    "Madison fault": (0, "1959 quake geology only; one 2003 light nr W Yellowstone "
                         "(~30km, one-off) -> fails both T1 clauses"),
    "Round Valley fault": (1, "Eastern Sierra / Owens Valley recurring sighting "
                              "record at 25-60km (Bishop 2012, Lone Pine 1991)"),
    "Little Valley fault": (2, "Lake Tahoe recurring UFO record <25km; local paper "
                               "+ Tahoetopia 'Lost Legend #5'; no NAMED light"),
    "Helena valley fault": (1, "Diamond City Light -- NAMED, but ~60km (Confederate "
                               "Gulch), so 25-60km clause"),
    "Red Rock fault": (0, "nothing; Lima/Dell returned geology and one 2016 "
                          "Beaverhead County orb, county-level not site-level"),
    "Sand Springs Range fault": (1, "Fallon 'UFO Capital of the West', recurring -- "
                                    "but 41-49km away, 25-60km clause"),
    "Mosquito fault": (2, "'unusual white lights and strange buzzing' at Alma "
                          "(7.6km), ghostsofamerica aggregator only"),
    "Sandia fault": (2, "Albuquerque recurring record <25km; Kirtland AFB 1957 is a "
                        "NAMED INCIDENT not a named recurring light -> T2 by rule"),
    "Bear River fault zone": (2, "Yellow Creek unexplained lights, NAMED and "
                                 "recurring, ~20km -- but folklore-blog attestation"),
    "Teton fault": (2, "glowing orbs nr Grand Teton + Teton Pass 'hotspot for "
                       "strange lights', recurring; web-native attestation"),
    # ---- DECOYS (bottom-half physics, matched on observer density)
    "Big Chino fault": (2, "Seligman appears REPEATEDLY in FBI UFO files 1940s-60s "
                           "(newspaper), 16.3km, recurring -- but no named light"),
    "Thompson Valley fault": (0, "one 2014 orb at Hot Springs (28.5km, one-off)"),
    "Bear River Range faults": (1, "1949 Sardine Canyon light+explosion, FBI/"
                                   "newspaper, ~25km, but a ONE-OFF event"),
    "Bull Mountain western border fault": (0, "Elkhorn ghost TOWN, no light record"),
    "Lida faults": (0, "Goldfield hauntings are apparitions in buildings, 44km, "
                       "no light record"),
    "Lone Pine fault": (1, "'Russian John' apparition Clayton ID (34km, recurring "
                           "since 1920s); Salmon-Challis UFO tales, vague"),
    "unnamed faults west of Hungry Valley": (0, "nothing at Lemmon Valley"),
    "Picuris-Pecos fault": (2, "Santa Fe 'Spook Lane' / 'Shades of Death Path' "
                               "devil-lights, NAMED, ~18km, tour-operator source"),
    "Sweetwater fault": (0, "Virginia City hauntings are apparitions, no lights"),
    "unnamed fault near Ovando": (0, "nothing at Seeley Lake"),
}


def sign_test(diffs):
    """Exact two-sided sign test over non-tied pairs."""
    nz = [d for d in diffs if d != 0]
    n, k = len(nz), sum(1 for d in nz if d > 0)
    if n == 0:
        return n, k, 1.0
    tail = sum(math.comb(n, i) for i in range(max(k, n - k), n + 1))
    return n, k, min(1.0, 2 * tail / 2 ** n)


def spearman(x, y):
    def rk(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for t in range(i, j + 1):
                r[s[t]] = avg
            i = j + 1
        return r
    rx, ry = rk(x), rk(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


if __name__ == "__main__":
    d = json.load(open(os.path.join(W, "lore_experiment_design.json"),
                      encoding="utf-8"))
    rows = []
    for p in d["pairs"]:
        w, dc = p["winner"], p["decoy"]
        wt, wn = SCORES[w["fault"]]
        dt, dn = SCORES[dc["fault"]]
        rows.append({"rank": w["rank"], "winner": w["fault"], "winner_tier": wt,
                     "winner_note": wn, "winner_obs": p["winner_obs"],
                     "decoy": dc["fault"], "decoy_tier": dt, "decoy_note": dn,
                     "decoy_obs": p["decoy_obs"],
                     "decoy_physics_score": dc["score"],
                     "winner_physics_score": w["score"]})

    wt = [r["winner_tier"] for r in rows]
    dt = [r["decoy_tier"] for r in rows]
    diffs = [a - b for a, b in zip(wt, dt)]
    n, k, p = sign_test(diffs)
    wmean, dmean = sum(wt) / len(wt), sum(dt) / len(dt)
    rho = spearman([r["rank"] for r in rows], wt)

    print("=" * 78)
    print("  LORE EXPERIMENT -- 20 sites, 60 queries, rubric frozen before lookup")
    print("=" * 78)
    print(f"{'#':>3} {'WINNER':<28}{'T':>2}   {'DECOY':<30}{'T':>2}  {'obs W/D':>8}")
    for r in rows:
        print(f"{r['rank']:>3} {r['winner'][:28]:<28}{r['winner_tier']:>2}   "
              f"{r['decoy'][:30]:<30}{r['decoy_tier']:>2}  "
              f"{r['winner_obs']:>3}/{r['decoy_obs']:<3}")

    print(f"\n  mean tier   winners {wmean:.2f}   decoys {dmean:.2f}   "
          f"difference {wmean - dmean:+.2f}")
    print(f"  T2 or above winners {sum(1 for t in wt if t >= 2)}/10   "
          f"decoys {sum(1 for t in dt if t >= 2)}/10")
    print(f"  T3 awarded  {sum(1 for t in wt + dt if t == 3)}/20  <-- see readout")
    print(f"  paired sign test: {k}/{n} non-tied pairs favour the winner, "
          f"two-sided p = {p:.3f}")
    print(f"  within winners, Spearman(physics rank, tier) = {rho:+.3f}  "
          f"(rank 1 = best physics)")

    supported = (wmean - dmean) >= 1.0
    print("\n" + "-" * 78)
    print(f"  PRE-DECLARED RULE: >=1.00 tier separation, predicted direction.")
    print(f"  OBSERVED: {wmean - dmean:+.2f}.  VERDICT: "
          f"{'H1 SUPPORTED' if supported else 'H1 NOT SUPPORTED'}")
    print("-" * 78)

    out = {"verdict": "SUPPORTED" if supported else "NOT SUPPORTED",
           "winner_mean_tier": round(wmean, 3), "decoy_mean_tier": round(dmean, 3),
           "separation": round(wmean - dmean, 3), "required": 1.0,
           "sign_test": {"non_tied": n, "favour_winner": k, "p_two_sided": round(p, 4)},
           "t3_awarded_of_20": sum(1 for t in wt + dt if t == 3),
           "spearman_rank_vs_tier_within_winners": round(rho, 3),
           "rows": rows}
    json.dump(out, open(os.path.join(W, "lore_experiment_result.json"), "w"), indent=1)
    print(f"\n[wrote] lore_experiment_result.json")
