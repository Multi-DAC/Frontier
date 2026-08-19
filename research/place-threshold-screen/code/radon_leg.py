"""A15 -- THE RADIOGENIC / RADON TERM. Pre-registered before the first sample was drawn.

Clayton, Day 199: "Let's do the water leg and the radon/uranium leg as well."

A13 named this leg as deliberately ABSENT and said why: radiogenic ionisation "wants the
NURE radiometric grid, not a lithology string." This is that grid. `code/radiometric_grid.py`
holds the acquisition and the three wrong turns it survived; read its docstring before
trusting a number here.

THE MECHANISM, stated so the bars can be aimed at it rather than at "uranium is interesting".

  U-238 -> ... -> Ra-226 -> Rn-222, a chemically inert gas with a 3.8 day half-life. Inert
  means it is not held by the mineral that bred it; 3.8 days means it can travel if there is
  a path. Fault damage zones are the path, and carrier gases (CO2, CH4) are the pump. Each
  Rn-222 decay deposits ~5.5 MeV in air and liberates of order 1e5 ion pairs.

  THE CLAIM THIS LEG CAN SUPPORT: ionised air has a lower electrical breakdown threshold and
  a raised conductivity, so a volume of radon-charged air near the ground is a place where a
  given field does more. That is a PRECONDITION argument, and it is a different and more
  modest claim than "radon makes lights". It also composes with A13: A13's positive holes are
  a charge SOURCE, this is the MEDIUM that source discharges into, and neither is evidence
  for the other.

  AND THE SECOND, SEPARATE CHANNEL, named because it bears on the reports rather than the
  optics: radon is a documented neurotoxicant and its decay products are alpha emitters
  retained in the lung. Any "place where people feel strange" hypothesis has a boring
  candidate mechanism available, and a screen that finds high-radon ground has found
  somewhere the ordinary explanation is STRONGER, not weaker. This leg is therefore as
  capable of deflating the project's subject as of supporting it, which is why it is worth
  running.

eTh IS THE CONTROL AND IT IS THE WHOLE DESIGN. Th-232's gaseous daughter is Rn-220 (thoron),
half-life 55 s -- a diffusion length of centimetres against radon's metres-to-tens-of-metres.
eU and eTh are strongly correlated across rock types, both being concentrated in felsic and
alkaline rock. So:

    HIGH eU AND HIGH eTh   -> felsic/alkaline LITHOLOGY. A13 already scores lithology. This
                              leg would be relabelling A13's term and must say so.
    HIGH eU, RELATIVE eTh  -> uranium decoupled from its rock-forming twin: mobilised by
                              groundwater and re-deposited, or radon actively accumulating.
                              This is the radon-SPECIFIC signal and the only one that is new.

The ratio is the measurement. Raw eU is a rock-type map wearing a radon label, and reporting
raw eU as "the radon term" would be this project's own signature defect committed on purpose.

AND IT IS THE JOINT TERM CLAYTON POINTED AT. Uranium is mobile as the uranyl ion in oxidising
water and immobile when reduced; a high eU/eTh anomaly is, mechanistically, a record of WATER
having moved uranium. A15 and A14 are therefore not two independent legs bolted on -- the
ratio is where the water leg and the radiogenic leg touch, and `radon_leg.py` and
`water_leg.py` share point populations so the two can be crossed later.

THE CONFOUND THAT COULD MANUFACTURE THE ENTIRE RESULT, and is measured rather than argued
away. The grid is 27.7% populated: 2,716,128 valid cells of 9,812,054. The holes are not
random. This compilation is largely NURE-era flying, and NURE FLEW WHERE URANIUM WAS BEING
PROSPECTED. So coverage itself is correlated with uranium prospectivity, and if the screen's
survivors are more likely to be COVERED than random ground, a naive comparison of measured
values would report a fact about 1970s exploration budgets as a fact about geology.
COVERAGE RATE IS THEREFORE ITS OWN REPORTED OUTCOME (BAR 0), tested before any value is
compared, and every value statistic is computed only on the measured subset with the
unmeasured count printed beside it.

THREE POPULATIONS, because two would not separate the two things that could be true.

  SURVIVORS   the 225 that passed the L1 gate; the screen's own output.
  NULL-RANDOM 400 points, SAME SEED and SAME bbox derivation as A8 and A12, so the three
              legs are computed on identical ground and their retentions can be compared.
              Answers: is this ground special versus the western US at large?
  NULL-FAULT  points drawn from the 1,157 faults that FAILED the L1 gate (REBUILT D200; this
              said "stage-2 nodes" and the code built a 27.5% regionally-concentrated subset
              of the true failures -- see water_leg.py's construction note). Answers the
              question NULL-RANDOM cannot: is this special versus OTHER MAPPED QUATERNARY
              FAULTS? Without it, any positive result is confounded with "faults are mapped
              in mountains and mountains are crystalline", and the leg would be measuring
              the fault catalogue rather than the screen.

DECLARED BEFORE THE FIRST SAMPLE -- and the first line is a PREDICTION, so it can be wrong:

  PREDICTION. Survivors will show a modest eU elevation over NULL-RANDOM, driven almost
  entirely by lithology (they sit on crystalline uplifts and random western ground includes
  basin fill), and will show NO elevation over NULL-FAULT, and NO eU/eTh ratio anomaly
  against either. I expect this leg to come back NEGATIVE on the only bar that is new
  information. Writing it here so a null cannot later be dressed as a discovery, and so a
  positive cannot be dressed as expected.

  BAR 0   COVERAGE HONEST if survivor coverage rate and NULL-RANDOM coverage rate differ by
          < 15 percentage points. If they differ by more, the value comparisons are reported
          as CONFOUNDED BY SURVEY SELECTION and no bar below may be called passed.
  BAR i   ELEVATED if survivor median eU exceeds NULL-RANDOM median eU with permutation
          p < 0.05 (two-sided, 10,000 relabellings of the difference in medians).
  BAR ii  RADON-SPECIFIC if survivor median eU/eTh exceeds NULL-RANDOM at p < 0.05. If
          BAR i passes and BAR ii fails, the leg has measured FELSIC ROCK, the finding
          belongs to A13, and this leg reports itself as redundant.
  BAR iii NOT-JUST-FAULTS if the eU/eTh contrast also holds against NULL-FAULT at p < 0.05.
          This is the bar that decides whether the SCREEN selected anything, as opposed to
          the fault catalogue having selected it.
  BAR iv  INDEPENDENT of the incumbent if |Spearman rho| between eU/eTh and the screen score
          across survivors is < 0.7. At >= 0.7 it is a relabelling of an existing term.

  ! NONE OF THESE BARS TESTS WHETHER RADON PRODUCES A LIGHT, A PORTAL, OR AN ANOMALY. They
    test whether a radiogenic term picks out different ground from the incumbent screen. A6
    already measured the founding gate against independently reported anomalous-light
    locales -- 0 of 6 passed against 34.4% of random western ground -- and nothing here
    improves that. The deliverable's header says so and this leg does not change it.
"""
import json, math, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import radiometric_grid as RG                                          # noqa: E402

OUT = "data/radon_leg.json"
SEED = 20260818            # same seed as A8/A12 -- shared draw, not shared verdict
N_NULL = 400
N_PERM = 10000
NEIGH_CELLS = 2            # +/-2 cells of 2 km = an 10x10 km window, radon's transport scale


def neighbourhood(elem, lat, lon, k=NEIGH_CELLS):
    """Mean of the (2k+1)^2 cells centred on the point, over the finite ones only.

    Radon migrates; a single 2 km cell is a smaller footprint than the process. Returns
    (mean, n_valid) and None when the whole window is unmeasured -- never 0.0.
    """
    import numpy as np
    arr, h = RG.load(elem)
    p = RG.to_dnag(lat, lon)
    if p is None:
        return None, 0
    c0 = int((p[0] - h["xllcorner"]) / h["cellsize"])
    r0 = int(h["nrows"] - 1 - (p[1] - h["yllcorner"]) / h["cellsize"])
    r1, r2 = max(0, r0 - k), min(int(h["nrows"]), r0 + k + 1)
    c1, c2 = max(0, c0 - k), min(int(h["ncols"]), c0 + k + 1)
    if r1 >= r2 or c1 >= c2:
        return None, 0
    w = arr[r1:r2, c1:c2]
    fin = np.isfinite(w)
    n = int(fin.sum())
    return (float(w[fin].mean()) if n else None), n


def probe(lat, lon):
    u, tu = RG.sample("U", lat, lon), RG.sample("Th", lat, lon)
    ku = RG.sample("K", lat, lon)
    un, unn = neighbourhood("U", lat, lon)
    tn, tnn = neighbourhood("Th", lat, lon)
    ratio = (u / tu) if (u is not None and tu not in (None, 0)) else None
    ratio_n = (un / tn) if (un is not None and tn not in (None, 0)) else None
    return dict(eU=u, eTh=tu, eK=ku, eU_10km=un, eTh_10km=tn,
                n_cells_U=unn, n_cells_Th=tnn,
                ratio=(round(ratio, 4) if ratio is not None else None),
                ratio_10km=(round(ratio_n, 4) if ratio_n is not None else None),
                covered=(u is not None))


def median(v):
    s = sorted(v)
    n = len(s)
    if not n:
        return None
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def perm_test(a, b, n_perm=N_PERM, seed=SEED):
    """Two-sided permutation test on the difference of medians. Assumption-free, and the
    right choice here because eU is strongly right-skewed and a t-test on it would be
    testing a normality claim nobody has made."""
    a, b = list(a), list(b)
    if len(a) < 5 or len(b) < 5:
        return None, None, "insufficient n"
    obs = median(a) - median(b)
    pool = a + b
    na = len(a)
    rnd = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        rnd.shuffle(pool)
        d = median(pool[:na]) - median(pool[na:])
        if abs(d) >= abs(obs) - 1e-12:
            hits += 1
    return round(obs, 4), round((hits + 1) / (n_perm + 1), 4), None


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    if len(xs) < 3:
        return None
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((p - mx) * (q - my) for p, q in zip(rx, ry))
    dx = math.sqrt(sum((p - mx) ** 2 for p in rx))
    dy = math.sqrt(sum((q - my) ** 2 for q in ry))
    return round(num / (dx * dy), 4) if dx and dy else None


if __name__ == "__main__":
    if not RG.self_test():
        sys.exit("[A15] ABORT: radiometric_grid self-test failed; georeferencing unproven")

    surv = json.load(open("data/stage5_join_summary.json"))["survivors_ranked"]
    stage2 = json.load(open("data/transport_screen_stage2.json"))["all"]

    print(f"[A15] survivors={len(surv)}", file=sys.stderr)
    rows = []
    for s in surv:
        rows.append(dict(fault=s["fault_name"], lat=s["lat"], lon=s["lon"],
                         rank=s.get("rank"), score=s.get("score"), **probe(s["lat"], s["lon"])))

    lats = [s["lat"] for s in surv]
    lons = [s["lon"] for s in surv]
    bbox = (min(lats), max(lats), min(lons), max(lons))
    rnd = random.Random(SEED)
    null_r = []
    for _ in range(N_NULL):
        la = rnd.uniform(bbox[0], bbox[1])
        lo = rnd.uniform(bbox[2], bbox[3])
        null_r.append(dict(lat=round(la, 4), lon=round(lo, 4), **probe(la, lo)))
    print(f"[A15] null-random={len(null_r)} in bbox {tuple(round(b,2) for b in bbox)}",
          file=sys.stderr)

    # NULL-FAULT: the gate's ACTUAL 1,157 L1 failures. Drawn with an independent stream so
    # the random-ground draw above is bit-for-bit identical to A8's and A12's.
    # REBUILT D200 -- was `stage2 minus survivor names`, a 392-fault regional draw that
    # yielded a 27.5% geographically-concentrated subset of the true failures (and 3 faults
    # that had actually PASSED). See water_leg.py's construction note.
    true_ctrl = json.load(open("data/null_fault_true.json"))
    surv_names = {" ".join(s["fault_name"].split()) for s in surv}
    pool, seen = [], set()
    for n in true_ctrl["rows"]:
        nm = " ".join((n.get("fault_name") or "").split())
        if not nm or nm in surv_names or nm in seen:
            continue
        if n.get("lat") is None or n.get("lon") is None:
            continue
        seen.add(nm)
        pool.append(n)
    assert len(pool) >= 1000, f"[A15] NULL-FAULT pool collapsed to {len(pool)}; expected ~1157"
    rnd2 = random.Random(SEED + 1)
    rnd2.shuffle(pool)
    null_f = [dict(fault=n["fault_name"], lat=n["lat"], lon=n["lon"],
                   **probe(n["lat"], n["lon"])) for n in pool[:N_NULL]]
    print(f"[A15] null-fault={len(null_f)} of {len(pool)} true L1-failed faults",
          file=sys.stderr)

    def cov(rs):
        return round(sum(1 for r in rs if r["covered"]) / len(rs), 4) if rs else None

    def vals(rs, key):
        return [r[key] for r in rs if r.get(key) is not None]

    c_s, c_r, c_f = cov(rows), cov(null_r), cov(null_f)
    bar0 = (c_s is not None and c_r is not None and abs(c_s - c_r) < 0.15)

    res = {}
    for key in ("eU", "ratio", "eU_10km", "ratio_10km", "eTh"):
        d_r, p_r, e_r = perm_test(vals(rows, key), vals(null_r, key))
        d_f, p_f, e_f = perm_test(vals(rows, key), vals(null_f, key))
        res[key] = dict(
            surv_median=(round(median(vals(rows, key)), 4) if vals(rows, key) else None),
            null_random_median=(round(median(vals(null_r, key)), 4) if vals(null_r, key) else None),
            null_fault_median=(round(median(vals(null_f, key)), 4) if vals(null_f, key) else None),
            n_surv=len(vals(rows, key)), n_null_random=len(vals(null_r, key)),
            n_null_fault=len(vals(null_f, key)),
            vs_random=dict(diff=d_r, p=p_r, note=e_r),
            vs_fault=dict(diff=d_f, p=p_f, note=e_f))

    paired = [(r["score"], r["ratio"]) for r in rows
              if r.get("score") is not None and r.get("ratio") is not None]
    rho = spearman([p[0] for p in paired], [p[1] for p in paired]) if paired else None

    bars = dict(
        bar0_coverage_honest=bar0,
        bar_i_elevated=(res["eU"]["vs_random"]["p"] is not None
                        and res["eU"]["vs_random"]["p"] < 0.05
                        and (res["eU"]["vs_random"]["diff"] or 0) > 0),
        bar_ii_radon_specific=(res["ratio"]["vs_random"]["p"] is not None
                               and res["ratio"]["vs_random"]["p"] < 0.05
                               and (res["ratio"]["vs_random"]["diff"] or 0) > 0),
        bar_iii_not_just_faults=(res["ratio"]["vs_fault"]["p"] is not None
                                 and res["ratio"]["vs_fault"]["p"] < 0.05
                                 and (res["ratio"]["vs_fault"]["diff"] or 0) > 0),
        bar_iv_independent=(rho is not None and abs(rho) < 0.7))

    top = sorted([r for r in rows if r.get("ratio_10km") is not None],
                 key=lambda r: -r["ratio_10km"])[:15]

    out = dict(
        leg="A15 radiogenic / radon term",
        frozen="Day 199, 2026-08-18; mechanism, populations, prediction and bars declared in "
               "radon_leg.py docstring before the first sample",
        source="USGS OFR 2005-1413 aeroradiometric grids, 2 km, DNAG spherical TM; "
               "acquisition and its three failure modes in radiometric_grid.py",
        seed=SEED, n_perm=N_PERM, neighbourhood_km=(2 * NEIGH_CELLS + 1) * 2,
        coverage=dict(survivors=c_s, null_random=c_r, null_fault=c_f,
                      confound="NURE-era flying followed uranium prospecting; a coverage "
                               "difference is a fact about exploration history, not geology"),
        statistics=res, spearman_ratio_vs_score=rho, bars=bars,
        top15_by_eU_eTh_10km=[dict(fault=r["fault"], ratio_10km=r["ratio_10km"],
                                   eU_10km=(round(r["eU_10km"], 3) if r["eU_10km"] else None),
                                   eTh_10km=(round(r["eTh_10km"], 3) if r["eTh_10km"] else None),
                                   rank=r.get("rank")) for r in top],
        survivors=rows, null_random=null_r, null_fault=null_f)
    json.dump(out, open(OUT, "w"), indent=1)

    print(f"[A15] coverage surv={c_s} null_rand={c_r} null_fault={c_f}", file=sys.stderr)
    for k in ("eU", "ratio"):
        r = res[k]
        print(f"[A15] {k:6s} surv={r['surv_median']} rand={r['null_random_median']} "
              f"fault={r['null_fault_median']} | p_rand={r['vs_random']['p']} "
              f"p_fault={r['vs_fault']['p']}", file=sys.stderr)
    print(f"[A15] rho(ratio,score)={rho}  bars={bars}", file=sys.stderr)
    print(f"[A15] wrote {OUT}", file=sys.stderr)
