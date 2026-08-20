"""Wait for A16 to land OR die, and make either outcome reach a breath. A TRIGGER, not a note.

Descended from watch_a8.py with ONE deliberate change, and the change is the whole point:
watch_a8 watches only for SUCCESS. A16's actual failure today was not slowness -- it was
SILENT DEATH. The first launch died at 15:05 because it was a shell child whose parent breath
ended, and nothing saw it for three and a half hours, because a dead job and a running job are
indistinguishable from the filesystem: both leave a log that has simply stopped growing.

watch_a8's design, applied to that, would have polled quietly for three hours and then said
"gave up" -- true, late, and carrying no diagnosis. So this watcher holds the PID as well as
the path, and reports the death the minute it happens, distinguishing it from the timeout.

It never kills anything. It writes its own log, one status file, and one line into the carapace
daily log -- because a status file inside a research repo is another artefact with no reader,
and the daily log is a thing a breath actually opens.

    Start-Process -WindowStyle Hidden python "code/watch_a16.py 23612"
    ^ Start-Process, NOT a shell background job. That distinction is what killed the 15:05 run.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

TARGET = "data/current_leg.json"
LOG = "work/a16_chain.log"
STATUS = "work/A16-STATUS.md"
DAILY = r"C:\Users\Wasch\carapace\memory\2026-08-19.md"
POLL_S = 45
MAX_WAIT_S = 90 * 60
MIN_BYTES = 200          # a 0-byte or stub file is a failure wearing a success's name

PID = int(sys.argv[1]) if len(sys.argv) > 1 else None
START = time.time()
# Only a file written AFTER this watcher started counts. A pre-existing stale artefact would
# otherwise fire instantly and the stale read would look like a fresh landing.
BASELINE = os.path.getmtime(TARGET) if os.path.exists(TARGET) else 0.0


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}\n")


def alive(pid):
    """True if pid is in the table. Returns True on an unreadable table -- an unknown must not
    be reported as a death, because a false death claim is louder and worse than a late one."""
    if pid is None:
        return True
    try:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                             capture_output=True, text=True, timeout=30)
        return str(pid) in (out.stdout or "")
    except Exception as e:
        log(f"WARN: could not read process table ({e}) -- assuming alive, NOT reporting a death")
        return True


def announce(headline, detail):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS, "w", encoding="utf-8") as f:
        f.write(f"# A16 — {headline}\n\n_{stamp}, written by code/watch_a16.py (pid {os.getpid()})_\n\n{detail}\n")
    try:
        with open(DAILY, "a", encoding="utf-8") as f:
            f.write(f"\n**{time.strftime('%H:%M')} — A16 WATCHER: {headline}** {detail}\n")
    except Exception as e:
        log(f"WARN: could not append to daily log ({e}) -- status file still written")
    log(f"ANNOUNCED: {headline}")


log(f"watching {TARGET} (baseline {BASELINE}) and pid {PID}; max wait {MAX_WAIT_S}s")

while time.time() - START < MAX_WAIT_S:
    if os.path.exists(TARGET) and os.path.getmtime(TARGET) > BASELINE:
        time.sleep(5)                          # let the writer close its handle
        size = os.path.getsize(TARGET)
        if size < MIN_BYTES:
            announce("LANDED BUT SUSPECT",
                     f"`{TARGET}` appeared at only {size} B (< {MIN_BYTES} B). That is a stub, not "
                     f"a result. Read it before believing it, and check `work/a16_run3.log`.")
            sys.exit(3)
        announce("LANDED",
                 f"`{TARGET}` written, {size:,} B. This is CLAYTON'S OWN LEG (rushing water / "
                 f"current + EM-active minerals). Next: section it into REPORT.md, re-read the "
                 f"report for numbers A16 moves, push, and hand it to him — he is waiting to publish.")
        sys.exit(0)

    if not alive(PID):
        time.sleep(5)                          # a last look: it may have written on the way out
        if os.path.exists(TARGET) and os.path.getmtime(TARGET) > BASELINE:
            continue                           # let the landing branch above report it properly
        elapsed = int(time.time() - START)
        announce("DIED WITHOUT WRITING — THIS IS THE 15:05 FAILURE AGAIN",
                 f"pid {PID} left the process table after {elapsed}s and `{TARGET}` does not exist. "
                 f"The run is DEAD, not slow. Tail `work/a16_run3.log` for the last arm reached "
                 f"(it was on null-random when the watcher armed). Relaunch with Start-Process, "
                 f"never a shell background job — a shell child dies with the breath that spawned it, "
                 f"which is exactly what happened at 15:05 and went unseen for three and a half hours.")
        sys.exit(1)

    time.sleep(POLL_S)

announce("TIMED OUT — STILL RUNNING, NOT FINISHED",
         f"{MAX_WAIT_S}s elapsed, pid {PID} still alive, `{TARGET}` still absent. This is a genuine "
         f"unknown and is reported as one: the job is slower than expected, not dead. Check the log "
         f"and decide whether to keep waiting. Nothing was killed.")
sys.exit(2)
