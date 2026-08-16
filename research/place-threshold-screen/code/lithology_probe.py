"""Nearest mapped quartz-rich rock, from a geologic map -- not from a density proxy.

This pays the debt named in §6.1 of the D196 dossier and carried unpaid since D137:

    "The granite proxy is density, not lithology. Both surveys call 'granite' = densest
     Bouguer quartile ... This could flip Finding B on its own."

Source: Macrostrat /geologic_units/map (global compilation; in CONUS it serves the USGS
state geologic map compilation, elsewhere coarser continental maps -- the returned
`source_id`/scale is recorded per hit so the coverage grade travels with the number).

METHOD. A single point query answers "what is under this pin", which is NOT the question:
the pin was deliberately placed in a basin low, so of course it returns basin fill. The
question is "how far to the nearest quartz-rich crystalline outcrop", so this samples a
polar grid (rings x azimuths) and returns the nearest ring on which one appears. The
answer is therefore quantized to the ring spacing and that is stated in the output.

⚠ PHYSICS CAVEAT, recorded here because the layer is named "piezo" and the name flatters
it: alpha-quartz is piezoelectric as a CRYSTAL. In an isotropic polycrystalline granite
the individual moments are randomly oriented and the bulk piezoelectric tensor averages
toward zero. A macroscopic piezo response needs preferred crystallographic orientation --
which strongly foliated/tectonized quartzite can have and an equigranular pluton largely
does not. So "granite nearby" is a WEAKER proxy for a piezo source than either survey has
treated it as, independent of how well it is measured. Tiers below are reported separately
for exactly this reason: TIER_FABRIC (aligned) is not the same claim as TIER_PLUTONIC.
"""
import json, math, os, sys, time, urllib.request, urllib.parse
try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

CACHE_PATH = "work/macrostrat_cache.json"
API = "https://macrostrat.org/api/v2/geologic_units/map"
R = 6371.0

TIER_PLUTONIC = ("granite", "granodiorite", "quartz monzonite", "monzogranite",
                 "syenogranite", "tonalite", "trondhjemite", "pegmatite", "aplite",
                 "alaskite", "granophyre", "granitoid", "quartz diorite")
TIER_FABRIC = ("quartzite", "gneiss", "quartz-mica schist", "mica schist", "schist",
               "metaquartzite", "granitic gneiss", "orthogneiss", "migmatite")
TIER_VOLCANIC = ("rhyolite", "dacite", "quartz latite", "ignimbrite", "welded tuff",
                 "rhyolitic tuff")
NEGATIVE = ("alluvium", "sedimentary", "sandstone", "shale", "limestone", "dolostone",
            "basalt", "gabbro", "ophiolite", "meta-basalt", "greenschist", "chert")

_cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}
_dirty = False


def _save():
    global _dirty
    if _dirty:
        json.dump(_cache, open(CACHE_PATH, "w"))
        _dirty = False


def unit_at(lat, lon, pause=0.12):
    """Cached Macrostrat point query. Returns list of unit dicts (may be empty)."""
    global _dirty
    k = f"{lat:.4f},{lon:.4f}"
    if k in _cache:
        return _cache[k]
    url = f"{API}?" + urllib.parse.urlencode({"lat": f"{lat:.4f}", "lng": f"{lon:.4f}"})
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=60))
        recs = d.get("success", {}).get("data", []) or []
    except Exception as e:
        print(f"[warn] macrostrat {k}: {e}", file=sys.stderr)
        return None                      # None = UNMEASURED, distinct from [] = no unit
    out = [{"name": r.get("name"), "lith": r.get("lith"), "b_age": r.get("b_age"),
            "t_age": r.get("t_age"), "source_id": r.get("source_id"),
            "scale": r.get("scale"), "map_id": r.get("map_id")} for r in recs]
    _cache[k] = out
    _dirty = True
    time.sleep(pause)
    return out


def classify(units):
    """Highest tier present in a unit list. Returns (tier, matched_term, unit_name)."""
    if units is None:
        return ("UNMEASURED", None, None)
    for tier, terms in (("TIER_PLUTONIC", TIER_PLUTONIC),
                        ("TIER_FABRIC", TIER_FABRIC),
                        ("TIER_VOLCANIC", TIER_VOLCANIC)):
        for u in units:
            blob = f"{u.get('lith') or ''} {u.get('name') or ''}".lower()
            for t in terms:
                if t in blob:
                    return (tier, t, u.get("name"))
    return ("NONE", None, units[0].get("name") if units else None)


def offset(lat, lon, az_deg, d_km):
    az = math.radians(az_deg)
    dn = d_km*math.cos(az); de = d_km*math.sin(az)
    return lat + dn/110.574, lon + de/(111.320*math.cos(math.radians(lat)))


RINGS = (0.0, 2.0, 5.0, 10.0, 15.0, 25.0, 40.0)
AZIMUTHS = tuple(range(0, 360, 45))


def nearest_quartz_rich(lat, lon, rings=RINGS, azimuths=AZIMUTHS):
    """Nearest ring at which a quartz-rich unit appears, per tier."""
    found = {}
    at_point = classify(unit_at(lat, lon))
    probed = 0
    unmeasured = 0
    for r in rings:
        azs = [0] if r == 0.0 else azimuths
        for az in azs:
            la, lo = offset(lat, lon, az, r) if r else (lat, lon)
            u = unit_at(la, lo)
            probed += 1
            if u is None:
                unmeasured += 1
                continue
            tier, term, nm = classify(u)
            if tier in ("TIER_PLUTONIC", "TIER_FABRIC", "TIER_VOLCANIC") and tier not in found:
                found[tier] = {"ring_km": r, "azimuth": az, "term": term, "unit": nm}
        if len(found) == 3:
            break
    _save()
    return {"at_point_tier": at_point[0], "at_point_unit": at_point[2],
            "at_point_term": at_point[1],
            "nearest": found, "ring_quantization_km": list(rings),
            "probes": probed, "unmeasured_probes": unmeasured,
            "max_search_radius_km": max(rings)}


if __name__ == "__main__":
    for tag, la, lo in (("Hubbell Spring PIN", 34.90, -106.53),
                        ("Sandia W scarp", 35.10, -106.51),
                        ("Tijeras CONTROL", 35.06, -106.36),
                        ("Socorro", 34.06, -106.90),
                        ("Hessdalen NORWAY", 62.783, 11.200),
                        ("Piedmont MO", 37.155, -90.696),
                        ("Toppenish Ridge WA", 46.350, -120.550),
                        ("Marfa TX", 30.240, -104.050),
                        ("Brown Mountain NC", 35.900, -81.790)):
        r = nearest_quartz_rich(la, lo)
        print(f"{tag:<22} at_point={r['at_point_tier']:<14} "
              f"({(r['at_point_unit'] or '')[:34]})")
        for t in ("TIER_PLUTONIC", "TIER_FABRIC", "TIER_VOLCANIC"):
            h = r["nearest"].get(t)
            print(f"     {t:<14} " + (f"{h['ring_km']:>5.1f} km  {h['term']:<18} "
                                      f"{(h['unit'] or '')[:38]}" if h else "  none within 40 km"))
        sys.stdout.flush()
