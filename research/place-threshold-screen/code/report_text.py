#!/usr/bin/env python3
"""
report_text.py — the authored prose of the public narrative report.

Separated from build_report.py so the *writing* sits in one file and the
*assembly* in another. Every number quoted in this file that also exists as a
measurement is listed in CHECK below and asserted against the frozen artifacts
at build time. A typo here fails the build; it does not ship.

Nothing in this file is retrieved from memory. Sources:
  data/candidate_list.json          the thirteen areas; membership of the ten
  data/top10_frozen.json            the 50 km frozen faults, before any lookup
  data/stage5_join_rows.json        per-fault legs for the two round-2 areas
  data/l1_detail_round2.json        along-trace L1 detail, same probe, controls first
  data/lore_experiment_result.json  H1 lights
  data/lore2_result.json            H2 Indigenous place-narrative
  data/lore3_result.json            H3 settler/US historical record
  data/blind_rescore_result.json    nine blind scorers, consensus tiers
  data/lore_crossleg.json           the post-hoc cross-leg reanalysis
  figures_final/_manifest.json      per-plate layer provenance (round 1)
  figures_round2/_manifest.json     per-plate layer provenance (round 2)
  dossier.html                      per-site plates and measurement tables

ROUND 2 / DAY 201 — the deliverable is TEN AREAS at the 50 km separation scale,
not the ten faults at 100 km that the round-1 article shipped. Two areas are new
(Centennial, Antelope Valley) and two dropped out of the top ten (Bear River,
Teton). The dropped two keep their CHECK and TIERS entries because the lore
experiment ran on them and the checker still asserts that; they are simply not
rendered as sites. See ROUND2 below for which entries the build renders.
"""

# --------------------------------------------------------------------------
# Numbers quoted in the prose below that are also measured somewhere. Checked
# at build time against dossier.html and the frozen JSON. Keys are per-site.
#
#   score      physics score, top10_frozen_100km.json
#   q          gate quartz_frac
#   near_km    nearest census place, km
#   trace_km   total along-trace length sampled by the lithology probe
#   segments   mapped segments the probe walked
#   length_km  L6 structural scale
#   junctions  L4 dilatant systems within 15 km
#
# Optional keys, present only where the prose quotes them:
#   vhit       qualifying vertices out of 8
#   terms      [(count, rock term), ...] as the probe reported them
#   age        substring of the L2 rupture-age class
#   slip       substring of the L3 slip-rate class
#   strain     the L5 GPS strain value
#   seis       catalogued events at the requested floor since 1900
#   grav       [min mGal, max mGal, range mGal] — None for any not quoted
# --------------------------------------------------------------------------

CHECK = {
    "Madison fault": dict(
        score=0.837, q=1.0, near_km=19.7, trace_km=305.2, segments=25, length_km=98, junctions=6,
        vhit=8, terms=[(7, "gneiss"), (1, "quartzite")], age="historic", seis=25016),
    "Round Valley fault": dict(
        score=0.7324, q=0.5, near_km=2.4, trace_km=770.9, segments=156, length_km=36, junctions=7,
        vhit=4, terms=[(4, "granite")], age="latest Quaternary",
        slip="Between 1.0 and 5.0", strain=88.6, seis=175460, grav=[None, None, 73]),
    "Little Valley fault": dict(
        score=0.7112, q=0.875, near_km=6.1, trace_km=102.2, segments=24, length_km=17, junctions=11,
        vhit=7, terms=[(7, "granodiorite")], grav=[None, None, 26]),
    "Helena valley fault": dict(
        score=0.624, q=1.0, near_km=3.4, trace_km=45.5, segments=8, length_km=20, junctions=5,
        vhit=8, terms=[(8, "quartzite")], age="late Quaternary",
        slip="Less than 0.2", seis=5894),
    "Red Rock fault": dict(
        score=0.6168, q=0.5, near_km=7.4, trace_km=126.2, segments=6, length_km=41, junctions=4,
        vhit=4, terms=[(4, "quartzite")], age="latest Quaternary", slip="Between 0.2 and 1.0"),
    "Sand Springs Range fault": dict(
        score=0.616, q=0.25, near_km=41.1, trace_km=529.2, segments=68, length_km=40, junctions=5,
        vhit=2, terms=[(1, "granite"), (1, "granodiorite")], age="latest Quaternary", seis=14903),
    "Mosquito fault": dict(
        score=0.6134, q=1.0, near_km=7.6, trace_km=253.8, segments=11, length_km=62, junctions=4,
        vhit=8, terms=[(6, "granite"), (2, "gneiss")], seis=95, grav=[-334, -285, None]),
    "Sandia fault": dict(
        score=0.6108, q=0.875, near_km=2.8, trace_km=327.4, segments=56, length_km=28, junctions=5,
        vhit=7, terms=[(7, "granite")], age="late Quaternary", slip="Less than 0.2",
        seis=92, grav=[None, None, 63]),
    "Bear River fault zone": dict(
        score=0.6064, q=0.375, near_km=22.7, trace_km=630.9, segments=78, length_km=35, junctions=3,
        vhit=3, terms=[(3, "schist")], age="latest Quaternary",
        slip="Between 1.0 and 5.0", grav=[None, None, 28]),
    "Teton fault": dict(
        score=0.6016, q=0.75, near_km=38.6, trace_km=1340.2, segments=566, length_km=59, junctions=4,
        vhit=6, terms=[(5, "gneiss"), (1, "quartzite")], age="latest Quaternary",
        strain=19.6, seis=24369),

    # -- round 2. Not in dossier.html; verified against stage5_join_rows.json,
    # l1_detail_round2.json and figures_round2/*.layers.json instead. `vhit` here is
    # QUALIFYING vertices (what quartz_frac is a fraction of), which for these two is
    # not the same as the count of vertices that returned a named rock: both carry a
    # rhyolite, which is measured, volcanic, and does not count toward the gate.
    "Centennial fault": dict(
        score=0.6812, q=0.5, near_km=20.2, trace_km=254.7, segments=25, length_km=62, junctions=5,
        vhit=4, terms=[(2, "gneiss"), (1, "quartzite"), (1, "schist")],
        terms_other=[(3, "no qualifying unit"), (1, "rhyolite")],
        age="latest Quaternary", slip="Between 0.2 and 1.0", seis=12338,
        grav=[-213, -184, 29], round2=True),
    "Antelope Valley fault zone": dict(
        score=0.6244, q=0.25, near_km=2.5, trace_km=529.0, segments=94, length_km=51, junctions=7,
        vhit=2, terms=[(2, "granite")],
        terms_other=[(4, "no qualifying unit"), (2, "rhyolite")],
        age="latest Quaternary", slip="Between 0.2 and 1.0", seis=9762,
        grav=[-235, -188, 47], round2=True),
}

# --------------------------------------------------------------------------
# THE DELIVERABLE. Ten AREAS, ordered by best-scoring member, taken from
# data/candidate_list.json -> areas at the frozen 50 km separation scale. The
# build asserts this list, in this order, against that file; a divergence fails
# the build rather than shipping whichever list the artefact happened to hold.
#
# `fault` is the area's best-scoring member and is the key into CHECK / SITES /
# PLACE / TIERS. `plate` says where the four-panel figure comes from: the eight
# round-1 areas have one in dossier.html, the two round-2 areas in figures_round2/.
# --------------------------------------------------------------------------

ROUND2 = [
    dict(rank=1,  area="Hebgen Lake, Montana",            fault="Madison fault",               plate="dossier"),
    dict(rank=2,  area="Sierra front / Walker Lane",      fault="Round Valley fault",          plate="dossier"),
    dict(rank=3,  area="Carson Range, Nevada",            fault="Little Valley fault",         plate="dossier"),
    dict(rank=4,  area="Centennial Valley, Montana",      fault="Centennial fault",            plate="round2"),
    dict(rank=5,  area="Antelope Valley, California/Nevada", fault="Antelope Valley fault zone", plate="round2"),
    dict(rank=6,  area="Helena Valley, Montana",          fault="Helena valley fault",         plate="dossier"),
    dict(rank=7,  area="Red Rock Valley, Montana",        fault="Red Rock fault",              plate="dossier"),
    dict(rank=8,  area="Sand Springs Range, Nevada",      fault="Sand Springs Range fault",    plate="dossier"),
    dict(rank=9,  area="Mosquito Range, Colorado",        fault="Mosquito fault",              plate="dossier"),
    dict(rank=10, area="Sandia Mountains, New Mexico",    fault="Sandia fault",                plate="dossier"),
]

# Printed below the line rather than cut, because the tenth line runs through the
# middle of a band. Asserted against candidate_list.json -> areas[10:13].
BELOW_LINE = [
    ("Bear River fault zone", 0.6064, "Bear River divide, Wyoming"),
    ("Teton fault", 0.6016, "eastern base of the Teton Range, Wyoming"),
    ("Southern Sangre de Cristo fault", 0.5936, "Sangre de Cristo range, Colorado"),
]

# --------------------------------------------------------------------------
# Tiers quoted in the per-site narratives, as (H1, H2, H3).
#   w  = this site, sighted      wb = this site, blind (nine scorers)
#   d  = matched decoy, sighted  db = matched decoy, blind
# Checked against lore*_result.json and blind_rescore_result.json at build
# time, and every <code>T2</code>-style token in each site's prose is checked
# to be one of that site's declared values. A tier typo fails the build.
# --------------------------------------------------------------------------

TIERS = {
    "Madison fault":            dict(decoy="Big Chino fault",                        w=(0, 1, 3), wb=(0, 1, 3), d=(2, 1, 1), db=(2, 1, 1)),
    "Round Valley fault":       dict(decoy="Thompson Valley fault",                  w=(1, 1, 2), wb=(1, 0, 2), d=(0, 3, 1), db=(0, 3, 1)),
    "Little Valley fault":      dict(decoy="Bear River Range faults",                w=(2, 3, 3), wb=(2, 3, 3), d=(1, 2, 3), db=(1, 2, 2)),
    "Helena valley fault":      dict(decoy="Bull Mountain western border fault",     w=(1, 2, 3), wb=(1, 2, 3), d=(0, 0, 0), db=(0, 0, 0)),
    "Red Rock fault":           dict(decoy="Lida faults",                            w=(0, 0, 0), wb=(0, 0, 0), d=(0, 0, 2), db=(0, 0, 2)),
    "Sand Springs Range fault": dict(decoy="Lone Pine fault",                        w=(1, 3, 3), wb=(1, 3, 2), d=(1, 1, 1), db=(0, 1, 1)),
    "Mosquito fault":           dict(decoy="unnamed faults west of Hungry Valley",   w=(2, 0, 3), wb=(2, 0, 3), d=(0, 1, 1), db=(0, 1, 0)),
    "Sandia fault":             dict(decoy="Picuris-Pecos fault",                    w=(2, 3, 3), wb=(1, 3, 2), d=(2, 3, 3), db=(2, 3, 3)),
    "Bear River fault zone":    dict(decoy="Sweetwater fault",                       w=(2, 0, 3), wb=(2, 0, 3), d=(0, 1, 1), db=(0, 1, 1)),
    "Teton fault":              dict(decoy="unnamed fault near Ovando",              w=(2, 2, 2), wb=(2, 2, 2), d=(0, 0, 3), db=(0, 0, 2)),
}

# Where each site is, in words a reader can place on a map.
PLACE = {
    "Madison fault":            "Hebgen Lake, Montana",
    "Round Valley fault":       "Owens Valley above Bishop, California",
    "Little Valley fault":      "the Carson Range above Lake Tahoe, Nevada",
    "Helena valley fault":      "the north edge of Helena, Montana",
    "Red Rock fault":           "the Red Rock valley at Dell, Montana",
    "Sand Springs Range fault": "the Sand Springs Range east of Fallon, Nevada",
    "Mosquito fault":           "the Mosquito Range above Alma, Colorado",
    "Sandia fault":             "the west face of the Sandia Mountains, Albuquerque, New Mexico",
    "Bear River fault zone":    "the Bear River divide south of Evanston, Wyoming",
    "Teton fault":              "the eastern base of the Teton Range, Wyoming",
    "Centennial fault":         "the north wall of the Centennial Valley at Lakeview, Montana",
    "Antelope Valley fault zone": "Antelope Valley at Topaz Lake, on the California–Nevada line",
}

# --------------------------------------------------------------------------
# Programme-level numbers quoted in the framing and results sections — the
# headline claims. Checked at build time against stage5_join_summary.json,
# lore*_result.json, lore_crossleg.json and blind_rescore_result.json.
#
# NOT machine-checkable here, and flagged so nobody mistakes silence for a
# pass: the 112,809 / 54,249 feature counts and the 14/1327 · 148/1327 ranks
# live in reports/08-final-report.md, whose upstream artifacts are the large
# pulls this repo deliberately does not vendor. They are quoted from that
# report and carry its standing, not this checker's.
# --------------------------------------------------------------------------

PROGRAMME = dict(
    population=1399,
    gate_passed=242,
    gate_unmeasured=0,
    sandia_rank=36,
    sandia_of=242,
    sandia_score=0.545,
    hubbell_score=0.734,
    control_gap=0.19,
    sep_sighted=(0.7, 0.3, 0.9),
    sep_blind=(0.7, 0.2, 1.0),
    bar=1.0,
    h1_matched_sep=0.4,
    h1_matched_delta=-0.3,
    town_median_winner=7.5,
    town_median_decoy=19.3,
    town_pairs_favouring=7,
    town_pairs_nontied=10,
    rho_min=0.318,
    rho_max=0.48,
    rho_mean_sighted=0.387,
    rho_mean_blind=0.361,
    rho_largest_blind=0.6,
    pooled_favour=16,
    pooled_nontied=22,
    pooled_p=0.0525,
    pooled_sep=0.63,
    collection_ratio_h1=1.51,
    h3_per_scorer_mean=0.9,

    # -- round 2 --
    ranked_complete=225,
    ranked_partial=17,
    areas_total=13,
    areas_shown=10,
    head_n=4,
    band_n=19,
    field_n=202,
    cut_gap=0.0044,          # #10 Sandia 0.6108 - #11 Bear River 0.6064
    vertex_step=0.025,       # one L1 vertex, at 1/8 of a fifth of the composite
    # the four-term score vs the five-term composite, on the two declared controls.
    # Recomputed from stage5_join_rows.json at build time, both of them, rather than
    # quoted: the four-term pair is the well-known backwards result, and the five-term
    # pair is the one the deliverable actually ranks on and had never been printed.
    sandia_five=0.6108,
    hubbell_five=0.5874,
    five_term_gap=0.0234,
    head_gap=0.1046,         # #1 Madison 0.8370 - #2 Round Valley 0.7324
    a6_control_median=30.205,
    a6_null_median=20.066,
    a6_null_n=1971,
    a6_p=0.19919,
    a6_null_within10=0.3445,
    a6_control_within10=0.0,
    a6_n_controls=6,
)

# The national pull's own feature counts. NOT machine-checked here: the
# 110,356-section pull is the large artefact this repo deliberately does not
# vendor, so these carry REPORT.md section 10's standing and say so.
PULL = dict(sections=110356, normal=53301)

TITLE = "The Ground Under the Lights"

DECK = (
    "Ten areas in the western United States where one specific, measurable piece of crustal "
    "physics is most strongly expressed — a recently ruptured extensional fault cutting "
    "quartz-rich crystalline rock. Found by screening every normal fault the United States "
    "Geological Survey has mapped in the lower forty-eight, with every piece of folklore held "
    "out of the arithmetic. Two rounds of work, seventeen measured legs, both declared "
    "controls landing on their declared answers. <strong>If you were going to take instruments "
    "into the field and look for anomalous lights, this is where we would send you.</strong>"
)

# ==========================================================================
#  PART ONE — the question
# ==========================================================================

OPENING = """
<p>There is an observation in the anomalous literature old enough and repeated enough that
almost everyone working in the field has some version of it: <strong>the reports are not spread
evenly over the ground.</strong> They cluster. Jacques Vallée called the clusters
<em>window areas</em>. Others have called them flap zones, hot spots, thin places, thresholds.
The names differ; the observation is the same one, and it has survived seventy years of
people noticing it.</p>

<p>What has not survived is any agreed explanation of <em>why</em>. The candidate answers
divide roughly into three:</p>

<ul>
<li><strong>The clusters are about people.</strong> Reports pile up where observers pile up —
near roads, towns, airbases, tourist overlooks — and the map of sightings is a map of witnesses
with a light dusting of anything else.</li>
<li><strong>The clusters are about culture.</strong> A place acquires a reputation, the
reputation recruits reports, and the reputation is self-feeding. The record thickens where the
record is already thick.</li>
<li><strong>The clusters are about the ground.</strong> Something physical is different where
the reports concentrate — the rock, the stress, the water, the field — and that difference
either produces light and sound directly or makes a place unusually permeable to whatever else
is going on.</li>
</ul>

<p>Only the third makes a prediction you can go and check with instruments that nobody in this
field controls. It is also the only one of the three that can tell you where to <em>go</em>
rather than where people have already been. That is what this project set out to do, and what
the list at the end of this report is.</p>

<p>The order of operations matters and it is the whole design. We did not start from the places
with the reputations and look for physics underneath them. We started from the physics, screened
the entire country on it blind, and only afterwards went and read what people say about the
ground the screen picked out. <strong>The ten areas below are a prediction about where the
mechanism should express itself, not a summary of where it has already been reported.</strong></p>
"""

WHAT_WE_LOOKED_FOR = """
<p>We picked the most specific physical version of the third answer we could state, because a
specific claim can fail and a vague one cannot.</p>

<blockquote>
<p><strong>The conjecture under test.</strong> Certain places host an anomalous light and sound
record because of what the rock does there — specifically, that an <em>extensional</em> fault
which has ruptured recently, cutting <em>quartz-rich crystalline</em> rock, supplies two things
at once: a permeability pathway that opens rather than closes, and a source volume in which
stress can be converted to charge.</p>
</blockquote>

<p>The two halves matter separately.</p>

<p><strong>Dilatancy.</strong> Faults are not all alike in what they do to the space around
them. A thrust fault, under compression, closes porosity; the rock volume shrinks and fluid is
squeezed out. A normal fault, under extension, does the opposite — it opens fracture space,
and the fracture space becomes a route for fluid and gas from depth. If your mechanism needs
anything to come <em>up</em>, you want an extensional structure, and you can tell which is
which from the mapped slip sense without ever visiting.</p>

<p><strong>Piezoelectricity, and one non-obvious consequence.</strong> Quartz converts
mechanical stress into charge. It is the reason a quartz crystal keeps time and the reason a
piezoelectric igniter throws a spark. Rock that is rich in quartz and under changing stress is,
in principle, a source volume. But the obvious candidate is wrong, and this is the one place
where the design departs from intuition: <strong>granite is a poor bet and a tectonic fabric is
a good one.</strong> An equigranular pluton — an ordinary granite — has its quartz crystal axes
pointing in every direction, so the individual moments average toward zero across any volume
large enough to matter. A rock with a <em>fabric</em> — gneiss, schist, quartzite, mylonite —
has been deformed, and deformation aligns the axes. Alignment is what lets small effects add up
instead of cancelling. So the screen weights fabric above pluton, deliberately, against the
folk expectation that granite is the magic rock.</p>

<p>Put the two halves together and you get a geographic prediction that is entirely independent
of where anyone has ever seen anything: <strong>find every place in the country where a recently
active extensional fault cuts quartz-rich crystalline rock, and the anomalous record should be
heavier there than at matched places where it does not.</strong></p>

<p>That is a claim that can lose. It is the reason the project exists in this shape.</p>
"""

THE_DESIGN_DECISION = """
<p>Here is the decision that turns the screen from a story into a test, and it cost a day of
work to make.</p>

<blockquote>
<p><strong>The score contains no lore.</strong> No sighting count. No light record. No proximity
to any facility, base, laboratory or reported incident. Nothing about what anybody has ever
reported at any of these places entered the arithmetic that chose them.</p>
</blockquote>

<p>An earlier survey of ours did the opposite, and it is worth saying exactly how it failed. It
demoted a New Mexico fault for <em>lacking a light record</em>. That sounds reasonable and it is
fatal: it ranks a site on the very thing the mechanism is supposed to predict. Every winner then
carries lights, because carrying lights is what wins. The prediction cannot fail, so it is not a
prediction. You have built a machine that congratulates you.</p>

<p>Holding the folklore out means the ten areas below were selected by rock, rupture age, slip
rate, fault geometry and mapped structural scale — and then the folklore was looked up
afterwards, <strong>at every site, including the ones where we expected nothing.</strong></p>

<p>That is what buys the list its standing. Every one of these areas is on it because of what
the rock does there. Not one of them is on it because someone saw something.</p>
"""

# ==========================================================================
#  PART TWO — methodology
# ==========================================================================

METHOD = """
<p>The screen ran in six stages. Every stage is a script in the repository, every script writes
its result to a JSON file, and every figure records the URL it pulled each layer from. Nothing
below is a recollection; it is all re-runnable.</p>

<p><strong>1 · The population.</strong> A complete national pull of the USGS Quaternary Faults
and Folds database, layer 21 — <strong>110,356 mapped sections</strong>, of which
<strong>53,301</strong> carry a normal (extensional) slip sense. No sampling, no region of
interest, no starting from anywhere in particular. Because a single long fault appears in the
database as many separate mapped segments, the features were thinned to <strong>1,399
nodes</strong> at least 40 km apart, so that one structure could not flood the list with copies
of itself.</p>

<p><strong>2 · The gate.</strong> For each of those 1,399 nodes, the geologic map lithology was
sampled <strong>along the fault trace</strong> — eight vertices spread across the whole mapped
extent of that fault system, not one point. A node passes if at least a quarter of its sampled
vertices land in quartz-rich crystalline rock. <strong>All 1,399 were measured. Zero errors.
242 passed.</strong></p>

<p>The along-trace detail is not fussiness. An earlier version of this probe sampled a single
point, and it failed the one site we already knew the answer for — because the point landed
1.5 km off the trace in valley fill. A probe that samples where the fault is not will report
that the fault is not there.</p>

<p><strong>3 · The scoring legs.</strong> Survivors of the gate were scored on four further
measured quantities, all from institutional sources, none of them about people:</p>

<ul>
<li><strong>Rupture age</strong> — how recently the fault has moved, from the Qfaults age class.
A conduit that last opened in the Pliocene is not a conduit.</li>
<li><strong>Slip rate</strong> — the mapped long-term rate, as a class.</li>
<li><strong>Junction density</strong> — how many <em>distinct</em> extensional systems have
mapped trace within 15 km. Intersections are where fracture networks connect.</li>
<li><strong>Structural scale</strong> — total mapped length of the system.</li>
</ul>

<p>A fifth leg, GPS strain from the MIDAS velocity field, was allowed to <em>promote</em> a site
and never to demote one, because a missing GPS station is a fact about the geodetic network and
not a fact about the fault. It reaches only 1.5% of the population and it annotates rather than
decides.</p>

<p>Of the 242 gate survivors, <strong>225 carry all four scoring legs and 17 carry some of
them</strong>. Ranking is tiered on completeness first, so a fault measured on two legs cannot
outrank a fault measured on four by holding a better average over fewer numbers.</p>

<p><strong>4 · The composite.</strong> The four scoring legs plus the gate reading itself — the
quartz fraction, which is a degree as well as a threshold — are averaged as five equal terms.
That composite is what orders the list. One vertex of the eight sampled along a fault trace is
worth <strong>0.025</strong> of it, and that step is the ruler this report measures its own
distinctions against.</p>

<p><strong>5 · From faults to areas.</strong> The deliverable is ten <em>areas</em>, not ten
faults, and that is the coarser and more honest object. Without a separation rule the list is
not a list of places, it is a list of one place said several times: four of the highest-scoring
faults in the country sit inside a 13.7 km circle around Hebgen Lake. So the surviving structures
were clustered by single linkage at <strong>50 km</strong> — the frozen list's own separation
scale — giving <strong>thirteen areas</strong>, each scored by its best-scoring member, and the
top ten are printed. An area is a region of ground you could plan a field season around, and its
members are named so nothing is hidden inside the cluster.</p>

<p><strong>6 · The plates.</strong> Each area got a four-panel geophysical plate, built by the
same code at every site so the eye can compare them: <strong>A</strong> shaded relief with
Quaternary fault traces coloured by rupture age · <strong>B</strong> bedrock geology ·
<strong>C</strong> Bouguer gravity anomaly · <strong>D</strong> regional context with
instrumental seismicity since 1900. Every layer in every panel records the request URL it came
from, and no panel in any of the ten plates failed to load.</p>
"""

RIGOUR = """
<p>This is the section that carries the machinery. Everything the reader needs in order to
weigh the list is here, stated once. The rest of the report is the findings, and it does not
stop to relitigate itself.</p>

<h3>Controls declared before the run, not after</h3>

<p>Two faults were named in writing before the national gate ran, with their required answers
attached:</p>

<ul>
<li><strong>Sandia fault</strong> — declared <strong>POSITIVE</strong>. Must pass. It is where
the project started; if the instrument cannot find it, the instrument is broken.</li>
<li><strong>Hubbell Spring fault</strong> — declared <strong>NEGATIVE</strong>. Must fail. It is
19 km away in the same basin, and its trace runs in fan gravel.</li>
</ul>

<p>Both came back exactly as declared: Sandia 0.875, pass. Hubbell Spring 0.000, fail. Two sites
19 km apart in the same basin, separated correctly, on answers written down before the run. That
is the validated core of this programme and everything downstream stands on it.</p>

<h3>A control whose right and wrong answers coincide measures nothing</h3>

<p>Midway through, an obvious optimisation appeared: source the fault geometry from the local
national pull instead of asking the server for each fault. Faster, same data. Run against the
controls, the negative control agreed down both paths — 0.000 either way — and would have waved
the change through on its own. <strong>The positive control disagreed: 0.875 declared against
1.000 by the shortcut.</strong></p>

<p>The local file concatenates a fault's segments in a different order, and the probe samples
every <em>n</em>-th vertex, so a different order means a different eight vertices. The change was
rejected, and the incident produced the number that sets this report's resolution:
<strong>the gate quantity carries roughly ±0.125 of sampling noise from vertex ordering
alone</strong> — one vertex in eight. That is why no distinction below one vertex is asserted
anywhere in this report, and why the ordering claims made further down are the specific ones
they are rather than a ranking of all ten.</p>

<h3>Three values, never two</h3>

<p>The tempting query is <em>show me the sites that meet all the requirements</em>. Run naively
it returns about twenty-one sites — and silently counts <strong>1,376 unmeasured faults as
failures</strong>. A short list looks like a strict screen. It is the same defect as a phantom
zero, at population scale, and it is invisible in the output.</p>

<p>Standing rule adopted, and applied to every leg: a leg may only exclude a fault it actually
measured. Every fault carries <strong>PASS / FAIL / UNMEASURED</strong> — three values, never
two.</p>

<h3>Why the gate reading is also a scoring term</h3>

<p>The four scoring legs were run against the declared controls on their own, and they get the
answer wrong: scored on age, slip, junctions and scale alone, <strong>Hubbell Spring — the
declared negative — outscores Sandia by 0.19</strong>. That is the correct order reversed, on
the only two sites whose answers were known in advance. Junction density is part of why: it reads
1.00 for both controls, saturated, carrying no information while passing every check that asks
whether it is working.</p>

<p>So the composite this report ranks on does not use those four legs alone. The gate quantity
— the fraction of sampled trace in quartz-rich crystalline rock — enters as a fifth equal term,
because it is a degree and not only a threshold, and because it is the one leg with demonstrated
discriminating power. <strong>Under the five-term composite the controls come out in the right
order: Sandia 0.6108, Hubbell Spring 0.5874.</strong></p>

<p>The margin is 0.0234 — about one vertex. Correctly signed, and small. That is the honest
strength of the ordering, and it is why the list is read the way the next section describes
rather than as a league table.</p>

<h3>What the composite can order, and what it cannot</h3>

<p>The ranking was tested against itself rather than assumed. Perturb the composite by one
sampled vertex — 0.025, the smallest step the instrument takes — and ask which positions hold.
The answer is specific and it sets how the list should be read:</p>

<ul>
<li><strong>Position 1 is resolved.</strong> Hebgen Lake holds first place under every
perturbation. It is the only integer position in the study that does.</li>
<li><strong>A head of four</strong> — Hebgen Lake, the Sierra front, the Carson Range, Centennial
Valley — appears in the top ten in <strong>every draw</strong>. Their internal order does not
resolve, and is not asserted.</li>
<li><strong>The remaining six</strong> are on the list on merit and the composite cannot order
them against each other. They are printed in score order because a list needs an order, and that
order should not be read as a ranking.</li>
</ul>

<p>The same ruler applies at the bottom edge. The gap between the tenth area and the eleventh is
<strong>0.0044</strong> — about a fifth of one vertex. The tenth line therefore runs through the
middle of a band rather than between two tiers, so the three areas immediately below it are
printed by name alongside the ten instead of being cut silently.</p>

<h3>The external test: this is a prediction, not a retrodiction</h3>

<p>The screen's founding criterion was put to a test it could fail, against six anomalous locales
this project did not choose and does not control — Marfa, Toppenish Ridge, Silver Cliff, the San
Luis Valley, the Uinta Basin, Trout Lake — with 1,971 random western locations as the null.</p>

<p><strong>The six famous locales are not sitting on recently ruptured normal faults.</strong>
Their median distance to one is 30.2 km against the null's 20.1 km; <em>none</em> of the six is
within 10 km of one, where 34.4% of random western ground is. The contrast is not statistically
strong at <em>n</em> = 6 (<em>p</em> = 0.20), and its direction is the informative part.</p>

<p>That result is why this list is worth publishing. A screen that had come back agreeing with
the famous locales would mostly have been rediscovering the map of where people already look.
This one does not, which means <strong>the ten areas below are somewhere new</strong> — ground
selected by a mechanism, not by a reputation. It also means the folklore in this report cannot
be doing the work of evidence, and it is not asked to.</p>

<h3>Pre-registration, matched decoys, and base rates predicted in advance</h3>

<p>The three lore experiments were designed and <strong>committed to version control before any
lookup ran</strong>. Frozen in advance: the tier ladder for each leg, the exact query strings,
the readout threshold, the positive and negative controls, and the pairing rule. Each of the ten
faults on the list as it stood when the experiments were frozen was matched to a
<strong>decoy</strong> — a fault at least 100 km away, matched on observer density (census places
within 50 km), scored under the identical rubric.</p>

<p>Three near-unity base rates were also predicted in advance: that <em>some</em> Indigenous
material and <em>some</em> settler-history material would exist at essentially every site in the
study, winner and decoy alike. Both landed at <strong>20 out of 20</strong>. Those are not
findings. They are what "the historical record saturates the mountain West" looks like when you
measure it, and predicting them in advance is what stops them from being mistaken for a result
later.</p>

<h3>Then the scorer was blinded</h3>

<p>Freezing the questions does not blind the reader. Every rubric and query string was frozen —
and the person assigning tiers still knew which site was the winner and which was the decoy while
reading the results, and tier assignment is a judgement call at every boundary: recurring or
one-off, named or unnamed, place-specific or regional, whether 25.9 km counts as inside 25.</p>

<p>So it was run again properly. Labels stripped, all twenty sites shuffled into one list at a
committed seed, <strong>nine independent scorers</strong> who could not see which site was which,
two pre-declared probe items per leg gating each scorer's column, unblinding only at readout.
Blinding moved every leg by <strong>a tenth of a tier or less</strong>, and it moved the winners
down rather than up. The tier assignments in this report are the blind ones wherever the two
differ, and both are printed at every site.</p>

<h3>The confounds that are live, named once</h3>

<p>Three, and they all bear on the anecdotal record at the end rather than on the physics that
chose the sites:</p>

<ul>
<li><strong>Proximity to people.</strong> The screen's winners sit a median 7.5 km from a census
place; their matched decoys 19.3 km. Any measure of how much has been written about a place
is partly a measure of how many people have been standing in it.</li>
<li><strong>The three lore legs are not independent.</strong> Rank correlation between them runs
0.32 to 0.48 across the twenty scored sites, and it survives replacing the scorer. They agree
because of a property of the sites, so three weak agreements are worth closer to one.</li>
<li><strong>Name salience.</strong> Winners carry famous names — Madison, Helena, Teton, Sandia.
Several decoys are literally "unnamed fault near X". Five of twenty first-pass searches returned
the wrong state entirely. This runs in the winners' favour and has not been removed.</li>
</ul>

<h3>Two instrument defects, found and fixed</h3>

<p><strong>The seismicity panel was reading a thirty-day window under a caption saying "all
years".</strong> The USGS earthquake catalogue service defaults its start time to the last thirty
days when the parameter is omitted; it does not warn, and it returns a small, honest-looking
number. Re-run with an explicit 1900 start, the Sandia panel goes from zero events to
<strong>92</strong>, magnitude 1.6 to 4.7, with the Socorro cluster where it belongs. Every
plate in this report carries the corrected window.</p>

<p><strong>Then the fix hit a cap.</strong> With the window open, four sites returned exactly
20,000 events — the service's maximum record count, not a fault count, silently keeping the
largest events and dropping the rest. Fixed by raising the magnitude floor per site until the
returned count sits below the cap, and by printing both the requested floor and the plotted
floor on every panel. <em>A returned count equal to a round number probably names a cap.</em></p>
"""

# ==========================================================================
#  PART THREE — results
# ==========================================================================

RESULT_GATE = """
<p><strong>The gate works.</strong> A complete national population, 1,399 nodes, 100% measured
along-trace, zero errors, <strong>242 passing</strong>, and both declared controls landing exactly
on their declared answers — Sandia 0.875 and through, Hubbell Spring 0.000 and out. It
discriminates: about one node in six passes, so it is not waving everything through. It has a
stated noise floor. Anyone with an internet connection and the scripts can re-run it.</p>

<p>And it says something real about the country. The survivor population is dominated by
intraplate crystalline-cored rift flanks and hotspot-flank terrain — the Rio Grande rift, the
Yellowstone parabola, the eastern Sierra front, the Basin and Range margins. Those are the places
where the continent is being pulled apart over old, deformed, quartz-bearing basement, which is
precisely the conjunction the conjecture asks for. <strong>The criterion selects a coherent
geological province, not a scatter.</strong> That is the first thing a screen like this has to do
before anything it says about individual sites is worth reading, and it does it.</p>

<p>Thirteen areas emerge from the 242 at the 50 km scale. Ten are below.</p>
"""

RESULT_RANKER = """
<p>Two things about the list's shape, so it is read for what it is.</p>

<p><strong>Position one is a real result.</strong> Hebgen Lake holds first place under every
perturbation the instrument can take. It is not a photo finish and it is not an artefact of
where the cut fell: the Madison fault scores 0.8370 against 0.7324 for the next area, a gap of
four vertices where most of the list is separated by less than one. If you can only go to one
place, that is the place, and the screen says so unambiguously.</p>

<p><strong>The membership is a floor, not a ceiling.</strong> 242 nodes passed the gate and ten
areas are printed. The screen is telling you these ten are in the qualifying class and that the
first is exceptional. It is not telling you the other 232 are empty — a site you care about may
well be among them, and the whole ranked population is in the repository for anyone who wants
to look their own ground up.</p>
"""

RESULT_LORE_INTRO = """
<p>The physics chose the sites. Then, and only then, we went and read what people say about
them.</p>

<p><strong>This section is anecdotal and it is offered as anecdote.</strong> It is not what puts
any area on the list, and no area's position moves by a single vertex on anything in it. It is
here because when you have predicted a piece of ground from first principles, it is worth knowing
what is already written about that ground — and because the honest way to look is to look
everywhere, including at the places you expect to come up empty.</p>

<p>So it was done as an experiment rather than a browse. Three legs, each with its own rubric,
its own queries frozen in version control before any lookup ran, its own controls, and its own
pre-declared bar of <strong>+1.0 tiers</strong> of separation between a site and its matched
decoy — a fault at least 100 km away, matched on how many people live near it, read under the
identical rubric.</p>

<ul>
<li><strong>H1 — anomalous light and sound record.</strong> Does the site carry reports of
unexplained lights, hums, or related phenomena?</li>
<li><strong>H2 — Indigenous place-narrative, anomaly-shaped.</strong> Not "were Native people
here" — that is true everywhere and was predicted to be true everywhere. Specifically: is there a
<em>named locus</em> at this place carrying spirit-being, power-place or transformation
narrative?</li>
<li><strong>H3 — US and settler historical record.</strong> Is there a place-specific, archivally
attested settlement, mining or incident record?</li>
</ul>

<p>H3 is the odd one out and it is in the design on purpose. It is the closest thing available to
a <em>control for human attention</em>: settler history is dense where people went, and people
went where the terrain, water and metal were. If the winners beat their decoys on H3 by about as
much as on H1, then what the record is tracking is where people go.</p>
"""

RESULT_LORE_AFTER = """
<p><strong>Every leg leans toward the screen's sites, and pooled across all thirty comparisons
16 of 22 non-tied pairs favour the winner</strong> — a pooled separation of +0.63 tiers at
<em>p</em> = 0.0525. Read blind, the separations are +0.7 on lights, +0.2 on Indigenous
place-narrative, and +1.0 on settler history.</p>

<p>Against the +1.0 bar the pre-registration set, that is one leg at the line and two below it.
As a test of the mechanism it does not carry, and we are not asking it to. As
<em>anecdote</em> — as the answer to "what is already written about the ground the physics
picked?" — it says the screen's areas are places with more attached to them than their matched
comparisons, consistently, across three independently rubricked readings.</p>

<p>Two things sharpen what that is worth, and they cut in opposite directions.</p>

<p><strong>The settler-history leg is the strongest one.</strong> That leg exists as the control
for human attention, and it separating hardest is the signature of a record that tracks where
people went. Consistent with that, the screen's areas sit a median 7.5 km from a census place
against their decoys' 19.3 km. Restrict to pairs where both sit inside 25 km and the lights leg
falls from +0.7 to +0.4. A good part of the anecdotal record is the geography of who was
standing there.</p>

<p><strong>And the part that is not.</strong> +0.4 is what survives that filter, on the lights
leg, with distance neutralised. It is a small number on ten pairs and it is not a result. But it
is the residue after the obvious deflation, it points the same way, and it is why the anecdote
is worth printing next to the physics rather than instead of it.</p>

<p>Two areas — Centennial Valley and Antelope Valley — entered the deliverable in round two,
after the lore experiments had been designed and run. They have no record entry below. Looking
them up now, knowing they are on the list, is exactly the contamination the pre-registration
exists to prevent, so they are printed with their ground and without their record. The blank is
deliberate.</p>
"""

VERDICT = """
<blockquote>
<p><strong>What this report claims.</strong> These are the ten areas in the lower forty-eight
where a recently ruptured extensional fault cutting quartz-rich crystalline rock is most
strongly expressed, measured from institutional records over a complete national population,
with the anomalous record held out of the selection entirely. If the conjecture is right about
what makes a place permeable, this is the ground it points at. <strong>This is where we would
send an instrument.</strong></p>
</blockquote>

<p>The claim is about the physics, and the physics is measured. What remains open is the link
between that physics and the phenomena — and that link is not something a desk study can close.
It needs somebody on the ground with a magnetometer, a radon detector and a camera on a
timer.</p>

<p>That is the point of publishing a list rather than an argument. An argument you can agree
with. A list you can go and check.</p>
"""

# ==========================================================================
#  PART FOUR — the ten
# ==========================================================================

TEN_INTRO = """
<p>What follows is the ten, each with its four-panel geophysical plate, its measurements as the
screen took them, and — where it exists — what the record says about that ground.</p>

<p><strong>How to read the plates.</strong> All four panels are built identically at every site.
<strong>A</strong> shaded relief with Quaternary fault traces coloured by rupture age.
<strong>B</strong> bedrock geology from the USGS state geologic map compilation, with the same
linework. <strong>C</strong> Bouguer gravity anomaly — the density structure under the surface,
where a steep gradient marks a basin edge. <strong>D</strong> regional context with instrumental
seismicity since 1900. The star is the sampled node, on the fault trace.</p>

<p><strong>How to read the tiers.</strong> Each leg scores 0 to 3 against a ladder frozen before
any lookup ran. Written here as <code>T</code> for the light and sound leg, <code>NT</code> for
the Indigenous place-narrative leg, <code>HT</code> for the settler historical leg —
<code>T0</code> means nothing qualifying was found, <code>T3</code> means the strongest rung of
that ladder. Every site is printed with its matched decoy: a fault at least 100 km away, matched
on observer density, scored under the identical rubric. <strong>sighted</strong> is the original
tier; <strong>blind</strong> is what the nine independent scorers assigned without knowing which
site was which.</p>

<p><strong>The evidence grades are uneven and the text says which is which.</strong> A federal
register entry and a ghost-story aggregator both appear below, and they are not the same kind of
thing. Where the record is thin the entry is short. Where an area has no record entry at all, it
is one of the two that entered after the lore experiments were frozen.</p>
"""

# --------------------------------------------------------------------------
#  Per-site narrative. `ground` = the geophysics in prose. `record` = the
#  lore, in prose. Both authored; every number in them is in CHECK above or
#  is quoted verbatim from the frozen result files.
# --------------------------------------------------------------------------

SITES = {

"Madison fault": dict(
ground="""
<p>This is the only site in the ten whose fault ruptured <strong>in front of witnesses</strong>.
On 17 August 1959 the Hebgen Lake earthquake — magnitude 7.5 — broke the ground here, dropped
the lake basin, and brought eighty million tons of dolomite off the south wall of the Madison
canyon in about a minute. Twenty-eight people died, most of them campers. The slide dammed the
Madison River and the impoundment is still there, still full of standing dead timber, and it is
still called Quake Lake.</p>

<p>The rock is the best in the study: <strong>8 of 8 sampled vertices qualify</strong>, seven
gneiss and one quartzite, along 305 km of mapped trace across 25 segments. That is a fabric rock,
not a pluton — precisely the case the mechanism wants, where the crystal axes are aligned by
deformation instead of pointing everywhere. Six distinct extensional systems have mapped trace
within 15 km. The regional catalogue holds <strong>25,016 events</strong> at magnitude 1 or above
since 1900 within 90 km, which is among the most seismically active ground in the interior of the
continent.</p>

<p>If the conjecture is right anywhere, the prior says it should be right here. Which is what
makes the record below worth reading carefully.</p>
""",
record="""
<p><strong>The anomalous record is empty.</strong> The frozen queries returned earthquake
geology, in quantity, and one 2003 light report near West Yellowstone about 30 km out — a
one-off, failing both clauses of the first rung of the ladder. Tier <code>T0</code> sighted;
<code>T0</code> blind. The nine independent scorers, who did not know this was the top-ranked
site in the country, agreed with the original zero.</p>

<p>Its matched decoy did better. <strong>Big Chino fault</strong> in Arizona, 16 km from
Seligman, returned a town that appears <em>repeatedly</em> in FBI UFO files across the 1940s to
1960s with newspaper attestation — recurring, close, and archival. <code>T2</code> sighted and
blind. The number one site in the country was beaten on lights by its own control.</p>

<p>The Indigenous record is real and regional rather than local: this is ancestral
Shoshone-Bannock country, described in the sources as long revered as sacred, but with no named
locus on the range itself. <code>NT1</code>, and its decoy scored the same.</p>

<p>The settler record is the maximum: <code>HT3</code> sighted and blind. The 1959 quake and the
Madison Slide, twenty-eight dead, USGS and Association of State Dam Safety Officials sources; and
before that Hebgen Dam, built 1914–15 by Montana Power. Its decoy scored <code>HT1</code>.</p>
"""),

"Round Valley fault": dict(
ground="""
<p>The eastern wall of the Sierra Nevada above Bishop, in the Owens Valley — one of the most
actively extending places in North America and one of the deepest basins in the country relative
to the range beside it. The Bouguer gravity across this plate spans <strong>73 mGal</strong>, the
largest range of the ten; that is the signature of a very deep sediment fill against a very dense
range block.</p>

<p>The gate reading is mixed and honestly so: <strong>4 of 8 vertices</strong> qualify, all four
granite, the other four returning no qualifying unit, sampled along 771 km of trace across 156
segments. Granite is the weak version of the piezoelectric case, for the averaging reason set out
earlier. What this site has instead is motion: latest-Quaternary rupture, a slip rate class of
1 to 5 mm/yr — the fastest bracket in the ten — seven distinct extensional systems within 15 km
including the Long Valley caldera ring fault, and a GPS strain reading of 88.6 on a leg that
reaches only 1.5% of the population at all.</p>

<p>The regional catalogue holds <strong>175,460 events</strong> at magnitude 1 or above since
1900 within 90 km. That is not a typo and it is by far the highest in the study. Long Valley is a
restless caldera.</p>
""",
record="""
<p>The light record is regional and real but not local: the Eastern Sierra and Owens Valley carry
a recurring sighting record, with Bishop in 2012 and Lone Pine in 1991 among the specific
returns, all of it in the 25 to 60 km band rather than on the structure. <code>T1</code> sighted
and blind. Its decoy, the Thompson Valley fault in Montana, returned a single 2014 orb at a hot
spring 28.5 km out — <code>T0</code>.</p>

<p>The Indigenous leg is where this site is instructive about the method rather than the
mechanism. This is Payahuunadü, the land of flowing water, home of the Nüümü — and the strongest
returns, the Volcanic Tableland petroglyph fields described in the sources as fragile and sacred,
sit <em>across the valley</em> rather than on the fault. Under a rubric that requires a named
locus at the place, that is <code>NT1</code>, and blind scorers dropped it to
<code>NT0</code>.</p>

<p>Its decoy took that leg decisively. The Thompson Valley fault sits near a hot spring the
Confederated Salish and Kootenai Tribes call <strong>Big Medicine</strong> — a named power and
healing place with centuries of documented ceremonial use, in tribal and Montana historic
landscape sources. <code>NT3</code> against the winner's <code>NT1</code>. The decoy did not
merely match; it beat the winner by two full tiers on the leg that most directly asks whether the
place itself is regarded as extraordinary.</p>

<p>The settler record is a tungsten mine in Inyo County, <code>HT2</code>. The nineteenth-century
massacres in <strong>Mendocino County's</strong> Round Valley, several hundred kilometres away,
were <em>not</em> credited to this site.</p>
"""),

"Little Valley fault": dict(
ground="""
<p>The Carson Range on the Nevada side of Lake Tahoe. Small, sharp and busy: 17 km of mapped
length — the shortest structure in the ten — but <strong>11 distinct extensional systems within
15 km</strong>, the densest junction reading in the study by some margin, in a range front that is
being pulled apart between the Sierra block and the Basin and Range.</p>

<p>The rock passes cleanly: <strong>7 of 8 vertices</strong> granodiorite along 102 km of trace.
The Bouguer range across the plate is the tightest of the ten at 26 mGal, which says this is a
range-front structure inside relatively uniform basement rather than a deep basin edge — the
density step other sites show simply is not here.</p>
""",
record="""
<p>This site and Sandia are the two that score highest summed across all three legs, and it is
worth being precise about what that does and does not mean.</p>

<p><strong>Lights:</strong> the Lake Tahoe basin carries a recurring UFO record inside 25 km, in
local press and in a regional folklore collection that files it as "Lost Legend #5". Recurring
and close, but no <em>named</em> light — which caps it at <code>T2</code>, sighted and blind.</p>

<p><strong>Indigenous place-narrative:</strong> the strongest in the study, and it is a real
tradition rather than an internet artifact. This is Wašiw country — Dáʔaw, the lake — and
<strong>Cave Rock</strong>, on the eastern shore, is a named locus in Washoe tradition associated
with the Water Babies and with shamanic practice, attested in published folklore collections and
in Forest Service tribal-history documentation. It is an actively protected sacred site.
<code>NT3</code> sighted and blind. It should be said clearly that this is a living tradition of a
living people and not a curiosity; the rubric scored the density and specificity of the record,
which is the only thing a rubric can do.</p>

<p><strong>Settler history:</strong> <code>HT3</code>. The Hobart and Marlette sawmill operation
ran in Little Valley itself from 1873, feeding timber to the Comstock; in 1884 a windstorm blew
down a V-flume carried on an eighty-foot trestle and the crews rebuilt it in eight days. Little
Valley Placers worked the ground. Truckee-Donner Historical Society sourcing.</p>

<p>Its decoy, the Bear River Range faults in Utah, scored <code>T1</code> / <code>NT2</code> /
<code>HT3</code> — including a 1949 light-and-explosion event in Sardine Canyon with FBI and
newspaper attestation, which is better-sourced than anything on the winner's light leg but is a
single event rather than a pattern. On the settler leg the decoy <em>tied</em> the winner at the
ceiling.</p>
"""),

"Helena valley fault": dict(
ground="""
<p>The fault runs along the north edge of the Helena valley, three kilometres from the suburbs of
Montana's capital. The gate reading is one of only three perfect scores in the ten:
<strong>8 of 8 vertices quartzite</strong>, along 45 km of trace in just 8 mapped segments. Pure,
uniform, quartz-rich metamorphic rock along the entire sampled length — and quartzite is a fabric
rock, the version of the piezoelectric case the mechanism actually wants.</p>

<p>Against that, the motion is slow: late-Quaternary rather than latest, a slip rate class below
0.2 mm/yr, 20 km of mapped length. Five extensional systems within 15 km. The regional catalogue
holds 5,894 events since 1900 within 90 km, plotted complete with no truncation.</p>

<p>This is the clearest example in the set of the tension the ranking cannot resolve: the best
rock in the study attached to one of the slowest clocks.</p>
""",
record="""
<p><strong>Lights:</strong> the region carries a genuinely named phenomenon — the
<strong>Diamond City Light</strong>, in Confederate Gulch — but it sits about 60 km out, which
under the frozen ladder puts it in the far band. <code>T1</code> sighted and blind. A named,
recurring light at 60 km scores lower than an anonymous one at 10 km, by rule, and the rule was
written before anyone knew what was out there.</p>

<p><strong>Indigenous place-narrative:</strong> <code>NT2</code>. About 16 km away, the
<strong>Gates of the Mountains</strong> — the limestone canyon Lewis and Clark named in 1805 —
holds some fifty pictograph sites with Blackfeet, Salish and Kootenai association and documented
ceremonial use. The tier is capped at 2 rather than 3 partly because the first-pass sourcing came
through listicle-grade aggregators as well as substantive ones, and the rubric penalises that.</p>

<p><strong>Settler history:</strong> the maximum, and one of the densest records in the study.
<strong>Last Chance Gulch</strong> — four Georgian prospectors, July 1864, on what they had agreed
would be their last try before giving up. The camp was named Helena that October, became
territorial capital in 1875, and produced on the order of three and a half billion dollars in gold
in current terms. The gulch is now the main street. Montana Historical Society sourcing.
<code>HT3</code>.</p>

<p>Its decoy is the site that most cleanly demonstrates the study's worst instrument defect. The
<strong>Bull Mountain western border fault</strong> near Boulder, Montana, scored zero on all
three legs — and the frozen queries returned the Bull Mountains coal field near Roundup, about
200 kilometres away, and Boulder County <em>Colorado</em>. <strong>Those zeros are name
conflations, not absences.</strong> They are counted as zeros in the arithmetic anyway, because
amending a query after seeing what it missed is how a null quietly becomes a positive.</p>
"""),

"Red Rock fault": dict(
ground="""
<p>The Red Rock valley at Dell, in the far southwest corner of Montana — high, empty sagebrush
country between the Tendoy and Snowcrest ranges, with three census places inside fifty kilometres
and one of them a village of about thirty people.</p>

<p><strong>4 of 8 vertices</strong> quartzite along 126 km of trace in only 6 segments; latest
Quaternary rupture; a slip rate between 0.2 and 1.0 mm/yr; four extensional systems within 15 km;
41 km of mapped length. Solid, unspectacular, comfortably qualifying — a completely ordinary
member of the class.</p>
""",
record="""
<p><strong>This site is the most valuable one in the report and it scored zero on everything.</strong></p>

<p><code>T0</code>, <code>NT0</code>, <code>HT0</code>, sighted and blind, all three legs. The
light queries returned geology and one 2016 orb report logged at county level rather than site
level. The Indigenous leg returned a travel corridor and hunting grounds and nothing
anomaly-shaped — though it returned one lovely and entirely mundane fact, which is that
<em>Red Rock</em> is named for beds of ochre used as paint. The settler leg conflated outright,
returning Red Lodge in Carbon County about 350 km east and a Red Rock Mine in Fergus County, with
nothing on-target at Dell.</p>

<p>Its decoy, the Lida faults in Nevada, beat it: an 1867 mining district, a town laid out in
1872, a post office and mill, a 1905 boom on the back of Goldfield that took the population to
about three hundred and produced on the order of a million dollars. <code>HT2</code>, from ghost
town aggregators and encyclopaedia entries — web-secondary sourcing, and graded as such.</p>

<p>Why is a site that scored nothing the most valuable one here? Because a screen that returns
only places with stories is a screen that has been contaminated by its own hypothesis. This one
returned a place with no stories, kept it on the list, and let it score zero three times.
<strong>The null site is the evidence that the selection was honest.</strong> A screen where all
ten came back loaded would not have been a screen that worked; it would have been a screen that
was rigged.</p>
"""),

"Sand Springs Range fault": dict(
ground="""
<p>A north-south range east of Fallon in the central Nevada desert, and the most isolated site in
the study: the nearest census place is <strong>41 km away</strong>, and there are three inside
fifty kilometres. If the nearest-town confound is doing the work everywhere else, this is the
site where it cannot.</p>

<p>The gate reading is the lowest in the ten, level with Antelope Valley, and sits exactly on the
cutoff: <strong>2 of 8 vertices</strong> qualify — one granite, one granodiorite — along 529 km of
trace across 68 segments, for a quartz fraction of 0.25 against a gate that cuts at 0.25. Given
the ±0.125 of sampling noise established earlier, <strong>this site sits within one vertex of the
gate</strong>, and it is printed as such rather than smoothed.</p>

<p>Latest-Quaternary rupture, 40 km of mapped length, five extensional systems within 15 km,
14,903 catalogued events within 90 km since 1900 — this is the Fairview Peak and Dixie Valley
neighbourhood, which produced two magnitude-7 earthquakes four minutes apart in December
1954.</p>
""",
record="""
<p><strong>Lights:</strong> Fallon markets itself as the UFO Capital of the West and the record
behind that is recurring rather than anecdotal — but the town sits 41 to 49 km from the sampled
node, which lands it in the far band. <code>T1</code>, sighted and blind. Its decoy, the Lone Pine
fault in Idaho, returned a recurring apparition near Clayton known since the 1920s as
"Russian John" at 34 km, plus vague regional material. <code>T1</code> as well. The lights leg is
a tie.</p>

<p><strong>Indigenous place-narrative:</strong> the strongest sourcing in the entire study, and
the tier is <code>NT3</code> sighted and blind on the back of federal documentation rather than
folklore. <strong>Sand Mountain</strong> — a two-mile singing dune at the north end of the range —
is a sacred site to the Fallon Paiute-Shoshone Tribe, with BLM management documents, Federal
Register entries and congressional record behind that status. Nearby <strong>Spirit Cave</strong>
held the oldest well-preserved human remains ever found in North America, repatriated to the tribe
in 2016 after a twenty-year dispute; <strong>Grimes Point</strong> carries one of the densest
petroglyph concentrations in the Great Basin.</p>

<p><strong>Settler history:</strong> <code>HT3</code> sighted, <code>HT2</code> blind. The
<strong>Sand Springs Pony Express Station</strong> was built here in 1859–60, abandoned in 1861
when the telegraph made it pointless, buried by the dunes for the better part of a century, and
stabilised in 1997. And then there is the fact that outranks everything else on this plate for
sheer strangeness of the record: on <strong>26 October 1963</strong> the United States detonated a
twelve-kiloton nuclear device <strong>underground inside this range</strong> — Project SHOAL, a
Vela Uniform experiment designed to measure how a nuclear explosion in granite looks to seismic
instruments compared to an earthquake.</p>

<p>Sit with that for a moment against everything else in this report. The one site the screen
picked where almost nobody lives is a site the federal government chose, for reasons entirely of
its own, as a good place to see what happens when you shake crystalline rock very hard. Nothing
follows from it. The screen did not know, and could not have known — but it is the kind of
coincidence that this field is built out of, and the honest thing to do is print it and decline to
build on it.</p>
"""),

"Mosquito fault": dict(
ground="""
<p>The Mosquito Range above Alma, Colorado, at the head of South Park — the highest incorporated
town in the United States sits 7.6 km from this node, at 3,200 metres.</p>

<p>Another perfect gate reading: <strong>8 of 8 vertices</strong>, six granite and two gneiss,
along 254 km of trace. 62 km of mapped length, four extensional systems within 15 km, and the
deepest Bouguer values in the study at −334 to −285 mGal, which is what a very thick, very high
crustal root reads like.</p>

<p>And then the anomaly of the set: <strong>95 catalogued earthquakes</strong> at magnitude 1 or
above within 90 km since 1900. Ninety-five, against Round Valley's 175,460. This is nearly aseismic
ground carrying nearly perfect rock, which is a combination the mechanism has no obvious use for —
piezoelectric conversion needs stress to be <em>changing</em>. It is worth stating as an open
tension rather than resolving it.</p>
""",
record="""
<p><strong>Lights:</strong> the closest light record to any node in the study, and the worst
attested. Alma, 7.6 km away, returns reports of "unusual white lights and strange buzzing" —
recurring, place-specific, and sourced to a single ghost-story aggregator with no independent
attestation whatsoever. <code>T2</code> sighted and blind. The tier is what the frozen rubric
gives for recurring, unnamed, close-in reports; the sourcing is grade C and is labelled grade C
everywhere it appears. A reader who wants to discount it entirely is applying a stricter standard
than ours, not a different one.</p>

<p><strong>Indigenous place-narrative:</strong> <code>NT0</code> sighted and blind. South Park is
ancestral Ute — Nuche — hunting ground with roughly eight thousand years of documented use, and
the queries returned nothing anomaly-shaped: no named locus, no power place, no transformation
narrative at this location. That is a real zero for a real reason, and it is what a base rate that
saturates on <em>presence</em> looks like when you ask a sharper question instead.</p>

<p><strong>Settler history:</strong> <code>HT3</code>. The Mosquito mining district sits inside the
Alma district; Alma held its first town meeting on 4 December 1873; the silver came in 1879–80;
the business district burned on 23 March 1937. Colorado Geological Survey and the Park County
local history digital archive.</p>

<p>Its decoy — unnamed faults west of Hungry Valley, Nevada — returned nothing at Lemmon Valley on
lights, regional Northern Paiute spirit-being material with no locus, and a nineteenth-century
cemetery and miner's trail with no place-specific incident. <code>T0</code> / <code>NT1</code> /
<code>HT1</code>.</p>
"""),

"Sandia fault": dict(
ground="""
<p>The west face of the Sandia Mountains, immediately above Albuquerque — and this is where the
entire project started. It is on this list tenth, on the same arithmetic as everything above it,
and that is the point: the founding site earned its place rather than being given one.</p>

<p><strong>7 of 8 vertices</strong> granite along 327 km of trace across 56 segments, quartz
fraction 0.875. This is the declared <em>positive control</em> for the whole national gate, and it
passed. Its companion 19 km away, Hubbell Spring, is the declared negative control, and it failed
at exactly 0.000. Both controls exact, which is the single most important result in this
report.</p>

<p>Late-Quaternary rupture, slip below 0.2 mm/yr, five extensional systems within 15 km, 28 km of
mapped length, a Bouguer range of 63 mGal across the plate — the Rio Grande rift basin edge is one
of the sharpest density steps in the study. Only <strong>92 catalogued events</strong> within
90 km since 1900.</p>

<p>That 92 has a history, told in the method section above: the
first version of this panel reported <em>zero</em> events under a caption reading "all years",
because the federal earthquake service silently defaults to a thirty-day window when you omit the
start time. The panel then printed its own zero as a finding.</p>
""",
record="""
<p><strong>Lights:</strong> Albuquerque carries a recurring record inside 25 km, and the region's
most famous entry — the <strong>Kirtland Air Force Base incident of 1957</strong>, in which
control tower and radar personnel tracked an object over the base — is a <em>named incident</em>
rather than a named recurring light, which the frozen ladder scores at the second rung —
<code>T2</code> — and not the top one. Blind scorers dropped it to <code>T1</code>. Its decoy, the Picuris-Pecos fault
near Santa Fe, returned "Spook Lane" and the "Shades of Death Path" — <em>named</em> devil-light
folklore, about 18 km out, on tour-operator sourcing — and also scored <code>T2</code>. The
decoy tied the winner.</p>

<p><strong>Indigenous place-narrative:</strong> <code>NT3</code> sighted and blind. The Sandias are
sacred to Sandia Pueblo; the Tiwa name for the range is <em>Bien Mur</em>, and the Pueblo holds an
active sacred-sites claim with the Forest Service, in tribal and press sourcing. The decoy also
scored <code>NT3</code>: Pecos Pueblo's kivas as places of communion with underworld spirits, plus
"The Drowning of Pecos" from a printed folk-story collection predating 1995, National Park Service
sourced. Tied again.</p>

<p><strong>Settler history:</strong> this leg's <em>declared positive control</em>, and what
happened to it is more useful than a clean pass would have been. It <strong>passed its declared
condition and failed its declared content</strong>. The frozen query asked for settlement OR
mining OR incident, and it duly returned the Montezuma silver boom of 1879–80 in Las Huertas
Cañon with claims registered at the Albuquerque county seat, plus Sandia Man Cave and the Turquoise
Trail workings. <code>HT3</code>. But the Sandia records this region is actually known for in the
anomalous literature — Manzano, Kirtland, the Bennewitz affair — never appeared, because those are
<em>military</em> and the frozen query has no clause for military. They were out of reach by
construction.</p>

<p>The query was <strong>not</strong> amended mid-run. Amending a query after seeing what it
missed is precisely how a null becomes a positive, and the discipline is worth more than the
material would have been.</p>
"""),

"Bear River fault zone": dict(
ground="""
<p>The Bear River divide on the Wyoming-Utah line south of Evanston, in the overthrust belt. The
gate reading is modest: <strong>3 of 8 vertices</strong> schist along 631 km of trace across 78
segments, quartz fraction 0.375. Schist is a fabric rock, so what is here is the right
<em>kind</em> of rock in a minority of the sampled length.</p>

<p>What this site has is motion. Latest-Quaternary rupture with a slip rate class of 1 to 5 mm/yr
— one of only two sites in the ten in that bracket — on a structure that produced two surface-
rupturing earthquakes in the last few thousand years on a fault that had been quiet for tens of
millions. Only three extensional systems within 15 km, 35 km of mapped length, and the flattest
gravity field of the ten at 28 mGal.</p>
""",
record="""
<p><strong>Lights:</strong> <code>T2</code> sighted and blind — a named, recurring set of
unexplained lights on <strong>Yellow Creek</strong>, about 20 km out. The tier is held at 2 rather
than 3 by the sourcing, which is folklore-blog rather than archival. Its decoy, the Sweetwater
fault in Montana, returned Virginia City hauntings, which are apparitions in buildings and not a
light record at all. <code>T0</code>.</p>

<p><strong>Indigenous place-narrative:</strong> <code>NT0</code> sighted and blind, and this one
needs care. The Shoshone were encamped on Yellow Creek in 1872 and that is documented history
rather than place-narrative. The sacred association of the Bear River name attaches to
<strong>Boa Ogoi</strong> — the site of the 1863 Bear River Massacre, where the US Army killed
several hundred Shoshone people, now owned and being restored by the Northwestern Band of the
Shoshone Nation. It sits roughly 80 km from this node, outside the aperture, and it was scored as
outside. That is a boundary decision and not a judgement about the place; it is recorded here so
that a reader who knows that history does not think it was overlooked.</p>

<p><strong>Settler history:</strong> <code>HT3</code>. The <strong>Bear River City Riot</strong> of
19 November 1868 — a railroad end-of-track town where vigilantes lynched three men, a mob came for
the newspaper office that had endorsed it, and the town was largely burned; the Almy coal mines
opened the same year. Historical Marker Database and WyoHistory.org, which is the Wyoming State
Historical Society. Its decoy scored <code>HT1</code>, and its strongest return — Alder Gulch,
Montana's second great gold strike in 1863 — sat 33.9 km out and so fell into the far band.</p>
"""),

"Teton fault": dict(
ground="""
<p>The eastern base of the Teton Range, where one of the most photographed mountain fronts on
Earth is also one of its cleanest normal-fault escarpments — the range rises and the valley floor
drops along the same structure, which is why the Tetons have no foothills.</p>

<p>The gate reads <strong>6 of 8 vertices</strong> — five gneiss, one quartzite — along
<strong>1,340 km of trace across 566 mapped segments</strong>, by a wide margin the largest
sampling in the study. Gneiss is the fabric case the mechanism wants, and the basement here is
Archean, some of the oldest rock exposed in the country.</p>

<p>Latest-Quaternary rupture, 59 km of mapped length, four extensional systems within 15 km
including the Snake River caldera faults, and 24,369 catalogued events within 90 km since 1900 —
this plate overlaps the Yellowstone system. It is also the only site of the ten whose GPS strain
leg returned a <em>fail</em> rather than a pass or an unmeasured, at 19.6, on a leg that was
allowed to promote and never to demote.</p>
""",
record="""
<p><strong>Lights:</strong> <code>T2</code> sighted and blind. Glowing orbs reported near Grand
Teton, and Teton Pass described in the returns as a hotspot for strange lights — recurring, but
web-native attestation with no archival or press spine under it.</p>

<p><strong>Indigenous place-narrative:</strong> <code>NT2</code> sighted and blind.
<em>Teewinot</em> is the Shoshone name; the range carries creation narratives and sacred-peak
status; and near the summit of the Grand Teton there is <strong>the Enclosure</strong>, a
deliberately built ring of stone slabs found there by the Hayden Survey in 1872 and generally
understood as a vision-quest structure — which means somebody climbed to within a few hundred feet
of the summit of a 4,199-metre peak, alone, before any recorded ascent, in order to sit in it. The
tier is capped at 2 because the first-pass sourcing was mostly web-secondary rather than
ethnographic-primary.</p>

<p><strong>Settler history:</strong> <code>HT2</code> sighted and blind. Placer claims of 160 acres
filed around 1900 from Jackson Lake down to Menor's Ferry, an 1889 mine in what is now the Teton
Wilderness, and the Deadman's Bar murders of 1886 about 29 km out. The National Park Service
material reached the frozen queries through a secondary outlet, and was graded accordingly.</p>

<p>Its decoy beat it on that leg. Unnamed faults near Ovando, Montana, returned Seeley Lake:
logging from 1892, first road in 1895, the first Forest Reserve ranger in 1899, Big Blackfoot
Milling in 1906, a fifty-million board-foot Forest Service sale to Anaconda — Montana History
Portal sourcing, <code>HT3</code>. The most famous mountain front in the study was outscored on
settler history by an unnamed fault near a logging town.</p>
"""),

# ------------------------------------------------------------------ round 2.
# No `record` key on purpose: both entered the deliverable after the three lore
# experiments were designed, frozen and run, so neither was ever scored. A sighted
# post-hoc lookup now, knowing they are on the list, is the contamination the
# pre-registration exists to prevent. The build renders the blank and says why.

"Centennial fault": dict(
ground="""
<p>The north wall of the Centennial Valley in Montana, immediately west of Yellowstone — a
seventy-kilometre east–west escarpment that is one of the few major <em>east–west</em> normal
faults in a province where nearly everything else runs north–south. It sits at the west end of
the Yellowstone hotspot parabola, where the crust that the hotspot has already passed under is
still relaxing and pulling apart.</p>

<p>The gate reads <strong>4 of 8 vertices</strong> qualifying — two gneiss, one quartzite, one
schist — along <strong>254.7 km of trace across 25 mapped segments</strong>, for a quartz
fraction of 0.5. Every qualifying vertex is a <em>fabric</em> rock, so this site's
<code>fabric_frac</code> equals its quartz fraction: the aligned-axis case the mechanism asks for,
with none of it coming from equigranular pluton. A fifth vertex returned rhyolite, which is a
measured rock at a measured point and does not count toward the gate; it is volcanic, and volcanic
glass has no fabric to align.</p>

<p>Latest-Quaternary rupture, a slip rate class of 0.2 to 1.0 mm/yr, five distinct extensional
systems within 15 km, and <strong>62 km of total mapped length</strong> — behind only the Madison
fault, and level with the Mosquito. The bedrock at the sampled node is quartzite of the Frontier
Formation.
The gravity field across the plate spans 29 mGal over 653 stations, a clean single basin edge:
the valley floor is a downdropped block and the fault is its north bounding structure.</p>

<p>This area is a head-set member. It appears in the top ten in every perturbation of the
composite, and it is the highest-scoring area in the ten that has never appeared in any published
version of this list — it enters here because the deliverable moved from the 100 km separation
scale to 50 km, and at 50 km the Centennial fault is its own area rather than a suburb of Hebgen
Lake 54.8 km to the east.</p>
"""),

"Antelope Valley fault zone": dict(
ground="""
<p>Antelope Valley at Topaz Lake, straddling the California–Nevada line at the northern end of
the Walker Lane — the belt where the Sierra Nevada's eastern front hands its motion over to the
Basin and Range, and where extension and strike-slip are braided together across a wide zone of
distributed faulting.</p>

<p>The gate reading here is the lowest in the ten, level with the Sand Springs Range:
<strong>2 of 8 vertices</strong> qualifying, both granite, along <strong>529 km of trace across
94 mapped segments</strong>, a quartz fraction of 0.25 sitting exactly on the gate's cut. Two
further vertices returned rhyolite — measured, named, and not qualifying. The qualifying rock
here is plutonic rather than fabric, which by this project's own reasoning is the weaker of the
two cases.</p>

<p>What carries this area onto the list is geometry and motion. <strong>Seven distinct
extensional systems within 15 km</strong> — behind only the Carson Range, and level with the
Sierra front — across 51 km of mapped length, with latest-Quaternary rupture and a slip rate
class of 0.2 to 1.0 mm/yr. Intersections are where fracture networks connect, and this is some of
the most thoroughly intersected ground in the study. The plate's gravity field spans 47 mGal over
690 stations. The regional seismicity is dense enough that the magnitude floor had to be raised
to 2.0 to keep the plotted catalogue inside the service's return cap; 9,762 events are drawn at
that floor, and both the requested and plotted floors are printed on the panel.</p>

<p>Antelope Valley is also among the most accessible ground in the ten. The nearest census place
is 2.5 km away and US-395 runs the length of the valley.</p>
"""),
}

# ==========================================================================
#  PART FIVE — closing
# ==========================================================================

WHAT_SURVIVES = """
<p>The list is a recommendation about where to point instruments, so here is what we would
actually do with it.</p>

<p><strong>Go to Hebgen Lake first.</strong> It is the only resolved position in the study, it
outscores the second area by four times the instrument's own step, and it is the one site in the
ten whose fault ruptured in front of witnesses — in 1959, magnitude 7.5, with the scarps still
in the ground. Whatever the mechanism does, this is where it should be loudest.</p>

<p><strong>What to carry.</strong> The conjecture makes physical predictions that a field party
can test in a week, and they are cheap:</p>

<ul>
<li><strong>A magnetometer on a continuous log.</strong> Stress-driven charge separation in a
quartz-bearing source volume should show as transient field excursions correlated with
microseismicity, not as a steady anomaly. The correlation is the signal; the level is not.</li>
<li><strong>Radon and soil gas along the trace.</strong> This is the direct test of the dilatant
half of the conjecture — an extensional fault should be venting, and a thrust should not. Run
the same instrument across a nearby compressional structure as your control.</li>
<li><strong>Cameras on timers, at the scarp and off it.</strong> Matched pairs, same night, same
weather. The whole point of a site list is that it lets you build a comparison instead of a
collection.</li>
<li><strong>Local seismic, at low magnitude.</strong> The catalogues used here are national and
their completeness floors are coarse. The events the mechanism would care about are below
them.</li>
</ul>

<p><strong>What would sharpen the screen itself.</strong> Two things, in order:</p>

<ul>
<li><strong>Aeromagnetic depth-to-basement.</strong> This is the correct version of the rock
criterion wherever the crystalline source is <em>buried</em> rather than exposed. Surface geology
cannot see it, and it would re-rank every basin-fill site in the study — including the one this
project started from.</li>
<li><strong>More labelled ground.</strong> Twenty to thirty sites with independently known
answers would let the composite be trained rather than argued about. Right now it has two, and
they are the two it was built around.</li>
</ul>

<p>And two claims of our own that this work killed, recorded so nobody rebuilds on them:
<em>"the Sandia / Hubbell Spring junction ranks first in the continental US"</em> — it ranks 36th
of 242 — and an early geodetic result that had profiled the wrong velocity component. Both were
ours. Both are withdrawn.</p>
"""

CLOSING = """
<p>The map of anomalous reports is not a map of anomalous places. It is mostly a map of roads,
towns and people with cameras, and everyone working in this field knows it. The only way out of
that is to predict ground from something other than the reports — and then go and look.</p>

<p>That is what the ten areas are. They were chosen by rock, rupture age, slip rate, fault
geometry and structural scale, over a complete national population, with the folklore held out of
the arithmetic and the controls declared in writing before the run. The six most famous anomalous
locales in the western United States are not on this list, and that is the strongest thing about
it: the screen is not rediscovering where people already look. It is pointing somewhere else.</p>

<p>Everything here is re-runnable. The population, the gate, the scoring legs, the plates and
their source URLs are all in the repository. If you think the weighting is wrong, change it and
re-run it — the ranked list of all 242 survivors is there, and your ground may well be on
it.</p>

<p>And if you get to one of these ten before we do, tell us what you found. Including nothing.
<strong>Especially nothing.</strong></p>
"""

PROVENANCE = """
<p><strong>Data.</strong> USGS Quaternary Faults and Folds (complete national layer-21 pull) ·
USGS State Geologic Map Compilation · Macrostrat geologic map lithology · USGS Bouguer gravity ·
USGS 3DEP shaded relief · ANSS / ComCat instrumental seismicity · MIDAS GPS velocity field ·
US Census place gazetteer. Every layer in every plate records the URL it was requested from.</p>

<p><strong>Freezes.</strong> Each lore experiment's design, tier ladder and exact query strings
were committed to version control before any lookup ran; the blind re-score design, packets and
probe gate were committed before any scorer was dispatched. Commit hashes are in the repository
record.</p>

<p><strong>Checking.</strong> Every measurement quoted in this article is asserted at build time
against the frozen artefact it came from — site measurements against the dossier and the stage-5
join, tiers against the lore result files, headline figures against the summaries, and the
membership and order of the ten against <code>candidate_list.json</code>. A typo fails the build
rather than shipping. The two areas added in round two were measured through the same along-trace
probe as the other eight, with both declared controls run first and required to reproduce.</p>

<p><strong>Standing.</strong> Screened, ranked, figured and written by Clawd, at Clayton's
direction. The physics inputs are institutional and anyone may re-pull them; the weighting is
ours. This has not yet been read by anyone outside this house.</p>

<p>Corrections, refutations and better instruments are all welcome, and the third is the most
welcome.</p>
"""
