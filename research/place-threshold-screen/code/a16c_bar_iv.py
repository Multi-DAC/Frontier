"""A16c -- BAR iv, RUN. Offline refit; no network, no new fetch.

WHY THIS EXISTS, stated before the result so it cannot be written to fit it.

REPORT.md sec.9 says bar iv "remains UNRUN ... the A13 charge population is stage-2 rather
than the gate survivors, a population mismatch ... priced at a ~1,003-fault rebuild."
That sentence is STALE and contradicts sec.9's own line 47 rows earlier, which reports the
coverage guards PASSING at 92.0% / 92.8%. The rebuild it prices was done on Day 200 at
14:53 (data/charge_term.json, 1,405-fault roster) BEFORE A16 ran at 19:26. Neither guard
fired: asymmetry 1.01x against a 2.0x trip, floor 92% against a 50% trip. current_leg.py
took the ELSE branch and bar iv RAN.

It ran and produced nothing, for a different reason, and the data file says so:

    interaction: {"n": 0, "beta": null, "test": {"n_a": 0, "n_b": 0, "p": null,
                  "note": "insufficient n"}}
    bars: {"bar_iv_interacts": false, "bar_iv_status": "FAIL"}

The interaction is built on `omega_max_wpm_resid` (current_leg.py:565). That field is
written by residualise() against the PRE-REGISTERED control set [log10(area), petma,
relief]. petma is served as literal 0 on all 24,264,177 NHDPlus HR reaches, _pos() correctly
rejects 0 as NODATA, so the residual was None on 1,025/1,025 rows -- the identical defect
A16b already diagnosed and repaired for the stream-power contrast. A16b refit the CONTRAST
on the two controls that exist and stopped one step short of bar iv, which is the only other
consumer of the field it rebuilt.

SO THIS IS NOT A NEW DEVIATION. It is A16b's already-declared deviation propagated to the
one place it did not reach. One thing changes: the control set. Everything else -- the
frozen interaction construction (rank-normalise both marginals over surv+nfault, take the
product, partial the marginals back out, permute the residual), SEED, N_PERM, two-tailed --
is imported from current_leg.py and runs unedited. Reimplementing the statistic would make
this a different test wearing bar iv's name.

TWO DEFECTS IN THE FROZEN CODE ARE REPRODUCED RATHER THAN FIXED, and named here so the
reader does not have to find them:
  1. residualise([p for p in both if p.get("x_raw")], ...) filters on TRUTHINESS, so a point
     whose product is exactly 0.0 is dropped. rank_norm() maps to [0,1] inclusive, so the
     minimum-ranked point in each marginal is exactly 0 -- a handful of points fall out for
     a reason that has nothing to do with their data. Reproduced, counted, and printed below.
  2. bar_iv_status maps a p of None to "FAIL", not "UNRUN" (current_leg.py:602 reads
     `bar_iv is None`, but bar_iv was set to False by the comparison, not left None). An
     untestable statistic rendered as a failed test is the exact shape this project spent
     Day 200 catching. Fixing the mapping is a code change to a frozen file and is filed,
     not done here.

Run: python code/a16c_bar_iv.py   ->  data/current_leg_a16c.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

from current_leg import (SEED, N_PERM, perm_test, residualise,  # noqa: E402
                         rank_norm, median)

SRC = os.path.join(DATA, "current_leg.json")
OUT = os.path.join(DATA, "current_leg_a16c.json")

CTRL_PREREG = ["area_max_km2", "pet_mean", "relief_m"]
CTRL_DEVIATION = ["area_max_km2", "relief_m"]          # A16b's declared deviation


def interaction(surv, nfault, ctrl_keys, pooled):
    """Bar iv exactly as current_leg.py:556-574 builds it, over a given control set."""
    n_res, beta_res = residualise(pooled, "omega_max_wpm", ctrl_keys)
    both = surv + nfault
    rc = rank_norm([p.get("charge_score") for p in both])
    ro = rank_norm([p.get("omega_max_wpm_resid") for p in both])
    for p, a, b in zip(both, rc, ro):
        p["x_marg_c"], p["x_marg_o"] = a, b
        p["x_raw"] = None if (a is None or b is None) else a * b
    truthy = [p for p in both if p.get("x_raw")]
    both_nonnull = [p for p in both if p.get("x_raw") is not None]
    n_x, beta_x = residualise(truthy, "x_raw", ["x_marg_c", "x_marg_o"])
    test = perm_test([p.get("x_raw_resid") for p in surv],
                     [p.get("x_raw_resid") for p in nfault])
    marg = perm_test([p.get("charge_score") for p in surv],
                     [p.get("charge_score") for p in nfault])
    return {
        "controls": ["log10(area_max_km2)"] + ctrl_keys[1:],
        "omega_residual_n": n_res,
        "omega_residual_beta": beta_res,
        "interaction_fit_n": n_x,
        "interaction_beta": beta_x,
        "dropped_by_truthiness_filter": len(both_nonnull) - len(truthy),
        "test": test,
        "marginal_charge": marg,
        "bar_iv_passes": (test.get("p") is not None and test["p"] < 0.05),
        "bar_iv_status": ("UNRUN -- statistic not computable"
                          if test.get("p") is None else
                          ("PASS" if test["p"] < 0.05 else "FAIL")),
    }


def main():
    src = json.load(open(SRC, encoding="utf-8"))
    surv, nfault, nrand = src["survivors"], src["null_fault"], src["null_random"]
    pooled = surv + nfault + nrand
    cov = src["charge_join_coverage"]

    print(f"loaded {len(surv)} survivors / {len(nfault)} null-fault / "
          f"{len(nrand)} null-random from {os.path.basename(SRC)}")
    print(f"charge coverage as run: {cov}")
    print(f"pet_mean non-null anywhere: "
          f"{sum(1 for p in pooled if p.get('pet_mean') is not None)}/{len(pooled)}")

    out = {}
    for label, ctrl in (("preregistered_3_control", CTRL_PREREG),
                        ("deviation_2_control", CTRL_DEVIATION)):
        # fresh copies: residualise() writes onto the points, and the two fits must not
        # inherit each other's residuals. A stale _resid surviving into the second fit
        # would silently make this a comparison of one model with itself.
        s = json.loads(json.dumps(surv))
        f = json.loads(json.dumps(nfault))
        r = json.loads(json.dumps(nrand))
        res = interaction(s, f, ctrl, s + f + r)
        out[label] = res
        print(f"\n-- {label} --")
        print(f"   omega residual fitted on n={res['omega_residual_n']}")
        print(f"   interaction fitted on n={res['interaction_fit_n']}, "
              f"beta={res['interaction_beta']}")
        print(f"   dropped by the x_raw truthiness filter: "
              f"{res['dropped_by_truthiness_filter']}")
        print(f"   BAR iv -> {res['bar_iv_status']}   test={res['test']}")
        print(f"   marginal charge: {res['marginal_charge']}")

    out["leg"] = "A16c -- bar iv run under A16b's declared control-set deviation"
    out["source"] = {"path": SRC, "bytes": os.path.getsize(SRC),
                     "charge_join_coverage": cov}
    out["seed"] = SEED
    out["n_perm"] = N_PERM
    out["two_tailed"] = True
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
