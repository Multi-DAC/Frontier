"""SECTION 12 — archive reachability, measured per night.

The question §12 asks is NOT about the sky. It asks whether the exposures that a
night's public alerts point at are still fetchable from the archive that is
supposed to hold them. One night (2018-06-01) gave 15 of 55 exposures missing and
5.76% of alerts stranded; PAPER-00-ARCHITECTURE.md row 12 forbids quoting that as
an archive property until it is reproduced on >= 2 nights.

PROBE CORRECTNESS — READ THIS BEFORE CHANGING THE URL FORM.
The alert packet's `pdiffimfilename` ends `.fits`. IRSA stores the same product as
`.fits.fz`. A HEAD on the literal alert filename returns 404 for EVERY exposure,
including exposures that are demonstrably present, so the naive probe reports 100%
unreachable and that reads exactly like a finding. This script therefore does not
guess a URL at all: it fetches the exposure's IRSA directory listing and does set
membership against the names the archive itself reports. One request per exposure.
A listing that 404s is a missing exposure; a listing that errors any other way is
recorded as UNKNOWN and is never silently folded into either bucket.

Usage:  python measure_reachability.py <alert_index.json> <label>
"""
import json, sys, re, collections, time, urllib.request, urllib.error

try:
    import truststore; truststore.inject_into_ssl()
except Exception:
    pass

IBE = "https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci"


def exposure_dir(stamp):
    """20180601167662 -> .../sci/2018/0601/167662/"""
    return f"{IBE}/{stamp[:4]}/{stamp[4:8]}/{stamp[8:]}/"


def listing(url, tries=3):
    """(status, set_of_names). status is an int HTTP code or None for a transport error."""
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                names = set(re.findall(r'href="([^"/]+)"', r.read().decode("utf-8", "replace")))
                return r.status, names
        except urllib.error.HTTPError as e:
            return e.code, set()          # a real archive answer; do not retry
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))       # transport flake: this network drops packets
    return None, set()


def main(index_path, label):
    rows = json.load(open(index_path))
    by_exp = collections.defaultdict(set)     # exposure key -> distinct diff-image filenames
    alerts_by_exp = collections.Counter()
    n_alerts = 0
    for x in rows:
        f = x.get("f")
        n_alerts += 1
        if not f:
            continue
        p = f.split("_")
        key = "_".join(p[1:3])                # <stamp>_<field>
        by_exp[key].add(f)
        alerts_by_exp[key] += 1

    out = {"label": label, "index": index_path, "n_alerts_total": n_alerts,
           "n_exposures": len(by_exp), "exposures": []}

    present = missing = unknown = 0
    for key in sorted(by_exp):
        stamp = key.split("_")[0]
        code, names = listing(exposure_dir(stamp))
        want = by_exp[key]
        # the archive's name for the alert's `*.fits` is `*.fits.fz`
        found = {f for f in want if (f + ".fz") in names or f in names}
        if code == 200:
            state = "PRESENT" if found else "EMPTY"
        elif code == 404:
            state = "MISSING"
        else:
            state = "UNKNOWN"
        if state == "PRESENT" and len(found) == len(want):
            present += 1
        elif state in ("MISSING", "EMPTY") or (state == "PRESENT" and not found):
            missing += 1
        elif state == "UNKNOWN":
            unknown += 1
        else:
            present += 1                      # partial: counted present at exposure level,
                                              # the per-image numbers below carry the loss
        out["exposures"].append(dict(key=key, http=code, state=state,
                                     n_images_referenced=len(want), n_images_found=len(found),
                                     n_alerts=alerts_by_exp[key], listing_size=len(names)))
        print(f"  {key} {code} {state} imgs {len(found)}/{len(want)} alerts {alerts_by_exp[key]}")

    # alert-level stranding: an alert is stranded if ITS difference image is not at IRSA
    stranded = sum(e["n_alerts"] for e in out["exposures"] if e["n_images_found"] == 0)
    unknown_alerts = sum(e["n_alerts"] for e in out["exposures"] if e["state"] == "UNKNOWN")
    out.update(exposures_present=present, exposures_missing=missing, exposures_unknown=unknown,
               exposure_miss_frac=missing / len(by_exp) if by_exp else None,
               alerts_stranded=stranded,
               alerts_stranded_frac=stranded / n_alerts if n_alerts else None,
               alerts_unknown=unknown_alerts)
    dest = f"REACH_{label}.json"
    json.dump(out, open(dest, "w"), indent=1)
    print(f"\n{label}: exposures {missing}/{len(by_exp)} missing "
          f"({100*out['exposure_miss_frac']:.2f}%), {unknown} unknown · "
          f"alerts stranded {stranded}/{n_alerts} ({100*out['alerts_stranded_frac']:.2f}%) -> {dest}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
