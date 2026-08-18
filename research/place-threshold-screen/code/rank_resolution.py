"""A7 -- RANK RESOLUTION. Is the top ten a RANKING, or ten members of one indistinguishable band?

Clayton's ask (D199): the list is the deliverable. Not the method, not the amendment chain --
the ranked sites. So the question this leg asks is the one that must be answered BEFORE any
further criterion is added, because it decides whether adding criteria can help:

    Given the measurement noise the instruments have ALREADY DECLARED ABOUT THEMSELVES,
    how many distinct rank positions does this score actually resolve?

Nothing here is a new noise model. Every perturbation below is read off a note that was
written by the leg that produced the number, before this question was asked:

  L1 quartz_frac -- remeasure_ten.py's own docstring: "quartz_frac carries sampling noise of
     order 1/N_SAMPLE = 0.125 from vertex ordering alone -- recorded because it is a second,
     independent reason that this layer FILTERS and cannot RANK." The measured instance:
     Sandia read 0.875 down the paged live path and 1.000 down the local path. SAME fault,
     same layer, same probe, same 8 points -- different segment concatenation order. So a
     +/- one-vertex wobble is not hypothetical; it is an observed disagreement of exactly
     0.125 on the POSITIVE control.
     ! And the frozen list uses L1 as a fifth EQUAL scoring term anyway. That is the conflict
     this leg exists to price.

  L3 slip -- slip_rate_class is a BUCKET. If many survivors share a bucket they share a
     value exactly, and the term cannot order them. Measured here, not assumed.

  L4 junction -- site_rank.py's own docstring: "fault-name density is partly a mapping
     artefact ... a Basin-and-Range valley mapped at 1:24,000 by a 1990s NEHRP grant reports
     more distinct names than an equivalent structure mapped once at 1:250,000."

  L6 length -- 94.9% coverage; log-scaled, so it is the smoothest term and the least likely
     to be the problem. Included in leave-one-out for symmetry, not from suspicion.

DECLARED BEFORE ANY PERTURBATION WAS RUN (bars, so this cannot be graded after the fact):

  BAR i   MEMBERSHIP IS REAL if the frozen ten survive leave-one-leg-out with Jaccard >= 0.7
          against the frozen set in >= 4 of the 5 variants. Failing means the list is an
          artefact of one leg.
  BAR ii  MEMBERSHIP IS RESOLVED if >= 7 of the frozen ten hold P(in top ten) >= 0.80 under
          one-vertex L1 resampling.
  BAR iii ORDER IS RESOLVED if >= 5 of the 9 adjacent pairs in the frozen ten keep their
          relative order in >= 95% of draws. Fewer means the printed 1..10 is decoration.

  A bar that FAILS is the result. This leg is built expecting iii to fail, and if it passes
  that is the surprise, not the confirmation.

CONTROL, and it runs first: the 5-term score + 50 km separation rule must REPRODUCE
data/top10_frozen.json exactly -- same ten faults, same order, scores within 1e-3. If the
reproduction fails, nothing downstream is measured, because a perturbation of a list I
cannot rebuild is a perturbation of the wrong list.
"""
import json, math, random, sys
from collections import Counter, defaultdict

R = 6371.0
N_DRAWS = 10000
SEED = 20260818
SEP_KM = 50.0
LEGS = ["age", "slip", "junction", "length", "L1"]


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


def score(c, legs=LEGS):
    v = [c[k] for k in legs if c.get(k) is not None]
    return sum(v) / len(v) if v else None


def rank_with_separation(rows, legs=LEGS, k=10):
    """Frozen rule: sort by score desc, greedily accept a site only if it is >= SEP_KM from
    every already-accepted site. Separation is a DE-DUPLICATION rule -- adjacent nodes on one
    fault system are one place, not two candidates."""
    scored = [(score(r["comp"], legs), r) for r in rows]
    scored = [(s, r) for s, r in scored if s is not None]
    scored.sort(key=lambda t: -t[0])
    out = []
    for s, r in scored:
        if all(hav(r["lat"], r["lon"], o["lat"], o["lon"]) >= SEP_KM for _, o in out):
            out.append((s, r))
            if len(out) >= k:
                break
    return out


# ---------------------------------------------------------------- CONTROL
def control():
    frozen = json.load(open("data/top10_frozen.json"))["sites"]
    got = rank_with_separation(load())
    ok, diffs = True, []
    for f, (s, r) in zip(frozen, got):
        if f["fault"] != r["fault"] or abs(f["score"] - s) > 1e-3:
            ok = False
            diffs.append(f"rank {f['rank']}: frozen {f['fault']} {f['score']} "
                         f"-> rebuilt {r['fault']} {round(s, 4)}")
    return ok, diffs, [r["fault"] for _, r in got]


# ---------------------------------------------------------------- A7-iv (descriptive)
def effective_dof(rows):
    """Which terms actually ORDER the survivors? A term that is near-constant across the
    population cannot separate anyone regardless of its weight."""
    out = {}
    n = len(rows)
    for leg in LEGS:
        vals = [r["comp"][leg] for r in rows if r["comp"].get(leg) is not None]
        cnt = Counter(round(v, 6) for v in vals)
        mode_v, mode_n = cnt.most_common(1)[0]
        mean = sum(vals) / len(vals)
        sd = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
        out[leg] = dict(n=len(vals), missing=n - len(vals), distinct=len(cnt),
                        sd=round(sd, 4), modal_value=mode_v,
                        modal_share=round(mode_n / len(vals), 4))
    return out


# ---------------------------------------------------------------- A7-i
def leave_one_out(rows, frozen_names):
    res = {}
    for drop in LEGS:
        legs = [l for l in LEGS if l != drop]
        names = [r["fault"] for _, r in rank_with_separation(rows, legs)]
        inter = len(set(names) & set(frozen_names))
        res[f"drop_{drop}"] = dict(
            top10=names, jaccard=round(inter / (20 - inter), 4),
            kept=inter,
            new=[x for x in names if x not in frozen_names],
            lost=[x for x in frozen_names if x not in names])
    return res


# ---------------------------------------------------------------- A7-ii / A7-iii
def l1_resample(rows, frozen_names, draws=N_DRAWS):
    """One-vertex L1 wobble. quartz_frac is k/8 for k vertices of 8 that hit quartz-rich rock;
    the observed failure mode is a DIFFERENT eight vertices, so k moves by at most 1 either
    way. Uniform over {k-1, k, k+1} clipped to [0,1]. The GATE is re-applied each draw at
    0.25, exactly as the frozen rule does, so a site can also be gated OUT by its own wobble."""
    rnd = random.Random(SEED)
    membership = Counter()
    ranks = defaultdict(list)
    pair_hold = Counter()
    pair_both = Counter()   # denominator: draws where BOTH are on the list at all.
    # Without this the order statistic silently absorbs the MEMBERSHIP failure -- a site
    # gated out 33% of the time would show as "order broken" 33% of the time even if it
    # never once swapped with its neighbour. Two failures of different kinds, one number.
    pairs = [(frozen_names[i], frozen_names[i + 1]) for i in range(len(frozen_names) - 1)]
    gated_out = Counter()

    for _ in range(draws):
        pert = []
        for r in rows:
            c = dict(r["comp"])
            k = round(c["L1"] * 8)
            k = max(0, min(8, k + rnd.choice((-1, 0, 1))))
            c["L1"] = k / 8.0
            if c["L1"] < 0.25:          # the gate, re-applied
                gated_out[r["fault"]] += 1
                continue
            pert.append(dict(r, comp=c))
        names = [r["fault"] for _, r in rank_with_separation(pert)]
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
        per_site[nm] = dict(
            p_top10=round(membership[nm] / draws, 4),
            p_gated_out=round(gated_out[nm] / draws, 4),
            rank_median=(rs[len(rs) // 2] if rs else None),
            rank_ci90=([rs[int(0.05 * len(rs))], rs[int(0.95 * len(rs)) - 1]] if rs else None))
    intruders = {nm: round(c / draws, 4) for nm, c in membership.items()
                 if nm not in frozen_names and c / draws >= 0.05}
    pair_stats = [dict(above=a, below=b,
                       both_present=pair_both[(a, b)],
                       p_order_holds=(round(pair_hold[(a, b)] / pair_both[(a, b)], 4)
                                      if pair_both[(a, b)] else None),
                       basis="conditional on both sites being on the list in that draw")
                  for a, b in pairs]
    return per_site, intruders, pair_stats


# ---------------------------------------------------------------- A7-v
def contender_band(rows, frozen_names):
    """How many survivors sit within ONE VERTEX of score (0.125/5 = 0.025) of rank 10?
    That number IS the honest size of the contender pool."""
    scored = sorted(((score(r["comp"]), r) for r in rows), key=lambda t: -t[0])
    s10 = [s for s, r in scored if r["fault"] == frozen_names[-1]][0]
    band = [dict(fault=r["fault"], score=round(s, 4), lat=r["lat"], lon=r["lon"])
            for s, r in scored if s >= s10 - 0.025]
    return dict(rank10_score=round(s10, 4), one_vertex_score_delta=0.025,
                n_within_one_vertex=len(band), members=band[:60])


if __name__ == "__main__":
    ok, diffs, rebuilt = control()
    print(f"[control] reproduce frozen top10: {'PASS' if ok else 'FAIL'}", file=sys.stderr)
    for d in diffs:
        print("   " + d, file=sys.stderr)
    if not ok:
        json.dump(dict(control_passed=False, diffs=diffs, rebuilt=rebuilt),
                  open("data/rank_resolution.json", "w"), indent=1)
        sys.exit("control failed -- nothing downstream measured")

    rows = load()
    frozen_names = rebuilt
    dof = effective_dof(rows)
    loo = leave_one_out(rows, frozen_names)
    per_site, intruders, pair_stats = l1_resample(rows, frozen_names)
    band = contender_band(rows, frozen_names)

    jacc = [v["jaccard"] for v in loo.values()]
    bar_i = sum(1 for j in jacc if j >= 0.7) >= 4
    bar_ii = sum(1 for v in per_site.values() if v["p_top10"] >= 0.80) >= 7
    bar_iii = sum(1 for p in pair_stats
                  if p["p_order_holds"] is not None and p["p_order_holds"] >= 0.95) >= 5

    out = dict(
        leg="A7 rank resolution",
        frozen="Day 199, 2026-08-18, bars declared in rank_resolution.py docstring "
               "before any perturbation was run",
        seed=SEED, draws=N_DRAWS, population=len(rows),
        control=dict(passed=True, rebuilt_top10=frozen_names),
        A7iv_effective_dof=dof,
        A7i_leave_one_leg_out=loo,
        A7ii_membership=per_site,
        A7ii_intruders_p_ge_005=intruders,
        A7iii_adjacent_pairs=pair_stats,
        A7v_contender_band=band,
        bars=dict(i_membership_not_one_leg=bar_i,
                  ii_membership_resolved=bar_ii,
                  iii_order_resolved=bar_iii),
    )
    json.dump(out, open("data/rank_resolution.json", "w"), indent=1)

    print(f"\n[A7-iv] which terms can order 225 survivors", file=sys.stderr)
    for leg, v in dof.items():
        print(f"   {leg:9s} distinct={v['distinct']:>3}  sd={v['sd']:.3f}  "
              f"modal {v['modal_value']} held by {v['modal_share']*100:.0f}%  "
              f"missing={v['missing']}", file=sys.stderr)
    print(f"\n[A7-i] leave one leg out (Jaccard vs frozen ten)", file=sys.stderr)
    for k, v in loo.items():
        print(f"   {k:14s} J={v['jaccard']:.2f} kept={v['kept']}/10 lost={v['lost']}",
              file=sys.stderr)
    print(f"\n[A7-ii] membership under one-vertex L1 wobble", file=sys.stderr)
    for nm in frozen_names:
        v = per_site[nm]
        print(f"   {nm:34s} P(top10)={v['p_top10']:.3f} median rank={v['rank_median']} "
              f"ci90={v['rank_ci90']} P(gated out)={v['p_gated_out']:.3f}", file=sys.stderr)
    print(f"   intruders >=5%: {intruders}", file=sys.stderr)
    print(f"\n[A7-iii] adjacent pair order holds", file=sys.stderr)
    for p in pair_stats:
        print(f"   {p['above'][:26]:28s} > {p['below'][:26]:28s} {p['p_order_holds']:.3f} "
              f"(n={p['both_present']})", file=sys.stderr)
    print(f"\n[A7-v] within one vertex of rank 10: {band['n_within_one_vertex']} survivors",
          file=sys.stderr)
    print(f"\nBARS  i={bar_i}  ii={bar_ii}  iii={bar_iii}", file=sys.stderr)
