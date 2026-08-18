# PRE-REGISTRATION — place-threshold screen, round 2

*Written **2026-08-18 (Day 199)**, BEFORE any round-2 lookup, any label, any re-weighting and
any basement-depth join is read. Committed first on purpose: everything downstream of this file
is only worth what this file's timestamp is worth. If a decision below is changed later, the
change is recorded as an amendment with its own date and reason — never by editing the original
line.*

**Why round 2 exists.** Round 1 shipped a working gate, a broken ranker, and three
sub-threshold lore legs. Its own closing paragraph names the three things that would move it:
*build the twenty-labelled-site set, blind a collection pass, run the aeromagnetic version.*
Clayton asked, on Day 199, that we do those ourselves rather than hand them to a reader. This
is the design for that, plus the two readout defects round 1 identified in itself.

---

## 0 · The distinction this whole round turns on

Round 1 printed ten sites and said, correctly, *"they are ten members of a qualifying class,
not the top ten places in America."* The request is to make them an actual ranking. There are
**two different products** hiding under that word and they need separating before anything is
built, because one is achievable and one may not be:

**Product A — ranked by criterion strength.** *"These are the ten sites where the
dilatant-rupture-through-quartz-fabric criterion is most strongly expressed."* This needs no
outcome labels. It needs only that the score be internally sound: no degenerate legs, no leg at
ceiling across the region where the ordering is being read, and a stated noise floor. It makes
**no claim that the ordering predicts anything**. It is a description of the physics, and it is
achievable in this round.

**Product B — ranked by predicted anomalous record.** *"These are the ten sites most likely to
carry an anomalous record."* This requires an outcome label, a validated relationship between
score and label, and enough labelled sites to measure it. **It may come back null.** If it
does, Product A ships and Product B is reported as a failure to detect, exactly as round 1's
lore legs were.

Both are built here. They are printed under different headings and never merged. **Any sentence
that ranks sites by criterion strength and is then read as a likelihood claim is the specific
error this round exists to not repeat.**

---

## 1 · Defects carried in from round 1, and what each one gets

| # | Round-1 defect | Round-2 remedy | Where |
|---|---|---|---|
| D1 | Nearest-town confound live and unremoved; winners median 7.5 km from a census place, decoys 19.3 km | Distance-to-nearest-place becomes a **design-time stratification axis**. Sites are drawn within distance bands so the confound is balanced by construction, not regressed out afterwards | §3 |
| D2 | The three lore legs are not independent (rho 0.32–0.48, survives disjoint panels) | Legs are **pooled into one outcome** with a pre-declared combination rule, and reported as one fact with one degree of freedom, not three | §5 |
| D3 | Landform-name salience deflates decoys; **5 of 20 first passes returned the wrong state** (Red Rock→Red Lodge, Boulder→Colorado, Sweetwater→Wyoming, Thompson Valley→Virginia, Round Valley→Mendocino) | **Coordinate-anchored, state-constrained queries**, with a mandatory locality-verification step that must resolve to within 25 km of the node before any evidence is scored. A query that cannot be anchored returns UNRESOLVED, which is a third value and is never scored as zero | §4 |
| D4 | Sighted **collection** (winners' evidence ran 1.51× longer than decoys') | **Fixed query budget, identical query templates, blinded labels, capped evidence length.** The collector sees a coordinate and a name, never a rank, score, or winner/decoy status | §4 |
| D5 | Separation-only bar; H3 cleared "≥1.0" at exactly 1.0 with p=0.18 and a live confound | **Conjunctive bar**: separation AND sign test AND distance-matched subset. All three or NOT SUPPORTED | §5 |
| D6 | Ranker fails its two declared controls by 0.19 in the wrong direction | Legs audited individually for degeneracy; the score is **re-specified from mechanism, not fitted to the controls**; then tested | §2, §6 |
| D7 | Junction density reads 1.00 at both controls | De-saturated: the leg is re-derived as a continuous quantity over the same national pull, and its ceiling behaviour is reported across the range the ordering is actually read in | §2 |
| D8 | The pipeline is **not re-runnable from the repository** — `stage5_join.py` reads four intermediates (`qfaults_normal_national.geojson`, `trace_lithology_full.json`, `transport_nodes_perfault.json`, `screen_strain_pass.json`) that no longer exist on disk | Re-pull and commit the manifest + checksums, or the reproducibility claim in the report's provenance section is false. **Found Day 199; it was not known when round 1 shipped** | §7 |

---

## 2 · Leg audit — declared before re-weighting

Measured Day 199 over the 225 fully-scored gate survivors, from
`data/stage5_join_summary.json`:

| leg | mean | sd | distinct values | verdict |
|---|---|---|---|---|
| age | 0.460 | 0.273 | 6 | usable, coarse |
| slip | 0.062 | 0.164 | 4 | **near-dead — 194 of 225 read exactly 0.0 (86%)** |
| junction | 0.573 | 0.369 | 5 | **saturated at the top — 73 of 225 at 1.00 (32%), and 7 of the printed ten** |
| length | 0.526 | 0.170 | 75 | usable, continuous |
| quartz (gate) | 0.545 | 0.281 | 7 | gate only, ±0.125 sampling noise |

**Two findings, both pre-declared here so neither can be discovered later in a flattering
direction:**

**(a) The junction leg's failure is worse than "saturated" and better-shaped than round 1 said.**
Across the full 225 it has real variance. It is at ceiling *specifically in the top decile* —
where the ordering is read. A leg that discriminates in the tail and saturates at the head is
not an inert leg; it is a leg that **selects the head and then cannot order it**. Round 1's
report says "saturated" flatly; that sentence is imprecise and is corrected in round 2.

**(b) The slip leg is 0.0 for 86% of survivors.** This was never stated in round 1. It means
the four-leg mean is, for the overwhelming majority of sites, a **three-leg mean with a
constant zero dragging every score down by a fixed amount** — which does not change the
ordering, but does mean one of the four declared legs contributed nothing to it for 194 of 225
sites. Reported as a coverage/encoding fact, not as a new criterion.

**Pre-declared consequence:** the round-2 score will be re-specified over legs that are
non-degenerate *in the range the ranking is read in*, and any leg failing that test is
reported as an annotation, exactly as L5 strain already is. **The re-specification is written
from mechanism before the control test is run, and is run once.** Iterating the weights until
the controls separate correctly is fitting four parameters to two points and is forbidden here
by name.

---

## 3 · The labelled set — N = 30, stratified, drawn before any lookup

**Population.** The 225 fully-measured gate survivors, plus a declared out-of-gate stratum.

**Strata (this is the round-1 defect `feedback_sample_drawn_from_one_stratum` made structural):**

| stratum | n | drawn from |
|---|---|---|
| S1 top | 8 | ranks 1–25 of the 225 |
| S2 upper-middle | 7 | ranks 26–90 |
| S3 lower-middle | 7 | ranks 91–160 |
| S4 bottom | 5 | ranks 161–225 |
| S5 **gate failures** | 3 | quartz_frac < 0.25, matched on age and length to S1 members |

S5 exists because **a ranker tested only inside the class its own gate selected has never been
asked whether the gate was the whole story.** Round 1 never had this stratum.

**Distance matching (D1).** Within each stratum, sites are drawn so the distribution of
distance-to-nearest-census-place is as close to uniform across strata as the population allows;
the achieved distributions are printed per stratum **before** any label is collected, and the
imbalance that remains is stated as a number rather than as a caveat. If a stratum cannot be
filled without a distance imbalance greater than a factor of 1.5 in median, that stratum is
reported as unbalanced and its label is analysed separately.

**Minimum separation** 50 km, as round 1. **Seed committed** in `data/round2_draw.json` at draw
time, with the draw script's hash.

---

## 4 · Blind collection — the queries, frozen

**What the collector sees per site:** an opaque ID, a latitude, a longitude, a fault name, and
a US state. **Never:** rank, score, stratum, component values, or whether the site is drawn
from the gate-pass or gate-fail population. Order shuffled at the committed seed.

**Query budget: exactly 6 queries per site per leg, no more, no fewer.** Round 1's 1.51×
evidence-length asymmetry is a *collection effort* asymmetry; a fixed budget is the only
mechanism that removes it, and it is enforced by the harness counting calls, not by intention.

**Query templates are frozen in `data/round2_queries.json` before the first call** and are
identical across sites modulo the substituted place, state and coordinate.

**Locality verification (D3) — the mandatory first step.** Before any evidence query runs, the
site's name must be resolved against the coordinate. A returned locality more than 25 km from
the node is a **conflation**, is logged by name, and that site's leg returns `UNRESOLVED`.
`UNRESOLVED` is a third value. It is never scored 0. Round 1's two zero-scores on the settler
leg, and the negative control's zero, were conflations scored as absences; that is the specific
mistake this clause exists to make impossible.

**Evidence cap:** the scored excerpt per site per leg is capped at a fixed character count,
declared in the query file. Length asymmetry cannot then encode effort.

---

## 5 · The readout bar — conjunctive, declared now (D2, D5)

The three round-1 legs are **pooled into a single outcome score** per site by a pre-declared
rule (equal-weight mean of the three tier ladders, `UNRESOLVED` excluded from the denominator
and its count reported). One outcome. One test. Round 1's three legs correlated 0.32–0.48 and
were therefore never three facts; pooling states that honestly instead of discovering it
afterwards.

**Product B is SUPPORTED only if all three of the following hold:**

1. **Separation** — Spearman rho between round-2 score and pooled outcome ≥ **+0.35** across
   the 30 labelled sites;
2. **Sign test** — two-sided p ≤ **0.05** on the top-half vs bottom-half comparison;
3. **Distance-matched subset** — the sign of (1) is preserved, with rho ≥ **+0.20**, on the
   subset where distance-to-place is matched.

Any one failing → **NOT SUPPORTED**, and Product B is not printed as a ranking. A near-miss is
a near-miss; round 1 already demonstrated that a bar cleared "at exactly the bar" by a float is
not a result. **No bar in this file may be adjusted after any label is read.**

---

## 6 · Product A — the criterion ranking, and what it is allowed to say

Built from the re-specified score of §2 plus the new basement leg of §7. It ships with:

- every leg's value range across the printed ten, so a reader can see at a glance which leg is
  doing the ordering;
- a **stated ordering noise floor** — the rank change induced by perturbing each leg within its
  own measurement noise, run as a bootstrap, so "rank 3 vs rank 6" carries an honest error bar
  or is reported as indistinguishable;
- the two declared controls, in the right direction or **printed failing**, with no
  re-weighting after the fact.

**What Product A may say:** these ten express the criterion most strongly. **What it may not
say, in any sentence, caption, or figure title:** that they are the ten most likely to carry an
anomalous record. That claim belongs to Product B and is licensed only by §5.

---

## 7 · The new physics leg — depth to basement (the "aeromagnetic version", done better)

Round 1 asked for aeromagnetic depth-to-basement as the correct rock criterion for a **buried**
crystalline source. **USGS has already published the inversion**, so this round uses the
published product rather than deriving one:

- **Shah, A.K. & Boyd, O.S., 2018**, *Depth to basement and thickness of unconsolidated
  sediments for the western United States — initial estimates for layers of the USGS National
  Crustal Model*, USGS Open-File Report 2018-1115, [doi:10.3133/ofr20181115](https://doi.org/10.3133/ofr20181115).
- Grid: `Dep2MzBasement_LLz.csv`, 1 km node spacing, WGS84, ScienceBase item
  `5b0d85eee4b0c39c934b0429`. Extent −124.72 to −102.73 E, 28.99 to 49.0 N.

**Coverage, measured Day 199 before any join was read: 225 of 225 survivors fall inside the
grid extent. Zero coverage hole.** Survivor longitude range −124.322 to −104.911, latitude
31.605 to 48.547 — comfortably inside on both axes. This number is recorded here, before the
join, precisely so that a later coverage figure cannot be reported as if it had been checked in
advance.

**How the leg enters, declared before it is computed.** Depth-to-basement is *not* simply
"shallower is better". The mechanism is a crystalline source coupling to the surface; the
prediction is that a **quartz-fabric source at shallow-to-moderate basement depth beneath a
dilatant rupture** is the coupled case, and that deep basin fill decouples it. So the leg is
declared as a **monotone-decreasing function of basement depth with a stated saturation
depth**, and both the functional form and the saturation depth are written into
`code/basement_leg.py` before the values are joined to site identities.

**The pre-declared consequence, stated now because it is the interesting one:** this leg
**re-ranks every basin-fill site downward**, including Sandia — the declared positive control,
which sits on the eastern flank of the Albuquerque basin — and including Hubbell Spring, the
declared negative. **If adding a mechanically-correct leg moves the positive control down, that
is reported, not absorbed.** It is exactly the case in which a "fix" would be tempting.

---

## 8 · Reproducibility (D8)

Round 1's provenance section says anyone may re-pull the physics inputs. **As of Day 199 that
is true of the sources and false of the pipeline**: four intermediates are referenced by path
and absent from the repository. Round 2 does not ship until either the intermediates are
regenerated and their manifest + checksums committed, or the provenance paragraph is amended to
say plainly which stages cannot currently be re-run. **The claim gets fixed or the claim gets
retracted; it does not get left standing.**

---

## 9 · What can still kill this round

Written down now so none of it can be presented later as a discovery:

- **N = 30 is small.** With 30 labels the rho confidence interval is wide (roughly ±0.35 at
  rho≈0.35). A pass at the bar is weak evidence; a fail is not proof of absence. Both readings
  are stated in advance.
- **The outcome label is still folklore**, still largely grade C, and blinding the collector
  does not make the underlying record less patchy. Blind collection removes *our* thumb; it
  does not remove the world's.
- **The gate-fail stratum is only n=3.** It tests whether the gate is the whole story; it does
  not test it well.
- **Product A can be honest and still be uninteresting.** A criterion ranking with no
  demonstrated predictive content is a well-documented sort order. That is a real possible
  outcome and it is not a failure of method.

---

*Frozen Day 199, 2026-08-18, before any round-2 lookup. Amendments append below with date and
reason; nothing above this line is edited.*

## Amendments

*(none yet)*
