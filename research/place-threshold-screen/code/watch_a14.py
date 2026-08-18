"""Detached poller: when A14 lands, write its verdict where a later breath will find it.

Same reason watch_a8.py exists. A14 runs about two hours; the breath that started it will not
be the breath that sees it finish, and "I will check back on it" is not a trigger -- it is a
carrier of an intention, and this project has a file of cases where that is exactly the same
as nothing. This turns the landing of data/water_leg.json into an event.

It deliberately does NOT rebuild the deliverable. A14 is a LABEL, not a filter: A7's rule is
that any new criterion must be tested as a tie-breaker against the measured resolution before
it may reorder anything, and A14's own pre-registration says the same. So this writes a
summary and stops. Deciding what to do with it is a judgement, and a poller should not make
judgements.
"""
import datetime, json, os, sys, time

TARGET = "data/water_leg.json"
LOG = "work/a14_chain.log"
MAX_WAIT = 4 * 3600
POLL = 30


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, file=sys.stderr)


if __name__ == "__main__":
    base = os.path.getmtime(TARGET) if os.path.exists(TARGET) else 0.0
    log(f"watching {TARGET} (baseline mtime {base}), max wait {MAX_WAIT}s")
    t0 = time.time()
    while time.time() - t0 < MAX_WAIT:
        time.sleep(POLL)
        if not os.path.exists(TARGET) or os.path.getmtime(TARGET) <= base:
            continue
        time.sleep(3)                       # let the writer finish closing the file
        try:
            d = json.load(open(TARGET))
        except Exception as e:
            log(f"{TARGET} touched but unreadable ({e}); still waiting")
            continue
        log(f"{TARGET} landed ({os.path.getsize(TARGET):,} bytes)")
        for k, v in d.get("statistics", {}).items():
            log(f"  {k:15s} surv={v['surv_median']} rand={v['null_random_median']} "
                f"fault={v['null_fault_median']} | p_rand={v['vs_random']['p']} "
                f"p_fault={v['vs_fault']['p']}")
        log(f"  rho(water,score)={d.get('spearman_water_vs_score')}")
        log(f"  bars={d.get('bars')}")
        log(f"  band tie-breaker: {d.get('band_tiebreaker')}")
        log("  ! A14 is a LABEL unless bar_ii/iii/iv pass AND it separates the band by more "
            "than the band's own wobble. Do not re-rank on it without that test (A7).")
        log("DONE.")
        sys.exit(0)
    log("GAVE UP -- A14 never landed. data/water_leg.json is absent, which means the water "
        "column is UNRUN, not 'no water signal'. Say UNRUN.")
    sys.exit(1)
