#!/usr/bin/env python3
"""
check_canon.py -- a GAUGE for Meridian's value canonicalization, not a stamp.

VALUE_CANONICALIZATION.md (2026-04-15) resolved the value proliferation correctly and then sat
for 112 days while an arithmetic error inside the chapter it governs went unexamined. A canon
file cannot audit the thing it stamps. This script can, because it RECOMPUTES.

Two modes, and the first is the one that matters:

  --derivation   Recompute the c_s chain from the primitives in CANON.json and test every
                 numerical claim the monograph prints. String-matching would never have found
                 F1; only recomputation did.
  --files        Scan the tree for dead values living in files whose role forbids them.
  (default)      Both.

Exit 0 = clean. Exit 1 = a CANONICAL-role claim is false. Exit 2 = could not run (which is
NOT the same as clean, and is reported as its own state on purpose).

Usage:  python check_canon.py [--derivation] [--files] [--quiet] [--root DIR]
Run from anywhere; --root defaults to the Meridian tree above this file.
"""

import argparse
import json
import math
import os
import re
import sys
from fnmatch import fnmatch

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)          # .../Meridian
CANON_PATH = os.path.join(HERE, "CANON.json")

RED, YEL, GRN, DIM, OFF = "\033[31m", "\033[33m", "\033[32m", "\033[2m", "\033[0m"
if os.name == "nt" and not os.environ.get("WT_SESSION"):
    RED = YEL = GRN = DIM = OFF = ""          # cmd.exe eats ANSI; silence beats mojibake

failures = []
notes = []


def fail(code, msg):
    failures.append((code, msg))
    print(f"{RED}FAIL {code}{OFF}  {msg}")


def ok(code, msg):
    print(f"{GRN}ok   {code}{OFF}  {msg}")


def note(code, msg=None):
    if msg is None:
        code, msg = "  ", code
    notes.append(msg)
    print(f"{YEL}note {code}{OFF}  {msg}")


# ---------------------------------------------------------------- the physics

def q0(w0, Om):
    return Om / 2 + (1 - Om) * (1 + 3 * w0) / 2


def C_q(w0, Om):
    q = q0(w0, Om)
    return 2 * (1 - q) / (3 * abs(1 + q))


def c_s(w0, Om, eps1):
    return math.sqrt(C_q(w0, Om) / eps1)


def check_derivation(canon, quiet=False):
    """Recompute every printed number from the primitives. This is the real gauge."""
    Om = canon["primitives"]["Omega_m"]["value"]
    e0 = canon["primitives"]["eps1"]["value"]
    es = canon["primitives"]["eps1"]["sigma"]
    bm = canon["benchmarks"]

    print(f"\n{DIM}--- derivation (Omega_m={Om}, eps1={e0}+/-{es}) ---{OFF}")
    if not quiet:
        for name, b in bm.items():
            w = b["w0"]
            tag = "  <- CANONICAL single number" if b.get("CANONICAL_SINGLE_NUMBER") else ""
            print(f"       {name:<20} w0={w:<7} q0={q0(w, Om):+.4f}  C_q={C_q(w, Om):.4f}  "
                  f"c_s^2={C_q(w, Om)/e0:6.1f}  c_s={c_s(w, Om, e0):5.2f}c{tag}")

    # --- C1: does the printed box equal what the text says it is? -------------
    claim = canon["claims_under_test"]["boxed_range"]
    lo_bm, hi_bm = (bm[k]["w0"] for k in claim["benchmark_span_used_by_ch5"])
    span_bench = sorted([c_s(lo_bm, Om, e0), c_s(hi_bm, Om, e0)])
    span_both = sorted([c_s(lo_bm, Om, e0 + es), c_s(hi_bm, Om, e0 - es)])
    printed = claim["printed"]

    def rounds_to(span, box):
        return math.floor(span[0]) == box[0] and math.ceil(span[1]) == box[1]

    combines = set(claim["text_claims_it_combines"])
    if combines == {"benchmark_spread"}:
        truth, label = span_bench, "benchmark spread only"
    else:
        truth, label = span_both, "eps1 + benchmark, as the text claims"

    if rounds_to(truth, printed):
        ok("C1", f"boxed range {printed} == {label} [{truth[0]:.2f},{truth[1]:.2f}]")
    else:
        fail("C1", f"boxed range {printed} does NOT contain its stated inputs.\n"
                   f"           text at {claim['where_claimed'][0]} says it combines "
                   f"{sorted(combines)}, which gives [{span_both[0]:.2f}c, {span_both[1]:.2f}c].\n"
                   f"           the printed box is the benchmark spread alone: "
                   f"[{span_bench[0]:.2f}c, {span_bench[1]:.2f}c].\n"
                   f"           quoted width {printed[1]-printed[0]}c vs honest "
                   f"{span_both[1]-span_both[0]:.2f}c -- understated "
                   f"{100*(1-(printed[1]-printed[0])/(span_both[1]-span_both[0])):.0f}%. "
                   f"See CS_AUDIT_2026-08-05.md F1.")

    # --- C2: is the headline evaluated at the designated benchmark? -----------
    h = canon["claims_under_test"]["headline_cs2"]
    canonical = next(k for k, v in bm.items() if v.get("CANONICAL_SINGLE_NUMBER"))
    used = h["benchmark_it_actually_uses"]
    cs2_canon = C_q(bm[canonical]["w0"], Om) / e0
    cs2_used = C_q(bm[used]["w0"], Om) / e0
    if used == canonical:
        ok("C2", f"headline c_s^2={h['printed']} is at the canonical benchmark ({canonical})")
    else:
        fail("C2", f"headline c_s^2={h['printed']} is evaluated at '{used}' "
                   f"(c_s^2={cs2_used:.1f}), but the canon designates '{canonical}' "
                   f"(c_s^2={cs2_canon:.1f}). Difference "
                   f"{100*abs(cs2_used-cs2_canon)/cs2_canon:.1f}% -- physically nil, "
                   f"bookkeeping real. See F2.")

    # --- C3: does the printed headline follow from the primitives at all? -----
    if abs(cs2_used - h["printed"]) / h["printed"] < 0.01:
        ok("C3", f"printed {h['printed']} reproduces from primitives at '{used}' "
                 f"({cs2_used:.1f}) -- Omega_m={Om} is the value ch5 silently uses")
    else:
        fail("C3", f"printed c_s^2={h['printed']} does not reproduce from ANY primitive set "
                   f"({used} gives {cs2_used:.1f}). Someone changed a primitive without "
                   f"re-deriving, or the chapter uses an undocumented Omega_m.")

    # --- C4: which uncertainty actually dominates, in c_s? --------------------
    # apples-to-apples: half-width about the GEOMETRIC mean, since c_s is multiplicative in both.
    # (Comparing a half-width about the central value against a full span is how tab:5-2's
    #  'dominant/subleading' got written -- so do not repeat it here.)
    d_eps = math.sqrt(math.sqrt((e0 + es) / (e0 - es))) - 1
    ratio = C_q(hi_bm, Om) / C_q(lo_bm, Om)
    d_bench = math.sqrt(math.sqrt(ratio)) - 1
    verdict = canon["claims_under_test"]["uncertainty_dominance"]
    comparable = abs(d_eps - d_bench) < 0.05
    if comparable and "FALSE" in verdict["VERDICT"]:
        ok("C4", f"eps1 spread {100*d_eps:.1f}% vs benchmark {100*d_bench:.1f}% in c_s "
                 f"-- comparable, and tab:5-2's 'dominant/subleading' is correctly "
                 f"flagged FALSE in CANON.json")
    elif comparable:
        fail("C4", f"tab:5-2 calls eps1 dominant, but in c_s it is {100*d_eps:.1f}% "
                   f"vs benchmark {100*d_bench:.1f}%. See F4.")
    else:
        note(f"C4 dominance shifted: eps1 {100*d_eps:.1f}% vs benchmark {100*d_bench:.1f}% "
             f"-- CANON.json's verdict may need revisiting")

    # --- C5: the label collision on 'JC' -------------------------------------
    jc = bm.get("spectral_chain_JC", {}).get("w0")
    ceff = bm.get("Ceff_band_lower", {}).get("w0")
    if jc is not None and ceff is not None and jc != ceff:
        edge = c_s(jc, Om, e0)
        if math.floor(edge) != printed[0]:
            fail("C5", f"the two benchmarks sharing the label 'JC' disagree: w0={jc} gives "
                       f"c_s={edge:.2f}c (floor {math.floor(edge)}), w0={ceff} gives "
                       f"c_s={c_s(ceff, Om, e0):.2f}c. The box's lower edge "
                       f"{printed[0]} survives only on ch5's choice. See F3.")
        else:
            ok("C5", "'JC' label collision no longer changes the box's lower edge")


# ---------------------------------------------------------------- the files

def role_of(relpath, roles):
    rp = relpath.replace("\\", "/")
    for role, globs in roles.items():
        for g in globs:
            if fnmatch(rp, g) or fnmatch(rp, "*/" + g) or fnmatch(rp, g.replace("**/", "*")):
                return role
    return "UNCLASSIFIED"


SKIP_EXT = {".log", ".aux", ".pdf", ".toc", ".out", ".lof", ".png", ".jpg", ".pyc", ".txt"}
SKIP_DIR = {".git", "figures", "__pycache__", "node_modules"}


def check_files(canon, root, quiet=False):
    print(f"\n{DIM}--- files (root: {root}) ---{OFF}")
    roles = canon["file_roles"]
    dead = [(re.compile(d["pattern"]), d) for d in canon["dead_values"]]
    markers = canon["marked_context_markers"]
    hits, scanned = 0, 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            if os.path.splitext(fn)[1].lower() not in (".tex", ".md", ".py", ".json"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            role = role_of(rel, roles)
            if role in ("SUPERSEDED", "HISTORICAL", "CANON_SELF"):
                continue                       # allowed to hold dead values, by definition
            scanned += 1
            try:
                text = open(full, encoding="utf-8", errors="replace").read()
            except OSError as e:
                note(f"unreadable: {rel} ({e})")
                continue
            per_file = {}                      # era -> [line numbers]
            for ln, line in enumerate(text.splitlines(), 1):
                if any(m in line for m in markers):
                    continue                   # explicitly marked as historical, in context
                for rx, d in dead:
                    if rx.search(line):
                        hits += 1
                        per_file.setdefault(d["era"], []).append(ln)
            for era, lns in per_file.items():   # one line per file+era, not per hit
                msg = (f"{role} file holds {len(lns)} unmarked dead value(s) [{era}]: "
                       f"{rel}:{','.join(str(n) for n in lns)}")
                (fail if role == "CANONICAL" else note)("F", msg)
    if hits == 0:
        ok("F0", f"{scanned} canonical/unclassified files scanned, no unmarked dead values")
    else:
        print(f"{DIM}       {hits} hit(s) across {scanned} scanned files{OFF}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--derivation", action="store_true")
    ap.add_argument("--files", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--root", default=DEFAULT_ROOT)
    a = ap.parse_args()
    if not (a.derivation or a.files):
        a.derivation = a.files = True

    try:
        canon = json.load(open(CANON_PATH, encoding="utf-8"))
    except Exception as e:
        print(f"{RED}CANNOT RUN{OFF}  {CANON_PATH}: {e}")
        print("           This is exit 2, not exit 0. Absence of a check is not a pass.")
        return 2

    print(f"{DIM}CANON.json updated {canon['_updated']}{OFF}")
    if a.derivation:
        check_derivation(canon, a.quiet)
    if a.files:
        check_files(canon, a.root, a.quiet)

    print()
    if failures:
        print(f"{RED}{len(failures)} FAILURE(S){OFF} -- see CS_AUDIT_2026-08-05.md")
        print("   Expected on 2026-08-05: C1, C2, C5 fail. They are the audit's open findings.")
        print("   When they are fixed in the .tex, this script goes green ON ITS OWN.")
        return 1
    print(f"{GRN}clean{OFF}" + (f" ({len(notes)} note(s))" if notes else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
