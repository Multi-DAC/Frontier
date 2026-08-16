"""National screen, stages 1-2 ONLY (conduit + driver + modern strain).

Split out from national_site_screen.py deliberately: the lithology stage hits the
Macrostrat API and shares a cache file with lithology_baserate.py, which is running.
Two writers on one cache is a corruption race, so strain -- which is purely local --
runs first and ranks the field. Lithology runs on the survivors afterwards.

FIXED HERE, both silent in the original:
  (a) endpoint was MapServer/12 = "New Mexico", not /21 = "National Database". A
      screen advertised as continental-US queried one state, and that state has ZERO
      faults above 5 mm/yr -- hence "[stage1] +0 (total 0)" with no error.
  (b) where-clause said 'Between 5.0 and 1.0 mm/yr'; the domain string is
      'Between 1.0 and 5.0 mm/yr'. Alone this drops 16,667 of 32,891 features -- half
      the population -- and still returns a plausible non-zero count from the OR's
      other arm. That is the dangerous one: it fails without looking like it failed.
"""
import json, sys, os
sys.path.insert(0, 'work')
import national_site_screen as N   # noqa: E402

nodes = json.load(open('work/screen_nodes.json'))
rows = []
for i, nd in enumerate(nodes):
    st = N.strain_at(nd['lat'], nd['lon'], nscram=200)
    rows.append({**nd, 'strain': st})
    if (i + 1) % 25 == 0:
        print(f'[{i+1}/{len(nodes)}]', file=sys.stderr, flush=True)
straining = [r for r in rows if r['strain'].get('verdict') == 'STRAINING']
unmeas = [r for r in rows if r['strain'].get('gmax_nstrain_yr') is None]
straining.sort(key=lambda r: -r['strain']['gmax_nstrain_yr'])
json.dump({'n_nodes': len(rows), 'n_straining': len(straining),
           'n_unmeasured': len(unmeas), 'straining': straining, 'all': rows},
          open('work/screen_strain_pass.json', 'w'), indent=1)
print(f'nodes={len(rows)}  STRAINING={len(straining)}  unmeasured={len(unmeas)}',
      file=sys.stderr)
for r in straining[:20]:
    print(f"  {r['fault_name'][:38]:<38} {r['lat']:7.3f},{r['lon']:9.3f} "
          f"slip={r['slip']:<5} gmax={r['strain']['gmax_nstrain_yr']:>7} "
          f"p={r['strain']['p_scramble']}", file=sys.stderr)
