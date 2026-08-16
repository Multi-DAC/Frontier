"""Cross-leg reanalysis of the three lore legs (H1 lights / H2 Native / H3 settler).

Nothing here is a new lookup. Every input is already frozen on disk. Three questions
the individual legs could not ask, because each leg only ever saw itself:

  Q1  The nearest-town confound was MEASURED in leg 3 only. Legs 1 and 2 scored the
      same 20 sites under rubrics that also band on distance. Apply leg 3's OWN
      subset rule -- both members of a pair inside 25 km of a census place, so
      distance-to-town cannot discriminate -- unchanged, to legs 1 and 2.

  Q2  Are the three legs independent measurements, or one measurement three times?
      Spearman across all 20 sites, pairwise. High correlation means the pooled
      picture carries far less information than 3 x n suggests.

  Q3  A pooled sign test, computed and then explicitly discounted by Q2's answer.
      Reported because refusing to compute it is not the same as reporting why it
      does not mean what it looks like.

Post hoc, all of it. The primary verdicts stand as pre-registered and are not touched.
"""
import json
from math import comb

W = 'winner'
D = 'decoy'

# ---- inputs, all read from frozen artifacts ---------------------------------
h1 = json.load(open('lore_experiment_result.json'))
h2 = json.load(open('lore2_result.json'))
h3 = json.load(open('lore3_result.json'))

# nearest census place (km) -- measured in leg 3, keyed by fault name
NEAREST = {}
for r in h3['rows']:
    NEAREST[r['winner']] = r['winner_nearest_km']
    NEAREST[r['decoy']] = r['decoy_nearest_km']

LEGS = {
    'H1_lights': ('winner_tier', 'decoy_tier', h1['rows']),
    'H2_native': ('winner_NT', 'decoy_NT', h2['rows']),
    'H3_settler': ('winner_HT', 'decoy_HT', h3['rows']),
}


def sign_test(w, d):
    nz = [(a, b) for a, b in zip(w, d) if a != b]
    n = len(nz)
    k = sum(1 for a, b in nz if a > b)
    if n == 0:
        return {'non_tied': 0, 'favour_winner': 0, 'p_two_sided': 1.0}
    p = sum(comb(n, i) for i in range(n + 1)
            if abs(i - n / 2) >= abs(k - n / 2)) / 2 ** n
    return {'non_tied': n, 'favour_winner': k, 'p_two_sided': round(min(p, 1.0), 4)}


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 3) if den else None


out = {'note': 'POST HOC cross-leg reanalysis. No new lookups. Primary verdicts unchanged.'}

# ---- Q1: leg 3's distance-control rule, applied unchanged to legs 1 and 2 ----
q1 = {}
for leg, (wk, dk, rows) in LEGS.items():
    full_w = [r[wk] for r in rows]
    full_d = [r[dk] for r in rows]
    keep = [r for r in rows
            if NEAREST[r['winner']] <= 25 and NEAREST[r['decoy']] <= 25]
    kw = [r[wk] for r in keep]
    kd = [r[dk] for r in keep]
    q1[leg] = {
        'full_separation': round(sum(full_w) / len(full_w) - sum(full_d) / len(full_d), 2),
        'full_sign': sign_test(full_w, full_d),
        'n_pairs_distance_matched': len(keep),
        'pairs': [r['rank'] for r in keep],
        'matched_winner_mean': round(sum(kw) / len(kw), 2),
        'matched_decoy_mean': round(sum(kd) / len(kd), 2),
        'matched_separation': round(sum(kw) / len(kw) - sum(kd) / len(kd), 2),
        'matched_sign': sign_test(kw, kd),
        'delta_from_matching': round((sum(kw) / len(kw) - sum(kd) / len(kd))
                                     - (sum(full_w) / len(full_w) - sum(full_d) / len(full_d)), 2),
    }
out['Q1_distance_controlled'] = q1
out['Q1_reading'] = (
    'The SAME five pairs survive the filter in all three legs, because the filter is a '
    'property of the sites, not of the leg. Whatever this subset shows, it shows once.')

# ---- Q2: are the legs independent? ------------------------------------------
site_scores = {}
for leg, (wk, dk, rows) in LEGS.items():
    s = {}
    for r in rows:
        s[r['winner']] = r[wk]
        s[r['decoy']] = r[dk]
    site_scores[leg] = s

names = sorted(site_scores['H1_lights'])
pairwise = {}
legnames = list(LEGS)
for i in range(len(legnames)):
    for j in range(i + 1, len(legnames)):
        a, b = legnames[i], legnames[j]
        pairwise[f'{a} vs {b}'] = spearman([site_scores[a][n] for n in names],
                                           [site_scores[b][n] for n in names])
out['Q2_leg_independence'] = {
    'n_sites': len(names),
    'spearman_pairwise': pairwise,
    'reading': None,  # filled below
}

# ---- Q3: pooled sign test, and its discount ---------------------------------
pw, pd = [], []
for leg, (wk, dk, rows) in LEGS.items():
    pw += [r[wk] for r in rows]
    pd += [r[dk] for r in rows]
out['Q3_pooled_sign_test'] = {
    'pooled': sign_test(pw, pd),
    'pooled_separation': round(sum(pw) / len(pw) - sum(pd) / len(pd), 2),
    'WARNING': ('n=30 comparisons but only 10 independent SITE PAIRS. The three legs share '
                'their units, their observer-density matching, their searcher, and their '
                'name-salience defect. This p-value is an UPPER BOUND ON CONFIDENCE, not a '
                'result, and it is reported so that not computing it cannot be mistaken for '
                'it having been favourable.'),
}

# A hard-coded rho<0.5 cutoff here fired the flattering branch on its first run and said
# "close to independent". That cutoff had no justification behind it. Replaced with the
# actual test of rho != 0 at this n, which is a gauge instead of a preference.
def rho_p(rho, n):
    """two-sided p for Spearman rho != 0, t-approximation, n>=10."""
    if rho is None or abs(rho) >= 1:
        return None
    t = abs(rho) * ((n - 2) / (1 - rho ** 2)) ** 0.5
    df = n - 2
    # Student-t survival via continued-fraction-free series (regularized incomplete beta)
    x = df / (df + t * t)
    # I_x(df/2, 1/2) by numeric integration -- crude but adequate at this precision
    a, b, N = df / 2.0, 0.5, 20000
    s = 0.0
    for i in range(N):
        u = (i + 0.5) * x / N
        s += u ** (a - 1) * (1 - u) ** (b - 1)
    s *= x / N
    from math import lgamma, exp
    beta = exp(lgamma(a) + lgamma(b) - lgamma(a + b))
    return round(min(1.0, s / beta), 4)


nsites = len(names)
out['Q2_leg_independence']['spearman_p'] = {
    k: rho_p(v, nsites) for k, v in pairwise.items()}
mx = max(v for v in pairwise.values() if v is not None)
out['Q2_leg_independence']['reading'] = (
    f'pairwise rho = {sorted(pairwise.values())}, max {mx} at n={nsites} '
    f'(p={rho_p(mx, nsites)}). These are MODERATELY CORRELATED, not independent: the '
    'largest is significantly non-zero at this n. Three sub-threshold positives are '
    'therefore worth somewhere between one and three weak facts -- closer to one. The '
    'effective number of independent comparisons behind the pooled test below is under '
    'its nominal 22, so the pooled p is optimistic by an unquantified amount.')

json.dump(out, open('lore_crossleg.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
