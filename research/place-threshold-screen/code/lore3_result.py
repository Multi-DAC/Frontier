"""H3 -- US/SETTLER HISTORICAL LEG. Scoring and readout.

Tiers assigned under the rubric frozen in lore3_design.py (committed f3a811fb /
9757807d) BEFORE any lookup. One query per site, the frozen string, no thread-chasing
on winners. 20 sites + 2 controls, identical protocol.

COVERAGE, stated rather than implied: all 20 sites scored, no NX/exclusions. Both
controls run. Nothing in this table is absent by omission.

THE UNREGISTERED CONFOUNDER, declared here the moment it was noticed and BEFORE the
verdict is read: the pairs were matched on COUNT of census places within 50 km. They
were never matched on DISTANCE TO THE NEAREST one -- and the HT rubric's 25 km cutoff
is a distance test. Settler record clusters at towns. See confound() below; it is
computed, not waved at, and it runs in the winners' favour.
"""
import json
from math import comb

# (rank, winner, HT, note, decoy, HT, note)
ROWS = [
 (1, "Madison fault", 3, "1959 M7.5 Hebgen Lake quake + Madison Slide, 28 dead, Quake Lake; Hebgen Dam 1914-15 Montana Power. USGS + ASDSO",
     "Big Chino fault", 1, "Big Chino Wash returned as geography + regional Yavapai use; Seligman railroad/Route 66 present but no locus-specific incident"),
 (2, "Round Valley fault", 2, "Round Valley tungsten mine, Inyo Co (Western Mining History). NOTE: first pass mostly returned MENDOCINO Round Valley -- name conflation, massacres NOT credited",
     "Thompson Valley fault", 1, "Lonepine PO 1911, Lower Dry Fork Reservoir 1921 (Reclamation) -- but at 26.0 km, so 25-60 km band. Thompson Valley hits were Tazewell Co, VIRGINIA -- conflation"),
 (3, "Little Valley fault", 3, "Hobart & Marlette sawmill in Little Valley 1873; 1884 V-flume blowdown on an 80-ft trestle, rebuilt in 8 days; Little Valley Placers. Truckee-Donner Historical Society",
     "Bear River Range faults", 3, "Avon founded at forks of East Creek and Little Bear River, local history + USU thesis 'An Environmental History of the Bear River Range 1860-1910'. Boa Ogoi NOT credited -- ~60km"),
 (4, "Helena valley fault", 3, "Last Chance Gulch, July 1864 'Four Georgians', named Oct 1864, territorial capital 1875, $3.5bn in gold, 1937-class fire hazard. Montana Historical Society textbook",
     "Bull Mountain western border fault", 0, "TOTAL CONFLATION: returned Bull Mountains coal field near Roundup (~200 km) and Boulder County COLORADO. Nothing on-target at Boulder MT"),
 (5, "Red Rock fault", 0, "CONFLATION: returned Red Lodge (Carbon Co, ~350 km) and Red Rock Mine in Fergus Co. Nothing on-target at Dell / Red Rock Valley",
     "Lida faults", 2, "Lida: 1867 mining district, town laid out 1872, PO + mill, 1905 Goldfield boom to pop 300, ~$1M produced. Ghost-town aggregators + Wikipedia = web-secondary"),
 (6, "Sand Springs Range fault", 3, "Sand Springs Pony Express Station built 1859-60, abandoned 1861, sand-buried a century, stabilized 1997 (SAH Archipedia, HMdb); PROJECT SHOAL 12 kt underground nuclear test in the range, 26 Oct 1963",
     "Lone Pine fault", 1, "Clayton ID founded 1881 as smelter site, Clayton Silver Mine / Bayhorse district -- but 34.1 km, so 25-60 km band. No 'Lone Pine' locus near Clayton"),
 (7, "Mosquito fault", 3, "Mosquito mining district within the Alma District; Alma's first town meeting 4 Dec 1873; 1879-80 silver; business district destroyed by fire 23 Mar 1937. Colorado Geological Survey + Park County Local History Digital Archive",
     "unnamed faults west of Hungry Valley", 1, "Lemmon Valley: 19th-c cemetery, Evans Canyon miner's trail. No named place-specific incident, no archival attestation"),
 (8, "Sandia fault", 3, "POSITIVE CONTROL. Montezuma silver-boom settlement 1879-80 in Las Huertas Canon, claims registered at Albuquerque county seat; Sandia Man Cave; Turquoise Trail / Tijeras Canyon mine",
     "Picuris-Pecos fault", 3, "Canoncito = Glorieta Unit of Pecos National Historical Park, site of the Confederate Army camp (Glorieta Pass, Mar 1862). NPS, primary"),
 (9, "Bear River fault zone", 3, "Bear River City Riot, 19 Nov 1868 -- vigilante lynching, town torched; Almy coal mines opened 1868. HMdb markers + WyoHistory.org (Wyoming State Historical Society)",
     "Sweetwater fault", 1, "Alder Gulch 1863, Montana's second major gold strike, Conrey Placer Mining Co -- but Alder is 33.9 km, 25-60 km band. 'Sweetwater Mines' hits were WYOMING/South Pass -- conflation"),
 (10, "Teton fault", 2, "~1900 160-acre placer claims filed Jackson Lake to Menor's Ferry (NPS, reaching me via buckrail = secondary); 1889 Teton Wilderness mine; 1886 Deadman's Bar murders at ~29 km",
     "unnamed fault near Ovando", 3, "Seeley Lake: logging 1892, first road 1895, Seely first ranger 1899-1900 Lewis & Clark Forest Reserve (USGS misspelled him onto the map), Big Blackfoot Milling 1906, USFS 50M board-ft sale to Anaconda. Montana History Portal"),
]

CONTROLS = {
 "Sandia fault (control+)": (3, "PASS on the declared condition -- named, place-specific incident <25 km. "
                                "BUT NOT the declared CONTENT: Manzano/Kirtland/Bennewitz never appeared, because "
                                "the frozen query says 'settlement OR mining OR incident' and the Sandia military "
                                "record is MILITARY. Out of reach BY CONSTRUCTION of the query, not by search failure. "
                                "Not amended mid-run; amending a query after seeing its miss is how a null becomes a positive."),
 "Hubbell Spring fault (control-)": (0, "Nothing returned. The instrument CAN return zero -- but Hubbell Spring is an "
                                        "obscure name 3.7 km from metro Albuquerque, so this zero may be name-obscurity "
                                        "rather than absence. Same contamination as the Bull Mountain HT0. Reported, "
                                        "EXCLUDED from the readout as pre-declared."),
}

# nearest census place, km -- from lore_experiment_design.json, matched on COUNT not DISTANCE
NEAREST_KM = {
 "Madison fault": 19.7, "Big Chino fault": 16.3,
 "Round Valley fault": 2.4, "Thompson Valley fault": 26.0,
 "Little Valley fault": 6.1, "Bear River Range faults": 22.3,
 "Helena valley fault": 3.4, "Bull Mountain western border fault": 8.0,
 "Red Rock fault": 7.4, "Lida faults": 37.8,
 "Sand Springs Range fault": 41.1, "Lone Pine fault": 34.1,
 "Mosquito fault": 7.6, "unnamed faults west of Hungry Valley": 13.8,
 "Sandia fault": 2.8, "Picuris-Pecos fault": 3.1,
 "Bear River fault zone": 22.7, "Sweetwater fault": 33.9,
 "Teton fault": 38.6, "unnamed fault near Ovando": 11.5,
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
    s = sorted(xs); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def main():
    W = [r[2] for r in ROWS]
    D = [r[5] for r in ROWS]
    wm, dm = sum(W) / len(W), sum(D) / len(D)
    sep = wm - dm
    verdict = "SUPPORTED" if sep >= 1.0 else "NOT SUPPORTED"

    pairs = json.load(open('lore_experiment_design.json'))['pairs']
    obs = {p[r]['fault']: p[r]['observer']['places_within_50km'] for p in pairs for r in ('winner', 'decoy')}

    # --- PRE-DECLARED kill rule: any pair where winner obs > 1.5x decoy obs -------
    flagged = [r[0] for r in ROWS if obs[r[1]] > 1.5 * max(obs[r[4]], 1e-9)]

    # --- UNREGISTERED confounder, computed: distance to nearest census place ------
    wkm = [NEAREST_KM[r[1]] for r in ROWS]
    dkm = [NEAREST_KM[r[4]] for r in ROWS]
    # post-hoc: restrict to pairs where BOTH members sit inside the rubric's 25 km
    # cutoff, so distance-to-town cannot discriminate. THIS IS POST HOC. It does not
    # replace the primary verdict and is not allowed to launder it.
    both_in = [r for r in ROWS if NEAREST_KM[r[1]] <= 25 and NEAREST_KM[r[4]] <= 25]
    bw = [r[2] for r in both_in]; bd = [r[5] for r in both_in]

    out = {
        "verdict_PRIMARY_prereg": verdict,
        "winner_mean_HT": round(wm, 2), "decoy_mean_HT": round(dm, 2),
        "separation": round(sep, 2), "required": 1.0,
        "sign_test": sign_test(W, D),
        "H_ANY_satisfied": "20/20 -- near-unity base rate, exactly as pre-declared; NOT a finding",
        "place_specific_ratio_HT2plus": {"winners": f"{sum(1 for x in W if x >= 2)}/10",
                                         "decoys": f"{sum(1 for x in D if x >= 2)}/10"},
        "zeroes": {"winners": [r[1] for r in ROWS if r[2] == 0], "decoys": [r[4] for r in ROWS if r[5] == 0]},
        "positive_control": CONTROLS["Sandia fault (control+)"][1],
        "negative_side_control": CONTROLS["Hubbell Spring fault (control-)"][1],
        "prereg_kill_rule": {"flagged_pairs": flagged or "none -- observer counts matched, no-op as predicted",
                             "note": "a no-op check is only a no-op after you run it"},
        "UNREGISTERED_CONFOUND_nearest_town_km": {
            "winner_median_km": median(wkm), "decoy_median_km": median(dkm),
            "winner_km": wkm, "decoy_km": dkm,
            "sign_test_winner_closer": sign_test([1] * 10, [0 if a < b else 2 for a, b in zip(wkm, dkm)]),
            "reading": "winners sit systematically CLOSER to a census place than their decoys. The HT rubric "
                       "cuts at 25 km. Settler record clusters at towns. This was NOT matched and it runs "
                       "in the winners' favour -- it is the leading alternative explanation for the +0.9.",
        },
        "POST_HOC_distance_controlled_subset": {
            "n_pairs": len(both_in),
            "pairs": [r[0] for r in both_in],
            "winner_mean": round(sum(bw) / len(bw), 2) if bw else None,
            "decoy_mean": round(sum(bd) / len(bd), 2) if bd else None,
            "separation": round(sum(bw) / len(bw) - sum(bd) / len(bd), 2) if bw else None,
            "sign_test": sign_test(bw, bd),
            "STATUS": "POST HOC, NOT PRE-REGISTERED, n small, winners at the HT3 ceiling. This is a "
                      "hypothesis for the next instrument, NOT a result, and it does NOT overturn the "
                      "primary verdict above.",
        },
        "instrument_defect_landform_name_salience": (
            "Winners carry famous landform names (Madison, Helena, Teton, Sandia); several decoys are "
            "'unnamed fault near X' or obscure (Bull Mountain western border, Hubbell Spring). Both HT0s in "
            "this table -- one winner, one decoy -- and the control's zero are NAME CONFLATIONS, not absences: "
            "Red Rock returned Red Lodge, Bull Mountain returned Roundup and Boulder COLORADO, Sweetwater "
            "returned Wyoming, Thompson Valley returned Virginia, Round Valley returned Mendocino. Five of "
            "twenty first passes went to the wrong state. This is an unmeasured bias with an unknown sign."),
        "rows": [{"rank": r[0], "winner": r[1], "winner_HT": r[2], "winner_note": r[3],
                  "decoy": r[4], "decoy_HT": r[5], "decoy_note": r[6],
                  "winner_nearest_km": NEAREST_KM[r[1]], "decoy_nearest_km": NEAREST_KM[r[4]]} for r in ROWS],
    }
    json.dump(out, open('lore3_result.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))


if __name__ == '__main__':
    main()
