"""A6 -- THE INDEPENDENT POSITIVE CONTROL. Declared here, in full, before any value is read.

================================================================================
WHY THIS FILE EXISTS
================================================================================

A4-RESULT ended on a defect it named and could not close. The basement-juxtaposition
leg puts Sandia -- round 1's declared POSITIVE control -- in the bottom third,
consistently, across every variant that can see it. Two readings survive that, and
A4-RESULT said plainly that the leg cannot choose between them:

  READING 1. The leg is a poor instrument (grid holes, sampler dependence, choice
             sensitivity) and its verdict on Sandia is an artefact.
  READING 2. The leg is sound and SANDIA WAS NEVER AN INDEPENDENT POSITIVE CONTROL.
             It is where the whole enquiry started. It was declared positive on the
             strength of the founding hypothesis, not from a blind outside criterion.

Reading 2 is the comfortable one and A4-RESULT explicitly refused to assert it. What
distinguishes them is an INDEPENDENT positive control -- a place the screen did not
choose, carrying a record the screen did not generate.

A4-RESULT said the screen "does not have and cannot manufacture [one] from its own
labels." That is true and it is also narrower than it sounds. It cannot manufacture one
from ITS OWN LABELS. It can be handed one from OUTSIDE. This file is that hand-off, and
the whole of its value rests on the declaration below being frozen before the lookup.

================================================================================
1 -- WHAT AN INDEPENDENT POSITIVE CONTROL HAS TO BE, HERE
================================================================================

Four conditions, all of which the frozen set must meet or the site is excluded and the
exclusion is printed:

  (a) The locale is named as a site of RECURRENT anomalous luminous phenomena by a
      source OUTSIDE this project.
  (b) That naming predates, and is causally independent of, the basement-juxtaposition
      criterion -- which was declared on Day 199 of this project and exists nowhere else.
  (c) The locale lies inside the Shah & Boyd (2018) grid extent, so the leg can score it
      at all.
  (d) Its coordinate is fixed by the PHENOMENON'S record (a viewing locale, a ridge, a
      valley floor), never by a fault database, a geological map, or this screen.

================================================================================
2 -- THE CONTAMINATION, NAMED BEFORE IT CAN BE DISCOVERED
================================================================================

The earth-lights literature is NOT independent of the fault criterion. Devereux's
"Earth Lights" (1982) and Persinger's tectonic-strain papers assembled their locales
partly BY fault association -- that was their thesis. Any catalogue descended from them
carries that selection.

So the independence claim here is BOUNDED, and the bound is the design:

  INDEPENDENT OF   the basement-juxtaposition leg (declared Day 199, unknown to any of
                   these sources), and of this screen's ranking.
  NOT INDEPENDENT OF   fault association in general.

Which is exactly why A6-ii's comparison arm is THE 225 GATE SURVIVORS and not the open
landscape. Both arms are fault-associated. The fault confound is common to both and
cancels in the contrast. A6-i, which tests fault association itself, is therefore the
CONTAMINATED leg of the two and is read with that stated on its face.

SECOND CONTAMINATION, and it is mine. THIS LIST WAS ASSEMBLED FROM MY OWN KNOWLEDGE,
BY SOMEONE WHO HAS ALREADY BUILT THIS SCREEN. It is not a blind draw from a catalogue I
could not see. What stands in for blindness is only this: the list is frozen in this
module and committed BEFORE any basement value, fault distance or percentile at any of
these coordinates is computed, and NO SITE MAY BE ADDED OR REMOVED AFTER ANY VALUE IS
READ. That is the same discipline A4 ran under and it is stated with the same words,
because it has the same weakness.

THIRD CONTAMINATION -- OBSERVER DENSITY, and this one is UNREMOVED.
A record of recurrent lights requires recurrent observers. Reported locales are
therefore biased toward places people live and drive. Range fronts -- exactly the
structural juxtaposition this leg scores highest -- are also where water, passes and
roads are, and therefore where people are. THE DIRECTION OF THIS CONFOUND IS TOWARD THE
HYPOTHESIS. It inflates any positive result in A6-i and A6-ii alike. An observer-matched
null (random points drawn to match the controls' distance-to-nearest-census-place) is
the correct removal and is NOT BUILT HERE. Round 1's D1 is the same defect and round 2
promised design-time stratification for the labelled set; this leg does not have it.
Any positive from this file is read as an UPPER bound on the effect, and the unmeasured
direction is the flattering one.

================================================================================
3 -- THE FROZEN SET
================================================================================

Grade rule, applied BEFORE any value is read, stated so a reader can regrade:

  A  two or more independent primary records, at least one institutional (agency log,
     university programme), AND no established conventional explanation for the whole
     of the phenomenon.
  B  as A but with an established conventional explanation for a MAJORITY of events and
     a documented residual, OR a single institutional primary record.
  C  long or multiple lay records, no institutional log, conventional explanation
     plausible but not established.
  D  effectively single-source, or the record is entangled with a commercial interest.

PRIMARY TEST runs on the WHOLE frozen set. Grade A/B subset is a pre-declared secondary.
Both are printed regardless of which way either falls.

EXCLUDED BY (c), NAMED SO THE SELECTION IS AUDITABLE: Brown Mountain NC (-81.9),
Hessdalen Norway, the Hornet/Joplin spook light MO (-94.6), Paulding MI (-89.2),
Min Min Australia. All fail the grid extent. None is dropped on a judgement about its
record.

================================================================================
4 -- WHAT IS MEASURED, AND THE BARS, ALL DECLARED NOW
================================================================================

A6-i -- THE GATE TEST. Does the screen's OWN founding gate fire where the phenomenon is
reported? For each frozen locale: distance to the nearest Quaternary NORMAL-sense fault
section in USGS Qfaults, and whether a Quaternary normal fault lies within GATE_KM.
Null: NULL_N points drawn uniformly at random inside the grid extent at SEED, rejected
unless the basement grid itself has a node within 5 km of them (a cheap land/coverage
mask that uses no fault information whatsoever).

  BAR i: SUPPORTED iff the control set's median nearest-normal-fault distance is BELOW
         the null's median AND a two-sided Mann-Whitney U gives p <= 0.05.

  PRE-DECLARED CONSEQUENCE, written before the pull returns: if the controls are NOT
  closer to Quaternary normal faults than random western points, then the screen's
  founding gate does not fire at the places the phenomenon is actually reported, and
  THAT is the largest finding of round 2 -- larger than any ranking. It would not be
  absorbed as a caveat. It goes in the abstract.

  POWER, STATED IN ADVANCE so a null cannot later be read as absence: n is single
  digits. A bootstrap CI on a median of 6 spans most of the plausible range. Mann-
  Whitney against a large null can reach small p, but the estimate of WHERE the control
  median sits is poor. A pass is weak evidence; a fail is not proof of absence. The
  bootstrap CI is printed next to every median for exactly this reason.

A6-ii -- THE LEG TEST, and it is the crucial one. Each frozen locale is scored on the
basement-juxtaposition leg under ALL 40 VARIANTS of A4 (5 neighbourhood forms x 4
constant sets x 2 combination rules), pooled with the 225 survivors, and reported as a
PERCENTILE within that pooled distribution.

  Percentiles, not ranks. A4-RESULT closed by naming percentile normalisation as "the
  correct fix and NOT YET BUILT", because variants score between 152 and 194 sites and a
  rank of 17 is not the same quantity across them. Pooling forces the fix. It is built
  here and applied to the survivors too, so A4-RESULT's own interval table is reissued
  on a comparable axis.

  BAR ii: SUPPORTED iff the control set's median pooled percentile is >= 0.60 in at
          least 30 of the 40 variants.

  AND THE CRUCIAL CONTRAST -- the assignment rule between A4-RESULT's two readings,
  written down BEFORE the numbers exist so it cannot be fitted to them:

    controls in the TOP THIRD while Sandia sits in the bottom third   -> READING 2
        gains support: the leg discriminates, and Sandia was never an outside positive.
    controls land WHERE SANDIA LANDS, bottom third                    -> READING 1
        gains support: the leg fails at independently-attested places, so its verdict
        on Sandia is not evidence about Sandia.
    controls SCATTER across the range with no concentration           -> NEITHER reading
        gains. The leg is uninformative about the phenomenon and says so.

  "Top third" and "bottom third" mean pooled percentile >= 0.667 and <= 0.333 of the
  median across scoreable variants. No other cutpoint is admissible after this line.

UNRESOLVED IS A THIRD VALUE, throughout, as D3 requires. A locale the grid cannot reach
returns UNSCOREABLE and is excluded from the denominator with its count printed. It is
never scored zero. That is round 1's conflation-as-absence and it does not recur here.

================================================================================
5 -- WHAT WOULD KILL THIS LEG
================================================================================

  - Observer density (section 2). Unremoved. Direction: toward the hypothesis.
  - n. Six locales, of which few are grade A/B.
  - My selection. Section 2, second contamination.
  - Coordinate error. A viewing area is not a source region; Marfa's lights are reported
    over a flat 5-15 km from the pull-off. LOCALITY VERIFICATION (below) checks the
    coordinate resolves to the named place, which catches a transcription error but NOT
    a source-region-vs-viewpoint error. That residual is stated, not fixed.
  - The leg being uninformative, which is a real and declared possible outcome and is
    not a failure of method.

LOCALITY VERIFICATION (D3, carried forward). Every coordinate is resolved against a
public gazetteer before scoring; a resolution more than VERIFY_KM from the declared
point is a CONFLATION, is logged by name, and that site is dropped from the leg with the
drop printed. Run with --verify to perform it; the scored output records whether it was
run and what it returned, so a run without it cannot be mistaken for a run with it.
"""
import csv
import hashlib
import json
import math
import os
import random
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D2B = os.path.join(HERE, "..", "work", "Dep2MzBasement_LLz.csv")
QF = os.path.join(HERE, "..", "work", "qfaults_west.geojson")
SITES = os.path.join(HERE, "..", "data", "stage5_join_summary.json")
OUT = os.path.join(HERE, "..", "data", "positive_control.json")

# ---------------------------------------------------------------------------
# THE FROZEN SET. Frozen Day 199, 2026-08-18, before any value at any of these
# coordinates was computed. Additions and removals after that point are forbidden.
# ---------------------------------------------------------------------------
CONTROLS = [
    dict(id="PC1", name="Marfa lights viewing area", state="TX",
         lat=30.2727, lon=-103.8722, grade="B",
         record="Reported since Ellison's 1883 account; continuous modern reporting; "
                "instrumented study by Texas State / SHSU physics groups 2004-2008.",
         conventional="Bunnell's programme attributed the MAJORITY of observed events to "
                      "vehicle headlights on US-67, with a documented unexplained residual. "
                      "Grade B, not A, for exactly that reason.",
         coord_basis="Official TxDOT viewing area on US-90 east of Marfa. Source region "
                     "is Mitchell Flat, 5-15 km SW -- see section 5, coordinate error."),
    dict(id="PC2", name="Toppenish Ridge / Yakama Reservation", state="WA",
         lat=46.3020, lon=-120.5510, grade="B",
         record="W.J. Vogel, fire control officer for the Yakama Nation, logged recurrent "
                "luminous phenomena 1972-1974 in an agency capacity; the log was written "
                "up independently and is the single institutional primary record here.",
         conventional="None established for the logged events.",
         coord_basis="Toppenish Ridge, the ridge line named in the reports."),
    dict(id="PC3", name="Silver Cliff cemetery", state="CO",
         lat=38.1447, lon=-105.4272, grade="C",
         record="Lay reports from the 1880s mining era onward; National Geographic "
                "feature, 1969.",
         conventional="Reflection of town and starlight off headstones is plausible and "
                      "has never been established or excluded.",
         coord_basis="The cemetery itself, which is the named locale."),
    dict(id="PC4", name="San Luis Valley (Crestone-Hooper corridor)", state="CO",
         lat=37.6500, lon=-105.8000, grade="C",
         record="Sustained regional compilation by C. O'Brien, 1990s, plus lay reports.",
         conventional="Not established. The record is regional rather than point-located, "
                      "which is itself a weakness for a 2 km-radius leg.",
         coord_basis="Valley floor midpoint of the corridor the compilation names."),
    dict(id="PC5", name="Uinta Basin / Skinwalker Ranch", state="UT",
         lat=40.2585, lon=-109.8878, grade="D",
         record="Frank Salisbury's 1974 Uinta Basin compilation is the older and cleaner "
                "record; the ranch-specific material is later.",
         conventional="Not established.",
         coord_basis="The ranch parcel named in the later material. GRADE D: the modern "
                     "record is entangled with a commercial interest, which is what the "
                     "grade rule penalises, and the site is kept only because the rule "
                     "is applied rather than the site chosen."),
    dict(id="PC6", name="Trout Lake / Mount Adams", state="WA",
         lat=46.0080, lon=-121.5250, grade="D",
         record="Recurrent reports from a single primary observer's property, 1990s on.",
         conventional="Not established.",
         coord_basis="Trout Lake valley, the named locale."),
]

# The declared controls of rounds 1 and 2, carried in for direct comparison. These are
# NOT independent positives -- that is the whole point of A6 -- and are labelled as the
# screen's own so no reader can mistake them for outside evidence.
SCREEN_CONTROLS = [
    dict(id="SC1", name="Sandia fault", state="NM", lat=35.180, lon=-106.470,
         declared="POSITIVE (round 1, from the founding hypothesis -- NOT independent)"),
    dict(id="SC2", name="Hubbell Spring fault", state="NM", lat=34.850, lon=-106.630,
         declared="NEGATIVE (round 1)"),
]

SEED = 20260818
NULL_N = 2000
GATE_KM = 25.0          # round 1's transport-screen association radius
VERIFY_KM = 25.0        # D3's conflation tolerance, unchanged
NODE_MASK_KM = 5.0      # land/coverage mask: basement grid node within this distance

# A4's 40 variants, imported by value so this file's declaration is self-contained.
K = 13
MAX_K_KM = 6.0
MIN_NODES = 3
R_FORMS = (1.0, 2.0, 3.0, 5.0)
CONSTS = [(50.0, 3000.0, 50.0, 2000.0),
          (100.0, 5000.0, 100.0, 3000.0),
          (250.0, 8000.0, 250.0, 5000.0),
          (500.0, 10000.0, 500.0, 8000.0)]
COMBOS = ("conjunctive", "additive")

BAR_II_PCTL = 0.60
BAR_II_VARIANTS = 30
TOP_THIRD = 0.667
BOTTOM_THIRD = 0.333

CELL = 0.05
SPAN = 2
R_EARTH = 6371.0


# --------------------------------------------------------------------------- maths
def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def s_min_of(d, dn, df):
    d = min(max(d, dn), df)
    return 1.0 - math.log10(d / dn) / math.log10(df / dn)


def s_con_of(c, cl, ch):
    c = min(max(c, cl), ch)
    return math.log10(c / cl) / math.log10(ch / cl)


def combine(sm, sc, how):
    return math.sqrt(sm * sc) if how == "conjunctive" else (sm + sc) / 2.0


def median(xs):
    v = sorted(xs)
    if not v:
        return None
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2.0


def boot_ci_median(xs, reps=4000, seed=SEED, lo=2.5, hi=97.5):
    """Percentile bootstrap CI on a median. Printed beside every median because n is
    single digits and a bare median at n=6 invites a reader to over-trust it."""
    if len(xs) < 2:
        return (None, None)
    rng = random.Random(seed)
    ms = []
    for _ in range(reps):
        ms.append(median([xs[rng.randrange(len(xs))] for _ in xs]))
    ms.sort()
    return (ms[int(lo / 100 * len(ms))], ms[min(len(ms) - 1, int(hi / 100 * len(ms)))])


def mannwhitney(a, b):
    """Two-sided Mann-Whitney U with tie correction, normal approximation.

    Normal approximation is stated rather than assumed correct: with n=6 the small
    sample is the control set, and the approximation's accuracy is governed by the
    SMALLER n. The p reported is therefore APPROXIMATE and is labelled so in the
    output. It is not rounded toward significance anywhere."""
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return None
    allv = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks = [0.0] * len(allv)
    i = 0
    ties = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        t = j - i + 1
        ties += t ** 3 - t
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    r1 = sum(ranks[k] for k in range(len(allv)) if allv[k][1] == 0)
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    n = n1 + n2
    mu = n1 * n2 / 2.0
    sd = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - ties / (n * (n - 1))))
    if sd == 0:
        return dict(U=u, p=1.0, note="zero variance")
    z = (u - mu + 0.5) / sd
    p = 2 * 0.5 * math.erfc(-(-abs(z)) / math.sqrt(2))
    return dict(U=round(u, 1), z=round(z, 3), p=round(min(1.0, p), 5),
                approx="normal approximation with tie and continuity correction")


def pctl_of(value, pool):
    """Fraction of the pool strictly below `value`, ties counted at half. This is the
    percentile-normalised axis A4-RESULT named as unbuilt."""
    below = sum(1 for v in pool if v < value)
    eq = sum(1 for v in pool if v == value)
    return (below + 0.5 * eq) / len(pool)


# --------------------------------------------------------------------------- grids
def stream_d2b(targets):
    want = set()
    for lat, lon in targets:
        r0, c0 = round(lat / CELL), round(lon / CELL)
        for dr in range(-SPAN, SPAN + 1):
            for dc in range(-SPAN, SPAN + 1):
                want.add((r0 + dr, c0 + dc))
    keep = defaultdict(list)
    with open(D2B, newline="") as f:
        rd = csv.reader(f)
        assert next(rd) == ["Lon_WGS84", "Lat_WGS84", "D2B_meters"]
        for row in rd:
            k = (round(float(row[1]) / CELL), round(float(row[0]) / CELL))
            if k in want:
                keep[k].append((float(row[1]), float(row[0]), float(row[2])))
    return keep


def nbrs(keep, lat, lon):
    r0, c0 = round(lat / CELL), round(lon / CELL)
    out = []
    for dr in range(-SPAN, SPAN + 1):
        for dc in range(-SPAN, SPAN + 1):
            for la, lo, v in keep.get((r0 + dr, c0 + dc), ()):
                out.append((hav(lat, lon, la, lo), v))
    out.sort()
    return out


def forms_for(nn):
    """The five neighbourhood forms of A4, from a distance-sorted neighbour list."""
    per = {}
    for R in R_FORMS:
        vs = [v for d, v in nn if d <= R]
        per[f"R{R:g}"] = vs if len(vs) >= MIN_NODES else None
    kk = nn[:K]
    per[f"k{K}"] = ([v for d, v in kk]
                    if len(kk) >= MIN_NODES and kk[-1][0] <= MAX_K_KM else None)
    return per


def score_all_variants(per):
    """40 scores (or None) keyed by variant name, from one site's five neighbourhoods."""
    out = {}
    for fname, vs in per.items():
        for ci, (dn, df, cl, ch) in enumerate(CONSTS):
            for how in COMBOS:
                key = f"{fname}|C{ci}|{how}"
                if not vs:
                    out[key] = None
                    continue
                sm = s_min_of(min(vs), dn, df)
                sc = s_con_of(max(vs) - min(vs), cl, ch)
                out[key] = combine(sm, sc, how)
    return out


# --------------------------------------------------------------------------- faults
def verts(ft):
    g = ft.get("geometry") or {}
    if g.get("type") == "LineString":
        return g["coordinates"]
    if g.get("type") == "MultiLineString":
        return [p for ln in g["coordinates"] for p in ln]
    return []


def load_normal_faults():
    """Quaternary NORMAL-sense sections only. The filter is printed with its census so a
    reader can see how many features it kept and on what field -- a silent filter that
    drops 90% of a layer is the shape of an absence manufactured by a handler."""
    fc = json.load(open(QF))
    kept, census = [], defaultdict(int)
    for ft in fc["features"]:
        p = ft.get("properties") or {}
        sense = (p.get("slip_sense") or "").strip().lower()
        census[sense or "(empty)"] += 1
        if "normal" not in sense:
            continue
        pts = [(c[1], c[0]) for c in verts(ft) if c and len(c) >= 2]
        if pts:
            kept.append((p.get("fault_name"), p.get("age"), pts))
    return kept, dict(census), len(fc["features"])


def nearest_normal(lat, lon, faults, cutoff_km=400.0):
    best = (1e18, None, None)
    for name, age, pts in faults:
        # cheap degree-box reject before the haversine loop
        if all(abs(a - lat) > 4.0 or abs(b - lon) > 5.0 for a, b in pts[:1]):
            pass
        for a, b in pts:
            if abs(a - lat) > 4.0 or abs(b - lon) > 5.0:
                continue
            d = hav(lat, lon, a, b)
            if d < best[0]:
                best = (d, name, age)
    if best[1] is None:
        return dict(dist_km=None, fault_name=None, age=None,
                    note=f"no normal-sense section within the {cutoff_km:g} km search box")
    return dict(dist_km=round(best[0], 3), fault_name=best[1], age=best[2])


# --------------------------------------------------------------------------- null
def draw_null(keep_mask_targets=None):
    """NULL_N uniform points in the grid extent, kept only if the basement grid has a
    node within NODE_MASK_KM. Uses no fault information of any kind, by construction."""
    rng = random.Random(SEED)
    cand = []
    while len(cand) < NULL_N * 4:
        lat = rng.uniform(29.0, 49.0)
        lon = rng.uniform(-124.72, -102.73)
        cand.append((round(lat, 5), round(lon, 5)))
    return cand


def sha(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()[:n]


# --------------------------------------------------------------------------- verify
def verify_localities():
    """D3's locality check against a public gazetteer. Network. Returns a per-site
    verdict; a resolution further than VERIFY_KM is a CONFLATION and drops the site."""
    import time
    import urllib.parse
    import urllib.request
    try:
        import truststore
        truststore.inject_into_ssl()
    except Exception as e:
        print(f"[warn] truststore: {e}", file=sys.stderr)
    out = {}
    for c in CONTROLS:
        q = f"{c['name'].split('(')[0].strip()}, {c['state']}, USA"
        url = ("https://nominatim.openstreetmap.org/search?"
               + urllib.parse.urlencode(dict(q=q, format="json", limit=1)))
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "place-threshold-screen/A6 (research)"})
            js = json.load(urllib.request.urlopen(req, timeout=45))
        except Exception as e:
            out[c["id"]] = dict(query=q, status="LOOKUP_FAILED", error=str(e))
            time.sleep(1.2)
            continue
        if not js:
            out[c["id"]] = dict(query=q, status="UNRESOLVED",
                                note="gazetteer returned no match; NOT scored zero")
        else:
            la, lo = float(js[0]["lat"]), float(js[0]["lon"])
            d = hav(c["lat"], c["lon"], la, lo)
            out[c["id"]] = dict(query=q, resolved=[round(la, 5), round(lo, 5)],
                                display=js[0].get("display_name"),
                                dist_km=round(d, 2),
                                status="OK" if d <= VERIFY_KM else "CONFLATION")
        time.sleep(1.2)
    return out


# --------------------------------------------------------------------------- main
def main():
    do_verify = "--verify" in sys.argv
    report = {"declared_in": os.path.basename(__file__),
              "frozen": "Day 199, 2026-08-18, before any value at any control coordinate",
              "seed": SEED, "bars": {
                  "i": "control median nearest-normal-fault distance < null median AND "
                       "Mann-Whitney two-sided p <= 0.05",
                  "ii": f"control median pooled percentile >= {BAR_II_PCTL} in >= "
                        f"{BAR_II_VARIANTS} of 40 variants"}}

    print("=" * 78)
    print("A6 -- INDEPENDENT POSITIVE CONTROL")
    print("=" * 78)

    # ---- 0. locality verification (D3) --------------------------------------
    if do_verify:
        print("\n[0] LOCALITY VERIFICATION (D3) -- gazetteer, tolerance "
              f"{VERIFY_KM:g} km\n")
        v = verify_localities()
        report["locality_verification"] = v
        for cid, r in v.items():
            nm = next(c["name"] for c in CONTROLS if c["id"] == cid)
            print(f"  {cid} {nm[:44]:44s} {r['status']:14s} "
                  f"{('%.1f km' % r['dist_km']) if r.get('dist_km') is not None else ''}")
        dropped = [k for k, r in v.items() if r["status"] == "CONFLATION"]
        if dropped:
            print(f"\n  DROPPED AS CONFLATIONS: {dropped}")
    else:
        report["locality_verification"] = "NOT RUN (--verify not passed)"
        dropped = []
        print("\n[0] LOCALITY VERIFICATION: NOT RUN. Pass --verify. Recorded as not run "
              "so this output cannot be mistaken for a verified one.")

    live = [c for c in CONTROLS if c["id"] not in dropped]

    # ---- 1. A6-i, the gate test ---------------------------------------------
    print("\n" + "=" * 78)
    print("[1] A6-i -- THE GATE TEST. Does the founding gate fire where the phenomenon")
    print("    is reported? CONTAMINATED LEG: the source literature is fault-selected.")
    print("=" * 78)

    if not os.path.exists(QF):
        print(f"\n  QFAULTS ABSENT at {QF} -- run code/fetch_qfaults_west.py first.")
        print("  A6-i is UNRUN, not negative. Recorded as such.")
        report["A6i"] = "UNRUN -- qfaults_west.geojson absent"
    else:
        faults, census, nfeat = load_normal_faults()
        print(f"\n  Qfaults west  : {nfeat} sections, sha {sha(QF)}")
        print(f"  NORMAL filter : kept {len(faults)} on `slip_sense` containing 'normal'")
        print("  slip_sense census (top 6):")
        for k, n in sorted(census.items(), key=lambda kv: -kv[1])[:6]:
            print(f"      {n:6d}  {k}")

        null_pts = draw_null()
        print(f"\n  null draw     : {len(null_pts)} candidates at seed {SEED}, "
              f"masked to grid coverage next")

        # land/coverage mask from the basement grid itself -- no fault information
        mask_keep = stream_d2b(null_pts + [(c["lat"], c["lon"]) for c in live]
                               + [(s["lat"], s["lon"]) for s in SCREEN_CONTROLS])
        null_ok = []
        for la, lo in null_pts:
            nn = nbrs(mask_keep, la, lo)
            if nn and nn[0][0] <= NODE_MASK_KM:
                null_ok.append((la, lo))
            if len(null_ok) >= NULL_N:
                break
        print(f"  null retained : {len(null_ok)} of {len(null_pts)} candidates pass the "
              f"{NODE_MASK_KM:g} km grid-coverage mask")

        cd, nd = [], []
        rows_i = []
        for c in live:
            r = nearest_normal(c["lat"], c["lon"], faults)
            rows_i.append(dict(id=c["id"], name=c["name"], grade=c["grade"], **r))
            if r["dist_km"] is not None:
                cd.append(r["dist_km"])
        for s in SCREEN_CONTROLS:
            r = nearest_normal(s["lat"], s["lon"], faults)
            rows_i.append(dict(id=s["id"], name=s["name"], grade="(screen's own)",
                               declared=s["declared"], **r))
        for la, lo in null_ok:
            r = nearest_normal(la, lo, faults)
            if r["dist_km"] is not None:
                nd.append(r["dist_km"])

        print("\n  CONTROL                                       grade   nearest normal "
              "Quaternary fault")
        for r in rows_i:
            d = f"{r['dist_km']:8.2f} km" if r["dist_km"] is not None else "     none  "
            print(f"    {r['id']} {r['name'][:38]:38s} {r['grade']:15s} {d}  "
                  f"{(r.get('fault_name') or '')[:30]}")

        mc, mn = median(cd), median(nd)
        ci = boot_ci_median(cd)
        mw = mannwhitney(cd, nd) if cd and nd else None
        print(f"\n  control median : {mc:8.2f} km   (bootstrap 95% CI "
              f"{ci[0]:.2f} - {ci[1]:.2f}, n={len(cd)})")
        print(f"  null median    : {mn:8.2f} km   (n={len(nd)})")
        if mw:
            print(f"  Mann-Whitney   : U={mw['U']}, z={mw.get('z')}, p={mw['p']}  "
                  f"({mw['approx']})")
        passed_i = bool(mw and mc is not None and mn is not None
                        and mc < mn and mw["p"] <= 0.05)
        print(f"\n  BAR i: {'SUPPORTED' if passed_i else 'NOT SUPPORTED'}")
        report["A6i"] = dict(rows=rows_i, control_median_km=mc, control_ci=ci,
                             null_median_km=mn, null_n=len(nd),
                             mannwhitney=mw, bar_passed=passed_i,
                             contamination="source literature is fault-selected; "
                                           "observer density unremoved, direction "
                                           "toward the hypothesis")

    # ---- 2. A6-ii, the leg test ---------------------------------------------
    print("\n" + "=" * 78)
    print("[2] A6-ii -- THE LEG TEST, pooled percentiles over all 40 variants.")
    print("=" * 78)

    sites = json.load(open(SITES))["survivors_ranked"]
    targets = ([(s["lat"], s["lon"]) for s in sites]
               + [(c["lat"], c["lon"]) for c in live]
               + [(s["lat"], s["lon"]) for s in SCREEN_CONTROLS])
    keep = stream_d2b(targets)

    def variants_for(lat, lon):
        return score_all_variants(forms_for(nbrs(keep, lat, lon)))

    surv_v = [variants_for(s["lat"], s["lon"]) for s in sites]
    ctrl_v = [variants_for(c["lat"], c["lon"]) for c in live]
    scrn_v = [variants_for(s["lat"], s["lon"]) for s in SCREEN_CONTROLS]

    vkeys = sorted(surv_v[0].keys())
    ctrl_p = {c["id"]: [] for c in live}
    scrn_p = {s["id"]: [] for s in SCREEN_CONTROLS}
    per_variant_ctrl_median = []

    for vk in vkeys:
        pool = [d[vk] for d in surv_v if d[vk] is not None]
        pool += [d[vk] for d in ctrl_v if d[vk] is not None]
        pool += [d[vk] for d in scrn_v if d[vk] is not None]
        if len(pool) < 20:
            per_variant_ctrl_median.append(None)
            continue
        this = []
        for c, d in zip(live, ctrl_v):
            if d[vk] is not None:
                p = pctl_of(d[vk], pool)
                ctrl_p[c["id"]].append(p)
                this.append(p)
        for s, d in zip(SCREEN_CONTROLS, scrn_v):
            if d[vk] is not None:
                scrn_p[s["id"]].append(pctl_of(d[vk], pool))
        per_variant_ctrl_median.append(median(this) if this else None)

    print("\n  SITE                                       grade  scoreable  pooled "
          "percentile")
    print("                                                    /40        med   "
          "[min - max]")
    rows_ii = []
    for c in live:
        ps = ctrl_p[c["id"]]
        if ps:
            m = median(ps)
            print(f"    {c['id']} {c['name'][:36]:36s} {c['grade']:5s}  {len(ps):3d}/40  "
                  f"   {m:.3f}  [{min(ps):.3f} - {max(ps):.3f}]")
        else:
            m = None
            print(f"    {c['id']} {c['name'][:36]:36s} {c['grade']:5s}  "
                  f"  0/40     UNSCOREABLE (third value; not scored zero)")
        rows_ii.append(dict(id=c["id"], name=c["name"], grade=c["grade"],
                            scoreable=len(ps), pctl_median=m,
                            pctl_min=min(ps) if ps else None,
                            pctl_max=max(ps) if ps else None))
    print()
    for s in SCREEN_CONTROLS:
        ps = scrn_p[s["id"]]
        if ps:
            print(f"    {s['id']} {s['name'][:36]:36s} {'own':5s}  {len(ps):3d}/40  "
                  f"   {median(ps):.3f}  [{min(ps):.3f} - {max(ps):.3f}]   "
                  f"{s['declared'][:24]}")
            rows_ii.append(dict(id=s["id"], name=s["name"], grade="(screen's own)",
                                declared=s["declared"], scoreable=len(ps),
                                pctl_median=median(ps), pctl_min=min(ps),
                                pctl_max=max(ps)))
        else:
            print(f"    {s['id']} {s['name'][:36]:36s} {'own':5s}    0/40     UNSCOREABLE")
            rows_ii.append(dict(id=s["id"], name=s["name"], grade="(screen's own)",
                                declared=s["declared"], scoreable=0, pctl_median=None))

    ok = [v for v in per_variant_ctrl_median if v is not None]
    n_pass = sum(1 for v in ok if v >= BAR_II_PCTL)
    passed_ii = n_pass >= BAR_II_VARIANTS
    print(f"\n  variants where the CONTROL SET's median percentile >= {BAR_II_PCTL}: "
          f"{n_pass} of {len(ok)}")
    print(f"  BAR ii: {'SUPPORTED' if passed_ii else 'NOT SUPPORTED'} "
          f"(needs {BAR_II_VARIANTS} of 40)")

    ab = [c for c in live if c["grade"] in ("A", "B")]
    ab_med = median([median(ctrl_p[c["id"]]) for c in ab if ctrl_p[c["id"]]])
    all_med = median([median(ctrl_p[c["id"]]) for c in live if ctrl_p[c["id"]]])
    print(f"\n  SECONDARY, pre-declared: grade A/B subset (n={len(ab)}) "
          f"median percentile = {ab_med if ab_med is None else round(ab_med, 3)}")

    # ---- 3. the crucial contrast, assigned by the rule declared in section 4 --
    sandia_ps = scrn_p.get("SC1") or []
    sandia_med = median(sandia_ps) if sandia_ps else None
    print("\n" + "=" * 78)
    print("[3] THE CRUCIAL CONTRAST -- assignment rule frozen in section 4 above.")
    print("=" * 78)
    print(f"\n  control set median percentile : "
          f"{'n/a' if all_med is None else round(all_med, 3)}")
    print(f"  Sandia median percentile      : "
          f"{'UNSCOREABLE' if sandia_med is None else round(sandia_med, 3)}")

    if all_med is None:
        verdict = "NEITHER -- no control was scoreable"
    elif all_med >= TOP_THIRD and (sandia_med is not None and sandia_med <= BOTTOM_THIRD):
        verdict = ("READING 2 gains support -- the leg discriminates, and Sandia was "
                   "never an independent outside positive")
    elif all_med <= BOTTOM_THIRD:
        verdict = ("READING 1 gains support -- the leg puts independently-attested "
                   "places in the bottom third too, so its verdict on Sandia is not "
                   "evidence about Sandia")
    else:
        verdict = ("NEITHER reading gains -- the controls neither concentrate high nor "
                   "sink low; the leg is uninformative about the phenomenon")
    print(f"\n  VERDICT: {verdict}")

    report["A6ii"] = dict(rows=rows_ii, control_median_pctl=all_med,
                          grade_AB_median_pctl=ab_med,
                          sandia_median_pctl=sandia_med,
                          variants_passing=n_pass, variants_scored=len(ok),
                          bar_passed=passed_ii, crucial_contrast=verdict,
                          percentile_note="pooled over 225 survivors + controls per "
                                          "variant; this is the percentile-normalised "
                                          "axis A4-RESULT named as not yet built")
    report["controls"] = CONTROLS
    report["screen_controls"] = SCREEN_CONTROLS
    report["unremoved_confound"] = ("observer density -- reports require observers; "
                                    "range fronts are where people are. Direction: "
                                    "TOWARD the hypothesis. Any positive here is an "
                                    "upper bound.")

    with open(OUT, "w") as f:
        json.dump(report, f, indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
