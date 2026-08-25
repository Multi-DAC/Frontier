"""Score PREREG-DMTN-PRIMARY.md Q1-Q6 against the fetched primaries. Recompute, don't transcribe.

`feedback_recomputing_beats_rereading`. Every ratio below is computed from the two integers
either side of it, in this file, so a transposed label shows up as a wrong number.

Inputs already on disk: _src_dmtn006.txt, _src_dmtn007.txt (fetch_dmtn.py),
_src_rubin_ldm612.txt (PASS 1, Day 201), PASS9_RESULTS.json, RETENTION_SURVEY.md.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- DMTN-006 Table 1
# Transcribed from _src_dmtn006.txt "Table 1 Source counts for visit 197367, and mean
# of all visits", units = counts per square degree. Two columns.
TABLE1 = {
    #                          visit 197367,  all visits (mean)
    "raw_positive":            (3_572,        19_475),
    "raw_negative":            (4_763,        23_018),
    "dipoles_not_incl_below":  (1_124,         1_609),
    "pos_after_5sig":          (  480,         1_022),
    "neg_after_5sig":          (  555,           600),
    "pos_excl_variables":      (  237,           344),
}

# ---------------------------------------------------------------- our ZTF number
# RETENTION_SURVEY.md, and it is ZTF's Figure 9.1 caption, not ours (pass 10 finding).
ZTF_RAW, ZTF_PACKAGED = 643_860, 228_287


def pct(num: int, den: int) -> float:
    return 100.0 * num / den


def main() -> None:
    out: dict = {"prereg": "PREREG-DMTN-PRIMARY.md @ f253aa6"}

    # ---- Q2/Q3: the discard cascade, both columns, computed not copied ----------
    cascade = {}
    for col, label in ((0, "visit_197367"), (1, "all_visits_mean")):
        raw = TABLE1["raw_positive"][col] + TABLE1["raw_negative"][col]
        kept = TABLE1["pos_after_5sig"][col] + TABLE1["neg_after_5sig"][col]
        cascade[label] = {
            "raw_per_sq_deg": raw,
            "kept_after_5sigma_per_sq_deg": kept,
            "discarded_per_sq_deg": raw - kept,
            "discarded_pct": round(pct(raw - kept, raw), 2),
            "reduction_factor": round(raw / kept, 2),
        }
    ours = {
        "raw_alerts": ZTF_RAW,
        "packaged": ZTF_PACKAGED,
        "discarded": ZTF_RAW - ZTF_PACKAGED,
        "discarded_pct": round(pct(ZTF_RAW - ZTF_PACKAGED, ZTF_RAW), 2),
        "reduction_factor": round(ZTF_RAW / ZTF_PACKAGED, 2),
    }
    out["Q2_Q3_discard_cascade"] = {
        "rubin_dmtn006_decam": cascade,
        "ours_ztf_fig9.1": ours,
        "unit_note": "Rubin's rows are per-sq-deg densities; ours are absolute alert "
                     "counts. The RATIO is unit-free, which is why the comparison is "
                     "possible at all. The two filters are NOT the same operation.",
    }

    # ---- the dipole share: DELIBERATELY NOT COMPUTED ---------------------------
    # Table 1 labels the dipole row "(not included below)". That fixes dipoles as
    # excluded from the rows BENEATH it. It does NOT say whether they are inside the
    # raw pos/neg rows ABOVE it. A share needs a denominator that is known, not
    # assumed. feedback_self_generated_denominator / feedback_bucket_derived_by_subtraction.
    p9 = json.loads((HERE / "PASS9_RESULTS.json").read_text(encoding="utf-8"))
    n_union = p9["P0"]["n_union"]
    n_pairs = p9["P0"]["n_pairs"]
    out["Q6_dipoles"] = {
        "rubin_dipole_density_per_sq_deg": {
            "visit_197367": TABLE1["dipoles_not_incl_below"][0],
            "all_visits_mean": TABLE1["dipoles_not_incl_below"][1],
        },
        "ours_pass9_block_S": {
            "n_union": n_union,
            "n_mutual_opposite_pairs": n_pairs,
            "sources_in_pairs": n_pairs * 2,
            "share_of_union_pct": round(pct(n_pairs * 2, n_union), 2),
        },
        "SHARE_COMPARISON_REFUSED": (
            "Table 1's dipole row is annotated '(not included below)', which fixes its "
            "relation to the rows BELOW and leaves its relation to the raw rows ABOVE "
            "unstated. A Rubin dipole SHARE is therefore not derivable from the "
            "published table, so ours cannot be placed against it. Recorded as "
            "not-computable rather than estimated."
        ),
    }

    # ---- Q4: where the 90/95 requirement actually lives -------------------------
    d6 = (HERE / "_src_dmtn006.txt").read_text(encoding="utf-8")
    ldm = (HERE / "_src_rubin_ldm612.txt").read_text(encoding="utf-8", errors="replace")
    q4 = {
        "in_dmtn006": {
            "hits_90_or_95_pct": len(re.findall(r"\b9[05]\s*%", d6)),
            "hits_purity": len(re.findall(r"purit", d6, re.I)),
            "hits_completeness_word": len(re.findall(r"completeness", d6, re.I)),
            "only_90_in_document": re.findall(r".{60}\b90\b.{60}", d6)[:3],
        },
        "in_ldm612_on_disk_since_day201": {
            "hits_90_pct": len(re.findall(r"90\s*%", ldm)),
            "hits_purity": len(re.findall(r"purit", ldm, re.I)),
        },
        "upstream_authority_cited_BY_ldm612": sorted(
            set(re.findall(r"LSE-\d+", ldm))
        ),
    }
    # LDM-612 cites TWO different authorities for the SAME number. Count each.
    q4["authority_split"] = {
        "cited_as_LSE-30": len(re.findall(r"purity at 6\s*.{0,3}\s*\[?LSE-30", ldm)),
        "cited_as_LSE-61": len(re.findall(r"SNR = 6\s*LSE-61", ldm)),
    }
    out["Q4_attribution"] = q4

    # ---- Q5: the 100x claim ----------------------------------------------------
    m = re.search(r".{300}raw rate we measure is\s*(\d+)\s*times this.{200}", d6, re.S)
    out["Q5_hundredfold"] = {
        "verbatim_found": bool(m),
        "multiplier": int(m.group(1)) if m else None,
        "context": re.sub(r"\s+", " ", m.group(0)).strip() if m else None,
        "baseline_stated": "33 detections per square degree expected from Gaussian "
                           "noise at 5 sigma (sigma_g=1.8 px, 2k x 4k sensor)",
        "raw_not_post_classifier": True,
        "dataset": "DECam / CTIO 4m, Program 2013A-724, 60s exposures, 2013",
    }

    # ---- Rubin's own admission of ignorance, which the write-up must carry ------
    adm = re.search(r".{160}currently unknown fraction of artifacts.{160}", ldm, re.S)
    out["rubin_states_its_own_rate_is_UNKNOWN"] = (
        re.sub(r"\s+", " ", adm.group(0)).strip() if adm else None
    )

    (HERE / "RUBIN_COMPARATOR.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8"
    )

    print("=== Q2/Q3 DISCARD CASCADE (unit-free ratios) ===")
    for k, v in cascade.items():
        print(f"  Rubin {k:16s} {v['raw_per_sq_deg']:>7,} -> {v['kept_after_5sigma_per_sq_deg']:>6,}"
              f"  discarded {v['discarded_pct']:.2f}%  ({v['reduction_factor']}x)")
    print(f"  OURS  ZTF fig 9.1    {ours['raw_alerts']:>7,} -> {ours['packaged']:>6,}"
          f"  discarded {ours['discarded_pct']:.2f}%  ({ours['reduction_factor']}x)")
    print()
    print("=== Q4 ATTRIBUTION ===")
    print(f"  DMTN-006: '90%|95%' x{q4['in_dmtn006']['hits_90_or_95_pct']} · "
          f"'purity' x{q4['in_dmtn006']['hits_purity']} · "
          f"'completeness' x{q4['in_dmtn006']['hits_completeness_word']}")
    print(f"  LDM-612 (on disk since D201): '90%' x"
          f"{q4['in_ldm612_on_disk_since_day201']['hits_90_pct']} · 'purity' x"
          f"{q4['in_ldm612_on_disk_since_day201']['hits_purity']}")
    print(f"  authority split: {q4['authority_split']}")
    print()
    print("=== Q5 ===")
    print(f"  multiplier found: {out['Q5_hundredfold']['multiplier']}x over "
          f"{out['Q5_hundredfold']['baseline_stated']}")
    print()
    print("=== Q6 ===")
    print(f"  ours: {n_pairs:,} pairs = {n_pairs*2:,} of {n_union:,} union sources "
          f"({out['Q6_dipoles']['ours_pass9_block_S']['share_of_union_pct']}%)")
    print("  Rubin share: NOT COMPUTABLE from the published table (see JSON).")
    print("\nwrote RUBIN_COMPARATOR.json")


if __name__ == "__main__":
    main()
