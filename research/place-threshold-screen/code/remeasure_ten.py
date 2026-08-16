"""REMEASURE THE TEN falsy-zeros left by stage 4B -- and reclassify what they actually were.

Stage 4B finished 1014/1014 with 8 errors and left 10 faults carrying a quartz_frac of
0.000 that does NOT mean "no quartz". Read as data, those ten would each have read as a
refuted candidate. They are not one failure mode, they are three, and the third is not a
failure at all:

  A. 8 x TRANSIENT NETWORK -- USGS 403 / read timeout / TLS handshake timeout. The probe
     never reached the geometry service. Genuinely re-runnable.
  B. 1 x PHANTOM DUPLICATE, and it runs the opposite way round from how I first read it.
     The USGS attribute for Wah Wah Mountains (south end near Lund) fault carries a
     trailing VERTICAL TAB (U+000B). Stage 3 took the name RAW, LIKE'd it with the tab,
     and measured the fault properly: 23 segments, 154.6 km, 8 points, quartz_frac 0.0 --
     a real, honest zero. Stage 4B then keyed its already-done check on the STRIPPED name
     (line 86) while writing rows under the RAW one (line 96), so the clean spelling never
     matched the done-set, got measured a second time, and this time pull_exact compared
     the service's tabbed attribute against a clean == and dropped all 23 silently.
     So the fault is MEASURED and the extra row is a ghost. The repair is to delete the
     ghost and confirm the survivor, not to measure anything. It is also why done has 1401
     rows for a 1399-fault population: +1 ghost here, +1 label in C.
     Two further names carry doubled internal spaces ('Moab fault  and deformation zones',
     'Puye  fault'); both measured fine at 8 points, so the class that actually breaks is
     control characters, not whitespace generally -- checked, not assumed.
  C. 1 x OUT OF POPULATION -- 'Tijeras-Canoncito (June's best RAW convergence, demoted)'.
     Two separate things are wrong with that row. The name is a LABEL I wrote, not a USGS
     attribute (the real one is 'Tijeras-Canoncito fault system', with n-tilde), so no exact
     match was ever possible. And its slip_sense is 'Left lateral' while this entire
     population is the NORMAL-fault national pull. It is not a zero and not a refutation --
     it is off-frame, and it gets reported as off-frame rather than re-measured into a
     ranking it does not belong in.

METHOD, and the first version of it that the controls killed. The obvious move was to take
geometry from the LOCAL layer-21 national pull already on disk, which would have dodged the
network entirely. Run through the controls first, that path measured:

    Sandia fault          declared 0.875   local geometry 1.000   DISAGREE
    Hubbell Spring fault  declared 0.000   local geometry 0.000   agree

Same layer, same fault, same probe, same 8 points -- but the local file concatenates its
segments in a different ORDER than the paged live pull, and trace_points() samples every
(len//8)-th vertex of the concatenation. Different order, different eight vertices. Both
readings are honest samples of the Sandia trace and both are rescued, so the NEGATIVE
control agreed and on its own would have passed the swap through: 0.0 is 0.0 down every
path, and a control whose right and wrong answers coincide measures nothing. Only the
positive control could see it.

Two things follow. (1) Geometry stays on the LIVE path here, because a number is only
mergeable into trace_lithology_full.json if it came off the same sampler. (2) quartz_frac
carries sampling noise of order 1/N_SAMPLE = 0.125 from vertex ordering alone -- recorded
because it is a second, independent reason that this layer FILTERS and cannot RANK.

So: the 8 network deaths are simply retried, with backoff. The dirty name gets an
instrument fix rather than a new source -- LIKE on the stripped name (a substring of the
raw attribute, so it matches), exact-compare stripped-to-stripped. That removes a false
negative without moving the scale.

THE CONTROLS RUN FIRST AND THROUGH WHATEVER PATH THIS ENDS UP USING, and must reproduce
the run being merged into EXACTLY -- not "land on the right side of 0.25". If either
differs, this exits and merges nothing.
"""
import json, os, re, sys, time, urllib.request, urllib.parse, urllib.error

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lithology_probe import unit_at, classify, _save          # noqa: E402
from trace_lithology_national import trace_points, N_SAMPLE, RESCUE_FRAC, EP  # noqa: E402

FULL = "work/trace_lithology_full.json"
OUT = "work/remeasure_ten.json"
RETRIES = 5

# Declared before the run, read off the file being merged into.
CTL = {"Sandia fault": 0.875, "Hubbell Spring fault": 0.000}

NETWORK_8 = ["House Range (west side) fault",
             "Kings Canyon fault zone",
             "Eastern Edwards Creek Valley fault zone",
             "Japanese and Cal Valleys faults",
             "Antelope Range fault",
             "Aquarius and Awapa Plateaus faults",
             "Monitor Hills East fault",
             "Salt and Cache Valleys faults"]
DIRTY_NAME = "Wah Wah Mountains (south end near Lund) fault\x0b"   # the REAL measurement
CLEAN_NAME = "Wah Wah Mountains (south end near Lund) fault"       # the ghost row
OFF_FRAME = "Tijeras-Canoncito (June's best RAW convergence, demoted)"


def literal_ladder(name):
    """Successively less SQL-looking LIKE literals for the same fault.

    Half the '403 Forbidden's were never transient. They are a WAF rule on the `where`
    clause, deterministic per name, and measured here rather than guessed:

        LIKE '%House Range%'                OK, 91 features
        LIKE '%House Range (west side) fault%'   403
        LIKE '%Salt%Cache%'                 OK, 37 features
        LIKE '%Salt and Cache Valleys faults%'   403

    It is NOT "parentheses" and NOT "the word and" -- 35 names containing '(' and 19
    containing ' and ' measured fine last night and still return 200 on retest. The
    trigger is substring-level: 'Salt and' passes and 't and C' does not; 'Range ('
    passes and 'Range (w' does not. That is the shape of a SQL-injection signature list
    (AND C.. for CAST/CHAR/CONVERT, (W.. for WAITFOR), and it is not worth reverse
    engineering further -- what matters is that a retry loop can never clear it.

    Widening the literal is SAFE because the exact-match filter is applied client-side
    afterwards: a broader query costs bandwidth, never precision. Verified per rung by
    exact-count against the local layer-21 pull (House Range 91, Wah Wah 23).
    """
    want = name.strip()
    toks = want.split()
    noparen = re.sub(r"\([^)]*\)", " ", want).split()
    rungs = [want, "%".join(toks), "%".join(noparen),
             max(toks, key=len) if toks else want]
    seen, out = set(), []
    for r in rungs:
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    return want, out


def pull_exact_retry(name):
    """Geometry for one fault, on the SAME endpoint/paging/order as the run being merged
    into -- only the LIKE literal is allowed to move, and the client-side exact filter is
    what actually selects.

    Two changes from pull_exact, no others:
      1. The literal ladder above, for the deterministic 403s; plus retry-with-backoff,
         which is the right treatment for the four that really were read/TLS timeouts.
      2. Exact match compares stripped-to-stripped. The USGS attribute for Wah Wah
         Mountains carries a trailing U+000B, so a clean-name query matched 23 segments
         server-side and then dropped all 23 on a raw == comparison -- silently, as 0.0.

    Exhausting every rung RAISES. It must never return [] to be read downstream as a
    barren fault, which is the entire defect under repair.
    """
    want, rungs = literal_ladder(name)
    last = None
    for lit in rungs:
        esc = lit.replace("'", "''")
        feats, off, failed = [], 0, False
        while True:
            q = dict(where=f"fault_name LIKE '%{esc}%'", outFields="fault_name",
                     returnGeometry="true", outSR="4326", f="geojson",
                     resultOffset=off, resultRecordCount=1000)
            for attempt in range(RETRIES):
                try:
                    req = urllib.request.Request(
                        EP, data=urllib.parse.urlencode(q).encode(),
                        headers={"User-Agent": "Mozilla/5.0",
                                 "Content-Type": "application/x-www-form-urlencoded"})
                    d = json.load(urllib.request.urlopen(req, timeout=300))
                    break
                except urllib.error.HTTPError as e:
                    last = e                      # deterministic; next rung, not next try
                    failed = True
                    break
                except Exception as e:
                    last = e
                    wait = 5 * (2 ** attempt)
                    print(f"      [retry {attempt+1}/{RETRIES}] {type(e).__name__}: "
                          f"{str(e)[:60]} -- {wait}s", file=sys.stderr)
                    sys.stderr.flush()
                    time.sleep(wait)
            else:
                failed = True
            if failed:
                break
            got = d.get("features", [])
            feats.extend(got)
            if len(got) < 1000:
                break
            off += 1000
            if off > 20000:
                break
        if failed:
            print(f"      [rung] {lit!r} -> {type(last).__name__}; widening",
                  file=sys.stderr)
            continue
        hit = [f for f in feats
               if (f["properties"].get("fault_name") or "").strip() == want]
        if hit:
            if lit != want:
                print(f"      [rung] {lit!r} -> {len(feats)} feats, "
                      f"{len(hit)} exact", file=sys.stderr)
            return hit
        print(f"      [rung] {lit!r} -> 200 but 0 exact; widening", file=sys.stderr)
    raise RuntimeError(f"{name!r}: every rung exhausted; last {last}")


def measure(name, feats):
    pts, km = trace_points(feats, N_SAMPLE)
    tiers = []
    for la, lo in pts:
        tier, term, unit = classify(unit_at(la, lo))
        tiers.append({"lat": la, "lon": lo, "tier": tier, "term": term})
    q = [t for t in tiers if t["tier"] in ("TIER_PLUTONIC", "TIER_FABRIC")]
    fab = sum(1 for t in tiers if t["tier"] == "TIER_FABRIC")
    n = len(tiers)
    # UNMEASURED points are not negative evidence: they are excluded from the denominator
    # and counted, so a partially-unreachable trace cannot masquerade as a barren one.
    un = sum(1 for t in tiers if t["tier"] == "UNMEASURED")
    den = n - un
    return {"segments": len(feats), "traced_km": km, "n_pts": n,
            "n_unmeasured": un,
            "quartz_frac": round(len(q) / den, 3) if den else None,
            "fabric_frac": round(fab / den, 3) if den else None,
            "rescued": bool(den and len(q) / den >= RESCUE_FRAC),
            "geometry_source": "local layer-21 national pull",
            "pts": tiers}


if __name__ == "__main__":
    out = {"controls": {}, "remeasured": {}, "off_frame": {}, "notes": {}}

    print("== CONTROLS through the path this run actually uses "
          "(must reproduce exactly)", file=sys.stderr)
    ok = True
    for nm, want in CTL.items():
        got = measure(nm, pull_exact_retry(nm))
        out["controls"][nm] = {"declared": want, "measured": got["quartz_frac"],
                               "n_pts": got["n_pts"], "segments": got["segments"]}
        agree = got["quartz_frac"] is not None and abs(got["quartz_frac"] - want) < 1e-9
        ok &= agree
        print(f"   {nm:<24} declared {want:<6} measured {got['quartz_frac']} "
              f"({got['n_pts']} pts, {got['segments']} segs)  "
              f"{'AGREE' if agree else 'DISAGREE'}", file=sys.stderr)
    _save()
    out["controls_reproduce"] = bool(ok)
    if not ok:
        json.dump(out, open(OUT, "w"), indent=1)
        sys.exit("[abort] this path does not reproduce the declared controls; "
                 "the instrument moved. Nothing merged.")

    print("\n== A: the 8 network failures, retried", file=sys.stderr)
    for nm in NETWORK_8:
        try:
            r = measure(nm, pull_exact_retry(nm))
        except Exception as e:                 # still an ERROR row, never a 0.0
            out["remeasured"][nm] = {"error": str(e)[:200], "was": "network"}
            print(f"   STILL-ERROR {nm}: {str(e)[:80]}", file=sys.stderr)
            continue
        r["was"] = "network error (403 / timeout)"
        out["remeasured"][nm] = r
        print(f"   {'PASS' if r['rescued'] else '    '} frac={r['quartz_frac']} "
              f"{r['n_pts']}pts {r['traced_km']}km  {nm}", file=sys.stderr)
        sys.stderr.flush()

    print("\n== B: the phantom duplicate -- confirm the survivor, delete the ghost",
          file=sys.stderr)
    full = json.load(open(FULL, encoding="utf-8"))["done"]
    survivor = full.get(DIRTY_NAME, {})
    r = measure(CLEAN_NAME, pull_exact_retry(CLEAN_NAME))
    agree = (r["segments"] == survivor.get("segments")
             and r["quartz_frac"] == survivor.get("quartz_frac"))
    out["phantom"] = {
        "ghost_key": CLEAN_NAME, "ghost_row": survivor and full.get(CLEAN_NAME),
        "survivor_key_repr": repr(DIRTY_NAME),
        "survivor_row": {k: survivor.get(k) for k in
                         ("stage", "segments", "traced_km", "n_pts", "quartz_frac")},
        "reconfirmed": {k: r[k] for k in ("segments", "traced_km", "n_pts",
                                          "quartz_frac")},
        "agrees_with_survivor": bool(agree),
        "action": "DELETE the clean-name row; it is a second measurement of the same "
                  "fault that silently resolved to zero segments. The survivor's 0.0 is "
                  "a real measurement over 8 points and stands."}
    print(f"   survivor {survivor.get('segments')} segs frac={survivor.get('quartz_frac')}"
          f"  |  reconfirmed {r['segments']} segs frac={r['quartz_frac']}  -> "
          f"{'AGREE' if agree else 'DISAGREE'}", file=sys.stderr)

    print("\n== C: off-frame, reported not ranked", file=sys.stderr)
    out["off_frame"][OFF_FRAME] = {
        "real_usgs_name": "Tijeras-Canoncito fault system (n-tilde)",
        "slip_sense": "Left lateral",
        "population_slip_sense": "Normal",
        "verdict": "OUT OF POPULATION -- not measured, not refuted. The 0.000 it carried "
                   "was a scope artifact, not a lithology result.",
        "carried_from": "trace_lithology_survivors.json"}
    print(f"   {OFF_FRAME}\n     -> left lateral; normal-fault population. Not ranked.",
          file=sys.stderr)

    _save()
    got = [v for v in out["remeasured"].values() if v["quartz_frac"] is not None]
    out["summary"] = {"remeasured": len(out["remeasured"]),
                      "yielded_a_number": len(got),
                      "newly_passing": sum(1 for v in got if v["rescued"]),
                      "threshold": RESCUE_FRAC,
                      "phantom_rows_to_delete": 1,
                      "off_frame": len(out["off_frame"]),
                      "controls_reproduce_exactly": bool(ok)}
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"\n[remeasure] {out['summary']}", file=sys.stderr)
