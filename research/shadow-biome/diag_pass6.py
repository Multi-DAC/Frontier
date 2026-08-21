"""PASS 6 DIAGNOSTICS D2 — dipoles, minarea, and frame-specific trailing.

Governed by PASS6_DIAGNOSTIC_PREDICTIONS.md, committed and pushed (685fa0c)
BEFORE this file was run. The hypotheses are POST-HOC and say so there.

Statistics are IMPORTED from pass6_stats, the same module measure_pass6.py
uses -- not reimplemented. The refactor that created that module was verified
by re-running measure_pass6.py and diffing PASS6_RESULTS.json (identical).

D2a runs off PASS6_catalog.npz. D2b re-extracts the 20 images already on disk
at five minarea values, reusing one background per (image, sign).
"""
import json, os, glob
import numpy as np
import sep
from astropy.io import fits

from pass6_stats import axial_R, axial_mean, nearest_neighbour_table

THRESH, MATCH, WALL = 5.0, 2.0, 1.6
PAIR_RADIUS = 10.0                      # D2a: "close" pair
MINAREA_LADDER = [2, 3, 5, 8, 12]       # D2b
res = {}

cat = np.load("PASS6_catalog.npz", allow_pickle=False)
X, Y, TH = cat["x"], cat["y"], cat["theta"]
EL, SG, IM = cat["elong"], cat["sign"], cat["image"]
frames = sorted(set(IM.tolist()))
print(f"catalogue: n = {len(EL)} detections across {len(frames)} frames\n")

# ==================================================================== D2a
print("--- D2a  DIPOLES  (close pairs within %.0f px) ---" % PAIR_RADIUS)
opp_n = opp_k = 0
exp_opp = 0.0
d_opp, d_same = [], []
d_all = []
for fn in frames:
    m = IM == fn
    x, y, th, sg, el = X[m], Y[m], TH[m], SG[m], EL[m]
    far = el > WALL
    idx, dist, delta, opp = nearest_neighbour_table(x, y, th, sg, PAIR_RADIUS)
    if idx.size == 0:
        continue
    sel = far[idx]                      # keep pairs whose ANCHOR is far-side
    if sel.sum() == 0:
        continue
    o, dl = opp[sel], delta[sel]
    opp_k += int(o.sum()); opp_n += int(o.size)
    d_opp.extend(dl[o].tolist()); d_same.extend(dl[~o].tolist())
    d_all.extend(dl.tolist())
    # C4: composition-matched null from THIS frame's far-side sign split
    nf = int(far.sum()); npos = int((sg[far] > 0).sum()); nneg = nf - npos
    if nf > 1:
        exp_opp += o.size * (2.0 * npos * nneg / (nf * (nf - 1.0)))

rate = opp_k / opp_n if opp_n else float("nan")
null = exp_opp / opp_n if opp_n else float("nan")
med_all = float(np.median(d_all)) if d_all else float("nan")
med_opp = float(np.median(d_opp)) if d_opp else float("nan")
med_same = float(np.median(d_same)) if d_same else float("nan")
D2a1 = rate >= 0.65
D2a2 = med_opp >= 70.0
D2a3 = (med_opp - med_same) >= 10.0
print(f"  far-side anchors with a neighbour <= {PAIR_RADIUS:.0f} px : n = {opp_n}")
print(f"  opposite-sign rate       : {100*rate:.2f}%   -> D2a-1 {'HELD' if D2a1 else 'REFUTED'} (>=65%)")
print(f"  C4 composition-matched null : {100*null:.2f}%   excess = {100*(rate-null):+.2f} pp")
print(f"  median |delta| all close pairs : {med_all:.2f} deg  (45 = uniform)")
print(f"  median |delta| opposite-sign   : {med_opp:.2f} deg (n={len(d_opp)})"
      f"  -> D2a-2 {'HELD' if D2a2 else 'REFUTED'} (>=70)")
print(f"  median |delta| same-sign       : {med_same:.2f} deg (n={len(d_same)})")
print(f"  opposite - same = {med_opp - med_same:+.2f} deg  -> D2a-3 "
      f"{'HELD' if D2a3 else 'REFUTED'} (>=10)")
res["D2a"] = dict(n_pairs=opp_n, opp_rate=rate, null_rate=null,
                  excess_pp=(rate - null) * 100 if opp_n else None,
                  med_all=med_all, med_opp=med_opp, med_same=med_same,
                  D2a1=bool(D2a1), D2a2=bool(D2a2), D2a3=bool(D2a3))

# ==================================================================== D2c
print("\n--- D2c  IS THE PREFERRED DIRECTION FRAME-SPECIFIC? ---")
rows = []
for fn in frames:
    m = IM == fn
    th, el = TH[m], EL[m]
    far = el > WALL
    rows.append(dict(image=fn, R_far=axial_R(th[far]), R_kept=axial_R(th[~far]),
                     dir_far=axial_mean(th[far]), dir_kept=axial_mean(th[~far])))
n_higher = sum(1 for r in rows if r["R_far"] > r["R_kept"])
dirs = np.radians(np.array([r["dir_far"] for r in rows], float))
R20 = float(abs(np.mean(np.exp(2j * dirs))))
spread = float(np.degrees(np.sqrt(-2.0 * np.log(R20))) / 2.0) if R20 > 0 else float("inf")
D2c1 = n_higher >= 15
D2c2 = spread >= 30.0
for r in rows:
    print(f"    {r['image'][22:44]}  R_far={r['R_far']:.3f} R_kept={r['R_kept']:.3f}"
          f"  dir_far={r['dir_far']:6.1f} deg")
print(f"  frames with R_far > R_kept : {n_higher}/20  -> D2c-1 {'HELD' if D2c1 else 'REFUTED'} (>=15)")
print(f"  circular spread of the 20 far-side directions : {spread:.2f} deg"
      f"  (uniform ~ 50)  -> D2c-2 {'HELD' if D2c2 else 'REFUTED'} (>=30)")
res["D2c"] = dict(n_R_far_higher=n_higher, R20=R20, spread_deg=spread,
                  per_frame=rows, D2c1=bool(D2c1), D2c2=bool(D2c2))

# ==================================================================== D2b
print("\n--- D2b  MINAREA LADDER (is 48.50%% a property of ZTF or of my parameter?) ---")
alerts = json.load(open("PASS5_alert_index.json"))
by_img = {}
for a in alerts:
    by_img.setdefault(a["f"], []).append(a)

ladder = {k: dict(n=0, n_far=0, rec=0, tot=0) for k in MINAREA_LADDER}
for p in sorted(glob.glob("diffimg/*.fz")):
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img); img[bad] = 0.0
    prep = []
    for sign, arr in ((+1, img), (-1, -img)):        # background computed ONCE
        bkg = sep.Background(arr, mask=bad)
        prep.append((np.ascontiguousarray(arr - bkg.back()), bkg.globalrms))
    al = by_img.get(fn, [])
    ax = np.array([a["x"] for a in al], float)
    ay = np.array([a["y"] for a in al], float)
    for ma in MINAREA_LADDER:
        xs, ys, es = [], [], []
        for sub, rms in prep:
            o = sep.extract(sub, THRESH, err=rms, minarea=ma, mask=bad)
            ok = o["b"] > 0
            xs.append(o["x"][ok]); ys.append(o["y"][ok]); es.append(o["a"][ok] / o["b"][ok])
        x = np.concatenate(xs); y = np.concatenate(ys); e = np.concatenate(es)
        ladder[ma]["n"] += len(e); ladder[ma]["n_far"] += int((e > WALL).sum())
        for j in range(len(al)):
            d = np.hypot(x + 1 - ax[j], y + 1 - ay[j])
            if d.size and d.min() <= MATCH:
                ladder[ma]["rec"] += 1
        ladder[ma]["tot"] += len(al)
    print(f"    {fn[22:44]} done", flush=True)

print(f"\n  {'minarea':>8} {'n':>8} {'frac_far':>10} {'recovery':>10}")
fr = {}
for ma in MINAREA_LADDER:
    d = ladder[ma]
    d["frac_far"] = d["n_far"] / d["n"] if d["n"] else float("nan")
    d["recovery"] = d["rec"] / d["tot"] if d["tot"] else float("nan")
    fr[ma] = d["frac_far"]
    print(f"  {ma:>8} {d['n']:>8} {d['frac_far']:>10.4f} {d['recovery']:>10.4f}")

D2b1 = ladder[2]["recovery"] >= 0.80
span = max(fr.values()) - min(fr.values())
D2b2 = span >= 0.05
seq = [fr[ma] for ma in MINAREA_LADDER]
D2b3 = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
print(f"\n  D2b-1 recovery at minarea=2 : {100*ladder[2]['recovery']:.2f}%"
      f"  -> {'HELD' if D2b1 else 'REFUTED'} (>=80%)")
print(f"  D2b-2 span of frac_far across ladder : {100*span:.2f} pp"
      f"  -> {'HELD' if D2b2 else 'REFUTED'} (>=5 pp)")
print(f"  D2b-3 frac_far increases with minarea : {['%.4f'%v for v in seq]}"
      f"  -> {'HELD' if D2b3 else 'REFUTED'}")
res["D2b"] = dict(ladder={str(k): ladder[k] for k in MINAREA_LADDER},
                  span=span, D2b1=bool(D2b1), D2b2=bool(D2b2), D2b3=bool(D2b3))

flags = dict(D2a1=D2a1, D2a2=D2a2, D2a3=D2a3, D2b1=D2b1, D2b2=D2b2,
             D2b3=D2b3, D2c1=D2c1, D2c2=D2c2)
res["summary"] = {k: bool(v) for k, v in flags.items()}
print(f"\n=== {sum(flags.values())}/8 diagnostic predictions HELD ===")
json.dump(res, open("PASS6_DIAG.json", "w"), indent=2)
print("wrote PASS6_DIAG.json")
