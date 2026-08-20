#!/usr/bin/env python3
"""
build_report.py — assemble the public narrative report for Substack.

This supersedes build_substack.py for publication. The difference is the
*shape*, not the styling:

  build_substack.py   reflows dossier.html into a Substack-safe paste.
                      Structure = the internal dossier's structure: legs table,
                      ladders, ten dossiers, caveats. Correct and unreadable
                      for anyone who has not already read the working reports.

  build_report.py     a narrative report. What we were looking for -> how it was
                      built -> what was done to try to kill it -> what it found
                      -> the ten sites with their lore told as prose. The
                      internal reports become the sources, not the article.

Prose lives in report_text.py. Assembly lives here. Every quoted measurement in
the prose is asserted against dossier.html and the frozen JSON before anything
is written; a typo in the prose fails the build.

Outputs into substack/:
  POST.html         the whole report, one paste
  POST-part1.html   the report without the ten site dossiers (email-safe)
  POST-part2.html   the ten site dossiers alone
  assets/           every image on disk, numbered in paste order
  PASTE-NOTES.md    the checklist
"""

import base64
import json
import re
import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_substack import (  # noqa: E402
    BANNER,
    PAGE_CSS,
    classify,
    esc,
    inline,
    normalise_image,
    render_measurements,
    shoot_tables,
    text_of,
)
import report_text as T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dossier.html"
OUT = ROOT / "substack"
ASSETS = OUT / "assets"


# ------------------------------------------------------------------ extraction


def parse_sites(soup):
    """Pull per-site plate, measurement table and stated facts out of the dossier.

    Nothing here is retyped by hand — the measurement bullets are the dossier's
    own rendered table, reflowed. That is deliberate: a hand-copied number is a
    number with no gauge behind it.
    """
    sites = []
    for sec in soup.find_all("section", class_="site"):
        hd = sec.find("div", class_="hd")
        head = re.sub(r"\s+", " ", hd.get_text(" ", strip=True))
        m = re.match(r"#(\d+)\s+(.+?)\s+★", head)
        if not m:
            raise SystemExit(f"unparsable site header: {head[:80]}")
        rank, name = int(m.group(1)), m.group(2).strip()

        fig = sec.find("figure")
        img = fig.find("img") if fig else None
        if img is None:
            raise SystemExit(f"{name}: no plate")
        mm = re.match(r"data:image/(\w+);base64,(.+)$", img.get("src", ""), re.S)
        if not mm:
            raise SystemExit(f"{name}: plate is not a data URI")
        plate = base64.b64decode(mm.group(2))

        table = next((t for t in sec.find_all("table") if classify(t) == "measurements"), None)
        if table is None:
            raise SystemExit(f"{name}: no measurements table")

        rows = {}
        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all(["td", "th"])
            if len(tds) < 3:
                continue
            label = re.sub(r"\s*\(.*?\)\s*", " ", text_of(tds[0]).split("·")[0]).strip()
            rows[label] = text_of(tds[2])

        sites.append(
            dict(
                rank=rank,
                name=name,
                head=head,
                plate=plate,
                measurements=render_measurements(table),
                rows=rows,
                coord=re.search(r"★\s*(-?[\d.]+),\s*(-?[\d.]+)", head).groups(),
            )
        )
    if len(sites) != 10:
        raise SystemExit(f"expected 10 sites, parsed {len(sites)}")
    return {s["name"]: s for s in sites}


# ------------------------------------------------------- round-2 site assembly


def areas_from_candidate_list():
    """The deliverable's membership and order, read from the artefact that owns it.

    report_text.ROUND2 is authored; this is measured. They must agree or the build
    stops. The failure this prevents is the one that opened round 2: two frozen ten-
    lists on disk under near-identical names, both stamped the same day, disagreeing
    about three of ten sites, with no artefact stating which fork the article was on.
    """
    doc = json.loads((ROOT / "data" / "candidate_list.json").read_text(encoding="utf-8"))
    ranked = sorted(doc["areas"], key=lambda a: -a["best_score"])
    return doc, ranked


def check_membership(problems):
    """Assert report_text.ROUND2 against candidate_list.json, in order."""
    doc, ranked = areas_from_candidate_list()
    n = 0
    if len(T.ROUND2) != T.PROGRAMME["areas_shown"]:
        problems.append(f"ROUND2 has {len(T.ROUND2)} rows, PROGRAMME says "
                        f"{T.PROGRAMME['areas_shown']}")
    if len(doc["areas"]) != T.PROGRAMME["areas_total"]:
        problems.append(f"candidate_list has {len(doc['areas'])} areas, prose says "
                        f"{T.PROGRAMME['areas_total']}")
    for i, row in enumerate(T.ROUND2):
        n += 1
        if i >= len(ranked):
            problems.append(f"ROUND2 #{row['rank']} has no area at that rank")
            continue
        if row["rank"] != i + 1:
            problems.append(f"ROUND2 row {i} declares rank {row['rank']}")
        got = ranked[i]["best_scoring"]
        if got != row["fault"]:
            problems.append(f"rank {i + 1}: ROUND2 says '{row['fault']}', "
                            f"candidate_list says '{got}'")
        elif abs(ranked[i]["best_score"] - T.CHECK[row["fault"]]["score"]) > 5e-5:
            problems.append(f"{got}: CHECK score {T.CHECK[row['fault']]['score']}, "
                            f"candidate_list best_score {ranked[i]['best_score']}")
    for i, (name, score, _where) in enumerate(T.BELOW_LINE):
        n += 1
        a = ranked[len(T.ROUND2) + i]
        if a["best_scoring"] != name or abs(a["best_score"] - score) > 5e-5:
            problems.append(f"BELOW_LINE #{i}: prose says {name} {score}, "
                            f"candidate_list says {a['best_scoring']} {a['best_score']}")
    # the cut gap the prose names, recomputed rather than trusted
    n += 1
    gap = ranked[9]["best_score"] - ranked[10]["best_score"]
    if abs(gap - T.PROGRAMME["cut_gap"]) > 5e-5:
        problems.append(f"cut_gap: prose says {T.PROGRAMME['cut_gap']}, computed {gap:.4f}")
    n += 1
    hgap = ranked[0]["best_score"] - ranked[1]["best_score"]
    if abs(hgap - T.PROGRAMME["head_gap"]) > 5e-5:
        problems.append(f"head_gap: prose says {T.PROGRAMME['head_gap']}, computed {hgap:.4f}")
    return n


def check_superlatives(problems):
    """Every 'the most / the lowest / behind only X' claim about the ten, recomputed.

    Written after four such claims in one drafting pass turned out to be false —
    'the highest junction count', 'the second-longest', 'the lowest gate reading',
    'the most accessible by a wide margin'. Three of the four were ties and one had
    the wrong site entirely. A superlative reads exactly like a measurement and has
    no gauge behind it unless one is built, so this is the gauge.

    Each entry is (key, kind, sites) where `sites` is every fault that ties for the
    extreme. A claim naming a unique winner where there is a tie fails here.
    """
    ten = [r["fault"] for r in T.ROUND2]
    val = lambda k: {f: T.CHECK[f][k] for f in ten}  # noqa: E731
    claims = [
        # (label, key, extreme, the sites the prose says hold it)
        ("Madison length", "length_km", "max", ["Madison fault"]),
        ("Little Valley junctions", "junctions", "max", ["Little Valley fault"]),
        ("lowest gate reading", "q", "min",
         ["Antelope Valley fault zone", "Sand Springs Range fault"]),
        ("Centennial/Mosquito length rank 2", "length_km", "max2",
         ["Centennial fault", "Mosquito fault"]),
        ("Antelope/Round Valley junction rank 2", "junctions", "max2",
         ["Antelope Valley fault zone", "Round Valley fault"]),
    ]
    # "the one site in the ten whose fault ruptured in front of witnesses" / "the only
    # site whose fault ruptured historically" — said twice, in the Madison entry and in
    # the recommendation. It rests on Madison being the only 'historic' rupture age.
    n = 1
    historic = sorted(f for f in ten if "historic" in str(T.CHECK[f].get("age", "")).lower())
    if historic != ["Madison fault"]:
        problems.append(f"superlative 'only historic rupture': recomputed {historic}")

    for label, key, kind, want in claims:
        n += 1
        v = val(key)
        if kind in ("max", "min"):
            target = max(v.values()) if kind == "max" else min(v.values())
            got = sorted(f for f in v if v[f] == target)
        else:  # max2 — the joint holders of the second-highest distinct value
            second = sorted(set(v.values()), reverse=True)[1]
            got = sorted(f for f in v if v[f] == second)
        if got != sorted(want):
            problems.append(f"superlative '{label}': prose says {sorted(want)}, "
                            f"recomputed {got}")
    return n


def round2_site(row):
    """Build a site dict for an area with no round-1 dossier entry.

    Same shape parse_sites() returns, sourced from the round-2 artefacts instead:
    legs from stage5_join_rows.json, along-trace L1 detail from l1_detail_round2.json
    (measured through the same probe, both controls run first), gravity and seismicity
    from the plate's own layers manifest, plate from figures_round2/.
    """
    name = row["fault"]
    s5 = {r["fault_name"]: r
          for r in json.loads((ROOT / "data" / "stage5_join_rows.json")
                              .read_text(encoding="utf-8"))["rows"]}[name]
    l1 = json.loads((ROOT / "data" / "l1_detail_round2.json")
                    .read_text(encoding="utf-8"))["sites"][name]
    stem = f"{row['rank']:02d}_{slug(name)}"
    fig = ROOT / "figures_round2"
    png = fig / f"{stem}.png"
    lay = fig / f"{stem}.layers.json"
    for p in (png, lay):
        if not p.exists():
            raise SystemExit(f"{name}: missing round-2 artefact {p}")
    man = json.loads(lay.read_text(encoding="utf-8"))
    return dict(rank=row["rank"], name=name, plate=png.read_bytes(),
                legs=s5["legs"], l1=l1, layers=man["layers"],
                coord=(f"{s5['lat']:.4f}", f"{s5['lon']:.4f}"),
                measurements=render_round2_measurements(s5, l1, man["layers"]))


def render_round2_measurements(s5, l1, layers):
    """The per-site 'Measured:' bullets, in the same shape the dossier's eight print.

    One deliberate difference. The dossier writes `quartz_frac 0.875 = 7/8 vertices —
    7x granite`, where the vertex count and the named-rock list coincide because every
    named rock at those eight sites qualified. Both round-2 sites return a rhyolite:
    measured, named, volcanic, and NOT counted toward the gate. Printing the dossier's
    shorthand here would inflate the gate reading by a vertex under a label that says
    quartz_frac, so the qualifying and non-qualifying terms are printed separately.
    """
    legs = s5["legs"]
    q = " · ".join(f"{c}× {t}" for t, c in l1["terms_qualifying"])
    other = " · ".join(f"{c}× {t}" for t, c in l1["terms_not_qualifying"])
    g, sm = layers["gravity_bouguer"], layers["seismicity"]
    floor = (f"M≥{sm['minmag_plotted']:g}"
             + ("" if sm["minmag_plotted"] == sm["minmag_requested"]
                else f" (raised from M≥{sm['minmag_requested']:g} to stay inside the "
                     f"service's {sm['limit']:,}-record cap)"))
    items = [
        ("L1 · trace lithology <strong>(THE GATE)</strong>", legs["L1_lithology"]["status"],
         f"quartz_frac <b>{l1['quartz_frac']}</b> = {l1['vertices_qualifying']}/"
         f"{l1['n_pts']} qualifying vertices — {q}<br>"
         f"also sampled, not qualifying: {other}<br>"
         f"along {l1['traced_km']} km of trace, {l1['segments']} segments · gate cuts at "
         f"0.25 · sampling noise ±0.125 from vertex ordering"),
        ("L2 · rupture age", legs["L2_age"]["status"], esc(legs["L2_age"]["age"])),
        ("L3 · slip rate", legs["L3_slip"]["status"], esc(legs["L3_slip"]["class"])),
        ("L4 · junction density", legs["L4_junction"]["status"],
         f"{legs['L4_junction']['value']} dilatant systems within 15 km<br>"
         + esc("; ".join(legs["L4_junction"]["systems"]))),
        ("L6 · structural scale", legs["L6_length"]["status"],
         f"{legs['L6_length']['value']} km total mapped length"),
        ("L5 · GPS strain <em>(annotates only, may promote, never demotes)</em>",
         legs["L5_strain"]["status"], esc(legs["L5_strain"]["why"])),
        ("Bouguer gravity <em>(panel C)</em>", g["status"],
         f"{g['min_mGal']:.0f} to {g['max_mGal']:.0f} mGal (range "
         f"{g['range_mGal']:.0f}) from {g['n_stations_in_pad']:,} stations in the padded box"),
        ("Instrumental seismicity <em>(panel D)</em>", sm["status"],
         f"<b>{sm['n_at_plotted_floor']:,}</b> catalogued events {floor} since 1900 in the "
         f"context box; all plotted, no truncation"),
    ]
    return "<ul>" + "".join(
        f"<li><strong>{lab}</strong> — <strong>{st}</strong><br>{txt}</li>"
        for lab, st, txt in items) + "</ul>"


def verify(dossier_sites):
    """Assert every measurement quoted in report_text.py against its source.

    The lesson this implements: a count written into prose from a quick scan is
    a count with no controls. Run the check before the number sets.

    Round 2 splits the sourcing. The eight areas whose best-scoring member has a
    round-1 dossier entry are still checked against dossier.html. The two that do
    not are checked against stage5_join_rows.json, l1_detail_round2.json and their
    plate's own layers manifest. The SCORE for all ten is checked against
    candidate_list.json, which is the artefact the deliverable's membership and
    order come from — not against either frozen ten-list, because neither of those
    files is the deliverable and the two of them disagree.
    """
    problems = []
    checked = [0]

    def want(name, key, got, exp):
        checked[0] += 1
        if got is None:
            problems.append(f"{name}: {key} not found in dossier")
        elif abs(float(got) - float(exp)) > 1e-6:
            problems.append(f"{name}: {key} prose says {exp}, source says {got}")

    for row in T.ROUND2:
        n = row["fault"]
        c = T.CHECK.get(n)
        if c is None:
            problems.append(f"{n}: no CHECK entry in report_text.py")
            continue
        if n not in T.PLACE:
            problems.append(f"{n}: no PLACE entry")
        if n not in T.SITES:
            problems.append(f"{n}: no narrative in report_text.SITES")
        if row["plate"] == "round2":
            verify_round2(n, c, problems, checked)
            continue
        s = dossier_sites.get(n)
        if s is None:
            problems.append(f"{n}: ROUND2 says plate='dossier' but the dossier has no such site")
            continue
        h = s["head"]

        want(n, "score", grab(r"physics score ([\d.]+)", h), c["score"])
        want(n, "quartz_frac", grab(r"quartz_frac ([\d.]+)", h), c["q"])
        want(n, "nearest_km", grab(r"nearest census place ([\d.]+) km", h), c["near_km"])

        l1 = s["rows"].get("L1")
        want(n, "trace_km", grab(r"along ([\d.]+) km of trace", l1 or ""), c["trace_km"])
        want(n, "segments", grab(r"([\d]+) segments", l1 or ""), c["segments"])
        want(n, "junctions", grab(r"(\d+) dilatant systems", s["rows"].get("L4", "")), c["junctions"])
        want(n, "length_km", grab(r"(\d+) km total mapped length", s["rows"].get("L6", "")), c["length_km"])

        # optional keys — only where the prose quotes them
        if "vhit" in c:
            want(n, "vertices", grab(r"= (\d+)/8 vertices", l1 or ""), c["vhit"])
        for cnt, term in c.get("terms", []):
            checked[0] += 1
            if f"{cnt}× {term}" not in (l1 or ""):
                problems.append(f"{n}: prose says {cnt}x {term}; L1 reads '{(l1 or '')[:110]}'")
        for key, leg in (("age", "L2"), ("slip", "L3")):
            if key not in c:
                continue
            checked[0] += 1
            if c[key].lower() not in s["rows"].get(leg, "").lower():
                problems.append(f"{n}: prose {key} '{c[key]}' absent from {leg} '{s['rows'].get(leg)}'")
        if "strain" in c:
            want(n, "strain", grab(r"([\d.]+)", s["rows"].get("L5", "")), c["strain"])
        if "seis" in c:
            want(n, "seismicity", grab(r"([\d]+) catalogued events", s["rows"].get("Instrumental seismicity", "")), c["seis"])
        if "grav" in c:
            g = s["rows"].get("Bouguer gravity", "")
            gm = re.search(r"(-?\d+) to (-?\d+) mGal \(range (\d+)\)", g)
            if not gm:
                problems.append(f"{n}: gravity row unparsable: '{g[:80]}'")
            else:
                for i, label in enumerate(("grav_min", "grav_max", "grav_range")):
                    if c["grav"][i] is not None:
                        want(n, label, gm.group(i + 1), c["grav"][i])

    areas_table_html(problems)          # CHECK vs the join, on age and slip
    checked[0] += check_membership(problems)
    checked[0] += check_superlatives(problems)
    checked[0] += verify_tiers(problems)
    checked[0] += verify_programme(problems)

    if problems:
        print("VERIFICATION FAILED — nothing written:")
        for p in problems:
            print("  ·", p)
        raise SystemExit(1)
    print(f"verified {checked[0]} quoted values (site measurements, membership and order, "
          f"superlatives, tiers, programme headline figures) against dossier.html, "
          f"candidate_list.json, stage5_join_rows.json, l1_detail_round2.json, "
          f"figures_round2/*.layers.json, stage5_join_summary.json, lore*_result.json, "
          f"lore_crossleg.json and blind_rescore_result.json — clean")


def verify_round2(name, c, problems, checked):
    """The two areas with no dossier entry, against the artefacts they were built from."""
    s5 = {r["fault_name"]: r
          for r in json.loads((ROOT / "data" / "stage5_join_rows.json")
                              .read_text(encoding="utf-8"))["rows"]}.get(name)
    l1d = json.loads((ROOT / "data" / "l1_detail_round2.json").read_text(encoding="utf-8"))
    l1 = l1d["sites"].get(name)
    if s5 is None or l1 is None:
        problems.append(f"{name}: no stage5 row and/or no l1_detail_round2 entry")
        return
    if not l1d.get("controls_reproduce"):
        problems.append("l1_detail_round2.json: controls did not reproduce")

    stem = f"{[r['rank'] for r in T.ROUND2 if r['fault'] == name][0]:02d}_{slug(name)}"
    lay = ROOT / "figures_round2" / f"{stem}.layers.json"
    if not lay.exists():
        problems.append(f"{name}: no layers manifest at {lay}")
        return
    layers = json.loads(lay.read_text(encoding="utf-8"))["layers"]
    dead = [k for k, v in layers.items() if v.get("status") != "PRESENT"]
    if dead:
        problems.append(f"{name}: plate has non-PRESENT layers {dead}")

    pairs = [
        ("quartz_frac", c["q"], l1["quartz_frac"], 1e-9),
        ("quartz_frac (stage5)", c["q"], s5["legs"]["L1_lithology"]["value"], 1e-9),
        ("qualifying vertices", c["vhit"], l1["vertices_qualifying"], 0),
        ("trace_km", c["trace_km"], l1["traced_km"], 5e-2),
        ("segments", c["segments"], l1["segments"], 0),
        ("junctions", c["junctions"], s5["legs"]["L4_junction"]["value"], 0),
        ("length_km", c["length_km"], s5["legs"]["L6_length"]["value"], 0),
        ("seismicity", c["seis"], layers["seismicity"]["n_at_plotted_floor"], 0),
        # CHECK must carry the value the BULLET PRINTS, which is round(), not trunc().
        # At tol=1.0 a CHECK of -212 passed against a source of -212.98 while the bullet
        # rendered -213 — so the prose and the table beside it disagreed by one and the
        # gauge stayed green. Compare against the rendered value, exactly.
        ("grav_min", c["grav"][0], round(layers["gravity_bouguer"]["min_mGal"]), 0),
        ("grav_max", c["grav"][1], round(layers["gravity_bouguer"]["max_mGal"]), 0),
        ("grav_range", c["grav"][2], round(layers["gravity_bouguer"]["range_mGal"]), 0),
    ]
    # near_km is the one quoted number with no frozen artefact behind it — it is
    # recomputed here from the Census gazetteer through the same observer() the lore
    # design used, so the site header line is measured rather than remembered. The
    # free control is that the same call reproduces Madison's dossier value of 19.7.
    try:
        import lore_experiment_design as LED
        places = LED.load_places()
        obs = LED.observer(places, s5["lat"], s5["lon"])
        ctl = LED.observer(places, 44.792, -111.438)     # Madison, from top10_frozen
        pairs.append(("near_km", c["near_km"], obs["nearest_km"], 0.05))
        pairs.append(("near_km control (Madison)", T.CHECK["Madison fault"]["near_km"],
                      ctl["nearest_km"], 0.05))
    except FileNotFoundError:
        problems.append(f"{name}: near_km unverifiable — code/gaz_place.zip is absent, so "
                        f"the site header would print an unchecked number")

    for label, said, real, tol in pairs:
        checked[0] += 1
        if real is None:
            problems.append(f"{name} {label}: source value is null")
        elif abs(float(said) - float(real)) > tol:
            problems.append(f"{name} {label}: prose says {said}, source says {real}")

    for key, leg, field in (("age", "L2_age", "age"), ("slip", "L3_slip", "class")):
        checked[0] += 1
        if c[key].lower() not in str(s5["legs"][leg][field]).lower():
            problems.append(f"{name}: prose {key} '{c[key]}' absent from "
                            f"{leg} '{s5['legs'][leg][field]}'")

    for cnt, term in c["terms"]:
        checked[0] += 1
        if [term, cnt] not in [list(x) for x in l1["terms_qualifying"]]:
            problems.append(f"{name}: prose says {cnt}x {term} qualifying; probe reports "
                            f"{l1['terms_qualifying']}")
    for cnt, term in c.get("terms_other", []):
        checked[0] += 1
        if [term, cnt] not in [list(x) for x in l1["terms_not_qualifying"]]:
            problems.append(f"{name}: prose says {cnt}x {term} non-qualifying; probe reports "
                            f"{l1['terms_not_qualifying']}")

    # These two are printed WITH their history and WITHOUT a score, and the gauge
    # enforces both halves. Day 201: Clayton's ruling is that the record is anecdote
    # reinforcing a physics claim, not evidence for it, so a missing history made the
    # article incomplete rather than clean — the narrative is now REQUIRED. What stays
    # forbidden is a tier. A sighted, post-hoc score on a site already known to be a
    # winner is the contamination the pre-registration exists to prevent, and unlike
    # prose it would enter arithmetic that is frozen and already published.
    checked[0] += 1
    if not T.SITES[name].get("record", "").strip():
        problems.append(f"{name}: no `record` narrative. Round-2 areas are printed with their "
                        f"history for completeness; the blank was retired on Day 201")
    checked[0] += 1
    if name in T.TIERS:
        problems.append(f"{name}: has a TIERS entry but was never in the lore experiment")

    # The real contamination guard, now that prose is allowed: no tier token may appear
    # in an unscored area's record. verify_tiers() only walks sites that ARE in TIERS,
    # so without this a fabricated <code>T3</code> here would meet no checker at all.
    checked[0] += 1
    stray = re.findall(r"<code>(N?H?T\d)</code>", T.SITES[name].get("record", ""))
    if stray:
        problems.append(f"{name}: record prose writes tier token(s) {sorted(set(stray))}, but "
                        f"this area was never scored in any lore experiment")


def grab(pat, s):
    m = re.search(pat, s or "")
    return m.group(1) if m else None


LEGS = (
    ("H1", "lore_experiment_result.json", "winner_tier", "decoy_tier", "L1", "T"),
    ("H2", "lore2_result.json", "winner_NT", "decoy_NT", "L2", "NT"),
    ("H3", "lore3_result.json", "winner_HT", "decoy_HT", "L3", "HT"),
)


def verify_tiers(problems):
    """Check every tier in report_text against the frozen result files.

    Two passes, because they fail differently:
      1. the declared TIERS table against the JSON — catches a transcription slip
      2. every <code>T2</code>-style token in each site's prose against that
         site's declared set — catches a tier invented inside a sentence
    """
    blind = json.loads((ROOT / "data" / "blind_rescore_result.json").read_text(encoding="utf-8"))
    consensus = blind["consensus_tiers"]
    truth = {}
    for leg, fname, wk, dk, bl, _pre in LEGS:
        rows = json.loads((ROOT / "data" / fname).read_text(encoding="utf-8"))["rows"]
        for r in rows:
            w, d = r["winner"], r["decoy"]
            truth.setdefault(w, {})[leg] = (r[wk], consensus[bl].get(w), d, r[dk], consensus[bl].get(d))

    n = 0
    for site, dec in T.TIERS.items():
        if site not in truth:
            problems.append(f"{site}: no rows in the frozen lore results")
            continue
        for i, (leg, *_rest) in enumerate(LEGS):
            ws, wbl, decoy, ds, dbl = truth[site][leg]
            for label, said, real in (
                ("winner sighted", dec["w"][i], ws),
                ("winner blind", dec["wb"][i], wbl),
                ("decoy sighted", dec["d"][i], ds),
                ("decoy blind", dec["db"][i], dbl),
            ):
                n += 1
                if said != real:
                    problems.append(f"{site} {leg} {label}: table says {said}, frozen result says {real}")
            n += 1
            if dec["decoy"] != decoy:
                problems.append(f"{site} {leg}: table names decoy '{dec['decoy']}', frozen result says '{decoy}'")

        # every tier token written into the prose must be one this site actually has
        prose = T.SITES[site]["record"]
        for pre_i, (_leg, *_r, pre) in enumerate(LEGS):
            allowed = {dec["w"][pre_i], dec["wb"][pre_i], dec["d"][pre_i], dec["db"][pre_i]}
            pat = rf"<code>{pre}(\d)</code>"
            for tok in re.findall(pat, prose):
                n += 1
                if int(tok) not in allowed:
                    problems.append(
                        f"{site}: prose writes <code>{pre}{tok}</code>; this site's {pre} values "
                        f"are {sorted(allowed)}")
    return n


def verify_programme(problems):
    """Check the headline numbers in the framing and results prose.

    These are the claims the whole report rests on. They were previously
    carried only by having been read once, which is a stamp and not a gauge.
    """
    def j(name):
        return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))

    s5, xl = j("stage5_join_summary.json"), j("lore_crossleg.json")
    bl = j("blind_rescore_result.json")
    h3 = j("lore3_result.json")
    p, n = T.PROGRAMME, 0

    rho_s = xl["Q2_leg_independence"]["spearman_pairwise"]
    rho_b = {k: v["blind_rho"] for k, v in bl["cross_leg"].items()}
    town = h3["UNREGISTERED_CONFOUND_nearest_town_km"]
    q1, q3 = xl["Q1_distance_controlled"], xl["Q3_pooled_sign_test"]
    ctrl = s5["controls"]

    pairs = [
        ("population", p["population"], s5["population"], 0),
        ("gate_passed", p["gate_passed"], s5["gate"]["passed"], 0),
        ("gate_unmeasured", p["gate_unmeasured"], s5["gate"]["unmeasured"], 0),
        ("sandia_rank", p["sandia_rank"], ctrl["Sandia fault"]["rank_among_survivors"], 0),
        ("sandia_of", p["sandia_of"], ctrl["Sandia fault"]["of"], 0),
        ("sandia_score", p["sandia_score"], ctrl["Sandia fault"]["score"], 5e-4),
        ("hubbell_score", p["hubbell_score"], ctrl["Hubbell Spring fault"]["score"], 5e-4),
        ("control_gap", p["control_gap"],
         ctrl["Hubbell Spring fault"]["score"] - ctrl["Sandia fault"]["score"], 5e-3),
        ("h1_matched_sep", p["h1_matched_sep"], q1["H1_lights"]["matched_separation"], 1e-9),
        ("h1_matched_delta", p["h1_matched_delta"], q1["H1_lights"]["delta_from_matching"], 1e-9),
        ("town_median_winner", p["town_median_winner"], town["winner_median_km"], 1e-9),
        ("town_median_decoy", p["town_median_decoy"], town["decoy_median_km"], 1e-9),
        ("town_pairs_favouring", p["town_pairs_favouring"], town["sign_test_winner_closer"]["favour_winner"], 0),
        ("town_pairs_nontied", p["town_pairs_nontied"], town["sign_test_winner_closer"]["non_tied"], 0),
        ("rho_min", p["rho_min"], min(rho_s.values()), 1e-9),
        ("rho_max", p["rho_max"], max(rho_s.values()), 1e-9),
        ("rho_mean_sighted", p["rho_mean_sighted"], sum(rho_s.values()) / 3, 5e-4),
        ("rho_mean_blind", p["rho_mean_blind"], sum(rho_b.values()) / 3, 5e-4),
        ("rho_largest_blind", p["rho_largest_blind"], max(rho_b.values()), 1e-9),
        ("pooled_favour", p["pooled_favour"], q3["pooled"]["favour_winner"], 0),
        ("pooled_nontied", p["pooled_nontied"], q3["pooled"]["non_tied"], 0),
        ("pooled_p", p["pooled_p"], q3["pooled"]["p_two_sided"], 1e-9),
        ("pooled_sep", p["pooled_sep"], q3["pooled_separation"], 1e-9),
        ("collection_ratio_h1", p["collection_ratio_h1"], bl["collection_bias"]["L1"]["ratio"], 5e-3),
        ("h3_per_scorer_mean", p["h3_per_scorer_mean"], bl["legs"]["L3"]["per_scorer_separation_mean"], 1e-9),
    ]
    # -- round 2. Every key added to PROGRAMME for this build gets a row here; a
    # PROGRAMME key with no pair is an unchecked number that reads exactly like a
    # checked one.
    pc = j("positive_control.json")["A6i"]
    cl = json.loads((ROOT / "data" / "candidate_list.json").read_text(encoding="utf-8"))
    rows5 = {r["fault_name"]: r for r in j("stage5_join_rows.json")["rows"]}

    def five_term(name):
        r = rows5[name]
        c = r["components"]
        return (c["age"] + c["slip"] + c["junction"] + c["length"]
                + r["legs"]["L1_lithology"]["value"]) / 5

    s5f, hbf = five_term("Sandia fault"), five_term("Hubbell Spring fault")
    pairs += [
        ("ranked_complete", p["ranked_complete"], s5["ranked_complete"], 0),
        ("ranked_partial", p["ranked_partial"], s5["ranked_partial"], 0),
        ("areas_total", p["areas_total"], len(cl["areas"]), 0),
        ("areas_shown", p["areas_shown"], len(T.ROUND2), 0),
        ("head_n", p["head_n"], len(cl["tiers"]["HEAD"]), 0),
        ("band_n", p["band_n"], len(cl["tiers"]["BAND"]), 0),
        ("field_n", p["field_n"], cl["tiers"]["FIELD_n"], 0),
        ("a6_control_median", p["a6_control_median"], pc["control_median_km"], 5e-3),
        ("a6_null_median", p["a6_null_median"], pc["null_median_km"], 5e-3),
        ("a6_null_n", p["a6_null_n"], pc["null_n"], 0),
        ("a6_p", p["a6_p"], pc["mannwhitney"]["p"], 5e-5),
        ("a6_null_within10", p["a6_null_within10"], pc["base_rate"]["within_10km"]["null_frac"], 5e-5),
        ("a6_control_within10", p["a6_control_within10"], pc["base_rate"]["within_10km"]["control_frac"], 1e-9),
        ("a6_n_controls", p["a6_n_controls"], sum(1 for r in j("positive_control.json")["A6i"]["rows"]
                                                  if r["id"].startswith("PC")), 0),
        ("sandia_five", p["sandia_five"], s5f, 5e-4),
        ("hubbell_five", p["hubbell_five"], hbf, 5e-4),
        ("five_term_gap", p["five_term_gap"], s5f - hbf, 5e-4),
        # one L1 vertex = 1/8 of one of five equal terms
        ("vertex_step", p["vertex_step"], 1 / 8 / 5, 1e-9),
    ]

    for i, leg in enumerate(("L1", "L2", "L3")):
        pairs.append((f"sep_sighted[{leg}]", p["sep_sighted"][i], bl["legs"][leg]["SIGHTED"]["separation"], 1e-9))
        pairs.append((f"sep_blind[{leg}]", p["sep_blind"][i], bl["legs"][leg]["BLIND_consensus"]["separation"], 1e-9))
    for _leg, fname, *_ in LEGS:
        pairs.append((f"bar ({fname})", p["bar"], j(fname)["required"], 1e-9))

    # META-GAUGE. Every key in PROGRAMME must appear in a pair above. Adding a
    # headline number to the prose and forgetting to wire its check produces a
    # number that reads exactly like a checked one and is not — which is what
    # happened on this build's first pass, to eighteen keys at once.
    # Checked in check_membership() instead, against candidate_list.json, because
    # they are recomputed from the area ranking rather than read from a summary.
    # Named here so the exemption is visible rather than implicit.
    ELSEWHERE = {"cut_gap", "head_gap"}
    covered = {lab.split("[")[0].split(" ")[0] for lab, *_ in pairs} | ELSEWHERE
    orphan = sorted(k for k in p if k not in covered)
    n += 1
    if orphan:
        problems.append(f"PROGRAMME keys with no build-time check: {orphan}")

    for label, said, real, tol in pairs:
        n += 1
        if real is None:
            problems.append(f"programme {label}: source value is null")
        elif abs(float(said) - float(real)) > tol:
            problems.append(f"programme {label}: prose says {said}, source says {real}")
    return n


def find_tables(soup):
    """Tables lifted from the dossier where the grid IS the argument, keyed by slug.

    Round 2 takes only the lore-legs table from here. The old `ten` and `suppressed`
    tables are NOT reused: both describe the 100 km fault list, which is not the
    deliverable any more, and scraping them was how the article's membership came to
    be coupled to a stale artefact in the first place. The areas table is now built
    from candidate_list.json by areas_table_html().
    """
    jobs, seen = [], {}
    captions = {"legs": "The three pre-registered lore experiments, sighted and blind"}
    for t in soup.find_all("table"):
        k = classify(t)
        if k.startswith("img:"):
            slug = k.split(":", 1)[1]
            if slug not in captions or slug in seen:
                continue
            seen[slug] = True
            jobs.append((slug, captions[slug], str(t)))
    missing = set(captions) - seen.keys()
    if missing:
        raise SystemExit(f"tables not found in dossier: {sorted(missing)}")
    return jobs


def areas_table_html(problems=None):
    """The ten areas, built from candidate_list.json — the artefact that owns them.

    Rupture age and slip class come from stage5_join_rows.json, NOT from CHECK.
    CHECK carries them only where a site's prose happens to quote them, so driving
    the table off it printed an em-dash in three of ten age cells and three of ten
    slip cells — a blank that reads as 'not measured' for a leg every one of these
    faults passed. Where CHECK does carry the value it is asserted to agree.
    """
    _doc, ranked = areas_from_candidate_list()
    by_best = {a["best_scoring"]: a for a in ranked}
    legs = {r["fault_name"]: r["legs"]
            for r in json.loads((ROOT / "data" / "stage5_join_rows.json")
                                .read_text(encoding="utf-8"))["rows"]}
    head = ("<tr><th>#</th><th>area</th><th>best-scoring structure</th><th>score</th>"
            "<th>gate</th><th>rupture age</th><th>slip mm/yr</th><th>junctions</th>"
            "<th>length km</th><th>extent km</th><th>structures</th></tr>")
    rows = []
    for r in T.ROUND2:
        c, a, lg = T.CHECK[r["fault"]], by_best[r["fault"]], legs[r["fault"]]
        age = lg["L2_age"]["age"]
        slip = re.sub(r"\s*mm/yr$", "", lg["L3_slip"]["class"])
        if problems is not None:
            for key, val in (("age", age), ("slip", slip)):
                if key in c and c[key].lower() not in val.lower():
                    problems.append(f"areas table {r['fault']}: CHECK {key} '{c[key]}' "
                                    f"disagrees with the join's '{val}'")
        rows.append(
            f"<tr><td>{r['rank']}</td><td>{esc(r['area'])}</td>"
            f"<td>{esc(r['fault'])}</td><td>{c['score']:.4f}</td>"
            f"<td>{c['q']}</td><td>{esc(age)}</td><td>{esc(slip)}</td>"
            f"<td>{c['junctions']}</td><td>{c['length_km']}</td>"
            f"<td>{a['extent_km']:.1f}</td><td>{a['n_members']}</td></tr>")
    return f"<table>{head}{''.join(rows)}</table>"


def below_line_html():
    """The three areas immediately under the cut, printed rather than dropped."""
    _doc, ranked = areas_from_candidate_list()
    by_best = {a["best_scoring"]: a for a in ranked}
    head = "<tr><th>#</th><th>structure</th><th>where</th><th>score</th><th>below #10 by</th></tr>"
    tenth = T.CHECK[T.ROUND2[-1]["fault"]]["score"]
    rows = "".join(
        f"<tr><td>{11 + i}</td><td>{esc(name)}</td><td>{esc(where)}</td>"
        f"<td>{score:.4f}</td><td>{tenth - by_best[name]['best_score']:.4f}</td></tr>"
        for i, (name, score, where) in enumerate(T.BELOW_LINE))
    return f"<table>{head}{rows}</table>"


# ------------------------------------------------------------------- assembly


class Doc:
    """Collects Substack-safe blocks and the images they reference."""

    def __init__(self):
        self.blocks = []
        self.images = []  # (fname, bytes, alt)

    def add(self, html):
        if html and html.strip():
            self.blocks.append(html.strip())

    def h2(self, s):
        self.add(f"<h2>{s}</h2>")

    def h3(self, s):
        self.add(f"<h3>{s}</h3>")

    def rule(self):
        self.add("<hr>")

    def image(self, data, alt, caption=""):
        data, mime = normalise_image(data, "png")
        fname = f"{len(self.images) + 1:02d}_{slug(alt)}.jpg"
        self.images.append((fname, data, alt))
        b64 = base64.b64encode(data).decode()
        self.add(f'<p><img alt="{esc(alt)}" src="data:image/{mime};base64,{b64}"></p>')
        if caption:
            self.add(f"<p><em>{caption}</em></p>")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:44]


def head_doc(shots):
    d = Doc()
    d.add(f"<p><em>{T.DECK}</em></p>")
    d.rule()

    d.h2("The observation this starts from")
    d.add(T.OPENING)

    d.h2("What we were looking for")
    d.add(T.WHAT_WE_LOOKED_FOR)

    d.h2("The one decision that makes it a test")
    d.add(T.THE_DESIGN_DECISION)

    d.rule()
    d.h2("How the screen was built")
    d.add(T.METHOD)

    d.h2("How it was controlled")
    d.add(T.RIGOUR)

    d.rule()
    d.h2("What the screen found")
    d.add(T.RESULT_GATE)

    d.h2("How to read the list")
    d.add(T.RESULT_RANKER)

    d.h2("What is already written about this ground")
    d.add(T.RESULT_LORE_INTRO)
    d.image(shots["legs"], "the three lore legs at a glance",
            "All three legs, sighted and blind, against their pre-declared bar of +1.0 tiers.")
    d.add(T.RESULT_LORE_AFTER)

    d.h2("What this report claims")
    d.add(T.VERDICT)
    return d


def ten_table_doc(shots):
    d = Doc()
    d.rule()
    d.h2("The ten areas")
    d.add(
        "<p>Selected on rock, rupture age, slip rate, junction density and structural scale, "
        "every one of those measured from institutional records over a complete national "
        "population, before a single piece of folklore was looked up. Each area is a cluster of "
        "qualifying structures at 50 km, scored by its best-scoring member; <em>extent</em> is "
        "how far across the area runs and <em>structures</em> is how many qualifying faults it "
        "contains.</p>"
    )
    d.image(shots["areas"], "the ten areas with their measured terms",
            "The ten areas, with the measured quantities that selected them.")
    d.h3("And the three immediately below the cut")
    d.add(
        "<p>The gap between tenth and eleventh is 0.0044 — about a fifth of the smallest step "
        "this instrument takes. A cut that fine runs through the middle of a band rather than "
        "between two tiers, so the next three are printed by name instead of disappearing.</p>"
    )
    d.image(shots["below"], "the three areas immediately below the cut",
            "Printed rather than dropped: the three areas immediately under the tenth line.")
    return d


def sites_doc(sites):
    d = Doc()
    d.add(T.TEN_INTRO)
    for s in sites:
        n = s["name"]
        row = next(r for r in T.ROUND2 if r["fault"] == n)
        narrative = T.SITES[n]
        d.rule()
        d.h2(f"#{s['rank']} · {row['area']}")
        lat, lon = s["coord"]
        d.add(
            f"<p><strong>{esc(T.PLACE[n])}</strong> · <code>{lat}, {lon}</code> · "
            f"best-scoring structure <strong>{esc(n)}</strong> · score "
            f"{T.CHECK[n]['score']:.4f} · gate reading <code>{T.CHECK[n]['q']}</code> · "
            f"nearest census place {T.CHECK[n]['near_km']} km</p>"
        )
        d.image(s["plate"], f"four-panel geophysical plate for {n}",
                f"{n}. <strong>A</strong> relief with Quaternary traces coloured by rupture age · "
                f"<strong>B</strong> bedrock geology · <strong>C</strong> Bouguer gravity · "
                f"<strong>D</strong> regional context with instrumental seismicity since 1900.")
        d.h3("The ground")
        d.add(narrative["ground"])
        d.add("<p><strong>Measured:</strong></p>")
        d.add(s["measurements"])
        d.h3("The record")
        if n not in T.TIERS:
            # Added this round, so there is history but no score. Say so once, here,
            # rather than repeating the caveat inside the narrative.
            d.add(
                "<p><em>Added to the deliverable this round, after the three lore experiments "
                "were frozen and run. The history below is printed for completeness and carries "
                "no tier and no score — it took no part in any experiment and moved nothing on "
                "the list.</em></p>"
            )
        d.add(narrative["record"])
    return d


def tail_doc():
    d = Doc()
    d.rule()
    d.h2("Where we would point an instrument")
    d.add(T.WHAT_SURVIVES)

    d.rule()
    d.h2("Why a list and not an argument")
    d.add(T.CLOSING)

    d.h2("Provenance and standing")
    d.add(T.PROVENANCE)
    d.add("<p>🦞🧍💜🔥♾️</p>")
    return d


def page(blocks):
    body = "\n".join(blocks)
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Place-Threshold Screen — Substack paste copy</title>"
        f"<style>{PAGE_CSS}</style></head><body>{BANNER}"
        f"<div class='paste'>{body}</div></body></html>"
    )


def wordcount(blocks):
    return len(re.sub(r"<[^>]+>", " ", "\n".join(blocks)).split())


def textbytes(html):
    return len(re.sub(r'src="data:[^"]+"', 'src="X"', html).encode())


# ----------------------------------------------------------------------- main


NOTES = """# Substack paste — {title}

Built by `code/build_report.py` from `dossier.html` + `code/report_text.py`.
Rebuild any time either changes; **nothing in `substack/` is hand-edited.**

This is the *narrative* build. `code/build_substack.py` still exists and still
works — it reflows the internal dossier one-for-one. That one is the internal
artifact. This one is the article.

## Do this

1. Open the file you want in a browser (double-click it).
2. Click anywhere below the orange line, **Ctrl-A**, **Ctrl-C**.
3. New Substack post → click in the body → **Ctrl-V**.
4. **Check the images came through.** If any are missing: Ctrl-Z, paste again.
   The first paste dropping images is known behaviour (Day 139, *The Curvature
   of Good and Evil*); the second paste usually carries them.
5. Anything still missing → drag it in from `substack/assets/`, numbered in
   paste order.

## Three builds — pick one

| file | words | text KB | images | what |
|---|---|---|---|---|
| `POST.html` | {w_all:,} | {kb_all:.0f} | {i_all} | the whole report, one post |
| `POST-part1.html` | {w_p1:,} | {kb_p1:.0f} | {i_p1} | the report **without** the ten site dossiers |
| `POST-part2.html` | {w_p2:,} | {kb_p2:.0f} | {i_p2} | the ten site dossiers alone |

**Gmail clips any email over 102 KB** with a *"[Message clipped]"* link. The web
version is never affected. `POST.html` goes over that; part 1 on its own does
not. So:

- **One post** → paste `POST.html`. Email readers get a clip link.
- **Two posts** → paste `POST-part1.html` today and `POST-part2.html` as the
  companion field guide. Part 1 already ends with a pointer to it, and part 2
  opens with a two-sentence recap so it stands alone.

## The title field — do NOT paste this, type it

**Title:** {title}

**Subtitle** — pick one:

- Ten areas in the western United States where the physics of anomalous places is
  most strongly expressed — screened from every mapped normal fault in the lower
  forty-eight, with the folklore held out of the arithmetic.
- A continental screen for the ground under the lights: 110,356 mapped sections,
  1,399 nodes, 242 through the gate, thirteen areas, ten printed.

If you publish it as two, part 2's title: **{title} — the ten areas**.

## Round 2 — what changed in this build

The deliverable is **ten AREAS at the 50 km separation scale**, driven from
`data/candidate_list.json`. The round-1 article shipped ten *faults* at 100 km,
scraped out of `dossier.html` — which coupled the article's membership to a stale
artefact. It no longer does. Two areas are new (Centennial Valley, Antelope
Valley) and two dropped below the cut (Bear River, Teton).

Both new areas were measured through the same along-trace probe as the other
eight, with both declared controls run first and required to reproduce exactly
(`code/l1_detail_round2.py`), and their plates are built by the same
`site_figure.build()` as the rest (`code/plates_round2.py`). Neither has a lore
entry: they entered after the three experiments were frozen, and a sighted
post-hoc lookup is the contamination the pre-registration exists to prevent.

Register: confounds and controls are stated **once**, in the method section, and
the rest of the article presents findings.

## What is checked at build time

Every measurement quoted in the prose — score, gate reading, trace length,
segment count, junction count, mapped length, nearest place — against
`dossier.html` for the eight round-1 areas and against
`stage5_join_rows.json` + `l1_detail_round2.json` + the plate's own layers
manifest for the two round-2 ones. Plus: **membership and order of the ten**
against `candidate_list.json`, the cut gap and head gap recomputed, every
superlative in the prose recomputed across the ten, all lore tiers against the
frozen result files, and the headline programme figures against the summaries.
A typo fails the build rather than shipping.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
{assets}
"""

PART1_TAILNOTE = (
    "<hr><p><em><strong>The ten areas themselves — plates, measurements and what the record says "
    "at each one — are in the companion piece.</strong> This half is the question, the method and "
    "the result; that half is the field guide.</em></p>"
)

PART2_HEAD = (
    "<p><em>This is the companion half of <strong>{title}</strong>, which sets out the conjecture "
    "under test, how the continental screen was built over every mapped normal fault in the lower "
    "forty-eight, and what it controls for. The short version: 1,399 nodes measured along-trace, "
    "242 through the gate, both declared controls exact, thirteen areas at the 50 km scale, ten "
    "printed here. Position one is resolved; the rest of the order is not asserted. Every area is "
    "on this list because of what the rock does there, not because anyone saw anything.</em></p>"
)


def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")

    dossier_sites = parse_sites(soup)
    verify(dossier_sites)

    sites = []
    for row in T.ROUND2:
        if row["plate"] == "round2":
            sites.append(round2_site(row))
        else:
            s = dict(dossier_sites[row["fault"]])
            s["rank"] = row["rank"]      # area rank, not the round-1 fault rank
            sites.append(s)

    shots = shoot_tables(find_tables(soup))
    # the areas grid is eleven columns; at the default 980 px the last header clips
    shots.update(shoot_tables([
        ("areas", "The ten areas, ordered by best-scoring member", areas_table_html()),
        ("below", "The three areas immediately below the cut", below_line_html()),
    ], width=1180))

    head = head_doc(shots)
    tent = ten_table_doc(shots)
    body = sites_doc(sites)
    tail = tail_doc()

    all_blocks = head.blocks + tent.blocks + body.blocks + tail.blocks
    p1_blocks = head.blocks + tent.blocks + [PART1_TAILNOTE] + tail.blocks
    p2_blocks = [PART2_HEAD.format(title=T.TITLE)] + body.blocks

    OUT.mkdir(exist_ok=True)
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    ASSETS.mkdir()

    # assets in whole-post paste order: the three tables sit before the plates
    ordered = head.images + tent.images + body.images
    for i, (fname, data, alt) in enumerate(ordered, 1):
        (ASSETS / f"{i:02d}_{fname.split('_', 1)[1]}").write_bytes(data)

    pages = {
        "POST.html": all_blocks,
        "POST-part1.html": p1_blocks,
        "POST-part2.html": p2_blocks,
    }
    stats = {}
    for fname, blocks in pages.items():
        html = page(blocks)
        (OUT / fname).write_text(html, encoding="utf-8")
        stats[fname] = dict(
            blocks=len(blocks),
            words=wordcount(blocks),
            images=len(re.findall(r"<img ", "\n".join(blocks))),
            post_bytes=len(html.encode()),
            text_bytes=textbytes(html),
        )

    (OUT / "_build_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    asset_lines = "\n".join(
        f"| {i:02d} | `{i:02d}_{fname.split('_', 1)[1]}` | {len(data) / 1024:.0f} KB | {alt} |"
        for i, (fname, data, alt) in enumerate(ordered, 1)
    )
    (OUT / "PASTE-NOTES.md").write_text(
        NOTES.format(
            title=T.TITLE,
            w_all=stats["POST.html"]["words"],
            kb_all=stats["POST.html"]["text_bytes"] / 1024,
            i_all=stats["POST.html"]["images"],
            w_p1=stats["POST-part1.html"]["words"],
            kb_p1=stats["POST-part1.html"]["text_bytes"] / 1024,
            i_p1=stats["POST-part1.html"]["images"],
            w_p2=stats["POST-part2.html"]["words"],
            kb_p2=stats["POST-part2.html"]["text_bytes"] / 1024,
            i_p2=stats["POST-part2.html"]["images"],
            assets=asset_lines,
        ),
        encoding="utf-8",
    )

    for fname, s in stats.items():
        print(f"{fname:18s} {s['words']:6,} words  {s['images']:2d} img  "
              f"{s['text_bytes'] / 1024:6.1f} KB text  {s['post_bytes'] / 1024 / 1024:5.2f} MB total")


if __name__ == "__main__":
    main()
