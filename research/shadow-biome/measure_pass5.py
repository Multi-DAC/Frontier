"""PASS 5 measurement — re-extraction from ZTF difference images with NO shape cut.

Governed by PREREGISTRATION.md and PASS5_PREDICTIONS.md, both committed and
pushed (10e9e1e) BEFORE this file was run and before any pixel was downloaded.

Every threshold below is copied from PASS5_PREDICTIONS.md §1, not chosen here.
Prints n beside every fraction (PREREGISTRATION.md §5).

Two implementation details decided here, NOT in the predictions file, disclosed
in the results document rather than buried:
  (a) sep finds POSITIVE sources; ZTF alerts include negative subtractions
      (isdiffpos='f'). So extraction is run on +data and on -data and the two
      catalogues are unioned with a sign tag. This is faithful to what the
      alert stream contains; it is not a change to any prediction.
  (b) FITS pixel coordinates are 1-indexed, sep's are 0-indexed. The primary
      match uses sep_x + 1. Both conventions are reported so the choice is
      visible rather than assumed.
"""
import json, os, sys, time, urllib.request
import numpy as np
import truststore
truststore.inject_into_ssl()

import sep
from astropy.io import fits

N_IMAGES   = 24          # PASS5_PREDICTIONS.md §1.1
THRESH_SIG = 5.0         # §1.3
MINAREA    = 5           # §1.3
MATCH_PX   = 2.0         # §1.4
IRSA = "https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/{yr}/{mmdd}/{frac}/{fn}.fz"
OUT  = "diffimg"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- selection
alerts = json.load(open("PASS5_alert_index.json"))
images = sorted({a["f"] for a in alerts if a["f"]})
M = len(images)
step = M // N_IMAGES
chosen = [images[i * step] for i in range(N_IMAGES)]
print(f"M = {M} distinct difference images; step = {step}; chosen = {len(chosen)}")
assert len(set(chosen)) == N_IMAGES

by_img = {}
for a in alerts:
    by_img.setdefault(a["f"], []).append(a)

def irsa_url(fn):
    # ztf_20180601167662_000526_zr_c12_o_q2_scimrefdiffimg.fits
    stamp = fn.split("_")[1]                 # 20180601167662
    return IRSA.format(yr=stamp[:4], mmdd=stamp[4:8], frac=stamp[8:], fn=fn)

# ---------------------------------------------------------------- download
t0 = time.time()
total_bytes = 0
paths = {}
for i, fn in enumerate(chosen, 1):
    p = os.path.join(OUT, fn + ".fz")
    if not os.path.exists(p):
        try:
            with urllib.request.urlopen(irsa_url(fn), timeout=180) as r, open(p, "wb") as f:
                f.write(r.read())
        except Exception as e:
            print(f"  [{i:2d}/{N_IMAGES}] DOWNLOAD FAILED {fn}: {type(e).__name__}", flush=True)
            continue
    total_bytes += os.path.getsize(p)
    paths[fn] = p
    print(f"  [{i:2d}/{N_IMAGES}] {os.path.getsize(p)/1e6:6.2f} MB  {fn}", flush=True)
t_dl = time.time() - t0
print(f"download: {len(paths)}/{N_IMAGES} images, {total_bytes/1e6:.1f} MB, {t_dl:.1f} s")

# ---------------------------------------------------------------- extraction
t1 = time.time()
det_elong, det_peak, det_sign, det_img = [], [], [], []
ctl_recovered, ctl_total, ctl_delong, ctl_dpix0, ctl_dpix1 = 0, 0, [], [], []
per_image = []

for fn, p in paths.items():
    with fits.open(p) as hdul:
        hdu = next(h for h in hdul if getattr(h, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img)
    img[bad] = 0.0

    cats = []
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        sub = arr - bkg.back()
        try:
            obj = sep.extract(sub, THRESH_SIG, err=bkg.globalrms,
                              minarea=MINAREA, mask=bad)
        except Exception as e:
            print(f"    extract failed ({sign:+d}) on {fn}: {type(e).__name__}")
            continue
        cats.append((sign, obj))

    xs, ys, els, pks, sgs = [], [], [], [], []
    for sign, obj in cats:
        a, b = obj["a"], obj["b"]
        ok = b > 0
        xs.append(obj["x"][ok]); ys.append(obj["y"][ok])
        els.append(a[ok] / b[ok]); pks.append(obj["peak"][ok])
        sgs.append(np.full(ok.sum(), sign))
    if not xs:
        continue
    X = np.concatenate(xs); Y = np.concatenate(ys)
    E = np.concatenate(els); P = np.concatenate(pks); S = np.concatenate(sgs)

    det_elong.append(E); det_peak.append(P); det_sign.append(S)
    det_img.append(np.full(len(E), fn))

    # ---- positive control: recover ZTF's own alerts on this image ----
    al = by_img.get(fn, [])
    ax = np.array([a["x"] for a in al], float)
    ay = np.array([a["y"] for a in al], float)
    ae = np.array([a["elong"] for a in al], float)
    n_rec = 0
    for j in range(len(al)):
        d0 = np.hypot(X - ax[j], Y - ay[j])            # 0-indexed convention
        d1 = np.hypot(X + 1 - ax[j], Y + 1 - ay[j])    # FITS 1-indexed (primary)
        ctl_dpix0.append(d0.min()); ctl_dpix1.append(d1.min())
        k = int(np.argmin(d1))
        if d1[k] <= MATCH_PX:
            n_rec += 1
            ctl_delong.append(abs(E[k] - ae[j]))
    ctl_recovered += n_rec; ctl_total += len(al)
    per_image.append(dict(image=fn, n_det=int(len(E)), n_alerts=len(al), n_recovered=n_rec))
    print(f"    {fn[:44]}  det={len(E):6d}  alerts={len(al):4d}  rec={n_rec:4d}", flush=True)

t_ex = time.time() - t1
E = np.concatenate(det_elong); P = np.concatenate(det_peak); S = np.concatenate(det_sign)
N = len(E)
print(f"\nextraction: {t_ex:.1f} s   total detections n = {N}")

# ---------------------------------------------------------------- scoring
res = {"n_images_requested": N_IMAGES, "n_images_ok": len(paths),
       "download_bytes": total_bytes, "download_s": t_dl, "extract_s": t_ex,
       "n_detections": int(N), "per_image": per_image}

print("\n--- CONTROL (decides whether anything below is interpretable) ---")
rec = ctl_recovered / ctl_total if ctl_total else float("nan")
med_de = float(np.median(ctl_delong)) if ctl_delong else float("nan")
print(f"  alerts on these images      : n = {ctl_total}")
print(f"  recovered within {MATCH_PX} px      : {ctl_recovered}  -> {100*rec:.2f}%")
print(f"  median nearest-neighbour distance, 0-indexed : {np.median(ctl_dpix0):.3f} px")
print(f"  median nearest-neighbour distance, 1-indexed : {np.median(ctl_dpix1):.3f} px")
print(f"  median |delta elong| on matched : {med_de:.4f}  (n = {len(ctl_delong)})")
INTERP = (rec >= 0.50) and (med_de <= 0.25)
print(f"  PRE-COMMITTED KILL CONDITION -> {'PASS, results interpretable' if INTERP else 'FAIL, elong>1.6 numbers are UNINTERPRETABLE'}")
res["control"] = dict(n_alerts=ctl_total, n_recovered=ctl_recovered, recovery=rec,
                      median_delong=med_de, n_matched=len(ctl_delong),
                      median_nn_px_0indexed=float(np.median(ctl_dpix0)),
                      median_nn_px_1indexed=float(np.median(ctl_dpix1)),
                      interpretable=bool(INTERP))

print("\n--- ELONGATION DISTRIBUTION, NO SHAPE CUT ---")
edges = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.5, 3.0, 5.0, 10.0, np.inf]
bins = {}
for i in range(len(edges) - 1):
    a, b = edges[i], edges[i + 1]
    c = int(((E >= a) & (E < b)).sum())
    bins[f"{a}-{b}"] = c
    print(f"  elong [{a:5.2f}, {b:5.2f}) : n = {c:8d}  ({100*c/N:6.3f}% of n={N})")
res["elong_bins"] = bins

f_past = float((E > 1.6).sum()) / N
print(f"\n  fraction with elong > 1.6 : {(E>1.6).sum()} / {N} = {100*f_past:.3f}%")
res["frac_past_wall"] = f_past

step_ratio = bins["1.6-1.7"] / bins["1.5-1.6"] if bins["1.5-1.6"] else float("nan")
Rp = bins["1.5-1.6"] / bins["1.2-1.3"] if bins["1.2-1.3"] else float("nan")
print(f"  n[1.6,1.7)/n[1.5,1.6) = {step_ratio:.4f}")
print(f"  R' = n[1.5,1.6)/n[1.2,1.3) = {Rp:.4f}   (pass 4 packaged stream: 0.2408)")
res["step_ratio_across_wall"] = step_ratio
res["R_prime"] = Rp

hi, lo = E > 1.6, E <= 1.6
mp_hi = float(np.median(P[hi])) if hi.any() else float("nan")
mp_lo = float(np.median(P[lo])) if lo.any() else float("nan")
print(f"  median peak, elong>1.6 : {mp_hi:.4f} (n={int(hi.sum())})")
print(f"  median peak, elong<=1.6: {mp_lo:.4f} (n={int(lo.sum())})")
res["median_peak_past"] = mp_hi; res["median_peak_kept"] = mp_lo
res["sign_split"] = {"positive": int((S > 0).sum()), "negative": int((S < 0).sum())}
print(f"  sign split: +{int((S>0).sum())} / -{int((S<0).sum())}")

print("\n--- PRE-REGISTERED PREDICTIONS, SCORED ---")
scored = {
    "P1_recovery_ge_80pct":      (rec >= 0.80,                     f"{100*rec:.2f}%"),
    "P2_median_delong_lt_0.10":  (med_de < 0.10,                   f"{med_de:.4f}"),
    "P3_frac_past_15_to_45pct":  (0.15 <= f_past <= 0.45,          f"{100*f_past:.3f}%"),
    "P4_step_ratio_gt_0.5":      (step_ratio > 0.5,                f"{step_ratio:.4f}"),
    "P5_Rprime_gt_0.241":        (Rp > 0.2408,                     f"{Rp:.4f}"),
    "P6_past_is_brighter":       (mp_hi > mp_lo,                   f"{mp_hi:.4f} vs {mp_lo:.4f}"),
    "P7_cost":                   (total_bytes < 200e6 and t_ex < 300, f"{total_bytes/1e6:.1f} MB / {t_ex:.1f} s"),
}
for k, (held, val) in scored.items():
    print(f"  {k:28s} {'HELD   ' if held else 'REFUTED'}  ({val})")
res["predictions"] = {k: {"held": bool(v[0]), "value": v[1]} for k, v in scored.items()}
if not INTERP:
    print("\n  ** CONTROL FAILED: P3-P6 are recorded but UNINTERPRETABLE per PASS5_PREDICTIONS.md **")

json.dump(res, open("PASS5_RESULTS.json", "w"), indent=2)
print("\nwrote PASS5_RESULTS.json")
