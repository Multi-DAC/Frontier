"""NATIVE / HISTORICAL LORE EXPERIMENT (v2) -- design and pre-declared rubric.

Written and committed BEFORE a single Native-lore query is run. Companion to
lore2_covariates.py, which measures the three confounders this design cannot argue
away. Same ordering discipline as v1: the freeze IS the instrument.

THE PREDICTION UNDER TEST, in Clayton's words (2026-08-16):
    "My guess is that Native lore specifically will group around our ranked sites."

    H2: physics rank -> density of place-specific Indigenous narrative
    H3: physics rank -> density of US/settler historical incident record

-----------------------------------------------------------------------------
WHY H2 IS NOT SHAPED LIKE H1, AND WHY THAT MATTERS MORE THAN THE RESULT

v1 tested a UFO/ghost-light record. That record is a MODERN artifact: it needs a
witness with a telephone, a newspaper, a sheriff's office, a web form. Matching on
census places within 50 km was therefore the correct confounder, and v1 did it.

Indigenous place-narrative is a DIFFERENT KIND OF OBJECT and the v1 matching does
almost nothing for it. Three ways it differs, all of which cut against a clean read:

  1. THE BASE RATE IS NEAR-UNITY. People lived, named and storied essentially every
     landform in the western US for millennia. "Is there Native lore here?" has the
     answer YES almost everywhere, and a test whose null is 100% cannot separate
     sites. So the raw presence of Native lore is NOT the measurement. What varies
     is whether that narrative is (a) ANOMALY-SHAPED and (b) SEARCHABLE. Both are
     scored, separately, and the second is a property of archives, not of rock.

  2. SEARCHABILITY IS A SETTLER ARTIFACT WITH A DIRECTION. What reaches a web index
     is the residue of who was ethnographied, who was displaced from where, which
     nations publish today, and which material was extracted and circulated without
     consent. That residue is dense in the Pueblo Southwest and thin across the
     Great Basin -- and it is thin in exactly the places where removal was most
     complete. This is a biased sample with a KNOWN SIGN, not noise around zero.

  3. MUCH OF THE REAL CORPUS IS RESTRICTED AND SHOULD STAY THAT WAY. Place-specific
     knowledge is frequently held by particular people, seasons or societies and is
     not mine to go collect. I am reading a published fragment. I am not going to
     treat silence as evidence of absence, and I am not going to go looking for
     material whose absence from the open web is the point.

  CONSEQUENCE, pre-declared: this instrument CAN REFUTE H2 and CANNOT CONFIRM IT. A
  null is informative -- if the ranked sites show no more anomaly-shaped Indigenous
  narrative than matched decoys, the prediction failed on the corpus available. A
  POSITIVE is not a discovery about rock until the covariates in lore2_covariates.py
  come out balanced, and even then it remains a claim about a published fragment.
  This asymmetry is stated now, before the numbers, so it cannot be discovered later
  at whatever strength happens to be convenient.

-----------------------------------------------------------------------------
THE DENOMINATOR, which is the actual fix for problem (1)

Every site is scored TWICE:

  N_ANY   Is there ANY documented, place-specific Indigenous association with this
          landform or its named features within 25 km? (naming, territory, travel
          route, resource use, residence, a recorded narrative of any kind.)
  N_ANOM  Of that, is any of it ANOMALY-SHAPED -- lights, spirit-beings tied to the
          locus, power/medicine places, taboo or avoidance, transformation,
          thunder/underworld association, emergence?

  The headline statistic is the RATIO N_ANOM / N_ANY across the group, not the count
  of N_ANOM. A site with rich documented lore and none of it anomalous is EVIDENCE
  AGAINST H2, and a count-only design would have scored it as a win.

-----------------------------------------------------------------------------
PRE-DECLARED TIERS. Fixed now. Applied identically to winners, decoys and controls.

  NATIVE (anomaly-shaped), scored only where N_ANY is satisfied:
    NT3  Place-specific anomaly-shaped narrative tied to THIS landform or a named
         feature on it, within 25 km, attested in ethnography, a tribal/nation
         source, an academic treatment, a state historical society, or a pre-1995
         printed collection.
    NT2  Same content, within 25 km, but attested only in modern web-native
         secondary retellings (tourism pages, listicles, aggregators, blogs).
    NT1  Anomaly-shaped narrative attributed to the broader region or nation without
         a locus, or a specific locus at 25-60 km.
    NT0  Documented Indigenous association exists (N_ANY yes) but nothing
         anomaly-shaped under the protocol.
    NX   N_ANY itself not established under the protocol -> EXCLUDED from the ratio
         and reported as a coverage gap, NOT scored as a zero. An unsearchable site
         is a hole in the instrument, not a negative result.

  US / SETTLER HISTORICAL (H-tier), scored independently:
    HT3  Named, place-specific historical incident or persistent local tradition
         within 25 km in a primary/archival source (newspaper archive, county
         history, USGS/military record, historical society).
    HT2  Same within 25 km, web-secondary only.
    HT1  Regional-level or 25-60 km.
    HT0  Nothing under the protocol.

  PROTOCOL, identical per site, no site gets an extra pass. Four queries:
    (a) <nearest named landform/range> + the tribe(s) whose territory it sits in
    (b) <landform/place> + Native American OR Indigenous + legend OR story OR sacred
    (c) <landform/place> + <state> + history + settlement OR mining OR incident
    (d) <tribe name> + <landform> + spirit OR lights OR taboo OR power
  Whatever the first pass returns is the score. Chasing a thread on a winner and not
  on its decoy is how a null gets converted into a positive without anyone deciding
  to cheat. This sentence is copied verbatim from v1 because it was the clause that
  mattered most there and nothing about a new subject makes it less true.

  SCORED BLIND? NO. Same as v1, same mitigation, same warning: I know which names
  are winners; query template and tier definitions are frozen here pre-lookup, so
  the discretion left to me is scoring. Read tier assignment as the weakest link.

-----------------------------------------------------------------------------
PRE-DECLARED READOUT
  Primary   : winners' mean NT vs decoys' mean NT, over pairs where BOTH members
              clear N_ANY. >= 1 full tier in the predicted direction = SUPPORTED.
  Secondary : ratio N_ANOM/N_ANY, winners vs decoys.
  Paired    : sign test across the 10 pairs, two-sided.
  Controls  : Sandia (physics pass, known-positive lore) and Hubbell Spring (physics
              pass, deliberately NOT lore-rescued) are scored under the identical
              protocol. Sandia is the POSITIVE CONTROL -- if the protocol cannot
              recover anomaly-shaped Indigenous narrative at Sandia, where it is
              abundantly published, the protocol is broken and NO other cell in this
              table means anything. That check is run and reported FIRST.
  Kill rule : inherited unchanged from lore2_covariates.py -- if winners beat decoys
              on relief by >300 m median, or any covariate sign test favours winners
              at p <= 0.125, a positive result is reported CONFOUNDED-NOT-SUPPORTED.

n=10 pairs. This can refute. It cannot confirm. Twice over, for H2.
"""

RUBRIC = {
    "designed": "2026-08-16",
    "supersedes": None,
    "companion": "lore_experiment_design.py (v1, anomalous-light record)",
    "hypotheses": {
        "H2": "physics rank -> anomaly-shaped Indigenous place-narrative density",
        "H3": "physics rank -> US/settler historical incident density",
    },
    "native_tiers": ["NT3", "NT2", "NT1", "NT0", "NX"],
    "settler_tiers": ["HT3", "HT2", "HT1", "HT0"],
    "denominator": "N_ANY -- any documented Indigenous association within 25 km",
    "headline": "ratio N_ANOM/N_ANY, not count of N_ANOM",
    "queries_per_site": 4,
    "blind": False,
    "positive_control": "Sandia fault -- run and reported FIRST; failure invalidates all",
    "negative_control": "Hubbell Spring fault",
    "asymmetry": ("instrument can REFUTE H2, cannot CONFIRM it; searchability of "
                  "Indigenous narrative is a settler-archive artifact with a known sign"),
    "excluded_not_zeroed": "NX sites are coverage gaps, not negatives",
    "readout_rule": ">=1 full tier separation on mean NT, predicted direction = SUPPORTED",
    "kill_rule": "see lore2_covariates.py -- confound beats effect",
    "lore_status_at_freeze": "NO Native-lore query has been run at the time of writing",
}

if __name__ == '__main__':
    import json
    json.dump(RUBRIC, open('lore2_design.json', 'w'), indent=1)
    print(json.dumps(RUBRIC, indent=1))
