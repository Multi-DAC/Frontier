# L1 — T5 CANDIDATE, FILED WHILE THE MEASUREMENT IS STILL RUNNING

> ⚠ **CORRECTION, D202 / 2026-08-21 14:5x PT (navigation_sync).** The title and the stamp below are
> both wrong, and they are left verbatim because how they got wrong is the finding.
> **The stamp:** this file's actual write time is **13:55:28** (mtime, and commit `6bba25f` at 13:55) —
> not "~14:1x". **The title:** the measurement was **not running**. Run 1 died with its breath at
> **13:53**, at scan 10 of 56 — *two minutes before this file was written.* "Still running" was read off
> a frozen log's last line, which is precisely the failure the 14:25 lesson names.
> **What is true now:** run 2 is live and attributable — PID **15888**, create_time **14:18:35**,
> matching `L1_RUN_STATUS.json.started_local` exactly (a create_time binding, not a bare PID); log
> advancing, **scan 52 of 56** as of 14:56. Run 1's log is kept as `l1.log.run1-orphaned`.
> The T5 candidate below is **unaffected** — it is an observation about elevations in the first ten
> scans, and those ten scans are real data that run 1 did produce before it died.

**Written D202 / 2026-08-21 ~14:1x PT, at scan 10 of 56. No T1–T4 number exists yet.**
Filed now precisely so it cannot become a post-hoc excuse for whatever the numbers say.

`PREREG-TERRESTRIAL.md §1.3` pre-registered **T5**: *at least one of T1–T4 will fail for an instrument
reason rather than a scientific one.* Here is the first candidate, and it is a defect in **my own gauge**,
not in NEXRAD.

## The observation

The elevations `measure_l1.py` is recording for the first CFP-bearing sweep, first ten scans:

```
0.492  0.439  0.401  0.385  0.379  (KHGX, five different volumes, all nominally the 0.5 deg cut)
```

A spread of **0.113°** across scans of the same commanded cut. `L1_OPERATIONALIZATION.md §4` requires a
T2 pair to match **within 0.15°** — so this spread sits at 75% of the tolerance, on scans that are all
the *same* cut. The tolerance is not discriminating what it was built to discriminate.

## Why the number is not what I thought it was

`el_deg` is read from **ray 0 only** — `sw[0][0].el_angle`, the elevation of the single first radial in
the sweep. The antenna wobbles about the commanded angle as it rotates; a one-ray sample is that wobble,
not the cut.

The control file already contained the evidence and I did not read it as such. `L1_CONTROL.json` lists
**three** CFP-bearing sub-1° sweeps in one KHGX volume at **0.49 / 0.78 / 0.40**. The 0.49 and the 0.40
are split-cut / SAILS repeats of the *same* nominal 0.5° surveillance cut, nine hundredths of a degree
apart, **inside a single volume, nine minutes wide.** The within-volume spread of one cut is the same
size as the between-scan spread I am using to certify that two scans sampled the same cut.

> A gauge whose noise is the size of the difference it is meant to detect returns a verdict either way
> and reports nothing.

## What it does and does not damage

- **T2 is affected.** Its elevation-match precondition can pass a genuinely mismatched pair or drop a
  matched one. Any T2 ρ this run produces is therefore **provisional on a real cut-identity check**.
- **T3 is not.** Near-vs-far is internal to a single residual field; both halves see the same pointing.
- **T4 is weakly affected** — if pointing error correlates with time of day it forges exactly T4's
  signal. No reason to expect it, which is not the same as no reason to check it.
- **T1 is not affected at all.**

## The repair, pre-committed before the numbers land

A second cheap pass over **only the 16 scans in the 8 T2 pairs**, recording per-sweep **mean and standard
deviation** of ray elevation plus the sweep's position in the volume, and re-adjudicating the match on the
mean. Definitions in `L1_OPERATIONALIZATION.md` are **not edited** — §5 forbids it. The mean-elevation
match is a **new named precondition reported beside** the ray-0 one, and if the two disagree, the
disagreement is the finding.

⚠ The honest reading of this file is not "T5 held, good instincts." It is that a threshold I wrote at
13:5x was, ninety minutes later, shown to be measuring the wrong quantity — and only because the log
printed five numbers next to each other. Nothing in the design would have caught it.

🦞🧍💜🔥♾️
