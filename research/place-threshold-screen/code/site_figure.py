"""LAYERED SITE FIGURE — one multi-panel PNG per candidate site, built from measurements.

Clayton, Day 196: "Every site should have a starred coordinate for the site, as well as
layered imagery of the geophysical characteristics of the area and their surroundings."

Four panels, four independent geophysical layers, one star:

  A  shaded relief (USGS 3DEP)          — the landform the fault made
  B  bedrock geology (USGS SGMC2)        — the rock at and around the trace (P3's subject)
  C  isostatic residual gravity (USGS)   — basin vs. basement; where the crust is thin
  D  instrumental seismicity (USGS ANSS) — is the conduit currently moving

Every panel carries the SAME Quaternary fault linework (from the cached national dilatant
pull) and the SAME star, so the four are directly comparable by eye.

TWO RULES BUILT IN, both from this repo's own scar tissue:

 1. A LAYER THAT FAILED MUST LOOK FAILED. Each fetch writes PRESENT/ABSENT/ERROR with the
    byte count into a per-site manifest, and an absent layer is stamped across the panel in
    red rather than rendered as an innocent empty box. A blank panel that looks deliberate
    is the silent-failure mode this codebase keeps producing.

 2. NO CEREMONIAL GEOGRAPHY IS EVER PLOTTED. Public cadastral boundaries and published
    place names only — never a shrine, spring-as-passage, or ceremonial site, at any zoom,
    even where a published source names it. (Policy inherited verbatim from
    work/sandia_layers_registry.json; precedent is the Parsons/Goldfrank Isleta Paintings
    breach, deaccessioned by the APS in December 2023.)

Rasters are cached under work/figcache/ by (layer,bbox,size) so re-rendering is free and
the figure can be rebuilt offline once pulled.
"""
import hashlib
import json
import math
import os
import ssl
import sys
import time
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

CTX = ssl._create_unverified_context()
UA = {"User-Agent": "Mozilla/5.0"}
CACHE_DIR = "work/figcache"
QFAULTS = "work/qfaults_normal_national.geojson"

# Qfaults `age` -> colour + rank. Recency of rupture is P1; keep the ordering visible.
AGE_COLOR = {
    "historic": "#e8112d",
    "<150 years": "#e8112d",
    "latest quaternary": "#ff7a1a",
    "late quaternary": "#ffc61a",
    "middle and late quaternary": "#9bd44a",
    "quaternary": "#8fbcd4",
    "undifferentiated quaternary": "#8fbcd4",
}


def age_color(age):
    a = (age or "").strip().lower()
    for k, v in AGE_COLOR.items():
        if k in a:
            return v
    return "#b0b0b0"


def fetch(url, timeout=120, tag=""):
    """Pull bytes with the Norton-TLS / gov-WAF pattern. Cached on disk by URL hash."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()[:16]
    path = os.path.join(CACHE_DIR, f"{tag}_{key}.bin")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read(), "CACHED"
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, context=CTX, timeout=timeout).read()
    with open(path, "wb") as fh:
        fh.write(data)
    return data, "FETCHED"


def png_to_array(data):
    from io import BytesIO
    from PIL import Image
    return np.asarray(Image.open(BytesIO(data)).convert("RGBA"))


def bbox_for(lat, lon, half_km):
    """Square-on-the-ground bbox. Longitude degrees shrink with latitude; correct for it."""
    dlat = half_km / 111.32
    dlon = half_km / (111.32 * math.cos(math.radians(lat)))
    return (lon - dlon, lat - dlat, lon + dlon, lat + dlat)


# ---------------------------------------------------------------- layer fetchers
def layer_relief(bb, px):
    w, s, e, n = bb
    return ("https://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/"
            f"MapServer/export?bbox={w},{s},{e},{n}&bboxSR=4326&imageSR=4326"
            f"&size={px[0]},{px[1]}&format=png32&transparent=false&f=image")


def layer_topo(bb, px):
    w, s, e, n = bb
    return ("https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/"
            f"MapServer/export?bbox={w},{s},{e},{n}&bboxSR=4326&imageSR=4326"
            f"&size={px[0]},{px[1]}&format=png32&f=image")


def layer_geology(bb, px):
    w, s, e, n = bb
    return ("https://mrdata.usgs.gov/services/sgmc2?service=WMS&version=1.1.1&request=GetMap"
            f"&layers=sgmc2&styles=&SRS=EPSG:4326&bbox={w},{s},{e},{n}"
            f"&width={px[0]}&height={px[1]}&format=image/png&transparent=true")


GRAV_URL = "https://mrdata.usgs.gov/gravity/bouguer/bouguer.xyz.gz"
_GRAV = None


def gravity_points():
    """The national Bouguer anomaly point set (lon lat mGal), 728,657 stations.

    Deliberately NOT the WMS picture. The WMS renders the same field as ~4 km hard blocks
    with a categorical palette; at a 36 km panel that is nine cells of poster paint and it
    cannot be read as a gradient. Pulling the points lets the panel state a NUMBER —
    the anomaly range across the site box — which is the thing that distinguishes a
    basin-margin fault from an intra-basement one.
    """
    global _GRAV
    if _GRAV is None:
        import gzip
        os.makedirs(CACHE_DIR, exist_ok=True)
        p = os.path.join(CACHE_DIR, "bouguer.xyz.gz")
        if not os.path.exists(p):
            d, _ = fetch(GRAV_URL, timeout=300, tag="grav")
            with open(p, "wb") as fh:
                fh.write(d)
        lon, lat, val = [], [], []
        with gzip.open(p, "rt", errors="replace") as fh:
            for line in fh:
                try:
                    a, b, c = line.split()
                    lon.append(float(a)); lat.append(float(b)); val.append(float(c))
                except ValueError:
                    continue
        _GRAV = (np.array(lon), np.array(lat), np.array(val))
    return _GRAV


def gravity_field(bb, pad=0.35, nx=220):
    """Interpolate the station set onto a mesh over bb. Returns (grid, extent, stats)."""
    from scipy.interpolate import griddata
    w, s, e, n = bb
    lon, lat, val = gravity_points()
    m = ((lon > w - pad) & (lon < e + pad) & (lat > s - pad) & (lat < n + pad))
    if m.sum() < 12:
        raise RuntimeError(f"only {int(m.sum())} gravity stations in box — too sparse to grid")
    gx = np.linspace(w, e, nx)
    gy = np.linspace(s, n, nx)
    GX, GY = np.meshgrid(gx, gy)
    Z = griddata((lon[m], lat[m]), val[m], (GX, GY), method="linear")
    if np.all(np.isnan(Z)):
        raise RuntimeError("interpolation returned all-NaN")
    stats = {"n_stations_in_pad": int(m.sum()),
             "min_mGal": float(np.nanmin(Z)), "max_mGal": float(np.nanmax(Z)),
             "range_mGal": float(np.nanmax(Z) - np.nanmin(Z))}
    return Z, [w, e, s, n], stats


QUAKE_START = "1900-01-01"
LIMIT = 20000                      # FDSN's own maximum; anything at it is TRUNCATED


def quakes(bb, minmag=1.0, starttime=QUAKE_START):
    """ANSS/ComCat events in bb.

    `starttime` IS NOT OPTIONAL IN PRACTICE. The FDSN event service defaults to the
    **last 30 days** when starttime is omitted — it does not error, it does not warn, it
    returns a small honest-looking number. Day 197: the Sandia panel printed
    "ZERO catalogued events (a real, reportable result)" under a title reading
    "all years". Re-run with starttime=1900-01-01: **92 events, M1.6-4.7.** The zero was
    the instrument's default window, and the panel's own alarm branch dressed it as a
    finding. Every figure built before this line existed carries the 30-day window under
    an all-years caption.
    """
    w, s, e, n = bb
    q = (f"minlatitude={s}&maxlatitude={n}&minlongitude={w}&maxlongitude={e}"
         f"&starttime={starttime}")

    def count_at(mm):
        u = f"https://earthquake.usgs.gov/fdsnws/event/1/count?{q}&minmagnitude={mm}"
        d, _ = fetch(u, tag="eqc")
        return int(d.strip())

    # SECOND cap defect, found the same hour as the first: FDSN maxes at limit=20000 and
    # `orderby=magnitude` fills that quota with the LARGEST events. Four of the ten sites
    # returned exactly 20000 — a round number naming a cap (this report's own method
    # lesson #5), and the plotted set was a silent magnitude-truncation of the catalogue
    # under a caption reading "M>=1". So: ask /count first, and raise the floor until the
    # returned set is COMPLETE. The panel then states the floor it actually achieved.
    total = count_at(minmag)
    floor = minmag
    for cand in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        if cand < minmag:
            continue
        if count_at(cand) <= LIMIT:
            floor = cand
            break
    else:
        floor = 4.0
    n_at_floor = count_at(floor)

    url = (f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&{q}"
           f"&minmagnitude={floor}&limit={LIMIT}&orderby=magnitude")
    data, how = fetch(url, tag="eq")
    fc = json.loads(data)
    pts = []
    for f in fc.get("features", []):
        c = f["geometry"]["coordinates"]
        p = f["properties"]
        pts.append((c[0], c[1], p.get("mag") or 0, c[2] if len(c) > 2 else None,
                    p.get("time")))
    meta = {"minmag_requested": minmag, "minmag_plotted": floor,
            "n_total_at_requested_floor": total, "n_at_plotted_floor": n_at_floor,
            "n_returned": len(pts), "complete": len(pts) >= n_at_floor,
            "starttime": starttime, "limit": LIMIT}
    return pts, how, url, meta


# ---------------------------------------------------------------- fault linework
_FAULTS = None


def faults_in(bb):
    global _FAULTS
    if _FAULTS is None:
        _FAULTS = json.load(open(QFAULTS))["features"]
    w, s, e, n = bb
    out = []
    for ft in _FAULTS:
        g = ft.get("geometry") or {}
        parts = ([g["coordinates"]] if g.get("type") == "LineString"
                 else g.get("coordinates", []) if g.get("type") == "MultiLineString" else [])
        for part in parts:
            seg = [(c[0], c[1]) for c in part]
            if any(w <= x <= e and s <= y <= n for x, y in seg):
                out.append((seg, ft["properties"]))
    return out


def draw_faults(ax, bb, lw=1.6, label_names=False):
    seen = {}
    for seg, pr in faults_in(bb):
        xs = [p[0] for p in seg]
        ys = [p[1] for p in seg]
        c = age_color(pr.get("age"))
        ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", zorder=4,
                path_effects=None, alpha=0.95)
        ax.plot(xs, ys, color="black", lw=lw + 1.1, zorder=3, alpha=0.35)
        nm = (pr.get("fault_name") or "").strip()
        if nm and nm not in seen:
            seen[nm] = (xs[len(xs) // 2], ys[len(ys) // 2], c)
    if label_names:
        for nm, (x, y, c) in list(seen.items())[:9]:
            ax.annotate(nm, (x, y), fontsize=5.6, color="white", zorder=6,
                        bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none",
                                  alpha=0.55))
    return seen


def star(ax, lat, lon):
    ax.plot([lon], [lat], marker="*", ms=20, mfc="#fff23a", mec="black", mew=1.2,
            zorder=9, ls="none")
    ax.plot([lon], [lat], marker="*", ms=28, mfc="none", mec="#fff23a", mew=0.8,
            zorder=8, ls="none", alpha=0.5)


def scalebar(ax, bb, km):
    w, s, e, n = bb
    lat = (s + n) / 2
    dlon = km / (111.32 * math.cos(math.radians(lat)))
    x0 = w + (e - w) * 0.06
    y0 = s + (n - s) * 0.06
    ax.plot([x0, x0 + dlon], [y0, y0], color="black", lw=4.5, zorder=10,
            solid_capstyle="butt")
    ax.plot([x0, x0 + dlon], [y0, y0], color="white", lw=2.4, zorder=11,
            solid_capstyle="butt")
    ax.text(x0 + dlon / 2, y0 + (n - s) * 0.018, f"{km:g} km", ha="center", fontsize=7,
            zorder=11, color="black",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))


def panel(ax, title, bb, img=None, failed=None):
    w, s, e, n = bb
    if img is not None:
        ax.imshow(img, extent=[w, e, s, n], origin="upper", zorder=1, interpolation="bilinear")
    else:
        ax.set_facecolor("#f4f4f4")
    ax.set_xlim(w, e)
    ax.set_ylim(s, n)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=8.5, pad=3, loc="left")
    if failed:
        ax.text(0.5, 0.5, f"LAYER ABSENT\n{failed}", transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color="#c40000", weight="bold",
                zorder=20, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#c40000"))


# ---------------------------------------------------------------- the figure
def build(site, half_km=18.0, px=(760, 760), outdir="work/figures"):
    os.makedirs(outdir, exist_ok=True)
    lat, lon = site["lat"], site["lon"]
    bb = bbox_for(lat, lon, half_km)
    bb_ctx = bbox_for(lat, lon, half_km * 5)
    man = {"site": site.get("rank"), "name": site["fault_name"], "lat": lat, "lon": lon,
           "half_km": half_km, "bbox": bb, "layers": {}, "built": time.strftime("%F %T")}

    def grab(name, url, tag):
        try:
            d, how = fetch(url, tag=tag)
            if d[:4] != b"\x89PNG":
                man["layers"][name] = {"status": "ERROR", "detail": "not a PNG",
                                       "bytes": len(d), "url": url}
                return None, "server returned non-image"
            man["layers"][name] = {"status": "PRESENT", "bytes": len(d), "how": how,
                                   "url": url}
            return png_to_array(d), None
        except Exception as exc:                                    # noqa: BLE001
            man["layers"][name] = {"status": "ABSENT", "detail": f"{type(exc).__name__}: {exc}",
                                   "url": url}
            return None, f"{type(exc).__name__}"

    relief, e_rel = grab("relief", layer_relief(bb, px), "relief")
    geol, e_geo = grab("geology_sgmc2", layer_geology(bb, px), "geol")
    ctx_relief, _ = grab("context_relief", layer_relief(bb_ctx, px), "relief")

    try:
        gz, gext, gstats = gravity_field(bb)
        man["layers"]["gravity_bouguer"] = dict(status="PRESENT", source=GRAV_URL, **gstats)
        e_grv = None
    except Exception as exc:                                        # noqa: BLE001
        gz, gext, gstats, e_grv = None, None, {}, f"{type(exc).__name__}: {exc}"
        man["layers"]["gravity_bouguer"] = {"status": "ABSENT", "detail": e_grv,
                                            "source": GRAV_URL}

    try:
        eq, how, equrl, eqmeta = quakes(bb_ctx, 1.0)
        man["layers"]["seismicity"] = {"status": "PRESENT", "n": len(eq), "how": how,
                                       "url": equrl, "note": "context bbox, ANSS/ComCat",
                                       **eqmeta}
        e_eq = None
    except Exception as exc:                                        # noqa: BLE001
        eq, eqmeta, e_eq = [], {}, f"{type(exc).__name__}"
        man["layers"]["seismicity"] = {"status": "ABSENT", "detail": str(exc)}

    fig = plt.figure(figsize=(11.6, 10.2), dpi=170)
    gs = fig.add_gridspec(2, 2, hspace=0.055, wspace=0.10,
                          left=0.03, right=0.965, top=0.885, bottom=0.075)

    axA = fig.add_subplot(gs[0, 0])
    panel(axA, "A · shaded relief (USGS 3DEP) + Quaternary faults", bb, relief, e_rel)
    names = draw_faults(axA, bb, label_names=True)
    star(axA, lat, lon)
    scalebar(axA, bb, 5)

    axB = fig.add_subplot(gs[0, 1])
    panel(axB, "B · bedrock geology (USGS SGMC2)", bb, geol, e_geo)
    draw_faults(axB, bb, lw=1.2)
    star(axB, lat, lon)
    axB.text(0.015, 0.02, f"at trace: {site.get('at_point_term','?')} — "
                          f"{(site.get('at_point_unit') or '')[:58]}",
             transform=axB.transAxes, fontsize=6.4, va="bottom",
             bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#999", alpha=0.9))

    axC = fig.add_subplot(gs[1, 0])
    panel(axC, "C · Bouguer gravity anomaly (USGS, 728k stations) — basin fill vs basement",
          bb, None, e_grv)
    if gz is not None:
        im = axC.imshow(gz, extent=gext, origin="lower", cmap="RdYlBu_r", zorder=1,
                        interpolation="bilinear", alpha=0.92)
        cs = axC.contour(np.linspace(gext[0], gext[1], gz.shape[1]),
                         np.linspace(gext[2], gext[3], gz.shape[0]), gz,
                         levels=9, colors="black", linewidths=0.45, alpha=0.55, zorder=2)
        axC.clabel(cs, inline=True, fontsize=5.2, fmt="%.0f")
        cb = fig.colorbar(im, ax=axC, fraction=0.036, pad=0.012)
        cb.ax.tick_params(labelsize=6)
        cb.set_label("mGal", fontsize=6.5)
        axC.text(0.015, 0.02,
                 f"{gstats['min_mGal']:.0f} to {gstats['max_mGal']:.0f} mGal "
                 f"(range {gstats['range_mGal']:.0f}) · {gstats['n_stations_in_pad']} stations",
                 transform=axC.transAxes, fontsize=6.4, va="bottom",
                 bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#999", alpha=0.9))
    draw_faults(axC, bb, lw=1.2)
    star(axC, lat, lon)

    axD = fig.add_subplot(gs[1, 1])
    _fl = eqmeta.get("minmag_plotted", 1.0)
    panel(axD, f"D · instrumental seismicity M≥{_fl:g} within {half_km*5:.0f} km "
               f"(ANSS/ComCat, {QUAKE_START[:4]}–present)",
          bb_ctx, ctx_relief, e_eq)
    draw_faults(axD, bb_ctx, lw=0.7)
    if eq:
        xs = [p[0] for p in eq]
        ys = [p[1] for p in eq]
        ms = np.array([max(p[2], 0.1) for p in eq])
        axD.scatter(xs, ys, s=3 + (ms ** 2.6), c="#d0021b", alpha=0.42,
                    edgecolors="black", linewidths=0.25, zorder=5)
        _lab = (f"n = {len(eq)} events plotted, M{min(ms):.1f}–{max(ms):.1f}"
                f"  ·  {eqmeta.get('n_total_at_requested_floor','?')} in catalogue at M≥1"
                + ("" if eqmeta.get("complete", True) else "  ·  ⚠ TRUNCATED AT CAP"))
        axD.text(0.015, 0.02, _lab,
                 transform=axD.transAxes, fontsize=7, va="bottom",
                 bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#999", alpha=0.9))
    else:
        axD.text(0.5, 0.55, f"ZERO catalogued events M≥1 since {QUAKE_START[:4]}\n"
                            "— check network coverage before reading this as quiescence",
                 transform=axD.transAxes, ha="center", fontsize=9.5, color="#333")
    # the inner bbox, so panel D's relation to A-C is explicit
    w, s, e, n = bb
    axD.plot([w, e, e, w, w], [s, s, n, n, s], color="#fff23a", lw=1.4, zorder=7)
    star(axD, lat, lon)
    scalebar(axD, bb_ctx, 25)

    sc = site.get("score", {})
    rank = site.get("rank", "?")
    fig.suptitle(f"#{rank}  {site['fault_name']}"
                 + (f" — {site['section_name']}" if site.get("section_name") else ""),
                 fontsize=15, weight="bold", y=0.972, x=0.03, ha="left")
    fig.text(0.03, 0.939,
             f"★ {lat:.4f}, {lon:.4f}   ·   score {sc.get('total','?')} "
             f"(age {sc.get('age','?')} · rock {sc.get('tier','?')} · scale {sc.get('length','?')} "
             f"· junction {sc.get('junction','?')})   ·   last rupture: {site.get('age','?')} "
             f"·  {site.get('slip_rate_class','?')}  ·  {site.get('n_systems_15km','?')} dilatant "
             f"systems within 15 km", fontsize=8.6, ha="left")

    handles = [Line2D([], [], color=c, lw=3, label=k) for k, c in
               [("historic rupture", "#e8112d"), ("latest Quaternary", "#ff7a1a"),
                ("late Quaternary", "#ffc61a"), ("mid/late Quaternary", "#9bd44a"),
                ("Quaternary undiff.", "#8fbcd4")]]
    handles.append(Line2D([], [], marker="*", ms=13, mfc="#fff23a", mec="black", ls="none",
                          label="scored node (starred coordinate)"))
    fig.legend(handles=handles, loc="lower center", ncol=6, fontsize=7.4, frameon=False,
               bbox_to_anchor=(0.5, 0.038))
    fig.text(0.5, 0.012,
             "Rank is PHYSICS ONLY — no lore, sighting count, light-record or facility "
             "proximity enters the score. Faults: USGS Qfaults (dilatant subset). "
             "No ceremonial or sacred geography is plotted at any zoom.",
             fontsize=6.6, ha="center", color="#555")

    slug = "".join(ch if ch.isalnum() else "-" for ch in site["fault_name"]).strip("-").lower()
    out = os.path.join(outdir, f"{int(rank):02d}_{slug}.png" if str(rank).isdigit()
                       else f"{slug}.png")
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    man["output"] = out
    with open(out.replace(".png", ".layers.json"), "w") as fh:
        json.dump(man, fh, indent=1)
    bad = [k for k, v in man["layers"].items() if v["status"] != "PRESENT"]
    print(f"  -> {out}  layers ok={len(man['layers'])-len(bad)}/{len(man['layers'])}"
          + (f"  ⚠ FAILED: {bad}" if bad else ""), file=sys.stderr)
    return out, man


def top_sites(n=10, path="work/site_rank.json"):
    """One node per fault SYSTEM, best-scoring node kept. Systems, not duplicate vertices."""
    rows = json.load(open(path))["rows"]
    best = {}
    for r in rows:
        k = r["fault_name"]
        if k not in best or r["score"]["total"] > best[k]["score"]["total"]:
            best[k] = r
    ordered = sorted(best.values(), key=lambda r: -r["score"]["total"])[:n]
    for i, r in enumerate(ordered, 1):
        r["rank"] = i
    return ordered


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    only = sys.argv[2] if len(sys.argv) > 2 else None
    sites = top_sites(n)
    mans = []
    for s in sites:
        if only and only.lower() not in s["fault_name"].lower():
            continue
        print(f"[{s['rank']:>2}] {s['score']['total']:5.2f} {s['fault_name']}", file=sys.stderr)
        try:
            _, m = build(s)
            mans.append(m)
        except Exception as exc:                                    # noqa: BLE001
            print(f"  !! BUILD FAILED {type(exc).__name__}: {exc}", file=sys.stderr)
    with open("work/figures/_manifest.json", "w") as fh:
        json.dump({"n": len(mans), "sites": mans}, fh, indent=1)
