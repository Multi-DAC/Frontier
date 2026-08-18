"""A8 -- THE FOUNDING CONSTRAINT, applied for the first time.

Coulthart's claim, which is the statement this entire project descends from, carries a
JURISDICTIONAL predicate we have never once used: the alleged site is in the continental US
and it is in a FOREST SERVICE controlled area. Ten reports in, the screen has been purely
geophysical -- age, dilatancy, quartz, junction density, length, basement. Land status has
never entered it. So the top ten has been answering a slightly different question than the
one that was asked.

WHAT THIS LEG IS AND IS NOT
  It is NOT evidence about portals. Land status is not a physical property of a fault; the
  US Forest Service was drawn on the map in 1905 and the Basin and Range was not. A site
  being on National Forest land raises no physical probability of anything.
  It IS the constraint the founding claim states. If the claim is about a place under FS
  jurisdiction, then a candidate list that ignores jurisdiction is a list of answers to a
  question nobody asked.

  So it enters as a FILTER on an already-physics-ranked list, never as a scoring term. A
  site is not more portal-like for being in a National Forest. It is merely eligible to be
  the site Coulthart described.

TWO LAYERS, because they mean different things and the difference matters here:
  ADMIN  EDW_ForestSystemBoundaries_01/0 -- Administrative Forest Boundaries. The proclaimed
         unit. INCLUDES private inholdings, state parcels and patented mining claims. This is
         what "in the Gallatin National Forest" colloquially means, and it is the looser read.
  OWN    EDW_BasicOwnership_01/0 -- surface ownership. Answers "is this specific ground
         federally owned and USFS-administered", which is the stricter read and the one that
         matches "forest service CONTROLLED".
  A site inside ADMIN but not OWN is inside a National Forest on the map and on somebody
  else's deed. Reported separately; never silently merged.

THE CONFOUND, declared before the numbers exist. National Forest land is disproportionately
mountainous public land, and Quaternary range-front normal faults are disproportionately in
mountains. The filter is therefore CORRELATED WITH THE SCREEN'S OWN CRITERION, in the
direction that flatters it. A high retention rate among survivors would prove nothing on its
own. So the leg computes a NULL: the same two queries against 400 random points drawn from
the same CONUS-west bounding region as the survivor population. The number that means
anything is the CONTRAST, not the retention.

DECLARED BEFORE THE FIRST QUERY:
  BAR i  The filter DISCRIMINATES if survivor ADMIN retention exceeds the null's by >= 15
         percentage points. If it does not, the filter is close to a no-op dressed as a
         criterion and must be reported as one.
  BAR ii The filter is DECISIVE for the deliverable if it removes >= 25% of the A7 contender
         band (the 23 survivors within one vertex of rank 10). A filter that keeps everyone
         cannot break a tie, and breaking that tie is the whole reason to run it.

  Bar i failing does NOT invalidate the filter -- the constraint is still what Coulthart
  stated, and a non-discriminating constraint is still a constraint. It only means the
  filter cannot be presented as though it found something.
"""
import json, math, os, random, sys, time, urllib.parse, urllib.request

try:
    import truststore; truststore.inject_into_ssl()
except Exception:
    pass

ADMIN = ("https://apps.fs.usda.gov/arcx/rest/services/EDW/"
         "EDW_ForestSystemBoundaries_01/MapServer/0/query")
OWN = ("https://apps.fs.usda.gov/arcx/rest/services/EDW/"
       "EDW_BasicOwnership_01/MapServer/0/query")
CACHE = "work/jurisdiction_cache.json"
SEED = 20260818
N_NULL = 400
NEAR_KM = 10.0

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def q(url, lat, lon, fields, buffer_m=0, tries=4):
    key = f"{url[-40:]}|{round(lat,5)}|{round(lon,5)}|{buffer_m}"
    if key in _cache:
        return _cache[key]
    p = dict(f="json", geometry=json.dumps({"x": lon, "y": lat,
                                            "spatialReference": {"wkid": 4326}}),
             geometryType="esriGeometryPoint", inSR="4326",
             spatialRel="esriSpatialRelIntersects", outFields=fields,
             returnGeometry="false")
    if buffer_m:
        p["distance"] = str(buffer_m)
        p["units"] = "esriSRUnit_Meter"
    u = url + "?" + urllib.parse.urlencode(p)
    for a in range(tries):
        try:
            r = json.load(urllib.request.urlopen(u, timeout=45))
            if "error" in r:
                raise RuntimeError(str(r["error"])[:160])
            out = [f["attributes"] for f in r.get("features", [])]
            _cache[key] = out
            return out
        except Exception as e:
            if a == tries - 1:
                _cache[key] = None          # NULL means UNMEASURED, never "not in a forest"
                print(f"   ! {type(e).__name__} {str(e)[:90]}", file=sys.stderr)
                return None
            time.sleep(1.5 * (a + 1))


def attr(rec, key):
    """The EDW services return attribute names LOWERCASED ('forestname'), not as declared in
    outFields ('FORESTNAME'). A plain .get('FORESTNAME') returns None on every row, which
    reads as 'this forest has no name' rather than 'I asked for the wrong key' -- absence
    manufactured by a key mismatch. Match case-insensitively and be done with it."""
    if not rec:
        return None
    kl = key.lower()
    for k, v in rec.items():
        if k.lower() == kl:
            return v
    return None


def classify(lat, lon):
    """Three-valued on purpose. None is UNMEASURED and must never be counted as absent --
    a network death that reads as 'not on Forest Service land' would silently delete
    candidates, and deletion is the failure mode this project keeps finding in itself."""
    a = q(ADMIN, lat, lon, "FORESTNAME,REGION")
    o = q(OWN, lat, lon, "OWNERCLASSIFICATION,FORESTNAME")
    near = None
    if a == []:
        near = q(ADMIN, lat, lon, "FORESTNAME,REGION", buffer_m=int(NEAR_KM * 1000))
    return dict(
        admin=(None if a is None else bool(a)),
        admin_forest=(attr(a[0], "FORESTNAME") if a else None),
        own=(None if o is None else bool(o)),
        own_class=(attr(o[0], "OWNERCLASSIFICATION") if o else None),
        own_forest=(attr(o[0], "FORESTNAME") if o else None),
        near10=(None if near is None else bool(near)),
        near10_forest=(attr(near[0], "FORESTNAME") if near else None))


def save():
    json.dump(_cache, open(CACHE, "w"))


if __name__ == "__main__":
    surv = json.load(open("data/stage5_join_summary.json"))["survivors_ranked"]
    frozen = json.load(open("data/top10_frozen.json"))["sites"]
    band = json.load(open("data/rank_resolution.json"))["A7v_contender_band"]["members"]
    band_names = {b["fault"] for b in band}

    print(f"[A8] {len(surv)} survivors x 2 layers", file=sys.stderr)
    rows = []
    for i, s in enumerate(surv, 1):
        c = classify(s["lat"], s["lon"])
        rows.append(dict(fault=s["fault_name"], lat=s["lat"], lon=s["lon"],
                         rank=s["rank"], score=s["score"], **c))
        if i % 25 == 0:
            print(f"   {i}/{len(surv)}", file=sys.stderr); save()
    save()

    # ---- null: same bbox as the survivor population, same two queries
    lats = [s["lat"] for s in surv]; lons = [s["lon"] for s in surv]
    bbox = (min(lats), max(lats), min(lons), max(lons))
    rnd = random.Random(SEED)
    print(f"[A8] null {N_NULL} pts in bbox {tuple(round(b,2) for b in bbox)}", file=sys.stderr)
    null = []
    for i in range(N_NULL):
        la = rnd.uniform(bbox[0], bbox[1]); lo = rnd.uniform(bbox[2], bbox[3])
        c = classify(la, lo)
        null.append(dict(lat=round(la, 4), lon=round(lo, 4), **c))
        if i % 50 == 0:
            print(f"   null {i}/{N_NULL}", file=sys.stderr); save()
    save()

    def frac(rs, k):
        m = [r for r in rs if r[k] is not None]
        return (round(sum(1 for r in m if r[k]) / len(m), 4) if m else None,
                len(m), len(rs) - len(m))

    s_admin, s_n, s_miss = frac(rows, "admin")
    s_own, _, _ = frac(rows, "own")
    n_admin, n_n, n_miss = frac(null, "admin")
    n_own, _, _ = frac(null, "own")

    band_rows = [r for r in rows if r["fault"] in band_names]
    band_out = [r for r in band_rows if r["admin"] is False]
    top10 = [r for r in rows if r["fault"] in {f["fault"] for f in frozen}]

    bar_i = (s_admin is not None and n_admin is not None
             and (s_admin - n_admin) >= 0.15)
    bar_ii = (len(band_rows) > 0 and len(band_out) / len(band_rows) >= 0.25)

    out = dict(
        leg="A8 jurisdiction (the founding constraint)",
        frozen="Day 199, 2026-08-18, bars declared in jurisdiction_leg.py before first query",
        seed=SEED,
        layers=dict(admin=ADMIN, own=OWN),
        survivors=dict(n=len(rows), measured=s_n, unmeasured=s_miss,
                       admin_frac=s_admin, own_frac=s_own),
        null=dict(n=len(null), measured=n_n, unmeasured=n_miss, bbox=bbox,
                  admin_frac=n_admin, own_frac=n_own),
        contrast_admin_pp=(None if None in (s_admin, n_admin)
                           else round((s_admin - n_admin) * 100, 1)),
        contender_band=dict(n=len(band_rows), removed_by_admin=len(band_out),
                            removed=[r["fault"] for r in band_out]),
        top10=[dict(fault=r["fault"], admin=r["admin"], forest=r["admin_forest"],
                    own=r["own"], own_class=r["own_class"],
                    near10=r["near10"], near10_forest=r["near10_forest"]) for r in top10],
        rows=rows, null_rows=null,
        bars=dict(i_discriminates=bar_i, ii_decisive_for_band=bar_ii),
        confound="National Forest land is mountainous public land; Quaternary range-front "
                 "normal faults are mountainous. Correlation is toward the hypothesis and is "
                 "the reason the null exists.",
    )
    json.dump(out, open("data/jurisdiction_leg.json", "w"), indent=1)

    print(f"\n survivors on ADMIN forest : {s_admin}  (n={s_n}, unmeasured={s_miss})",
          file=sys.stderr)
    print(f" null      on ADMIN forest : {n_admin}  (n={n_n}, unmeasured={n_miss})",
          file=sys.stderr)
    print(f" contrast                  : {out['contrast_admin_pp']} pp", file=sys.stderr)
    print(f" survivors USFS-OWNED      : {s_own}   null: {n_own}", file=sys.stderr)
    print(f"\n contender band {len(band_rows)} -> removed by ADMIN: {len(band_out)}",
          file=sys.stderr)
    print("\n FROZEN TEN:", file=sys.stderr)
    for r in out["top10"]:
        tag = ("IN  " + str(r["forest"]) if r["admin"] else
               ("near " + str(r["near10_forest"]) if r["near10"] else "OUT"))
        print(f"   {r['fault']:34s} {tag:44s} owned={r['own']} {r['own_class'] or ''}",
              file=sys.stderr)
    print(f"\nBARS  i={bar_i}  ii={bar_ii}", file=sys.stderr)
