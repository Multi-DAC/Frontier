"""Build L1_SAMPLE.json — the NEXRAD CFP sample, PINNED TO EXACT S3 KEYS, before any scan is read.

Governed by PREREG-TERRESTRIAL.md §1.3 and §3.1.

What this script is allowed to touch, and what it is not:
  ALLOWED   - the S3 *listing* API (keys, sizes, mtimes). A key name carries a timestamp and a byte
              count and nothing else; no moment data is read here.
  FORBIDDEN - GET on any object. Not one byte of a volume scan is fetched by this file.

Selection rule is deterministic and written before the listing is consulted:
  For each radar x date, compute local sunrise / solar noon / sunset (astral 3.2, no network), then take,
  for each of those three anchors, the FIRST volume scan starting at or after the anchor and the NEXT one
  after it. 3 anchors x 2 = 6 volume scans per radar-date, which is the prereg's count.

TWO INSTRUMENT DEFECTS, both caught before any moment data was read, both recorded because T5 says a
pass reporting no instrument trouble has probably missed some:
  D1  My hand-rolled NOAA solar routine double-counted the J2000 half-day: it returned "sunrise" at
      23:31Z for Houston in July (true 11:31Z). Replaced with astral, validated against five gauges in
      solar_gauge.py. ⚠ The negative control there corrects my own first diagnosis: I read the two radars
      landing 17 s apart as "longitude is being dropped", and it was not -- the broken routine scores the
      longitude gauge at exactly the right 19.6 min. Four of the five gauges PASS on the known-bad
      routine; only the equation-of-time bound fires. See L1_SOLAR_GAUGE.json["negative_control"].
  D2  Every US sunset falls on the NEXT UTC day, so a single-day listing returns nothing at or after the
      sunset anchor -- silently, as an empty pick rather than an error. The dusk half of T4, the whole
      point of the prediction, would have been dropped with no message. Listings are now pooled over
      date-1 / date / date+1.

AMENDMENT, recorded rather than performed silently (see L1_SAMPLE.json["amendments"]):
  PREREG-TERRESTRIAL.md §1.3 fixes the sample at 2 radars x 6 scans x 4 dates = 48, and separately T2
  requires "two scans 30 days apart, same radar and elevation". Those 48 contain no 30-day pair. The
  partner scans were implied by T2 and not counted by the sample line. This script adds 8 of them
  (2 radars x 4 dates x 1 solar-noon-anchored scan at date+30d) and labels them `role: "t2_partner"`.
  The primary sample is unchanged at 48.
"""
import json, re, sys, datetime as dt
import requests
from astral import Observer
from astral.sun import sunrise as _sunrise, sunset as _sunset, noon as _noon

BUCKET = "unidata-nexrad-level2"          # NOT noaa-nexrad-level2; that one stopped growing 2025-09-01
LIST_URL = f"https://{BUCKET}.s3.amazonaws.com/"

# Site coordinates are ASSERTED here and VERIFIED LATER against each decoded file's own header.
# Any mismatch is recorded as a defect, not quietly corrected. (radar_coords_verified: false)
RADARS = {
    "KHGX": {"lat": 29.4719, "lon": -95.0792, "elev_m": 5,    "contrast": "coastal",  "site": "Houston/Galveston, TX"},
    "KDDC": {"lat": 37.7608, "lon": -99.9688, "elev_m": 789,  "contrast": "interior", "site": "Dodge City, KS"},
}

# One per season, drawn across 2024-2025. Each gets a +30d partner for T2.
BASE_DATES = {
    "autumn": "2024-10-16",
    "winter": "2025-01-15",
    "spring": "2025-04-16",
    "summer": "2025-07-16",
}

ELEVATION_CUT_DEG = 0.5   # lowest split cut; the one that sees ground clutter and near-field biology

KEY_RE = re.compile(r"([A-Z]{4})(\d{8})_(\d{6})(_V06)?$")


# ---------------------------------------------------------------- solar geometry (astral, validated)
def _solar_times(lat, lon, date):
    """(sunrise, solar_noon, sunset) as UTC datetimes, day-wrap corrected -- see D2 in the header.

    astral stamps a post-midnight-UTC sunset with the SAME calendar date, which reads as a sunset
    BEFORE its own sunrise. Unwrapped here so the ordering gauge means what it says."""
    o = Observer(lat, lon, 0)
    sr, nn, ss = _sunrise(o, date), _noon(o, date), _sunset(o, date)
    if ss < nn:
        ss += dt.timedelta(days=1)
    if sr > nn:
        sr -= dt.timedelta(days=1)
    assert sr < nn < ss, f"solar ordering violated for {lat},{lon} on {date}"
    return sr, nn, ss


# ---------------------------------------------------------------- listing only
def list_day(radar, date):
    """List every volume-scan key for one radar-day. LISTING ONLY - no object is fetched."""
    out, token = [], None
    prefix = f"{date:%Y/%m/%d}/{radar}/"
    while True:
        params = {"list-type": "2", "prefix": prefix, "max-keys": "1000"}
        if token:
            params["continuation-token"] = token
        body = _get(LIST_URL, params=params).text
        for m in re.finditer(r"<Contents>(.*?)</Contents>", body, re.S):
            blob = m.group(1)
            key = re.search(r"<Key>(.*?)</Key>", blob).group(1)
            size = int(re.search(r"<Size>(\d+)</Size>", blob).group(1))
            km = KEY_RE.search(key)
            if not km:
                continue                                   # MDM / _V06_MDM sidecar files and friends
            start = dt.datetime.strptime(km.group(2) + km.group(3), "%Y%m%d%H%M%S").replace(
                tzinfo=dt.timezone.utc)
            out.append({"key": key, "size_bytes": size, "start_utc": start})
        if "<IsTruncated>true</IsTruncated>" in body:
            token = re.search(r"<NextContinuationToken>(.*?)</NextContinuationToken>", body).group(1)
        else:
            break
    out.sort(key=lambda d: d["start_utc"])
    return out


_SESSION = requests.Session()


def _get(url, **kw):
    """This machine drops connections on a ~2.55 s cadence (a WPA3 re-key loop, diagnosed D198).
    A ConnectionReset here is a network artefact, not a fact about the archive -- retry, do not
    let it become an empty listing that reads as 'this radar-day has no scans'."""
    last = None
    for attempt in range(6):
        try:
            r = _SESSION.get(url, timeout=60, **kw)
            r.raise_for_status()
            return r
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            last = e
            import time
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"listing failed after 6 attempts: {last}")


_LIST_CACHE = {}


def list_window(radar, date):
    """Pool date-1 / date / date+1. D2: every US sunset anchor lands on the NEXT UTC day, and a
    single-day listing would return an empty pick for it with no error."""
    pooled = []
    for off in (-1, 0, 1):
        d = date + dt.timedelta(days=off)
        ck = (radar, d)
        if ck not in _LIST_CACHE:
            _LIST_CACHE[ck] = list_day(radar, d)
        pooled.extend(_LIST_CACHE[ck])
    pooled.sort(key=lambda x: x["start_utc"])
    return pooled


def pick_after(scans, anchor, count):
    """First `count` scans starting at or after `anchor`. Deterministic; no look-at-the-data."""
    later = [s for s in scans if s["start_utc"] >= anchor]
    return later[:count]


def main():
    sample = {
        "written_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "governed_by": "PREREG-TERRESTRIAL.md §1.3, §3.1",
        "bucket": BUCKET,
        "elevation_cut_deg": ELEVATION_CUT_DEG,
        "radar_coords_verified": False,
        "state_at_writing": "LISTING ONLY. No volume-scan object has been fetched or decoded.",
        "amendments": [
            {
                "id": "L1-A1",
                "against": "PREREG-TERRESTRIAL.md §1.3 sample line (2 radars x 6 scans x 4 dates = 48)",
                "what": "T2 needs two scans 30 days apart; the 48 contain no such pair. 8 partner scans "
                        "added (2 radars x 4 dates x 1, solar-noon anchored, at date+30d).",
                "primary_sample_unchanged": True,
                "declared_before_any_fetch": True,
            }
        ],
        "selection_rule": "per radar-date: sunrise / solar-noon / sunset anchors (NOAA solar position); "
                          "for each anchor take the first volume scan starting at or after it and the "
                          "next one. t2_partner dates take the solar-noon anchor scan only.",
        "radars": RADARS,
        "short_picks": [],
        "scans": [],
    }

    for radar, meta in RADARS.items():
        for season, ds in BASE_DATES.items():
            base = dt.date.fromisoformat(ds)
            for role, date in (("primary", base), ("t2_partner", base + dt.timedelta(days=30))):
                scans = list_window(radar, date)
                sunrise, noon, sunset = _solar_times(meta["lat"], meta["lon"], date)
                if not scans:
                    sample["scans"].append({"radar": radar, "season": season, "role": role,
                                            "date": date.isoformat(), "key": None,
                                            "note": "NO KEYS LISTED FOR THIS RADAR-DAY"})
                    continue
                anchors = ([("sunrise", sunrise, 2), ("solar_noon", noon, 2), ("sunset", sunset, 2)]
                           if role == "primary" else [("solar_noon", noon, 1)])
                for aname, atime, n in anchors:
                    picked = pick_after(scans, atime, n)
                    if len(picked) < n:
                        # D2 again, generalized: a short pick is the failure that produced no error.
                        sample["short_picks"].append(
                            {"radar": radar, "date": date.isoformat(), "anchor": aname,
                             "wanted": n, "got": len(picked)})
                    for s in picked:
                        sample["scans"].append({
                            "radar": radar, "season": season, "role": role,
                            "date": date.isoformat(), "anchor": aname,
                            "anchor_utc": atime.isoformat(timespec="seconds"),
                            "key": s["key"], "size_bytes": s["size_bytes"],
                            "start_utc": s["start_utc"].isoformat(timespec="seconds"),
                            "lag_s": int((s["start_utc"] - atime).total_seconds()),
                        })
                print(f"  {radar} {date} {role}: {len(scans)} scans listed", file=sys.stderr)

    n_prim = sum(1 for s in sample["scans"] if s.get("role") == "primary" and s.get("key"))
    n_part = sum(1 for s in sample["scans"] if s.get("role") == "t2_partner" and s.get("key"))
    sample["counts"] = {"primary": n_prim, "t2_partner": n_part,
                        "primary_expected": 48, "t2_partner_expected": 8,
                        "complete": n_prim == 48 and n_part == 8,
                        "short_picks": len(sample["short_picks"]),
                        "total_bytes": sum(s.get("size_bytes", 0) for s in sample["scans"])}
    with open("L1_SAMPLE.json", "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=1)
    print(json.dumps(sample["counts"], indent=1))
    if not sample["counts"]["complete"]:
        print("!! SAMPLE INCOMPLETE -- see short_picks", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
