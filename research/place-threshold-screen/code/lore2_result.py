"""NATIVE / HISTORICAL LORE EXPERIMENT (v2) -- scoring and readout.

Tiers below were assigned under the rubric frozen in lore2_design.py BEFORE any
lookup. Protocol amendment, declared before any winner/decoy data existed: 3 queries
per site, not 4 (query (a), territory identification, proved redundant with (b) in the
positive-control run). Applied identically to all 20 sites.

COVERAGE, stated rather than implied: the two NATIVE queries were run for all 20 sites
and both controls. The third (settler-history) query was NOT run for any site. So H3 is
UNTESTED -- uniformly, for everyone -- and the HT column below is empty by omission,
not by finding. It is not reported as a null.
"""
import json
from math import comb

# tier, one-line justification. NT scale: NT3=3 NT2=2 NT1=1 NT0=0, NX=excluded.
ROWS = [
 (1, "Madison fault", 1, "Shoshone-Bannock ancestral, 'long revered as sacred' -- regional, no locus on the range",
     "Big Chino fault", 1, "Yavapai territory, Big Chino Wash villages, 'spiritual ties to plateaus and washes' -- regional"),
 (2, "Round Valley fault", 1, "Payahuunadu/Nuumu; Volcanic Tableland petroglyphs 'fragile and sacred' but across the valley, not the fault",
     "Thompson Valley fault", 3, "'Big Medicine' hot springs -- NAMED power/healing place, centuries of ceremonial use, CSKT + Montana Historic Landscapes"),
 (3, "Little Valley fault", 3, "Washoe Da ow aga / Cave Rock Water Babies -- named spirit-beings, shaman practice, folklore collections + USFS tribal history",
     "Bear River Range faults", 2, "Old Main Hill / Logan Temple hill named sacred Shoshone loci <25km; student-paper attestation"),
 (4, "Helena valley fault", 2, "Gates of the Mountains ~16km: 50 pictograph sites, Blackfeet/Salish/Kootenai, ceremonial; first-pass sources part listicle",
     "Bull Mountain western border fault", 0, "Boulder hot springs known to Native people (use, not anomaly). Sacred-mountain hit was Sweet Grass Hills, a search conflation"),
 (5, "Red Rock fault", 0, "Travel corridor + hunting grounds; 'Red Rock' from ochre paint beds. Nothing anomaly-shaped",
     "Lida faults", 0, "Shoshone/N. Paiute camp and gathering point at Lida Valley. Nothing anomaly-shaped"),
 (6, "Sand Springs Range fault", 3, "Sand Mountain sacred to Fallon Paiute-Shoshone; Spirit Cave (mummy repatriated 2016), Grimes Point. BLM + Federal Register + congressional",
     "Lone Pine fault", 1, "Salmon corridor ceded lands, pictographs/burials/'other sacred sites' -- FWS source but no locus near Clayton"),
 (7, "Mosquito fault", 0, "Ute/Nuche ancestral hunting ground 8,000 yrs. Nothing anomaly-shaped returned",
     "unnamed faults west of Hungry Valley", 1, "N. Paiute spirit-beings (Wolf/Coyote/water babies) regional; no locus at Lemmon/Hungry Valley"),
 (8, "Sandia fault", 3, "Sandia Mtns sacred to Sandia Pueblo, Tiwa 'Bien Mur', active USFS sacred-sites claim. Tribal + newspaper",
     "Picuris-Pecos fault", 3, "Pecos Pueblo kivas as communion with underworld spirits + 'The Drowning of Pecos' in a pre-1995 printed folk-story collection; NPS"),
 (9, "Bear River fault zone", 0, "Shoshone encamped on Yellow Creek 1872 (historical). Bear River sacredness attaches to Boa Ogoi ~80km away",
     "Sweetwater fault", 1, "Washoe water babies (me-tsung) across territory; locus is Cave Rock ~40km, not Virginia City"),
 (10, "Teton fault", 2, "Teewinot; vision-quest stone structures in the upper Grand Teton; 'sacred peaks', creation stories. Mostly web-secondary first pass",
     "unnamed fault near Ovando", 0, "Cokalahishkit buffalo road, Semte'use presence, Camp Paxson stewardship. Nothing anomaly-shaped"),
]

CONTROLS = {
 "Sandia fault (control+)": (3, "POSITIVE CONTROL -- recovered on the first pass. Protocol works."),
 "Hubbell Spring fault (control-)": (None, "not scored this pass"),
}


def sign_test(w, d):
    nz = [(a, b) for a, b in zip(w, d) if a != b]
    k = sum(1 for a, b in nz if a > b)
    n = len(nz)
    if n == 0:
        return {"non_tied": 0, "favour_winner": 0, "p_two_sided": 1.0}
    p = sum(comb(n, i) for i in range(n + 1) if abs(i - n / 2) >= abs(k - n / 2)) / 2 ** n
    return {"non_tied": n, "favour_winner": k, "p_two_sided": round(min(1.0, p), 4)}


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def main():
    W = [r[2] for r in ROWS]
    D = [r[5] for r in ROWS]
    wm, dm = sum(W) / len(W), sum(D) / len(D)

    # headline: ratio of sites with ANY anomaly-shaped narrative, over sites where
    # N_ANY held. N_ANY held at all 20 -- which is itself the base-rate finding.
    w_anom = sum(1 for x in W if x >= 1)
    d_anom = sum(1 for x in D if x >= 1)

    # Sandia is both positive control and winner #8; report winners without it too.
    W_ns = [r[2] for r in ROWS if r[1] != "Sandia fault"]
    D_ns = [r[5] for r in ROWS if r[1] != "Sandia fault"]

    out = {
        "verdict": None,
        "winner_mean_NT": round(wm, 2), "decoy_mean_NT": round(dm, 2),
        "separation": round(wm - dm, 2), "required": 1.0,
        "sign_test": sign_test(W, D),
        "N_ANY_satisfied": "20/20 -- the near-unity base rate the design predicted",
        "anomaly_shaped_ratio": {"winners": f"{w_anom}/10", "decoys": f"{d_anom}/10"},
        "excluding_sandia_which_is_also_the_positive_control": {
            "winner_mean": round(sum(W_ns) / len(W_ns), 2),
            "decoy_mean": round(sum(D_ns) / len(D_ns), 2),
            "separation": round(sum(W_ns) / len(W_ns) - sum(D_ns) / len(D_ns), 2)},
        "positive_control": CONTROLS["Sandia fault (control+)"][1],
        "H3_settler_history": "UNTESTED -- third query not run for any site; absent by omission",
        "rows": [{"rank": r[0], "winner": r[1], "winner_NT": r[2], "winner_note": r[3],
                  "decoy": r[4], "decoy_NT": r[5], "decoy_note": r[6]} for r in ROWS],
    }
    out["verdict"] = ("SUPPORTED" if (wm - dm) >= 1.0 else "NOT SUPPORTED")

    # --- confound covariates, and the pre-declared kill rule -------------------
    try:
        cov = json.load(open('lore2_covariates.json'))
        by = {(s['role'], s['fault']): s for s in cov['sites']}
        dr, dt, dn = [], [], []
        for r in ROWS:
            w = by.get(('winner', r[1])); d = by.get(('decoy', r[4]))
            if not w or not d:
                continue
            if w['relief'].get('relief_m') and d['relief'].get('relief_m'):
                dr.append(w['relief']['relief_m'] - d['relief']['relief_m'])
            if w['tribal'].get('km') is not None and d['tribal'].get('km') is not None:
                dt.append(w['tribal']['km'] - d['tribal']['km'])
            if w['nps'].get('km') is not None and d['nps'].get('km') is not None:
                dn.append(w['nps']['km'] - d['nps']['km'])
        fired = []
        if dr and median(dr) > 300:
            fired.append(f"relief median +{median(dr):.0f} m > 300 m")
        for nm, dd in (("relief", dr), ("tribal_km", dt), ("nps_km", dn)):
            if dd:
                st = sign_test([1] * len(dd), [0 if x > 0 else 2 for x in dd])
                if st["p_two_sided"] <= 0.125 and st["favour_winner"] > st["non_tied"] / 2:
                    fired.append(f"{nm} sign test p={st['p_two_sided']}")
        out["covariates"] = {
            "n_pairs_measured": len(dr),
            "relief_delta_median_m": round(median(dr), 1) if dr else None,
            "relief_deltas_m": dr,
            "tribal_km_delta_median": round(median(dt), 1) if dt else None,
            "nps_km_delta_median": round(median(dn), 1) if dn else None,
            "kill_rule_fired": fired or "NO -- covariates balanced; the null stands on its own",
        }
    except FileNotFoundError:
        out["covariates"] = "lore2_covariates.json not present at scoring time"

    json.dump(out, open('lore2_result.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))


if __name__ == '__main__':
    main()
