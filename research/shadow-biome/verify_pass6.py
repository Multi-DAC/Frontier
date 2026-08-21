"""PASS 6 VERIFICATION — two things I owe before writing anything up.

POST-HOC and labelled as such. Neither is a new claim; both are attacks on my
own pass-6 result, which is why they do not need pre-registration to be honest.

V1. THE COUNT DISCREPANCY. measure_pass6.py reported n = 8528 detections at
    minarea=5. diag_pass6.py's minarea ladder reported n = 8526 at the same
    minarea with what should be identical extraction. A 0.023% gap is exactly
    the "unremarkable number I was about to use" that today's own lesson says
    to chase. Recompute both code paths in one process, per image.

V2. THE MISSING CONTROL for D2a. I measured that 96.25% of far-side close
    pairs are opposite-sign against a 47.21% composition-matched null -- and
    never asked whether the KEPT side does the same thing. If it does, "the far
    side is dipoles" is not a statement about the far side at all.
"""
import json, os, glob
import numpy as np
import sep
from astropy.io import fits

from pass6_stats import nearest_neighbour_table

THRESH, MINAREA, WALL, PAIR_RADIUS = 5.0, 5, 1.6, 10.0

# ============================================================ V1
print("--- V1  COUNT DISCREPANCY: 8528 (measure) vs 8526 (diag) ---")
tot_a = tot_b = 0
for p in sorted(glob.glob("diffimg/*.fz")):
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img); img[bad] = 0.0

    # path A -- exactly measure_pass6.py: a fresh Background per sign, and a
    # PRIOR sep.Background(img) call made before the loop for local S/N.
    _bkg0 = sep.Background(img, mask=bad)
    _sub0, _rms0 = img - _bkg0.back(), _bkg0.globalrms
    na = 0
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        o = sep.extract(arr - bkg.back(), THRESH, err=bkg.globalrms,
                        minarea=MINAREA, mask=bad)
        na += int((o["b"] > 0).sum())

    # path B -- exactly diag_pass6.py: backgrounds precomputed into a list,
    # subtracted images made contiguous, then extract per minarea.
    prep = []
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        prep.append((np.ascontiguousarray(arr - bkg.back()), bkg.globalrms))
    nb = 0
    for sub, rms in prep:
        o = sep.extract(sub, THRESH, err=rms, minarea=MINAREA, mask=bad)
        nb += int((o["b"] > 0).sum())

    tot_a += na; tot_b += nb
    if na != nb:
        print(f"    DIFFERS  {fn[22:44]}  measure-path={na}  diag-path={nb}  ({na-nb:+d})")
print(f"  totals: measure-path = {tot_a}   diag-path = {tot_b}   delta = {tot_a-tot_b:+d}")
print(f"  -> {'RESOLVED: the two paths differ' if tot_a != tot_b else 'NOT REPRODUCED in one process'}")

# ============================================================ V2
print("\n--- V2  D2a KEPT-SIDE CONTROL (the control I failed to pre-register) ---")
cat = np.load("PASS6_catalog.npz", allow_pickle=False)
X, Y, TH, EL, SG, IM = (cat["x"], cat["y"], cat["theta"],
                        cat["elong"], cat["sign"], cat["image"])
frames = sorted(set(IM.tolist()))

out = {}
for label, want_far in (("far", True), ("kept", False)):
    k = n = 0
    exp = 0.0
    deltas = []
    anchors_total = 0
    for fn in frames:
        m = IM == fn
        x, y, th, sg, el = X[m], Y[m], TH[m], SG[m], EL[m]
        side = (el > WALL) if want_far else (el <= WALL)
        anchors_total += int(side.sum())
        idx, dist, delta, opp = nearest_neighbour_table(x, y, th, sg, PAIR_RADIUS)
        if idx.size == 0:
            continue
        sel = side[idx]
        if sel.sum() == 0:
            continue
        o, dl = opp[sel], delta[sel]
        k += int(o.sum()); n += int(o.size); deltas.extend(dl.tolist())
        ns = int(side.sum()); npos = int((sg[side] > 0).sum()); nneg = ns - npos
        if ns > 1:
            exp += o.size * (2.0 * npos * nneg / (ns * (ns - 1.0)))
    out[label] = dict(anchors=anchors_total, paired=n,
                      paired_share=n / anchors_total if anchors_total else float("nan"),
                      opp_rate=k / n if n else float("nan"),
                      null=exp / n if n else float("nan"),
                      med_delta=float(np.median(deltas)) if deltas else float("nan"),
                      opp_share_of_side=k / anchors_total if anchors_total else float("nan"))
    d = out[label]
    print(f"  {label:5s}: anchors={d['anchors']:5d}  with a neighbour<= {PAIR_RADIUS:.0f}px="
          f"{d['paired']:5d} ({100*d['paired_share']:5.2f}%)")
    print(f"         opposite-sign rate={100*d['opp_rate']:6.2f}%  null={100*d['null']:6.2f}%"
          f"  excess={100*(d['opp_rate']-d['null']):+6.2f} pp   median|delta|={d['med_delta']:.2f} deg")
    print(f"         => {100*d['opp_share_of_side']:.2f}% of the {label} side sits in an"
          f" opposite-sign pair within {PAIR_RADIUS:.0f} px")

diff = out["far"]["opp_share_of_side"] - out["kept"]["opp_share_of_side"]
print(f"\n  far-minus-kept share in opposite-sign close pairs = {100*diff:+.2f} pp")
print("  -> the dipole reading is FAR-SIDE SPECIFIC" if diff > 0.10 else
      "  -> the dipole reading is NOT specific to the far side; it describes the whole catalogue")

json.dump(dict(V1=dict(measure_path=tot_a, diag_path=tot_b, delta=tot_a - tot_b),
               V2=out, far_minus_kept=diff),
          open("PASS6_VERIFY.json", "w"), indent=2)
print("\nwrote PASS6_VERIFY.json")
