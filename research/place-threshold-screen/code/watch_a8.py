"""Wait for A8 to land, then rebuild the deliverable. A TRIGGER, not a note to myself.

jurisdiction_leg.py takes ~90 minutes (625 points x 2 live ArcGIS queries) and will outlive
the breath that started it. candidate_list.py must be re-run once it lands, or the shipped
list keeps saying JURISDICTION: UNRUN while the answer sits on disk beside it. "I will
re-run it" is not a clock -- this file is.

Bounded on purpose: gives up after MAX_WAIT and says so in the log rather than lingering.
It never kills anything and never writes anything except its own log and whatever
candidate_list.py writes.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

TARGET = "data/jurisdiction_leg.json"
LOG = "work/a8_chain.log"
POLL_S = 60
MAX_WAIT_S = 3 * 3600
START = time.time()
# Only a file written AFTER this watcher started counts. A pre-existing stale artefact
# would otherwise fire the rebuild instantly and the rebuild would look like a success.
BASELINE = os.path.getmtime(TARGET) if os.path.exists(TARGET) else 0.0


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}\n")


log(f"watching {TARGET} (baseline mtime {BASELINE}), max wait {MAX_WAIT_S}s")
while time.time() - START < MAX_WAIT_S:
    if os.path.exists(TARGET) and os.path.getmtime(TARGET) > BASELINE:
        time.sleep(5)                      # let the writer close the handle
        log(f"{TARGET} landed ({os.path.getsize(TARGET)} bytes) -- rebuilding deliverable")
        r = subprocess.run([sys.executable, "code/candidate_list.py"],
                           capture_output=True, text=True)
        log(f"candidate_list.py exit={r.returncode}")
        for line in (r.stderr or "").strip().splitlines():
            log("  " + line)
        if r.returncode == 0:
            log("REBUILT. reports/CANDIDATE-LIST.md now carries the jurisdiction column.")
        else:
            log("REBUILD FAILED -- the list still says UNRUN. Do not ship it.")
        sys.exit(r.returncode)
    time.sleep(POLL_S)

log(f"GAVE UP after {MAX_WAIT_S}s. A8 never wrote {TARGET}. The deliverable still says "
    f"JURISDICTION: UNRUN, which is TRUE and is the correct thing for it to say.")
sys.exit(2)
