"""Five gauges on the solar-anchor calculation, each of which fails on its own evidence.

This exists because the FIRST implementation was wrong and looked fine: a hand-rolled NOAA routine
double-counted the J2000 half-day and returned "sunrise" at 23:31Z for Houston in July. Nothing in the
sample-building path would have caught that -- it produced keys, the keys were real, the anchors were
simply pointing at the wrong hour of the day. T4 (dawn/dusk vs noon) is a DIRECTIONAL prediction, so a
12-hour offset would have swapped its two arms and delivered a clean, confident, inverted result.

⚠ AND THEN THE NEGATIVE CONTROL CORRECTED THE ABOVE. Running the known-bad routine back through the
five gauges: FOUR OF FIVE PASS. Only G2 (equation-of-time bound) fires, at 729.5 min ~= the 12.16 h
offset. G1 passes because a half-day shift moves sunrise, noon and sunset TOGETHER and preserves their
order. G3 and G4 pass because day LENGTH is a difference and the offset cancels out of it. And G5 passes
at exactly 19.6 min -- so longitude was entering correctly all along, and my first reading of the failure
("the two radars landed 17 s apart, so longitude is being dropped") was WRONG. That 17 s was latitude and
declination happening to cancel in mid-July, not a missing term. Left here as written rather than
rewritten: the wrong diagnosis is the more useful record.

So this file's five gauges are ONE gauge against this fault and four decorations. They are kept because
they cover different faults, but the honest ratio is stated rather than implied by the count.

Emits L1_SOLAR_GAUGE.json, including the negative-control result. Run before trusting L1_SAMPLE.json.
"""
import datetime as dt, json, math
from build_l1_sample import RADARS, BASE_DATES, _solar_times


def _broken_d1(lat, lon, date):
    """The D1 implementation, verbatim and still broken, as a NEGATIVE CONTROL. A gauge that has only
    ever seen the good answer is untested; this is the input where right and wrong differ."""
    n = (date - dt.date(2000, 1, 1)).days + 0.5 - lon / 360.0
    M = (357.5291 + 0.98560028 * n) % 360.0
    C = 1.9148 * math.sin(math.radians(M)) + 0.0200 * math.sin(math.radians(2 * M)) \
        + 0.0003 * math.sin(math.radians(3 * M))
    lam = (M + C + 180.0 + 102.9372) % 360.0
    J = 2451545.0 + n + 0.0053 * math.sin(math.radians(M)) - 0.0069 * math.sin(math.radians(2 * lam))
    decl = math.asin(math.sin(math.radians(lam)) * math.sin(math.radians(23.4397)))
    cw = (math.sin(math.radians(-0.833)) - math.sin(math.radians(lat)) * math.sin(decl)) / \
         (math.cos(math.radians(lat)) * math.cos(decl))
    w = math.degrees(math.acos(max(-1.0, min(1.0, cw))))
    f = lambda jd: dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(days=jd - 2440587.5)
    nn = f(J)
    return nn - dt.timedelta(days=w / 360.0), nn, nn + dt.timedelta(days=w / 360.0)


def _score(fn):
    """Run the five gauges over an arbitrary solar routine. Returns {gauge: bool}."""
    r_ = {}
    order, devmax = True, 0.0
    for r, m in RADARS.items():
        for ds in BASE_DATES.values():
            d = dt.date.fromisoformat(ds)
            sr, nn, ss = fn(m["lat"], m["lon"], d)
            r_[(r, ds)] = (sr, nn, ss)
            order = order and sr < nn < ss
            mean = dt.datetime.combine(d, dt.time(12), tzinfo=dt.timezone.utc) - \
                dt.timedelta(hours=m["lon"] / 15)
            devmax = max(devmax, abs((nn - mean).total_seconds()) / 60)
    L = lambda r, ds: (r_[(r, ds)][2] - r_[(r, ds)][0]).total_seconds() / 3600
    off = (r_[("KDDC", BASE_DATES["summer"])][1] - r_[("KHGX", BASE_DATES["summer"])][1]).total_seconds() / 60
    pred = (abs(RADARS["KDDC"]["lon"]) - abs(RADARS["KHGX"]["lon"])) * 4
    return {
        "G1_ordering": order,
        "G2_equation_of_time": devmax < 20,
        "G3_seasonal": L("KHGX", BASE_DATES["summer"]) > L("KHGX", BASE_DATES["winter"]) and
                       L("KDDC", BASE_DATES["summer"]) > L("KDDC", BASE_DATES["winter"]),
        "G4_latitude_amplitude": L("KDDC", BASE_DATES["summer"]) > L("KHGX", BASE_DATES["summer"]) and
                                 L("KDDC", BASE_DATES["winter"]) < L("KHGX", BASE_DATES["winter"]),
        "G5_longitude": abs(off - pred) < 2,
        "_noon_dev_max_min": round(devmax, 1),
        "_lon_offset_min": round(off, 1),
    }

rows, res = [], {}
for r, m in RADARS.items():
    for season, ds in BASE_DATES.items():
        d = dt.date.fromisoformat(ds)
        sr, nn, ss = _solar_times(m["lat"], m["lon"], d)
        res[(r, ds)] = (sr, nn, ss)
        mean_noon = dt.datetime.combine(d, dt.time(12), tzinfo=dt.timezone.utc) - \
            dt.timedelta(hours=m["lon"] / 15)
        rows.append({
            "radar": r, "season": season, "date": ds,
            "sunrise_utc": sr.isoformat(timespec="seconds"),
            "solar_noon_utc": nn.isoformat(timespec="seconds"),
            "sunset_utc": ss.isoformat(timespec="seconds"),
            "day_length_h": round((ss - sr).total_seconds() / 3600, 3),
            "noon_dev_from_mean_solar_min": round(abs((nn - mean_noon).total_seconds()) / 60, 2),
        })

dl = lambda r, ds: (res[(r, ds)][2] - res[(r, ds)][0]).total_seconds() / 3600
lon_off = (res[("KDDC", "2025-07-16")][1] - res[("KHGX", "2025-07-16")][1]).total_seconds() / 60
lon_pred = (abs(RADARS["KDDC"]["lon"]) - abs(RADARS["KHGX"]["lon"])) * 4  # 4 min per degree

gauges = {
    "G1_ordering": {
        "claim": "sunrise < solar_noon < sunset for every radar-date",
        "pass": all(dt.datetime.fromisoformat(x["sunrise_utc"]) <
                    dt.datetime.fromisoformat(x["solar_noon_utc"]) <
                    dt.datetime.fromisoformat(x["sunset_utc"]) for x in rows),
        "kills": "the J2000 half-day error, and the UTC day-wrap that stamps a 01:21Z sunset with the "
                 "previous calendar date",
    },
    "G2_equation_of_time": {
        "claim": "|solar noon - local MEAN solar noon| < 20 min at all dates",
        "measured_max_min": max(x["noon_dev_from_mean_solar_min"] for x in rows),
        "pass": max(x["noon_dev_from_mean_solar_min"] for x in rows) < 20,
        "kills": "an arbitrary constant offset; the residual it leaves is the equation of time, which "
                 "peaks near +14 min in mid-October -- and mid-October is where the maximum lands",
    },
    "G3_seasonal": {
        "claim": "summer day length > winter day length at BOTH radars",
        "pass": dl("KHGX", "2025-07-16") > dl("KHGX", "2025-01-15") and
                dl("KDDC", "2025-07-16") > dl("KDDC", "2025-01-15"),
        "kills": "a declination sign error",
    },
    "G4_latitude_amplitude": {
        "claim": "the higher-latitude radar (KDDC 37.8N) is more extreme in BOTH directions: longer "
                 "summer day AND shorter winter day than KHGX (29.5N)",
        "pass": dl("KDDC", "2025-07-16") > dl("KHGX", "2025-07-16") and
                dl("KDDC", "2025-01-15") < dl("KHGX", "2025-01-15"),
        "kills": "latitude entering with the wrong sign or being ignored -- and unlike G3 it cannot be "
                 "satisfied by getting one season right",
    },
    "G5_longitude": {
        "claim": "UTC solar-noon offset between the two sites equals their longitude difference",
        "predicted_min": round(lon_pred, 2), "measured_min": round(lon_off, 2),
        "pass": abs(lon_off - lon_pred) < 2,
        "kills": "longitude dropped entirely. NOTE: it does NOT catch D1 -- the broken routine scores "
                 "19.6 min here too. My original tell ('the radars landed 17 s apart, so longitude is "
                 "being dropped') was a wrong diagnosis of a real symptom.",
    },
}

control = _score(_broken_d1)
caught = [k for k in gauges if not control[k]]
out = {
    "written_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "library": "astral 3.2",
    "all_pass": all(g["pass"] for g in gauges.values()),
    "negative_control": {
        "subject": "the D1 hand-rolled NOAA routine, verbatim (J2000 half-day double-counted)",
        "gauges_that_fire": caught,
        "gauges_that_pass_on_known_bad": [k for k in gauges if control[k]],
        "detection_ratio": f"{len(caught)}/5",
        "per_gauge": {k: control[k] for k in gauges},
        "diagnostics": {"noon_dev_max_min": control["_noon_dev_max_min"],
                        "lon_offset_min": control["_lon_offset_min"]},
        "reading": "ONE gauge of five is load-bearing against this fault. A half-day offset moves all "
                   "three anchors together, so G1's ordering survives it and G3/G4's day LENGTHS are "
                   "differences the offset cancels out of. The count of gauges is not the strength of "
                   "the gauge.",
        "why_it_mattered": "T4 is directional -- dawn/dusk vs noon. A 12 h offset swaps its arms and "
                           "returns a clean inverted result with no error anywhere.",
    },
    "gauges": gauges,
    "anchors": rows,
}
with open("L1_SOLAR_GAUGE.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
for k, g in gauges.items():
    print(f"{'PASS' if g['pass'] else 'FAIL'}  {k}: {g['claim']}")
print("ALL PASS:", out["all_pass"])
print(f"NEGATIVE CONTROL: {len(caught)}/5 gauges fire on the known-bad routine -> {caught}")
assert caught, "GAUGE SET IS INERT: it does not catch the fault it was written for"
