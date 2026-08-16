"""STAGE 4B -- trace-probe the recovered field. One instrument over the whole population.

After stage 4A the candidate set is 1,645 nodes on 1,399 named dilatant faults, not 507 on
392. Stage 3 measured 352 of those faults (the at-point failures) and stage 3B measured 62
(the at-point survivors). This run measures THE REST, with the identical probe, and merges
all three into a single file where every fault carries a quartz_frac obtained the same way.

Why every fault and not just the promising ones: a screen whose recall is unmeasured cannot
rank. That defect has now appeared three times in this pipeline at three different levels --
June's survey ranked on the light-record (the outcome variable), the at-point lithology probe
was a false-negative machine (Sandia 0.00 at point, 0.88 on trace), and the noder deleted
72.6% of the field. Each fix exposed the next one up. This is the level where the population
is finally the whole population, so it is the level where a rank means something.

Controls carry forward from stage 3 unchanged and are re-asserted at load:
    Sandia fault          0.88  POSITIVE -- must be >= RESCUE_FRAC
    Hubbell Spring fault  0.00  NEGATIVE -- must be <  RESCUE_FRAC
If the merged file ever disagrees with those two numbers, the scale moved and every
comparison across the three stages is void. It exits rather than reporting.

Resumable at every CKPT faults. Expect ~3-4 h: ~985 faults x 8 Macrostrat points, paced to
one client (stage 3B must finish first -- two clients on the same public API earn a
rate-limit that corrupts both runs).
"""
import json, os, sys, time

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lithology_probe import unit_at, classify, _save  # noqa: E402
from trace_lithology_national import pull_exact, trace_points, N_SAMPLE, RESCUE_FRAC  # noqa: E402

OUT = "work/trace_lithology_full.json"
PRIOR = ["work/trace_lithology_national.json", "work/trace_lithology_survivors.json"]
NODES = "work/transport_nodes_perfault.json"
CKPT = 5
CTL = {"Sandia fault": ("POSITIVE", True), "Hubbell Spring fault": ("NEGATIVE", False)}


def wait_for(pid):
    import subprocess
    while True:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            f"if (Get-Process -Id {pid} -EA SilentlyContinue)"
                            f" {{'ALIVE'}} else {{'GONE'}}"],
                           capture_output=True, text=True)
        if "GONE" in r.stdout:
            return
        print(f"[wait] pid {pid} still on Macrostrat ...", file=sys.stderr)
        sys.stderr.flush()
        time.sleep(45)


def check_controls(done, where):
    for nm, (label, want) in CTL.items():
        v = (done.get(nm) or {}).get("quartz_frac")
        if v is None:
            continue
        if (v >= RESCUE_FRAC) is not want:
            sys.exit(f"[abort] control {nm} ({label}) reads {v} in {where}; "
                     f"threshold {RESCUE_FRAC}. Scale moved -- all three stages void.")
    return {nm: (done.get(nm) or {}).get("quartz_frac") for nm in CTL}


if __name__ == "__main__":
    for a in sys.argv[1:]:
        if a.startswith("--wait-pid="):
            wait_for(int(a.split("=")[1]))

    state = json.load(open(OUT)) if os.path.exists(OUT) else {"done": {}}
    for p in PRIOR:                       # warm start: never re-measure what is measured
        if os.path.exists(p):
            prior = json.load(open(p)).get("done", {})
            for k, v in prior.items():
                if "quartz_frac" in v and k not in state["done"]:
                    state["done"][k] = dict(v, stage=os.path.basename(p))
            print(f"[warm] {len(prior)} rows from {p}", file=sys.stderr)
    print(f"[ctl] {check_controls(state['done'], 'warm start')}", file=sys.stderr)

    nd = json.load(open(NODES))
    best = {}
    for n in nd["all"]:                   # one representative node per fault, best first
        nm = (n.get("fault_name") or "").strip()
        if nm and nm not in best:
            best[nm] = n
    todo = [n for nm, n in best.items() if nm not in state["done"]]
    todo.sort(key=lambda r: (-(r.get("age_rank") or 0),
                             -(r.get("total_fault_length") or 0)))
    print(f"[stage4b] {len(best)} faults in the recovered field; "
          f"{len(state['done'])} already measured; {len(todo)} to go", file=sys.stderr)

    for i, n in enumerate(todo, 1):
        nm = n["fault_name"]
        try:
            feats = pull_exact(nm)
            pts, km = trace_points(feats, N_SAMPLE)
            tiers = []
            for la, lo in pts:
                tier, term, unit = classify(unit_at(la, lo))
                tiers.append({"lat": la, "lon": lo, "tier": tier, "term": term})
            q = [t for t in tiers if t["tier"] in ("TIER_PLUTONIC", "TIER_FABRIC")]
            fab = sum(1 for t in tiers if t["tier"] == "TIER_FABRIC")
            frac = round(len(q) / len(tiers), 3) if tiers else 0.0
            state["done"][nm] = {"stage": "stage4b", "segments": len(feats),
                                 "traced_km": km, "n_pts": len(tiers),
                                 "quartz_frac": frac,
                                 "fabric_frac": round(fab / len(tiers), 3) if tiers else 0.0,
                                 "rescued": bool(frac >= RESCUE_FRAC and tiers),
                                 "age": n.get("age"), "age_rank": n.get("age_rank"),
                                 "total_fault_length": n.get("total_fault_length"),
                                 "lat": n.get("lat"), "lon": n.get("lon"), "pts": tiers}
            mark = "PASS" if state["done"][nm]["rescued"] else "    "
            print(f"[{i}/{len(todo)}] {mark} frac={frac:.2f} {len(tiers)}pts  {nm[:52]}",
                  file=sys.stderr)
        except Exception as e:
            state["done"][nm] = {"stage": "stage4b", "error": str(e)[:200]}
            print(f"[{i}/{len(todo)}] ERROR {nm[:40]}: {e}", file=sys.stderr)
        sys.stderr.flush()
        if i % CKPT == 0:
            _save()
            json.dump(state, open(OUT, "w"), indent=1)

    _save()
    ok = [v for v in state["done"].values() if "quartz_frac" in v]
    passing = [k for k, v in state["done"].items() if v.get("rescued") or v.get("holds")]
    state["summary"] = {"faults_measured": len(ok), "faults_passing": len(passing),
                        "threshold": RESCUE_FRAC,
                        "controls": check_controls(state["done"], "final"),
                        "errors": sum(1 for v in state["done"].values() if "error" in v)}
    json.dump(state, open(OUT, "w"), indent=1)
    print(f"[stage4b] {state['summary']}", file=sys.stderr)
