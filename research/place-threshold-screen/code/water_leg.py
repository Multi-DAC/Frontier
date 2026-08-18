"""A14 -- THE WATER / ELECTROKINETIC TERM. Pre-registered before the first query.

Clayton, Day 199: "high electromagnetic potential from either water or mineral, or both
combined, are relevant" ... "Let's do the water leg and the radon/uranium leg as well."

A13 named this leg as deliberately ABSENT and said why: the electrokinetic term "is NOT in
this leg because it is not a LITHOLOGY ... Guessing it from rock type would be reading
hydrology off a geologic map ... until that leg exists this screen's water coverage is ZERO,
not partial." This is that leg.

THE MECHANISM. Groundwater moving through a fractured medium drags the mobile part of the
electrical double layer at the mineral-water interface and generates a streaming current;
the resulting self-potential is the largest naturally occurring electrical signal in shallow
crust, routinely tens to hundreds of millivolts across fault-controlled flow, and it is what
self-potential surveys have mapped over dams, geothermal fields and fault zones for a
century. The coupling coefficient is

        C = eps * zeta / (eta * sigma)

    eps  fluid permittivity      zeta  zeta potential of the mineral-water interface
    eta  fluid viscosity         sigma FLUID ELECTRICAL CONDUCTIVITY

  ! SIGMA IS IN THE DENOMINATOR, AND THIS LEG IS BUILT AROUND THAT SIGN. The intuitive move
    -- "mineralised, saline, conductive water must make a bigger electrical anomaly" -- is
    BACKWARDS. Raising fluid conductivity SUPPRESSES the streaming potential, because the
    same dragged charge is short-circuited through the more conductive electrolyte. A screen
    that scored salinity positively would have the sign of its own physics wrong and would
    still produce a confident ranked list. Salinity is therefore NOT scored here at all; the
    honest statement is that its effect is opposite to the naive one and that this leg does
    not have the fluid-chemistry data to price it.

  The terms that ARE scored, each because it is a measurable proxy for a factor that is
  actually in the numerator or in the flow rate:

    W1 SPRING AND SEEP DENSITY.  A spring is where subsurface flow is FOCUSED and reaches
       the surface -- the observable end of exactly the flow that generates the potential.
       In the arid west a mapped spring on a range front is usually fault-controlled
       discharge. Source: NHD layer 0, FTYPE 458 (SpringSeep).
    W2 HYDRAULIC HEAD GRADIENT.  The driver. Topographic relief sets the head that pushes
       water through the rock, and the classic field observation is the "mountain effect":
       self-potential varies systematically and negatively with elevation because of
       topographically driven groundwater flow. Source: USGS 3DEP, sampled as a 5x5 grid at
       +/-5 km, batched.
    W3 PERENNIAL SURFACE WATER.  In the Basin and Range an ephemeral wash means a rainstorm;
       a PERENNIAL stream means sustained groundwater discharge. The distinction is the
       measurement, so the query is restricted to FCODE 46006 (perennial) and intermittent
       flowlines are deliberately not counted. Source: NHD flowline.

THE CIRCULARITY THAT WOULD MAKE A POSITIVE RESULT MEANINGLESS, and the control for it.
Springs occur along faults BECAUSE faults are permeability contrasts. Comparing the screen's
survivors against random western ground would therefore find more springs on the survivors
with near-certainty, and the finding would be "faults leak", which was known before this
project started and says nothing whatever about the screen. The comparison that carries
information is against OTHER MAPPED QUATERNARY FAULTS. So, as in A15 and with the same
points:

  SURVIVORS   the 225 that passed the L1 gate.
  NULL-RANDOM 400 points, SAME SEED and SAME bbox derivation as A8/A12/A15 -- shared draw,
              not shared verdict. Reported, but it is the WEAK comparison and is labelled so.
  NULL-FAULT  400 stage-2 nodes that FAILED the L1 gate. THE BAR THAT MATTERS.

AND THE SECOND CONFOUND, which A7-iv already priced for the junction term and which applies
here unchanged: NHD spring density is a MAPPING density. Springs are recorded where someone
walked, and the west is surveyed unevenly. A raw count difference between two populations
can be a difference in survey attention. NULL-FAULT partially controls this too -- mapped
faults and mapped springs share much of the same survey history -- and the residual is
stated rather than corrected, because there is no national spring-survey-effort layer to
correct against.

DECLARED BEFORE THE FIRST QUERY -- the first line is a PREDICTION, so it can be wrong:

  PREDICTION. Survivors will show substantially more springs and more relief than
  NULL-RANDOM (near-tautological: they are on faults, and faults are in mountains), and
  will show NO significant difference from NULL-FAULT on any of the three terms. I expect
  this leg to return a null on every bar that carries information. Written here so that the
  tautological half cannot later be reported as a discovery.

  BAR i   LEAKS if survivor median spring count within 25 km exceeds NULL-RANDOM at
          permutation p < 0.05. Expected to pass and expected to mean little.
  BAR ii  DISCRIMINATES if survivor spring count exceeds NULL-FAULT at p < 0.05. This is
          the bar that decides whether the SCREEN selected wetter faults, as opposed to the
          fault catalogue having selected them.
  BAR iii GRADIENT if survivor relief exceeds NULL-FAULT at p < 0.05.
  BAR iv  PERENNIAL if survivor perennial-flowline count exceeds NULL-FAULT at p < 0.05.
  BAR v   INDEPENDENT if |Spearman rho| between the water score and the screen score across
          survivors is < 0.7. At >= 0.7 it is a relabelling of terrain the screen already
          scores.

  ! AND THE TIE-BREAKER CONSTRAINT A7 IMPOSED ON EVERY NEW CRITERION. A7 measured that the
    top ten is not a ranking: only 4 of 9 adjacent order pairs hold, 23 survivors sit within
    one L1 vertex of the rank-10 line, and slip is the same number for 86.2% of the 225. Any
    new criterion used to reorder that band must be tested AS A TIE-BREAKER against that
    measured resolution or it merely adds a fifth coarse ordinal and moves names at random.
    So this leg reports, separately from the bars, whether the water score SEPARATES the 23
    band members by more than the band's own score wobble. If it does not, the correct use
    of this leg is as a LABEL on the areas, not as a re-ranking, and it will say so.

  ! NO BAR HERE TESTS WHETHER WATER PRODUCES A LIGHT OR AN ANOMALY. A6 stands unchanged.
"""
import json, math, os, random, sys, time, urllib.parse, urllib.request

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

OUT = "data/water_leg.json"
CACHE = "work/water_cache.json"
SEED = 20260818
N_NULL = 400
N_PERM = 10000
SPRING_KM = 25.0
FLOW_KM = 10.0
RELIEF_KM = 5.0
RELIEF_N = 5

NHD = "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer"
NHD_POINT_LAYER = 0            # 'Point'; SpringSeep is FTYPE 458 INSIDE it, not a layer id
NHD_FLOW_LAYER = 6             # 'Flowline - Large Scale'
FTYPE_SPRINGSEEP = 458
FCODE_PERENNIAL = 46006
ELEV = ("https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation"
        "/ImageServer/getSamples")

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def _save():
    json.dump(_cache, open(CACHE, "w"))


def _get(url, tries=3, timeout=90):
    last = None
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "place-threshold-screen/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            last = e
            time.sleep(1.5 * (a + 1))
    print(f"   [net] {type(last).__name__}: {str(last)[:90]}", file=sys.stderr)
    return None


def nhd_count(lat, lon, layer, where, radius_km):
    """Feature count within radius. None means UNMEASURED, never 0.

    Three-valued for the reason this project keeps relearning: a network failure scored as
    'no springs here' silently deletes the wettest candidate and looks like a measurement.
    """
    key = f"nhd|{layer}|{where}|{radius_km}|{lat:.4f},{lon:.4f}"
    if key in _cache:
        return _cache[key]
    g = json.dumps({"x": lon, "y": lat, "spatialReference": {"wkid": 4326}})
    u = (f"{NHD}/{layer}/query?f=json&where={urllib.parse.quote(where)}"
         f"&geometry={urllib.parse.quote(g)}&geometryType=esriGeometryPoint&inSR=4326"
         f"&spatialRel=esriSpatialRelIntersects&distance={int(radius_km*1000)}"
         f"&units=esriSRUnit_Meter&returnCountOnly=true")
    j = _get(u)
    v = None
    if j is not None and "error" not in j:
        v = j.get("count")
        if v is None:                        # some layers ignore returnCountOnly
            v = len(j.get("features", []))
    _cache[key] = v
    return v


def elev_batch(points):
    """[(lat,lon)] -> [elev|None], one call. 3DEP getSamples takes a multipoint.

    ! RESULTS ARE MATCHED BY RETURNED COORDINATE, NOT BY POSITION OR BY locationId, and the
      reason is a defect this function shipped with and its self-test caught. 3DEP returns
      `samples` OUT OF REQUEST ORDER and numbers `locationId` FROM ZERO. Three points came
      back as locationId 1, 2, 0 -- so indexing by position scrambles them, and the obvious
      `locationId - 1` correction scrambles them differently AND drops the first point.

      What made it dangerous rather than merely wrong: every value returned was real, finite
      and topographically plausible. Hubbell Spring was assigned 1285 m (the Bonneville salt
      flats' elevation) and the salt flats were assigned 2603 m (a Montana fault scarp's).
      Nothing errored. The only visible symptom was one None at the end of the shift, and had
      the batch been one point longer that would have vanished too.

      The returned `location` is echoed back per sample, so matching on it cannot be off by
      one. Tolerance is 1e-6 deg (~0.1 m), far below the 10 m DEM cell.
    """
    g = json.dumps({"points": [[lo, la] for la, lo in points],
                    "spatialReference": {"wkid": 4326}})
    u = (f"{ELEV}?f=json&geometryType=esriGeometryMultipoint"
         f"&geometry={urllib.parse.quote(g)}&returnFirstValueOnly=true")
    j = _get(u)
    if j is None or "samples" not in j:
        return [None] * len(points)
    out = [None] * len(points)
    index = {(round(lo, 6), round(la, 6)): i for i, (la, lo) in enumerate(points)}
    for s in j["samples"]:
        try:
            v = float(s.get("value"))
        except (TypeError, ValueError):
            continue
        loc = s.get("location") or {}
        i = index.get((round(float(loc.get("x", 1e9)), 6), round(float(loc.get("y", 1e9)), 6)))
        if i is None:
            i = s.get("locationId")                     # 0-based fallback, coords missing
            if not isinstance(i, int) or not (0 <= i < len(points)):
                continue
        if math.isfinite(v) and v > -1000:
            out[i] = v
    return out


def prefetch_relief(centres, save_every=15):
    """Fill the relief cache one SITE per call, and never more.

    ! MEASURED, NOT ASSUMED, AND THE OBVIOUS OPTIMISATION IS THE WRONG ONE. The first version
      of this batched 200 points (8 sites) per call, reasoning that fewer round trips is
      faster. It is not: 3DEP getSamples cost is driven by THE NUMBER OF DEM TILES TOUCHED,
      not by the point count. A 25-point grid spanning +/-5 km sits on one or two tiles and
      returns in 4-5 s; 200 points scattered across eight sites in different states span many
      tiles and did not return inside a 5-minute wall.

      That failure is worse than slow. `_get` retries three times at a 90 s timeout, so a
      stalled chunk burns 4.5 minutes and then returns None for all 200 points -- and a
      site whose grid comes back mostly None is recorded as UNMEASURED relief. The run would
      have completed, taken two hours, and reported a large field of honest-looking
      unmeasured relief caused entirely by a batching choice. A timeout converting a red into
      an unknown is the quiet version of this project's favourite defect.

      Per-site it is: ~5 s each, and the cache is written every 15 sites so a kill costs
      seconds rather than the run.
    """
    need = [c for c in centres
            if f"relief|{RELIEF_KM}|{RELIEF_N}|{c[0]:.4f},{c[1]:.4f}" not in _cache]
    if not need:
        return
    print(f"   [relief] {len(need)} sites, one call each", file=sys.stderr)
    for i, c in enumerate(need, 1):
        ev = [e for e in elev_batch(relief_grid(*c)) if e is not None]
        rel = None
        if len(ev) >= RELIEF_N * RELIEF_N * 0.8:
            mean = sum(ev) / len(ev)
            rel = dict(relief_m=round(max(ev) - min(ev), 1), mean_m=round(mean, 1),
                       sd_m=round((sum((e - mean) ** 2 for e in ev) / len(ev)) ** 0.5, 1),
                       n=len(ev))
        _cache[f"relief|{RELIEF_KM}|{RELIEF_N}|{c[0]:.4f},{c[1]:.4f}"] = rel
        if i % save_every == 0:
            print(f"   [relief] {i}/{len(need)}", file=sys.stderr)
            _save()
    _save()


def relief_grid(lat, lon):
    """RELIEF_N x RELIEF_N sample points spanning +/-RELIEF_KM, in lat/lon."""
    dlat = RELIEF_KM / 111.0
    dlon = RELIEF_KM / (111.0 * max(0.2, math.cos(math.radians(lat))))
    pts = []
    for i in range(RELIEF_N):
        for j in range(RELIEF_N):
            fy = -1 + 2 * i / (RELIEF_N - 1)
            fx = -1 + 2 * j / (RELIEF_N - 1)
            pts.append((lat + fy * dlat, lon + fx * dlon))
    return pts


def median(v):
    s = sorted(v)
    n = len(s)
    if not n:
        return None
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def perm_test(a, b, n_perm=N_PERM, seed=SEED):
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
        if abs(median(pool[:na]) - median(pool[na:])) >= abs(obs) - 1e-12:
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
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0 + 1
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


def self_test():
    """The queries are checked where a right and a wrong answer DISAGREE, before the run.

    Hubbell Spring is the project's founding site and is named for a spring; a query that
    cannot find springs there is broken regardless of what it returns elsewhere. The Bonneville
    salt flats are flat; a relief query that reports mountains there is broken. Both fixtures
    fail loudly rather than returning a plausible number.
    """
    ok = True
    n = nhd_count(34.72, -106.68, NHD_POINT_LAYER, f"FTYPE={FTYPE_SPRINGSEEP}", SPRING_KM)
    print(f"   springs within {SPRING_KM:.0f} km of Hubbell Spring NM: {n}", file=sys.stderr)
    if not n:
        print("   !! FAIL: no springs at the site the project is named after", file=sys.stderr)
        ok = False

    # --- THE ELEVATION FIXTURE IS BUILT SO THAT A PERMUTATION FAILS IT.
    # The first version of this test used three points and checked only for None. It caught
    # the locationId scramble by luck -- one point fell off the end of an off-by-one and left
    # a None. Every other point had been silently reassigned to a different mountain and the
    # test said nothing. A fixture for an ordering defect must FAIL UNDER PERMUTATION, so
    # these three sites are chosen to be mutually separated by >200 m and each is checked
    # against its own expected elevation, not merely against being non-null.
    fix = [("Hubbell Spring NM", 34.72, -106.68, 1505),
           ("Bonneville flats UT", 40.75, -113.85, 1285),
           ("Hebgen scarp MT", 44.84, -111.34, 2604)]
    ev = elev_batch([(la, lo) for _, la, lo, _ in fix])
    for (nm, _, _, exp), got in zip(fix, ev):
        bad = got is None or abs(got - exp) > 200
        print(f"   elev {nm:22s} got={got} expect~{exp}{'   !! MISMATCH' if bad else ''}",
              file=sys.stderr)
        if bad:
            ok = False
    if not ok:
        print("   !! FAIL: 3DEP samples are misassigned or missing -- see elev_batch note",
              file=sys.stderr)
    elif ev == sorted(ev):
        print("   (note: fixture elevations happen to be sorted; ordering check is weak)",
              file=sys.stderr)
    flat = elev_batch(relief_grid(40.75, -113.85))
    steep = elev_batch(relief_grid(44.84, -111.34))
    if all(e is not None for e in flat) and all(e is not None for e in steep):
        rf, rs = max(flat) - min(flat), max(steep) - min(steep)
        print(f"   relief: Bonneville flats={rf:.0f} m   Hebgen={rs:.0f} m", file=sys.stderr)
        if rf >= rs:
            print("   !! FAIL: salt flats are not less rugged than Hebgen -- "
                  "grid geometry is suspect", file=sys.stderr)
            ok = False
    print(f"   SELF-TEST {'PASS' if ok else 'FAIL'}", file=sys.stderr)
    _save()
    return ok


def probe(lat, lon):
    sp = nhd_count(lat, lon, NHD_POINT_LAYER, f"FTYPE={FTYPE_SPRINGSEEP}", SPRING_KM)
    pf = nhd_count(lat, lon, NHD_FLOW_LAYER, f"FCODE={FCODE_PERENNIAL}", FLOW_KM)
    key = f"relief|{RELIEF_KM}|{RELIEF_N}|{lat:.4f},{lon:.4f}"
    if key in _cache:
        rel = _cache[key]
    else:
        ev = [e for e in elev_batch(relief_grid(lat, lon)) if e is not None]
        rel = None
        if len(ev) >= RELIEF_N * RELIEF_N * 0.8:
            mean = sum(ev) / len(ev)
            rel = dict(relief_m=round(max(ev) - min(ev), 1),
                       mean_m=round(mean, 1),
                       sd_m=round((sum((e - mean) ** 2 for e in ev) / len(ev)) ** 0.5, 1),
                       n=len(ev))
        _cache[key] = rel
    return dict(springs_25km=sp, perennial_10km=pf,
                relief_m=(rel or {}).get("relief_m"),
                elev_mean_m=(rel or {}).get("mean_m"),
                relief_sd_m=(rel or {}).get("sd_m"),
                measured=(sp is not None and rel is not None))


def run(pop, label):
    prefetch_relief([(p["lat"], p["lon"]) for p in pop])
    rows = []
    for i, p in enumerate(pop, 1):
        rows.append(dict(**{k: v for k, v in p.items() if k in ("fault", "lat", "lon",
                                                                "rank", "score")},
                         **probe(p["lat"], p["lon"])))
        if i % 20 == 0:
            print(f"   {label} {i}/{len(pop)}", file=sys.stderr)
            _save()
    _save()
    return rows


if __name__ == "__main__":
    if not self_test():
        sys.exit("[A14] ABORT: query self-test failed; a null would be unreadable")

    surv = json.load(open("data/stage5_join_summary.json"))["survivors_ranked"]
    stage2 = json.load(open("data/transport_screen_stage2.json"))["all"]

    print(f"[A14] survivors={len(surv)}", file=sys.stderr)
    rows = run([dict(fault=s["fault_name"], lat=s["lat"], lon=s["lon"],
                     rank=s.get("rank"), score=s.get("score")) for s in surv], "surv")

    lats = [s["lat"] for s in surv]
    lons = [s["lon"] for s in surv]
    bbox = (min(lats), max(lats), min(lons), max(lons))
    rnd = random.Random(SEED)
    rpts = [dict(lat=round(rnd.uniform(bbox[0], bbox[1]), 4),
                 lon=round(rnd.uniform(bbox[2], bbox[3]), 4)) for _ in range(N_NULL)]
    print(f"[A14] null-random={N_NULL} in bbox {tuple(round(b,2) for b in bbox)}", file=sys.stderr)
    null_r = run(rpts, "null-rand")

    surv_names = {s["fault_name"] for s in surv}
    pool, seen = [], set()
    for n in stage2:
        nm = (n.get("fault_name") or "").strip()
        if not nm or nm in surv_names or nm in seen:
            continue
        if n.get("lat") is None or n.get("lon") is None:
            continue
        seen.add(nm)
        pool.append(dict(fault=nm, lat=n["lat"], lon=n["lon"]))
    rnd2 = random.Random(SEED + 1)
    rnd2.shuffle(pool)
    print(f"[A14] null-fault={min(N_NULL,len(pool))} of {len(pool)} non-survivor faults",
          file=sys.stderr)
    null_f = run(pool[:N_NULL], "null-fault")

    def vals(rs, k):
        return [r[k] for r in rs if r.get(k) is not None]

    res = {}
    for k in ("springs_25km", "perennial_10km", "relief_m", "elev_mean_m"):
        d_r, p_r, e_r = perm_test(vals(rows, k), vals(null_r, k))
        d_f, p_f, e_f = perm_test(vals(rows, k), vals(null_f, k))
        res[k] = dict(surv_median=median(vals(rows, k)),
                      null_random_median=median(vals(null_r, k)),
                      null_fault_median=median(vals(null_f, k)),
                      n_surv=len(vals(rows, k)), n_null_random=len(vals(null_r, k)),
                      n_null_fault=len(vals(null_f, k)),
                      vs_random=dict(diff=d_r, p=p_r, note=e_r),
                      vs_fault=dict(diff=d_f, p=p_f, note=e_f))

    # water score: rank-normalised mean of the three terms, only where all three exist.
    # Deliberately NOT a weighted physical sum -- there is no measured exchange rate between
    # a spring count and a metre of relief, and inventing one would be a fabricated constant.
    def rank_norm(rs, k):
        v = [(r.get(k), i) for i, r in enumerate(rs)]
        ok = sorted([x for x in v if x[0] is not None])
        out = [None] * len(rs)
        for pos, (_, i) in enumerate(ok):
            out[i] = pos / max(1, len(ok) - 1)
        return out

    ns, nf, nr = rank_norm(rows, "springs_25km"), rank_norm(rows, "relief_m"), \
        rank_norm(rows, "perennial_10km")
    for i, r in enumerate(rows):
        parts = [x for x in (ns[i], nf[i], nr[i]) if x is not None]
        r["water_score"] = round(sum(parts) / len(parts), 4) if len(parts) == 3 else None

    paired = [(r["score"], r["water_score"]) for r in rows
              if r.get("score") is not None and r.get("water_score") is not None]
    rho = spearman([p[0] for p in paired], [p[1] for p in paired]) if paired else None

    # --- A7 tie-breaker test: does the water score separate the 23-member band?
    band_sep = None
    try:
        band = json.load(open("data/rank_resolution.json"))["A7v_contender_band"]["members"]
        bn = {b["fault"] for b in band}
        bw = [r["water_score"] for r in rows
              if r["fault"] in bn and r.get("water_score") is not None]
        bs = [r["score"] for r in rows if r["fault"] in bn and r.get("score") is not None]
        if len(bw) >= 3:
            band_sep = dict(
                n_band_scored=len(bw),
                water_score_spread=round(max(bw) - min(bw), 4),
                screen_score_spread=round(max(bs) - min(bs), 4) if bs else None,
                note="A tie-breaker is only usable if it separates band members by more than "
                     "the band's own score wobble. Reported, not asserted.")
    except Exception as e:
        band_sep = dict(error=str(e)[:150])

    bars = dict(
        bar_i_leaks=(res["springs_25km"]["vs_random"]["p"] is not None
                     and res["springs_25km"]["vs_random"]["p"] < 0.05
                     and (res["springs_25km"]["vs_random"]["diff"] or 0) > 0),
        bar_ii_discriminates=(res["springs_25km"]["vs_fault"]["p"] is not None
                              and res["springs_25km"]["vs_fault"]["p"] < 0.05
                              and (res["springs_25km"]["vs_fault"]["diff"] or 0) > 0),
        bar_iii_gradient=(res["relief_m"]["vs_fault"]["p"] is not None
                          and res["relief_m"]["vs_fault"]["p"] < 0.05
                          and (res["relief_m"]["vs_fault"]["diff"] or 0) > 0),
        bar_iv_perennial=(res["perennial_10km"]["vs_fault"]["p"] is not None
                          and res["perennial_10km"]["vs_fault"]["p"] < 0.05
                          and (res["perennial_10km"]["vs_fault"]["diff"] or 0) > 0),
        bar_v_independent=(rho is not None and abs(rho) < 0.7))

    top = sorted([r for r in rows if r.get("water_score") is not None],
                 key=lambda r: -r["water_score"])[:15]

    out = dict(
        leg="A14 water / electrokinetic term",
        frozen="Day 199, 2026-08-18; mechanism, sign of sigma, populations, prediction and "
               "bars declared in water_leg.py docstring before the first query",
        sources=dict(springs=f"NHD MapServer layer {NHD_POINT_LAYER} FTYPE={FTYPE_SPRINGSEEP}",
                     perennial=f"NHD layer {NHD_FLOW_LAYER} FCODE={FCODE_PERENNIAL}",
                     relief="USGS 3DEP getSamples, %dx%d grid at +/-%.0f km"
                            % (RELIEF_N, RELIEF_N, RELIEF_KM)),
        physics_note="Streaming-potential coupling C = eps*zeta/(eta*sigma). Fluid "
                     "conductivity is in the DENOMINATOR: salinity SUPPRESSES the signal. "
                     "Salinity is not scored, and the naive positive weighting would have "
                     "the sign wrong.",
        seed=SEED, n_perm=N_PERM,
        radii=dict(spring_km=SPRING_KM, perennial_km=FLOW_KM, relief_km=RELIEF_KM),
        statistics=res, spearman_water_vs_score=rho, band_tiebreaker=band_sep, bars=bars,
        top15_by_water_score=[dict(fault=r["fault"], water_score=r["water_score"],
                                   springs_25km=r["springs_25km"],
                                   perennial_10km=r["perennial_10km"],
                                   relief_m=r["relief_m"], rank=r.get("rank")) for r in top],
        survivors=rows, null_random=null_r, null_fault=null_f)
    json.dump(out, open(OUT, "w"), indent=1)

    for k in ("springs_25km", "relief_m", "perennial_10km"):
        r = res[k]
        print(f"[A14] {k:15s} surv={r['surv_median']} rand={r['null_random_median']} "
              f"fault={r['null_fault_median']} | p_rand={r['vs_random']['p']} "
              f"p_fault={r['vs_fault']['p']}", file=sys.stderr)
    print(f"[A14] rho(water,score)={rho}  bars={bars}", file=sys.stderr)
    print(f"[A14] wrote {OUT}", file=sys.stderr)
