"""PASS 6 — is the far side of ZTF's elong<=1.6 cut INSTRUMENTAL?

Governed by PASS6_PREDICTIONS.md, committed and pushed (f3c51a5) BEFORE this
file was run. Every threshold below is copied from that file, not chosen here.

Downloads nothing: the 20 difference images are already in diffimg/ from pass 5.

Three shape tests (P1 axis alignment, P2 streak collinearity, P3 bright-source
proximity), each scored against the KEPT side measured by the same code so my
extractor's own biases -- including pixel-grid quantisation of theta at minimum
area -- sit on both sides of the comparison. Plus P4 per-frame heterogeneity,
and P5-P8, the classification of pass 5's unexplained 41% control miss.

Angles are AXIAL (mod 180 deg). All circular statistics are on 2*theta.
"""
import json, os, glob
import numpy as np
import sep
from astropy.io import fits

# Statistics live in pass6_stats so diag_pass6.py reuses the SAME functions by
# import rather than by copy (PASS6_DIAGNOSTIC_PREDICTIONS.md, Controls).
from pass6_stats import (AXIS_DEG, BRIGHT_PCT, NN_RADIUS,
                         axial_R, axis_fraction, collinearity, bright_proximity)

# ------------------------------------------------ PASS6_PREDICTIONS.md sec.1
THRESH, MINAREA, MATCH = 5.0, 5, 2.0
BOX         = 2        # half-width -> 5x5 box for local S/N
WALL        = 1.6      # ZTF's own packaging cut
SEED        = 12345    # controls only; fixed so C1/C2 are reproducible

CHANCE_AXIS = 2 * AXIS_DEG / 90.0     # = 0.2222


# ---------------------------------------------------------------- CONTROLS
# Run FIRST. PASS6_PREDICTIONS.md sec.4: all three must pass or sec.2 is
# reported UNINTERPRETABLE. A gauge that has only ever rendered one verdict
# is furniture.
rng = np.random.default_rng(SEED)
c1_theta = rng.vonmises(0.0, 2.0, 1000) / 2.0            # kappa=2 on 2*theta
C1_R = axial_R(c1_theta)
c2_theta = rng.uniform(-np.pi / 2, np.pi / 2, 1000)
C2_R = axial_R(c2_theta)
_t = np.linspace(0, 400, 200)
_ang = np.radians(31.7)                                   # arbitrary, not axis-aligned
C3_med, C3_n = collinearity(_t * np.cos(_ang), _t * np.sin(_ang),
                            np.full(200, _ang))
C1 = C1_R > 0.30
C2 = C2_R < 0.10
C3 = C3_med < 10.0
CTRL_OK = C1 and C2 and C3
print("--- CONTROLS (PASS6_PREDICTIONS.md sec.4) ---")
print(f"  C1 can detect alignment   R = {C1_R:.4f}  (need > 0.30)  -> {'PASS' if C1 else 'FAIL'}")
print(f"  C2 does not false-alarm   R = {C2_R:.4f}  (need < 0.10)  -> {'PASS' if C2 else 'FAIL'}")
print(f"  C3 can detect collinearity med|d| = {C3_med:.4f} deg (need < 10)  -> {'PASS' if C3 else 'FAIL'}")
print(f"  -> section 2 is {'INTERPRETABLE' if CTRL_OK else '**UNINTERPRETABLE**'}\n")

# ------------------------------------------------------------------ alerts
alerts = json.load(open("PASS5_alert_index.json"))
by_img = {}
for a in alerts:
    by_img.setdefault(a["f"], []).append(a)

# ------------------------------------------------------------- extraction
X_, Y_, TH_, A_, B_, EL_, PK_, FL_, NP_, FG_, SN_, SG_, IM_ = ([] for _ in range(13))
per_frame = []
miss_rows = []

files = sorted(glob.glob("diffimg/*.fz"))
print(f"--- EXTRACTION: {len(files)} images already on disk ---")
for p in files:
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img)
    img[bad] = 0.0
    H, W = img.shape

    bkg0 = sep.Background(img, mask=bad)          # for local S/N at alert positions
    sub0, rms0 = img - bkg0.back(), bkg0.globalrms

    fx, fy, fth, fa, fb, fpk, ffl, fnp, ffg, fsn, fsg = ([] for _ in range(11))
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        o = sep.extract(arr - bkg.back(), THRESH, err=bkg.globalrms,
                        minarea=MINAREA, mask=bad)
        ok = o["b"] > 0
        fx.append(o["x"][ok]);    fy.append(o["y"][ok])
        fth.append(o["theta"][ok])
        fa.append(o["a"][ok]);    fb.append(o["b"][ok])
        fpk.append(o["peak"][ok]); ffl.append(o["flux"][ok])
        fnp.append(o["npix"][ok]); ffg.append(o["flag"][ok])
        fsn.append(o["peak"][ok] / bkg.globalrms)
        fsg.append(np.full(int(ok.sum()), sign))

    x = np.concatenate(fx); y = np.concatenate(fy); th = np.concatenate(fth)
    a = np.concatenate(fa); b = np.concatenate(fb)
    pk = np.concatenate(fpk); fl = np.concatenate(ffl)
    npx = np.concatenate(fnp); fg = np.concatenate(ffg)
    sn = np.concatenate(fsn); sg = np.concatenate(fsg)
    el = a / b

    X_.append(x); Y_.append(y); TH_.append(th); A_.append(a); B_.append(b)
    EL_.append(el); PK_.append(pk); FL_.append(fl); NP_.append(npx)
    FG_.append(fg); SN_.append(sn); SG_.append(sg)
    IM_.append(np.full(len(el), fn))

    far = el > WALL
    kept = ~far
    fm, fn_n = collinearity(x[far], y[far], th[far])
    km, kn_n = collinearity(x[kept], y[kept], th[kept])
    dfar = bright_proximity(x, y, pk, far)
    dkept = bright_proximity(x, y, pk, kept)
    per_frame.append(dict(
        image=fn, n=int(len(el)), n_far=int(far.sum()),
        frac_far=float(far.mean()),
        axis_far=axis_fraction(th[far]), axis_kept=axis_fraction(th[kept]),
        R_far=axial_R(th[far]), R_kept=axial_R(th[kept]),
        collin_far=fm, collin_kept=km,
        med_bright_far=float(np.median(dfar)) if dfar.size else float("nan"),
        med_bright_kept=float(np.median(dkept)) if dkept.size else float("nan"),
    ))

    # ------------------- the 41%: classify EVERY alert on this frame -------
    for al in by_img.get(fn, []):
        ax, ay = al.get("x"), al.get("y")
        row = dict(image=fn, magpsf=al.get("magpsf"), rb=al.get("rb"),
                   isdiffpos=al.get("isdiffpos"), elong=al.get("elong"))
        if ax is None or ay is None:
            row.update(cls="NO_POSITION", recovered=False, nn=None, snr=None)
            miss_rows.append(row); continue
        d = np.hypot(x + 1 - ax, y + 1 - ay)      # FITS 1-indexed, as pass 5
        nn = float(d.min())
        rec = nn <= MATCH
        ci, ri = int(round(ax - 1)), int(round(ay - 1))     # -> 0-indexed array
        if not (0 <= ci < W and 0 <= ri < H):
            cls, snr_loc = "OUT_OF_BOUNDS", None
        else:
            r0, r1 = max(0, ri - BOX), min(H, ri + BOX + 1)
            c0, c1 = max(0, ci - BOX), min(W, ci + BOX + 1)
            if bad[r0:r1, c0:c1].any():
                cls, snr_loc = "MASKED", None
            else:
                snr_loc = float(np.abs(sub0[r0:r1, c0:c1]).max() / rms0)
                if rec:
                    cls = "RECOVERED"
                elif snr_loc < THRESH:
                    cls = "BELOW_THRESHOLD"
                elif nn <= 5.0:
                    cls = "NEAR_MISS_RADIUS"
                else:
                    cls = "UNEXTRACTED_DESPITE_FLUX"
        if rec and cls not in ("OUT_OF_BOUNDS", "MASKED"):
            cls = "RECOVERED"
        row.update(cls=cls, recovered=bool(rec), nn=nn, snr=snr_loc)
        miss_rows.append(row)

    print(f"    {fn[:44]}  n={len(el):5d}  far={int(far.sum()):5d}"
          f"  axis_far={axis_fraction(th[far]):.3f}  collin_far={fm:.1f}", flush=True)

X = np.concatenate(X_); Y = np.concatenate(Y_); TH = np.concatenate(TH_)
A = np.concatenate(A_); B = np.concatenate(B_); EL = np.concatenate(EL_)
PK = np.concatenate(PK_); FLX = np.concatenate(FL_); NPX = np.concatenate(NP_)
FG = np.concatenate(FG_); SN = np.concatenate(SN_); SG = np.concatenate(SG_)
IM = np.concatenate(IM_)
N = len(EL)
np.savez_compressed("PASS6_catalog.npz", x=X, y=Y, theta=TH, a=A, b=B, elong=EL,
                    peak=PK, flux=FLX, npix=NPX, flag=FG, snr=SN, sign=SG, image=IM)
print(f"\nextraction: n = {N} detections; wrote PASS6_catalog.npz "
      f"(pass 5 saved only elong/peak/sign/image, which is why this pass had to re-extract)")

FAR, KEPT = EL > WALL, EL <= WALL
res = dict(n=int(N), n_far=int(FAR.sum()), n_kept=int(KEPT.sum()),
           frac_far=float(FAR.mean()),
           controls=dict(C1_R=C1_R, C2_R=C2_R, C3_med_deg=C3_med,
                         C1=bool(C1), C2=bool(C2), C3=bool(C3),
                         interpretable=bool(CTRL_OK)),
           per_frame=per_frame)

# ------------------------------------------------------------- P1 axis
p1_far, p1_kept = axis_fraction(TH[FAR]), axis_fraction(TH[KEPT])
P1 = (0.22 <= p1_far <= 0.40) and (p1_far - p1_kept >= 0.05)
print("\n--- P1 AXIS ALIGNMENT (chance = %.4f) ---" % CHANCE_AXIS)
print(f"  far side  : {p1_far:.4f}  (n={int(FAR.sum())})   axial R = {axial_R(TH[FAR]):.4f}")
print(f"  kept side : {p1_kept:.4f}  (n={int(KEPT.sum())})   axial R = {axial_R(TH[KEPT]):.4f}")
print(f"  excess far-kept = {p1_far - p1_kept:+.4f}   -> P1 {'HELD' if P1 else 'REFUTED'}")
res["P1"] = dict(far=p1_far, kept=p1_kept, excess=p1_far - p1_kept,
                 R_far=axial_R(TH[FAR]), R_kept=axial_R(TH[KEPT]),
                 chance=CHANCE_AXIS, held=bool(P1))

# ------------------------------------------------------ P2 collinearity
cf = np.array([f["collin_far"] for f in per_frame], float)
ck = np.array([f["collin_kept"] for f in per_frame], float)
p2_far, p2_kept = float(np.nanmedian(cf)), float(np.nanmedian(ck))
P2 = (p2_far < 40.0) and (p2_kept - p2_far >= 3.0)
print("\n--- P2 STREAK COLLINEARITY (uniform = 45 deg) ---")
print(f"  far side  median |delta| : {p2_far:.3f} deg   (median over {len(cf)} frames)")
print(f"  kept side median |delta| : {p2_kept:.3f} deg")
print(f"  kept-far = {p2_kept - p2_far:+.3f} deg   -> P2 {'HELD' if P2 else 'REFUTED'}")
res["P2"] = dict(far_deg=p2_far, kept_deg=p2_kept,
                 delta=p2_kept - p2_far, held=bool(P2))

# --------------------------------------------------- P3 bright proximity
bf = np.array([f["med_bright_far"] for f in per_frame], float)
bk = np.array([f["med_bright_kept"] for f in per_frame], float)
p3_far, p3_kept = float(np.nanmedian(bf)), float(np.nanmedian(bk))
ratio = p3_far / p3_kept if p3_kept else float("nan")
P3 = ratio < 0.90
print("\n--- P3 BRIGHT-SOURCE PROXIMITY ---")
print(f"  far side  median distance to nearest bright : {p3_far:.2f} px")
print(f"  kept side median distance to nearest bright : {p3_kept:.2f} px")
print(f"  ratio far/kept = {ratio:.4f}   -> P3 {'HELD' if P3 else 'REFUTED'} (<0.90)")
res["P3"] = dict(far_px=p3_far, kept_px=p3_kept, ratio=ratio, held=bool(P3))

# ------------------------------------------------- P4 frame heterogeneity
ff = np.array([f["frac_far"] for f in per_frame], float)
iqr = float(np.percentile(ff, 75) - np.percentile(ff, 25))
P4 = iqr > 0.10
print("\n--- P4 PER-FRAME HETEROGENEITY ---")
print(f"  far-side fraction per frame: min={ff.min():.4f} q1={np.percentile(ff,25):.4f} "
      f"med={np.median(ff):.4f} q3={np.percentile(ff,75):.4f} max={ff.max():.4f}")
print(f"  IQR = {iqr:.4f}   -> P4 {'HELD' if P4 else 'REFUTED'} (>0.10)")
res["P4"] = dict(iqr=iqr, min=float(ff.min()), max=float(ff.max()),
                 median=float(np.median(ff)), held=bool(P4))

# ------------------------------------------------------------ P5-P8: 41%
cls_counts = {}
for r in miss_rows:
    cls_counts[r["cls"]] = cls_counts.get(r["cls"], 0) + 1
n_alerts = len(miss_rows)
n_rec = sum(1 for r in miss_rows if r["cls"] == "RECOVERED")
unrec = [r for r in miss_rows if r["cls"] != "RECOVERED"]
print(f"\n--- THE 41%: {n_alerts} alerts, {n_rec} recovered "
      f"({100*n_rec/n_alerts:.2f}%), {len(unrec)} classified ---")
for k in sorted(cls_counts, key=lambda z: -cls_counts[z]):
    print(f"  {k:26s} {cls_counts[k]:5d}  ({100*cls_counts[k]/n_alerts:5.2f}%)")

mag_r = np.array([r["magpsf"] for r in miss_rows
                  if r["cls"] == "RECOVERED" and r["magpsf"] is not None], float)
mag_u = np.array([r["magpsf"] for r in unrec if r["magpsf"] is not None], float)
d_mag = float(np.median(mag_u) - np.median(mag_r)) if mag_r.size and mag_u.size else float("nan")
P5 = d_mag >= 0.5
print(f"\n  P5 median magpsf  recovered={np.median(mag_r):.3f} (n={mag_r.size})  "
      f"unrecovered={np.median(mag_u):.3f} (n={mag_u.size})")
print(f"     delta = {d_mag:+.3f} mag  -> P5 {'HELD' if P5 else 'REFUTED'} (>=0.5, fainter)")

n_geom = sum(1 for r in unrec if r["cls"] in ("OUT_OF_BOUNDS", "MASKED", "NO_POSITION"))
f_geom = n_geom / len(unrec) if unrec else float("nan")
P6 = f_geom < 0.10
print(f"  P6 geometry/mask share of misses : {n_geom}/{len(unrec)} = {100*f_geom:.2f}%"
      f"  -> P6 {'HELD' if P6 else 'REFUTED'} (<10%)")

n_thr = sum(1 for r in unrec if r["cls"] == "BELOW_THRESHOLD")
f_thr = n_thr / len(unrec) if unrec else float("nan")
P7 = f_thr >= 0.60
print(f"  P7 below-threshold share of misses: {n_thr}/{len(unrec)} = {100*f_thr:.2f}%"
      f"  -> P7 {'HELD' if P7 else 'REFUTED'} (>=60%)")

withmag = [r for r in miss_rows if r["magpsf"] is not None]
P8 = False; rec_bright = float("nan"); terc = None
if len(withmag) >= 9:
    m = np.array([r["magpsf"] for r in withmag], float)
    cut = np.percentile(m, 100.0 / 3.0)                 # brightest = SMALLEST magpsf
    br = [r for r in withmag if r["magpsf"] <= cut]
    rec_bright = sum(1 for r in br if r["cls"] == "RECOVERED") / len(br)
    terc = dict(cut_mag=float(cut), n=len(br))
    P8 = rec_bright >= 0.80
print(f"  P8 recovery in brightest magpsf tercile : {100*rec_bright:.2f}%"
      f"  -> P8 {'HELD' if P8 else 'REFUTED'} (>=80%)")

res["control_miss"] = dict(n_alerts=n_alerts, n_recovered=n_rec,
                           recovery=n_rec / n_alerts if n_alerts else float("nan"),
                           classes=cls_counts,
                           median_magpsf_recovered=float(np.median(mag_r)) if mag_r.size else None,
                           median_magpsf_unrecovered=float(np.median(mag_u)) if mag_u.size else None,
                           delta_mag=d_mag, geom_share=f_geom, thr_share=f_thr,
                           recovery_bright_tercile=rec_bright, tercile=terc)
res["predictions"] = {"P1": bool(P1), "P2": bool(P2), "P3": bool(P3), "P4": bool(P4),
                      "P5": bool(P5), "P6": bool(P6), "P7": bool(P7), "P8": bool(P8)}

held = sum(res["predictions"].values())
print(f"\n=== {held}/8 pre-registered predictions HELD ===")
if not CTRL_OK:
    print("  ** CONTROLS FAILED: P1-P4 are recorded but UNINTERPRETABLE **")
json.dump(res, open("PASS6_RESULTS.json", "w"), indent=2)
json.dump(miss_rows, open("PASS6_MISSES.json", "w"), indent=2)
print("wrote PASS6_RESULTS.json + PASS6_MISSES.json")
