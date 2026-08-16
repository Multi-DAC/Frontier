"""ONE HTML DOSSIER — the frozen top ten, each as a small self-contained report.

Clayton, Day 197: "compile an HTML report of the top ten with their lore and coordinate
plot attached, geophysical layers mapped onto the plots ... so that each is a small report
of the history, lore, measurements, and mapping."

WHAT THIS DOES AND DOES NOT DO
------------------------------
It ASSEMBLES. Every number, tier and note in the output is read from a file that was
written before this script existed. **No new lookup of any kind is performed here** — not
for lore, not for history, not to "flesh out" a thin note.

That restriction is the point, not a shortcut. Report 10 §5 measured collection asymmetry:
winner notes already run 1.51x longer than decoy notes on H1. If I went back now and
enriched the ten winners' lore — the ten I know are winners, without touching their decoys —
I would manufacture exactly the bias that leg was built to detect, and the enrichment would
be invisible in the output because it would look like better research.

So the lore sections read verbatim from the frozen result files, decoy alongside winner,
and where a note is thin the dossier says the note is thin.

SOURCES (all local, all pre-existing):
  work/top10_frozen_100km.json    the site list the lore legs ran on
  work/stage5_join.json           per-fault leg statuses (PASS/FAIL/UNMEASURED)
  work/trace_lithology_full.json  8-vertex along-trace lithology
  work/lore_experiment_*.json     H1 anomalous-light leg (design + result)
  work/lore2_*.json               H2 Indigenous-narrative leg
  work/lore3_*.json               H3 settler-history leg
  work/blind_rescore_result.json  the nine-scorer blind consensus tiers
  work/figures_final/*.png        the four-panel plates + per-site layer manifests

Output: work/place-threshold-dossier.html  (self-contained; images inlined as JPEG)
"""
import base64
import html
import io
import json
import os
import sys

FIGDIR = "work/figures_final"
OUT = "work/place-threshold-dossier.html"
JPEG_WIDTH = 1700
JPEG_QUALITY = 82

TIER_DEFS = {
    "H1": [("T3", "named, place-specific, recurring record ≤25 km, non-listicle source"),
           ("T2", "recurring record ≤25 km, web-aggregator sources only"),
           ("T1", "isolated / one-off ≤25 km, or recurring at 25–60 km"),
           ("T0", "nothing under the protocol")],
    "H2": [("NT3", "place-specific anomaly-shaped narrative tied to THIS landform, ≤25 km, "
                   "in ethnography / a tribal source / academic or state-historical "
                   "treatment / a pre-1995 printed collection"),
           ("NT2", "same content ≤25 km but attested only in modern web-native retellings"),
           ("NT1", "anomaly-shaped narrative at region or nation level with no locus, "
                   "or a specific locus at 25–60 km"),
           ("NT0", "documented Indigenous association exists, nothing anomaly-shaped"),
           ("NX", "association itself not established under the protocol → EXCLUDED from "
                  "the ratio, reported as a coverage gap, never scored as a zero")],
    "H3": [("HT3", "named, place-specific incident or persistent local tradition ≤25 km in a "
                   "primary/archival source"),
           ("HT2", "same ≤25 km, web-secondary only"),
           ("HT1", "regional level, or 25–60 km"),
           ("HT0", "nothing under the protocol")],
}


def dms(v, pos, neg):
    h = pos if v >= 0 else neg
    v = abs(v)
    d = int(v)
    m = int((v - d) * 60)
    s = (v - d - m / 60) * 3600
    return f"{d}°{m:02d}′{s:04.1f}″{h}"


def img_b64(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > JPEG_WIDTH:
        im = im.resize((JPEG_WIDTH, round(im.height * JPEG_WIDTH / im.width)),
                       Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode(), buf.tell(), im.size


def e(x):
    return html.escape(str(x if x is not None else "—"))


def load():
    d = {}
    d["frozen"] = json.load(open("work/top10_frozen_100km.json"))
    d["join"] = {r["fault_name"]: r for r in json.load(open("work/stage5_join.json"))["rows"]}
    d["joinmeta"] = {k: v for k, v in json.load(open("work/stage5_join.json")).items()
                     if k != "rows"}
    d["lith"] = json.load(open("work/trace_lithology_full.json"))["done"]
    d["h1d"] = json.load(open("work/lore_experiment_design.json"))
    d["h1"] = json.load(open("work/lore_experiment_result.json"))
    d["h2"] = json.load(open("work/lore2_result.json"))
    d["h3"] = json.load(open("work/lore3_result.json"))
    d["blind"] = json.load(open("work/blind_rescore_result.json"))
    d["crossleg"] = json.load(open("work/lore_crossleg.json"))
    d["figman"] = json.load(open(os.path.join(FIGDIR, "_manifest.json")))
    return d


# ------------------------------------------------------------------ page furniture
CSS = """
:root{--ink:#16181d;--mut:#5d646f;--line:#d8dce3;--bg:#fbfbfc;--acc:#7a3d12;
      --warn:#8d2f18;--ok:#1f5c3d;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:16px/1.62 "Iowan Old Style",Georgia,"Times New Roman",serif;}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px 90px}
h1{font-size:2.15rem;line-height:1.18;margin:.2em 0 .1em;letter-spacing:-.01em}
h2{font-size:1.5rem;margin:2.4em 0 .5em;padding-bottom:.25em;border-bottom:2px solid var(--ink)}
h3{font-size:1.12rem;margin:1.6em 0 .4em}
.sub{color:var(--mut);font-size:.95rem}
code,.mono{font-family:"SF Mono",Consolas,"DejaVu Sans Mono",monospace;font-size:.88em}
header.top{padding:54px 0 8px;border-bottom:1px solid var(--line);margin-bottom:8px}
.banner{background:#fff5ee;border:1px solid #e6c3aa;border-left:5px solid var(--acc);
        padding:16px 20px;margin:26px 0;border-radius:3px}
.banner.warn{background:#fdf0ee;border-color:#e9bab0;border-left-color:var(--warn)}
.banner.ok{background:#eef6f1;border-color:#bcd9c9;border-left-color:var(--ok)}
.banner p{margin:.45em 0}
.banner b{letter-spacing:.01em}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.9rem}
th,td{text-align:left;padding:7px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;background:#f2f3f6;border-bottom:1.5px solid #c3c8d1}
td.num,th.num{text-align:right;font-family:"SF Mono",Consolas,monospace;font-size:.86em}
.site{background:var(--card);border:1px solid var(--line);border-radius:5px;
      padding:0 30px 30px;margin:38px 0;box-shadow:0 1px 3px rgba(20,22,28,.05)}
.site>.hd{margin:0 -30px 0;padding:20px 30px 16px;border-bottom:1px solid var(--line);
          background:#f7f8fa;border-radius:5px 5px 0 0}
.rk{display:inline-block;background:var(--ink);color:#fff;border-radius:3px;
    padding:2px 10px;font-weight:700;margin-right:10px;font-size:.95rem}
.coord{font-family:"SF Mono",Consolas,monospace;font-size:.92rem;color:var(--acc);
       font-weight:600}
figure{margin:22px 0 6px}
figure img{width:100%;height:auto;border:1px solid var(--line);border-radius:3px;
           display:block}
figcaption{color:var(--mut);font-size:.83rem;margin-top:8px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 34px}
@media(max-width:820px){.cols{grid-template-columns:1fr}}
.tier{display:inline-block;font-family:"SF Mono",Consolas,monospace;font-weight:700;
      border-radius:3px;padding:1px 8px;font-size:.86rem;border:1px solid}
.t0{background:#f1f2f4;border-color:#d2d6dd;color:#606874}
.t1{background:#fdf5e3;border-color:#e4d5a8;color:#7a5c12}
.t2{background:#fbeadd;border-color:#e6c3aa;color:#8a4a16}
.t3{background:#f8e0e0;border-color:#e0b0b0;color:#8d2f18}
.note{margin:.35em 0 1.1em;font-size:.94rem}
.who{color:var(--mut);font-size:.8rem;text-transform:uppercase;letter-spacing:.07em;
     font-weight:700;margin-top:1em}
.dl{color:var(--mut);font-size:.86rem}
footer{margin-top:60px;padding-top:22px;border-top:1px solid var(--line);
       color:var(--mut);font-size:.87rem}
.strike{text-decoration:line-through;color:var(--mut)}
"""


def tier_class(label):
    n = "".join(c for c in str(label) if c.isdigit())
    return "t" + (n if n in "0123" else "0")


def legs_table(row, lr, man):
    legs = row.get("legs", {})
    g = (man.get("layers", {}).get("gravity_bouguer") or {})
    q = (man.get("layers", {}).get("seismicity") or {})
    pts = lr.get("pts") or []
    hit = sum(1 for p in pts if p.get("term"))
    terms = {}
    for p in pts:
        terms[p.get("term") or "no qualifying unit"] = \
            terms.get(p.get("term") or "no qualifying unit", 0) + 1
    termstr = ", ".join(f"{v}× {k}" for k, v in sorted(terms.items(), key=lambda kv: -kv[1]))

    rows = [
        ("L1 · trace lithology <span class='dl'>(THE GATE)</span>",
         e(legs.get("L1_lithology", {}).get("status")),
         f"quartz_frac <b>{lr.get('quartz_frac')}</b> = {hit}/{len(pts)} vertices — {e(termstr)}"
         f"<br><span class='dl'>along {lr.get('traced_km','?')} km of trace, "
         f"{lr.get('segments','?')} segments · gate cuts at 0.25 · "
         f"sampling noise ±0.125 from vertex ordering</span>"),
        ("L2 · rupture age", e(legs.get("L2_age", {}).get("status")),
         e(legs.get("L2_age", {}).get("age"))),
        ("L3 · slip rate", e(legs.get("L3_slip", {}).get("status")),
         e(legs.get("L3_slip", {}).get("class"))),
        ("L4 · junction density", e(legs.get("L4_junction", {}).get("status")),
         f"{e(legs.get('L4_junction', {}).get('value'))} dilatant systems within 15 km"
         f"<br><span class='dl'>{e('; '.join(legs.get('L4_junction', {}).get('systems', [])))}"
         "</span>"),
        ("L6 · structural scale", e(legs.get("L6_length", {}).get("status")),
         f"{e(legs.get('L6_length', {}).get('value'))} km total mapped length"),
        ("L5 · GPS strain <span class='dl'>(annotates only, may promote, never demotes)</span>",
         e(legs.get("L5_strain", {}).get("status")),
         e(legs.get("L5_strain", {}).get("why") or legs.get("L5_strain", {}).get("value"))),
        ("Bouguer gravity <span class='dl'>(panel C)</span>", e(g.get("status")),
         (f"{g.get('min_mGal',0):.0f} to {g.get('max_mGal',0):.0f} mGal "
          f"(range {g.get('range_mGal',0):.0f}) from "
          f"{g.get('n_stations_in_pad','?')} stations in the padded box"
          if g.get("status") == "PRESENT" else e(g.get("detail")))),
        ("Instrumental seismicity <span class='dl'>(panel D)</span>", e(q.get("status")),
         ((f"<b>{q.get('n_total_at_requested_floor','?')}</b> catalogued events M≥1 since "
           f"1900 within {(man.get('half_km', 18) * 5):.0f} km"
           + (f"; plotted at M≥{q.get('minmag_plotted')} "
              f"({q.get('n_returned','?')} events) because the full M≥1 set exceeds the "
              f"20,000-record FDSN cap and would have been silently truncated"
              if (q.get("minmag_plotted") or 1.0) > 1.0
              else f"; all {q.get('n_returned','?')} plotted, no truncation"))
          if q.get("status") == "PRESENT" else e(q.get("detail")))),
    ]
    out = ["<table><tr><th style='width:31%'>leg</th><th style='width:12%'>status</th>"
           "<th>measured</th></tr>"]
    for a, b, c in rows:
        out.append(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>")
    out.append("</table>")
    return "".join(out)


def lore_block(d, name):
    def find(rows, key="winner"):
        for r in rows:
            if r.get(key) == name:
                return r
        return None

    blind = d["blind"]["consensus_tiers"]
    out = []
    for leg, key, wkey, dkey, label, bl in [
        ("H1", "h1", "winner_tier", "decoy_tier",
         "H1 · anomalous light / sound record", "L1"),
        ("H2", "h2", "winner_NT", "decoy_NT",
         "H2 · Indigenous place-narrative, anomaly-shaped", "L2"),
        ("H3", "h3", "winner_HT", "decoy_HT",
         "H3 · US / settler historical record", "L3"),
    ]:
        r = find(d[key]["rows"])
        if not r:
            continue
        pre = {"H1": "T", "H2": "NT", "H3": "HT"}[leg]
        wt, dt = r.get(wkey), r.get(dkey)
        wb = blind.get(bl, {}).get(name)
        db = blind.get(bl, {}).get(r.get("decoy"))
        out.append(f"<h3>{label}</h3>")
        out.append("<table><tr><th style='width:19%'>role</th><th style='width:11%'>site</th>"
                   "<th class='num' style='width:9%'>sighted</th>"
                   "<th class='num' style='width:9%'>blind</th><th>scored evidence, verbatim "
                   "from the frozen result file</th></tr>")
        out.append(
            f"<tr><td><b>this site</b></td><td>{e(name)}</td>"
            f"<td class='num'><span class='tier {tier_class(wt)}'>{pre}{e(wt)}</span></td>"
            f"<td class='num'><span class='tier {tier_class(wb)}'>"
            f"{pre + str(wb) if wb is not None else '—'}</span></td>"
            f"<td>{e(r.get('winner_note'))}</td></tr>")
        out.append(
            f"<tr><td>matched decoy<br><span class='dl'>observer-density matched, "
            f"≥100 km away, scored under the identical rubric</span></td>"
            f"<td>{e(r.get('decoy'))}</td>"
            f"<td class='num'><span class='tier {tier_class(dt)}'>{pre}{e(dt)}</span></td>"
            f"<td class='num'><span class='tier {tier_class(db)}'>"
            f"{pre + str(db) if db is not None else '—'}</span></td>"
            f"<td>{e(r.get('decoy_note'))}</td></tr>")
        out.append("</table>")
        if leg == "H3" and r.get("winner_nearest_km") is not None:
            out.append(f"<p class='dl'>Nearest census place — this site "
                       f"<b>{r['winner_nearest_km']} km</b>, decoy "
                       f"<b>{r.get('decoy_nearest_km')} km</b>. This is the unregistered "
                       f"confound of report 08 §4.1: across the ten pairs winners sit a "
                       f"median 7.5 km from a town against the decoys' 19.3 km, and all "
                       f"three rubrics band on distance.</p>")
    return "".join(out)


def build():
    d = load()
    figs = {m["name"]: m for m in d["figman"]["sites"]}
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>Place-Threshold Screen — the frozen ten</title>"
             f"<style>{CSS}</style></head><body><div class='wrap'>"]

    # ---------------------------------------------------------------- front matter
    parts.append("""
<header class='top'>
<h1>Place-Threshold Screen — the frozen ten</h1>
<p class='sub'>A CONUS-wide physics-only screen for dilatant Quaternary faults rupturing
quartz-rich crystalline rock, with the folklore held out until the physics was frozen —
then tested against it in three pre-registered experiments. One dossier per site:
starred coordinate, four mapped geophysical layers, every measured leg, and the lore
evidence exactly as it was scored.</p>
<p class='sub'>Clawd · carapace body · Day 197 · 2026-08-16 · companion to
<span class='mono'>reports/08-final-report.md</span> and
<span class='mono'>reports/10-blind-rescore.md</span></p>
</header>

<div class='banner warn'>
<p><b>Read the ordering as a list, not as a ranking.</b> The gate works and its two controls
land exactly where they were declared. The <i>scorer</i> does not: it separates the same two
controls by <b>0.19 in the wrong direction</b>. Every bit of demonstrated discriminating
power in this programme lives in the single binary lithology gate. These ten are ten members
of a 225-strong survivor population, printed in score order because withholding the order
would be worse — <b>not</b> ten sites shown to be better than the eleventh.</p>
<p><b>All three lore legs came back NOT SUPPORTED.</b> H1 lights +0.7, H2 Indigenous
narrative +0.3, H3 settler history +0.9, against a pre-declared bar of +1.0 full tier.
Re-scored blind by nine independent scorers who had never seen which site was which, H3
crosses at <i>exactly</i> +1.00 — which report 10 §4 treats as a fact about a bar written
too weakly, not about the hypothesis. The lore in this document is <b>evidence that was
scored</b>. It is not a result.</p>
</div>

<div class='banner'>
<p><b>Nothing here was looked up for this dossier.</b> Every tier, note, coordinate and
number is read from a file written before this document existed. Enriching only the ten
winners' lore — knowing they are the winners, without touching their decoys — would
manufacture the exact collection asymmetry report 10 §5 was built to measure, and it would
look like better research while doing it. Where a note is thin, the note is thin.</p>
<p><b>No ceremonial or sacred geography is plotted at any zoom</b>, in any panel, even where
a published source names it. Policy inherited verbatim from the Sandia layer registry.</p>
</div>
""")

    # verdict summary
    parts.append("<h2>The three lore legs at a glance</h2>")
    parts.append("<table><tr><th>leg</th><th>hypothesis</th><th class='num'>winners</th>"
                 "<th class='num'>decoys</th><th class='num'>separation</th>"
                 "<th class='num'>needed</th><th class='num'>blind</th>"
                 "<th>sign test</th><th>verdict</th></tr>")
    for leg, key, name, bl in [("H1", "h1", "anomalous light / sound record", "L1"),
                               ("H2", "h2", "Indigenous anomaly-shaped narrative", "L2"),
                               ("H3", "h3", "US / settler historical record", "L3")]:
        r = d[key]
        wm = r.get("winner_mean_tier", r.get("winner_mean_NT", r.get("winner_mean_HT")))
        dm = r.get("decoy_mean_tier", r.get("decoy_mean_NT", r.get("decoy_mean_HT")))
        st = r.get("sign_test", {})
        b = d["blind"]["legs"][bl]["BLIND_consensus"]
        v = r.get("verdict", r.get("verdict_PRIMARY_prereg", "?"))
        parts.append(
            f"<tr><td><b>{leg}</b></td><td>{e(name)}</td><td class='num'>{e(wm)}</td>"
            f"<td class='num'>{e(dm)}</td><td class='num'><b>{r['separation']:+.2f}</b></td>"
            f"<td class='num'>+{r['required']:.2f}</td>"
            f"<td class='num'>{b['separation']:+.2f}</td>"
            f"<td class='mono'>{e(st.get('favour_winner'))}/{e(st.get('non_tied'))} "
            f"p={e(st.get('p_two_sided'))}</td><td><b>{e(v)}</b></td></tr>")
    parts.append("</table>")
    parts.append("<p class='dl'>Blind column: consensus of three independent scorers per leg, "
                 "nine in total, disjoint across legs, working from label-stripped and shuffled "
                 "evidence packets with planted probe items to catch a scorer who did not read. "
                 "Blinding moved winners <i>down</i> on all three legs and cost ≤0.1 tiers — "
                 "the sighted searcher was the smallest of the four known instrument biases, "
                 "not the largest, which is the opposite of what report 08 §7.1 predicted.</p>")

    # tier ladders
    parts.append("<h2>The tier ladders, frozen before any lookup ran</h2><div class='cols'>")
    for leg, title in [("H1", "H1 · anomalous light / sound"),
                       ("H2", "H2 · Indigenous narrative"),
                       ("H3", "H3 · settler history")]:
        parts.append(f"<div><h3>{title}</h3><table>")
        for t, txt in TIER_DEFS[leg]:
            parts.append(f"<tr><td style='width:16%'><span class='tier {tier_class(t)}'>{t}"
                         f"</span></td><td>{e(txt)}</td></tr>")
        parts.append("</table></div>")
    parts.append("</div>")

    # list rule
    fz = d["frozen"]
    parts.append(f"""
<h2>How these ten were selected</h2>
<p>Population: <b>{fz['population']}</b> completely-measured survivors of the lithology gate,
out of 1,399 CONUS nodes thinned ≥40 km apart from the complete USGS Qfaults normal-fault
pull. Selection rule, frozen {e(fz['frozen'])}:</p>
<p class='mono' style='background:#f2f3f6;padding:12px 16px;border-radius:3px'>{e(fz['rule'])}</p>
<p><b>Lore status at selection: {e(fz['lore_status'])}.</b> Control on the selector itself:
{e(fz['control'])}.</p>
<div class='banner warn'><p><b>This list is not the table in report 08 §2, and the difference
matters.</b> That table is a plain score ordering with no spatial separation and the
lithology gate applied as a filter only. This list applies lithology as a fifth scoring
term and enforces 100 km between sites, so a cluster cannot occupy the whole list —
{e(len(fz['suppressed_by_separation']))} higher-scoring faults are suppressed by proximity
to a site already taken, including Red Canyon (0.770) and Hebgen (0.767), both within 14 km
of Madison. <b>This is the list the three lore experiments actually ran against</b>, so it is
the list that can carry lore, and it is the one printed here. Report 08 never prints it.</p>
</div>""")
    parts.append("<table><tr><th class='num'>#</th><th>fault</th><th class='num'>score</th>"
                 "<th class='num'>quartz</th><th class='num'>age</th><th class='num'>slip</th>"
                 "<th class='num'>junction</th><th class='num'>scale</th>"
                 "<th>starred coordinate</th></tr>")
    for s in fz["sites"]:
        c = s["components"]
        parts.append(
            f"<tr><td class='num'><b>{s['rank']}</b></td><td>{e(s['fault'])}</td>"
            f"<td class='num'>{s['score']:.4f}</td><td class='num'>{s['L1']}</td>"
            f"<td class='num'>{c['age']}</td><td class='num'>{c['slip']}</td>"
            f"<td class='num'>{c['junction']}</td><td class='num'>{c['length']}</td>"
            f"<td class='mono'>{s['lat']:.4f}, {s['lon']:.4f}</td></tr>")
    parts.append("</table>")
    parts.append("<h3>Suppressed by the 100 km separation rule</h3><table>"
                 "<tr><th>fault</th><th class='num'>score</th><th>suppressed by</th>"
                 "<th class='num'>km</th><th>would have ranked above</th></tr>")
    for s in fz["suppressed_by_separation"]:
        parts.append(f"<tr><td>{e(s['fault'])}</td><td class='num'>{s['score']:.4f}</td>"
                     f"<td>{e(s['suppressed_by'])}</td><td class='num'>{s['km']}</td>"
                     f"<td class='num'>#{e(s['would_have_ranked_above'])}</td></tr>")
    parts.append("</table>")

    # ---------------------------------------------------------------- the ten
    parts.append("<h2>The ten dossiers</h2>")
    total_b = 0
    for s in fz["sites"]:
        name = s["fault"]
        man = figs.get(name)
        row = d["join"].get(name, {})
        lr = d["lith"].get(name, {})
        h1row = next((r for r in d["h1"]["rows"] if r["winner"] == name), {})
        obs = None
        for p in d["h1d"]["pairs"]:
            if p["winner"]["fault"] == name:
                obs = p["winner"]["observer"]
        parts.append(f"<section class='site' id='site{s['rank']}'>")
        parts.append(
            f"<div class='hd'><h3 style='margin:0;font-size:1.45rem'>"
            f"<span class='rk'>#{s['rank']}</span>{e(name)}</h3>"
            f"<p style='margin:.45em 0 0'><span class='coord'>★ {s['lat']:.4f}, "
            f"{s['lon']:.4f}</span> &nbsp;<span class='dl'>"
            f"{dms(s['lat'],'N','S')} {dms(s['lon'],'E','W')}</span><br>"
            f"<span class='dl'>physics score {s['score']:.4f} · gate quartz_frac "
            f"{s['L1']} · "
            + (f"nearest census place {obs['nearest_km']} km ({e(obs['nearest'][0]['place'])}, "
               f"{e(obs['nearest'][0]['state'])}) · {obs['places_within_50km']} places "
               f"within 50 km" if obs else "observer data unavailable")
            + "</span></p></div>")

        if man and os.path.exists(man["output"]):
            b64, nb, size = img_b64(man["output"])
            total_b += nb
            parts.append(
                f"<figure><img alt='four-panel geophysical plate for {e(name)}' "
                f"src='data:image/jpeg;base64,{b64}'>"
                f"<figcaption><b>A</b> shaded relief (USGS 3DEP) with Quaternary fault "
                f"linework coloured by rupture age · <b>B</b> bedrock geology (USGS SGMC2) "
                f"with the along-trace lithology stated · <b>C</b> Bouguer gravity anomaly "
                f"interpolated from the 728,657-station USGS point set, not the WMS picture "
                f"· <b>D</b> ANSS/ComCat seismicity at 5× out, inner box drawn so the zoom "
                f"relation is explicit. Same star and same linework on all four. "
                f"Full-resolution PNG: <span class='mono'>"
                f"figures_final/{e(os.path.basename(man['output']))}</span></figcaption>"
                f"</figure>")
        else:
            parts.append("<div class='banner warn'><p><b>PLATE ABSENT</b> — the figure for "
                         "this site did not render. This box is here so that a missing "
                         "panel cannot read as a deliberate omission.</p></div>")

        parts.append("<h3>Measurements</h3>")
        parts.append(legs_table(row, lr, man or {}))
        parts.append("<h3>History, lore, and the decoy it was tested against</h3>")
        parts.append(lore_block(d, name))
        parts.append("</section>")

    # ---------------------------------------------------------------- back matter
    cl = d["crossleg"]
    parts.append(f"""
<h2>What the reader has to hold against all ten of these</h2>
<div class='banner warn'>
<p><b>1 · The nearest-town confound is live and unremoved.</b> Winners sit a median 7.5 km
from a census place; their decoys 19.3 km. All three rubrics band on distance. Restricting
to pairs where both members are inside 25 km — where distance cannot discriminate — H1's
separation falls from +0.7 to <b>+0.4</b>. The same five pairs survive that filter in all
three legs, so whatever the subset shows, it shows once.</p>
<p><b>2 · The three legs are not independent.</b> Spearman across all twenty sites runs
rho = 0.32–0.48, and it <i>survives</i> deleting the common scorer (blind panels: mean
0.387 → 0.361, largest pair rises to 0.600). The correlation is a property of the sites.
Three sub-threshold positives are therefore worth between one and three weak facts, and
closer to one.</p>
<p><b>3 · Landform-name salience deflates the decoys.</b> Winners carry famous names;
several decoys are "unnamed fault near X". <b>Five of twenty first passes went to the wrong
state</b> — Red Rock returned Red Lodge, Bull Mountain returned Boulder <i>Colorado</i>,
Sweetwater returned Wyoming, Thompson Valley returned Virginia, Round Valley returned
Mendocino. Both zero-scores in H3 are name conflations, not absences. Unmeasured.</p>
<p><b>4 · Every separation above is an upper bound</b>, because defects 1–3 all run in the
winners' favour and none of them has been removed.</p>
</div>

<h2>Two instrument defects found while building this dossier</h2>
<div class='banner'>
<p><b>Panel D was reading a 30-day window under a caption saying "all years".</b> The USGS
FDSN event service defaults <span class='mono'>starttime</span> to the last 30 days when the
parameter is omitted. It does not warn; it returns a small, honest-looking number. The Sandia
panel printed <i>"ZERO catalogued events (a real, reportable result)"</i> — the panel's own
alarm branch dressing an instrument default as a finding. Re-run with
<span class='mono'>starttime=1900-01-01</span>: <b>92 events, M1.6–4.7</b>, and the Socorro
cluster appears. Every seismicity panel built before this fix, including the ten committed
under report 07, carries the 30-day window under the all-years caption.</p>
<p><b>Then the fix hit the cap.</b> With the window opened, four of the ten returned
<b>exactly 20,000</b> events — FDSN's maximum, filled by <span class='mono'>orderby=magnitude
</span> with the largest events, i.e. a silent magnitude truncation under a caption reading
"M≥1". A returned count equal to a round number names a cap: this repo's own method lesson
#5, arriving a second time in the same hour. Now each panel asks the
<span class='mono'>/count</span> endpoint first and raises its magnitude floor until the
plotted set is <i>complete</i>, then states the floor it achieved. Round Valley sits in the
Long Valley caldera and carries <b>175,460</b> catalogued events at M≥1; it plots at M≥2.5.</p>
<p>Neither defect changes any ranking or any lore verdict — seismicity annotates and does not
score. Both are recorded because a figure that was wrong for a day was on its way to being
cited as though it never had been.</p>
</div>

<h2>Reproduction</h2>
<table>
<tr><th>artifact</th><th>built by</th></tr>
<tr><td class='mono'>data/top10_frozen_100km.json</td><td class='mono'>code/stage5_join.py</td></tr>
<tr><td class='mono'>data/trace_lithology_full.json</td><td class='mono'>code/trace_lithology_full.py</td></tr>
<tr><td class='mono'>data/lore_experiment_*.json</td><td class='mono'>code/lore_experiment_design.py → _result.py</td></tr>
<tr><td class='mono'>data/lore2_*.json · data/lore3_*.json</td><td class='mono'>code/lore2_*.py · code/lore3_*.py</td></tr>
<tr><td class='mono'>data/blind_rescore_result.json</td><td class='mono'>code/blind_rescore_design.py → _readout.py</td></tr>
<tr><td class='mono'>figures_final/*.png</td><td class='mono'>code/dossier_figures.py → site_figure.py</td></tr>
<tr><td class='mono'>this file</td><td class='mono'>code/dossier_html.py</td></tr>
</table>
<p class='dl'>Design freezes, all committed before their lookups ran:
<span class='mono'>e96efc3d</span> (H1) · <span class='mono'>b9ad2d1a</span> (H2) ·
<span class='mono'>f3a811fb</span> / <span class='mono'>9757807d</span> (H3) ·
<span class='mono'>5ae888dd</span> (blind re-score design, packets and probe gate, committed
before any scorer was dispatched).</p>

<footer>
<p><b>Nobody outside this body has read any of this.</b> The world's own data has spoken — the
screen ran, the controls landed, the nulls are real. A human and a non-Claude model have not.
Every verdict in this document is <b>PROVISIONAL</b> until that happens.</p>
<p>Data: USGS Qfaults (layer 21, complete national pull) · USGS SGMC2 bedrock geology ·
USGS 3DEP shaded relief · USGS Bouguer gravity station set (728,657 stations) ·
USGS ANSS/ComCat · US Census 2023 gazetteer · Macrostrat.
Repository <span class='mono'>Multi-DAC/Frontier</span>,
tree <span class='mono'>research/place-threshold-screen/</span>.</p>
<p>🦞🧍💜🔥♾️</p>
</footer>
</div></body></html>""")

    doc = "".join(parts)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"wrote {OUT}  {len(doc.encode('utf-8'))/1e6:.2f} MB "
          f"({total_b/1e6:.2f} MB of inlined imagery, {len(fz['sites'])} sites)",
          file=sys.stderr)
    return OUT


if __name__ == "__main__":
    build()
