"""NATIVE / HISTORICAL LORE EXPERIMENT (v2) -- covariate measurement.

Run and committed BEFORE any Native-lore lookup. Same ordering discipline as v1.

WHY THIS FILE EXISTS AT ALL. Clayton's prediction is "Native lore specifically will
group around our ranked sites." That prediction has a back door wide enough to drive
the whole result through, and v1's matching does NOT close it:

  v1 matched decoys on CENSUS PLACES within 50 km -- a modern settler-town proxy. That
  is the right confounder for a 1950s UFO-sighting record and close to IRRELEVANT for
  whether a place carries documented Indigenous lore. The pairs are reusable; the
  matching is not. So the covariates get MEASURED instead, and pre-declared as able to
  kill the finding.

THE THREE BACK DOORS, in the order I expect them to matter:

  C1 RELIEF. The physics score rewards long, young, high-slip normal faults. Those ARE
     the range fronts -- Teton, Madison, Sandia, Sangre de Cristo. Prominent mountains
     attract sacred-place narrative in essentially every culture area on the continent.
     If winners out-relieve decoys, "physics predicts Native lore" and "big mountains
     have stories" are the same sentence and this experiment cannot separate them.
     MEASURED: 7x7 grid of NED 10 m elevations over a +/-25 km box; relief = max - min.

  C2 TRIBAL PRESENCE. Whether a place's lore is on the searchable web tracks whether a
     federally recognised nation nearby publishes, and whether ethnographers collected.
     MEASURED: geodesic km to the nearest Federal American Indian Reservation or
     off-reservation trust land (Census TIGERweb, 2020 vintage), 0 if inside.

  C3 INTERPRETIVE LITERATURE. An NPS unit generates ethnographic overviews, trailhead
     signage and a thousand blog posts. A nameless fault in Nevada generates none. This
     is a pure documentation term with no connection to rock.
     MEASURED: geodesic km to the nearest NPS unit boundary, 0 if inside.

PRE-DECLARED KILL RULE, fixed before any lore is looked at:
  If winners exceed decoys on C1 relief by more than 300 m of median local relief, OR
  the paired sign test on any covariate favours winners at p <= 0.125 (the same
  threshold v1's readout used), then a positive Native-lore result is reported as
  CONFOUNDED-NOT-SUPPORTED regardless of its size. A confound that survives measurement
  is not neutralised by being mentioned in a footnote.

  If the covariates come out balanced, the lore comparison stands on its own.

NOTHING IN THIS FILE LOOKS AT LORE. It reads coordinates and returns terrain and
jurisdiction. Run it, commit it, then and only then start searching.
"""
import json, math, time, urllib.parse, urllib.request
import truststore; truststore.inject_into_ssl()

R_EARTH = 6371.0088


def haversine(la1, lo1, la2, lo2):
    p = math.pi / 180
    a = (math.sin((la2 - la1) * p / 2) ** 2
         + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(a))


def get(url, timeout=90, tries=3):
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as fh:
                return json.load(fh)
        except Exception as exc:
            if k == tries - 1:
                raise
            time.sleep(2 + 3 * k)


# ---------------------------------------------------------------- C1 relief
def relief(lat, lon, half_km=25.0, n=7):
    """max-min NED 10 m elevation over an n x n grid on a square-on-the-ground box."""
    dlat = half_km / 111.32
    dlon = half_km / (111.32 * math.cos(math.radians(lat)))
    pts = []
    for i in range(n):
        for j in range(n):
            fy = -1 + 2 * i / (n - 1)
            fx = -1 + 2 * j / (n - 1)
            pts.append((lat + fy * dlat, lon + fx * dlon))
    loc = '|'.join(f'{a:.5f},{b:.5f}' for a, b in pts)
    r = get('https://api.opentopodata.org/v1/ned10m?locations=' + loc)
    time.sleep(1.1)                      # opentopodata: 1 call/sec, respected
    ev = [x['elevation'] for x in r['results'] if x['elevation'] is not None]
    if len(ev) < n * n * 0.8:
        return {'relief_m': None, 'n_ok': len(ev), 'note': 'insufficient DEM coverage'}
    mean = sum(ev) / len(ev)
    sd = (sum((e - mean) ** 2 for e in ev) / len(ev)) ** 0.5
    return {'relief_m': round(max(ev) - min(ev), 1), 'max_m': round(max(ev), 1),
            'min_m': round(min(ev), 1), 'sd_m': round(sd, 1), 'n_ok': len(ev)}


# ------------------------------------------------- C2/C3 distance to polygons
def nearest_polygon_km(lat, lon, url, layer, radius_km, name_field):
    """Geodesic km to nearest polygon boundary within radius_km; 0.0 if inside one."""
    q = {
        'geometry': json.dumps({'x': lon, 'y': lat, 'spatialReference': {'wkid': 4326}}),
        'geometryType': 'esriGeometryPoint', 'inSR': '4326', 'outSR': '4326',
        'spatialRel': 'esriSpatialRelIntersects',
        'distance': str(radius_km * 1000), 'units': 'esriSRUnit_Meter',
        'outFields': name_field, 'returnGeometry': 'true', 'f': 'json',
    }
    r = get(f'{url}/{layer}/query?' + urllib.parse.urlencode(q))
    best, best_name = None, None
    for feat in r.get('features', []):
        nm = (feat.get('attributes') or {}).get(name_field)
        rings = (feat.get('geometry') or {}).get('rings') or []
        for ring in rings:
            # inside test (ray casting) -- an interior point is distance 0, not
            # "distance to the nearest vertex", which would be badly wrong for a
            # site sitting in the middle of a large reservation.
            inside = False
            for a in range(len(ring)):
                x1, y1 = ring[a - 1][0], ring[a - 1][1]
                x2, y2 = ring[a][0], ring[a][1]
                if (y1 > lat) != (y2 > lat):
                    xin = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
                    if xin > lon:
                        inside = not inside
            if inside:
                return {'km': 0.0, 'name': nm, 'inside': True}
            for x, y in ring:
                d = haversine(lat, lon, y, x)
                if best is None or d < best:
                    best, best_name = d, nm
    if best is None:
        return {'km': None, 'name': None, 'inside': False,
                'note': f'none within {radius_km} km'}
    return {'km': round(best, 1), 'name': best_name, 'inside': False}


TIGER = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/AIANNHA/MapServer'
NPS = ('https://services1.arcgis.com/fBc8EJBxQRMcHlei/arcgis/rest/services/'
       'NPS_Land_Resources_Division_Boundary_and_Tract_Data_Service/FeatureServer')


def main():
    d = json.load(open('lore_experiment_design.json'))
    sites = []
    for p in d['pairs']:
        sites.append(dict(role='winner', rank=p['winner']['rank'],
                          fault=p['winner']['fault'], lat=p['winner']['lat'],
                          lon=p['winner']['lon'], score=p['winner']['score']))
        sites.append(dict(role='decoy', rank=p['winner']['rank'],
                          fault=p['decoy']['fault'], lat=p['decoy']['lat'],
                          lon=p['decoy']['lon'], score=p['decoy']['score']))
    # the two pre-declared controls, carried through every stage of this program
    sites.append(dict(role='control', rank=None, fault='Sandia fault (control+)',
                      lat=35.201, lon=-106.446, score=None))
    sites.append(dict(role='control', rank=None, fault='Hubbell Spring fault (control-)',
                      lat=34.812, lon=-106.646, score=None))

    out = []
    for s in sites:
        rec = dict(s)
        rec['relief'] = relief(s['lat'], s['lon'])
        rec['tribal'] = nearest_polygon_km(s['lat'], s['lon'], TIGER, 38, 150, 'BASENAME')
        if rec['tribal']['km'] is None:
            rec['tribal_trust'] = nearest_polygon_km(s['lat'], s['lon'], TIGER, 39, 150,
                                                     'BASENAME')
        rec['nps'] = nearest_polygon_km(s['lat'], s['lon'], NPS, 2, 150, 'UNIT_NAME')
        out.append(rec)
        print(f"{s['role']:8s} {s['fault'][:34]:34s} "
              f"relief={rec['relief'].get('relief_m')} "
              f"tribal={rec['tribal'].get('km')} nps={rec['nps'].get('km')}", flush=True)

    json.dump({'measured': '2026-08-16',
               'purpose': 'confound covariates for the Native/historical lore experiment',
               'lore_status': 'HELD OUT -- no Native-lore query has been run at write time',
               'kill_rule': ('winners > decoys by >300 m median relief, or paired sign '
                             'test p<=0.125 on any covariate favouring winners => a '
                             'positive lore result is CONFOUNDED-NOT-SUPPORTED'),
               'sites': out}, open('lore2_covariates.json', 'w'), indent=1)
    print('\nwrote lore2_covariates.json')


if __name__ == '__main__':
    main()
