"""A13 -- THE CHARGE TERM, GENERALISED BEYOND QUARTZ. Pre-registered before the first query.

Clayton, Day 199: "regarding piezoelectricity, we have focused on quartz, but any other
potentially piezoelectrical or electromagnetically active minerals or substances should be
equally considered, if there are any others."

There are. And the honest answer is worse than "there are others": the literature's
strongest lab result points AT ROCK THIS SCREEN CURRENTLY SCORES AS A NEGATIVE.

    code/lithology_probe.py:45, the incumbent classifier, verbatim:
        NEGATIVE = ("alluvium", "sedimentary", "sandstone", "shale", "limestone",
                    "dolostone", "basalt", "gabbro", "ophiolite", ...)

    Freund and colleagues loaded air-dry tiles of granite, anorthosite, gabbro, limestone and
    marble uniaxially and measured the stress-activated current flowing out of the stressed
    volume. ANORTHOSITE AND GABBRO PRODUCED 10-50x THE CURRENT OF GRANITE (granite itself
    ~1e-5 A per cubic metre stressed at 50 MPa). The carriers are positive holes (defect
    electrons in the O2- sublattice) activated from peroxy defects O3X-OO-XO3 with X = Si or
    Al -- a defect of the SILICATE FRAMEWORK, present in igneous and high-grade metamorphic
    rock generally. Quartz is not required. Plagioclase-rich, quartz-poor rock is the BEST
    performer in the only direct comparison of rock types I can find.

    EVIDENCE GRADE, stated because it bounds everything below: SECONDARY. Two independent
    search reads returned the same rock ordering and the same order-of-magnitude figure, but
    both paraphrase the same body of work (Freund et al.), and I could not read the primary
    text -- the ScienceDirect page 403s and the arXiv PDF returned binary this fetcher could
    not decode. The 10-50x figure is therefore UNCONFIRMED AGAINST PRIMARY SOURCE and is
    flagged as such in every artefact that cites it. It is enough to justify measuring the
    rock; it is not enough to rank on.

SO THE INCUMBENT L1 TERM IS NOT "the charge term". It is one pathway of at least five, and
its own physics has a defect nobody in this project has stated:

  BULK PIEZOELECTRIC RESPONSE REQUIRES CRYSTALLOGRAPHIC ALIGNMENT. Quartz grains in a
  granite are randomly oriented, so their individual dipoles largely CANCEL and the net
  bulk moment tends to zero. Piezoelectricity survives at rock scale mainly where a fabric
  aligns the c-axes -- foliated quartzite, mylonite, sheared vein quartz. The incumbent
  classifier already half-knows this: it separates TIER_FABRIC ("aligned") from
  TIER_PLUTONIC, and lithology_probe.py:25 says in a comment that this is deliberate. Then
  the screen collapses both into one quartz_frac and ranks on the sum. The distinction was
  measured and then discarded.

THE FIVE PATHWAYS, each with the rock signature it is detectable by. Declared here, with
weights, BEFORE any node is scored.

  P1 PEROXY / POSITIVE-HOLE (Freund).            weight 1.00
     Stress-activated charge carriers in silicate frameworks. Strongest in plagioclase-rich
     mafic and anorthositic rock; present in granite; absent in carbonate.
     SIGNATURE: gabbro, anorthosite, norite, diorite, diabase, dolerite, basalt, granulite,
     amphibolite, charnockite, granite, granodiorite, gneiss.
  P2 PIEZOELECTRIC, ALIGNED.                     weight 0.75
     Non-centrosymmetric minerals in a rock with a fabric that prevents cancellation.
     SIGNATURE: quartzite, mylonite, quartz vein, schist, orthogneiss  (+ tourmaline-bearing
     pegmatite/greisen -- tourmaline is both piezo- AND pyroelectric, unlike quartz).
  P3 PIEZOELECTRIC, UNALIGNED.                   weight 0.25
     The incumbent term, at the weight its own cancellation argument implies rather than the
     weight it has been carrying.
     SIGNATURE: granite, granodiorite, quartz monzonite, tonalite, rhyolite, aplite.
  P4 PIEZOMAGNETIC / SEISMOMAGNETIC.             weight 0.50
     Stress-modulated magnetisation in magnetite-bearing rock -- the tectonomagnetic effect.
     A magnetic rather than electric channel, and not reducible to P1.
     SIGNATURE: magnetite, banded iron formation, serpentinite, peridotite, ultramafic,
     skarn, ilmenite-bearing gabbro.
  P5 CONDUCTIVE CHANNEL.                         weight 0.50
     Does NOT generate charge -- it CONCENTRATES and routes it. Graphite, sulphide and
     saline-fluid networks are the strongest crustal conductors known and are what
     magnetotelluric surveys actually image. A generator with no conductor disperses; this
     is the term that says where current goes.
     SIGNATURE: graphite, graphitic schist, black shale, massive sulphide, pyrite, pyrrhotite,
     serpentinite, marine shale.

  DELIBERATELY NOT A PATHWAY, and named so the omission is visible rather than accidental:
  the WATER / electrokinetic (streaming-potential) term Clayton also asked for. Fluid moving
  through a fractured rock generates a streaming potential, and it is a real and probably
  large channel here. It is NOT in this leg because it is not a LITHOLOGY, and this leg
  scores lithology at points. Guessing it from rock type would be reading hydrology off a
  geologic map. It needs its own leg against a hydrologic layer (NHD + water table +
  geothermal), and until that leg exists this screen's "water" coverage is ZERO, not partial.

  ALSO NOT A PATHWAY: radiogenic ionisation (U/Th/radon). Same reason -- it wants the NURE
  radiometric grid, not a lithology string.

METHOD. Every node is re-probed at the SAME EIGHT TRACE VERTICES the incumbent used
(trace_lithology_national.py's geometry, unchanged), and each vertex is classified TWICE:
once by the incumbent quartz map and once by the pathway map. Paired, on identical points.
The incumbent's Macrostrat cache was lost with an untracked work/ directory, so this run
rebuilds it as a side effect.

POPULATION: all 507 stage-2 nodes, NOT the 225 gate survivors.
  This is the whole point and it is not an efficiency choice. The L1 gate passed 242 and
  failed 1157. If the generalised term is scored only on rock that already passed a
  QUARTZ gate, it can confirm the gate and can never overturn it -- the fixture would be
  built where the right and wrong answers agree. The mafic rock the Freund result points at
  is, by construction, on the far side of that gate.

DECLARED BEFORE THE FIRST QUERY:

  PREDICTION. Nodes scored NONE by the incumbent (386 of 507) will contain a substantial
  population of P1-positive mafic rock. I expect the generalised term to promote sites the
  quartz gate excluded. If it does not -- if P1 and quartz_frac turn out to be nearly the
  same ordering -- then the incumbent gate was accidentally fine and this leg's finding is
  a null, which is a real and publishable outcome.

  BAR i   The generalised term is DISTINCT from the incumbent if Spearman rho between
          charge_score and quartz_frac across the 507 is < 0.7. At rho >= 0.7 it is a
          relabelling of the existing term and must be reported as one, not as a new layer.
  BAR ii  It is CONSEQUENTIAL if >= 20% of the nodes in the top 50 by charge_score were
          gated OUT by the incumbent quartz gate (quartz_frac < 0.25).
  BAR iii The mafic claim SPECIFICALLY holds if nodes whose dominant pathway is P1-mafic
          (gabbro/anorthosite/basalt family) rank higher under charge_score than under the
          incumbent by a median of >= 50 positions. If P1-mafic does not move, the Freund
          result has no purchase on this dataset whatever the lab says, and I will say so.

  ! NONE OF THE THREE BARS TESTS WHETHER ANY OF THIS PRODUCES A PORTAL, OR A LIGHT, OR AN
    ANOMALY. They test whether a differently-specified rock term picks a different set of
    places. A6 already measured what the founding gate does against independently reported
    anomalous-light locales -- 0 of 6 passed, against 34.4% of random western ground -- and
    nothing in this leg improves that. A13 can only change WHICH places the screen names.
    Whether the screen names anything real is a separate and still-unanswered question, and
    the deliverable's header says so.
"""
import json, math, os, sys, time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lithology_probe as LP                                            # noqa: E402
from trace_lithology_national import pull_exact, trace_points           # noqa: E402

OUT = "work/charge_term.json"
N_SAMPLE = 8
CKPT = 5
GATE = 0.25

PATHWAYS = {
    # P1 IS SPLIT, and the split was forced by this file's own smoke test: with one P1 list,
    # granite scored 1.00 exactly as gabbro did, so the leg could not express the gradient it
    # exists to test, and BAR iii could never fire. The reported lab ordering is
    # anorthosite/gabbro at 10-50x granite. The weight ratio here is 2.5x (1.00 vs 0.40) --
    # FAR below the reported 10-50x, deliberately, because that figure is SECONDARY-grade
    # (see docstring) and encoding an unconfirmed order of magnitude as a weight would let
    # one unread paper dominate the ranking.
    "P1a_peroxy_mafic": (1.00, (
        "gabbro", "anorthosite", "norite", "diabase", "dolerite", "basalt", "diorite",
        "granulite", "amphibolite", "charnockite", "andesite", "troctolite")),
    "P1b_peroxy_felsic": (0.40, (
        "granite", "granodiorite", "gneiss", "monzonite", "syenite", "tonalite")),
    "P2_piezo_aligned": (0.75, (
        "quartzite", "mylonite", "quartz vein", "schist", "orthogneiss", "metaquartzite",
        "tourmaline", "pegmatite", "greisen", "phyllite", "migmatite")),
    "P3_piezo_unaligned": (0.25, (
        "granite", "granodiorite", "quartz monzonite", "tonalite", "rhyolite", "aplite",
        "quartz diorite", "granitoid", "dacite")),
    "P4_piezomagnetic": (0.50, (
        "magnetite", "iron formation", "serpentinite", "peridotite", "ultramafic",
        "dunite", "pyroxenite", "skarn", "ilmenite", "ophiolite")),
    "P5_conductive": (0.50, (
        "graphite", "graphitic", "black shale", "sulphide", "sulfide", "pyrite",
        "pyrrhotite", "serpentinite", "marine shale", "argillite")),
}
# A term appearing in two pathways (granite in P1 and P3, serpentinite in P4 and P5) is
# DELIBERATE -- one rock can carry two mechanisms, and forcing a partition would encode a
# claim about which mechanism dominates that nobody has measured. Each pathway is scored
# independently and the node score is the weighted MAX, not the sum: a sum would let a rock
# that is mediocre on four pathways outscore one that is excellent on the strongest, which
# is an arithmetic claim about mechanism additivity nobody has evidence for.


def pathways_at(units):
    """Which pathways does this unit list light up? Returns {pathway: matched_term}."""
    if units is None:
        return None
    blob = " ".join(f"{u.get('lith') or ''} {u.get('name') or ''}" for u in units).lower()
    hits = {}
    for p, (_w, terms) in PATHWAYS.items():
        for t in terms:
            if t in blob:
                hits[p] = t
                break
    return hits


def charge_of(hits):
    """Weighted MAX over lit pathways. 0.0 when nothing lights up; None when unmeasured."""
    if hits is None:
        return None
    return max((PATHWAYS[p][0] for p in hits), default=0.0)


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(num / (dx * dy), 4) if dx and dy else None


if __name__ == "__main__":
    nodes = json.load(open("data/transport_screen_stage2.json"))["all"]
    seen, todo = set(), []
    for n in nodes:
        nm = (n.get("fault_name") or "").strip()
        if not nm or nm in seen:
            continue
        seen.add(nm)
        todo.append(n)
    state = json.load(open(OUT)) if os.path.exists(OUT) else {"done": {}}
    print(f"[A13] {len(todo)} distinct faults from {len(nodes)} stage-2 nodes; "
          f"{len(state['done'])} already done", file=sys.stderr)

    for i, n in enumerate(todo, 1):
        nm = n["fault_name"]
        if nm in state["done"]:
            continue
        try:
            pts, km = trace_points(pull_exact(nm), N_SAMPLE)
            vtx = []
            for la, lo in pts:
                units = LP.unit_at(la, lo)
                q_tier, q_term, _ = LP.classify(units)
                hits = pathways_at(units)
                vtx.append(dict(lat=la, lon=lo, quartz_tier=q_tier, quartz_term=q_term,
                                pathways=hits, charge=charge_of(hits)))
            meas = [v for v in vtx if v["charge"] is not None]
            qhit = [v for v in vtx if v["quartz_tier"] in ("TIER_PLUTONIC", "TIER_FABRIC")]
            state["done"][nm] = dict(
                n_pts=len(vtx), traced_km=km, lat=n.get("lat"), lon=n.get("lon"),
                quartz_frac=(round(len(qhit) / len(vtx), 3) if vtx else 0.0),
                charge_score=(round(sum(v["charge"] for v in meas) / len(meas), 4)
                              if meas else None),
                pathway_counts=dict(Counter(p for v in meas for p in (v["pathways"] or {}))),
                vertices=vtx)
            d = state["done"][nm]
            print(f"[{i}/{len(todo)}] q={d['quartz_frac']:.2f} charge={d['charge_score']} "
                  f"{sorted(d['pathway_counts'])} {nm[:44]}", file=sys.stderr)
        except Exception as e:
            state["done"][nm] = dict(error=str(e)[:200])
            print(f"[{i}/{len(todo)}] ERROR {nm[:40]}: {e}", file=sys.stderr)
        sys.stderr.flush()
        if i % CKPT == 0:
            LP._save()
            json.dump(state, open(OUT, "w"), indent=1)

    LP._save()
    json.dump(state, open(OUT, "w"), indent=1)

    ok = {k: v for k, v in state["done"].items()
          if "error" not in v and v.get("charge_score") is not None}
    qs = [v["quartz_frac"] for v in ok.values()]
    cs = [v["charge_score"] for v in ok.values()]
    rho = spearman(qs, cs)

    by_charge = sorted(ok.items(), key=lambda kv: -kv[1]["charge_score"])
    top50 = by_charge[:50]
    gated_out_in_top50 = [k for k, v in top50 if v["quartz_frac"] < GATE]

    q_order = {k: i for i, (k, _) in enumerate(
        sorted(ok.items(), key=lambda kv: -kv[1]["quartz_frac"]), 1)}
    c_order = {k: i for i, (k, _) in enumerate(by_charge, 1)}
    MAFIC = ("gabbro", "anorthosite", "norite", "diabase", "dolerite", "basalt")
    moves = []
    for k, v in ok.items():
        blob = " ".join(str(x) for x in (v.get("pathway_counts") or {})).lower()
        terms = " ".join(str(vv.get("pathways")) for vv in v["vertices"]).lower()
        if any(m in terms for m in MAFIC):
            moves.append(q_order[k] - c_order[k])
    moves.sort()
    med_move = moves[len(moves) // 2] if moves else None

    bars = dict(i_distinct=(rho is not None and rho < 0.7),
                ii_consequential=(len(gated_out_in_top50) / 50 >= 0.20 if top50 else False),
                iii_mafic_moves=(med_move is not None and med_move >= 50))
    out = dict(leg="A13 generalised charge term",
               frozen="Day 199, 2026-08-18; pathways, weights, prediction and bars in "
                      "charge_term.py docstring before the first query",
               evidence_grade_freund="SECONDARY -- 10-50x figure not confirmed against "
                                     "primary text; see docstring",
               population=len(ok), errors=len(state["done"]) - len(ok),
               pathways={p: dict(weight=w, terms=list(t)) for p, (w, t) in PATHWAYS.items()},
               spearman_charge_vs_quartz=rho,
               top50_by_charge=[k for k, _ in top50],
               top50_gated_out_by_quartz=gated_out_in_top50,
               n_mafic=len(moves), median_rank_move_mafic=med_move,
               bars=bars, rows=ok)
    json.dump(out, open("data/charge_term.json", "w"), indent=1)
    print(f"[A13] rho={rho} | {len(gated_out_in_top50)}/50 of top-50 were gated OUT by "
          f"quartz | mafic median rank move={med_move} | bars={bars}", file=sys.stderr)
    print("[A13] wrote data/charge_term.json", file=sys.stderr)
