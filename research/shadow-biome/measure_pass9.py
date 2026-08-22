"""PASS 9 -- BLOCK P (P_D pre-registered, with its minarea ladder and the
V2 opposition re-run on survivors), BLOCK S (the scramble control pair_mask
has never had), BLOCK C (a citable() with a positive control), BLOCK F
(found_by at find time; G1 retires).

Governed by PASS9_PREDICTIONS.md, committed and pushed (32877a0) BEFORE this
file existed. Every threshold below is COPIED from that file, not chosen here.

  P0     REPRODUCTION CONTROL: independent P_D == 3870 / 0.422997     [excluded]
  P1     frac_far(P_D) < frac_far(union) at >= 4 of 5 minarea rungs
  P2     |move| >= 3.0 pp at >= 3 of 5 rungs
  P3     frac_far(pairs only) > frac_far(union) at >= 4 of 5 rungs
  P4     pair_share(minarea=2) > pair_share(minarea=12)
  P5     survivors: far-minus-kept opp_share_of_side <= +5.0 pp
  P6     survivors: far-side (opp_rate - null) < +20.0 pp
  S-NULL scramble preserves n, sign multiset, frac_far(union)          [gate]
  S1     median scrambled mutual-opp-pair count <= 50% of observed 2329
  S2     median |frac_far(P_D_scr) - frac_far(union)| <= 2.0 pp
  C1     strengthened citable() rejects 6 of 6 known-bad citations     [gate]
  C2     DEF-10 fails anchoring; DEF-04 and DEF-02 survive -- all three correct
  C3     >= 2 of the 12 legacy rows fail anchoring
  F1     pass 9 produces < 6 find-time register rows -> G1 RETIRED
  R4-CONTROL  R4 fires on a deliberate duplicate injected into pass 9's own set

R1: a verdict key for every registered letter, asserted against a literal list.
R2: every gate records its rejections; zero-rejection gates are named.
"""
import json, os, glob, sys
import numpy as np
import sep
from astropy.io import fits

from pass6_stats import nearest_neighbour_table

# ------------------------------------------ constants COPIED, not re-chosen
THRESH, MATCH, WALL = 5.0, 2.0, 1.6      # measure_pass6.py:27-29
PAIR_RADIUS = 10.0                        # diag_pass6.py:21
MINAREA_LADDER = [2, 3, 5, 8, 12]
CAT_MINAREA = 5
# PASS9_PREDICTIONS.md thresholds, transcribed
P0_N, P0_FF = 3870, 0.422997
P1_MIN_RUNGS = 4
P2_MIN_PP, P2_MIN_RUNGS = 3.0, 3
P3_MIN_RUNGS = 4
P5_MAX_PP = 5.0
P6_MAX_PP = 20.0
S_OFFSETS = [(40, 0), (-40, 0), (0, 40), (0, -40),
             (40, 40), (40, -40), (-40, 40), (-40, -40)]   # sec.2, fixed, no RNG
S1_MAX_FRAC = 0.50
S1_OBSERVED_PAIRS = 2329                  # PASS8_RESULTS.md sec.2, declared peek
S2_MAX_PP = 2.0
C1_REQUIRED = 6
C3_MIN_FAIL = 2
F1_MAX_FINDTIME = 6

REJ = {}
V = {}
TRIPLES = {}
FINDTIME = []          # BLOCK F: rows recorded AS THEY ARE FOUND, in this run


def gate(name, n_in, n_kept, note=""):
    d = REJ.setdefault(name, {"n_in": 0, "n_kept": 0, "n_rejected": 0, "note": note})
    d["n_in"] += int(n_in)
    d["n_kept"] += int(n_kept)
    d["n_rejected"] += int(n_in - n_kept)
    return d


def verdict(key, value, quantity, threshold, comparator):
    V[key] = None if value is None else bool(value)
    TRIPLES[key] = (str(quantity), None if threshold is None else float(threshold),
                    str(comparator))
    return V[key]


def r4_check(triples):
    seen, coll = {}, []
    for k, t in triples.items():
        if t in seen:
            coll.append((seen[t], k, t))
        else:
            seen[t] = k
    return coll


def find_time(what, cite, anchor, why, found_by="gauge"):
    """BLOCK F: called AT THE MOMENT a defect is noticed, inside the block that
    noticed it. Provenance is 'find-time' because the call site IS the finding."""
    row = dict(id="DEF-%02d" % (13 + len(FINDTIME)), pass_="9",
               found_by=found_by, found_at="pass9",
               found_by_provenance="find-time",
               what=what, cite=cite, anchor=anchor, why=why)
    FINDTIME.append(row)
    print(f"    >> FIND-TIME DEFECT {row['id']}: {what}")
    return row


def pair_mask(X, Y, SG, IM):
    """Mutual nearest neighbour <= PAIR_RADIUS px, opposite sign.
    Transcribed from measure_pass8.py:pair_mask so P0 is not tested against a
    different implementation of the thing under test."""
    n = len(X)
    paired = np.zeros(n, bool)
    drop = np.zeros(n, bool)
    for fn in np.unique(IM):
        m = np.where(IM == fn)[0]
        x, y, s = X[m], Y[m], SG[m]
        k = len(m)
        if k < 2:
            continue
        d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
        np.fill_diagonal(d, np.inf)
        nn = d.argmin(axis=1)
        nd = d[np.arange(k), nn]
        for i in range(k):
            j = nn[i]
            if nd[i] <= PAIR_RADIUS and nn[j] == i and s[i] * s[j] < 0:
                paired[m[i]] = True
                if s[i] < 0:
                    drop[m[i]] = True
    return paired, drop


res = {"prereg": "PASS9_PREDICTIONS.md", "prereg_commit": "32877a0"}

# ====================================================== load frozen catalogue
cat = np.load("PASS6_catalog.npz", allow_pickle=True)
EL, SG, IM = cat["elong"], cat["sign"], cat["image"]
X, Y, TH = cat["x"], cat["y"], cat["theta"]
N = len(EL)
FAR = EL > WALL
ff_union = float(FAR.mean())
paired, drop = pair_mask(X, Y, SG, IM)

# ============================================================== P0  CONTROL
print("=" * 78)
print("P0  REPRODUCTION CONTROL -- P_D built independently as ~paired")
print("=" * 78)
P_D = ~paired                       # NOT ~drop, NOT a negation of pass 8's array
n_pd = int(P_D.sum())
ff_pd = float(FAR[P_D].mean())
n_pairs = int(paired.sum()) // 2
gate("P0_pair_removal", N, n_pd, "P_D drops BOTH members of every mutual opposite pair")
print(f"  union   n = {N:>6}   frac_far = {ff_union:.6f}")
print(f"  P_D     n = {n_pd:>6}   frac_far = {ff_pd:.6f}   "
      f"move = {100*(ff_pd-ff_union):+.3f} pp")
print(f"  mutual opposite pairs = {n_pairs}   members = {int(paired.sum())}")
p0_ok = (n_pd == P0_N) and (round(ff_pd, 6) == P0_FF)
verdict("P0", p0_ok, "(n_PD, round(frac_far,6)) vs pass-8 post-hoc", None, "==")
print(f"  P0 -> {'HOLDS' if p0_ok else '**VOID -- PASS8_RESULTS.md sec.2 table is wrong**'}"
      f"   (excluded from the held-total, prereg sec.5)")
if not p0_ok:
    find_time(f"P_D irreproducible: got n={n_pd} ff={ff_pd:.6f}, "
              f"pass 8 published {P0_N}/{P0_FF}",
              "json:PASS9_RESULTS.json:/P0", "P0", "reproduction control failed")
res["P0"] = dict(n_union=N, frac_far_union=ff_union, n_PD=n_pd, frac_far_PD=ff_pd,
                 move_pp=100*(ff_pd-ff_union), n_pairs=n_pairs,
                 expected_n=P0_N, expected_ff=P0_FF, reproduced=p0_ok)

# ================================== P5/P6  V2 OPPOSITION RE-RUN ON SURVIVORS
print("\n" + "=" * 78)
print("P5/P6  THE V2 OPPOSITION ANALYSIS, RE-RUN ON THE P_D SURVIVORS")
print("=" * 78)


def v2(sel_x, sel_y, sel_th, sel_sg, sel_el, sel_im, label_prefix=""):
    """Transcribed from verify_pass6.py:70-105. Pairing is NON-mutual nearest
    neighbour, which is why running it on P_D survivors is not tautological."""
    out = {}
    for label, want_far in (("far", True), ("kept", False)):
        k = n = 0
        exp = 0.0
        deltas = []
        anchors_total = 0
        for fn in sorted(set(sel_im.tolist())):
            m = sel_im == fn
            x, y, th, sg, el = sel_x[m], sel_y[m], sel_th[m], sel_sg[m], sel_el[m]
            side = (el > WALL) if want_far else (el <= WALL)
            anchors_total += int(side.sum())
            idx, dist, delta, opp = nearest_neighbour_table(x, y, th, sg, PAIR_RADIUS)
            if idx.size == 0:
                continue
            s = side[idx]
            if s.sum() == 0:
                continue
            o, dl = opp[s], delta[s]
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
        print(f"  {label_prefix}{label:5s}: anchors={d['anchors']:5d} paired={d['paired']:5d}"
              f"  opp_rate={100*d['opp_rate']:6.2f}%  null={100*d['null']:6.2f}%"
              f"  excess={100*(d['opp_rate']-d['null']):+7.2f} pp"
              f"  share_of_side={100*d['opp_share_of_side']:6.2f}%")
    return out


print("  -- union (reproduce PASS6_VERIFY.json /V2, a declared peek, not scored) --")
v2_union = v2(X, Y, TH, SG, EL, IM, "union ")
print("  -- P_D survivors (NEW -- this is what P5/P6 are scored on) --")
v2_pd = v2(X[P_D], Y[P_D], TH[P_D], SG[P_D], EL[P_D], IM[P_D], "P_D   ")

fmk_union = 100.0 * (v2_union["far"]["opp_share_of_side"] - v2_union["kept"]["opp_share_of_side"])
fmk_pd = 100.0 * (v2_pd["far"]["opp_share_of_side"] - v2_pd["kept"]["opp_share_of_side"])
exc_union = 100.0 * (v2_union["far"]["opp_rate"] - v2_union["far"]["null"])
exc_pd = 100.0 * (v2_pd["far"]["opp_rate"] - v2_pd["far"]["null"])

print(f"\n  far-minus-kept share : union {fmk_union:+.2f} pp  ->  P_D {fmk_pd:+.2f} pp"
      f"   (P5 threshold <= +{P5_MAX_PP:.1f})")
print(f"  far-side opp excess  : union {exc_union:+.2f} pp  ->  P_D {exc_pd:+.2f} pp"
      f"   (P6 threshold <  +{P6_MAX_PP:.1f})")
verdict("P5", fmk_pd <= P5_MAX_PP, "far_minus_kept_share_pp_PD", P5_MAX_PP, "<=")
verdict("P6", exc_pd < P6_MAX_PP, "far_opp_excess_pp_PD", P6_MAX_PP, "<")
print(f"  P5 -> {'HELD' if V['P5'] else 'REFUTED'}    P6 -> {'HELD' if V['P6'] else 'REFUTED'}")
if not (V["P5"] and V["P6"]):
    print("  ** PRE-COMMITTED (prereg sec.1c): pair_mask() is UNDER-INCLUSIVE.")
    print("     Every P_A/P_B/P_D number in passes 7-9 is a LOWER BOUND on the")
    print("     artefact, not a measurement of it, and section 11 must say so. **")
    find_time("far-side dipole structure survives removal of every mutual "
              "opposite pair -- pair_mask() finds a subset of the dipole "
              "population, not the population",
              "json:PASS9_RESULTS.json:/P5P6", "P5P6",
              "P5/P6 refuted; scoped by prereg sec.1c before the run")
res["P5P6"] = dict(union=v2_union, P_D=v2_pd, far_minus_kept_union_pp=fmk_union,
                   far_minus_kept_PD_pp=fmk_pd, far_excess_union_pp=exc_union,
                   far_excess_PD_pp=exc_pd)

# ==================================================== BLOCK S  THE SCRAMBLE
print("\n" + "=" * 78)
print("S   SCRAMBLE CONTROL -- shown the case where pair_mask SHOULD find nothing")
print("=" * 78)


def scramble(x, y, sg, im, dx, dy):
    """Translate every sign<0 detection by (dx,dy), wrapping into the observed
    [min,max] range of that frame's detections. Positives untouched."""
    xs, ys = x.copy(), y.copy()
    for fn in np.unique(im):
        m = np.where(im == fn)[0]
        x0, x1 = x[m].min(), x[m].max()
        y0, y1 = y[m].min(), y[m].max()
        wx, wy = x1 - x0, y1 - y0
        neg = m[sg[m] < 0]
        if not len(neg) or wx <= 0 or wy <= 0:
            continue
        xs[neg] = x0 + np.mod(x[neg] - x0 + dx, wx)
        ys[neg] = y0 + np.mod(y[neg] - y0 + dy, wy)
    return xs, ys


find_time("the first draft of the S-NULL gate compared SG to itself "
          "(np.array_equal(np.sort(SG), np.sort(SG))) and compared frac_far(union) "
          "to a quantity the scramble never touches -- it could not have failed",
          "file:measure_pass9.py|S_null_offset", "S_null_offset",
          "caught by reading the block before running it; the repair is the "
          "positives-untouched / negatives-moved / in-range triple now in place",
          found_by="eye")

s_rows, s_null_ok = [], True
for dx, dy in S_OFFSETS:
    xs, ys = scramble(X, Y, SG, IM, dx, dy)
    pr_s, _ = pair_mask(xs, ys, SG, IM)
    npairs_s = int(pr_s.sum()) // 2
    surv = ~pr_s
    ff_s = float(FAR[surv].mean())
    # S-NULL: n preserved, POSITIVES untouched, NEGATIVES actually moved, and
    # every scrambled coordinate still inside its frame's observed range.
    # (An earlier draft of this gate compared SG to itself and to a quantity the
    # scramble never touches -- it could not fail. DEF-13 below, at find time.)
    posm, negm = SG > 0, SG < 0
    moved = np.hypot(xs[negm] - X[negm], ys[negm] - Y[negm]) > 1e-9
    inrange = True
    for fn in np.unique(IM):
        m = np.where(IM == fn)[0]
        inrange = inrange and bool(
            (xs[m] >= X[m].min() - 1e-6).all() and (xs[m] <= X[m].max() + 1e-6).all()
            and (ys[m] >= Y[m].min() - 1e-6).all() and (ys[m] <= Y[m].max() + 1e-6).all())
    ok = (len(xs) == N and len(ys) == N
          and np.array_equal(xs[posm], X[posm]) and np.array_equal(ys[posm], Y[posm])
          and float(moved.mean()) >= 0.99 and inrange)
    gate("S_null_offset", 4, int(not ok) * 4,
         "S-NULL sub-checks per offset (kept = FAILED checks)")
    s_null_ok = s_null_ok and ok
    gate("S_scramble_pairs", N, int(surv.sum()),
         "scrambled P_D drops both members of every mutual opposite pair")
    s_rows.append(dict(dx=dx, dy=dy, n_pairs=npairs_s, n_survivors=int(surv.sum()),
                       frac_far=ff_s, move_pp=100*(ff_s-ff_union)))
    print(f"  offset ({dx:>+4},{dy:>+4})  pairs={npairs_s:>5}  survivors={int(surv.sum()):>5}"
          f"  frac_far={ff_s:.6f}  move={100*(ff_s-ff_union):+7.3f} pp")

med_pairs = float(np.median([r["n_pairs"] for r in s_rows]))
med_absmove = float(np.median([abs(r["move_pp"]) for r in s_rows]))
frac_of_obs = med_pairs / S1_OBSERVED_PAIRS
print(f"\n  median scrambled pairs = {med_pairs:.1f}  = {100*frac_of_obs:.1f}% of the"
      f" observed {S1_OBSERVED_PAIRS}   (S1 threshold <= {100*S1_MAX_FRAC:.0f}%)")
print(f"  median |move| = {med_absmove:.3f} pp  against the observed 6.199 pp"
      f"   (S2 threshold <= {S2_MAX_PP:.1f})")
verdict("S-NULL", s_null_ok, "scramble preserves n/signs/frac_far_union", None, "==")
verdict("S1", frac_of_obs <= S1_MAX_FRAC, "median_scrambled_pairs / observed",
        S1_MAX_FRAC, "<=")
verdict("S2", med_absmove <= S2_MAX_PP, "median_abs_move_pp_scrambled", S2_MAX_PP, "<=")
print(f"  S-NULL -> {'PASS' if V['S-NULL'] else '**VOID**'}"
      f"    S1 -> {'HELD' if V['S1'] else 'REFUTED'}"
      f"    S2 -> {'HELD' if V['S2'] else 'REFUTED'}")
if not V["S2"]:
    print("  ** PRE-COMMITTED (prereg sec.2): chance pairs move frac_far too, so the")
    print("     mutual-NN construction SELECTS ELONGATED DETECTIONS BY GEOMETRY.")
    print("     Section 11 reports the union; P_D is reported as UNEXPLAINED. **")
    find_time("mutual-NN pairing moves frac_far even on scrambled positions -- "
              "the pair FINDER selects elongated detections by geometry",
              "json:PASS9_RESULTS.json:/S", "S2",
              "S2 refuted; scoped by prereg sec.2 before the run")
res["S"] = dict(offsets=s_rows, median_pairs=med_pairs, observed_pairs=S1_OBSERVED_PAIRS,
                frac_of_observed=frac_of_obs, median_abs_move_pp=med_absmove,
                null_ok=s_null_ok)

# ========================================= P1-P4  THE minarea LADDER
print("\n" + "=" * 78)
print("P1-P4  P_D OVER THE minarea LADDER  (re-extraction, 20 images)")
print("=" * 78)
files = sorted(glob.glob("diffimg/*.fz"))
rungs = {ma: dict(x=[], y=[], sg=[], im=[], el=[]) for ma in MINAREA_LADDER}
for p in files:
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(z for z in h if getattr(z, "data", None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img)
    img[bad] = 0.0
    prep = []
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        prep.append((sign, np.ascontiguousarray(arr - bkg.back()), bkg.globalrms))
    for ma in MINAREA_LADDER:
        for sign, sub, rms in prep:
            o = sep.extract(sub, THRESH, err=rms, minarea=ma, mask=bad)
            ok = o["b"] > 0
            gate(f"P_b_positive_minarea{ma}", len(o), int(ok.sum()),
                 "sep semi-minor axis b > 0")
            k = int(ok.sum())
            rungs[ma]["x"].append(o["x"][ok])
            rungs[ma]["y"].append(o["y"][ok])
            rungs[ma]["el"].append(o["a"][ok] / o["b"][ok])
            rungs[ma]["sg"].append(np.full(k, sign))
            rungs[ma]["im"].append(np.full(k, fn, dtype=object))
    print(f"    {fn[22:46]} done", flush=True)

print(f"\n  {'minarea':>8} {'n':>7} {'pairs':>6} {'p_share':>8} {'ff_union':>9}"
      f" {'ff_P_D':>9} {'move_pp':>8} {'ff_pairs':>9} {'pairs_pp':>9}")
ladder, n_p1, n_p2, n_p3, disagree = {}, 0, 0, 0, []
for ma in MINAREA_LADDER:
    d = rungs[ma]
    x = np.concatenate(d["x"]); y = np.concatenate(d["y"])
    sg = np.concatenate(d["sg"]); el = np.concatenate(d["el"])
    im = np.concatenate(d["im"]).astype("U57")
    far = el > WALL
    ffu = float(far.mean())
    pr, _ = pair_mask(x, y, sg, im)
    surv = ~pr
    ffd = float(far[surv].mean()) if surv.any() else float("nan")
    ffp = float(far[pr].mean()) if pr.any() else float("nan")
    move = 100.0 * (ffd - ffu)
    pmove = 100.0 * (ffp - ffu)
    p1 = ffd < ffu
    p2 = abs(move) >= P2_MIN_PP
    p3 = ffp > ffu
    n_p1 += int(p1); n_p2 += int(p2); n_p3 += int(p3)
    if p1 != p3:
        disagree.append(ma)
    ladder[str(ma)] = dict(n=int(len(x)), n_pairs=int(pr.sum()) // 2,
                           pair_share=float(pr.mean()), frac_far_union=ffu,
                           frac_far_PD=ffd, move_pp=move,
                           frac_far_pairs=ffp, pairs_move_pp=pmove,
                           p1=bool(p1), p2=bool(p2), p3=bool(p3))
    print(f"  {ma:>8} {len(x):>7} {int(pr.sum())//2:>6} {pr.mean():>8.4f} {ffu:>9.6f}"
          f" {ffd:>9.6f} {move:>+8.3f} {ffp:>9.6f} {pmove:>+9.3f}")

ps_lo = ladder[str(MINAREA_LADDER[0])]["pair_share"]
ps_hi = ladder[str(MINAREA_LADDER[-1])]["pair_share"]
print(f"\n  P1 rungs with frac_far(P_D) < union      : {n_p1}/5  (need >= {P1_MIN_RUNGS})")
print(f"  P2 rungs with |move| >= {P2_MIN_PP:.1f} pp          : {n_p2}/5  (need >= {P2_MIN_RUNGS})")
print(f"  P3 rungs with frac_far(pairs) > union    : {n_p3}/5  (need >= {P3_MIN_RUNGS})")
print(f"  P4 pair_share  minarea=2 {ps_lo:.4f}  vs  minarea=12 {ps_hi:.4f}")
verdict("P1", n_p1 >= P1_MIN_RUNGS, "n_rungs_PD_below_union", P1_MIN_RUNGS, ">=")
verdict("P2", n_p2 >= P2_MIN_RUNGS, "n_rungs_move_ge_3pp", P2_MIN_RUNGS, ">=")
verdict("P3", n_p3 >= P3_MIN_RUNGS, "n_rungs_pairs_above_union", P3_MIN_RUNGS, ">=")
verdict("P4", ps_lo > ps_hi, "pair_share_minarea2 - pair_share_minarea12", 0.0, ">")
for k in ("P1", "P2", "P3", "P4"):
    print(f"  {k} -> {'HELD' if V[k] else 'REFUTED'}")
if disagree:
    print(f"  ** P1/P3 DISAGREE at minarea {disagree} -- prereg sec.1b calls this a defect **")
    find_time(f"P1 and P3 are the same fact from two sides and disagree at "
              f"minarea {disagree}",
              "json:PASS9_RESULTS.json:/ladder", "ladder",
              "prereg sec.1b named this a defect before the run")
res["ladder"] = dict(rungs=ladder, n_p1=n_p1, n_p2=n_p2, n_p3=n_p3,
                     pair_share_lo=ps_lo, pair_share_hi=ps_hi, p1_p3_disagree=disagree)

# ================================================ BLOCK C  ANCHORED CITATIONS
print("\n" + "=" * 78)
print("C   A citable() THAT CAN FAIL -- positive control first")
print("=" * 78)


def citable(c):
    """Strengthened over measure_pass8.py:citable. Grammar:
         file:PATH[|ANCHOR]      anchor must appear ANYWHERE in the file
         line:PATH:N[|ANCHOR]    anchor must appear ON THAT LINE
         json:PATH:/ptr          the pointer must resolve
    An unanchored file:/line: cite resolves on existence alone, as before --
    the strengthening is that a row MAY carry an anchor and then must satisfy it."""
    try:
        anchor = None
        if "|" in c:
            c, anchor = c.split("|", 1)
        kind, rest = c.split(":", 1)
        if kind == "file":
            if not os.path.exists(rest):
                return False
            if anchor is None:
                return True
            with open(rest, encoding="utf-8", errors="replace") as fh:
                return anchor in fh.read()
        if kind == "line":
            f, ln = rest.rsplit(":", 1)
            if not os.path.exists(f):
                return False
            with open(f, encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
            n = int(ln)
            if len(lines) < n or n < 1:
                return False
            return True if anchor is None else (anchor in lines[n - 1])
        if kind == "json":
            f, ptr = rest.split(":", 1)
            if not os.path.exists(f):
                return False
            o = json.load(open(f))
            for part in [p for p in ptr.split("/") if p]:
                if isinstance(o, dict):
                    if part not in o:
                        return False
                    o = o[part]
                else:
                    return False
            return True
    except Exception:
        return False
    return False


# prereg sec.3, the six fixed known-bad citations, transcribed literally
KNOWN_BAD = ["file:NO_SUCH_FILE.md",
             "line:measure_pass8.py:999999",
             "line:measure_pass8.py:1|ZZZ_NOT_IN_THIS_LINE",
             "json:PASS8_RESULTS.json:/no/such/pointer",
             "json:NO_SUCH_FILE.json:/D1",
             "file:PASS8_RESULTS.md|ZZZ_NOT_IN_THIS_FILE"]
n_rej = 0
for c in KNOWN_BAD:
    ok = citable(c)
    n_rej += int(not ok)
    print(f"  {'REJECTED' if not ok else '** ACCEPTED **':<16} {c}")
gate("C1_known_bad", len(KNOWN_BAD), len(KNOWN_BAD) - n_rej,
     "known-bad citations that the gauge ACCEPTED (kept = accepted = failure)")
print(f"  C1 rejected {n_rej}/{C1_REQUIRED} known-bad citations")
verdict("C1", n_rej == C1_REQUIRED, "n_known_bad_rejected", C1_REQUIRED, "==")
print(f"  C1 GATE -> {'FIRES' if V['C1'] else '**FURNITURE -- block C reports nothing**'}")

# The twelve legacy rows, now ANCHORED. Anchor rule, fixed and stated: the most
# specific literal identifier in the row's own `what` sentence. Written after
# the prereg was pushed and BEFORE this script was run -- disclosed in
# PASS9_RESULTS.md sec.C, because a hostile reader is owed the ordering.
LEGACY = [
  dict(id="DEF-01", pass_="L1", found_by="eye",
       what="el_match True 8/8 with n_dropped 0 -- a precondition that never rejected",
       cite="file:L1_T5_CANDIDATE.md", anchor="el_match"),
  dict(id="DEF-02", pass_="7", found_by="gauge",
       what="o['b'] > 0 rejected 0 objects at all five minarea rungs",
       cite="json:PASS7_RESULTS.json:/I/unexercised", anchor=None),
  dict(id="DEF-03", pass_="7", found_by="gauge",
       what="NO_POSITION branch never executes -- every alert carries x/y",
       cite="json:PASS7_RESULTS.json:/I/rejection_table/C_alert_has_position", anchor=None),
  dict(id="DEF-04", pass_="7", found_by="eye",
       what="I1 and I2 set to the SAME boolean -- the gauge grades its own success",
       cite="line:measure_pass7.py:352", anchor="I1"),
  dict(id="DEF-05", pass_="4", found_by="eye",
       what="PASS4_RESULTS.json stale against the prose that documents its correction",
       cite="file:CORRECTIONS.json", anchor="PASS4_RESULTS"),
  dict(id="DEF-06", pass_="7", found_by="eye",
       what="sep 'non-determinism' contradicted by exact 5-rung reproduction a day later",
       cite="json:PASS7_DIAG.json:/Q2/same_process", anchor=None),
  dict(id="DEF-07", pass_="6", found_by="eye",
       what="PASS6_RESULTS vs PASS6_DIAG frac_far differ 0.047 pp at the SAME minarea",
       cite="json:PASS6_DIAG.json:/D2b/ladder/5/frac_far", anchor=None),
  dict(id="DEF-08", pass_="7", found_by="gauge",
       what="7(a) is the wrong operation -- caught by B2, a pre-committed agreement control",
       cite="json:PASS7_RESULTS.json:/B/b2_gap_pp", anchor=None),
  dict(id="DEF-09", pass_="8", found_by="eye",
       what="the owed 'third procedure' is degenerate: P_C == P_A as a set",
       cite="file:PASS8_PREDICTIONS.md", anchor="P_C"),
  dict(id="DEF-10", pass_="8", found_by="eye",
       what="PASS8_PREDICTIONS N4's rationale mis-states BOTH structures: both compute "
            "Background inside the sign loop; the real difference is the extra bkg0 call "
            "and diag's FIVE extracts from one prep",
       cite="line:diag_pass6.py:114", anchor="Background"),
  dict(id="DEF-11", pass_="6a", found_by="eye",
       what="PAPER-00 sec.2 row 6a read 'PRE-REGISTERED, NOT RUN' for ~3h after L1 landed",
       cite="file:PAPER-00-ARCHITECTURE.md", anchor="PRE-REGISTERED, NOT RUN"),
  dict(id="DEF-12", pass_="6", found_by="eye",
       what="pass6_stats.py's re-run-and-diff gauge cannot fail a correct refactor -- "
            "it can only ever render one verdict",
       cite="line:pass6_stats.py:1", anchor="re-run"),
]
for r in LEGACY:
    r["found_at"] = "pass" + str(r["pass_"])
    r["found_by_provenance"] = "backfilled"      # BLOCK F: no exceptions
    full = r["cite"] + ("|" + r["anchor"] if r["anchor"] else "")
    r["cite_anchored"] = full
    r["citable_pass8_rule"] = bool(citable(r["cite"]))
    r["citable_anchored"] = bool(citable(full))

if V["C1"]:
    failed = [r["id"] for r in LEGACY if not r["citable_anchored"]]
    loosened = [r["id"] for r in LEGACY
                if r["citable_pass8_rule"] and not r["citable_anchored"]]
    gate("C_anchored_resolves", len(LEGACY),
         sum(1 for r in LEGACY if r["citable_anchored"]),
         "the row's cited location contains the row's own anchor")
    print(f"\n  legacy rows: {len(LEGACY)}   FAIL anchoring: {len(failed)} {failed}")
    print(f"  rows pass 8 called citable that anchoring rejects: {loosened}")
    for r in LEGACY:
        if not r["citable_anchored"]:
            print(f"    UNCITABLE  {r['id']}  {r['cite_anchored']}")
    c2 = (("DEF-10" in failed) and ("DEF-04" not in failed) and ("DEF-02" not in failed))
    print(f"\n  C2  DEF-10 fails: {'DEF-10' in failed}   DEF-04 survives: "
          f"{'DEF-04' not in failed}   DEF-02 survives: {'DEF-02' not in failed}")
    verdict("C2", c2, "three named C2 outcomes all correct", None, "==")
    verdict("C3", len(failed) >= C3_MIN_FAIL, "n_legacy_failing_anchor", C3_MIN_FAIL, ">=")
    print(f"  C2 -> {'HELD' if V['C2'] else 'REFUTED'}"
          f"    C3 -> {'HELD' if V['C3'] else 'REFUTED'}  ({len(failed)} failing)")
    if failed:
        find_time(f"citation rot in DEFECT_REGISTER: {len(failed)} of 12 legacy rows "
                  f"cite a location that no longer contains what the row describes "
                  f"({failed})",
                  "json:PASS9_RESULTS.json:/C", "C3",
                  "found by the anchored citable(), which is a gauge, at run time")
else:
    failed, loosened = [], []
    verdict("C2", None, "three named C2 outcomes all correct", None, "==")
    verdict("C3", None, "n_legacy_failing_anchor", C3_MIN_FAIL, ">=")
    print("  ** C1 did not fire -- C2/C3 UNSCORED, exactly as pass 8's G2 should have been **")
res["C"] = dict(known_bad=KNOWN_BAD, n_rejected=n_rej, legacy=LEGACY,
                failed=failed, loosened_by_pass8_rule=loosened)

# ================================================== BLOCK F  found_by AT FIND TIME
print("\n" + "=" * 78)
print("F   found_by AT FIND TIME -- and the retirement of G1")
print("=" * 78)
n_ft = len(FINDTIME)
print(f"  find-time rows produced by pass 9 : {n_ft}   (F1 threshold < {F1_MAX_FINDTIME})")
for r in FINDTIME:
    print(f"    {r['id']}  [{r['found_by']}/{r['found_by_provenance']}]  {r['what'][:88]}")
verdict("F1", n_ft < F1_MAX_FINDTIME, "n_findtime_rows", F1_MAX_FINDTIME, "<")
print(f"  F1 -> {'HELD' if V['F1'] else 'REFUTED'}")
if V["F1"]:
    g1_state = ("RETIRED -- n_findtime = %d is under the floor. The eye-vs-gauge "
                "ratio is UNMEASURED. Pass 8's G1 was computed on a backfilled, "
                "self-generated denominator and does not survive into the paper."
                % n_ft)
else:
    g1_state = ("RE-SCORABLE on find-time rows only -- n_findtime = %d. The pass-8 "
                "G1 number is still void; a new one may be computed from find-time "
                "rows and must be labelled as pass-9-onward." % n_ft)
print("  " + g1_state.replace(". ", ".\n  "))
REGISTER = LEGACY + FINDTIME
json.dump(REGISTER, open("DEFECT_REGISTER.json", "w"), indent=2)
n_bf = sum(1 for r in REGISTER if r["found_by_provenance"] == "backfilled")
print(f"  DEFECT_REGISTER.json rewritten: {len(REGISTER)} rows "
      f"({n_bf} backfilled, {n_ft} find-time)")
res["F"] = dict(n_findtime=n_ft, n_backfilled=n_bf, findtime_rows=FINDTIME,
                g1_state=g1_state)

# ================================================ R4-CONTROL  ON THIS RUN'S SHAPE
print("\n" + "=" * 78)
print("R4-CONTROL  inject a duplicate triple into a COPY of pass 9's own verdicts")
print("=" * 78)
probe = {k: t for k, t in TRIPLES.items() if k != "R4-CONTROL"}
victim = sorted(probe)[0]
probe["ZZ-INJECTED"] = probe[victim]
coll_probe = r4_check(probe)
fired = any("ZZ-INJECTED" in (a, b) for a, b, _ in coll_probe)
for a, b, t in coll_probe:
    print(f"  COLLISION  {a} and {b} on {t}")
print(f"  duplicate of {victim} injected; R4 fires -> "
      f"{'YES' if fired else '**NO -- R4 IS FURNITURE**'}")
verdict("R4-CONTROL", fired, "r4_fires_on_injected_duplicate", None, "==")
coll9 = r4_check({k: t for k, t in TRIPLES.items() if k != "R4-CONTROL"})
print(f"  R4 on pass 9's own verdicts: "
      f"{'CLEAN' if not coll9 else '** %d COLLISION(S) **' % len(coll9)}")
for a, b, t in coll9:
    print(f"    COLLISION  {a} / {b}  {t}")
res["R4"] = dict(collisions=[[a, b, list(t)] for a, b, t in coll9], ok=not coll9,
                 control_fired=fired, injected_duplicate_of=victim)

# =========================================== R2/R3  UNEXERCISED PRECONDITIONS
print("\n" + "=" * 78)
print("R2  UNEXERCISED-PRECONDITION GAUGE")
print("=" * 78)
for k in sorted(REJ):
    d = REJ[k]
    flag = "  <== REJECTED NOTHING" if d["n_rejected"] == 0 else ""
    print(f"  {k:32s} in={d['n_in']:>7} kept={d['n_kept']:>7} "
          f"rejected={d['n_rejected']:>7}{flag}")
unexercised = sorted(k for k, d in REJ.items() if d["n_rejected"] == 0)
if unexercised:
    print(f"\n  !! R3 WARNING: {len(unexercised)} precondition(s) rejected NOTHING:")
    for k in unexercised:
        print(f"     - {k}")
res["unexercised"] = unexercised
res["rejections"] = REJ

# ============================================================ R1 ASSERTION
REGISTERED = ["P0", "P1", "P2", "P3", "P4", "P5", "P6",
              "S-NULL", "S1", "S2", "C1", "C2", "C3", "F1", "R4-CONTROL"]
missing = [k for k in REGISTERED if k not in V]
extra = [k for k in V if k not in REGISTERED]
res["verdicts"] = {k: V[k] for k in REGISTERED if k in V}
res["triples"] = {k: list(TRIPLES[k]) for k in TRIPLES}
res["R1"] = dict(registered=REGISTERED, missing=missing, extra=extra,
                 ok=(not missing and not extra))

EXCLUDED = {"P0", "S-NULL", "C1", "R4-CONTROL"}      # prereg sec.5
scored = [k for k in REGISTERED if k not in EXCLUDED]
held = sum(1 for k in scored if V.get(k) is True)
refuted = sum(1 for k in scored if V.get(k) is False)
unscored = [k for k in scored if V.get(k) is None]

json.dump(res, open("PASS9_RESULTS.json", "w"), indent=2)
print("\n" + "=" * 78)
print(f"=== {held}/{len(scored)} pre-registered predictions HELD"
      f"   ({refuted} refuted, {len(unscored)} unscored) ===")
if unscored:
    print(f"    UNSCORED (gate failed upstream): {unscored}")
print(f"    excluded from the total: {sorted(EXCLUDED)}  (prereg sec.5)")
print(f"    P0 reproduction : {'HOLDS' if V.get('P0') else '**VOID**'}")
print(f"    S-NULL gate     : {'PASS' if V.get('S-NULL') else '**VOID**'}")
print(f"    C1 gate         : {'FIRES' if V.get('C1') else '**FURNITURE**'}")
print(f"    R4-CONTROL      : {'FIRED' if V.get('R4-CONTROL') else '**FURNITURE**'}")
print("wrote PASS9_RESULTS.json + DEFECT_REGISTER.json")
assert not missing and not extra, f"R1 VIOLATED: missing={missing} extra={extra}"
print("R1 satisfied: a verdict key exists for every registered prediction letter")
