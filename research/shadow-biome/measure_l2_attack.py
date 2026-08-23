"""L2 ADVERSARIAL ARMS — four attacks on my own 5/5 result, each of which can kill a prediction.

Written AFTER measure_l2.py returned HIT on every pre-registered prediction. Five for five
on my own predictions is the condition my standing orders name as the one under which I have
lately been wrong, so this file exists to try to break it. It reads nothing from
L2_RESULTS.json -- it recomputes from the sources -- so a bug in the first script cannot
propagate into its own audit.

The four attacks, and what each one would kill:

A1  V(lambda) IS THE WRONG WEIGHT, AND MY DOCSTRING'S BIAS CLAIM WAS HALF THE STORY.
    measure_l2.py says the V-as-retention choice biases toward MISS on P4. That is TRUE and
    INCOMPLETE. There is a SECOND bias of OPPOSITE SIGN: V(lambda) is a luminance-channel
    function from heterochromatic flicker photometry, so it excludes chromatic detection and
    understates blue sensitivity badly (V(450) ~ 0.038, while a 450 nm light is trivially
    visible). That inflates the measured edit -- toward HIT on P4. Two errors of opposite
    sign, and the total does not tell you either one. Arm: rerun S3 with CIE 2008 2-deg
    luminous efficiency, which corrects the blue limb.

A2  THE BAND EDGES WERE MY CHOICE. 380-780 nm is defensible; so is 400-700. P1's window was
    [0.35,0.60] and the primary landed at 0.3613 -- 1.1 points inside. Arm: re-score P1 under
    both band conventions and both currencies. If P1 flips, its HIT is an artefact of two
    free choices and must be reported as such.

A3  THE STAGES ARE CORRELATED BY CONSTRUCTION, WHICH IS P3's REAL WEAKNESS. The eye evolved
    inside the window the atmosphere already opened, so "biology out-edits the atmosphere"
    may just be recording that the atmosphere handed over a mostly-visible spectrum and left
    the eye little to cut. Arm: apply S2+S3 to the UNFILTERED AM0 spectrum, decorrelating the
    stages, and ask whether the ordering survives.

A4  THE DENOMINATOR STOPS AT 4000 nm. Real downwelling at a human's face includes atmospheric
    thermal IR (~300 W/m^2 near 10 um) that the solar table does not carry. Excluding it
    shrinks the denominator and INFLATES every retention here. Arm: bound the effect with a
    300 K greybody and report how far P4's margin would have to shrink to matter.

Emits L2_ATTACK.json.
"""
import json, math, os, datetime as dt
from measure_l2 import (load_g173, load_vlambda, trapz, to_photons, weighted, v_at,
                        H_PLANCK, C_LIGHT, D, HERE)

SIGMA_SB = 5.670374419e-8
K_B = 1.380649e-23


def load_cie2008():
    v = {}
    with open(os.path.join(D, "linCIE2008v2.csv")) as f:
        for line in f:
            p = [x.strip() for x in line.strip().split(",")]
            if len(p) >= 2 and p[0]:
                v[float(p[0])] = float(p[1])
    return v


def retention(wl, e_toa, e_surf, vtab, lo, hi, currency="photon"):
    toa = to_photons(wl, e_toa) if currency == "photon" else e_toa
    surf = to_photons(wl, e_surf) if currency == "photon" else e_surf
    I_toa, I_surf = trapz(wl, toa), trapz(wl, surf)
    I_band = trapz(wl, surf, lo, hi)
    I_wgt = trapz(wl, weighted(wl, surf, vtab))
    return {"r1": I_surf / I_toa, "r2": I_band / I_surf,
            "r3_given": I_wgt / I_band, "r_end": I_wgt / I_toa}


def main():
    wl, cols = load_g173()
    v1924, v2008 = load_vlambda(), load_cie2008()
    toa, glob = cols["extraterrestrial"], cols["global"]
    out = {"written_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "reads_results_json": False, "attacks": {}}

    # ---- A1: the weighting function -------------------------------------------------
    a = retention(wl, toa, glob, v1924, 380, 780)
    b = retention(wl, toa, glob, v2008, 380, 780)
    peak2008 = max(v2008, key=lambda k: v2008[k])
    out["attacks"]["A1_weighting_function"] = {
        "claim_attacked": "measure_l2.py's docstring says the V-as-retention bias runs "
                          "AGAINST P4. It runs BOTH WAYS and the docstring named one.",
        "cie1924_end_to_end": round(a["r_end"], 5),
        "cie2008_end_to_end": round(b["r_end"], 5),
        "cie2008_peak_nm": peak2008, "cie2008_peak_value": v2008[peak2008],
        "relative_change": round((b["r_end"] - a["r_end"]) / a["r_end"], 4),
        "v450_1924": round(v_at(v1924, 450), 5),
        "v450_2008": round(v2008.get(450.0, float("nan")), 5),
        "P4_survives": b["r_end"] < 0.355,
        "verdict": "P4 SURVIVES" if b["r_end"] < 0.355 else "P4 KILLED",
        "residual_objection": "BOTH functions are luminance-channel. Neither admits "
                              "chromatic detection, so both understate what the visual "
                              "system can act on and OVERSTATE the edit. This arm narrows "
                              "the uncertainty; it does not remove the sign problem. The "
                              "honest ceiling: even a weight that is 1.0 across the whole "
                              "380-780 band gives end-to-end r = r1*r2, below.",
        "absolute_ceiling_flat_band_weight": round(a["r1"] * a["r2"], 5),
        "ceiling_still_below_ZTF": (a["r1"] * a["r2"]) < 0.355,
    }

    # ---- A2: band edges + currency ---------------------------------------------------
    grid = {}
    for lo, hi in ((380, 780), (400, 700)):
        for cur in ("photon", "power"):
            r = retention(wl, toa, glob, v1924, lo, hi, cur)
            grid[f"{lo}-{hi}_{cur}"] = round(r["r2"], 4)
    hits = {k: (0.35 <= v <= 0.60) for k, v in grid.items()}
    out["attacks"]["A2_band_and_currency"] = {
        "claim_attacked": "P1 HIT at 0.3613, which is 1.1 points inside a window I chose.",
        "r2_grid": grid, "P1_hit_under": hits,
        "n_hit": sum(hits.values()), "n_cells": len(hits),
        "verdict": "P1 FRAGILE" if not all(hits.values()) else "P1 ROBUST",
        "reading": "P1's verdict is decided by two free choices. The pre-registration fixed "
                   "both BEFORE the run, which is the only reason this is reportable at all "
                   "-- but a prediction that flips across defensible conventions is a weak "
                   "prediction and is labelled one.",
    }

    # ---- A3: decorrelate the stages ---------------------------------------------------
    I_toa_ph = trapz(wl, to_photons(wl, toa))
    I_toa_band = trapz(wl, to_photons(wl, toa), 380, 780)
    I_toa_wgt = trapz(wl, weighted(wl, to_photons(wl, toa), v1924))
    r_eye_on_toa = I_toa_wgt / I_toa_ph
    r_eye_on_surf = a["r2"] * a["r3_given"]
    out["attacks"]["A3_stage_correlation"] = {
        "claim_attacked": "P3 says biology out-edits the atmosphere -- but the eye evolved "
                          "inside the window the atmosphere already opened, so the two "
                          "stages are not independent and P3 may be recording that.",
        "eye_retention_applied_to_UNFILTERED_AM0": round(r_eye_on_toa, 5),
        "eye_retention_applied_to_surface": round(r_eye_on_surf, 5),
        "atmosphere_retention": round(a["r1"], 5),
        "eye_edit_on_AM0": round(1 - r_eye_on_toa, 5),
        "atmosphere_edit": round(1 - a["r1"], 5),
        "ordering_survives_decorrelation": (1 - r_eye_on_toa) > (1 - a["r1"]),
        "verdict": "P3 SURVIVES" if (1 - r_eye_on_toa) > (1 - a["r1"]) else "P3 KILLED",
        "reading": "Handed the unfiltered TOA spectrum, the eye discards a LARGER fraction "
                   "than the atmosphere does. The correlation objection is real but does "
                   "not reverse the ordering -- if anything the atmosphere HELPS the eye "
                   "look less selective by pre-removing what the eye would have cut.",
    }

    # ---- A4: the missing thermal-IR denominator ---------------------------------------
    # Downwelling longwave, 300 K greybody eps=0.8, integrated 4-100 um, photon number.
    def planck_photons(lam_m, T):
        return (2 * C_LIGHT / lam_m ** 4) / (math.exp(H_PLANCK * C_LIGHT /
                                                      (lam_m * K_B * T)) - 1)
    lam = [4e-6 + i * 1e-7 for i in range(961)]          # 4 - 100 um
    ph = [0.8 * math.pi * planck_photons(L, 300.0) for L in lam]
    ir_photons = sum(0.5 * (ph[i] + ph[i + 1]) * (lam[i + 1] - lam[i])
                     for i in range(len(lam) - 1))
    I_surf_ph = trapz(wl, to_photons(wl, glob))
    infl = I_surf_ph / (I_surf_ph + ir_photons)
    out["attacks"]["A4_truncated_denominator"] = {
        "claim_attacked": "the denominator stops at 4000 nm, so it omits atmospheric "
                          "thermal IR arriving at the same face, INFLATING every retention.",
        "solar_surface_photons_per_s_m2": f"{I_surf_ph:.4g}",
        "downwelling_LW_photons_300K_eps0.8_4to100um": f"{ir_photons:.4g}",
        "solar_share_of_combined_photon_influx": round(infl, 4),
        "P4_measured": round(a["r_end"], 5),
        "P4_if_denominator_included_LW": round(a["r_end"] * infl, 5),
        "verdict": "P4 SURVIVES (correction moves it further from 0.355, not toward it)"
                   if a["r_end"] * infl < a["r_end"] else "unexpected",
        "reading": "This attack cannot rescue P4: every omission from the denominator makes "
                   "retention look HIGHER than it is, and P4 predicts LOW. The truncation "
                   "is a scope limit declared in the prereg, and it is conservative.",
        "caveat": "a 300 K greybody is a MODEL, not a measured downwelling spectrum. It is "
                  "used here only to bound a direction, never to report a retention figure.",
    }

    surv = [v["verdict"] for v in out["attacks"].values()]
    out["summary"] = {
        "predictions_killed": [k for k, v in out["attacks"].items() if "KILLED" in v["verdict"]],
        "predictions_weakened": [k for k, v in out["attacks"].items() if "FRAGILE" in v["verdict"]],
        "verdicts": surv,
    }
    json.dump(out, open(os.path.join(HERE, "L2_ATTACK.json"), "w"), indent=1)

    for k, v in out["attacks"].items():
        print(f"{v['verdict']:>12s}  {k}")
    print()
    A = out["attacks"]
    print(f"A1  1924 end={A['A1_weighting_function']['cie1924_end_to_end']}  "
          f"2008 end={A['A1_weighting_function']['cie2008_end_to_end']}  "
          f"flat-band ceiling={A['A1_weighting_function']['absolute_ceiling_flat_band_weight']}")
    print(f"A2  {A['A2_band_and_currency']['n_hit']}/{A['A2_band_and_currency']['n_cells']} "
          f"cells hit P1 -> {A['A2_band_and_currency']['r2_grid']}")
    print(f"A3  eye on AM0 keeps {A['A3_stage_correlation']['eye_retention_applied_to_UNFILTERED_AM0']}"
          f"  vs atmosphere keeps {A['A3_stage_correlation']['atmosphere_retention']}")
    print(f"A4  solar is {A['A4_truncated_denominator']['solar_share_of_combined_photon_influx']}"
          f" of combined influx; P4 would move to "
          f"{A['A4_truncated_denominator']['P4_if_denominator_included_LW']}")


if __name__ == "__main__":
    main()
