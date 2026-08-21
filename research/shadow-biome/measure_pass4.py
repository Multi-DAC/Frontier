"""
PASS 4 measurement — ZTF public alerts, night of 2018-06-01.
Governed by PREREGISTRATION.md and PASS4_PREDICTIONS.md (+ AMENDMENT 1).
Both were committed and pushed BEFORE this file was run and before the tarball
was opened. Every threshold below is copied from those documents, not chosen here.

Prints n beside every fraction (PREREGISTRATION.md §5).
"""
import tarfile, io, json, sys, collections
import fastavro

TARBALL = "data/ztf_public_20180601.tar.gz"

# --- thresholds, quoted from ZTF Explanatory Supplement v5.0 §9.1 ---------
# packaging (already applied by IPAC to everything in this file):
PKG = dict(nbad=4, fwhm=7.0, elong=1.6, magdiff_lo=-0.4, magdiff_hi=0.75)
# survey's own SUGGESTED purity cuts, shape half only (no rb cut):
PUR = dict(nbad=0, fwhm=5.0, elong=1.2, magdiff_abs=0.1)

rows = []
n_files = n_parse_fail = 0

with tarfile.open(TARBALL, "r:gz") as tf:
    for member in tf:
        if not member.isfile() or not member.name.endswith(".avro"):
            continue
        n_files += 1
        try:
            buf = io.BytesIO(tf.extractfile(member).read())
            rec = next(iter(fastavro.reader(buf)))
            c = rec["candidate"]
            rows.append((
                c.get("elong"), c.get("fwhm"), c.get("nbad"),
                c.get("magap"), c.get("magpsf"), c.get("rb"),
                c.get("isdiffpos"), c.get("programid"), c.get("fid"),
            ))
        except Exception:
            n_parse_fail += 1
        if n_files % 20000 == 0:
            print(f"  ...{n_files} files", file=sys.stderr, flush=True)

N_files = n_files
print(f"avro files in tarball : {N_files}")
print(f"parse failures        : {n_parse_fail}")

# drop rows with a missing field needed by any cut -- counted, not silently dropped
usable = [r for r in rows if None not in (r[0], r[1], r[2], r[3], r[4])]
N = len(usable)
print(f"rows with all 5 cut fields present : {N}  (dropped {len(rows)-N})")

progs = collections.Counter(r[7] for r in rows)
print(f"programid distribution : {dict(progs)}")
fids = collections.Counter(r[8] for r in rows)
print(f"filter (fid) distribution : {dict(fids)}")

def magdiff(r):
    return r[3] - r[4]          # magap - magpsf, per §9.1

cuts = {
    "nbad=0":          lambda r: r[2] == PUR["nbad"],
    "fwhm<=5":         lambda r: r[1] <= PUR["fwhm"],
    "elong<=1.2":      lambda r: r[0] <= PUR["elong"],
    "|magdiff|<=0.1":  lambda r: abs(magdiff(r)) <= PUR["magdiff_abs"],
}

# ---- sanity: does the data actually respect the PACKAGING cuts? ----------
print("\n--- SANITY: packaging cuts should already hold for every row ---")
viol = {
    "nbad<=4":   sum(1 for r in usable if r[2] > PKG["nbad"]),
    "fwhm<=7":   sum(1 for r in usable if r[1] > PKG["fwhm"]),
    "elong<=1.6":sum(1 for r in usable if r[0] > PKG["elong"]),
    "magdiff in [-0.4,0.75]": sum(
        1 for r in usable if not (PKG["magdiff_lo"] <= magdiff(r) <= PKG["magdiff_hi"])),
}
for k, v in viol.items():
    print(f"  violations of {k:24s}: {v}  ({100*v/N:.4f}% of n={N})")

# ---- M1 / M1c : all four purity cuts jointly -----------------------------
survivors = [r for r in usable if all(f(r) for f in cuts.values())]
S = len(survivors) / N
print("\n--- M1 / M1c : joint purity-cut survival (no rb cut) ---")
print(f"  n_in  = {N}")
print(f"  n_out = {len(survivors)}")
print(f"  S     = {100*S:.3f}%")

# ---- M3 : per-cut attribution, one-at-a-time AND leave-one-out ----------
print("\n--- M3 : per-cut attribution at stage 2 ---")
print(f"{'cut':18s} {'one-at-a-time n':>16s} {'%':>9s}   {'leave-one-out n':>16s} {'%':>9s}")
m3 = {}
for name, f in cuts.items():
    oaat = sum(1 for r in usable if f(r))
    others = [g for k, g in cuts.items() if k != name]
    loo = sum(1 for r in usable if all(g(r) for g in others))
    m3[name] = (oaat, loo)
    print(f"{name:18s} {oaat:16d} {100*oaat/N:8.3f}%   {loo:16d} {100*loo/N:8.3f}%")

killer = min(m3.items(), key=lambda kv: kv[1][0])[0]
print(f"  single largest killer (lowest one-at-a-time survival): {killer}")

# ---- M2 : boundary proximity on elong -----------------------------------
print("\n--- M2 : boundary proximity on elong ---")
bins = {}
lo = 1.0
edges = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
for i in range(len(edges) - 1):
    a, b = edges[i], edges[i + 1]
    # top bin is CLOSED at 1.6: elong is stored float32, so the pipeline's own
    # 1.6 promotes to 1.600000023841858 > 1.6 in float64 and would fall out of
    # every bin. Verified on 2 rows of 2018-06-01. See PASS4_RESULTS.md §0a.
    c = (sum(1 for r in usable if a <= r[0] < b) if b < edges[-1]
         else sum(1 for r in usable if a <= r[0] <= b + 1e-6))
    bins[(a, b)] = c
    print(f"  elong [{a:.1f}, {b:.1f}) : n = {c:8d}  ({100*c/N:6.3f}%)")
below1 = sum(1 for r in usable if r[0] < 1.0)
atmax = sum(1 for r in usable if r[0] == 1.6)
print(f"  elong < 1.0 (should be 0 by definition) : {below1}")
print(f"  elong exactly 1.6                       : {atmax}")

n_boundary = bins[(1.5, 1.6)]
n_ref = bins[(1.2, 1.3)]
R = n_boundary / n_ref if n_ref else float("nan")
print(f"\n  R = n[1.5,1.6) / n[1.2,1.3) = {n_boundary} / {n_ref} = {R:.4f}")
print(f"  PRE-REGISTERED PREDICTION: R < 0.10  ->  {'HELD' if R < 0.10 else 'REFUTED'}")

# ---- extras that cost nothing -------------------------------------------
print("\n--- context (not pre-registered, reported with n) ---")
rb_ok = [r for r in usable if r[5] is not None]
if rb_ok:
    hi = sum(1 for r in rb_ok if r[5] >= 0.65)
    print(f"  rb >= 0.65 : {hi} / {len(rb_ok)} = {100*hi/len(rb_ok):.3f}%")
neg = sum(1 for r in rows if r[6] in ("f", "0", 0, False))
print(f"  negative-subtraction alerts (isdiffpos f/0) : {neg} / {len(rows)}")

json.dump({
    "n_avro_files": N_files, "n_parse_fail": n_parse_fail, "n_usable": N,
    "programid": {str(k): v for k, v in progs.items()},
    "packaging_violations": viol,
    "M1_joint_survivors": len(survivors), "M1_S": S,
    "M3": {k: {"one_at_a_time": v[0], "leave_one_out": v[1]} for k, v in m3.items()},
    "M2_bins": {f"{a}-{b}": c for (a, b), c in bins.items()},
    "M2_R": R,
}, open("PASS4_RESULTS.json", "w"), indent=2)
print("\nwrote PASS4_RESULTS.json")
