"""A12 -- JURISDICTION, FOUR CLASSES. Widening A8 from "Forest Service" to the constraint
Clayton actually stated.

Day 199: "I'm not saying we should exclude non-Forest Service sites, but what I'd say is
that it's very likely all sites will sit in either government, federal, military, or Native
land. Let's ... use the jurisdiction filter based on those four types of land."

A8 asked one question -- is this point on USFS ground -- because that is the predicate in
the Coulthart claim the project descends from. A8 stays as it is; it answers the founding
claim and nothing here supersedes it. A12 asks the wider question, and it is a DIFFERENT
question with a DIFFERENT base rate, so it gets its own null rather than borrowing A8's
interpretation.

    ! It borrows A8's null POINTS -- same SEED, same bbox derivation, same sequence -- so
      the two legs are computed on identical ground and their retentions can be subtracted.
      Sharing the draw is what makes them comparable; sharing the VERDICT would not.

THE FOUR CLASSES, mapped onto fields that exist, verified live before this file was written:

  BLM National Surface Management Agency, layer 1 (verified: type Feature Layer, polygon,
  fields include ADMIN_DEPT_CODE / ADMIN_AGENCY_CODE / ADMIN_UNIT_NAME).
    FEDERAL   ADMIN_AGENCY_CODE in the federal set (BLM FS NPS FWS BOR BIA DOE DOD ...)
    MILITARY  ADMIN_AGENCY_CODE == DOD.  A SUBSET of federal, flagged separately and never
              added to it -- Clayton's four classes overlap, and a "union" that double-counts
              DOD would inflate the retention with arithmetic rather than land.
    GOVT      state or local: ADMIN_AGENCY_CODE in the state/local set. This is the
              "government" class as distinct from "federal".
  TIGERweb AIANNHA (verified live) for the tenure boundaries, because BIA-administered
  acreage in SMA is NOT the same set as reservation land:
    TRIBAL    layer 2 Federal American Indian Reservations
              layer 3 Off-Reservation Trust Lands
              layer 4 State American Indian Reservations
              -- and NOT layers 7-10 (Oklahoma Tribal / State Designated / Tribal Designated
              Statistical Areas). Those are STATISTICAL geographies drawn for the census,
              not land tenure. Counting them as "Native land" would be a category error that
              silently doubles the class over eastern Oklahoma.

    ! CORRECTED BY THIS FILE'S OWN POSITIVE CONTROL, before the leg was run. This docstring
      first claimed: "SMA is the 'without PriUnk' service: private and unknown parcels are
      NOT in it, so an empty response means on-no-public-polygon." That is FALSE. The service
      returns ADMIN_AGENCY_CODE == 'PVT' as a feature -- the control hit it twice out of five
      points. The service name refers to what is cached/drawn, not to what the query layer
      holds. Had I not run the control, every PVT point would have landed in `unmapped` and
      the leg would have reported its single most common code as an anomaly I had to go read.
      PRIVATE is now an explicit class, and `no_public_agency` means "SMA returned nothing OR
      returned a private/unknown code" -- which is what the filter actually needs to know.

  AND THE CONTROL FOUND SOMETHING ABOUT THE SCREEN, not just about the code. The Madison
  fault -- rank 1, the only site A7 resolves to an integer position -- returns PVT here, and
  A8's cache independently returns EMPTY on the USFS administrative-boundary layer at the
  same coordinate, with three National Forests within 10 km. Two unrelated services agree
  that the screen's top site is not on federal ground at its own listed point. That is a
  result about the list, and it is why the buffered re-ask below exists.

THREE-VALUED THROUGHOUT, as A8 is. None means UNMEASURED. A network failure that reads as
"not on federal land" would delete a candidate silently, and silent deletion is the defect
this project keeps finding in itself.

DECLARED BEFORE THE FIRST QUERY -- and the first line is a PREDICTION, so it can be wrong:

  PREDICTION. The union of four classes will NOT discriminate. Federal ownership alone is
  roughly half the land area of the eleven western states, and the union adds state, local
  and tribal on top of that. I expect null retention well above 50% and a survivor-minus-null
  contrast far under the bar. Writing this here so that a high retention cannot later be
  reported as a finding.

  BAR i   DISCRIMINATES if survivor union-retention exceeds null union-retention by >= 15
          percentage points. Same bar and same points as A8, deliberately.
  BAR ii  DECISIVE for the deliverable if it removes >= 25% of the A7 contender band (the 23
          survivors within one L1 vertex of the rank-10 line). A filter that keeps everyone
          cannot break a tie.
  BAR iii If BAR i fails, the leg's useful output is NOT a filter at all but a CLASS LABEL
          per site -- which of the four, and which named unit. A label is reportable; a
          non-discriminating filter dressed as a criterion is not.

WHAT THIS IS NOT. Land status is not a physical property of a fault. The Forest Service was
drawn on the map in 1905 and the Basin and Range was not. Nothing here raises the physical
probability of anything; it establishes only whether a site is ELIGIBLE to be the place the
founding claim describes. It enters as a filter flag, never as a scoring term.
"""
import json, math, os, random, sys, time, urllib.parse, urllib.request

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

SMA = ("https://gis.blm.gov/arcgis/rest/services/lands/"
       "BLM_Natl_SMA_Cached_without_PriUnk/MapServer/1/query")
TIGER = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
         "AIANNHA/MapServer/{}/query")
TRIBAL_LAYERS = (2, 3, 4)          # tenure only; 7-10 are statistical areas, excluded above

CACHE = "work/jurisdiction4_cache.json"
SEED = 20260818                    # identical to A8 -- shares the null draw
N_NULL = 400

# Code sets, ENUMERATED FROM THE SERVICE, not guessed. `returnDistinctValues` on layer 1
# gives 33 (ADMIN_DEPT_CODE, ADMIN_AGENCY_CODE) pairs; these sets are that list, partitioned.
#
#   ! The first draft of this block WAS guessed, and it was wrong in the way that matters:
#     it had "FS" for the Forest Service. The service says USFS. Every Forest Service point
#     -- the founding claim's own class -- would have scored federal=False. The `unmapped`
#     guard would have flagged it after the fact; asking the service beforehand cost one
#     query and removed the need to be lucky. Classification is on DEPT, which partitions
#     cleanly; agency code is kept only to name the specific body.
FED_DEPTS = {"DHS", "DOC", "DOD", "DOE", "DOI", "DOJ", "DOT", "HHS", "HUD", "IA",
             "OTHFE", "USDA", "VA"}
MIL_DEPTS = {"DOD"}                       # ARMY, DOD, NAVY, USACE, USAF, USMC
GOVT_DEPTS = {"ST", "LG"}
TRIBAL_AGENCIES = {"BIA", "NTVALL", "NTVPIC"}
PRIVATE = {"PVT", "UND", ""}              # UND = undetermined; found by the control, above
NEAR_KM = 10.0      # the buffered re-ask, applied ONLY to point-misses (see below)

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def q(url, lat, lon, fields, buffer_m=0, tries=4):
    key = f"{url[-46:]}|{round(lat,5)}|{round(lon,5)}|{buffer_m}"
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
            r = json.load(urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=45))
            if "error" in r:
                raise RuntimeError(str(r["error"])[:160])
            out = [f["attributes"] for f in r.get("features", [])]
            _cache[key] = out
            return out
        except Exception as e:
            if a == tries - 1:
                _cache[key] = None       # UNMEASURED, never "not on public land"
                print(f"   ! {type(e).__name__} {str(e)[:90]}", file=sys.stderr)
                return None
            time.sleep(1.5 * (a + 1))


def attr(rec, key):
    """Case-insensitive. These services lowercase attribute names regardless of what
    outFields declared, and a plain .get('ADMIN_AGENCY_CODE') returns None on every row --
    absence manufactured by a key mismatch. A8 was bitten by exactly this."""
    if not rec:
        return None
    kl = key.lower()
    for k, v in rec.items():
        if k.lower() == kl:
            return v
    return None


def classify(lat, lon):
    sma = q(SMA, lat, lon, "ADMIN_AGENCY_CODE,ADMIN_DEPT_CODE,ADMIN_UNIT_NAME")
    trib = {}
    for lid in TRIBAL_LAYERS:
        trib[lid] = q(TIGER.format(lid), lat, lon, "NAME,BASENAME")

    code = (attr(sma[0], "ADMIN_AGENCY_CODE") or "").strip().upper() if sma else None
    unit = attr(sma[0], "ADMIN_UNIT_NAME") if sma else None
    dept = (attr(sma[0], "ADMIN_DEPT_CODE") or "").strip().upper() if sma else None

    if sma is None:
        federal = military = govt = sma_tribal = None
    else:
        federal = bool(dept and dept in FED_DEPTS)
        military = bool(dept and dept in MIL_DEPTS)
        govt = bool(dept and dept in GOVT_DEPTS)
        sma_tribal = bool(code and code in TRIBAL_AGENCIES)

    tvals = [trib[l] for l in TRIBAL_LAYERS]
    if any(t is None for t in tvals):
        tiger_tribal, tribal_name = None, None
    else:
        hit = [t for t in tvals if t]
        tiger_tribal = bool(hit)
        tribal_name = (attr(hit[0][0], "NAME") or attr(hit[0][0], "BASENAME")) if hit else None

    # TWO tribal sources, OR'd but also reported apart. BIA-administered acreage in SMA and
    # reservation/trust boundaries in TIGER are different sets -- a reservation contains fee
    # land BIA does not administer, and BIA administers parcels outside reservation lines.
    # Collapsing them to one flag would hide which source carried each site.
    if sma_tribal is None and tiger_tribal is None:
        tribal = None
    else:
        tribal = bool(sma_tribal) or bool(tiger_tribal)

    parts = [federal, military, govt, tribal]
    if any(p is None for p in parts):
        union = None if all(p in (None, False) for p in parts) else True
        # True short-circuits: a confirmed hit on ANY class makes the union true even if
        # another class is unmeasured. Only an all-miss-with-an-unknown is genuinely unknown.
    else:
        union = any(parts)

    # THE BUFFERED RE-ASK, and it is asymmetric ON PURPOSE: it runs only where the point
    # query MISSED. A fault node is a vertex on a mapped trace; the "site" is the structure.
    # Madison (rank 1) sits on private ground with three National Forests inside 10 km, so a
    # point-only answer deletes candidates for a cartographic accident. Reported as its own
    # field -- NEVER merged into `union`, because "on federal land" and "within 10 km of
    # federal land" are different claims and merging them would launder the weaker one.
    near_code = near_union = None
    if union is False:
        n = q(SMA, lat, lon, "ADMIN_AGENCY_CODE,ADMIN_UNIT_NAME",
              buffer_m=int(NEAR_KM * 1000))
        if n is not None:
            codes = {(attr(f, "ADMIN_AGENCY_CODE") or "").strip().upper() for f in n}
            codes = {c for c in codes if c and c not in PRIVATE}
            near_code = sorted(codes) or None
            near_union = bool(codes)

    is_private = bool(code and code in PRIVATE)
    mapped = FED_DEPTS | GOVT_DEPTS | PRIVATE
    return dict(agency_code=code or None, dept_code=dept or None, unit_name=unit,
                federal=federal, military=military, govt=govt, tribal=tribal,
                tribal_sma=sma_tribal, tribal_tiger=tiger_tribal,
                tribal_name=tribal_name, union=union,
                near10_union=near_union, near10_codes=near_code,
                private=is_private,
                unmapped=(f"{dept}/{code}" if (sma and dept and dept not in mapped)
                          else None),
                no_public_agency=(sma is not None and (sma == [] or is_private)))


def save():
    json.dump(_cache, open(CACHE, "w"))


def frac(rs, k):
    m = [r for r in rs if r.get(k) is not None]
    return (round(sum(1 for r in m if r[k]) / len(m), 4) if m else None,
            len(m), len(rs) - len(m))


if __name__ == "__main__":
    surv = json.load(open("data/stage5_join_summary.json"))["survivors_ranked"]
    band = json.load(open("data/rank_resolution.json"))["A7v_contender_band"]["members"]
    band_names = {b["fault"] for b in band}

    print(f"[A12] {len(surv)} survivors x 4 layers", file=sys.stderr)
    rows = []
    for i, s in enumerate(surv, 1):
        rows.append(dict(fault=s["fault_name"], lat=s["lat"], lon=s["lon"],
                         rank=s["rank"], score=s["score"], **classify(s["lat"], s["lon"])))
        if i % 25 == 0:
            print(f"   {i}/{len(surv)}", file=sys.stderr); save()
    save()

    # ---- null: A8's draw, reproduced exactly (same seed, same bbox derivation, same order)
    lats = [s["lat"] for s in surv]; lons = [s["lon"] for s in surv]
    bbox = (min(lats), max(lats), min(lons), max(lons))
    rnd = random.Random(SEED)
    print(f"[A12] null {N_NULL} pts in bbox {tuple(round(b,2) for b in bbox)} "
          f"(A8's draw, reproduced)", file=sys.stderr)
    null = []
    for i in range(N_NULL):
        la = rnd.uniform(bbox[0], bbox[1]); lo = rnd.uniform(bbox[2], bbox[3])
        null.append(dict(lat=round(la, 4), lon=round(lo, 4), **classify(la, lo)))
        if i % 50 == 0:
            print(f"   null {i}/{N_NULL}", file=sys.stderr); save()
    save()

    out = dict(leg="A12 jurisdiction, four classes",
               frozen="Day 199, 2026-08-18; classes, layer ids, exclusions, prediction and "
                      "bars all in jurisdiction4_leg.py docstring before the first query",
               seed=SEED, n_null=N_NULL, bbox=[round(b, 4) for b in bbox],
               null_shared_with="A8 jurisdiction_leg.py (same seed, bbox, sequence)",
               survivors=rows, null=null)

    stats = {}
    for k in ("federal", "military", "govt", "tribal", "union", "private", "near10_union"):
        s_f, s_n, s_miss = frac(rows, k)
        n_f, n_n, n_miss = frac(null, k)
        stats[k] = dict(survivor=s_f, survivor_measured=s_n, survivor_unmeasured=s_miss,
                        null=n_f, null_measured=n_n, null_unmeasured=n_miss,
                        contrast_pp=(round((s_f - n_f) * 100, 2)
                                     if (s_f is not None and n_f is not None) else None))
        print(f"   {k:9s} survivors={s_f}  null={n_f}  "
              f"contrast={stats[k]['contrast_pp']} pp", file=sys.stderr)

    band_rows = [r for r in rows if r["fault"] in band_names]
    removed = [r["fault"] for r in band_rows if r["union"] is False]
    unmeasured_band = [r["fault"] for r in band_rows if r["union"] is None]
    bar_i = (stats["union"]["contrast_pp"] is not None
             and stats["union"]["contrast_pp"] >= 15.0)
    bar_ii = (len(removed) / len(band_rows) >= 0.25) if band_rows else False
    out["stats"] = stats
    out["band"] = dict(n=len(band_rows), removed=removed, n_removed=len(removed),
                       unmeasured=unmeasured_band,
                       frac_removed=(round(len(removed) / len(band_rows), 4)
                                     if band_rows else None))
    out["bars"] = dict(i_discriminates=bar_i, ii_decisive=bar_ii,
                       iii_fallback_is_class_label=(not bar_i))
    unmapped = sorted({r["unmapped"] for r in rows + null if r.get("unmapped")})
    out["unmapped_agency_codes"] = unmapped
    if unmapped:
        print(f"[A12] ! agency codes I did not map: {unmapped} -- these were counted as "
              f"NEITHER federal nor govt and must be read before this leg is cited",
              file=sys.stderr)
    print(f"[A12] BAR i discriminates={bar_i} | BAR ii decisive={bar_ii} "
          f"({len(removed)}/{len(band_rows)} of band removed)", file=sys.stderr)

    json.dump(out, open("data/jurisdiction4_leg.json", "w"), indent=1)
    print("[A12] wrote data/jurisdiction4_leg.json", file=sys.stderr)
