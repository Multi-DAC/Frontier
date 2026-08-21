"""PASS 5 pre-flight: is the tarball's MEMBER ORDER correlated with time-of-night?

This decides whether a PREFIX of a tarball is a fair sample of a night or a
biased slice of it. Run on the one night already on disk (2018-06-01) BEFORE
any pass-5 night is downloaded, so the answer is known before the design is
committed. Nothing here is a pass-5 measurement.
"""
import tarfile, io, json, sys
import fastavro

rows = []
with tarfile.open("data/ztf_public_20180601.tar.gz", "r:gz") as tf:
    for i, m in enumerate(tf):
        if not m.isfile() or not m.name.endswith(".avro"):
            continue
        try:
            rec = next(iter(fastavro.reader(io.BytesIO(tf.extractfile(m).read()))))
            c = rec["candidate"]
            rows.append((len(rows), c.get("jd"), c.get("elong"), c.get("fwhm"),
                         c.get("field"), c.get("rcid")))
        except Exception:
            pass
        if len(rows) % 5000 == 0 and rows:
            print(f"  ...{len(rows)}", file=sys.stderr, flush=True)

import numpy as np
idx = np.array([r[0] for r in rows], float)
jd  = np.array([r[1] for r in rows], float)
el  = np.array([r[2] for r in rows], float)
fw  = np.array([r[3] for r in rows], float)
n = len(rows)
print(f"n = {n}")

from scipy.stats import spearmanr
rho_t, p_t = spearmanr(idx, jd)
print(f"Spearman(member index, jd) = {rho_t:.4f}  p={p_t:.3g}")
print(f"jd span = {jd.max()-jd.min():.4f} d = {(jd.max()-jd.min())*24:.2f} h")

# how much of the night does the first 17,991-equivalent PREFIX cover?
for frac in (0.05, 0.10, 0.25, 0.50):
    k = int(n*frac)
    cov = (jd[:k].max()-jd[:k].min()) / (jd.max()-jd.min())
    print(f"  first {frac:.0%} of members covers {cov:.1%} of the night's jd span")

# does the prefix have a different elong/fwhm distribution from the whole?
for frac in (0.10, 0.25, 0.50):
    k = int(n*frac)
    print(f"  first {frac:.0%}: mean elong {el[:k].mean():.4f} (all {el.mean():.4f}) | "
          f"mean fwhm {fw[:k].mean():.4f} (all {fw.mean():.4f})")

fields_all = len(set(r[4] for r in rows))
fields_10  = len(set(r[4] for r in rows[:int(n*0.10)]))
print(f"distinct fields: whole night {fields_all}, first 10% {fields_10}")

json.dump({"n": n, "spearman_idx_jd": rho_t, "p": p_t,
           "jd_span_hours": (jd.max()-jd.min())*24,
           "prefix_coverage": {str(f): float((jd[:int(n*f)].max()-jd[:int(n*f)].min())/(jd.max()-jd.min())) for f in (0.05,0.10,0.25,0.50)},
           "fields_all": fields_all, "fields_first10pct": fields_10},
          open("PASS5_ORDER_PROBE.json","w"), indent=2)
print("wrote PASS5_ORDER_PROBE.json")
