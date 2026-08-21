"""PASS 8 BLOCK N -- the sec.9a re-test at n=20 instead of n=1.

Governed by PASS8_PREDICTIONS.md sec.2, committed and pushed (6567f2b) BEFORE
this file existed. Every threshold below is COPIED from that file.

  N1     >=1 of 20 images varies across 4 repeated IN-PROCESS extractions
  N2     EVERY image has spread 0 across 3 FRESH-PROCESS runs   <- load-bearing
  N3     <10 of 20 images show in-process variation             (low confidence)
  N4     structures M and D differ by >=1 object summed over 20 images
  N5     DIRECTIONAL: structure M yields the HIGHER frac_far
  N-NULL GATE: fresh runs 1 and 2 must be byte-identical, or N4/N5 are NOT
         scored. D201's rule (mem-2de96b0c): a re-run-and-diff gauge that has
         not run its own no-op is void in both directions.

** N-NULL and N2 are the same experiment scored for two different reasons.
   Declared in the prereg sec.2; neither is cited as support for the other. **

R2 applies here too: every gate records what it rejected.
"""
import json, glob, os, subprocess, sys, time
import numpy as np
import sep
from astropy.io import fits

THRESH, WALL, MINAREA = 5.0, 1.6, 5
IN_PROC_REPEATS = 4      # prereg sec.2 N1
FRESH_RUNS = 3           # prereg sec.2 N2
CHILD = "_nd_child.py"

REJ = {}


def gate(name, n_in, n_kept, note=""):
    d = REJ.setdefault(name, {"n_in": 0, "n_kept": 0, "n_rejected": 0, "note": note})
    d["n_in"] += int(n_in)
    d["n_kept"] += int(n_kept)
    d["n_rejected"] += int(n_in - n_kept)
    return d


def canonical_M_inproc(img, bad):
    """Structure M, in-process. Same sequence as _nd_child.py's M branch."""
    bkg0 = sep.Background(img, mask=bad)
    _ = img - bkg0.back()
    n = n_far = 0
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        o = sep.extract(arr - bkg.back(), THRESH, err=bkg.globalrms,
                        minarea=MINAREA, mask=bad)
        ok = o["b"] > 0
        gate("N_b_positive", len(o), int(ok.sum()), "sep semi-minor axis b > 0")
        e = o["a"][ok] / o["b"][ok]
        n += len(e)
        n_far += int((e > WALL).sum())
    return n, n_far


def child(path, structure):
    r = subprocess.run([sys.executable, CHILD, path, structure],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"child failed on {path}/{structure}:\n{r.stderr[-2000:]}")
    return json.loads(r.stdout.strip())


files = sorted(glob.glob("diffimg/*.fz"))
print("=" * 78)
print(f"BLOCK N -- sec.9a re-test over {len(files)} image(s)")
print("=" * 78)
gate("N_images_present", len(files), len(files), "diffimg/*.fz on disk")

out = {"prereg": "PASS8_PREDICTIONS.md", "prereg_commit": "6567f2b",
       "n_images": len(files), "per_image": {}}
t0 = time.time()

for p in files:
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img)
    img[bad] = 0.0

    # ---- in-process: repeated calls in ONE process (the varying condition)
    ip = [canonical_M_inproc(img, bad)[0] for _ in range(IN_PROC_REPEATS)]

    # ---- fresh: one image per process, FRESH_RUNS times
    fr = [child(p, "M") for _ in range(FRESH_RUNS)]
    fr_n = [d["n"] for d in fr]
    fr_far = [d["n_far"] for d in fr]

    # ---- structure D, fresh process, once
    dD = child(p, "D")

    row = dict(in_process=ip, in_process_spread=max(ip) - min(ip),
               fresh_M=fr_n, fresh_M_spread=max(fr_n) - min(fr_n),
               fresh_M_far=fr_far,
               struct_D_n=dD["n"], struct_D_far=dD["n_far"])
    out["per_image"][fn] = row
    print(f"  {fn[22:46]:24s} inproc {ip}  spread {row['in_process_spread']}"
          f" | fresh {fr_n} spread {row['fresh_M_spread']} | D {dD['n']}",
          flush=True)

R = out["per_image"]
n_vary_inproc = sum(1 for r in R.values() if r["in_process_spread"] > 0)
n_vary_fresh = sum(1 for r in R.values() if r["fresh_M_spread"] > 0)

V = {}
V["N1"] = bool(n_vary_inproc >= 1)
V["N2"] = bool(n_vary_fresh == 0)
V["N3"] = bool(n_vary_inproc < 10)

# ---------------- N-NULL: fresh run 1 vs run 2, all 20 images
null_mismatch = [fn for fn, r in R.items() if r["fresh_M"][0] != r["fresh_M"][1]]
V["N-NULL"] = bool(len(null_mismatch) == 0)
gate("N_null_pairs", len(R), len(R) - len(null_mismatch),
     "fresh run 1 == fresh run 2 (the no-op the gauge owes itself)")

# ---------------- N4 / N5: structure A/B, gated on N-NULL
M_n = sum(r["fresh_M"][0] for r in R.values())
D_n = sum(r["struct_D_n"] for r in R.values())
M_far = sum(r["fresh_M_far"][0] for r in R.values())
D_far = sum(r["struct_D_far"] for r in R.values())
ff_M = M_far / M_n if M_n else float("nan")
ff_D = D_far / D_n if D_n else float("nan")

if V["N-NULL"]:
    V["N4"] = bool(abs(M_n - D_n) >= 1)
    V["N5"] = bool(ff_M >= ff_D)
    n4_note = "scored"
else:
    V["N4"] = None
    V["N5"] = None
    n4_note = "NOT SCORED -- N-NULL failed, the diff gauge is void in both directions"

print("\n" + "-" * 78)
print(f"  images varying IN-PROCESS  : {n_vary_inproc} / {len(R)}")
print(f"  images varying FRESH       : {n_vary_fresh} / {len(R)}")
print(f"  N1  >=1 varies in-process        -> {'HELD' if V['N1'] else 'REFUTED'}")
print(f"  N2  fresh spread 0 on ALL images -> {'HELD' if V['N2'] else 'REFUTED'}"
      f"   ** load-bearing **")
print(f"  N3  in-process varies on <10     -> {'HELD' if V['N3'] else 'REFUTED'}")
print(f"  N-NULL fresh run1 == run2        -> {'PASS' if V['N-NULL'] else '**VOID**'}"
      f"   (gate, not counted)")
print(f"\n  structure M (measure_pass6): n = {M_n}   frac_far = {ff_M:.6f}")
print(f"  structure D (diag_pass6)   : n = {D_n}   frac_far = {ff_D:.6f}")
print(f"  |M - D| = {abs(M_n - D_n)} object(s)   frac_far delta = "
      f"{100*(ff_M - ff_D):+.4f} pp")
print(f"  N4  structures differ by >=1     -> {V['N4']}  [{n4_note}]")
print(f"  N5  M yields the higher frac_far -> {V['N5']}")

out.update(n_vary_inproc=n_vary_inproc, n_vary_fresh=n_vary_fresh,
           null_mismatch=null_mismatch,
           struct_M=dict(n=M_n, n_far=M_far, frac_far=ff_M),
           struct_D=dict(n=D_n, n_far=D_far, frac_far=ff_D),
           n_delta=int(M_n - D_n), frac_far_delta_pp=100.0 * (ff_M - ff_D),
           n4_status=n4_note, verdicts=V, rejections=REJ,
           elapsed_s=round(time.time() - t0, 1))

# ---------------- R2/R3: unexercised preconditions WARN
unex = [k for k, d in REJ.items() if d["n_rejected"] == 0]
out["unexercised"] = unex
if unex:
    print(f"\n  !! R3 WARNING -- gate(s) that rejected NOTHING: {unex}")
    print("     A precondition that has never rejected anything is not")
    print("     observably a precondition. Named, not silently trusted.")

json.dump(out, open("PASS8_NONDET.json", "w"), indent=2)
print(f"\nwrote PASS8_NONDET.json  ({out['elapsed_s']}s)")
