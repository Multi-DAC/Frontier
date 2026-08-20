"""A16c-CAL -- IS BAR iv's TEST CALIBRATED, OR DOES IT FIRE ON A MARGINAL SHIFT?

Bar iv came out PASS at p=0.0086 under A16b's control-set deviation. Written BEFORE looking
at whether that survives, because this is the check that decides whether it means anything.

THE SUSPICION, stated so it can be wrong.

The frozen construction is:
    x_raw = rank_norm(charge_score) * rank_norm(omega_resid)          [ranks over surv+nfault]
    residualise(x_raw, controls=[x_marg_c, x_marg_o])   -> y = log10(x_raw), LINEAR in ranks
    permute the residual, survivors vs null-fault

log10(a*b) = log10(a) + log10(b). The model regresses that on a and b UNLOGGED. So the
residual is a strongly non-linear, deterministic function of the two marginals -- it is not
a clean interaction term. And the marginals are NOT balanced between arms: median charge
score 0.5625 on survivors against 0.0938 on the fault control, p = 0.0. If a curved residual
is evaluated at systematically different marginal values in the two arms, a difference in
that residual appears WITH NO INTERACTION PRESENT. That would make bar iv's pass a restatement
of the marginal charge contrast in a shape that looks like new information.

THE CONTROL, and it corrupts exactly one thing.

Within each arm independently, permute charge_score across that arm's points. This preserves
each arm's charge distribution EXACTLY -- the marginal shift between arms survives untouched,
the coverage pattern survives, the omega values survive -- and destroys only the pairing
between a fault's charge and its own flow residual. Under this shuffle the true interaction
is zero BY CONSTRUCTION. Everything downstream is then run unedited.

READING IT:
  false-positive rate ~5%  -> the test is calibrated; bar iv's p=0.0086 is a real contrast.
  materially above 5%      -> the statistic reports marginal shift as interaction, and bar iv
                              must be reported UNRUN-BY-CONSTRUCTION rather than PASS.
This is a two-sided instrument: it can clear bar iv or kill it, and I do not know which.

Run: python code/a16c_bar_iv_calibration.py [n_iter] [n_perm]
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

from current_leg import SEED, perm_test, residualise, rank_norm  # noqa: E402

SRC = os.path.join(DATA, "current_leg.json")
OUT = os.path.join(DATA, "current_leg_a16c_calibration.json")
CTRL = ["area_max_km2", "relief_m"]


def bar_iv_p(surv, nfault, nrand, n_perm):
    """Bar iv exactly as frozen, returning its p. Points are mutated; pass copies."""
    residualise(surv + nfault + nrand, "omega_max_wpm", CTRL)
    both = surv + nfault
    rc = rank_norm([p.get("charge_score") for p in both])
    ro = rank_norm([p.get("omega_max_wpm_resid") for p in both])
    for p, a, b in zip(both, rc, ro):
        p["x_marg_c"], p["x_marg_o"] = a, b
        p["x_raw"] = None if (a is None or b is None) else a * b
    residualise([p for p in both if p.get("x_raw")], "x_raw",
                ["x_marg_c", "x_marg_o"])
    t = perm_test([p.get("x_raw_resid") for p in surv],
                  [p.get("x_raw_resid") for p in nfault], n_perm=n_perm)
    return t.get("p"), t


def main():
    n_iter = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    n_perm = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

    src = json.load(open(SRC, encoding="utf-8"))
    surv0, nf0, nr0 = src["survivors"], src["null_fault"], src["null_random"]

    def fresh():
        return (json.loads(json.dumps(surv0)), json.loads(json.dumps(nf0)),
                json.loads(json.dumps(nr0)))

    # OBSERVED, re-run here at the calibration's own n_perm so the comparison is like-for-like.
    s, f, r = fresh()
    p_obs, t_obs = bar_iv_p(s, f, r, n_perm)
    print(f"observed bar iv p = {p_obs}  (n_perm={n_perm})  {t_obs}", flush=True)

    rng = random.Random(SEED + 99)
    ps, fired, t0 = [], 0, time.time()
    for i in range(n_iter):
        s, f, r = fresh()
        for arm in (s, f):                       # shuffle WITHIN arm -> marginal preserved
            vals = [p.get("charge_score") for p in arm]
            rng.shuffle(vals)
            for p, v in zip(arm, vals):
                p["charge_score"] = v
        p_null, _ = bar_iv_p(s, f, r, n_perm)
        if p_null is not None:
            ps.append(p_null)
            fired += (p_null < 0.05)
        if (i + 1) % 20 == 0:
            el = time.time() - t0
            print(f"  {i+1}/{n_iter}  fired {fired}  "
                  f"({fired/max(len(ps),1):.1%})  {el:.0f}s "
                  f"eta {el/(i+1)*(n_iter-i-1):.0f}s", flush=True)

    ps.sort()
    rate = fired / len(ps) if ps else None
    # where does the OBSERVED p sit against the null distribution of p's?
    beat = sum(1 for x in ps if x <= p_obs) if p_obs is not None else None
    res = {
        "leg": "A16c calibration -- within-arm charge shuffle, interaction zero by construction",
        "n_iter": n_iter, "n_perm": n_perm, "n_usable": len(ps),
        "observed_p": p_obs,
        "false_positive_rate_at_0.05": rate,
        "null_p_quantiles": {q: (ps[int(q * (len(ps) - 1))] if ps else None)
                             for q in (0.01, 0.05, 0.10, 0.25, 0.50)},
        "null_runs_at_or_below_observed_p": beat,
        "empirical_p_of_observed": ((beat + 1) / (len(ps) + 1)) if beat is not None else None,
        "seed": SEED + 99,
    }
    json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
