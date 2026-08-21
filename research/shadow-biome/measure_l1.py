"""L1 MEASUREMENT — T1-T4 over the 56 pinned scans.

Definitions are frozen in L1_OPERATIONALIZATION.md, committed BEFORE this file was written.
This script may not introduce a statistic that file does not name.

Stage 1 (fetch+grid) caches one .npz per scan under data/nexrad/ (gitignored) so stage 2 can be
re-run without re-downloading. Byte counts are checked against L1_SAMPLE.json on every fetch.
"""
import io, json, os, sys, time, datetime as dt
import numpy as np, requests
from metpy.io import Level2File
from scipy.stats import spearmanr

S3 = "https://unidata-nexrad-level2.s3.amazonaws.com/"
CACHE = os.path.join("data", "nexrad")
NEAR_KM = 50.0
RANGE_CAP_KM = 460.0
NAZ = 360                       # 1.0 deg azimuth bins
MIN_SUPPORT = 12                # >= 12 of 24 primary scans finite for a baseline cell
EL_TOL = 0.15                   # T2 elevation match, deg


def grab(sweep, name):
    b = name.encode().ljust(3)[:3]
    h0 = sweep[0][4][b][0]
    A = np.full((len(sweep), h0.num_gates), np.nan, dtype=np.float32)
    for i, ray in enumerate(sweep):
        d = ray[4][b][1]
        A[i, :len(d)] = d
    return A, h0


def gridify(raw):
    """-> dict with the 360 x Ngates CFP lattice for the FIRST CFP-bearing sweep."""
    f = Level2File(io.BytesIO(raw))
    idx = None
    for i, sw in enumerate(f.sweeps):
        if b"CFP" in sw[0][4]:
            idx = i
            break
    if idx is None:
        return {"has_cfp": False}
    sw = f.sweeps[idx]
    C, ch = grab(sw, "CFP")
    az = np.array([r[0].az_angle for r in sw], dtype=np.float64) % 360.0
    rng = (ch.first_gate + np.arange(ch.num_gates) * ch.gate_width)   # km
    keep = rng <= RANGE_CAP_KM
    C, rng = C[:, keep], rng[keep]

    G = np.full((NAZ, C.shape[1]), np.nan, dtype=np.float32)
    bins = np.floor(az).astype(int) % NAZ
    for k in range(NAZ):
        m = bins == k
        if not m.any():
            continue
        blk = C[m]
        with np.errstate(invalid="ignore"):
            cnt = np.isfinite(blk).sum(0)
            s = np.nansum(np.where(np.isfinite(blk), blk, 0.0), 0)
        G[k] = np.where(cnt > 0, s / np.maximum(cnt, 1), np.nan)
    return {"has_cfp": True, "sweep_index": idx, "grid": G,
            "el_deg": round(float(sw[0][0].el_angle), 3),
            "first_gate": float(ch.first_gate), "gate_width": float(ch.gate_width),
            "n_gates": int(C.shape[1]), "range_km": rng.astype(np.float32),
            "n_rays": int(C.shape[0]), "az_bins_filled": int(np.isfinite(G).any(1).sum()),
            "n_distinct": int(len(np.unique(G[np.isfinite(G)]))),
            "n_distinct_raw": int(len(np.unique(C[np.isfinite(C)]))),
            "finite_cell_pct": round(float(100 * np.isfinite(G).mean()), 3)}


def fetch(sc):
    os.makedirs(CACHE, exist_ok=True)
    tag = sc["key"].replace("/", "_") + ".npz"
    p = os.path.join(CACHE, tag)
    if os.path.exists(p):
        z = np.load(p, allow_pickle=True)
        return json.loads(str(z["meta"])), z["grid"], z["range_km"]
    raw = requests.get(S3 + sc["key"], timeout=600).content
    ok = len(raw) == sc["size_bytes"]
    g = gridify(raw)
    meta = {k: v for k, v in g.items() if k not in ("grid", "range_km")}
    meta.update({"key": sc["key"], "bytes_fetched": len(raw),
                 "bytes_listed": sc["size_bytes"], "byte_count_matches": ok})
    if not g["has_cfp"]:
        np.savez_compressed(p, meta=json.dumps(meta),
                            grid=np.zeros((0, 0), np.float32), range_km=np.zeros(0, np.float32))
        return meta, np.zeros((0, 0), np.float32), np.zeros(0, np.float32)
    np.savez_compressed(p, meta=json.dumps(meta), grid=g["grid"], range_km=g["range_km"])
    return meta, g["grid"], g["range_km"]


def main():
    sample = json.load(open("L1_SAMPLE.json", encoding="utf-8"))
    scans = sample["scans"]
    metas, grids, ranges = [], [], []
    t0 = time.time()
    for i, sc in enumerate(scans):
        m, G, R = fetch(sc)
        m.update({"radar": sc["radar"], "date": sc["date"], "anchor": sc["anchor"],
                  "role": sc["role"], "season": sc["season"], "start_utc": sc["start_utc"]})
        metas.append(m); grids.append(G); ranges.append(R)
        print("[%2d/%d] %-40s cfp=%s el=%s gates=%s %.0fs"
              % (i + 1, len(scans), sc["key"].split("/")[-1], m.get("has_cfp"),
                 m.get("el_deg"), m.get("n_gates"), time.time() - t0), flush=True)

    out = {"written_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "governed_by": "L1_OPERATIONALIZATION.md (committed 936e6e3, before this ran)",
           "n_scans": len(scans), "scans": metas}

    bad_bytes = [m["key"] for m in metas if not m.get("byte_count_matches", True)]
    out["byte_count_mismatches"] = bad_bytes

    # ---------------- T1 -------------------------------------------------------------------------
    ok1 = [m for m in metas if m.get("has_cfp") and m.get("n_distinct", 0) > 1]
    out["T1"] = {"n_total": len(metas), "n_pass": len(ok1),
                 "pct": round(100 * len(ok1) / len(metas), 2),
                 "threshold_pct": 90.0, "holds": 100 * len(ok1) / len(metas) >= 90.0,
                 "failures": [{"key": m["key"], "has_cfp": m.get("has_cfp"),
                               "n_distinct": m.get("n_distinct")} for m in metas if m not in ok1]}

    # ---------------- baseline per radar (primary scans only) ------------------------------------
    base, geom = {}, {}
    for radar in sample["radars"]:
        sel = [i for i, m in enumerate(metas)
               if m["radar"] == radar and m["role"] == "primary" and m.get("has_cfp")]
        gw = {(round(metas[i]["first_gate"], 4), round(metas[i]["gate_width"], 4)) for i in sel}
        ng = min(metas[i]["n_gates"] for i in sel)
        geom[radar] = {"n_primary_used": len(sel), "gate_geometries": [list(x) for x in gw],
                       "common_n_gates": ng,
                       "elevations": sorted({metas[i]["el_deg"] for i in sel})}
        stack = np.stack([grids[i][:, :ng] for i in sel])          # (n, 360, ng)
        cnt = np.isfinite(stack).sum(0)
        with np.errstate(all="ignore"):
            med = np.nanmedian(stack, axis=0)
        med = np.where(cnt >= MIN_SUPPORT, med, np.nan).astype(np.float32)
        base[radar] = med
        geom[radar]["baseline_cells"] = int(np.isfinite(med).sum())
        geom[radar]["baseline_cell_pct"] = round(float(100 * np.isfinite(med).mean()), 2)
        geom[radar]["range_km"] = ranges[sel[0]][:ng].tolist()
    out["baseline"] = {k: {kk: vv for kk, vv in v.items() if kk != "range_km"}
                       for k, v in geom.items()}

    # ---------------- residuals per scan ---------------------------------------------------------
    def resid(i):
        radar = metas[i]["radar"]
        ng = geom[radar]["common_n_gates"]
        G, B = grids[i][:, :ng], base[radar]
        rng = np.asarray(geom[radar]["range_km"], dtype=np.float32)
        near = rng < NEAR_KM
        both = np.isfinite(G) & np.isfinite(B)
        d = np.where(both, G - B, np.nan)
        newc = np.isfinite(G) & ~np.isfinite(B)
        f = lambda a, sel: (float(np.nanmean(a[:, sel])) if np.isfinite(a[:, sel]).any() else None)
        r = {"key": metas[i]["key"], "radar": radar, "anchor": metas[i]["anchor"],
             "date": metas[i]["date"], "season": metas[i]["season"], "role": metas[i]["role"],
             "n_cells_both": int(both.sum()),
             "R_mag": f(np.abs(d), slice(None)),
             "R_mag_near": f(np.abs(d), near), "R_mag_far": f(np.abs(d), ~near),
             "R_pos": f(np.maximum(d, 0), slice(None)),
             "R_pos_near": f(np.maximum(d, 0), near), "R_pos_far": f(np.maximum(d, 0), ~near),
             "R_new": (float(newc.sum() / max(np.isfinite(G).sum(), 1))),
             "R_new_near": float(newc[:, near].sum() / max(np.isfinite(G[:, near]).sum(), 1)),
             "R_new_far": float(newc[:, ~near].sum() / max(np.isfinite(G[:, ~near]).sum(), 1))}
        return r

    res = [resid(i) for i in range(len(metas)) if metas[i].get("has_cfp")]
    out["residuals"] = res
    prim = [r for r in res if r["role"] == "primary"]

    med = lambda xs: (float(np.median(xs)) if len(xs) else None)
    pick = lambda rows, k: [r[k] for r in rows if r[k] is not None]

    # ---------------- T3 -------------------------------------------------------------------------
    n_, f_ = med(pick(prim, "R_mag_near")), med(pick(prim, "R_mag_far"))
    out["T3"] = {"median_R_mag_near_db": n_, "median_R_mag_far_db": f_,
                 "ratio": (n_ / f_ if f_ else None), "holds": bool(n_ is not None and f_ is not None and n_ > f_),
                 "secondary": {
                     "R_pos_near": med(pick(prim, "R_pos_near")), "R_pos_far": med(pick(prim, "R_pos_far")),
                     "R_new_near": med(pick(prim, "R_new_near")), "R_new_far": med(pick(prim, "R_new_far"))}}

    # ---------------- T4 -------------------------------------------------------------------------
    t4 = {}
    for radar in list(sample["radars"]) + ["POOLED"]:
        rows = prim if radar == "POOLED" else [r for r in prim if r["radar"] == radar]
        dd = [r for r in rows if r["anchor"] in ("sunrise", "sunset")]
        nn = [r for r in rows if r["anchor"] == "solar_noon"]
        a, b = med(pick(dd, "R_mag")), med(pick(nn, "R_mag"))
        t4[radar] = {"n_dawn_dusk": len(dd), "n_noon": len(nn),
                     "median_R_mag_dawn_dusk_db": a, "median_R_mag_noon_db": b,
                     "delta_db": (a - b if a is not None and b is not None else None),
                     "holds": bool(a is not None and b is not None and a > b),
                     "by_anchor": {k: med(pick([r for r in rows if r["anchor"] == k], "R_mag"))
                                   for k in ("sunrise", "solar_noon", "sunset")},
                     "R_new_by_anchor": {k: med(pick([r for r in rows if r["anchor"] == k], "R_new"))
                                         for k in ("sunrise", "solar_noon", "sunset")}}
    t4["holds"] = bool(all(t4[r]["holds"] for r in sample["radars"]))
    t4["rule"] = "BOTH radars must hold (L1_OPERATIONALIZATION.md §4, tightened against the premise)"
    out["T4"] = t4

    # ---------------- T2 -------------------------------------------------------------------------
    pairs = []
    for i, m in enumerate(metas):
        if m["role"] != "t2_partner" or not m.get("has_cfp"):
            continue
        cands = [j for j, p in enumerate(metas)
                 if p["role"] == "primary" and p["radar"] == m["radar"]
                 and p["anchor"] == "solar_noon" and p["season"] == m["season"] and p.get("has_cfp")]
        if not cands:
            pairs.append({"partner": m["key"], "status": "NO PRIMARY MATCH"}); continue
        j = min(cands, key=lambda j: metas[j]["start_utc"])
        A, B = metas[j], m
        d_el = abs(A["el_deg"] - B["el_deg"])
        geom_ok = (round(A["first_gate"], 4), round(A["gate_width"], 4)) == \
                  (round(B["first_gate"], 4), round(B["gate_width"], 4))
        rec = {"radar": m["radar"], "season": m["season"], "primary": A["key"], "partner": B["key"],
               "el_primary": A["el_deg"], "el_partner": B["el_deg"], "d_el_deg": round(d_el, 3),
               "el_match": d_el <= EL_TOL, "gate_geometry_match": geom_ok,
               "days_apart": round((dt.datetime.fromisoformat(B["start_utc"])
                                    - dt.datetime.fromisoformat(A["start_utc"])).total_seconds() / 86400, 2)}
        if not (rec["el_match"] and geom_ok):
            rec["status"] = "DROPPED — " + ("elevation mismatch" if not rec["el_match"]
                                            else "gate geometry mismatch")
            pairs.append(rec); continue
        ng = min(A["n_gates"], B["n_gates"])
        Ga, Gb = grids[j][:, :ng], grids[i][:, :ng]
        both = np.isfinite(Ga) & np.isfinite(Gb)
        sel = both & ((Ga > 0) | (Gb > 0))
        rho, p = spearmanr(Ga[sel], Gb[sel])
        # secondary: fill non-finite with 0 over the union of >0 cells
        Fa, Fb = np.nan_to_num(Ga, nan=0.0), np.nan_to_num(Gb, nan=0.0)
        u = (Fa > 0) | (Fb > 0)
        rho2, _ = spearmanr(Fa[u], Fb[u])
        rec.update({"status": "OK", "n_cells": int(sel.sum()), "rho_primary": float(rho),
                    "p": float(p), "n_cells_union_filled": int(u.sum()),
                    "rho_secondary_zerofill": float(rho2)})
        pairs.append(rec)
    good = [x["rho_primary"] for x in pairs if x.get("status") == "OK"]
    out["T2"] = {"pairs": pairs, "n_ok": len(good), "n_dropped": len(pairs) - len(good),
                 "median_rho": med(good), "threshold": 0.70,
                 "holds": bool(len(good) and med(good) >= 0.70),
                 "median_rho_secondary": med([x["rho_secondary_zerofill"]
                                              for x in pairs if x.get("status") == "OK"])}

    out["verdicts"] = {k: out[k]["holds"] for k in ("T1", "T2", "T3", "T4")}
    with open("L1_RESULTS.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({"T1": out["T1"]["pct"], "T2": out["T2"]["median_rho"],
                      "T3": [out["T3"]["median_R_mag_near_db"], out["T3"]["median_R_mag_far_db"]],
                      "T4": {r: out["T4"][r]["delta_db"] for r in sample["radars"]},
                      "verdicts": out["verdicts"]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
