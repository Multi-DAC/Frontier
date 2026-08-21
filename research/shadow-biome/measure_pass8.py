"""PASS 8 -- BLOCK D (resolve B2 against an external anchor) + BLOCK G (gauge
independence). Block N lives in nondet_pass8.py and is merged here.

Governed by PASS8_PREDICTIONS.md, committed and pushed (6567f2b) BEFORE this
file existed. Every threshold below is COPIED from that file, not chosen here.

  D1     IDENTITY CONTROL: P_C (collapse-then-drop) == P_A (sign=+1) as a set
  D2     ZTF issues negative-difference alerts on these frames, >= 1.0%
  D3     RULING: r_neg >= r_pos - 10.0 pp
  D4     the pre-committed decision rule, applied
  D5     unpaired negatives are not huddled near bright positives, ratio >= 0.67
  D6     the D3 gap keeps its SIGN at >= 4 of 5 minarea rungs
  G1     eye >= 2 * gauge in DEFECT_REGISTER.json
  G2     >= 1 register row has no citable artifact
  R4     no two verdicts share a (quantity, threshold, comparator) triple
  R4-CONTROL  R4 run against PASS 7's verdict set MUST fire on I1/I2

R1: a verdict key for every registered letter, asserted against a literal list.
R2: every gate records its rejections; zero-rejection gates are named.
"""
import json, os, glob, sys
import numpy as np
import sep
from astropy.io import fits

# ------------------------------------------ constants COPIED, not re-chosen
THRESH, MATCH, WALL = 5.0, 2.0, 1.6      # measure_pass6.py:27-29
PAIR_RADIUS = 10.0                        # diag_pass6.py:21
MINAREA_LADDER = [2, 3, 5, 8, 12]
CAT_MINAREA = 5
# PASS8_PREDICTIONS.md sec.1b / sec.3 thresholds
D2_MIN_NEG_SHARE = 0.010
D3_TOL_PP = 10.0
D5_MIN_RATIO = 0.67
D6_MIN_RUNGS = 4
G1_FACTOR = 2.0
# prereg sec.1b: every spelling accepted, the set is FIXED HERE
NEG_TOKENS = {"f", "F", "0", "-1", -1, 0, False}

REJ = {}
V = {}
TRIPLES = {}          # R4: verdict -> (quantity, threshold, comparator)


def gate(name, n_in, n_kept, note=""):
    d = REJ.setdefault(name, {"n_in": 0, "n_kept": 0, "n_rejected": 0, "note": note})
    d["n_in"] += int(n_in)
    d["n_kept"] += int(n_kept)
    d["n_rejected"] += int(n_in - n_kept)
    return d


def verdict(key, value, quantity, threshold, comparator):
    """R4: a verdict must declare WHAT it was decided on. Collisions are a
    hard failure -- measure_pass7.py:352-353 set I1 and I2 to one boolean."""
    V[key] = None if value is None else bool(value)
    TRIPLES[key] = (str(quantity), None if threshold is None else float(threshold),
                    str(comparator))
    return V[key]


def r4_check(triples, label):
    """Return the list of colliding verdict-key pairs."""
    seen, coll = {}, []
    for k, t in triples.items():
        if t in seen:
            coll.append((seen[t], k, t))
        else:
            seen[t] = k
    return coll


def pair_mask(X, Y, SG, IM):
    """Mutual nearest neighbour <= PAIR_RADIUS px, opposite sign.
    Transcribed from diag_pass7.py:38-56 so D1 is not tested against itself
    with a different implementation of the thing under test."""
    n = len(X)
    paired = np.zeros(n, bool)
    drop = np.zeros(n, bool)          # the '-' member of each mutual opp pair
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


res = {"prereg": "PASS8_PREDICTIONS.md", "prereg_commit": "6567f2b"}

# ====================================================== load frozen catalogue
cat = np.load("PASS6_catalog.npz", allow_pickle=True)
EL, SG, IM = cat["elong"], cat["sign"], cat["image"]
X, Y, PK = cat["x"], cat["y"], cat["peak"]
N = len(EL)
FAR = EL > WALL
paired, drop = pair_mask(X, Y, SG, IM)
pos, neg = SG > 0, SG < 0
unp_pos = pos & ~paired
unp_neg = neg & ~paired

# ============================================================== D1  IDENTITY
print("=" * 78)
print("D1  IDENTITY CONTROL -- is the owed 'third procedure' actually 7(a)?")
print("=" * 78)
P_A = pos.copy()
P_B = ~drop                                    # 7(b): pair-collapse
P_C = P_B & ~unp_neg                           # ... and drop unpaired negatives
gate("D1_collapse_drops", N, int((~drop).sum()),
     "7(b) removes the '-' member of each mutual opposite-sign pair")
gate("D1_unpaired_neg_drops", int(P_B.sum()), int(P_C.sum()),
     "P_C additionally removes unpaired negatives")

same_set = bool(np.array_equal(P_A, P_C))
ff_A, ff_C = float(FAR[P_A].mean()), float(FAR[P_C].mean())
ff_B = float(FAR[P_B].mean())
print(f"  |P_A| = {int(P_A.sum())}   |P_B| = {int(P_B.sum())}   |P_C| = {int(P_C.sum())}")
print(f"  frac_far  P_A = {ff_A:.6f}   P_B = {ff_B:.6f}   P_C = {ff_C:.6f}")
print(f"  P_A and P_C identical as a SET : {same_set}")
verdict("D1", same_set and abs(ff_A - ff_C) == 0.0,
        "set_equality(P_A,P_C) and |ff_A-ff_C|", 0.0, "==")
print(f"  D1 CONTROL -> {'HOLDS' if V['D1'] else '**VOID -- pairing code is broken**'}"
      f"   (excluded from the held-total, prereg sec.5)")
if same_set:
    print("  ** CONFIRMED: the owed 'third procedure' IS 7(a). The debt was")
    print("     mis-specified against prose, not against measure_pass7.py. **")
res["D1"] = dict(n_A=int(P_A.sum()), n_B=int(P_B.sum()), n_C=int(P_C.sum()),
                 frac_far_A=ff_A, frac_far_B=ff_B, frac_far_C=ff_C,
                 identical=same_set)

# ================================================ D2  THE EXTERNAL ANCHOR
print("\n" + "=" * 78)
print("D2  DOES ZTF ITSELF ALERT ON NEGATIVE DIFFERENCES ON THESE 20 FRAMES?")
print("=" * 78)
alerts_all = json.load(open("PASS5_alert_index.json"))
files = sorted(glob.glob("diffimg/*.fz"))
frames = {os.path.basename(p)[:-3] for p in files}
alerts = [a for a in alerts_all if a["f"] in frames]
gate("D2_alerts_on_our_frames", len(alerts_all), len(alerts),
     "alert's frame is one of the 20 images in diffimg/")

def is_neg(a):
    v = a.get("isdiffpos")
    return v in NEG_TOKENS

with_flag = [a for a in alerts if a.get("isdiffpos") is not None]
gate("D2_alert_has_isdiffpos", len(alerts), len(with_flag),
     "alert carries an isdiffpos label at all")
neg_al = [a for a in with_flag if is_neg(a)]
pos_al = [a for a in with_flag if not is_neg(a)]
neg_share = len(neg_al) / len(with_flag) if with_flag else float("nan")
spellings = sorted({repr(a.get("isdiffpos")) for a in with_flag})
print(f"  alerts on our 20 frames : {len(alerts)}   carrying isdiffpos: {len(with_flag)}")
print(f"  distinct isdiffpos spellings seen : {spellings}")
print(f"  ZTF NEGATIVE alerts : {len(neg_al)}   POSITIVE : {len(pos_al)}"
      f"   neg share = {100*neg_share:.3f}%")
verdict("D2", neg_share >= D2_MIN_NEG_SHARE, "neg_share", D2_MIN_NEG_SHARE, ">=")
print(f"  D2 neg share >= {100*D2_MIN_NEG_SHARE:.1f}%  -> "
      f"{'HELD' if V['D2'] else 'REFUTED'}")
if not V["D2"]:
    print("  ** ANCHOR VOID. D3/D5/D6 are still measured and reported, but D4's")
    print("     ruling is NO RULING -- prereg sec.1b: a missing anchor is an")
    print("     unknown, not a pass. **")
res["D2"] = dict(n_alerts_all=len(alerts_all), n_alerts_frames=len(alerts),
                 n_with_flag=len(with_flag), spellings=spellings,
                 n_neg=len(neg_al), n_pos=len(pos_al), neg_share=neg_share)


# ================================================ D3  THE RULING MEASUREMENT
def match_rates(x, y, sg, im, unp_pos_m, unp_neg_m, alist):
    """For each alert, nearest detection on its own frame within MATCH px.
    Returns (r_neg, r_pos, detail). Denominator is ALL alerts of that sign,
    matched or not -- prereg sec.1b, kept literal."""
    idx_by_img = {}
    for k, fn in enumerate(im):
        idx_by_img.setdefault(fn, []).append(k)
    idx_by_img = {k: np.array(v) for k, v in idx_by_img.items()}

    hit = {"neg_in_unp_neg": 0, "pos_in_unp_pos": 0,
           "neg_total": 0, "pos_total": 0,
           "neg_matched": 0, "pos_matched": 0}
    for a in alist:
        ax, ay = a.get("x"), a.get("y")
        neg_flag = is_neg(a)
        hit["neg_total" if neg_flag else "pos_total"] += 1
        if ax is None or ay is None:
            continue
        m = idx_by_img.get(a["f"])
        if m is None or not len(m):
            continue
        d = np.hypot(x[m] + 1 - ax, y[m] + 1 - ay)   # FITS 1-indexed, as pass 5/6
        j = int(d.argmin())
        if d[j] > MATCH:
            continue
        k = int(m[j])
        hit["neg_matched" if neg_flag else "pos_matched"] += 1
        if neg_flag and unp_neg_m[k]:
            hit["neg_in_unp_neg"] += 1
        if (not neg_flag) and unp_pos_m[k]:
            hit["pos_in_unp_pos"] += 1
    r_neg = hit["neg_in_unp_neg"] / hit["neg_total"] if hit["neg_total"] else float("nan")
    r_pos = hit["pos_in_unp_pos"] / hit["pos_total"] if hit["pos_total"] else float("nan")
    return r_neg, r_pos, hit


print("\n" + "=" * 78)
print("D3  RULING: do ZTF's negative alerts land on our UNPAIRED negatives?")
print("=" * 78)
r_neg, r_pos, hit = match_rates(X, Y, SG, IM, unp_pos, unp_neg, with_flag)
gap_pp = 100.0 * (r_neg - r_pos)
print(f"  unpaired negatives in catalogue : {int(unp_neg.sum())}"
      f"   unpaired positives : {int(unp_pos.sum())}")
print(f"  ZTF neg alerts {hit['neg_total']:>5}  matched {hit['neg_matched']:>5}"
      f"  of which UNPAIRED-NEG {hit['neg_in_unp_neg']:>5}   r_neg = {r_neg:.4f}")
print(f"  ZTF pos alerts {hit['pos_total']:>5}  matched {hit['pos_matched']:>5}"
      f"  of which UNPAIRED-POS {hit['pos_in_unp_pos']:>5}   r_pos = {r_pos:.4f}")
print(f"  gap r_neg - r_pos = {gap_pp:+.3f} pp   (threshold >= -{D3_TOL_PP:.1f})")
verdict("D3", gap_pp >= -D3_TOL_PP, "r_neg - r_pos (pp)", -D3_TOL_PP, ">=")
print(f"  D3 -> {'HELD' if V['D3'] else 'REFUTED'}")
res["D3"] = dict(r_neg=r_neg, r_pos=r_pos, gap_pp=gap_pp, counts=hit,
                 n_unpaired_neg=int(unp_neg.sum()), n_unpaired_pos=int(unp_pos.sum()))

# =========================================== D5  THE JUNK HYPOTHESIS, DIRECT
print("\n" + "=" * 78)
print("D5  ARE UNPAIRED NEGATIVES HUDDLED AROUND BRIGHT POSITIVES?")
print("=" * 78)
d_neg, d_pos = [], []
for fn in np.unique(IM):
    m = np.where(IM == fn)[0]
    p_here = m[pos[m]]
    if not len(p_here):
        continue
    thr = np.percentile(PK[p_here], 90.0)
    bright = p_here[PK[p_here] >= thr]
    gate("D5_bright_decile", len(p_here), len(bright),
         "top-decile peak positives on the frame")
    if not len(bright):
        continue
    bx, by = X[bright], Y[bright]
    for sel, sink in ((unp_neg, d_neg), (unp_pos, d_pos)):
        q = m[sel[m]]
        if not len(q):
            continue
        dd = np.hypot(X[q][:, None] - bx[None, :], Y[q][:, None] - by[None, :])
        sink.extend(dd.min(axis=1).tolist())
med_neg = float(np.median(d_neg)) if d_neg else float("nan")
med_pos = float(np.median(d_pos)) if d_pos else float("nan")
ratio = med_neg / med_pos if med_pos else float("nan")
print(f"  median distance to nearest bright positive:")
print(f"    unpaired NEGATIVES : {med_neg:8.2f} px   (n={len(d_neg)})")
print(f"    unpaired POSITIVES : {med_pos:8.2f} px   (n={len(d_pos)})")
print(f"    ratio neg/pos = {ratio:.4f}   (threshold >= {D5_MIN_RATIO})")
verdict("D5", ratio >= D5_MIN_RATIO, "median_dist_ratio", D5_MIN_RATIO, ">=")
print(f"  D5 -> {'HELD' if V['D5'] else 'REFUTED'}"
      f"   (refuted = they huddle = halo residuals)")
res["D5"] = dict(median_unpaired_neg=med_neg, median_unpaired_pos=med_pos,
                 ratio=ratio, n_neg=len(d_neg), n_pos=len(d_pos))

# ======================================== D6  THE GAP AS A CURVE, NOT A SCALAR
print("\n" + "=" * 78)
print("D6  THE D3 GAP OVER THE minarea LADDER  (re-extraction, 20 images)")
print("=" * 78)
rungs = {}
for ma in MINAREA_LADDER:
    rungs[ma] = dict(x=[], y=[], sg=[], im=[], el=[])

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
            gate(f"D6_b_positive_minarea{ma}", len(o), int(ok.sum()),
                 "sep semi-minor axis b > 0")
            k = int(ok.sum())
            rungs[ma]["x"].append(o["x"][ok])
            rungs[ma]["y"].append(o["y"][ok])
            rungs[ma]["el"].append(o["a"][ok] / o["b"][ok])
            rungs[ma]["sg"].append(np.full(k, sign))
            rungs[ma]["im"].append(np.full(k, fn, dtype=object))
    print(f"    {fn[22:46]} done", flush=True)

print(f"\n  {'minarea':>8} {'n':>7} {'r_neg':>9} {'r_pos':>9} {'gap_pp':>9} {'sign':>6}")
ladder_out, signs = {}, []
for ma in MINAREA_LADDER:
    d = rungs[ma]
    x = np.concatenate(d["x"]); y = np.concatenate(d["y"])
    sg = np.concatenate(d["sg"]); el = np.concatenate(d["el"])
    im = np.concatenate(d["im"]).astype("U57")
    pr, dr = pair_mask(x, y, sg, im)
    up = (sg > 0) & ~pr
    un = (sg < 0) & ~pr
    rn, rp, h = match_rates(x, y, sg, im, up, un, with_flag)
    g = 100.0 * (rn - rp)
    s = int(np.sign(g))
    signs.append(s)
    ladder_out[str(ma)] = dict(n=int(len(x)), r_neg=rn, r_pos=rp, gap_pp=g,
                               n_unpaired_neg=int(un.sum()),
                               n_unpaired_pos=int(up.sum()),
                               frac_far_union=float((el > WALL).mean()),
                               counts=h)
    print(f"  {ma:>8} {len(x):>7} {rn:>9.4f} {rp:>9.4f} {g:>+9.3f} {s:>6}")

ref_sign = int(np.sign(gap_pp))
n_agree = sum(1 for s in signs if s == ref_sign)
print(f"\n  frozen-catalogue gap sign = {ref_sign:+d};"
      f" ladder rungs agreeing: {n_agree}/{len(MINAREA_LADDER)}")
verdict("D6", n_agree >= D6_MIN_RUNGS, "n_rungs_agreeing_on_sign",
        D6_MIN_RUNGS, ">=")
print(f"  D6 sign holds at >= {D6_MIN_RUNGS} rungs -> "
      f"{'HELD' if V['D6'] else 'REFUTED'}")
res["D6"] = dict(ladder=ladder_out, reference_sign=ref_sign, n_agree=n_agree,
                 signs=signs)

# ================================================= D4  THE PRE-COMMITTED RULE
print("\n" + "=" * 78)
print("D4  APPLYING THE DECISION RULE  (prereg sec.1b -- written before the data)")
print("=" * 78)
if not V["D2"]:
    ruling = "NO RULING -- the anchor is void (D2 refuted). Section 8 stays PROVISIONAL."
elif V["D3"]:
    ruling = ("D3 HELD -> the 2505 unpaired negatives are a ZTF-validated population. "
              "7(a) is CONFIRMED as the wrong operation. PAPER-00 sec.8's amendment "
              "(7b, 0.217 pp) is PROMOTED from PROVISIONAL to STANDING. B2's refutation "
              "is recorded as having caught a PLAN defect, not a measurement defect.")
else:
    ruling = ("D3 REFUTED -> the unpaired negatives are NOT externally corroborated. "
              "PAPER-00 sec.8's amendment STAYS PROVISIONAL and the paper must report "
              "frac_far under BOTH procedures side by side, with the disagreement "
              "stated. It may NOT pick the one that reads better.")
print("  " + ruling.replace(". ", ".\n  "))
verdict("D4", None, "decision rule (not a prediction)", None, "n/a")
res["D4"] = dict(ruling=ruling, d2=V["D2"], d3=V["D3"])

# ============================================ BLOCK G  THE DEFECT REGISTER
print("\n" + "=" * 78)
print("G   DEFECT REGISTER -- the pattern claim gets a NOTATION")
print("=" * 78)
# Each row: what, found_by (gauge|eye), and a CITATION that is CHECKED below.
# 'gauge' means an automated check surfaced it without my reading for it.
REGISTER = [
  dict(id="DEF-01", pass_="L1", found_by="eye",
       what="el_match True 8/8 with n_dropped 0 -- a precondition that never rejected",
       cite="file:L1_T5_CANDIDATE.md"),
  dict(id="DEF-02", pass_="7", found_by="gauge",
       what="o['b'] > 0 rejected 0 objects at all five minarea rungs",
       cite="json:PASS7_RESULTS.json:/I/unexercised"),
  dict(id="DEF-03", pass_="7", found_by="gauge",
       what="NO_POSITION branch never executes -- every alert carries x/y",
       cite="json:PASS7_RESULTS.json:/I/rejection_table/C_alert_has_position"),
  dict(id="DEF-04", pass_="7", found_by="eye",
       what="I1 and I2 set to the SAME boolean -- the gauge grades its own success",
       cite="line:measure_pass7.py:352"),
  dict(id="DEF-05", pass_="4", found_by="eye",
       what="PASS4_RESULTS.json stale against the prose that documents its correction",
       cite="file:CORRECTIONS.json"),
  dict(id="DEF-06", pass_="7", found_by="eye",
       what="sep 'non-determinism' contradicted by exact 5-rung reproduction a day later",
       cite="json:PASS7_DIAG.json:/Q2/same_process"),
  dict(id="DEF-07", pass_="6", found_by="eye",
       what="PASS6_RESULTS vs PASS6_DIAG frac_far differ 0.047 pp at the SAME minarea",
       cite="json:PASS6_DIAG.json:/D2b/ladder/5/frac_far"),
  dict(id="DEF-08", pass_="7", found_by="gauge",
       what="7(a) is the wrong operation -- caught by B2, a pre-committed agreement control",
       cite="json:PASS7_RESULTS.json:/B/b2_gap_pp"),
  dict(id="DEF-09", pass_="8", found_by="eye",
       what="the owed 'third procedure' is degenerate: P_C == P_A as a set",
       cite="file:PASS8_PREDICTIONS.md"),
  dict(id="DEF-10", pass_="8", found_by="eye",
       what="PASS8_PREDICTIONS N4's rationale mis-states BOTH structures: both compute "
            "Background inside the sign loop; the real difference is the extra bkg0 call "
            "and diag's FIVE extracts from one prep",
       cite="line:diag_pass6.py:114"),
  dict(id="DEF-11", pass_="6a", found_by="eye",
       what="PAPER-00 sec.2 row 6a read 'PRE-REGISTERED, NOT RUN' for ~3h after L1 landed",
       cite="file:PAPER-00-ARCHITECTURE.md"),
  dict(id="DEF-12", pass_="6", found_by="eye",
       what="pass6_stats.py's re-run-and-diff gauge cannot fail a correct refactor -- "
            "it can only ever render one verdict",
       cite="line:pass6_stats.py:1"),
]


def citable(c):
    """G2 is MECHANICAL: a citation is real only if it resolves on disk."""
    try:
        kind, rest = c.split(":", 1)
        if kind == "file":
            return os.path.exists(rest)
        if kind == "line":
            f, ln = rest.rsplit(":", 1)
            if not os.path.exists(f):
                return False
            with open(f, encoding="utf-8", errors="replace") as fh:
                return len(fh.readlines()) >= int(ln)
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


for r in REGISTER:
    r["citable"] = bool(citable(r["cite"]))
gate("G_citation_resolves", len(REGISTER),
     sum(1 for r in REGISTER if r["citable"]),
     "the row's cited artifact actually exists on disk")

cited = [r for r in REGISTER if r["citable"]]
uncit = [r for r in REGISTER if not r["citable"]]
n_eye = sum(1 for r in cited if r["found_by"] == "eye")
n_gauge = sum(1 for r in cited if r["found_by"] == "gauge")
print(f"  register rows: {len(REGISTER)}   citable: {len(cited)}   UNCITABLE: {len(uncit)}")
for r in uncit:
    print(f"    UNCITABLE  {r['id']}  cite={r['cite']}")
print(f"  found_by among CITABLE rows -- eye: {n_eye}   gauge: {n_gauge}")
verdict("G1", n_eye >= G1_FACTOR * n_gauge, "n_eye / n_gauge", G1_FACTOR, ">=")
print(f"  G1 eye >= {G1_FACTOR:g} x gauge -> {'HELD' if V['G1'] else 'REFUTED'}")
if not V["G1"]:
    print("  ** G1 REFUTED means I2's STANDING RATIONALE is wrong: 'every instrument")
    print("     defect in this program so far was found by me, by hand, late.'")
    print("     It has justified the whole instrument block and was never counted. **")
verdict("G2", len(uncit) >= 1, "n_uncitable", 1, ">=")
print(f"  G2 >= 1 uncitable row -> {'HELD' if V['G2'] else 'REFUTED'}")
res["G"] = dict(register=REGISTER, n_citable=len(cited), n_uncitable=len(uncit),
                n_eye=n_eye, n_gauge=n_gauge)
json.dump(REGISTER, open("DEFECT_REGISTER.json", "w"), indent=2)

# =================================== R4-CONTROL  THE KNOWN-BAD INPUT
print("\n" + "=" * 78)
print("R4-CONTROL  run the new gauge against PASS 7's verdict set")
print("=" * 78)
p7 = json.load(open("PASS7_RESULTS.json"))
p7v = p7["verdicts"]
# Triples reconstructed from measure_pass7.py, transcribed line by line.
P7_TRIPLES = {
    "A1": ("frac_far_plus", 0.4849906191369606, "<"),
    "A2": ("frac_far_plus", 0.35, ">="),
    "A3": ("a3_gap_pp", 3.0, ">="),
    "A4": ("a4_span_pp", 5.0, "<="),
    "B1": ("frac_far_collapsed", 0.4849906191369606, "<"),
    "B2": ("b2_gap_pp", 4.0, "<="),
    "B3": ("n_collapsed == n - n_mutual_opp", None, "=="),
    "C1": ("recovery", 0.7313829787234043, "=="),
    "C2": ("largest_residual_class", None, "=="),
    "C3": ("delta_mag", 1.0, ">="),
    "C4": ("frames_with_residual", 20.0, "=="),
    "I1": ("gauge_found", None, "=="),      # measure_pass7.py:352
    "I2": ("gauge_found", None, "=="),      # measure_pass7.py:353  <- the defect
}
coll7 = r4_check(P7_TRIPLES, "pass7")
fired = any({a, b} == {"I1", "I2"} for a, b, _ in coll7)
for a, b, t in coll7:
    print(f"  COLLISION  {a} and {b} decided on the SAME triple {t}")
print(f"  R4-CONTROL fires on I1/I2 -> {'YES' if fired else '**NO -- R4 IS FURNITURE**'}")
verdict("R4-CONTROL", fired, "r4_fires_on_pass7_I1I2", None, "==")
if not fired:
    print("  ** BLOCK G REPORTS ZERO. A gauge shown only its own clean output has")
    print("     not been tested (prereg sec.3). **")
res["R4_control"] = dict(collisions=[[a, b, list(t)] for a, b, t in coll7],
                         fired_on_I1_I2=fired, pass7_verdicts=p7v)

# =================================== R4  ON PASS 8'S OWN VERDICTS
coll8 = r4_check({k: t for k, t in TRIPLES.items() if k != "R4-CONTROL"}, "pass8")
print(f"\n  R4 on pass 8's own verdicts: "
      f"{'CLEAN' if not coll8 else '** %d COLLISION(S) **' % len(coll8)}")
for a, b, t in coll8:
    print(f"    COLLISION  {a} / {b}  {t}")
res["R4"] = dict(collisions=[[a, b, list(t)] for a, b, t in coll8], ok=not coll8)

# =================================== MERGE BLOCK N
print("\n" + "=" * 78)
print("BLOCK N  (merged from PASS8_NONDET.json)")
print("=" * 78)
if not os.path.exists("PASS8_NONDET.json"):
    print("  ** PASS8_NONDET.json ABSENT -- block N did not run. R1 will fail. **")
    nd = None
else:
    nd = json.load(open("PASS8_NONDET.json"))
    for k, v in nd["verdicts"].items():
        V[k] = v
        TRIPLES[k] = ("block-N:" + k, None, "see nondet_pass8.py")
    for k, d in nd.get("rejections", {}).items():
        REJ.setdefault("N::" + k, d)
    print(f"  in-process varying: {nd['n_vary_inproc']}/{nd['n_images']}   "
          f"fresh varying: {nd['n_vary_fresh']}/{nd['n_images']}")
    print(f"  struct M n={nd['struct_M']['n']} ff={nd['struct_M']['frac_far']:.6f}  |  "
          f"struct D n={nd['struct_D']['n']} ff={nd['struct_D']['frac_far']:.6f}")
    for k in ("N1", "N2", "N3", "N4", "N5", "N-NULL"):
        print(f"  {k:7s} -> {nd['verdicts'].get(k)}")
    res["N"] = nd

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
REGISTERED = ["D1", "D2", "D3", "D4", "D5", "D6",
              "N1", "N2", "N3", "N4", "N5",
              "G1", "G2", "R4-CONTROL", "N-NULL"]     # literal, from prereg sec.4
missing = [k for k in REGISTERED if k not in V]
extra = [k for k in V if k not in REGISTERED]
res["verdicts"] = {k: V[k] for k in REGISTERED if k in V}
res["triples"] = {k: list(TRIPLES[k]) for k in TRIPLES}
res["R1"] = dict(registered=REGISTERED, missing=missing, extra=extra,
                 ok=(not missing and not extra))

# prereg sec.5: D1, N-NULL, R4-CONTROL, D4 are EXCLUDED from the held-total
EXCLUDED = {"D1", "N-NULL", "R4-CONTROL", "D4"}
scored = [k for k in REGISTERED if k not in EXCLUDED]
held = sum(1 for k in scored if V.get(k) is True)
refuted = sum(1 for k in scored if V.get(k) is False)
unscored = [k for k in scored if V.get(k) is None]

json.dump(res, open("PASS8_RESULTS.json", "w"), indent=2)
print("\n" + "=" * 78)
print(f"=== {held}/{len(scored)} pre-registered predictions HELD"
      f"   ({refuted} refuted, {len(unscored)} unscored) ===")
if unscored:
    print(f"    UNSCORED (gate failed upstream): {unscored}")
print(f"    excluded from the total: {sorted(EXCLUDED)}  (prereg sec.5)")
print(f"    D1 identity   : {'HOLDS' if V.get('D1') else '**VOID**'}")
print(f"    N-NULL gate   : {'PASS' if V.get('N-NULL') else '**VOID**'}")
print(f"    R4-CONTROL    : {'FIRED' if V.get('R4-CONTROL') else '**FURNITURE**'}")
print("wrote PASS8_RESULTS.json + DEFECT_REGISTER.json")
assert not missing and not extra, f"R1 VIOLATED: missing={missing} extra={extra}"
print("R1 satisfied: a verdict key exists for every registered prediction letter")
