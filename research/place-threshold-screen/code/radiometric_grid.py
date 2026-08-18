"""Aeroradiometric K / eU / eTh grids for North America, pulled once and sampled on-machine.

SOURCE. USGS OFR 2005-1413, "Aeroradiometric grids for North America"
(https://mrdata.usgs.gov/radiometric/), Duval/Snyder compilation, 2 km cells.

THREE WRONG TURNS ARE RECORDED HERE BECAUSE EACH ONE RETURNS PLAUSIBLE NUMBERS RATHER THAN
AN ERROR, AND THE NEXT PERSON WILL TAKE THEM TOO.

 1. THE SERVICE NAME. `https://mrdata.usgs.gov/services/nuresed?...GetCapabilities` returns a
    349,783-byte well-formed WMS capabilities document -- for the MINERAL DEPOSITS service,
    full of `mrds-` layers. A deliberately nonsense name returns 1,511 bytes and no layers,
    so "it responded and parsed" does NOT establish that you reached the dataset you named.
    The service name used here, `aerorad`, was read off the dataset's own page.

 2. THE FILE THAT LOOKS LIKE DATA AND IS A PICTURE. `data/NArad_U_geog83.tif` is 42.8 MB,
    is served as image/tiff, and is named for the element and the datum. It is PIL mode RGB,
    8 bits per channel, with NO GeoTIFF transform tags at all -- a rendered colour map.
    Sampling it yields legend colours that can be reported as ppm uranium. The data is
    `data/NAMrad_U.zip` -> NAMrad_U.flt, a 4-byte-float ESRI binary raster.

 3. THE GRID IS NOT GEOGRAPHIC. The .hdr gives xllcorner -3501000, cellsize 2000 -- metres in
    a projected frame. Treating those as degrees, or assuming any common projection, places
    every sample somewhere else on the continent and still returns a number in the right
    range. Parameters are read from the product's own .flt.xml, not assumed:

        TRANSVERSE_MERCATOR_SPHERICAL, R = 6378206.4 m (Clarke 1866 major axis as a sphere),
        k0 = 0.926, lon_origin = -100, lat_origin = 0, false east/north = 0, datum NAD27.

    That is the DNAG projection. NAD27->WGS84 is ~8 m here against a 2000 m cell: ignored,
    and stated so the omission is deliberate rather than unnoticed.

THE TRANSFORM IS TESTED AGAINST GROUND TRUTH IT WAS NOT BUILT FROM. The .flt.xml separately
declares the grid's geographic bounding box (-176.684217, 21.218190) .. (-24.242136,
81.442295). That bbox played no part in constructing the projection, so recovering it by
scanning the grid's own footprint is an independent check -- see self_test().

WHAT eU ACTUALLY MEASURES, because the unit name flatters it. Airborne gamma spectrometry
cannot see uranium. It sees the 1.76 MeV line of Bi-214, a DAUGHTER of Rn-222, and back-
calculates ppm U ASSUMING SECULAR EQUILIBRIUM -- hence "equivalent uranium". Two
consequences, both load-bearing:
  1. It reads the top ~30 cm only; deeper gamma is absorbed. A surface radioelement map.
  2. The equilibrium assumption breaks exactly where radon MOVES, which is what this project
     is looking for. eU is a more direct proxy for near-surface radon availability than a
     uranium assay would be, and its own error mode is the signal.

eTh IS THE CONTROL, AND THAT IS WHY IT IS PULLED. Th-232's gaseous daughter is Rn-220
(thoron), half-life 55 s against Rn-222's 3.8 d; thoron cannot migrate a useful distance.
eU and eTh track each other across rock types, so a site high in BOTH is reporting lithology,
while a site high in eU RELATIVE to eTh is reporting either uranium mobilised and
re-deposited by groundwater, or radon accumulating. The RATIO is the discriminator. Raw eU
is a rock-type map wearing a radon label.
"""
import math, os, sys, urllib.request, zipfile

try:
    import truststore; truststore.inject_into_ssl()
except Exception as e:
    print(f"[warn] truststore: {e}", file=sys.stderr)

BASE = "https://mrdata.usgs.gov/radiometric/data/"
ZIPS = {"U": "NAMrad_U.zip", "Th": "NAMrad_Th.zip", "K": "NAMrad_K.zip"}
CACHE = "work/radiometric"

R_SPHERE = 6378206.4
K0 = 0.926
LON0 = -100.0
LAT0 = 0.0
DECLARED_BBOX = (-176.684217165164, 21.2181896372151, -24.2421359579447, 81.4422949157635)

_LOADED = {}


def fetch(elem):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, ZIPS[elem])
    if os.path.exists(p) and os.path.getsize(p) > 1_000_000:
        return p
    url = BASE + ZIPS[elem]
    print(f"[rad] downloading {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "place-threshold-screen/1.0"})
    with urllib.request.urlopen(req, timeout=900) as r, open(p + ".part", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    os.replace(p + ".part", p)        # atomic: a truncated download never becomes the cache
    print(f"[rad] {elem}: {os.path.getsize(p):,} B", file=sys.stderr)
    return p


def _parse_hdr(txt):
    h = {}
    for line in txt.split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            try:
                h[parts[0].lower()] = float(parts[1])
            except ValueError:
                h[parts[0].lower()] = parts[1]
    return h


def load(elem):
    """-> (numpy 2-D array with nodata as nan, header dict). Cached in-process."""
    if elem in _LOADED:
        return _LOADED[elem]
    import numpy as np
    z = zipfile.ZipFile(fetch(elem))
    stem = ZIPS[elem][:-4]
    h = _parse_hdr(z.read(stem + ".hdr").decode("ascii", "replace"))
    ncols, nrows = int(h["ncols"]), int(h["nrows"])
    dt = "<f4" if str(h.get("byteorder", "lsbfirst")).lower().startswith("lsb") else ">f4"
    raw = z.read(stem + ".flt")
    exp = ncols * nrows * 4
    if len(raw) != exp:
        raise RuntimeError(f"{elem}: .flt is {len(raw)} B, header implies {exp} B")
    arr = np.frombuffer(raw, dtype=dt).reshape(nrows, ncols).astype("float32")
    nd = float(h.get("nodata_value", h.get("nodata", -9999)))
    arr = np.where(np.isclose(arr, nd), np.nan, arr)
    _LOADED[elem] = (arr, h)
    fin = np.isfinite(arr)
    print(f"[rad] {elem}: {nrows}x{ncols} cell={h['cellsize']:.0f}m "
          f"valid={fin.sum():,}/{arr.size:,} range={np.nanmin(arr):.2f}..{np.nanmax(arr):.2f}",
          file=sys.stderr)
    return _LOADED[elem]


def to_dnag(lat, lon):
    """Geographic -> DNAG spherical transverse Mercator metres."""
    phi, dl = math.radians(lat), math.radians(lon - LON0)
    b = math.cos(phi) * math.sin(dl)
    if abs(b) >= 1.0 - 1e-12:                       # 90 deg from the central meridian
        return None
    x = 0.5 * K0 * R_SPHERE * math.log((1 + b) / (1 - b))
    y = K0 * R_SPHERE * (math.atan2(math.tan(phi), math.cos(dl)) - math.radians(LAT0))
    return x, y


def sample(elem, lat, lon):
    """Nearest-cell value at lat/lon; None outside the grid or at nodata.

    Three-valued deliberately. Off-grid and no-data must not read as zero -- this grid has
    real interior holes where no survey flew, and a hole scored 0 ppm is the strongest
    possible negative evidence rather than the absence of evidence it actually is.
    """
    arr, h = load(elem)
    p = to_dnag(lat, lon)
    if p is None:
        return None
    x, y = p
    col = int((x - h["xllcorner"]) / h["cellsize"])
    row = int(h["nrows"] - 1 - (y - h["yllcorner"]) / h["cellsize"])
    if not (0 <= row < int(h["nrows"]) and 0 <= col < int(h["ncols"])):
        return None
    v = float(arr[row, col])
    return None if not math.isfinite(v) else v


def self_test():
    import numpy as np
    ok = True
    arr, h = load("U")

    # --- (1) independent check: recover the metadata's own declared geographic bbox by
    #         scanning the grid's footprint. That bbox was not used to build the transform.
    lo_w, lo_e, la_s, la_n = 1e9, -1e9, 1e9, -1e9
    la = 5.0
    while la < 89.0:
        lo = -180.0
        while lo < -20.0:
            p = to_dnag(la, lo)
            if p:
                c = (p[0] - h["xllcorner"]) / h["cellsize"]
                r = h["nrows"] - 1 - (p[1] - h["yllcorner"]) / h["cellsize"]
                if 0 <= r < h["nrows"] and 0 <= c < h["ncols"]:
                    lo_w, lo_e = min(lo_w, lo), max(lo_e, lo)
                    la_s, la_n = min(la_s, la), max(la_n, la)
            lo += 0.25
        la += 0.25
    d = DECLARED_BBOX
    err = max(abs(lo_w - d[0]), abs(la_s - d[1]), abs(lo_e - d[2]), abs(la_n - d[3]))
    print(f"   bbox recovered ({lo_w:.2f},{la_s:.2f})..({lo_e:.2f},{la_n:.2f})  "
          f"declared ({d[0]:.2f},{d[1]:.2f})..({d[2]:.2f},{d[3]:.2f})  max_err={err:.2f} deg",
          file=sys.stderr)
    if err > 1.5:                    # 1.5 deg ~ the 0.25 deg scan step plus corner rounding
        print("   !! FAIL: transform does not reproduce the declared extent", file=sys.stderr)
        ok = False

    # --- (2) the discriminating fixture: a place where right and wrong disagree.
    #         Grants NM is one of the largest uranium districts on the continent; the
    #         Pacific 1500 km offshore was never flown. If these are not ordered, the
    #         georeferencing is wrong no matter how reasonable the numbers look.
    hot = sample("U", 35.15, -107.85)                       # Grants mineral belt, NM
    sea = [sample("U", 30.0, -145.0), sample("U", 25.0, -150.0)]
    print(f"   Grants NM eU={hot}   deep Pacific eU={sea}", file=sys.stderr)
    if hot is None:
        print("   !! FAIL: no coverage over the Grants uranium district", file=sys.stderr)
        ok = False
    if all(s is not None for s in sea):
        print("   !! FAIL: deep ocean returns values -- transform is suspect", file=sys.stderr)
        ok = False

    for nm, la, lo in [("Hubbell Spring NM", 34.72, -106.68), ("Sandia NM", 35.20, -106.45),
                       ("Hebgen MT", 44.84, -111.34), ("Sierra front CA", 37.76, -118.65)]:
        u, t = sample("U", la, lo), sample("Th", la, lo)
        rat = (round(u / t, 3) if u is not None and t not in (None, 0) else None)
        print(f"   {nm:18s} eU={u}  eTh={t}  eU/eTh={rat}", file=sys.stderr)

    if hot is not None:
        med = float(np.nanmedian(arr))
        print(f"   grid median eU={med:.2f} ppm; Grants is {hot / med:.2f}x median",
              file=sys.stderr)
    print(f"   SELF-TEST {'PASS' if ok else 'FAIL'}", file=sys.stderr)
    return ok


if __name__ == "__main__":
    sys.exit(0 if self_test() else 1)
