"""BLIND RE-SCORE -- design, sanitiser and packet builder.  §7.1 of the final report.

THE DEFECT BEING REPAIRED, stated exactly:
  Every rubric and every query string in the three lore legs was frozen before any
  lookup.  The SCORER was not.  I knew which site was the physics winner and which
  was its matched decoy while I was reading returns and assigning tiers -- and tier
  assignment is a judgement call at every boundary (recurring vs one-off, named vs
  unnamed, place-specific vs regional, whether 25.9 km counts).  That is a term in
  every one of the three legs, it is in no leg's design document, and because it is
  SHARED it is also a candidate common cause for the rho = 0.32-0.48 cross-leg
  correlation reported in §4.2 of report 08.

WHAT THIS INSTRUMENT CAN AND CANNOT DO, declared before it runs:
  CAN   -- remove the scorer's knowledge of role (winner/decoy/control), rank, and
           pair membership at the moment of tier assignment.
  CAN   -- remove the COMMON scorer across legs: each leg goes to a different set of
           scorers with no shared context, so cross-leg rho can be recomputed with
           the shared-cause candidate deleted.  This is the sharpest test here.
  CANNOT -- undo sighted COLLECTION.  The evidence notes were written by the sighted
           scorer.  If I chased threads harder on winners, that bias is baked into
           the text and a blind re-tier inherits it.  Gauged, not waved at: see
           collection_bias() in blind_rescore_readout.py.  Result stands as an
           UPPER BOUND on how much of the separation the blinding can remove.

SANITISATION (applied identically to every item, no exceptions):
  - fault name, rank, role, pair partner, nearest-town distance: REMOVED.
  - explicit tier tokens in the note text (T0-T3, NT0-3, HT0-3) -> "[TIER]".
    Those leak the sighted answer directly.  Everything else in the note is
    EVIDENCE and is kept verbatim, including stated distances, source types and
    conflation warnings -- those are the facts the rubric operates on.
  - role words (winner, decoy, control, POSITIVE CONTROL) -> removed.
  - opaque IDs, deterministic shuffle, SEED = 20260816, committed in this file
    BEFORE any scorer sees anything.

CONTROLS ON THE NEW INSTRUMENT (the blind scorers are themselves untested):
  Two synthetic probe items are seeded into every leg's packet, indistinguishable
  in form from real ones, with tiers pre-declared HERE:
      probe_pos -> top tier (3),  probe_null -> bottom tier (0)
  VOID RULE, pre-declared: a scorer column that misses EITHER probe by more than
  one tier is VOID and is dropped from the consensus before any readout is read.
  Probe items are excluded from every statistic.

READOUT, pre-declared:
  - 3 independent scorers per leg, no shared context, different scorers per leg.
  - consensus tier = MEDIAN of the surviving columns (ties -> lower tier, the
    conservative direction for a hypothesis that needs separation).
  - primary blinded verdict re-applies each leg's ORIGINAL readout rule verbatim
    (>= 1.0 full tier separation, winners over decoys, predicted direction).
  - also reported: per-scorer verdicts, blind-vs-sighted weighted kappa,
    inter-scorer weighted kappa (rubric reliability -- a number the program has
    never had), and cross-leg Spearman rho on consensus tiers.
  - NOTHING is unblinded until every scorer column is on disk.
"""
import json
import os
import random
import re

W = os.path.dirname(os.path.abspath(__file__))
SEED = 20260816

# ---------------------------------------------------------------- source legs
import lore_experiment_result as L1
import lore2_result as L2
import lore3_result as L3

TIER_TOKEN = re.compile(r'\b(?:N|H)?T[0-3]\b')
ROLE_WORD = re.compile(r'(?i)\b(positive control|negative control|control[+-]|'
                       r'winner|decoy|control)\b')

# Two leak channels, handled at DIFFERENT widths on purpose.
#
# (1) LEAK_SPANS -- the sighted tier written into the note as a conclusion
#     ("-> T2 by rule", "fails both T1 clauses", "so 25-60km clause").  These are
#     excised as SPANS, not as clauses.  A first cut dropped the whole clause and
#     took the discriminator with it: "recurring -- but 41-49km away, 25-60km
#     clause" lost the 41-49 km, and distance is precisely what the rubric turns
#     on.  A filter scoped wider than the thing it is filtering deletes evidence
#     and the deletion is silent.
# (2) META -- commentary about the INSTRUMENT rather than about the site ("the
#     instrument CAN return zero", "EXCLUDED from the readout as pre-declared").
#     No site facts live in these, so they go at clause width.
#     NOT in this list, deliberately: "first pass" / "web-secondary" / "listicle".
#     Those read as commentary and are actually the NT3-vs-NT2 discriminator.
LEAK_SPANS = [
    re.compile(r'\s*-+>\s*[^;.]*$'),
    re.compile(r'(?i)[,;]?\s*(?:so\s+)?(?:it is\s+)?(?:the\s+)?25-?60\s*km\s*'
               r'(?:band|clause)'),
    re.compile(r'(?i)\s*\[TIER\]\s*(?:by rule|clauses?)'),
]
META = ("instrument", "readout", "pre-declared", "prereg", "verdict",
        "protocol", "by rule", "amend")
SPLIT = re.compile(r'(\s*;\s*|\s+--\s+|(?<=[a-z0-9)\'"])\.\s+)')


def sanitise(note):
    s = TIER_TOKEN.sub('[TIER]', note)
    s = ROLE_WORD.sub('[REDACTED]', s)
    for rx in LEAK_SPANS:
        s = rx.sub('', s)
    parts = SPLIT.split(s)
    units, delims = parts[0::2], parts[1::2] + ['']
    out = ''.join(u + d for u, d in zip(units, delims)
                  if u.strip() and not any(m in u.lower() for m in META))
    out = re.sub(r'\[REDACTED\][ ,.-]*', '', out)
    out = re.sub(r'\s+', ' ', out).strip(' .-,;')
    return out


# ------------------------------------------------------- synthetic probe items
PROBES = {
    "L1": [
        ("probe_pos", 3,
         "recurring nocturnal light at a named locus 9 km out, logged 1931-present; "
         "attested in a 1974 county historical society volume and the local daily "
         "newspaper archive"),
        ("probe_null", 0,
         "returned bedrock mapping reports and a state highway realignment notice "
         "only; no light, apparition or anomaly record of any kind at any distance"),
    ],
    "L2": [
        ("probe_pos", 3,
         "named spirit-being said to inhabit a spring on this landform, avoidance "
         "taboo recorded; tribal cultural-resources office statement plus a 1961 "
         "university ethnography, 11 km"),
        ("probe_null", 0,
         "documented ancestral hunting territory and a named seasonal camp within "
         "the area; nothing anomaly-shaped in any source returned"),
    ],
    "L3": [
        ("probe_pos", 3,
         "1887 powder-magazine explosion at a named townsite 12 km out, 9 dead; "
         "county history volume plus contemporaneous newspaper archive"),
        ("probe_null", 0,
         "nothing on-target returned; hits resolved to a same-named county in "
         "another state at several hundred km"),
    ],
}

RUBRICS = {
    "L1": """T3  named place-specific recurring record within 25 km, non-listicle source
T2  recurring record within 25 km, web-aggregator / blog / tourism source only
T1  isolated or one-off event within 25 km, OR a recurring record at 25-60 km
T0  nothing under the protocol""",
    "L2": """NT3  place-specific anomaly-shaped narrative tied to THIS landform or a named
     feature on it, within 25 km, attested in ethnography, a tribal/nation source,
     an academic treatment, a state historical society, or a pre-1995 printed
     collection.
NT2  same content, within 25 km, but attested only in modern web-native secondary
     retellings (tourism pages, listicles, aggregators, blogs).
NT1  anomaly-shaped narrative attributed to the broader region or nation without a
     locus, OR a specific locus at 25-60 km.
NT0  documented Indigenous association exists but nothing anomaly-shaped under the
     protocol.
("anomaly-shaped" = lights/fire in the sky, sky-beings or star-people, a named
 power/medicine locus, taboo or avoidance, transformation, thunder/underworld
 association, emergence.)""",
    "L3": """HT3  named, place-specific historical incident or persistent local tradition
     within 25 km in a primary/archival source (newspaper archive, county history,
     USGS/military record, historical society).
HT2  same within 25 km, web-secondary only.
HT1  regional-level, OR 25-60 km.
HT0  nothing under the protocol.""",
}


def build():
    items = {"L1": [], "L2": [], "L3": []}

    for name, (tier, note) in L1.SCORES.items():
        items["L1"].append({"key": name, "sighted": tier, "note": note})

    for r in L2.ROWS:
        items["L2"].append({"key": r[1], "sighted": r[2], "note": r[3]})
        items["L2"].append({"key": r[4], "sighted": r[5], "note": r[6]})

    for r in L3.ROWS:
        items["L3"].append({"key": r[1], "sighted": r[2], "note": r[3]})
        items["L3"].append({"key": r[4], "sighted": r[5], "note": r[6]})
    # leg 3's negative-side control is a real 21st item; it was scored under the
    # same protocol and reported, so it is blinded too (still excluded at readout).
    items["L3"].append({"key": "Hubbell Spring fault (control-)",
                        "sighted": L3.CONTROLS["Hubbell Spring fault (control-)"][0],
                        "note": L3.CONTROLS["Hubbell Spring fault (control-)"][1]})

    key_map, packets = {}, {}
    for leg in ("L1", "L2", "L3"):
        rows = [dict(it, probe=None) for it in items[leg]]
        for pid, ptier, pnote in PROBES[leg]:
            rows.append({"key": pid, "sighted": ptier, "note": pnote, "probe": pid})

        rng = random.Random(SEED + int(leg[1]))
        rng.shuffle(rows)

        packet, kmap = [], {}
        for i, r in enumerate(rows, 1):
            iid = f"{leg}-{i:02d}"
            kmap[iid] = {"key": r["key"], "sighted": r["sighted"],
                         "probe": r["probe"], "note_raw": r["note"]}
            packet.append({"id": iid, "evidence": sanitise(r["note"])})
        key_map[leg] = kmap
        packets[leg] = {"leg": leg, "rubric": RUBRICS[leg], "items": packet}

    json.dump(packets, open(os.path.join(W, "blind_packet.json"), "w"), indent=1)
    json.dump(key_map, open(os.path.join(W, "blind_keymap.json"), "w"), indent=1)
    print(f"[seed] {SEED}")
    for leg in packets:
        n = len(packets[leg]["items"])
        print(f"[{leg}] {n} items ({n - 2} real + 2 probes)")
    print("[wrote] blind_packet.json  blind_keymap.json")


if __name__ == "__main__":
    build()
