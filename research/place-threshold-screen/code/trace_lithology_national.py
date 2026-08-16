"""STAGE 3 -- the recall fix. Re-probe every node that FAILED at-point, along its own trace.

Why. Addendum 3 sec.3: the Sandia fault scored NONE ('Quaternary sedimentary') on the
at-point probe and then returned quartz-rich at 12 of 16 points sampled along its MAPPED
TRACE, one of them a unit named `Sandia Granite`. The at-point probe is therefore a
false-NEGATIVE machine: a range-front normal fault has alluvium on its hanging wall, so a
point placed a kilometre off-trace lands in fan gravel and reports NONE with no error.

That defect does not stop at Sandia. 386 of 507 nodes scored NONE and 59 scored
TIER_VOLCANIC, and the top-5 national list is drawn from the 62 survivors -- a list whose
RECALL is unmeasured. Ranking the survivors of a test known to produce false negatives is
the same error as June's, one level up. This run measures the recall.

Method, per node that failed at-point:
  1. pull the node's parent fault by name (LIKE, then exact -- fault_name matching in this
     service is case-sensitive and exact-match drops segments silently), PAGED.
  2. sample up to N_SAMPLE vertices spread evenly along the concatenated trace.
  3. Macrostrat point query at each; quartz_frac = quartz-rich points / points measured.

A node is RESCUED at quartz_frac >= RESCUE_FRAC. That threshold is declared here before the
run, not chosen after seeing the histogram: Sandia = 0.75, Hubbell Spring = 0.03, and the
gap between them is where the line goes. Both are re-measured by this run as controls --
Sandia is the KNOWN POSITIVE (must be rescued) and Hubbell Spring the KNOWN NEGATIVE (must
not be). If either control comes out wrong the whole pass is void, and it says so.

Resumable: state in work/trace_lithology_national.json, rewritten every CKPT nodes.
"""
import json, math, os, sys, time, urllib.request, urllib.parse

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lithology_probe import unit_at, classify, _save  # noqa: E402

EP = "https://earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/21/query"
OUT = "work/trace_lithology_national.json"
N_SAMPLE = 8
RESCUE_FRAC = 0.25          # declared before the run; Sandia 0.75 / Hubbell 0.03
CKPT = 5
R = 6371.0

CONTROLS = [("Sandia fault", "POSITIVE"), ("Hubbell Spring fault", "NEGATIVE")]


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def pull_exact(name):
    esc = name.replace("'", "''")
    feats, off = [], 0
    while True:
        q = dict(where=f"fault_name LIKE '%{esc}%'", outFields="fault_name",
                 returnGeometry="true", outSR="4326", f="geojson",
                 resultOffset=off, resultRecordCount=1000)
        req = urllib.request.Request(
            EP, data=urllib.parse.urlencode(q).encode(),
            headers={"User-Agent": "Mozilla/5.0",
                     "Content-Type": "application/x-www-form-urlencoded"})
        d = json.load(urllib.request.urlopen(req, timeout=300))
        got = d.get("features", [])
        feats.extend(got)
        if len(got) < 1000:
            break
        off += 1000
        if off > 20000:
            break
    return [f for f in feats if (f["properties"].get("fault_name") or "") == name]


def trace_points(feats, n):
    pts = []
    for ft in feats:
        g = ft.get("geometry") or {}
        parts = ([g["coordinates"]] if g.get("type") == "LineString"
                 else g.get("coordinates", []) if g.get("type") == "MultiLineString" else [])
        for part in parts:
            for c in part:
                pts.append((round(c[1], 4), round(c[0], 4)))
    if not pts:
        return [], 0.0
    km = sum(hav(*pts[i], *pts[i + 1]) for i in range(len(pts) - 1)
             if hav(*pts[i], *pts[i + 1]) < 30)
    step = max(1, len(pts) // n)
    return pts[::step][:n], round(km, 1)


if __name__ == "__main__":
    wait_pid = None
    for a in sys.argv[1:]:
        if a.startswith("--wait-pid="):
            wait_pid = int(a.split("=")[1])
    if wait_pid:
        import subprocess
        while True:
            r = subprocess.run(["powershell", "-NoProfile", "-Command",
                                f"if (Get-Process -Id {wait_pid} -EA SilentlyContinue)"
                                f" {{'ALIVE'}} else {{'GONE'}}"],
                               capture_output=True, text=True)
            if "GONE" in r.stdout:
                break
            print(f"[wait] pid {wait_pid} still on Macrostrat ...", file=sys.stderr)
            sys.stderr.flush()
            time.sleep(60)

    d = json.load(open("work/transport_screen_stage2.json"))
    todo, seen = [], set()
    for n in d["all"]:
        if n["at_point_tier"] in ("TIER_PLUTONIC", "TIER_FABRIC"):
            continue                       # already a hit; recall is what's at issue
        nm = (n.get("fault_name") or "").strip()
        if not nm or n.get("forced") or nm in seen:
            continue
        seen.add(nm)
        todo.append(n)
    for nm, _ in CONTROLS:
        if nm not in seen:
            todo.insert(0, {"fault_name": nm, "lat": None, "lon": None,
                            "age": "control", "age_rank": -1, "at_point_tier": "CONTROL",
                            "total_fault_length": 0})
    state = json.load(open(OUT)) if os.path.exists(OUT) else {"done": {}}
    print(f"[stage3] {len(todo)} distinct failed-at-point faults; "
          f"{len(state['done'])} already done", file=sys.stderr)
    for i, n in enumerate(todo, 1):
        nm = n["fault_name"]
        if nm in state["done"]:
            continue
        try:
            feats = pull_exact(nm)
            pts, km = trace_points(feats, N_SAMPLE)
            tiers = []
            for la, lo in pts:
                tier, term, unit = classify(unit_at(la, lo))
                tiers.append({"lat": la, "lon": lo, "tier": tier, "term": term})
            q = [t for t in tiers if t["tier"] in ("TIER_PLUTONIC", "TIER_FABRIC")]
            frac = round(len(q) / len(tiers), 3) if tiers else 0.0
            state["done"][nm] = {"segments": len(feats), "traced_km": km,
                                 "n_pts": len(tiers), "quartz_frac": frac,
                                 "rescued": bool(frac >= RESCUE_FRAC and tiers),
                                 "at_point_tier": n["at_point_tier"],
                                 "age": n.get("age"), "age_rank": n.get("age_rank"),
                                 "total_fault_length": n.get("total_fault_length"),
                                 "lat": n.get("lat"), "lon": n.get("lon"),
                                 "pts": tiers}
            mark = "RESCUED" if state["done"][nm]["rescued"] else "       "
            print(f"[{i}/{len(todo)}] {mark} frac={frac:.2f} {len(tiers)}pts  {nm[:52]}",
                  file=sys.stderr)
        except Exception as e:
            state["done"][nm] = {"error": str(e)[:200]}
            print(f"[{i}/{len(todo)}] ERROR {nm[:40]}: {e}", file=sys.stderr)
        sys.stderr.flush()
        if i % CKPT == 0:
            _save()
            json.dump(state, open(OUT, "w"), indent=1)
    _save()
    ok = [v for v in state["done"].values() if "quartz_frac" in v]
    res = [k for k, v in state["done"].items() if v.get("rescued")]
    ctl = {k: state["done"].get(k, {}).get("quartz_frac") for k, _ in CONTROLS}
    state["summary"] = {"measured": len(ok), "rescued": len(res),
                        "rescue_frac_threshold": RESCUE_FRAC, "controls": ctl,
                        "controls_valid": (ctl.get("Sandia fault") or 0) >= RESCUE_FRAC
                                          and (ctl.get("Hubbell Spring fault") or 1) < RESCUE_FRAC,
                        "rescued_names": sorted(res)}
    json.dump(state, open(OUT, "w"), indent=1)
    print(f"[stage3] measured {len(ok)}, RESCUED {len(res)}, controls {ctl}",
          file=sys.stderr)
