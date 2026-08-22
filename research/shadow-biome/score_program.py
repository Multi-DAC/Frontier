"""PROGRAM-WIDE SCORE — the arithmetic §10 is owed.

Day 202 / 2026-08-21 ~23:5x PT. No new science. One pass over every pre-registered
letter list this program has committed, scored against each pass's OWN declared
exclusion rule.

WHY THIS IS A SCRIPT AND NOT A HAND TALLY:
  A hand tally is a stamp. It is right once and rots silently the next time a pass
  lands. This recomputes from the per-pass artifacts every time it is run, and it
  CROSS-CHECKS its own hand-transcribed rows for passes 4-6 against the verdict
  tables in those passes' own markdown. Disagreement is a hard failure, not a note.

THE THREE THINGS THIS FIXES, all found by doing the arithmetic:
  1. LETTER COLLISIONS. Passes 5, 6 and 9 all use P1..P8. Pass 5's P2 HELD;
     pass 6's P2 was REFUTED. `PAPER-00-ARCHITECTURE.md` row 10 cites "P2 refuted"
     with no pass qualifier. Every key here is pass-qualified. Bare letters are
     ambiguous across this program and may not appear in the paper.
  2. L1's T5 IS SCORED NOWHERE MACHINE-READABLE. `L1_RESULTS.json /verdicts` has
     T1..T4 only. T5 was pre-registered in `PREREG-TERRESTRIAL.md:87` and scored
     REFUTED in `L1_T5_VERDICT.md:24`. The dict-only count therefore said 4/4 and
     the true L1 line is 4/5.
  3. CONTROLS ARE NOT FINDINGS. Every pass from 6 onward excluded its gates and
     controls from its own total. Applied uniformly here, backward too.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- kinds ------------------------------------------------------------------
PREREG = "prereg"        # committed before the data existed
DIAG = "diagnostic"      # minted after seeing an earlier pass, before its own run
CONTROL = "control"      # gate / positive control / identity check - EXCLUDED
UNEXERCISED = "unexercised"   # decision rule that never fired - EXCLUDED
COST = "cost"            # operational prediction (bytes, wall-clock), not science

SCORED_KINDS = {PREREG, DIAG, COST}

# --- passes 4-6: hand-transcribed, then cross-checked against their own tables
# Source lines cited so the transcription is auditable, not trusted.
HAND = {
    "pass4": {  # PASS4_RESULTS.md:44-50
        "M1": (False, PREREG),
        "M1b": (True, PREREG),
        "M1c-count": (True, PREREG),
        "M1c-survival": (True, PREREG),
        "M2": (False, PREREG),
        "M3": (True, PREREG),
        "M1d": (None, UNEXERCISED),   # "no prediction offered", explicitly unscored
    },
    "pass5": {  # PASS5_RESULTS.md:186-196
        "P1": (False, PREREG),
        "P2": (True, PREREG),
        "P3": (False, PREREG),
        "P4": (True, PREREG),
        "P5": (True, PREREG),
        "P6": (False, PREREG),
        "P7": (True, COST),           # download < 200 MB, extraction < 5 min
        "D1a": (False, DIAG),
        "D1b": (False, DIAG),
        "D1c": (True, DIAG),
        "D1d": (True, DIAG),
    },
    "pass6": {  # PASS6_RESULTS.md:82-85,125-140,158-165
        "P1": (False, PREREG),
        "P2": (False, PREREG),
        "P3": (False, PREREG),
        "P4": (True, PREREG),
        "P5": (True, PREREG),
        "P6": (True, PREREG),
        "P7": (False, PREREG),
        "P8": (True, PREREG),
        "D2a-1": (True, DIAG),
        "D2a-2": (True, DIAG),
        "D2a-3": (False, DIAG),
        "D2b-1": (False, DIAG),
        "D2b-2": (True, DIAG),
        "D2b-3": (False, DIAG),
        "D2c-1": (False, DIAG),
        "D2c-2": (True, DIAG),
        # C1/C2/C3 are synthetic-data gates (PASS6_PREDICTIONS.md:153-167). Not in
        # the 16. Recorded so their absence from the total is deliberate, not lost.
        "C1": (True, CONTROL),
        "C2": (True, CONTROL),
        "C3": (True, CONTROL),
    },
}

# --- passes 7-9 + L1: read the machine-readable dicts, classify the keys -----
KIND_7_9_L1 = {
    "pass7": {  # PASS7_RESULTS.md:8 - B3 is an identity control, excluded
        "B3": CONTROL,
    },
    "pass8": {  # PASS8_RESULTS.md:8 - D1, D4, N-NULL, R4-CONTROL excluded
        "D1": CONTROL, "N-NULL": CONTROL, "R4-CONTROL": CONTROL,
        "D4": UNEXERCISED,
    },
    "pass9": {  # PASS9_PREDICTIONS.md:238 - P0, S-NULL, C1, R4-CONTROL excluded
        "P0": CONTROL, "S-NULL": CONTROL, "C1": CONTROL, "R4-CONTROL": CONTROL,
    },
    "l1": {},
}

JSON_SOURCES = {
    "pass7": "PASS7_RESULTS.json",
    "pass8": "PASS8_RESULTS.json",
    "pass9": "PASS9_RESULTS.json",
    "l1": "L1_RESULTS.json",
}

# T5: pre-registered PREREG-TERRESTRIAL.md:87, scored REFUTED L1_T5_VERDICT.md:24,
# and absent from L1_RESULTS.json/verdicts. Injected here BECAUSE it is absent -
# that absence is itself finding #2 above.
INJECTED = {
    "l1": {"T5": (False, PREREG, "L1_T5_VERDICT.md:24 - absent from the JSON dict")},
}


def parse_md_table_verdicts(path):
    """Re-derive verdicts from a results markdown's own pipe tables.

    Independent route to the same numbers. Only rows whose cells contain an
    unambiguous HELD/REFUTED/FAILED token are returned.
    """
    out = {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        key = re.sub(r"[*`\s]", "", cells[0])
        if not re.fullmatch(r"[A-Z][A-Za-z0-9-]*", key or ""):
            continue
        joined = " ".join(cells[1:]).upper()
        has_held = "HELD" in joined
        has_ref = "REFUTED" in joined or "FAILED" in joined
        if has_held == has_ref:      # neither, or both -> not unambiguous
            continue
        out[key] = has_held
    return out


def main():
    rows = []          # (pass, key, held, kind)
    problems = []

    for p, keys in HAND.items():
        for k, (held, kind) in keys.items():
            rows.append((p, k, held, kind))

    for p, fname in JSON_SOURCES.items():
        verdicts = json.loads((HERE / fname).read_text(encoding="utf-8"))["verdicts"]
        for k, v in verdicts.items():
            kind = KIND_7_9_L1[p].get(k, UNEXERCISED if v is None else PREREG)
            rows.append((p, k, v, kind))
    for p, keys in INJECTED.items():
        for k, (held, kind, _why) in keys.items():
            rows.append((p, k, held, kind))

    # --- cross-check the hand transcription against each file's own tables ---
    for p, fname in (("pass4", "PASS4_RESULTS.md"),
                     ("pass5", "PASS5_RESULTS.md"),
                     ("pass6", "PASS6_RESULTS.md")):
        derived = parse_md_table_verdicts(HERE / fname)
        checked = 0
        for k, held in derived.items():
            if k not in HAND[p]:
                continue
            hand_held, kind = HAND[p][k]
            if kind in (CONTROL, UNEXERCISED):
                continue
            checked += 1
            if hand_held != held:
                problems.append(
                    f"{p}:{k} hand={hand_held} but {fname} table says {held}")
        if checked == 0:
            problems.append(f"{p}: cross-check matched ZERO rows in {fname} "
                            f"- the parser is narrowed, not the data clean")
        print(f"  cross-check {p}: {checked} row(s) re-derived from {fname}, "
              f"agreement {'OK' if not problems else 'SEE BELOW'}")

    # --- totals --------------------------------------------------------------
    def tally(sel):
        h = sum(1 for r in sel if r[2] is True)
        n = len(sel)
        return h, n

    print("\n" + "=" * 72)
    print("PROGRAM SCORE - pass-qualified, controls excluded")
    print("=" * 72)

    order = ["pass4", "pass5", "pass6", "pass7", "pass8", "pass9", "l1"]
    per_pass = {}
    for p in order:
        sel = [r for r in rows if r[0] == p and r[3] in SCORED_KINDS]
        pre = [r for r in sel if r[3] == PREREG]
        dia = [r for r in sel if r[3] == DIAG]
        cost = [r for r in sel if r[3] == COST]
        excl = [r for r in rows if r[0] == p and r[3] not in SCORED_KINDS]
        h, n = tally(sel)
        refuted = sorted(r[1] for r in sel if r[2] is False)
        per_pass[p] = {
            "held": h, "scored": n,
            "prereg": list(tally(pre)), "diagnostic": list(tally(dia)),
            "cost": list(tally(cost)),
            "excluded": sorted(r[1] for r in excl),
            "refuted": refuted,
        }
        print(f"{p:>6}  {h:>2}/{n:<2}   prereg {tally(pre)[0]}/{tally(pre)[1]}"
              f"   diag {tally(dia)[0]}/{tally(dia)[1]}"
              f"   cost {tally(cost)[0]}/{tally(cost)[1]}"
              f"   excluded {len(excl)}"
              f"   refuted: {', '.join(refuted) if refuted else '-'}")

    scored = [r for r in rows if r[3] in SCORED_KINDS]
    H, N = tally(scored)
    pre = [r for r in scored if r[3] == PREREG]
    dia = [r for r in scored if r[3] == DIAG]
    cost = [r for r in scored if r[3] == COST]
    hp, np_ = tally(pre)
    hd, nd = tally(dia)
    hc, nc = tally(cost)
    excluded_all = [r for r in rows if r[3] not in SCORED_KINDS]

    print("-" * 72)
    print(f"TOTAL            {H}/{N}  ({100.0*H/N:.1f}% held)")
    print(f"  pre-registered {hp}/{np_}  ({100.0*hp/np_:.1f}%)")
    print(f"  post-hoc diag  {hd}/{nd}  ({100.0*hd/nd:.1f}%)")
    print(f"  cost/ops       {hc}/{nc}")
    print(f"  excluded (controls, gates, unexercised): {len(excluded_all)}")
    print(f"  REFUTED, pass-qualified: "
          f"{', '.join(f'{r[0]}:{r[1]}' for r in scored if r[2] is False)}")

    # --- collision report: bare letters are ambiguous ------------------------
    from collections import defaultdict
    by_key = defaultdict(list)
    for r in scored:
        by_key[r[1]].append(r)
    collisions = {k: [(r[0], r[2]) for r in v] for k, v in by_key.items()
                  if len(v) > 1}
    split = {k: v for k, v in collisions.items()
             if len({h for _, h in v}) > 1}
    print(f"\nLETTER COLLISIONS: {len(collisions)} key(s) used by >1 pass; "
          f"{len(split)} of them disagree on the verdict.")
    for k, v in sorted(split.items()):
        print(f"  {k}: " + ", ".join(
            f"{p}={'HELD' if h else 'REFUTED'}" for p, h in v))

    # --- the era split: the number §10 actually has to explain ---------------
    # Passes 4-6 asked questions about ZTF's sky and data. Passes 7-9 + L1 asked
    # questions largely about our OWN extraction and our own artefact taxonomy.
    # If the hit-rate jumps at that boundary, the honest reading has two branches
    # and the flattering one is not automatically the right one.
    EARLY = {"pass4", "pass5", "pass6"}
    early = [r for r in scored if r[0] in EARLY]
    late = [r for r in scored if r[0] not in EARLY]
    he, ne = tally(early)
    hl, nl = tally(late)
    print(f"\nERA SPLIT (the number §10 must explain):")
    print(f"  passes 4-6 (about ZTF's data)     {he}/{ne}  ({100.0*he/ne:.1f}%)")
    print(f"  passes 7-9 + L1 (about our own)   {hl}/{nl}  ({100.0*hl/nl:.1f}%)")
    print(f"  swing: +{100.0*hl/nl - 100.0*he/ne:.1f} pp")

    out = {
        "era_split": {
            "early_passes_4_6": {"held": he, "scored": ne},
            "late_passes_7_9_L1": {"held": hl, "scored": nl},
            "note": "The early era tested claims about ZTF's data; the late era "
                    "tested claims largely about our own extraction and our own "
                    "artefact taxonomy. A rising hit-rate across that boundary is "
                    "AMBIGUOUS between calibration improving and the questions "
                    "getting closer to our own machinery. It may not be reported "
                    "as the first without the second printed beside it.",
        },
        "written": "D202 / 2026-08-21 ~23:5x PT",
        "generated_by": "score_program.py - recomputed, never transcribed",
        "convention": "each pass's own declared exclusion rule, applied uniformly "
                      "backward to passes 4-6",
        "total": {"held": H, "scored": N},
        "prereg": {"held": hp, "scored": np_},
        "diagnostic": {"held": hd, "scored": nd},
        "cost": {"held": hc, "scored": nc},
        "excluded_count": len(excluded_all),
        "refuted_pass_qualified": [f"{r[0]}:{r[1]}" for r in scored
                                   if r[2] is False],
        "per_pass": per_pass,
        "letter_collisions_disagreeing": {
            k: {p: bool(h) for p, h in v} for k, v in split.items()},
        "passes_1_3": "policy and instrument-specification only; five findings, "
                      "ZERO scorable predictions. Excluded from the denominator "
                      "and named here so the exclusion is not silent.",
        "cross_check_problems": problems,
    }
    (HERE / "PROGRAM_SCORE.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print("\nwrote PROGRAM_SCORE.json")

    if problems:
        print("\n" + "!" * 72)
        for pr in problems:
            print("  MISMATCH:", pr)
        print("!" * 72)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
