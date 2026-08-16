"""BLIND RE-SCORE -- unblind and read out.  §7.1.

Run only after every scorer column is on disk.  Order of operations is the order
declared in blind_rescore_design.py: probes first, VOID rule applied, and only then
is the keymap opened.
"""
import json
import os
from fractions import Fraction
from math import comb


def sep_exact(a, b):
    """Separation of two integer-tier lists as an EXACT rational.

    Not decorative.  The blind H-3 consensus is winners 23/10 minus decoys 13/10,
    which is 1 exactly and 0.9999999999999998 in binary floating point -- and the
    pre-declared readout rule is `>= 1.0`.  Read off floats, the verdict at the
    boundary is decided by the representation rather than by the data.  The first
    run of this script did exactly that and reported NOT SUPPORTED.
    """
    n = len(a)
    return Fraction(sum(a), n) - Fraction(sum(b), n)


def verdict(a, b, bar=1):
    return "SUPPORTED" if sep_exact(a, b) >= bar else "NOT SUPPORTED"

import lore_experiment_result as L1
import lore2_result as L2
import lore3_result as L3

W = os.path.dirname(os.path.abspath(__file__))
LEGS = ("L1", "L2", "L3")
LEG_NAME = {"L1": "H-1 anomalous-light", "L2": "H-2 Indigenous narrative",
            "L3": "H-3 settler history"}


# ------------------------------------------------------------------ statistics
def sign_test(w, d):
    nz = [(a, b) for a, b in zip(w, d) if a != b]
    k = sum(1 for a, b in nz if a > b)
    n = len(nz)
    if n == 0:
        return {"non_tied": 0, "favour_winner": 0, "p_two_sided": 1.0}
    p = sum(comb(n, i) for i in range(n + 1)
            if abs(i - n / 2) >= abs(k - n / 2)) / 2 ** n
    return {"non_tied": n, "favour_winner": k, "p_two_sided": round(min(1.0, p), 4)}


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5 if sxx and syy else 0.0


def spearman(x, y):
    return round(pearson(ranks(x), ranks(y)), 3)


def weighted_kappa(a, b, kmax=3):
    """Linear-weighted Cohen's kappa on an ordinal 0..kmax scale."""
    n = len(a)
    cats = range(kmax + 1)
    obs = sum(1 - abs(x - y) / kmax for x, y in zip(a, b)) / n
    pa = {c: sum(1 for x in a if x == c) / n for c in cats}
    pb = {c: sum(1 for y in b if y == c) / n for c in cats}
    exp = sum(pa[i] * pb[j] * (1 - abs(i - j) / kmax) for i in cats for j in cats)
    return round((obs - exp) / (1 - exp), 3) if exp < 1 else 1.0


def median_low(xs):
    """Median; on an even split take the LOWER value -- conservative for a
    hypothesis that needs winners to separate upward."""
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else s[n // 2 - 1]


# ---------------------------------------------------------------- pair mapping
PAIRS = [(r[0], r[1], r[4]) for r in L3.ROWS]          # (rank, winner, decoy)
ROLE = {}
for rank, win, dec in PAIRS:
    ROLE[win] = ("winner", rank)
    ROLE[dec] = ("decoy", rank)

SIGHTED = {
    "L1": dict(L1.SCORES.items()),
    "L2": {},
    "L3": {},
}
SIGHTED["L1"] = {k: v[0] for k, v in L1.SCORES.items()}
for r in L2.ROWS:
    SIGHTED["L2"][r[1]] = r[2]
    SIGHTED["L2"][r[4]] = r[5]
for r in L3.ROWS:
    SIGHTED["L3"][r[1]] = r[2]
    SIGHTED["L3"][r[4]] = r[5]


def main():
    packets = json.load(open(os.path.join(W, "blind_packet.json")))
    keymap = json.load(open(os.path.join(W, "blind_keymap.json")))
    scores = json.load(open(os.path.join(W, "blind_scores.json")))

    out = {"protocol": scores["protocol"], "probe_gate": {}, "legs": {},
           "cross_leg": {}, "collection_bias": {}}

    # ---- 1. PROBE GATE, before anything else is looked at ------------------
    surviving = {}
    for leg in LEGS:
        km = keymap[leg]
        probes = {i: km[i] for i in km if km[i]["probe"]}
        gate = {}
        keep = []
        for who, col in scores[leg].items():
            miss = {i: (col[i], probes[i]["sighted"]) for i in probes
                    if abs(col[i] - probes[i]["sighted"]) > 1}
            gate[who] = {"probes": {i: col[i] for i in probes},
                         "expected": {i: probes[i]["sighted"] for i in probes},
                         "VOID": bool(miss)}
            if not miss:
                keep.append(who)
        surviving[leg] = keep
        out["probe_gate"][leg] = {"columns": gate, "surviving": keep}

    # ---- 2. consensus + per-leg readout ------------------------------------
    consensus = {}
    for leg in LEGS:
        km, keep = keymap[leg], surviving[leg]
        cons, per_scorer = {}, {}
        for iid, meta in km.items():
            if meta["probe"]:
                continue
            cons[meta["key"]] = median_low([scores[leg][w][iid] for w in keep])
        consensus[leg] = cons

        names = [(rk, w, d) for rk, w, d in PAIRS]
        Wt = [cons[w] for _, w, _ in names]
        Dt = [cons[d] for _, _, d in names]
        wm, dm = sum(Wt) / len(Wt), sum(Dt) / len(Dt)

        sW = [SIGHTED[leg][w] for _, w, _ in names]
        sD = [SIGHTED[leg][d] for _, _, d in names]
        swm, sdm = sum(sW) / len(sW), sum(sD) / len(sD)

        for who in keep:
            cw = [scores[leg][w] for w in keep]
        for who in scores[leg]:
            col = {km[i]["key"]: scores[leg][who][i] for i in km if not km[i]["probe"]}
            a = [col[w] for _, w, _ in names]
            b = [col[d] for _, _, d in names]
            per_scorer[who] = {
                "winner_mean": round(sum(a) / len(a), 2),
                "decoy_mean": round(sum(b) / len(b), 2),
                "separation": round(float(sep_exact(a, b)), 2),
                "verdict": verdict(a, b),
                "sign_test": sign_test(a, b),
                "kappa_vs_sighted": weighted_kappa(
                    [col[k] for k in SIGHTED[leg]], [SIGHTED[leg][k] for k in SIGHTED[leg]]),
            }

        allk = list(SIGHTED[leg])
        pairsk = [(x, y) for i, x in enumerate(keep) for y in keep[i + 1:]]
        inter = [weighted_kappa(
            [{km[i]["key"]: scores[leg][x][i] for i in km if not km[i]["probe"]}[k] for k in allk],
            [{km[i]["key"]: scores[leg][y][i] for i in km if not km[i]["probe"]}[k] for k in allk])
            for x, y in pairsk]

        out["legs"][leg] = {
            "name": LEG_NAME[leg],
            "SIGHTED": {"winner_mean": round(swm, 2), "decoy_mean": round(sdm, 2),
                        "separation": round(float(sep_exact(sW, sD)), 2),
                        "sign_test": sign_test(sW, sD),
                        "verdict": verdict(sW, sD)},
            "BLIND_consensus": {"winner_mean": round(wm, 2), "decoy_mean": round(dm, 2),
                                "separation": round(float(sep_exact(Wt, Dt)), 2),
                                "sign_test": sign_test(Wt, Dt),
                                "verdict": verdict(Wt, Dt)},
            "separation_shift": round(float(sep_exact(Wt, Dt) - sep_exact(sW, sD)), 2),
            "separation_exact": {"sighted": str(sep_exact(sW, sD)),
                                 "blind": str(sep_exact(Wt, Dt)), "bar": "1"},
            "per_scorer_separation_mean": round(
                sum(per_scorer[w]["separation"] for w in keep) / len(keep), 2),
            "per_scorer_verdict_count_SUPPORTED": sum(
                1 for w in keep if per_scorer[w]["verdict"] == "SUPPORTED"),
            "winner_mean_shift": round(wm - swm, 2),
            "decoy_mean_shift": round(dm - sdm, 2),
            "kappa_blind_vs_sighted": weighted_kappa(
                [consensus[leg][k] for k in allk], [SIGHTED[leg][k] for k in allk]),
            "inter_scorer_kappa": {"pairs": [round(v, 3) for v in inter],
                                   "mean": round(sum(inter) / len(inter), 3)},
            "exact_agreement_blind_vs_sighted": round(
                sum(1 for k in allk if consensus[leg][k] == SIGHTED[leg][k]) / len(allk), 3),
            "per_scorer": per_scorer,
        }

    # ---- 3. cross-leg rho, with NO common scorer ---------------------------
    sites = [w for _, w, _ in PAIRS] + [d for _, _, d in PAIRS]
    for a, b in (("L1", "L2"), ("L1", "L3"), ("L2", "L3")):
        out["cross_leg"][f"{a}x{b}"] = {
            "sighted_rho": spearman([SIGHTED[a][s] for s in sites],
                                    [SIGHTED[b][s] for s in sites]),
            "blind_rho": spearman([consensus[a][s] for s in sites],
                                  [consensus[b][s] for s in sites]),
        }

    # ---- 4. collection-bias gauge (what blinding CANNOT reach) -------------
    for leg in LEGS:
        km = keymap[leg]
        raw = {km[i]["key"]: km[i]["note_raw"] for i in km if not km[i]["probe"]}
        wl = [len(raw[w]) for _, w, _ in PAIRS]
        dl = [len(raw[d]) for _, _, d in PAIRS]
        out["collection_bias"][leg] = {
            "winner_mean_note_chars": round(sum(wl) / len(wl), 1),
            "decoy_mean_note_chars": round(sum(dl) / len(dl), 1),
            "ratio": round((sum(wl) / len(wl)) / (sum(dl) / len(dl)), 3),
            "sign_test_winner_longer": sign_test(wl, dl),
        }

    out["consensus_tiers"] = consensus
    json.dump(out, open(os.path.join(W, "blind_rescore_result.json"), "w"), indent=1)

    # ------------------------------------------------------------- printout
    print("PROBE GATE (pre-declared: >1 tier off either probe => column VOID)")
    for leg in LEGS:
        g = out["probe_gate"][leg]
        for who, v in g["columns"].items():
            print(f"  {leg}-{who}: got {v['probes']} expected {v['expected']}"
                  f"  {'VOID' if v['VOID'] else 'ok'}")
        print(f"  {leg} surviving columns: {g['surviving']}")
    print()
    for leg in LEGS:
        L = out["legs"][leg]
        print(f"== {leg}  {L['name']}")
        print(f"   SIGHTED  W {L['SIGHTED']['winner_mean']}  D {L['SIGHTED']['decoy_mean']}"
              f"  sep {L['SIGHTED']['separation']:+.2f}  {L['SIGHTED']['verdict']}"
              f"  sign p={L['SIGHTED']['sign_test']['p_two_sided']}")
        print(f"   BLIND    W {L['BLIND_consensus']['winner_mean']}  D {L['BLIND_consensus']['decoy_mean']}"
              f"  sep {L['BLIND_consensus']['separation']:+.2f}  {L['BLIND_consensus']['verdict']}"
              f"  sign p={L['BLIND_consensus']['sign_test']['p_two_sided']}")
        print(f"   shift    sep {L['separation_shift']:+.2f}"
              f"   (W {L['winner_mean_shift']:+.2f}, D {L['decoy_mean_shift']:+.2f})")
        print(f"   kappa blind-vs-sighted {L['kappa_blind_vs_sighted']}"
              f"   inter-scorer {L['inter_scorer_kappa']['mean']}"
              f"   exact-agree {L['exact_agreement_blind_vs_sighted']}")
        for who, v in L["per_scorer"].items():
            print(f"     scorer {who}: sep {v['separation']:+.2f}  {v['verdict']}")
        print()
    print("CROSS-LEG rho (blind columns share NO scorer):")
    for k, v in out["cross_leg"].items():
        print(f"   {k}: sighted {v['sighted_rho']:+.3f}   blind {v['blind_rho']:+.3f}")
    print()
    print("COLLECTION BIAS -- note richness by role (blinding cannot reach this):")
    for leg in LEGS:
        c = out["collection_bias"][leg]
        print(f"   {leg}: winner {c['winner_mean_note_chars']} ch vs decoy "
              f"{c['decoy_mean_note_chars']} ch  ratio {c['ratio']}  "
              f"sign p={c['sign_test_winner_longer']['p_two_sided']}")
    print("\n[wrote] blind_rescore_result.json")


if __name__ == "__main__":
    main()
