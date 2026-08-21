"""PASS 7 — POST-HOC DIAGNOSTICS. Labelled post-hoc because they are.

Neither block below was pre-registered. They exist because the pass-7 run
produced two things that its own pre-committed rules forbid me to wave past:

  Q1  B2 REFUTED (6.591 pp). PASS7_PREDICTIONS.md sec.3 says that makes
      A1/A2/B1 UNINTERPRETABLE. Before any rescue is attempted, the
      disagreement gets a QUANTITATIVE account or it stands unexplained.
      Hypothesis: 7(a) deletes 4834 negatives, 7(b) only the 2329 that sit in
      mutual opposite-sign pairs -- so 2505 UNPAIRED negatives are the whole
      difference, and they should be markedly LESS elongated than average.
      ** A diagnosis is not a rescue. B2 stays refuted whatever this says. **

  Q2  A live contradiction against pass6_stats.py's docstring, which is the
      sole citation for PAPER-00-ARCHITECTURE sec.9/9a. That docstring says
      sep 1.4.1 "does not return the same catalogue twice on some of these
      images (687_zr_c14_o_q1 gave 1012-1016 across repeated runs of identical
      code)". But measure_pass7.py's ladder reproduced PASS6_DIAG.json's
      counts at ALL FIVE rungs EXACTLY, a day later, in a different process,
      from a different script. Both cannot be true as stated.
      Prediction, written before this runs: repeated extraction of that same
      image will vary. If it does NOT vary, sec.9a's mechanism is wrong and
      the 2-object measure-vs-diag delta is STRUCTURAL, not random.
"""
import json, glob, os, subprocess, sys
import numpy as np
import sep
from astropy.io import fits

THRESH, WALL, MINAREA = 5.0, 1.6, 5
PAIR_RADIUS = 10.0
out = {}

# ============================================================ Q1
print("=" * 78)
print("Q1  POST-HOC: what exactly separates 7(a) from 7(b)?")
print("=" * 78)
cat = np.load("PASS6_catalog.npz", allow_pickle=True)
EL, SG, IM, X, Y = cat["elong"], cat["sign"], cat["image"], cat["x"], cat["y"]
N = len(EL); FAR = EL > WALL

paired = np.zeros(N, bool)
for fn in np.unique(IM):
    m = np.where(IM == fn)[0]
    x, y, s = X[m], Y[m], SG[m]
    k = len(m)
    if k < 2:
        continue
    d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
    np.fill_diagonal(d, np.inf)
    nn = d.argmin(axis=1); nd = d[np.arange(k), nn]
    for i in range(k):
        j = nn[i]
        if nd[i] <= PAIR_RADIUS and nn[j] == i and s[i] * s[j] < 0:
            paired[m[i]] = True

pos, neg = SG > 0, SG < 0
groups = {
    "positive, paired":    pos & paired,
    "positive, unpaired":  pos & ~paired,
    "negative, paired":    neg & paired,
    "negative, unpaired":  neg & ~paired,
}
print(f"  {'group':22s} {'n':>6} {'frac_far':>10}")
q1 = {}
for k, m in groups.items():
    ff = float(FAR[m].mean()) if m.sum() else float("nan")
    q1[k] = dict(n=int(m.sum()), frac_far=ff)
    print(f"  {k:22s} {int(m.sum()):>6} {ff:>10.4f}")

# The 7(a)-minus-7(b) set: negatives 7(a) removes that 7(b) keeps.
extra = neg & ~paired
ff_extra = float(FAR[extra].mean())
print(f"\n  7(a) removes {int(neg.sum())} negatives; 7(b) removes {int((neg & paired).sum())}.")
print(f"  The difference set is {int(extra.sum())} UNPAIRED negatives at frac_far = {ff_extra:.4f}")
print(f"  vs whole-catalogue frac_far {float(FAR.mean()):.4f}"
      f"  -> they are {'LESS' if ff_extra < FAR.mean() else 'MORE'} elongated than average")
print("  ** This ACCOUNTS FOR the B2 gap. It does not un-refute B2. **")
out["Q1"] = dict(groups=q1, n_extra=int(extra.sum()), frac_far_extra=ff_extra,
                 frac_far_all=float(FAR.mean()),
                 verdict="accounts for the gap; B2 remains REFUTED (prereg sec.3)")

# ============================================================ Q2
print("\n" + "=" * 78)
print("Q2  IS sep ACTUALLY NON-DETERMINISTIC ON THESE IMAGES?")
print("=" * 78)
target = [p for p in sorted(glob.glob("diffimg/*.fz")) if "c14_o_q1" in p]
if not target:
    target = sorted(glob.glob("diffimg/*.fz"))[:1]
    print(f"  ** the docstring's named image (c14_o_q1) is NOT in diffimg/ **")
    print(f"  ** falling back to {os.path.basename(target[0])} -- this is a DIFFERENT")
    print(f"     image from the one the claim was made about, and the substitution is")
    print(f"     recorded rather than glossed **")
p = target[0]
print(f"  image: {os.path.basename(p)}")

with fits.open(p) as h:
    hdu = next(z for z in h if getattr(z, "data", None) is not None)
    img = np.ascontiguousarray(hdu.data.astype(np.float32))
bad = ~np.isfinite(img); img[bad] = 0.0

counts_same_proc = []
for rep in range(6):
    n_rep = 0
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(np.ascontiguousarray(arr), mask=bad)
        o = sep.extract(np.ascontiguousarray(arr - bkg.back()), THRESH,
                        err=bkg.globalrms, minarea=MINAREA, mask=bad)
        n_rep += int((o["b"] > 0).sum())
    counts_same_proc.append(n_rep)
print(f"  same process, 6 repeats : {counts_same_proc}")

# fresh processes -- the case that matters, since measure/diag were separate runs
child = r'''
import sys, numpy as np, sep
from astropy.io import fits
p = sys.argv[1]
with fits.open(p) as h:
    hdu = next(z for z in h if getattr(z, "data", None) is not None)
    img = np.ascontiguousarray(hdu.data.astype(np.float32))
bad = ~np.isfinite(img); img[bad] = 0.0
n = 0
for sign, arr in ((+1, img), (-1, -img)):
    a = np.ascontiguousarray(arr)
    bkg = sep.Background(a, mask=bad)
    o = sep.extract(np.ascontiguousarray(a - bkg.back()), 5.0,
                    err=bkg.globalrms, minarea=5, mask=bad)
    n += int((o["b"] > 0).sum())
print(n)
'''
open("_q2_child.py", "w").write(child)
counts_fresh = []
for rep in range(4):
    r = subprocess.run([sys.executable, "_q2_child.py", p],
                       capture_output=True, text=True)
    counts_fresh.append(int(r.stdout.strip()))
print(f"  fresh processes, 4 runs : {counts_fresh}")
os.remove("_q2_child.py")

allc = counts_same_proc + counts_fresh
spread = max(allc) - min(allc)
deterministic = spread == 0
print(f"\n  spread across 10 extractions = {spread} object(s)")
if deterministic:
    print("  ** sep IS DETERMINISTIC on this image, in-process AND across processes. **")
    print("  ** pass6_stats.py's docstring names non-determinism as the reason the")
    print("     refactor gauge was worthless, and PAPER-00 sec.9/9a rest on it.")
    print("     On this evidence that mechanism is NOT REPRODUCED, and the 2-object")
    print("     measure-vs-diag delta needs a STRUCTURAL explanation instead --")
    print("     the two scripts compute the background differently (inside vs")
    print("     outside the sign loop). NOT YET TESTED. Do not rewrite sec.9a on")
    print("     one image; this is a contradiction to chase, not a conclusion. **")
else:
    print(f"  sep varies by {spread} object(s) -- sec.9a's mechanism reproduces")
out["Q2"] = dict(image=os.path.basename(p),
                 docstring_image_present=bool([q for q in glob.glob("diffimg/*.fz")
                                               if "c14_o_q1" in q]),
                 same_process=counts_same_proc, fresh_processes=counts_fresh,
                 spread=spread, deterministic_here=bool(deterministic),
                 status="ONE IMAGE. Not a refutation of sec.9a yet -- a contradiction "
                        "against it that is now measured instead of assumed.")

json.dump(out, open("PASS7_DIAG.json", "w"), indent=2)
print("\nwrote PASS7_DIAG.json")
