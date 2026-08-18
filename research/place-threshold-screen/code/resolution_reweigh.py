"""A11 -- DROP THE DEAD WEIGHT, REWEIGH ON TERMS WITH ACTUAL RESOLUTION.

Clayton, Day 199: "Let's drop the dead weight and reweigh on terms with actual resolution."

A7 measured the effective degrees of freedom of the five scoring terms and found the field
is far flatter than the score's four decimal places imply. The worst offender: `slip` takes
the SAME VALUE for 86.22% of the 225 survivors. A term that agrees with itself on six
sevenths of the field is not ranking anything; it is adding a constant to almost every score
and a jolt to the remaining 14%, which is worse than adding nothing, because the jolt is not
signal -- it is the USGS slip-rate CLASS boundary, a reporting artefact of how a mapper
chose to bin a rate.

WHAT "RESOLUTION" MEANS HERE, declared before any term is scored.
A ranking term earns its place by SEPARATING PAIRS OF SITES. So the measure is the fraction
of the 225x224/2 = 25,200 unordered site pairs to which the term assigns different values:

    sep(term) = 1 - SUM_i (share_i)^2          [Simpson/Gini; exactly P(two random sites differ)]

This has no free parameter, no threshold to tune, and it is the quantity the score actually
consumes. A term with k equally populated levels scores 1 - 1/k.

THE BAR, declared before the numbers exist.
    DEAD WEIGHT if sep(term) < 0.5.
Justification, and it is not arbitrary: 0.5 is the BEST a perfectly balanced binary flag can
do. A term declared as a graded ordinal that separates fewer pairs than one coin flip is not
delivering the resolution its own specification claims. It may still be a fine GATE (a
necessary condition, pass/fail); it is not a fine RANKER. Those are different jobs and this
project has been letting one term do both.

    ! This bar may kill more than `slip`. That is the point of declaring it first. Whatever
      it kills is reported, including if it kills a term I would rather keep.

TWO REWEIGHINGS, both reported, neither privileged:
    R1 EQUAL-ON-SURVIVORS  drop dead weight, mean of what remains. (The frozen rule's own
                           form, minus the dead terms. Simplest thing that answers the ask.)
    R2 SEPARATION-WEIGHTED keep every term but weight it by sep(term), normalised. Nothing
                           is discarded; terms that order more of the field get more say.
                           This is the softer reading of "reweigh", and it is a CONTROL on
                           R1: if R1 and R2 disagree, the result is an artefact of the
                           discard, not of the resolution measurement.

AND THE TEST THAT MATTERS, because A7 makes it mandatory.
A7's finding was that the top ten is not a ranking. Any new criterion must therefore be
declared and tested AS A TIE-BREAKER AGAINST THAT MEASURED RESOLUTION, or it merely moves
names around inside a band the data cannot resolve, and calls the motion an improvement.
So each variant is put through A7's OWN one-vertex L1 bootstrap and scored on:

    BAR A  RESOLUTION GAIN. The variant must raise the count of sites holding
           P(top ten) >= 0.80. Frozen list: 4 of 10. If a reweigh does not raise that, it
           has not bought resolution -- it has bought a different arbitrary order.
    BAR B  ORDER GAIN. The variant must raise the count of adjacent pairs whose order holds
           in >= 80% of draws (conditional on both being listed). Frozen list: 4 of 9.
    BAR C  NO STEALTH SHUFFLE. If BAR A and BAR B both fail but Jaccard vs the frozen list
           is < 0.7, the reweigh has CHANGED THE ANSWER WITHOUT IMPROVING IT, and that is
           the worst of the three outcomes -- it must be reported in that language.

WHAT THIS LEG CANNOT DO. It cannot add information. Every variant here is a re-combination
of the same five measured columns; if the field is genuinely flat, no weighting recovers a
ranking from it, and the honest output is "still four ranks, different names in the band."
A11 is a test of whether the flatness was an artefact of weighting. It is not a fix for it.
"""
import json, math, random, sys
from collections import Counter, defaultdict

R = 6371.0
N_DRAWS = 10000
SEED = 20260818
SEP_KM = 50.0
LEGS = ["age", "slip", "junction", "length", "L1"]
DEAD_BAR = 0.5
P_BAR = 0.80


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def load():
    d = json.load(open("data/stage5_join_summary.json"))
    rows = []
    for r in d["survivors_ranked"]:
        c = dict(r["components"])
        c["L1"] = r["quartz_frac"]
        rows.append(dict(fault=r["fault_name"], lat=r["lat"], lon=r["lon"], comp=c))
    return rows


def wscore(c, weights):
    """Weighted mean over terms with a non-null value. A term absent from `weights` is
    dropped entirely; a term present with weight 0 is also dropped (same thing, said twice,
    so a caller cannot accidentally leave a zero-weight term contributing a denominator)."""
    num = den = 0.0
    for k, w in weights.items():
        v = c.get(k)
        if v is None or w == 0:
            continue
        num += w * v
        den += w
    return num / den if den else None


def rank_with_separation(rows, weights, k=10):
    scored = [(wscore(r["comp"], weights), r) for r in rows]
    scored = [(s, r) for s, r in scored if s is not None]
    scored.sort(key=lambda t: -t[0])
    out = []
    for s, r in scored:
        if all(hav(r["lat"], r["lon"], o["lat"], o["lon"]) >= SEP_KM for _, o in out):
            out.append((s, r))
            if len(out) >= k:
                break
    return out


# ------------------------------------------------------------ A11-i  separation
def separation(rows):
    """sep = 1 - sum(share^2) over the observed value distribution of the term."""
    out = {}
    for leg in LEGS:
        vals = [r["comp"].get(leg) for r in rows]
        vals = [v for v in vals if v is not None]
        n = len(vals)
        cnt = Counter(vals)
        sep = 1.0 - sum((c / n) ** 2 for c in cnt.values())
        top = cnt.most_common(1)[0]
        out[leg] = dict(n=n, distinct=len(cnt), sep=round(sep, 4),
                        modal_value=top[0], modal_share=round(top[1] / n, 4),
                        pairs_separated=int(round(sep * n * (n - 1) / 2)),
                        verdict=("DEAD WEIGHT" if sep < DEAD_BAR else "RESOLVES"))
    return out


# ------------------------------------------------------------ A11-ii  bootstrap
def bootstrap(rows, weights, frozen_names, draws=N_DRAWS):
    """A7's one-vertex L1 wobble, verbatim in mechanism, applied to a variant's weights.

    NOTE the gate stays at 0.25 on RAW quartz_frac in every variant, including variants that
    give L1 zero ranking weight. Dropping L1 as a RANKER is not the same act as dropping the
    lithology GATE, and conflating them would silently re-admit 1157 gated nodes under cover
    of a reweighting. If the gate is to go, that is its own leg with its own bars."""
    rnd = random.Random(SEED)
    membership, gated_out = Counter(), Counter()
    ranks = defaultdict(list)
    pair_hold, pair_both = Counter(), Counter()
    pairs = [(frozen_names[i], frozen_names[i + 1]) for i in range(len(frozen_names) - 1)]

    for _ in range(draws):
        pert = []
        for r in rows:
            c = dict(r["comp"])
            k = round(c["L1"] * 8)
            k = max(0, min(8, k + rnd.choice((-1, 0, 1))))
            c["L1"] = k / 8.0
            if c["L1"] < 0.25:
                gated_out[r["fault"]] += 1
                continue
            pert.append(dict(r, comp=c))
        names = [r["fault"] for _, r in rank_with_separation(pert, weights)]
        for i, nm in enumerate(names, 1):
            membership[nm] += 1
            ranks[nm].append(i)
        pos = {nm: i for i, nm in enumerate(names)}
        for a, b in pairs:
            if a in pos and b in pos:
                pair_both[(a, b)] += 1
                if pos[a] < pos[b]:
                    pair_hold[(a, b)] += 1

    per_site = {}
    for nm in frozen_names:
        rs = sorted(ranks.get(nm, []))
        per_site[nm] = dict(p_top10=round(membership[nm] / draws, 4),
                            p_gated_out=round(gated_out[nm] / draws, 4),
                            rank_median=(rs[len(rs) // 2] if rs else None))
    n_resolved = sum(1 for v in per_site.values() if v["p_top10"] >= P_BAR)
    order_ok = order_strict = 0
    order_rows = []
    for a, b in pairs:
        both = pair_both[(a, b)]
        p = (pair_hold[(a, b)] / both) if both else None
        order_rows.append(dict(above=a, below=b, both_present=both,
                               p_order_holds=(round(p, 4) if p is not None else None)))
        if p is not None and p >= P_BAR:
            order_ok += 1
        if p is not None and p >= 1.0:
            order_strict += 1
    # TWO counts, because they are two different published claims and reporting only the
    # looser one would read as a contradiction of A7. A7's headline "4 of 9 hold" counted
    # pairs at p == 1.0 (order FULLY determined). This leg's BAR_B uses p >= 0.80 and gets
    # 6 of 9 on the same draws -- verified identical pair-by-pair against
    # data/rank_resolution.json before this line was written. Neither number is wrong; they
    # answer "never once swapped" and "swaps in under a fifth of draws".
    intruders = {nm: round(c / draws, 4) for nm, c in membership.items()
                 if nm not in frozen_names and c / draws >= 0.05}
    return dict(per_site=per_site, n_resolved=n_resolved, n_pairs=len(pairs),
                order_holds=order_ok, order_holds_strict=order_strict,
                order_rows=order_rows, intruders=intruders)


def jaccard(a, b):
    sa, sb = set(a), set(b)
    return round(len(sa & sb) / len(sa | sb), 4) if (sa | sb) else 0.0


if __name__ == "__main__":
    rows = load()
    frozen = [s["fault"] for s in json.load(open("data/top10_frozen.json"))["sites"]]
    print(f"[A11] {len(rows)} survivors, {len(frozen)} frozen names", file=sys.stderr)

    sep = separation(rows)
    dead = [k for k, v in sep.items() if v["verdict"] == "DEAD WEIGHT"]
    alive = [k for k in LEGS if k not in dead]
    print("[A11-i] separation:", file=sys.stderr)
    for k in LEGS:
        v = sep[k]
        print(f"    {k:9s} sep={v['sep']:.4f}  distinct={v['distinct']:3d}  "
              f"modal_share={v['modal_share']:.4f}  {v['verdict']}", file=sys.stderr)
    print(f"[A11-i] DEAD WEIGHT: {dead or 'none'} | SURVIVING: {alive}", file=sys.stderr)

    variants = {
        "FROZEN": {k: 1.0 for k in LEGS},
        "R1_equal_on_survivors": {k: 1.0 for k in alive},
        "R2_separation_weighted": {k: sep[k]["sep"] for k in LEGS},
    }
    if not dead:
        print("[A11] no term met the dead-weight bar; R1 is identical to FROZEN and is "
              "reported as such rather than dropped, so the null result is visible.",
              file=sys.stderr)

    results = {}
    for name, w in variants.items():
        top = [r["fault"] for _, r in rank_with_separation(rows, w)]
        bs = bootstrap(rows, w, frozen)
        results[name] = dict(weights={k: round(v, 4) for k, v in w.items()},
                             top10=top, jaccard_vs_frozen=jaccard(top, frozen),
                             n_resolved=bs["n_resolved"],
                             order_holds=bs["order_holds"],
                             order_holds_strict=bs["order_holds_strict"],
                             n_pairs=bs["n_pairs"],
                             per_site=bs["per_site"], order_rows=bs["order_rows"],
                             intruders=bs["intruders"])
        print(f"[A11-ii] {name:24s} jaccard={results[name]['jaccard_vs_frozen']:.3f}  "
              f"P>=0.80: {bs['n_resolved']}/10  order: {bs['order_holds']}/{bs['n_pairs']}",
              file=sys.stderr)

    base = results["FROZEN"]
    verdicts = {}
    for name in ("R1_equal_on_survivors", "R2_separation_weighted"):
        r = results[name]
        a = r["n_resolved"] > base["n_resolved"]
        b = r["order_holds"] > base["order_holds"]
        b_lost = r["order_holds"] < base["order_holds"]
        churn = r["jaccard_vs_frozen"] < 0.7
        # The `a or b` reading was written first and was WRONG, in the direction that
        # flatters the leg: a variant that gains one site of membership and LOSES two
        # adjacent order pairs has not bought resolution, it has traded one kind of
        # instability for another while replacing over half the list. A gain must be a gain
        # on one bar with NO LOSS on the other, or it is a trade and must say so.
        if a and b:
            summary = "RESOLUTION GAINED on both bars"
        elif (a and not b_lost) or (b and not b_lost and not a):
            summary = "RESOLUTION GAINED on one bar, no loss on the other"
        elif (a or b) and b_lost:
            summary = ("TRADE, NOT A GAIN -- one bar up, the other down"
                       + (" and over half the list changed" if churn else ""))
        elif churn:
            summary = "STEALTH SHUFFLE -- changed the answer without improving it"
        else:
            summary = "NO GAIN, NO SHUFFLE -- the reweigh is a no-op on resolution"
        verdicts[name] = dict(
            BAR_A_resolution_gain=dict(passed=a, was=base["n_resolved"],
                                       now=r["n_resolved"]),
            BAR_B_order_gain=dict(passed=b, lost=b_lost, was=base["order_holds"],
                                  now=r["order_holds"],
                                  was_strict=base["order_holds_strict"],
                                  now_strict=r["order_holds_strict"]),
            BAR_C_stealth_shuffle=dict(triggered=churn,
                                       jaccard=r["jaccard_vs_frozen"]),
            summary=summary)
        print(f"[A11-iii] {name}: {verdicts[name]['summary']}", file=sys.stderr)

    out = dict(leg="A11 resolution reweigh",
               frozen="Day 199, 2026-08-18; bars in resolution_reweigh.py docstring, "
                      "written before any term was scored",
               seed=SEED, draws=N_DRAWS, population=len(rows),
               dead_weight_bar=DEAD_BAR, p_bar=P_BAR,
               A11i_separation=sep, dead_weight=dead, surviving_terms=alive,
               A11ii_variants=results, A11iii_verdicts=verdicts)
    json.dump(out, open("data/resolution_reweigh.json", "w"), indent=1)
    print("[A11] wrote data/resolution_reweigh.json", file=sys.stderr)
