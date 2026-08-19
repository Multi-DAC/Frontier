"""THE DELIVERABLE -- the candidate list rendered at the resolution the instruments support.

This is NOT an experiment. It measures nothing new and it must not. It takes results that
already exist -- A7's rank resolution, A8's jurisdiction filter, the basement leg's per-site
scoreability -- and renders the one artefact Clayton actually asked for: the places, with
their uncertainty attached rather than stripped off.

WHY IT EXISTS. Ten reports and eight amendments produced a table headed "rank 1..10". A7
then measured what that table can support and the answer was: one position, one set, one
band. A ranked list is a claim about ORDER, and printing 1..10 asserts nine order relations
of which the instrument resolves four -- three of those on a quarter of the sample. So the
list as printed is a claim the project cannot back, and reprinting it while writing "but see
A7" underneath is exactly the failure this project keeps catching in other people's work.
The fix is not a disclaimer. The fix is to print the structure that was measured.

THE THREE STRUCTURAL RULES, declared here before the file was run:

  R-A  A SITE GETS AN INTEGER POSITION only if its adjacent order relations hold at
       >= 0.95 ON THE FULL DENOMINATOR -- both the relation above it and the relation
       below it, except at the ends of the list where only the existing one is required.
       "Full denominator" means all N_DRAWS draws had both sites present. A pair that never
       swaps in the 23% of draws where both sites still exist is not a resolved order; it is
       a resolved order CONDITIONAL on a membership failure, which is a different claim.
       Derived from the data, not fitted to it: if a future re-run resolves more pairs, more
       positions print, with no edit here.

  R-B  TIERS ARE MEMBERSHIP, NOT RANK. HEAD = P(top ten) == 1.0 and P(gated out) == 0 under
       one-vertex L1 resampling. BAND = within one L1 vertex (0.025 of composite score) of
       the rank-10 line and not in HEAD. FIELD = the rest of the 225. Within a tier, rows
       are emitted ALPHABETICALLY. Not by score. A score column is still printed, because
       hiding it would be its own dishonesty, but it is labelled as not resolving order and
       the row order does not encode it.

  R-C  JURISDICTION IS A FILTER FLAG AND NEVER A SCORE. Being on National Forest land raises
       no physical probability of anything; it is the predicate the founding claim states.
       It can make a site ELIGIBLE or INELIGIBLE for that specific claim. It cannot make a
       site better.

THE GUARDS, and each one exists because this project has already been bitten by its absence:

  G1  ABORT if A7's reproduction control did not pass. A rendering of a list I cannot
      rebuild is a rendering of the wrong list.
  G2  ABORT on any name that appears in one source and not another. A quiet inner-join drop
      would shorten the deliverable and look like a shorter deliverable.
  G3  THE ABSENT COLUMN. If a leg's output file is missing, its column is emitted as the
      literal "UNRUN" on every row plus a top-level status, and is NEVER omitted. An omitted
      constraint column reads as "no constraint applied", which is the exact shape of every
      absence-as-result defect this project has logged.
  G4  THE ORDER GUARD, run against the emitted rows rather than against my intention: at
      most the sites R-A resolved may carry a non-null `position`, and no tier may be
      emitted in score order. Checked after construction, so an edit that reintroduces the
      league table fails the build instead of shipping.
  G5  THE PROVENANCE GUARD. Every number in the output must be traceable to a file on disk;
      the emitter records the source path and byte length of each input it read, and refuses
      to write if an input it declared is absent without a G3 status.

WHAT THIS LIST IS NOT. A6 asked the screen's founding gate, once, whether it fires where the
phenomenon is independently reported, and the answer was no and not significantly no. This
renderer therefore carries A6's verdict in its header rather than in a footnote. The list is
a ranking of places by a geophysical criterion whose predictive validity is UNDEMONSTRATED
and, on the one external test run so far, unsupported. It is a search plan, not a finding.
"""
import datetime as dt
import json, math, os, sys
from datetime import date

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

VERTEX = 0.025          # one L1 vertex, in composite score units (A7-v)
ORDER_BAR = 0.95        # R-A
SEP_KM = 50.0           # the frozen list's own separation rule
PROV = []               # G5
R_EARTH = 6371.0


def hav(a, b, c, d):
    la1, lo1, la2, lo2 = map(math.radians, (a, b, c, d))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def clusters(points, link_km):
    """Single-linkage at link_km. Deliberately the SAME scale as the frozen list's own
    separation rule, so an AREA is exactly 'the neighbourhood the ranking was already
    deduplicating over' -- not a new free parameter chosen to make the picture look good."""
    names = list(points)
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if hav(points[a][0], points[a][1], points[b][0], points[b][1]) <= link_km:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    out = {}
    for n in names:
        out.setdefault(find(n), []).append(n)
    return list(out.values())


def load(path, required=True):
    if not os.path.exists(path):
        if required:
            sys.exit(f"G5 ABORT: declared input missing and no G3 status: {path}")
        PROV.append(dict(path=path, bytes=None, mtime=None, status="ABSENT"))
        return None
    b = os.path.getsize(path)
    PROV.append(dict(path=path, bytes=b,
                     mtime=dt.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(
                         timespec="seconds"),
                     status="read"))
    return json.load(open(path, encoding="utf-8"))


def unread_inputs():
    """G5b: data/*.json that exist and were NOT read by this build.

    G5 as written only proved every number traces to a file. It could not see a
    file that landed AFTER the last build and was never consulted -- which is the
    way this deliverable actually goes stale: a leg completes, its result sits in
    data/, and the list keeps rendering without it and without saying so.
    """
    read = {os.path.normpath(p["path"]) for p in PROV}
    out = []
    for fn in sorted(os.listdir("data")):
        if not fn.endswith(".json"):
            continue
        p = os.path.normpath(os.path.join("data", fn))
        if p in read or fn == "candidate_list.json":
            continue
        out.append((fn, dt.datetime.fromtimestamp(os.path.getmtime(p))))
    return out


def main():
    a7 = load("data/rank_resolution.json")
    frozen = load("data/top10_frozen.json")
    join = load("data/stage5_join_summary.json")
    stab = load("data/basement_stability.json", required=False)
    juris = load("data/jurisdiction_leg.json", required=False)

    # ---- G1
    if not a7.get("control", {}).get("passed"):
        sys.exit("G1 ABORT: A7 reproduction control did not pass.")

    frozen_names = [s["fault"] for s in frozen["sites"]]
    memb = a7["A7ii_membership"]
    pairs = {(p["above"], p["below"]): p for p in a7["A7iii_adjacent_pairs"]}
    band = {m["fault"]: m for m in a7["A7v_contender_band"]["members"]}
    draws = a7["draws"]

    surv = {r["fault_name"]: r for r in join["survivors_ranked"]}

    # ---- G2
    for nm in frozen_names:
        if nm not in surv:
            sys.exit(f"G2 ABORT: frozen site absent from survivor join: {nm}")
        if nm not in memb:
            sys.exit(f"G2 ABORT: frozen site absent from A7 membership: {nm}")
    for nm in band:
        if nm not in surv:
            sys.exit(f"G2 ABORT: band member absent from survivor join: {nm}")

    # ---- R-A: which positions are resolved, derived
    def full(a, b):
        p = pairs.get((a, b))
        return bool(p and p["both_present"] == draws and p["p_order_holds"] >= ORDER_BAR)

    positions, resolved_prefix = {}, []
    for i, nm in enumerate(frozen_names):
        above_ok = (i == 0) or full(frozen_names[i - 1], nm)
        below_ok = (i == len(frozen_names) - 1) or full(nm, frozen_names[i + 1])
        if above_ok and below_ok:
            positions[nm] = i + 1
            resolved_prefix.append(nm)

    # ---- R-B: tiers
    head = sorted(nm for nm in frozen_names
                  if memb[nm]["p_top10"] == 1.0 and memb[nm]["p_gated_out"] == 0.0)
    band_only = sorted(nm for nm in band if nm not in head)
    field_n = join["population"]["survivors"] if isinstance(
        join.get("population"), dict) and "survivors" in join.get("population", {}) \
        else len(surv)

    # ---- per-site scoreability on the basement leg (G3 if the leg never ran)
    if stab:
        sc = {r["fault_name"]: (r["scoreable_in"], r["of_variants"])
              for r in stab["per_site"]}
    else:
        sc = None

    # ---- jurisdiction, three-valued, G3 if unrun
    if juris:
        jur = {r["fault"]: r for r in juris["rows"]}
        jur_status = "RUN"
    else:
        jur, jur_status = {}, "UNRUN"

    def jrow(nm):
        if jur_status == "UNRUN":
            return dict(admin="UNRUN", own="UNRUN", forest=None, eligible="UNRUN")
        r = jur.get(nm)
        if r is None:
            return dict(admin="UNMEASURED", own="UNMEASURED", forest=None,
                        eligible="UNMEASURED")
        def tri(v):
            return "UNMEASURED" if v is None else ("IN" if v else "OUT")
        elig = tri(r["admin"])
        if elig == "OUT" and r.get("near10"):
            elig = "NEAR(<=10km)"
        return dict(admin=tri(r["admin"]), own=tri(r["own"]),
                    forest=r.get("admin_forest") or r.get("near10_forest"),
                    own_class=r.get("own_class"), eligible=elig)

    # SEPARATION SUPPRESSION. A band member can carry a high score and P(top ten) < 0.05 for
    # a reason that has nothing to do with its score: a better-scoring survivor sits within
    # SEP_KM of it and the frozen rule keeps only one per neighbourhood. Red Canyon scores
    # 0.7698 -- second highest in the entire 225 -- and never appears, because Madison is
    # 13.7 km away. Printing "<0.05" beside "0.7698" with no explanation invites the reader
    # to conclude the score is noise. It is the dedup rule, and it is named per row.
    def suppressor(nm):
        me = surv[nm]
        my = band[nm]["score"] if nm in band else None
        if my is None:
            return None
        best = None
        for other, o in band.items():
            if other == nm or o["score"] <= my:
                continue
            d = hav(me["lat"], me["lon"], o["lat"], o["lon"])
            if d <= SEP_KM and (best is None or o["score"] > best[1]):
                best = (other, o["score"], d)
        return best

    # A7's membership table covers the frozen ten; A7's INTRUDER table covers everyone else
    # who entered the top ten in >= 5% of draws. Reading only the first and printing an em
    # dash for the rest would put a blank where a measurement exists -- and would blank it
    # hardest for Sandia (0.505), which is the single most consequential cell in this file.
    # Below the 5% reporting threshold the honest cell is "<0.05", not "unknown".
    intr = a7["A7ii_intruders_p_ge_005"]
    INTRUDER_FLOOR = 0.05

    def p_top_ten(nm):
        if nm in memb:
            return memb[nm]["p_top10"], "frozen"
        if nm in intr:
            return intr[nm], "intruder"
        return None, "below_floor"

    def row(nm, tier):
        s = surv[nm]
        m = memb.get(nm)
        caveats = []
        if m and m["p_gated_out"] >= 0.05:
            caveats.append(f"falls out of the 225 entirely in "
                           f"{m['p_gated_out']*100:.1f}% of L1 draws")
        if sc is not None:
            got, of = sc.get(nm, (0, 0))
            if of and got == 0:
                caveats.append("UNSCOREABLE on the basement leg (no node in window)")
            elif of and got < of:
                caveats.append(f"basement-scoreable in only {got}/{of} variants")
        elif stab is None:
            caveats.append("basement scoreability UNRUN")
        p, basis = p_top_ten(nm)
        if basis == "intruder":
            caveats.append(f"NOT on the frozen ten; enters it in {p*100:.1f}% of L1 draws")
        sup = suppressor(nm)
        if sup and basis == "below_floor":
            caveats.append(f"SUPPRESSED BY THE {SEP_KM:.0f} km SEPARATION RULE, not by "
                           f"score — {sup[0]} scores {sup[1]:.4f} at {sup[2]:.1f} km")
        return dict(
            site=nm, tier=tier,
            position=positions.get(nm),
            lat=s["lat"], lon=s["lon"],
            score_not_an_order=round(band[nm]["score"], 4) if nm in band else None,
            p_in_top_ten=p, p_in_top_ten_basis=basis,
            p_gated_out=(m["p_gated_out"] if m else None),
            jurisdiction=jrow(nm),
            caveats=caveats)

    rows = ([row(nm, "HEAD") for nm in head]
            + [row(nm, "BAND") for nm in band_only])

    # ---- G4, run against the emitted rows
    pos_rows = [r for r in rows if r["position"] is not None]
    if {r["site"] for r in pos_rows} != set(resolved_prefix):
        sys.exit("G4 ABORT: emitted positions do not match the R-A derivation.")
    for tier in ("HEAD", "BAND"):
        names = [r["site"] for r in rows if r["tier"] == tier]
        if names != sorted(names):
            sys.exit(f"G4 ABORT: tier {tier} is not emitted alphabetically.")
        scores = [r["score_not_an_order"] for r in rows if r["tier"] == tier]
        clean = [s for s in scores if s is not None]
        if len(clean) > 2 and (clean == sorted(clean, reverse=True) or
                               clean == sorted(clean)):
            sys.exit(f"G4 ABORT: tier {tier} is emitted in score order.")

    # ---- AREAS. Clayton's ask is "areas in which anomalous phenomena are most likely
    # present". The screen emits FAULTS, and A7 says the fault-level order is not resolved.
    # The area level is a coarser question and the data may answer it where it cannot answer
    # the finer one -- so it is asked explicitly rather than left implicit in a map.
    #
    # THE CONFOUND, declared: an area's MEMBER COUNT inherits the same mapping-density
    # artefact A7-iv already priced in the junction term. A valley mapped at 1:24,000 by a
    # 1990s NEHRP grant reports more distinct fault names than the same structure mapped once
    # at 1:250,000. So member count is NOT evidence of anything and is never used to order
    # areas here. What the clustering buys is the OPPOSITE: it stops the reader counting the
    # same place several times.
    pts = {nm: (surv[nm]["lat"], surv[nm]["lon"]) for nm in list(head) + band_only}
    areas = []
    for grp in clusters(pts, SEP_KM):
        grp = sorted(grp)
        best = max(grp, key=lambda n: band[n]["score"] if n in band else -1)
        areas.append(dict(
            members=grp, n_members=len(grp),
            contains_head=sorted(n for n in grp if n in head),
            best_scoring=best,
            best_score=round(band[best]["score"], 4) if best in band else None,
            centroid=[round(sum(pts[n][0] for n in grp) / len(grp), 3),
                      round(sum(pts[n][1] for n in grp) / len(grp), 3)],
            extent_km=round(max((hav(*pts[a], *pts[b]) for a in grp for b in grp),
                                default=0.0), 1)))
    # Sorted by the name the table DISPLAYS. Sorting by members[0] while displaying
    # best_scoring produced a table that claimed to be alphabetical and visibly was not --
    # the sort key and the shown column have to be the same column or the claim is false.
    areas.sort(key=lambda a: (not a["contains_head"], a["best_scoring"]))

    # SINGLE-LINKAGE CHAINS, and the chain is visible in extent_km rather than hidden by it.
    # A 50 km link does not mean a 50 km area: A--B--C at 45 km each is one 90 km "area".
    # Reported, not smoothed. And the link scale's own sensitivity is printed, because
    # Centennial sits 54.8 km from Madison and therefore separates by 4.8 km of margin.
    link_sensitivity = {f"{k:.0f}": len(clusters(pts, k)) for k in (30.0, 40.0, 50.0, 60.0,
                                                                   75.0)}

    out = dict(
        built=str(date.today()),
        what_this_is="A search plan. Places ranked by a geophysical criterion whose "
                     "predictive validity is UNDEMONSTRATED and, on the one external test "
                     "run (A6), unsupported.",
        a6_verdict="The screen's founding gate (R1 CONDUIT, <=10 km to a Quaternary normal "
                   "fault) was asked once whether it fires where anomalous lights are "
                   "independently reported. 0 of 6 control locales pass it; 34.4% of random "
                   "western ground does. p=0.199 on the distance contrast, direction "
                   "against the hypothesis. A fail at n=6 is not proof of absence, and it "
                   "is not support either.",
        resolution="A7: one integer position resolved, a head-set of "
                   f"{len(head)} with unresolved internal order, a band of "
                   f"{len(band)} the score cannot order. One L1 vertex = {VERTEX} score.",
        rules=dict(R_A="integer position requires adjacent order >=0.95 on the FULL "
                       "denominator, both sides",
                   R_B="tiers are membership; rows alphabetical within tier; score printed "
                       "but does not set row order",
                   R_C="jurisdiction is a filter flag, never a score"),
        resolved_positions=positions,
        tiers=dict(HEAD=head, BAND=band_only, FIELD_n=field_n - len(head) - len(band_only)),
        areas=areas,
        areas_link_sensitivity_km_to_count=link_sensitivity,
        areas_note="Single-linkage at the frozen list's own 50 km separation scale. Member "
                   "count inherits the junction term's mapping-density artefact and is not "
                   "used to order areas.",
        jurisdiction_status=jur_status,
        basement_scoreability_status=("RUN" if stab else "UNRUN"),
        rows=rows,
        provenance=PROV)
    json.dump(out, open("data/candidate_list.json", "w"), indent=1)

    # ---------------------------------------------------------------- markdown
    L = []
    L.append("# CANDIDATE LIST — place-threshold screen")
    L.append("")
    L.append(f"*Built {out['built']}. Rendered at the resolution A7 measured, "
             "not at the resolution the score is printed to.*")
    L.append("")
    L.append("## What this list is")
    L.append("")
    L.append(out["what_this_is"])
    L.append("")
    L.append("**A6, the one external test:** " + out["a6_verdict"])
    L.append("")
    L.append("**A7, the resolution:** " + out["resolution"])
    L.append("")
    if jur_status == "UNRUN":
        L.append("> **JURISDICTION FILTER: NOT RUN.** The founding claim's Forest Service "
                 "predicate has not been applied to these rows. The column below reads "
                 "UNRUN and must not be read as 'no constraint'.")
        L.append("")

    def tbl(title, names, note):
        L.append(f"## {title}")
        L.append("")
        L.append(note)
        L.append("")
        L.append("| # | site | lat, lon | score¹ | P(top 10)² | jurisdiction³ | caveats |")
        L.append("|---|---|---|---|---|---|---|")
        for nm in names:
            r = next(x for x in rows if x["site"] == nm)
            p = str(r["position"]) if r["position"] else "—"
            sc_ = f"{r['score_not_an_order']:.4f}" if r["score_not_an_order"] else "—"
            pt = ("&lt;0.05" if r["p_in_top_ten_basis"] == "below_floor"
                  else f"{r['p_in_top_ten']:.3f}")
            j = r["jurisdiction"]["eligible"]
            if r["jurisdiction"].get("forest"):
                j += f" ({r['jurisdiction']['forest']})"
            cav = "; ".join(r["caveats"]) or "—"
            L.append(f"| {p} | **{nm}** | {r['lat']}, {r['lon']} | {sc_} | {pt} | {j} "
                     f"| {cav} |")
        L.append("")

    tbl("HEAD — membership certain, order mostly not",
        head,
        "Every site here holds P(in top ten) = 1.000 under one-vertex L1 resampling and is "
        "never gated out. **Rows are alphabetical.** A number in the first column means the "
        "position survived R-A; an em dash means the site is in the head set and its "
        "position within it is not resolved.")
    tbl("BAND — within one L1 vertex of the rank-10 line",
        band_only,
        f"These {len(band_only)} sites are within {VERTEX} of composite score of the "
        "rank-10 cut. The score cannot order them and neither can this table. Some are "
        "currently inside the frozen top ten and some are outside it; that distinction is "
        "not a measurement.")
    L.append("## AREAS — the coarser question, which the data answers better")
    L.append("")
    L.append("The screen emits faults; A7 says the fault-level order is not resolved. "
             "Single-linkage clustering of the head and band at **the frozen list's own "
             "50 km separation scale** — not a new free parameter — collapses "
             f"{len(head) + len(band_only)} named structures into **{len(areas)} areas**. "
             "Areas containing a head site are listed first; within that, alphabetically.")
    L.append("")
    L.append("> **Member count is not evidence.** It inherits the same mapping-density "
             "artefact A7-iv priced in the junction term: a valley mapped at 1:24,000 "
             "reports more distinct fault names than the same structure mapped once at "
             "1:250,000. What the clustering buys is the opposite — it stops the same "
             "place being counted several times.")
    L.append("")
    L.append("| area (best-scoring member) | centroid | extent | structures | head sites |")
    L.append("|---|---|---|---|---|")
    for a in areas:
        hs = ", ".join(a["contains_head"]) or "—"
        L.append(f"| **{a['best_scoring']}** | {a['centroid'][0]}, {a['centroid'][1]} | "
                 f"{a['extent_km']} km | {a['n_members']} | {hs} |")
    L.append("")
    L.append("**Single linkage chains, and the chain is in the extent column rather than "
             "hidden by it.** A 50 km link does not produce 50 km areas: three structures "
             "45 km apart in a line are one area 90 km long. The largest here is "
             f"{max(a['extent_km'] for a in areas)} km, which is a **corridor, not a "
             "locality**, and is named as one.")
    L.append("")
    L.append("**Sensitivity of the area count to the link scale**, printed because "
             "Centennial fault separates from the Madison cluster by 4.8 km of margin:")
    L.append("")
    L.append("| link | " + " | ".join(f"{k} km" for k in link_sensitivity) + " |")
    L.append("|---|" + "---|" * len(link_sensitivity))
    L.append("| areas | " + " | ".join(str(v) for v in link_sensitivity.values()) + " |")
    L.append("")
    L.append("## Footnotes")
    L.append("")
    L.append("1. **score is printed and does not order the table.** Four of its five terms "
             "take 4–7 distinct values across the 225 survivors and one of them (slip) is "
             "the same number for 86% of the field. The composite is a coarse lattice; "
             "differences below one lattice step are not differences.")
    L.append("2. P(in top ten) under ±1 vertex of `quartz_frac`, 10,000 draws — the noise "
             "the quartz layer declared about itself before this question was asked. "
             "`<0.05` is A7's reporting floor for sites outside the frozen ten, and means "
             "measured-and-small, not unmeasured.")
    L.append("3. Three-valued. UNMEASURED is not OUT. UNRUN is not 'unconstrained'.")
    L.append("")
    L.append("**Not in this table and belonging in the report:** the 1959 Hebgen Lake "
             "rupture supplies the three highest raw scores in the whole 225 (Madison, Red "
             "Canyon, Hebgen — 11.6 and 13.7 km apart). The 50 km separation rule prints it "
             "once. The screen's strongest signal is one earthquake, counted three times.")

    # ------------------------------------------------- G5b: rendered provenance
    # PROV was collected since the first build and written only into
    # data/candidate_list.json. Nobody reads that. The staleness this guard
    # exists to catch is only visible if it reaches the human-facing document.
    unread = unread_inputs()
    L.append("")
    L.append("## Provenance — what this build read, and what it did not")
    L.append("")
    L.append(f"Built {dt.datetime.now().isoformat(timespec='seconds')}. "
             "This block is generated, not asserted.")
    L.append("")
    L.append("| input | status | bytes | last written |")
    L.append("|---|---|---|---|")
    for p in PROV:
        L.append(f"| `{p['path']}` | {p['status']} | "
                 f"{'' if p['bytes'] is None else format(p['bytes'], ',')} | "
                 f"{p['mtime'] or '—'} |")
    L.append("")
    # The discriminating cut is not read-vs-unread -- most of data/ is upstream
    # input to other legs and always unread here.
    #
    # A single "newer than the newest input I read" cut was the obvious rule and it
    # UNDER-REPORTS: a leg landing at 15:14 hides behind an input read at 15:46
    # even though this build never consulted it. The cut that does not hide one is
    # SAME DAY AS THE BUILD -- every result produced in the working session that
    # this document does not carry. It over-reports (some same-day files are
    # deliberately not inputs here), and over-reporting is the safe direction:
    # a named file a reader dismisses costs a glance, an omitted one costs the claim.
    now = dt.datetime.now()
    read_m = [p["mtime"] for p in PROV if p["mtime"]]
    cut = max(read_m) if read_m else None
    pending = [(fn, m) for fn, m in unread if m.date() == now.date()]
    if pending:
        L.append(f"⚠ **{len(pending)} result file(s) in `data/` were written today and "
                 "were NOT read by this build.** No number above reflects them. A leg "
                 "completing does not update this document; only a rebuild does, and only "
                 "for the inputs `main()` declares. Some of these are deliberately not "
                 "inputs to the list — the guard cannot tell intent, so it names them all.")
        L.append("")
        L.append("| written today, unread here | last written | postdates every input read? |")
        L.append("|---|---|---|")
        for fn, m in sorted(pending, key=lambda x: x[1], reverse=True):
            iso = m.isoformat(timespec="seconds")
            L.append(f"| `data/{fn}` | {iso} | {'yes' if cut and iso > cut else 'no'} |")
    else:
        L.append("No `data/*.json` was written today and left unread by this build.")
    L.append("")
    L.append(f"*({len(unread) - len(pending)} further `data/*.json` are unread and predate "
             "today — upstream inputs to other legs, not results of this session.)*")

    open("reports/CANDIDATE-LIST.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"HEAD {len(head)} · BAND {len(band_only)} · FIELD {out['tiers']['FIELD_n']}",
          file=sys.stderr)
    print(f"resolved integer positions: {positions or 'NONE'}", file=sys.stderr)
    print(f"jurisdiction: {jur_status} · basement scoreability: "
          f"{out['basement_scoreability_status']}", file=sys.stderr)
    print("wrote data/candidate_list.json, reports/CANDIDATE-LIST.md", file=sys.stderr)


if __name__ == "__main__":
    main()
