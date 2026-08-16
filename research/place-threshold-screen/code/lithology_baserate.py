"""BASE RATE for the piezo layer -- "is quartz-rich rock near this pin UNUSUAL?"

Tonight's lithology probe (work/lithology_probe.py, run against Macrostrat's geologic
map rather than the Bouguer density proxy) reported quartz-rich crystalline rock within
0-5 km at four classic anomaly sites (Hessdalen, Brown Mountain, Marfa, Piedmont MO)
and at 10 km at the Hubbell Spring PIN. That looks like a convergence.

It is not a result until it has a denominator. "Granite within 5 km" may simply be what
the western United States looks like. The lesson board's own row, pushed this morning:
repeated output across independent units is a SHARED CAUSE, not agreement.

So: draw random land points in the western CONUS, run the IDENTICAL instrument, and
report the percentile the pins sit at. A convergence that is at the 50th percentile is
a fact about the continent, not about the sites.

CAVEATS, stated before the number:
  - Uniform lat/lon sampling is not equal-area. Over 31-49N the cos(lat) weight varies
    by ~1.4x; points at the north are slightly over-weighted. Recorded, not corrected.
  - The anomaly sites were NOT drawn from this population. They were selected by other
    people for having lights. Any percentile here is descriptive, not a hypothesis test.
  - Macrostrat coverage varies by state; an UNMEASURED probe is counted and reported.
"""
import json, os, random, sys, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lithology_probe import nearest_quartz_rich, _save      # noqa: E402

random.seed(20260815)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
OUT = "work/lithology_baserate.json"

# western CONUS box; ocean/no-map points return no unit and are counted as MISS-nodata
LAT = (31.0, 49.0)
LON = (-124.5, -100.0)

SITES = {
    "Hubbell Spring PIN": (34.90, -106.53),
    "Sandia W scarp": (35.10, -106.51),
    "Tijeras CONTROL": (35.06, -106.36),
    "Socorro": (34.06, -106.90),
    "Toppenish Ridge WA (known FAIL)": (46.350, -120.550),
    "Marfa TX": (30.240, -104.050),
}


def score(r):
    """Nearest ring (km) at which PLUTONIC or FABRIC appears; None if neither <=40 km."""
    hits = [r["nearest"][t]["ring_km"] for t in ("TIER_PLUTONIC", "TIER_FABRIC")
            if t in r["nearest"]]
    return min(hits) if hits else None


def main():
    rows = []
    for i in range(N):
        la = random.uniform(*LAT)
        lo = random.uniform(*LON)
        r = nearest_quartz_rich(la, lo)
        d = score(r)
        rows.append({"lat": round(la, 4), "lon": round(lo, 4), "nearest_km": d,
                     "at_point": r["at_point_tier"],
                     "unmeasured_probes": r["unmeasured_probes"],
                     "probes": r["probes"]})
        print(f"[{i+1}/{N}] {la:7.3f} {lo:9.3f}  nearest="
              f"{'none>40' if d is None else f'{d:5.1f} km'}  "
              f"unmeasured={r['unmeasured_probes']}/{r['probes']}")
        sys.stdout.flush()
        _save()

    got = [r["nearest_km"] for r in rows if r["nearest_km"] is not None]
    n = len(rows)
    frac = lambda k: sum(1 for r in rows if r["nearest_km"] is not None
                         and r["nearest_km"] <= k) / n
    summary = {
        "n_random_points": n,
        "box": {"lat": LAT, "lon": LON},
        "frac_quartz_rich_within": {f"{k}km": round(frac(k), 3)
                                    for k in (0, 2, 5, 10, 15, 25, 40)},
        "frac_none_within_40km": round(1 - frac(40), 3),
        "median_nearest_km_where_found": (sorted(got)[len(got)//2] if got else None),
        "total_unmeasured_probes": sum(r["unmeasured_probes"] for r in rows),
        "total_probes": sum(r["probes"] for r in rows),
    }
    site_rows = {}
    for tag, (la, lo) in SITES.items():
        d = score(nearest_quartz_rich(la, lo))
        pct = (None if d is None else
               round(100.0 * sum(1 for r in rows if r["nearest_km"] is not None
                                 and r["nearest_km"] < d) / n, 1))
        site_rows[tag] = {"nearest_km": d,
                          "pct_of_random_points_CLOSER_than_this": pct}
    out = {"summary": summary, "sites": site_rows, "random_points": rows}
    json.dump(out, open(OUT, "w"), indent=1)
    print("\n" + json.dumps({"summary": summary, "sites": site_rows}, indent=1))


if __name__ == "__main__":
    main()
