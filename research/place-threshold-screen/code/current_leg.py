"""A16 -- THE CURRENT TERM AND THE WATER x CHARGE INTERACTION. Pre-registered before query.

Clayton, Day 200: "You were looking at springs, but I'm wondering if rushing water, like
rivers or anything with a current, alongside the electromagnetically active minerals, would
be worth looking at. Hydroelectricity, as it were."

He is naming two things A14 did not measure, and he is right about both.

  1. A14 measured WHERE WATER IS (spring count W1, perennial presence W3) and THE HEAD THAT
     COULD DRIVE IT (relief W2). It never measured HOW MUCH IS MOVING or HOW FAST. Presence
     is not flux. The coupling coefficient C = eps*zeta/(eta*sigma) is a CONVERSION
     EFFICIENCY; the potential is dV = C * dp, and A14 shipped without the dp term.
  2. NO LEG IN THIS PROJECT HAS CROSSED WATER WITH LITHOLOGY. Every score to date is
     ADDITIVE. "Both combined" is an INTERACTION, and an interaction is not implied by two
     marginals -- two terms can each be null and their product carry signal, and two terms
     can each be strong and their product be nothing. It has never been tested here.

THE MECHANISM, and its sign problem, declared first because declaring sigma's sign first is
the only thing A14 did that survived.

  The catchment-scale observable for hydraulic energy actually being dissipated is STREAM
  POWER, Omega = rho * g * Q * S  (W/m), Q discharge, S channel slope.

  ! I DO NOT KNOW THE SIGN, AND SAY SO BEFORE THE QUERY. A river is a DRAIN, not a driver --
    it is the discharge boundary of the flow system, not its engine. High surface discharge
    can mean (a) high total subsurface throughput, so more streaming current [POSITIVE], or
    (b) flow short-circuited down the channel, never traversing the rock mass [NEGATIVE].
    Which dominates is a real open question and I cannot resolve it from a map. THE TEST IS
    THEREFORE TWO-TAILED. A one-tailed test here would be exactly the A14 salinity error
    with the sign reversed: a confident ranked list built on a guessed direction.

THE TWO CONFOUNDS, both in the term BY CONSTRUCTION, both priced before the first query.

  RELIEF. Omega contains S, which is channel gradient, which is relief -- the nuisance
    variable A8, A12 and A14 have now all converged on. A14's failure was structural: its
    headline table was UNSTRATIFIED and the relief stratification came afterwards, so the
    project read a p=0.0001 before it read the Simpson's paradox underneath it. HERE THE
    STRATIFIED TABLE IS THE HEADLINE. The pooled number is printed BELOW it and labelled
    CONFOUNDED. Bar iii is the bar A14 would have failed had it been asked in advance.

  CLIMATE, and it is the WORSE one, visible in the first two probe points. Madison fault
    (MT, near Yellowstone) returns max qema 1339 cfs; La Jencia (NM) returns 4.0 cfs. Those
    two numbers differ mostly because of how much rain falls, not because of anything the
    screen selected. Discharge is a PRECIPITATION VARIABLE wearing a hydrology label.
    NULL-FAULT controls it only partially (both populations are western faults, drawn from
    overlapping ground). The correction is available in the same query and costs no extra
    call: NHDPlus HR EROM carries `petma` (mean annual potential evapotranspiration) and
    `totdasqkm` (total drainage area) per flowline. THE PRIMARY STATISTIC IS THEREFORE A
    RESIDUAL, not a raw value:

        log10(Omega) ~ b0 + b1*log10(totdasqkm) + b2*petma + b3*relief_m     [pooled OLS]

    fitted across the POOLED population (survivors + both nulls together, so the fit cannot
    know which group a point is in), and the survivor-vs-NULL-FAULT test is run on the
    RESIDUAL. Size, climate and terrain are removed before the question is asked.

THE TERMS SCORED, each because it sits in the numerator or in the flow rate:

  C1 DISCHARGE      max qema over network flowlines within 10 km (cfs). Volume moving.
                    Most climate-loaded; reported, residualised, never ranked raw.
  C2 VELOCITY       max vema (fps). Literally "rushing". THE LEAST CLIMATE-LOADED TERM --
                    velocity is set by gradient and channel geometry, and a small steep
                    creek and a large slow river can carry the same Q at different v. This
                    is the closest thing in the data to what Clayton actually described.
  C3 STREAM POWER   max over reaches of rho*g*Q*S, from qema x slope. The physics quantity.
  X  INTERACTION    rank(C3) x rank(charge_score), tested AFTER both marginals are partialled
                    out. charge_score from A13 (data/charge_term.json), per fault.

THE BARS. Declared, with the failure condition spelled out, before any point is scored.

  BAR i    LEAKS         C2 survivors vs NULL-RANDOM, permutation p < 0.05 TWO-TAILED.
                         Expected to pass. Means little -- faults are in mountains and
                         mountains have steep creeks.
  BAR ii   DISCRIMINATES C2 survivors vs NULL-FAULT, p < 0.05 two-tailed. The bar that
                         carries information.
  BAR iii  SURVIVES      bar ii holds in >= 3 of 4 RELIEF QUARTILES with CONSISTENT SIGN.
                         THIS IS THE BAR A14 FAILED AFTER THE FACT. A term that only works
                         pooled is measuring terrain.
  BAR iv   INTERACTS     the residualised product term X discriminates survivors from
                         NULL-FAULT at p < 0.05 AFTER both marginals are partialled out.
                         Clayton's "both combined", asked so it can answer no.
  BAR v    NOT RELABEL   separates the 23-member A7 contender band better than a random
                         relabelling of its OWN values, p < 0.05, 20,000 draws. The exact
                         test A14 flunked at the 54th percentile. Without this the leg is a
                         LABEL and may not move one name on the list (A7's standing rule).

PREDICTION, written here so it can be wrong, and it is a pessimistic one:

  I expect BAR ii to PASS on raw C2 and to FAIL on the residual, because velocity tracks
  gradient and gradient is relief. I expect BAR iii to FAIL. I expect BAR iv -- the
  interaction -- to be the only bar with a real chance of carrying new information, and I
  put it BELOW 50%. If all five pass, the finding is that the screen selects high-stream-
  power fault segments in electromagnetically active rock, and it would be the first term
  in this project that is not terrain wearing a different name.

  ! A16 IS FORBIDDEN FROM REORDERING THE LIST UNLESS BARS ii, iii AND v ALL PASS. Written
    before the result exists, because A14 proved I will read a 2.5x as a finding if the
    guard is a sentence in a note instead of a condition in the code.

FROZEN: populations, seed and radii are inherited UNCHANGED from A14 (data/water_leg.json)
-- same 225 survivors, the SAME NULL-FAULT A14 used, same 400 NULL-RANDOM, same seed
20260818. This leg draws no new points, so it cannot be accused of choosing ground that
suits it.

  ! CORRECTED D200 / 2026-08-19. This line read "same 326 NULL-FAULT". That 326 was the
    OLD control, built by name-subtraction from a stage-2 draw and shown in A16's pre-flight
    to be a 27.5% regionally-concentrated subset of the gate's true 1,157 failures. A14 was
    rebuilt on the true roster the same day, so the inherited NULL-FAULT is now a 400-draw
    from 1,157. The count is deliberately NOT restated here: this docstring is narration and
    would rot again. data/water_leg.json is the state.

  ! BAR iv IS CONDITIONAL, and that is declared here rather than discovered at runtime.
    A13's charge term is computed over stage-2 (charge_term.py:89 says so in capitals), not
    over the gate survivors, so it covers 65/225 of them. Bar iv emits UNRUN with its reason
    when either the coverage floor or the coverage-asymmetry guard fires. Bars i/ii/iii/v and
    may_reorder_list do not read the charge term and are unaffected. See
    work/a17_charge_coverage_frame.md for the measurement and the priced repair.
"""
import json
import math
import os
import random
import sys
import time
import urllib.parse
import urllib.request

try:
    import truststore
    truststore.inject_into_ssl()
except Exception as e:                                    # noqa: BLE001
    print(f"[warn] truststore: {e}", file=sys.stderr)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = "data/current_leg.json"
CACHE = "work/current_cache.json"
WATER = "data/water_leg.json"
CHARGE = "data/charge_term.json"

SEED = 20260818                      # inherited from A14, deliberately not re-rolled
N_PERM = 20000
FLOW_KM = 10.0                       # same radius as A14's W3 perennial term
RHO_G = 9806.65                      # rho*g, N/m^3
CFS_TO_CMS = 0.0283168466

NHDHR = "https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3"

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def _save():
    tmp = CACHE + ".tmp"
    json.dump(_cache, open(tmp, "w"))
    os.replace(tmp, CACHE)


def _get(url, tries=3, timeout=120):
    last = None
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "place-threshold-screen/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:                            # noqa: BLE001
            last = e
            time.sleep(1.5 * (a + 1))
    print(f"   [net] {type(last).__name__}: {str(last)[:90]}", file=sys.stderr)
    return None


def reaches(lat, lon, radius_km=FLOW_KM):
    """Network flowlines within radius, with EROM attributes. None means UNMEASURED, not empty.

    Three-valued for A14's stated reason: a network failure scored as 'no water here' deletes
    a candidate silently and looks exactly like a measurement. An EMPTY LIST is a real answer
    (no mapped network flowline in 10 km); None is a refusal to answer.
    """
    key = f"hr|{radius_km}|{lat:.4f},{lon:.4f}"
    if key in _cache:
        return _cache[key]
    g = json.dumps({"x": lon, "y": lat, "spatialReference": {"wkid": 4326}})
    u = (f"{NHDHR}/query?f=json&where=1%3D1"
         f"&outFields=qema,vema,slope,totdasqkm,petma,streamorde"
         f"&geometry={urllib.parse.quote(g)}&geometryType=esriGeometryPoint&inSR=4326"
         f"&spatialRel=esriSpatialRelIntersects&distance={int(radius_km * 1000)}"
         f"&units=esriSRUnit_Meter&returnGeometry=false&resultRecordCount=4000")
    j = _get(u)
    if j is None or "error" in j:
        return None
    rows = []
    for f in j.get("features", []):
        a = f.get("attributes", {})
        rows.append([a.get("qema"), a.get("vema"), a.get("slope"),
                     a.get("totdasqkm"), a.get("petma"), a.get("streamorde")])
    _cache[key] = rows
    return rows


def _pos(v):
    """NHDPlus sentinels. -9998/-9999 are NODATA and 0 slope is not a measured gradient."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v <= 0 or v < -9000:
        return None
    return v


def terms(rows):
    """rows -> dict of C1/C2/C3 + the two controls. None throughout if unmeasured."""
    if rows is None:
        return None
    q = [x for x in (_pos(r[0]) for r in rows) if x is not None]
    v = [x for x in (_pos(r[1]) for r in rows) if x is not None]
    # stream power needs Q and S on the SAME reach, so it is computed per-row, not from maxima
    om, area, pet = [], [], []
    for r in rows:
        qq, ss = _pos(r[0]), _pos(r[2])
        if qq is not None and ss is not None:
            om.append(RHO_G * qq * CFS_TO_CMS * ss)
        aa, pp = _pos(r[3]), _pos(r[4])
        if aa is not None:
            area.append(aa)
        if pp is not None:
            pet.append(pp)
    return {
        "n_reach": len(rows),
        "q_max_cfs": max(q) if q else None,
        "v_max_fps": max(v) if v else None,
        "omega_max_wpm": max(om) if om else None,
        "area_max_km2": max(area) if area else None,
        "pet_mean": (sum(pet) / len(pet)) if pet else None,
    }


# ---------------------------------------------------------------- statistics

def median(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return None
    n = len(v)
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def perm_test(a, b, n_perm=N_PERM, seed=SEED, two_tailed=True):
    """Permutation test on the difference of medians. TWO-TAILED by declaration."""
    a = [x for x in a if x is not None]
    b = [x for x in b if x is not None]
    if len(a) < 3 or len(b) < 3:
        return {"n_a": len(a), "n_b": len(b), "p": None, "note": "insufficient n"}
    obs = median(a) - median(b)
    pool = a + b
    na = len(a)
    rnd = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        rnd.shuffle(pool)
        d = median(pool[:na]) - median(pool[na:])
        if (abs(d) >= abs(obs)) if two_tailed else (d >= obs):
            hits += 1
    return {"n_a": na, "n_b": len(b), "med_a": round(median(a), 4),
            "med_b": round(median(b), 4), "diff": round(obs, 4),
            "p": round((hits + 1) / (n_perm + 1), 4), "two_tailed": two_tailed}


def ols(y, X):
    """Plain least squares via normal equations. Returns coefficients incl. intercept."""
    n = len(y)
    k = len(X[0]) + 1
    A = [[1.0] + list(row) for row in X]
    XtX = [[sum(A[i][r] * A[i][c] for i in range(n)) for c in range(k)] for r in range(k)]
    Xty = [sum(A[i][r] * y[i] for i in range(n)) for r in range(k)]
    # Gaussian elimination with partial pivoting
    M = [XtX[r] + [Xty[r]] for r in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12:
            return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(k):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(k + 1)]
    return [M[r][k] for r in range(k)]


def residualise(pts, ykey, ctrl_keys):
    """Pooled OLS of log10(y) on controls; writes '<ykey>_resid' onto each usable point.

    Fitted on the POOLED population so the fit cannot see group membership. Points missing
    y or any control get None and are excluded from the residual test -- excluded, not
    zero-filled, because a zero-filled residual is a fabricated measurement at the mean.
    """
    use = [p for p in pts
           if p.get(ykey) is not None and all(p.get(c) is not None for c in ctrl_keys)]
    if len(use) < 10 + len(ctrl_keys):
        return 0, None
    y = [math.log10(p[ykey]) for p in use]
    X = [[math.log10(p[c]) if c.endswith("km2") else float(p[c]) for c in ctrl_keys]
         for p in use]
    beta = ols(y, X)
    if beta is None:
        return 0, None
    for p, yy, xx in zip(use, y, X):
        pred = beta[0] + sum(b * x for b, x in zip(beta[1:], xx))
        p[ykey + "_resid"] = yy - pred
    return len(use), [round(b, 5) for b in beta]


def rank_norm(vals):
    """Rank-normalise to [0,1]. None stays None."""
    idx = [i for i, v in enumerate(vals) if v is not None]
    order = sorted(idx, key=lambda i: vals[i])
    out = [None] * len(vals)
    m = max(len(order) - 1, 1)
    for r, i in enumerate(order):
        out[i] = r / m
    return out


def spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 5:
        return None
    rx = rank_norm([p[0] for p in pairs])
    ry = rank_norm([p[1] for p in pairs])
    n = len(pairs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(num / (dx * dy), 4) if dx and dy else None


def quartile_bounds(vals):
    v = sorted(x for x in vals if x is not None)
    if len(v) < 8:
        return None
    return [v[int(len(v) * f)] for f in (0.25, 0.5, 0.75)]


# ---------------------------------------------------------------- self test

def self_test():
    """Exercise the branches that would fail silently. Runs before any network call."""
    ok = True

    # _pos must reject NHDPlus sentinels AND zero slope, not merely negatives
    for bad in (-9998, -9999.0, 0, 0.0, None, "", "n/a"):
        if _pos(bad) is not None:
            print(f"  FAIL _pos({bad!r}) -> {_pos(bad)!r}"); ok = False
    if _pos(0.031) != 0.031:
        print("  FAIL _pos passthrough"); ok = False

    # stream power must pair Q and S on the SAME reach. A reach with Q and no S contributes
    # nothing; taking max(Q)*max(S) across different reaches would invent a reach.
    rows = [[100.0, 2.0, None, 50.0, 700.0, 4],      # big Q, NO slope -> no omega
            [1.0, 0.5, 0.10, 5.0, 700.0, 2]]         # small Q, steep  -> the only omega
    t = terms(rows)
    expect = RHO_G * 1.0 * CFS_TO_CMS * 0.10
    if abs(t["omega_max_wpm"] - expect) > 1e-6:
        print(f"  FAIL omega pairing: {t['omega_max_wpm']} != {expect}"); ok = False
    if t["q_max_cfs"] != 100.0:
        print("  FAIL q_max"); ok = False

    # UNMEASURED must not collapse to empty
    if terms(None) is not None:
        print("  FAIL terms(None)"); ok = False
    t0 = terms([])
    if t0 is None or t0["q_max_cfs"] is not None or t0["n_reach"] != 0:
        print("  FAIL terms([]) should be a real empty answer"); ok = False

    # two-tailed perm test must not be fooled by sign: a LOWER median is still a difference
    rnd = random.Random(1)
    lo = [rnd.gauss(0, 1) for _ in range(60)]
    hi = [rnd.gauss(3, 1) for _ in range(60)]
    p_up = perm_test(hi, lo, n_perm=2000)["p"]
    p_dn = perm_test(lo, hi, n_perm=2000)["p"]
    if not (p_up < 0.05 and p_dn < 0.05):
        print(f"  FAIL two-tailed symmetry: up={p_up} dn={p_dn}"); ok = False
    p_one = perm_test(lo, hi, n_perm=2000, two_tailed=False)["p"]
    if p_one < 0.5:
        print(f"  FAIL one-tailed control should be large, got {p_one}"); ok = False

    # OLS must recover a known plane exactly
    beta_true = [2.0, 1.5, -0.5]
    X = [[i * 0.1, (i % 7) * 0.3] for i in range(40)]
    y = [beta_true[0] + beta_true[1] * a + beta_true[2] * b for a, b in X]
    got = ols(y, X)
    if got is None or max(abs(g - t) for g, t in zip(got, beta_true)) > 1e-6:
        print(f"  FAIL ols: {got}"); ok = False

    # residualise must EXCLUDE incomplete points, never zero-fill them
    r2 = random.Random(7)
    pts = []
    for _ in range(30):
        a, p_, rl = r2.uniform(0.5, 3.0), r2.uniform(400, 900), r2.uniform(100, 1200)
        pts.append({"omega_max_wpm": 10.0 ** (0.8 * a - 0.002 * p_ + 0.001 * rl + 1.0),
                    "area_max_km2": 10.0 ** a, "pet_mean": p_, "relief_m": rl})
    pts.append({"omega_max_wpm": 100.0, "area_max_km2": None,
                "pet_mean": 500, "relief_m": 300})
    n_used, b = residualise(pts, "omega_max_wpm", ["area_max_km2", "pet_mean", "relief_m"])
    if n_used != 30 or "omega_max_wpm_resid" in pts[-1]:
        print(f"  FAIL residualise exclusion: n={n_used}"); ok = False
    if b is None or max(abs(x - y) for x, y in zip(b, [1.0, 0.8, -0.002, 0.001])) > 1e-6:
        print(f"  FAIL residualise recovery: {b}"); ok = False
    if any(abs(p.get("omega_max_wpm_resid", 9)) > 1e-9 for p in pts[:30]):
        print("  FAIL residuals should be ~0 on an exact fit"); ok = False

    # AND the singular case must REFUSE, not emit garbage. Perfectly collinear controls --
    # which is what my first fixture accidentally was, and the code caught it before I did.
    sing = [{"omega_max_wpm": 10.0 ** (1 + 0.5 * i), "area_max_km2": 10.0 ** (0.1 * i),
             "pet_mean": 500 + i, "relief_m": 300 + 5 * i} for i in range(30)]
    n_s, b_s = residualise(sing, "omega_max_wpm", ["area_max_km2", "pet_mean", "relief_m"])
    if n_s != 0 or b_s is not None or any("omega_max_wpm_resid" in p for p in sing):
        print(f"  FAIL singular controls should refuse: n={n_s}"); ok = False

    print("  self-test: " + ("PASS" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------- run

def measure(pop, label, save_every=20):
    t0 = time.time()
    for i, p in enumerate(pop):
        r = reaches(p["lat"], p["lon"])
        t = terms(r)
        if t is None:
            p["measured"] = False
        else:
            p.update(t)
            p["measured"] = True
        if (i + 1) % save_every == 0:
            _save()
            el = time.time() - t0
            print(f"  {label} {i+1}/{len(pop)}  {el/ (i+1):.1f}s/pt  "
                  f"eta {(len(pop)-i-1) * el/(i+1)/60:.0f}m", flush=True)
    _save()
    n_ok = sum(1 for p in pop if p.get("measured"))
    print(f"  {label}: {n_ok}/{len(pop)} measured", flush=True)
    return pop


def main():
    print("A16 CURRENT LEG -- pre-registered; see module docstring.", flush=True)
    if not self_test():
        print("ABORT: self-test failed."); sys.exit(2)

    water = json.load(open(WATER))
    surv = water["survivors"]
    nfault = water["null_fault"]
    nrand = water["null_random"]
    print(f"  populations inherited from A14: {len(surv)} / {len(nfault)} / {len(nrand)}",
          flush=True)

    # A13's charge term is a COVARIATE FROM ANOTHER FRAME. charge_term.py:89 declares its
    # population in capitals -- "all 507 stage-2 nodes, NOT the 225 gate survivors" -- and
    # A16 joined to it anyway. The declaration existed; the consumer never read it.
    #
    # BOTH arms are measured before either guard fires. The D200 pre-flight exited on the
    # first arm, which hid the second arm's number and made the defect look like a name-join
    # failure for twenty minutes. See work/a17_charge_coverage_frame.md.
    charge = json.load(open(CHARGE))["rows"]
    cov, frac = {}, {}
    for pop, lab in ((surv, "survivors"), (nfault, "null-fault")):
        hit = 0
        for p in pop:
            c = charge.get(p.get("fault"))
            p["charge_score"] = c.get("charge_score") if c else None
            hit += c is not None
        cov[lab] = f"{hit}/{len(pop)}"
        frac[lab] = (hit / len(pop)) if pop else 0.0
        print(f"  charge coverage {lab}: {hit}/{len(pop)} = {frac[lab]:.1%}", flush=True)

    # GUARD B -- ASYMMETRY, checked FIRST because it names the real defect. A covariate
    # covering 98% of one arm and 29% of the other is not a covariate with missing data:
    # its missingness pattern carries the group label, so the interaction would be partly a
    # contrast between two sampling frames. Measured D200: 3.38x on the old NULL-FAULT,
    # 0.87x on the rebuilt one. The ratio is a direct gauge of the frame defect, and no bar
    # was ever declared on it -- which is why it was free to confirm the rebuild.
    lo, hi = min(frac.values()), max(frac.values())
    ratio = (hi / lo) if lo > 0 else float("inf")
    print(f"  charge coverage asymmetry: {ratio:.2f}x (guard fires above 2.0x)", flush=True)
    # GUARD A -- floor. Under half an arm scored, the interaction is mostly absence.
    low = [l for l in frac if frac[l] < 0.5]

    bar_iv_unrun = None
    if ratio > 2.0:
        bar_iv_unrun = (f"COVERAGE ASYMMETRY {ratio:.2f}x between arms ({cov}). A13's "
                        f"missingness is a proxy for arm membership, so the interaction "
                        f"would be partly a frame contrast rather than physics.")
    elif low:
        bar_iv_unrun = (f"COVERAGE FLOOR: {', '.join(f'{l} {cov[l]}' for l in low)} below "
                        f"50%. A13's population is stage-2 (charge_term.py:89), not the gate "
                        f"survivors -- a POPULATION MISMATCH, not a name-join failure. "
                        f"Repair is a charge-term rebuild over the true rosters (~1,003 new "
                        f"faults); see work/a17_charge_coverage_frame.md.")
    if bar_iv_unrun:
        print(f"  BAR iv -> UNRUN: {bar_iv_unrun}", flush=True)
        print("  bars i/ii/iii/v are UNAFFECTED -- they read flow, not charge -- and "
              "may_reorder_list does not consult bar iv. Continuing.", flush=True)

    measure(surv, "survivors")
    measure(nfault, "null-fault")
    measure(nrand, "null-random")

    pooled = surv + nfault + nrand
    n_res, beta = residualise(pooled, "omega_max_wpm",
                              ["area_max_km2", "pet_mean", "relief_m"])
    print(f"  residual model fitted on {n_res} pooled points; beta={beta}", flush=True)

    stats = {}
    for key in ("v_max_fps", "q_max_cfs", "omega_max_wpm", "omega_max_wpm_resid"):
        stats[key] = {
            "vs_null_random": perm_test([p.get(key) for p in surv],
                                        [p.get(key) for p in nrand]),
            "vs_null_fault": perm_test([p.get(key) for p in surv],
                                       [p.get(key) for p in nfault]),
        }

    # BAR iii -- the stratified table IS the headline
    bounds = quartile_bounds([p.get("relief_m") for p in pooled])
    strata = []
    if bounds:
        edges = [-1e9] + bounds + [1e9]
        for qi in range(4):
            lo, hi = edges[qi], edges[qi + 1]
            a = [p.get("v_max_fps") for p in surv
                 if p.get("relief_m") is not None and lo <= p["relief_m"] < hi]
            b = [p.get("v_max_fps") for p in nfault
                 if p.get("relief_m") is not None and lo <= p["relief_m"] < hi]
            r = perm_test(a, b, n_perm=5000)
            r["quartile"] = qi + 1
            r["relief_lo"] = None if qi == 0 else round(lo, 1)
            r["relief_hi"] = None if qi == 3 else round(hi, 1)
            strata.append(r)
    sig = [s for s in strata if s.get("p") is not None and s["p"] < 0.05]
    signs = {(1 if s.get("diff", 0) > 0 else -1) for s in sig}
    bar_iii = len(sig) >= 3 and len(signs) == 1

    # BAR iv -- the interaction, marginals partialled out.
    # UNRUN is a declared state, not an omission: it emits with its reason, per the project's
    # G3 convention (an absent leg emits UNRUN on every row, never an omitted column).
    inter = {}
    if bar_iv_unrun:
        inter = {"status": "UNRUN", "reason": bar_iv_unrun,
                 "coverage": cov, "asymmetry": round(ratio, 3)}
        bar_iv = None
    else:
        both = surv + nfault
        for p in both:
            cs, om = p.get("charge_score"), p.get("omega_max_wpm_resid")
            p["x_term"] = None
        rc = rank_norm([p.get("charge_score") for p in both])
        ro = rank_norm([p.get("omega_max_wpm_resid") for p in both])
        for p, a, b in zip(both, rc, ro):
            p["x_marg_c"], p["x_marg_o"] = a, b
            p["x_raw"] = None if (a is None or b is None) else a * b
        n_x, beta_x = residualise([p for p in both if p.get("x_raw")],
                                  "x_raw", ["x_marg_c", "x_marg_o"])
        inter["n"] = n_x
        inter["beta"] = beta_x
        inter["test"] = perm_test([p.get("x_raw_resid") for p in surv],
                                  [p.get("x_raw_resid") for p in nfault])
        inter["marginal_charge"] = perm_test([p.get("charge_score") for p in surv],
                                             [p.get("charge_score") for p in nfault])
        bar_iv = inter["test"].get("p") is not None and inter["test"]["p"] < 0.05

    # BAR v -- the band relabelling test A14 flunked
    band = sorted([p for p in surv if p.get("rank")], key=lambda p: p["rank"])[:23]
    bandv = [p.get("v_max_fps") for p in band]
    bandv_ok = [x for x in bandv if x is not None]
    bar_v = {"n_band": len(bandv_ok)}
    if len(bandv_ok) >= 8:
        rn = rank_norm(bandv)
        obs = max(x for x in rn if x is not None) - min(x for x in rn if x is not None)
        rnd = random.Random(SEED)
        pool = [x for x in rn if x is not None]
        hits = 0
        for _ in range(N_PERM):
            rnd.shuffle(pool)
            if (max(pool) - min(pool)) <= obs:
                hits += 1
        bar_v.update({"observed_spread": round(obs, 4),
                      "p_le_obs": round((hits + 1) / (N_PERM + 1), 4)})
    bar_v_pass = bar_v.get("p_le_obs") is not None and bar_v["p_le_obs"] < 0.05

    bars = {
        "bar_i_leaks": (stats["v_max_fps"]["vs_null_random"].get("p") or 1) < 0.05,
        "bar_ii_discriminates": (stats["v_max_fps"]["vs_null_fault"].get("p") or 1) < 0.05,
        "bar_iii_survives_relief": bar_iii,
        # null here means UNRUN, NOT failed -- inter["reason"] carries why. A reader who
        # takes null for false would read an unmeasured bar as a negative result.
        "bar_iv_interacts": bar_iv,
        "bar_iv_status": "UNRUN" if bar_iv is None else ("PASS" if bar_iv else "FAIL"),
        "bar_v_not_relabelling": bar_v_pass,
    }
    may_reorder = bars["bar_ii_discriminates"] and bars["bar_iii_survives_relief"] and bar_v_pass

    out = {
        "leg": "A16 -- current / hydroelectric term + water x charge interaction",
        "frozen": ("Populations, seed and radii inherited UNCHANGED from A14. "
                   "Two-tailed by declaration. Residual is the primary statistic."),
        "asked_by": "Clayton, Day 200 / 2026-08-19: 'rushing water ... hydroelectricity, as it were'",
        "seed": SEED, "n_perm": N_PERM, "flow_km": FLOW_KM,
        "charge_join_coverage": cov,
        "source": NHDHR,
        "residual_model": {"y": "log10(omega_max_wpm)",
                           "controls": ["log10(area_max_km2)", "petma", "relief_m"],
                           "n": n_res, "beta": beta},
        "statistics": stats,
        "relief_strata_v_max": strata,
        "interaction": inter,
        "band_relabelling": bar_v,
        "spearman_v_vs_score": spearman([p.get("v_max_fps") for p in surv],
                                        [p.get("score") for p in surv]),
        "spearman_v_vs_relief": spearman([p.get("v_max_fps") for p in surv],
                                         [p.get("relief_m") for p in surv]),
        "bars": bars,
        "may_reorder_list": may_reorder,
        "guard": ("A16 may not move a name unless bars ii, iii and v all pass. "
                  "Declared before the result existed."),
        "survivors": surv, "null_fault": nfault, "null_random": nrand,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps({"bars": bars, "may_reorder": may_reorder,
                      "v_vs_fault": stats["v_max_fps"]["vs_null_fault"],
                      "omega_resid_vs_fault": stats["omega_max_wpm_resid"]["vs_null_fault"],
                      "interaction": inter.get("test", {"status": inter.get("status"),
                                                        "reason": inter.get("reason")}),
                      "strata": [(s["quartile"], s.get("diff"), s.get("p")) for s in strata]},
                     indent=1), flush=True)
    print(f"WROTE {OUT}", flush=True)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    main()
