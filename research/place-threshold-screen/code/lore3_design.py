"""H3 -- US / SETTLER HISTORICAL LEG. Design, rubric and the exact 20 query strings.

Written and committed BEFORE a single H3 lookup is run. Companion to lore2_design.py
(which froze both H2 and H3 tiers) and lore2_result.py (which reported H3 as UNTESTED,
absent by omission rather than by finding). This file closes that stated gap.

INHERITED UNCHANGED from lore2_design.py, not re-decided here:
  * the HT tier ladder (HT3/HT2/HT1/HT0), verbatim
  * query template (c): <landform/place> + <state> + history + settlement OR mining OR incident
  * the 10 matched winner/decoy pairs and their observer matching
  * "whatever the first pass returns is the score" -- no thread-chasing on winners
  * scoring is NOT blind; tier assignment is the weakest link and is named as such
  * readout: >= 1 full tier separation on the mean, predicted direction = SUPPORTED

-----------------------------------------------------------------------------
WHY H3 IS A BETTER-INSTRUMENTED TEST THAN H2, AND WHY THAT CUTS BOTH WAYS

H2's problem was that its covariate matching did almost nothing. Indigenous place-
narrative is not produced by modern population; matching on census places within 50 km
matched the wrong thing, and the design said so before the numbers came in.

H3 is the opposite case. Settler historical record IS a modern-population artifact --
it needs a newspaper, a county clerk, a mining registrar, a historical society. That
is exactly what the v1 observer proxy measures. So the matching that was nearly inert
for H2 is the CORRECT confounder control for H3, and it is already frozen and already
near-exact (4/4, 16/15, 47/44, 22/22, 3/3, 3/3, 20/20, 59/61, 6/6, 5/5).

The cost of that is stated now, not later: because the pairs are matched on the very
thing that generates settler record, H3 has had its most likely positive mechanism
DELIBERATELY REMOVED. If winners still beat decoys, it is not "more people wrote about
the winners." If they do not, the honest reading is that the physics rank carries no
settler-historical signal beyond population -- which is the interesting question and
also, on the H2 precedent, the likely answer.

-----------------------------------------------------------------------------
THE DENOMINATOR, same fix as H2's N_ANY, applied before looking

  H_ANY   Any documented US/settler historical association within 25 km -- settlement,
          mining district, ranching, railroad, military, road, named incident.
  H_SPEC  Of that, is any of it a NAMED, PLACE-SPECIFIC incident or persistent local
          tradition attached to this landform or a named feature on it?

  Expected base rate on H_ANY: near unity, same as N_ANY came in at 20/20. Every
  western US site of this kind has settlement or mining history. A count of H_ANY is
  therefore worthless as a discriminator and is NOT the headline. The headline is the
  mean HT and the H_SPEC/H_ANY ratio. This paragraph is written before the queries run
  so that a 20/20 result cannot be reported as a finding afterwards.

-----------------------------------------------------------------------------
HT TIERS -- copied verbatim from lore2_design.py, not restated in new words

  HT3  Named, place-specific historical incident or persistent local tradition within
       25 km in a primary/archival source (newspaper archive, county history,
       USGS/military record, historical society).
  HT2  Same within 25 km, web-secondary only.
  HT1  Regional-level or 25-60 km.
  HT0  Nothing under the protocol.

  There is deliberately no HX. Unlike Indigenous narrative, absence of settler record
  in a web index is genuinely informative -- the archive bias runs the other way. An
  H3 zero is a zero.

-----------------------------------------------------------------------------
POSITIVE CONTROL, with its expected answer declared IN ADVANCE

  Sandia fault. Run FIRST, reported FIRST. I hold independent ground truth here from
  the Manzano document produced on 2026-08-15: Manzano Weapons Storage Area, Kirtland
  AFB, and the 1979-80 Bennewitz affair with its documented AFOSI disinformation
  operation -- all within 25 km of 35.153 / -106.472.

  PASS  = query (c) returns named, place-specific historical incident within 25 km.
  FAIL  = it returns only generic Albuquerque-area background. If it FAILS, the
          protocol is broken and NO other cell in this table means anything -- and
          note that this is precisely how the v1 lore run died: three frozen queries
          at Sandia returned generic Albuquerque UFO history and never touched
          Bennewitz. The same failure mode is live here and is being watched for.

  NEGATIVE-SIDE CONTROL: Hubbell Spring fault (35.02 / -106.72), scored under the
  identical protocol, reported, and EXCLUDED from the winner/decoy readout.

-----------------------------------------------------------------------------
KILL RULE, pre-declared

  If H3 comes out SUPPORTED, it is reported as CONFOUNDED unless the observer-density
  match holds on the pairs that drove it -- i.e. any pair where the winner has more
  than 1.5x the decoy's census places within 50 km is flagged and the readout is
  recomputed without it. The pairs are already matched, so this should be a no-op;
  it is written down anyway because a no-op check is only a no-op after you run it.
"""
import json

PAIRS = json.load(open('lore_experiment_design.json'))['pairs']

STRIP_SUFFIX = (' fault zone', ' faults', ' fault')
STRIP_PLACE = (' CDP', ' city', ' town', ' village')


def landform(name, nearest_place):
    """Mechanical, so the query set is reproducible from the frozen file alone."""
    base = name
    for s in STRIP_SUFFIX:
        if base.endswith(s):
            base = base[:-len(s)]
            break
    if base.lower().startswith('unnamed'):
        return None          # no landform name exists -> place carries the query
    return base


def place(p):
    for s in STRIP_PLACE:
        if p.endswith(s):
            return p[:-len(s)]
    return p


def query_for(site):
    nearest = site['observer']['nearest'][0]
    pl, st = place(nearest['place']), nearest['state']
    lf = landform(site['fault'], pl)
    head = f'"{lf}" {pl} {st}' if lf else f'{pl} {st}'
    return f'{head} history settlement OR mining OR incident'


def main():
    out = {
        'designed': '2026-08-16',
        'leg': 'H3 -- US/settler historical record',
        'inherits': 'lore2_design.py (HT tiers, template (c), pairs, readout, no-thread-chasing)',
        'hypothesis': 'H3: physics rank -> density of US/settler historical incident record',
        'denominator': 'H_ANY (near-unity expected); headline is mean HT and H_SPEC/H_ANY',
        'queries_per_site': 1,
        'blind': False,
        'covariate_note': 'observer matching (census places <=50km) is the CORRECT control '
                          'for H3 and was nearly inert for H2; the likely positive mechanism '
                          'has therefore been deliberately removed',
        'positive_control': {
            'site': 'Sandia fault',
            'expected_before_running': 'Manzano Weapons Storage Area / Kirtland AFB / '
                                       'Bennewitz 1979-80 AFOSI operation, all <25 km',
            'fail_condition': 'generic Albuquerque background only -- exactly how the v1 run died',
            'order': 'run and reported FIRST',
        },
        'negative_side_control': 'Hubbell Spring fault -- scored, reported, excluded from readout',
        'readout_rule': '>=1 full tier separation on mean HT, predicted direction = SUPPORTED',
        'kill_rule': 'if SUPPORTED, flag any pair where winner observer count > 1.5x decoy '
                     'and recompute without it',
        'h3_status_at_freeze': 'NO settler-history query has been run for ANY site at the time of writing',
        'queries': [],
    }
    for i, p in enumerate(PAIRS, 1):
        for role in ('winner', 'decoy'):
            s = p[role]
            out['queries'].append({
                'rank': i, 'role': role, 'fault': s['fault'],
                'lat': s['lat'], 'lon': s['lon'],
                'observer_places_50km': s['observer']['places_within_50km'],
                'query': query_for(s),
            })
    json.dump(out, open('lore3_design.json', 'w'), indent=1)
    for q in out['queries']:
        print(f"{q['rank']:>2} {q['role']:<6} {q['fault']:<38} {q['query']}")


if __name__ == '__main__':
    main()
