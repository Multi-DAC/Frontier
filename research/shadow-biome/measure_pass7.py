"""PASS 7 — de-doubling the far side, and the residual misses at minarea=2.

Governed by PASS7_PREDICTIONS.md, committed and pushed (da25f0c) BEFORE this
file existed. Every threshold below is COPIED from that file, not chosen here.

Four blocks:
  A  single-sign          A1-A4   (A1-A3 off the frozen catalogue; A4 re-extracts)
  B  pair-collapse        B1-B3   (B3 is an identity CONTROL, not a finding)
  C  residual misses      C1-C4   at minarea=2
  I  the instrument       I1-I2   scored by R2's gauge, not by my eye

R1/R2/R3 (PASS7_PREDICTIONS.md sec.5) are HARD REQUIREMENTS, not options:
  R1  a verdict key for EVERY letter registered in the prereg; asserted below
      against a literal list, because L1's T5 was pre-registered and scored
      NOWHERE and the fix has to be a trigger rather than a resolution.
  R2  every filter/gate/precondition records HOW MANY ITEMS IT REJECTED, and
      any that rejected zero is named in `unexercised`. Generalised from the L1
      defect: el_match was True 8/8 with n_dropped 0 -- a precondition that has
      never rejected anything is not observably a precondition.
  R3  `unexercised` non-empty WARNS and is written to JSON. Gauge, not gate.
"""
import json, os, glob
import numpy as np
import sep
from astropy.io import fits

# ---------------------------------------- constants COPIED, not re-chosen
THRESH, MATCH, WALL, BOX = 5.0, 2.0, 1.6, 2      # measure_pass6.py:27-29
PAIR_RADIUS = 10.0                                # diag_pass6.py:21
MINAREA_LADDER = [2, 3, 5, 8, 12]                 # diag_pass6.py
CAT_MINAREA = 5                                   # the frozen catalogue's rung

# PASS7_PREDICTIONS.md GIVEN-2
UNION_FRAC_FAR = 0.4849906191369606
# PASS7_PREDICTIONS.md sec.4 standing state
D2B_RECOVERY_MINAREA2 = 0.7313829787234043

# ============================================================== R2 GAUGE
REJ = {}


def gate(name, n_in, n_kept, note=""):
    """Record a filter's throughput. R2: the rejection count is the point."""
    d = REJ.setdefault(name, {"n_in": 0, "n_kept": 0, "n_rejected": 0, "note": note})
    d["n_in"] += int(n_in)
    d["n_kept"] += int(n_kept)
    d["n_rejected"] += int(n_in - n_kept)
    return d


res = {"prereg": "PASS7_PREDICTIONS.md", "prereg_commit": "da25f0c"}
V = {}                                            # the verdicts dict R1 asserts on

# ================================================== A1-A3  FROZEN CATALOGUE
cat = np.load("PASS6_catalog.npz", allow_pickle=True)
EL, SG, IM = cat["elong"], cat["sign"], cat["image"]
X, Y, TH = cat["x"], cat["y"], cat["theta"]
N = len(EL)
FAR = EL > WALL

plus = SG > 0
minus = SG < 0
gate("A_sign_plus_selection", N, int(plus.sum()),
     "7(a): keep sign=+1 only. measure_pass6.py:84-95 gives each sign its own "
     "background from its own array, so this subset IS a +data-only extraction.")
gate("A_wall_far_minarea5", N, int(FAR.sum()),
     "elong > 1.6, ZTF's own packaging cut, on the frozen catalogue")

ff_plus = float(FAR[plus].mean())
ff_minus = float(FAR[minus].mean())
ff_union = float(FAR.mean())
drop_pp = 100.0 * (ff_union - ff_plus)

print("=" * 78)
print("A  SINGLE-SIGN  (frozen PASS6_catalog.npz, minarea=%d)" % CAT_MINAREA)
print("=" * 78)
print(f"  n = {N}   sign=+1: {int(plus.sum())}   sign=-1: {int(minus.sum())}"
      f"   (GIVEN-1, seen before the prereg -- observation, NOT a held prediction)")
print(f"  frac_far  union   = {ff_union:.6f}   (GIVEN-2 published {UNION_FRAC_FAR:.6f})")
print(f"  frac_far  +only   = {ff_plus:.6f}")
print(f"  frac_far  -only   = {ff_minus:.6f}")
print(f"  union -> +only drop = {drop_pp:+.3f} pp")

V["A1"] = bool(ff_plus < UNION_FRAC_FAR)
V["A2"] = bool(ff_plus >= 0.35)
a3_gap_pp = 100.0 * (ff_minus - ff_plus)
V["A3"] = bool(a3_gap_pp >= 3.0)
print(f"  A1 +only below union 0.48499              -> {'HELD' if V['A1'] else 'REFUTED'}")
print(f"  A2 far side survives, +only >= 0.35       -> {'HELD' if V['A2'] else 'REFUTED'}")
print(f"  A3 DIRECTIONAL: -side more elongated by >=3.0 pp : {a3_gap_pp:+.3f} pp"
      f"  -> {'HELD' if V['A3'] else 'REFUTED'}")

res["A"] = dict(n=N, n_plus=int(plus.sum()), n_minus=int(minus.sum()),
                frac_far_union=ff_union, frac_far_plus=ff_plus,
                frac_far_minus=ff_minus, drop_pp=drop_pp, a3_gap_pp=a3_gap_pp)

# ==================================================== B  PAIR-COLLAPSE
# Mutual nearest neighbour within 10.0 px, opposite sign, collapse to the
# sign=+1 member. Mutuality is the STRICTER reading of D2a's anchor->neighbour
# and was chosen in the prereg BEFORE knowing what it does to the number.
print("\n" + "=" * 78)
print("B  PAIR-COLLAPSE  (mutual NN <= %.1f px, opposite sign, keep + geometry)" % PAIR_RADIUS)
print("=" * 78)

drop_idx = np.zeros(N, bool)          # the '-' members to remove
n_mutual_opp = 0
n_mutual_same = 0
n_no_neighbour = 0
n_not_mutual = 0

for fn in np.unique(IM):
    m = np.where(IM == fn)[0]
    x, y, s = X[m], Y[m], SG[m]
    k = len(m)
    if k < 2:
        n_no_neighbour += k
        continue
    d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
    np.fill_diagonal(d, np.inf)
    nn = d.argmin(axis=1)
    nd = d[np.arange(k), nn]
    within = nd <= PAIR_RADIUS
    n_no_neighbour += int((~within).sum())
    for i in range(k):
        j = nn[i]
        if not within[i]:
            continue
        if nn[j] != i:                              # not mutual
            n_not_mutual += 1
            continue
        if i > j:                                   # score each mutual pair once
            continue
        if s[i] * s[j] < 0:
            n_mutual_opp += 1
            drop_idx[m[i] if s[i] < 0 else m[j]] = True
        else:
            n_mutual_same += 1

gate("B_within_pair_radius", N, N - n_no_neighbour,
     f"has a nearest neighbour <= {PAIR_RADIUS} px")
gate("B_mutual_nn", n_mutual_opp * 2 + n_mutual_same * 2 + n_not_mutual,
     n_mutual_opp * 2 + n_mutual_same * 2, "mutual nearest-neighbour requirement")
gate("B_opposite_sign", n_mutual_opp + n_mutual_same, n_mutual_opp,
     "mutual pairs must be OPPOSITE sign to be a dipole")

keep = ~drop_idx
n_coll = int(keep.sum())
ff_coll = float(FAR[keep].mean())
b2_gap_pp = 100.0 * abs(ff_coll - ff_plus)

print(f"  detections with no neighbour <= {PAIR_RADIUS:.0f} px : {n_no_neighbour}")
print(f"  had a neighbour but not mutual              : {n_not_mutual}")
print(f"  mutual pairs, SAME sign     (kept whole)    : {n_mutual_same}")
print(f"  mutual pairs, OPPOSITE sign (collapsed)     : {n_mutual_opp}")
print(f"  n_collapsed = {n_coll}   frac_far = {ff_coll:.6f}")

V["B1"] = bool(ff_coll < UNION_FRAC_FAR)
V["B2"] = bool(b2_gap_pp <= 4.0)
V["B3"] = bool(n_coll == N - n_mutual_opp)
print(f"  B1 collapsed below union 0.48499          -> {'HELD' if V['B1'] else 'REFUTED'}")
print(f"  B2 |collapsed - +only| <= 4.0 pp : {b2_gap_pp:.3f} pp"
      f"  -> {'HELD' if V['B2'] else 'REFUTED'}")
print(f"  B3 CONTROL identity n_coll == n - n_pairs -> {'HOLDS' if V['B3'] else '**VOID**'}"
      f"   (may NOT be counted in any held-total, prereg sec.3)")
if not V["B2"]:
    print("  ** B2 REFUTED: A1/A2 and B1 are UNINTERPRETABLE (prereg sec.3) **")

res["B"] = dict(pair_radius=PAIR_RADIUS, n_no_neighbour=n_no_neighbour,
                n_not_mutual=n_not_mutual, n_mutual_same=n_mutual_same,
                n_mutual_opp=n_mutual_opp, n_collapsed=n_coll,
                frac_far_collapsed=ff_coll, b2_gap_pp=b2_gap_pp)

# ============================== A4 + C  RE-EXTRACTION OVER THE 20 IMAGES
print("\n" + "=" * 78)
print("A4 ladder + C  residual misses at minarea=2  (re-extraction, 20 images)")
print("=" * 78)

alerts = json.load(open("PASS5_alert_index.json"))
by_img = {}
for a in alerts:
    by_img.setdefault(a["f"], []).append(a)

ladder = {ma: {"n_p": 0, "far_p": 0, "n_m": 0, "far_m": 0} for ma in MINAREA_LADDER}
miss_rows = []
n_noposition = 0

files = sorted(glob.glob("diffimg/*.fz"))
for p in files:
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img)
    img[bad] = 0.0
    H, W = img.shape

    bkg0 = sep.Background(img, mask=bad)          # local S/N at alert positions
    sub0, rms0 = img - bkg0.back(), bkg0.globalrms

    prep = []
    for sign, arr in ((+1, img), (-1, -img)):     # background ONCE per sign
        bkg = sep.Background(arr, mask=bad)
        prep.append((sign, np.ascontiguousarray(arr - bkg.back()), bkg.globalrms))

    ma2_x, ma2_y = None, None
    for ma in MINAREA_LADDER:
        xs, ys = [], []
        for sign, sub, rms in prep:
            o = sep.extract(sub, THRESH, err=rms, minarea=ma, mask=bad)
            ok = o["b"] > 0
            gate(f"reextract_b_positive_minarea{ma}", len(o), int(ok.sum()),
                 "sep semi-minor axis b > 0")
            e = o["a"][ok] / o["b"][ok]
            key = "p" if sign > 0 else "m"
            ladder[ma][f"n_{key}"] += len(e)
            ladder[ma][f"far_{key}"] += int((e > WALL).sum())
            xs.append(o["x"][ok]); ys.append(o["y"][ok])
        if ma == 2:
            ma2_x, ma2_y = np.concatenate(xs), np.concatenate(ys)

    # ------------------- C: classify EVERY alert at minarea=2, pass-6 rules
    for al in by_img.get(fn, []):
        ax, ay = al.get("x"), al.get("y")
        row = dict(image=fn, magpsf=al.get("magpsf"), elong=al.get("elong"))
        if ax is None or ay is None:
            n_noposition += 1
            row.update(cls="NO_POSITION", recovered=False, nn=None, snr=None)
            miss_rows.append(row); continue
        d = np.hypot(ma2_x + 1 - ax, ma2_y + 1 - ay)      # FITS 1-indexed, as pass 5/6
        nn_d = float(d.min())
        rec = nn_d <= MATCH
        ci, ri = int(round(ax - 1)), int(round(ay - 1))
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
                elif nn_d <= 5.0:
                    cls = "NEAR_MISS_RADIUS"
                else:
                    cls = "UNEXTRACTED_DESPITE_FLUX"
        if rec and cls not in ("OUT_OF_BOUNDS", "MASKED"):
            cls = "RECOVERED"
        row.update(cls=cls, recovered=bool(rec), nn=nn_d, snr=snr_loc)
        miss_rows.append(row)

    print(f"    {fn[22:44]} done", flush=True)

gate("C_alert_has_position", len(miss_rows), len(miss_rows) - n_noposition,
     "alert carries x/y in PASS5_alert_index.json")

# ------------------------------------------------------------------- A4
print(f"\n  {'minarea':>8} {'ff_union':>9} {'ff_plus':>9} {'drop_pp':>9}")
drops = {}
for ma in MINAREA_LADDER:
    d = ladder[ma]
    n_tot = d["n_p"] + d["n_m"]
    ff_u = (d["far_p"] + d["far_m"]) / n_tot if n_tot else float("nan")
    ff_p = d["far_p"] / d["n_p"] if d["n_p"] else float("nan")
    d.update(frac_far_union=ff_u, frac_far_plus=ff_p, drop_pp=100.0 * (ff_u - ff_p))
    drops[ma] = d["drop_pp"]
    print(f"  {ma:>8} {ff_u:>9.4f} {ff_p:>9.4f} {d['drop_pp']:>+9.3f}")

a4_span = max(drops.values()) - min(drops.values())
V["A4"] = bool(a4_span <= 5.0)
print(f"  A4 span of the drop across the ladder : {a4_span:.3f} pp"
      f"  -> {'HELD' if V['A4'] else 'REFUTED'} (<=5.0)")
res["A4"] = dict(ladder={str(k): ladder[k] for k in MINAREA_LADDER},
                 drops_pp={str(k): drops[k] for k in MINAREA_LADDER},
                 span_pp=a4_span)

# ------------------------------------------------------------------- C
cls_counts = {}
for r in miss_rows:
    cls_counts[r["cls"]] = cls_counts.get(r["cls"], 0) + 1
n_alerts = len(miss_rows)
n_rec = cls_counts.get("RECOVERED", 0)
unrec = [r for r in miss_rows if r["cls"] != "RECOVERED"]
recovery = n_rec / n_alerts if n_alerts else float("nan")

print(f"\n  minarea=2: {n_alerts} alerts, {n_rec} recovered ({100*recovery:.2f}%), "
      f"{len(unrec)} residual")
for k in sorted(cls_counts, key=lambda z: -cls_counts[z]):
    print(f"    {k:26s} {cls_counts[k]:5d}")

V["C1"] = bool(abs(recovery - D2B_RECOVERY_MINAREA2) <= 0.020)
unrec_counts = {k: v for k, v in cls_counts.items() if k != "RECOVERED"}
biggest = max(unrec_counts, key=lambda z: unrec_counts[z]) if unrec_counts else None
V["C2"] = bool(biggest == "UNEXTRACTED_DESPITE_FLUX")

mag_r = np.array([r["magpsf"] for r in miss_rows
                  if r["cls"] == "RECOVERED" and r["magpsf"] is not None], float)
mag_u = np.array([r["magpsf"] for r in unrec if r["magpsf"] is not None], float)
d_mag = float(np.median(mag_u) - np.median(mag_r)) if mag_r.size and mag_u.size else float("nan")
V["C3"] = bool(d_mag >= 1.0)

frames_with_miss = len({r["image"] for r in unrec})
V["C4"] = bool(frames_with_miss >= 12)

print(f"  C1 recovery within 2.0 pp of {D2B_RECOVERY_MINAREA2:.4f}: "
      f"{100*(recovery - D2B_RECOVERY_MINAREA2):+.3f} pp"
      f"  -> {'HELD' if V['C1'] else 'REFUTED'}")
print(f"  C2 largest residual class = UNEXTRACTED_DESPITE_FLUX (is {biggest})"
      f"  -> {'HELD' if V['C2'] else 'REFUTED'}")
print(f"  C3 DIRECTIONAL: d_mag = {d_mag:+.3f} mag (need >=1.0)"
      f"  -> {'HELD' if V['C3'] else 'REFUTED'}")
print(f"  C4 residual spread across {frames_with_miss}/{len(files)} frames (need >=12)"
      f"  -> {'HELD' if V['C4'] else 'REFUTED'}")

res["C"] = dict(minarea=2, n_alerts=n_alerts, n_recovered=n_rec, recovery=recovery,
                classes=cls_counts, largest_residual_class=biggest,
                median_magpsf_recovered=float(np.median(mag_r)) if mag_r.size else None,
                median_magpsf_unrecovered=float(np.median(mag_u)) if mag_u.size else None,
                delta_mag=d_mag, frames_with_residual=frames_with_miss,
                n_frames=len(files))

# ======================================================= R2/R3 + I1-I2
print("\n" + "=" * 78)
print("R2  UNEXERCISED-PRECONDITION GAUGE")
print("=" * 78)
unexercised = sorted(k for k, d in REJ.items() if d["n_rejected"] == 0)
for k in sorted(REJ):
    d = REJ[k]
    flag = "  <== REJECTED NOTHING" if d["n_rejected"] == 0 else ""
    print(f"  {k:34s} in={d['n_in']:>7} kept={d['n_kept']:>7} "
          f"rejected={d['n_rejected']:>7}{flag}")
if unexercised:
    print(f"\n  ** R3 WARNING: {len(unexercised)} precondition(s) rejected NOTHING. "
          f"A precondition that has never rejected anything is not observably a "
          f"precondition. **")
    for k in unexercised:
        print(f"     - {k}")
else:
    print("\n  every recorded precondition rejected at least one item")

# I1/I2 are scored by hand-entered evidence, but the SCORING PATH exists in the
# artifact -- which is the whole point of R1. The gauge's own output decides I2.
gauge_found = bool(unexercised) or (not V["B3"]) or (not V["C1"])
res["I"] = dict(unexercised=unexercised, rejection_table=REJ,
                gauge_surfaced_something=gauge_found,
                provisional=True,
                note="PROVISIONAL ON THIS RUN. I1/I2 are set from the gauge's own output "
                     "only. If the gauge found nothing and I later find a defect BY EYE, "
                     "that flips I1 to HELD and I2 to REFUTED, and it must be entered as "
                     "a dated amendment rather than by editing these keys -- the by-eye "
                     "find is exactly what I2 predicts against, so it may not be "
                     "laundered into agreement.")
V["I1"] = bool(gauge_found)
V["I2"] = bool(gauge_found)
print(f"\n  I1 an instrument defect surfaced         -> {'HELD' if V['I1'] else 'REFUTED'}")
print(f"  I2 R2's gauge surfaced it, not my eye   -> {'HELD' if V['I2'] else 'REFUTED'}")
if not V["I1"]:
    print("  ** I1 REFUTED is the SUSPICIOUS outcome, pre-labelled: a pass reporting no")
    print("     instrument trouble is more likely to have MISSED it than avoided it.")
    print("     No sentence may cite a clean pass 7 as evidence of instrument soundness. **")

# ============================================================ R1 ASSERTION
REGISTERED = ["A1", "A2", "A3", "A4", "B1", "B2", "B3",
              "C1", "C2", "C3", "C4", "I1", "I2"]     # literal, from the prereg
missing = [k for k in REGISTERED if k not in V]
extra = [k for k in V if k not in REGISTERED]
res["verdicts"] = {k: bool(V[k]) for k in REGISTERED if k in V}
res["R1"] = dict(registered=REGISTERED, missing=missing, extra=extra,
                 ok=(not missing and not extra))
json.dump(res, open("PASS7_RESULTS.json", "w"), indent=2)
json.dump(miss_rows, open("PASS7_MISSES.json", "w"), indent=2)

# B3 is an identity CONTROL and is excluded from the held-total (prereg sec.3).
scored = [k for k in REGISTERED if k != "B3"]
held = sum(1 for k in scored if V.get(k))
print("\n" + "=" * 78)
print(f"=== {held}/{len(scored)} pre-registered predictions HELD "
      f"(B3 excluded: identity control, prereg sec.3) ===")
print(f"    B3 identity: {'HOLDS' if V['B3'] else '**VOID -- the pass is void**'}")
print("wrote PASS7_RESULTS.json + PASS7_MISSES.json")
assert not missing and not extra, f"R1 VIOLATED: missing={missing} extra={extra}"
print("R1 satisfied: a verdict key exists for every registered prediction letter")
