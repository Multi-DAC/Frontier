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
    return sites


def verify(sites, frozen):
    """Assert every measurement quoted in report_text.py against its source.

    The lesson this implements: a count written into prose from a quick scan is
    a count with no controls. Run the check before the number sets.
    """
    fz = {s["fault"]: s for s in frozen["sites"]}
    problems = []
    checked = [0]

    def want(name, key, got, exp):
        checked[0] += 1
        if got is None:
            problems.append(f"{name}: {key} not found in dossier")
        elif abs(float(got) - float(exp)) > 1e-6:
            problems.append(f"{name}: {key} prose says {exp}, source says {got}")

    for s in sites:
        n = s["name"]
        c = T.CHECK.get(n)
        if c is None:
            problems.append(f"{n}: no CHECK entry in report_text.py")
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

        # and against the frozen list, which is the artifact the ten came from
        if n not in fz:
            problems.append(f"{n}: absent from top10_frozen_100km.json")
        else:
            want(n, "score (frozen)", fz[n]["score"], c["score"])
            want(n, "quartz_frac (frozen)", fz[n]["L1"], c["q"])

        if n not in T.PLACE:
            problems.append(f"{n}: no PLACE entry")
        if n not in T.SITES:
            problems.append(f"{n}: no narrative in report_text.SITES")

    for n in T.CHECK:
        if n not in {s["name"] for s in sites}:
            problems.append(f"{n}: CHECK entry names a site the dossier does not have")

    checked[0] += verify_tiers(problems)
    checked[0] += verify_programme(problems)

    if problems:
        print("VERIFICATION FAILED — nothing written:")
        for p in problems:
            print("  ·", p)
        raise SystemExit(1)
    print(f"verified {checked[0]} quoted values (site measurements, tiers, programme "
          f"headline figures) against dossier.html, top10_frozen_100km.json, "
          f"stage5_join_summary.json, lore*_result.json, lore_crossleg.json and "
          f"blind_rescore_result.json — clean")


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
    for i, leg in enumerate(("L1", "L2", "L3")):
        pairs.append((f"sep_sighted[{leg}]", p["sep_sighted"][i], bl["legs"][leg]["SIGHTED"]["separation"], 1e-9))
        pairs.append((f"sep_blind[{leg}]", p["sep_blind"][i], bl["legs"][leg]["BLIND_consensus"]["separation"], 1e-9))
    for _leg, fname, *_ in LEGS:
        pairs.append((f"bar ({fname})", p["bar"], j(fname)["required"], 1e-9))

    for label, said, real, tol in pairs:
        n += 1
        if real is None:
            problems.append(f"programme {label}: source value is null")
        elif abs(float(said) - float(real)) > tol:
            problems.append(f"programme {label}: prose says {said}, source says {real}")
    return n


def find_tables(soup):
    """The three tables where the grid IS the argument, keyed by slug."""
    jobs, seen = [], {}
    captions = {
        "legs": "The three pre-registered lore experiments, sighted and blind",
        "ten": "The ten, with the five terms that selected them",
        "suppressed": "Suppressed by the 100 km separation rule",
    }
    for t in soup.find_all("table"):
        k = classify(t)
        if k.startswith("img:"):
            slug = k.split(":", 1)[1]
            if slug in seen:
                continue
            seen[slug] = True
            jobs.append((slug, captions.get(slug, ""), str(t)))
    missing = set(captions) - seen.keys()
    if missing:
        raise SystemExit(f"tables not found in dossier: {sorted(missing)}")
    return jobs


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

    d.h2("Methodological rigour, and where it caught us")
    d.add(T.RIGOUR)

    d.rule()
    d.h2("Result one — the gate works")
    d.add(T.RESULT_GATE)

    d.h2("Result two — the ranking does not")
    d.add(T.RESULT_RANKER)

    d.h2("Result three — the three lore experiments")
    d.add(T.RESULT_LORE_INTRO)
    d.image(shots["legs"], "the three lore legs at a glance",
            "All three legs, sighted and blind, against their pre-declared bar of +1.0 tiers.")
    d.add(T.RESULT_LORE_AFTER)

    d.h2("The verdict, stated as plainly as it can be")
    d.add(T.VERDICT)
    return d


def ten_table_doc(shots):
    d = Doc()
    d.rule()
    d.h2("The ten sites the physics chose")
    d.add(
        "<p>Selected on rock, rupture age, slip rate, junction density and structural scale, "
        "with every one of those quantities measured from institutional records before a single "
        "piece of folklore was looked up. Read them as ten members of a qualifying class. "
        "<strong>The ordering is not validated and this is not a ranking.</strong></p>"
    )
    d.image(shots["ten"], "the ten with their five scoring terms",
            "The ten, with the five measured terms that selected them.")
    d.h3("Nine faults the separation rule suppressed")
    d.add(
        "<p>Sites were required to sit 100 km apart, taken greedily from the top. Nine faults "
        "were removed by that rule, and several scored higher than sites that remain on the "
        "list. They are printed because a suppression rule you cannot see is a thumb on the "
        "scale — three of these sit inside a 14 km circle around Hebgen Lake, which is one "
        "place, not three.</p>"
    )
    d.image(shots["suppressed"], "faults suppressed by the 100 km rule",
            "Nine faults removed by the separation rule, with what suppressed each one.")
    return d


def sites_doc(sites):
    d = Doc()
    d.add(T.TEN_INTRO)
    for s in sites:
        n = s["name"]
        narrative = T.SITES[n]
        d.rule()
        d.h2(f"#{s['rank']} · {n}")
        lat, lon = s["coord"]
        d.add(
            f"<p><strong>{esc(T.PLACE[n])}</strong> · <code>{lat}, {lon}</code> · "
            f"physics score {T.CHECK[n]['score']:.4f} · gate reading "
            f"<code>{T.CHECK[n]['q']}</code> · nearest census place "
            f"{T.CHECK[n]['near_km']} km</p>"
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
        d.add(narrative["record"])
    return d


def tail_doc():
    d = Doc()
    d.rule()
    d.h2("What a reader has to hold against all ten of these")
    d.add(T.HOLD_AGAINST)

    d.h2("Two defects found in our own instruments")
    d.add(T.DEFECTS)

    d.h2("What survives, and what would move it")
    d.add(T.WHAT_SURVIVES)

    d.rule()
    d.h2("Why print a negative result at all")
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

- A continental screen for the physics of anomalous places, with the folklore
  held out until the physics was frozen — and the null printed in full.
- Ten faults, four geophysical layers each, three pre-registered lore
  experiments, nine blind scorers, and a result that did not go our way.

If you publish it as two, part 2's title: **{title} — the ten sites**.

## What this build does that the old one did not

| | old (`build_substack.py`) | this |
|---|---|---|
| structure | the internal dossier's | question → method → rigour → results → sites |
| lore | tier tables per site | **narrative prose per site**, tiers stated inline |
| framing | none — opens on a results table | opens on the observation and the conjecture |
| method | scattered through captions | its own section, plus a rigour section |
| tables | 3 imaged + 44 reflowed | 3 imaged, the rest written into the prose |
| numbers | rendered from data | rendered from data **and asserted against it** |

Every measurement quoted in the prose — score, gate reading, trace length,
segment count, junction count, mapped length, nearest place — is checked against
`dossier.html` and `data/top10_frozen_100km.json` at build time. A typo fails
the build rather than shipping.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
{assets}
"""

PART1_TAILNOTE = (
    "<hr><p><em><strong>The ten sites themselves — plates, measurements and the record at each "
    "one told as narrative — are in the companion piece.</strong> This half is the question, the "
    "method and the result; that half is the field guide.</em></p>"
)

PART2_HEAD = (
    "<p><em>This is the companion half of <strong>{title}</strong>, which sets out the "
    "conjecture under test, how the continental screen was built, what was done to try to kill "
    "the result, and what the three pre-registered lore experiments returned. The short version "
    "of that half: the gate works and its two declared controls are exact; the ranking fails its "
    "own controls by 0.19 in the wrong direction; and all three lore experiments come back NOT "
    "SUPPORTED. Read the ten below as ten members of a qualifying class, not as a "
    "ranking.</em></p>"
)


def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    frozen = json.loads((ROOT / "data" / "top10_frozen_100km.json").read_text(encoding="utf-8"))

    sites = parse_sites(soup)
    verify(sites, frozen)

    shots = shoot_tables(find_tables(soup))

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
