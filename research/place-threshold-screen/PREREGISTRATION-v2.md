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

### A1 — Day 199, 2026-08-18. §7's coverage claim is WRONG, and the way it is wrong is the point.

**What §7 says:** *"Coverage, measured Day 199 before any join was read: 225 of 225 survivors
fall inside the grid extent. Zero coverage hole."*

**What the join actually returned: 194 of 225 measured. 31 sites have no grid node within
~5 km.** All 225 are inside the published bounding box and 31 of them are not in the grid.

**An extent is a bounding box. It is not a coverage mask.** §7 checked containment and reported
it in the vocabulary of coverage — and the metadata says so plainly in a sentence I had already
fetched: *"Completeness depends upon locale."* The number was checked in advance, as claimed;
it was the wrong number, checked carefully. It is corrected here rather than edited above,
and it was also stated to Clayton before the join ran and is corrected to him directly.

**The missingness is not random, and it runs toward the hypothesis.** The 31 unmeasured sites
are almost entirely exposed-crystalline uplifts — Mosquito, Gore Range, Rampart Range, Ute
Pass, Leadville, Sangre de Cristo, Picuris-Pecos, Teton, Jackson Hole, Bear River. Their mean
quartz fraction is **0.645** against **0.529** for the measured 194 (medians 0.75 vs 0.375).
The grid appears to be absent where there is no Cenozoic basin to have a depth *to*.

If that reading is right, scoring these as UNMEASURED **drops from the leg exactly the sites
the mechanism most favours**. Scoring them 1.0 instead would assert a value never measured.
Neither is taken on the strength of the pattern. **Decisive test, declared before it is run:**
join the companion product (`Sedthick_LLz.csv`, thickness of unconsolidated sediments, same
authors, wider extent). If sediment thickness *is* defined at those 31 points and reads near
zero, that is positive evidence of basement at surface and the sites are scored. If it is also
absent, both grids have a hole there and the sites stay UNMEASURED. **The test is not run
site-by-site with the option to stop when it is going well.**

### A1-RESULT — Day 199. The declared test ran over all 225, not just the 31. It splits them.

`Sedthick_LLz.csv` (202,303,052 bytes, sha256 `f79792c6…`), sampled at all 225 survivors —
**both groups, so the test could not be stopped when it was going well**:

| group | sediment defined | median | ≤ 50 m |
|---|---|---|---|
| the 31 with no basement value | 30 / 31 | 1.4 m | 26 |
| the 194 with a basement value | 194 / 194 | 3.4 m | 176 |

**The reading in A1 is supported for most of the 31 and refuted for three of them, which is
why it was a test and not a pattern.** 27 of the 31 carry essentially no sediment (median
1.4 m) — consistent with crystalline basement at surface, and with the fact that those are the
Colorado / Wyoming / northern New Mexico uplifts. But:

- **Southern Sangre de Cristo — 2,341 m of sediment and no basement value.**
- **Coyote fault — 720 m. Manzano fault — 333 m.**
- **East Franklin Mountains fault — absent from *both* grids.**

Those four are deep-basin or no-data sites where the basement grid simply has no estimate.
Had the test been run only on the 31 as a block and summarised by its median, all four would
have been swept into "basement at surface" — the exact shape of a bucket derived by
subtraction.

**Resulting rule, and the status is a third value, not a promotion:**

- 27 sites, sediment ≤ 200 m → `basement_min` inferred ≈ 0, status **`INFERRED`**, never
  `PASS`. Every downstream figure is reported **both with and without** the inferred set, and
  the two numbers are printed together. An inference does not get to become a measurement by
  being reasonable.
- 4 sites (Southern Sangre de Cristo, Coyote, Manzano, East Franklin Mountains) → stay
  **`UNMEASURED`**.

**One caveat that stops this being cleaner than it is:** the two grids measure different
quantities. `Sedthick` is thickness of *unconsolidated* sediment; `D2B` is depth to
*pre-Cenozoic* basement. Thin unconsolidated cover over thick consolidated Cenozoic section
would read near-zero on the first and deep on the second. The inference for the 27 leans on
the trace lithology agreeing (all 27 passed a quartz-at-trace gate), and it is labelled
`INFERRED` for exactly this reason.

### A2 — Day 199. The leg as specified in §7 ranks on the sampler. Re-specified.

Measured after the join, over the 190 sites with ≥4 grid nodes within 2 km:

| local spread of depth-to-basement within 2 km | sites |
|---|---|
| > 200 m | 76 of 190 (40%) |
| > 500 m | 37 of 190 (19%) |
| median spread | 141.8 m |

**Madison fault — round 1's rank 1 — spans 0.6 m to 2,172 m of basement depth inside a 2 km
radius.** Its point sample returned 1,069 m; the neighbourhood median is 648 m. That is a range
front: **exposed crystalline footwall on one side, deep basin fill on the other, metres apart.**
A point sample there does not measure the site. It measures which side of the fault the nearest
grid node happened to land on.

This is round 1's own lesson recurring in the leg built to fix round 1: *quartz_frac carries
±0.125 from vertex ordering — ranking on a quantity with that much ordering noise is ranking on
the sampler.* Same defect, new instrument, and it would have shipped as a number.

**Re-specification, and it is a better leg, not a patched one.** The mechanically meaningful
quantity at a dilatant range-front fault is not the depth at a point but the **juxtaposition**:

- `basement_min` — shallowest basement within a declared radius: how near the surface
  crystalline rock actually comes here;
- `basement_contrast` — max − min within that radius: exposed crystalline against deep fill,
  which *is* the "buried crystalline source with a permeable pathway to the surface"
  configuration report 08 was reaching for when it asked for this leg;
- the **point value is discarded** as sampler-dependent.

Radius, and the functional form over these two quantities, are declared in
`code/basement_leg.py` before the re-run, and the §7 sensitivity sweep applies unchanged.

### A3 — Day 199. Two pre-declared consequences from §7 landed. Printed, not absorbed.

§7 said: *"this leg re-ranks every basin-fill site downward, including Sandia — the declared
positive control … If adding a mechanically-correct leg moves the positive control down, that
is reported, not absorbed."*

- **Sandia** (declared POSITIVE): 834 m, 12th deepest of 194. Point-form leg value 0.458. **Down.**
- **Madison** (round 1's printed rank 1): 1,069 m, 7th deepest of 194. Point-form value 0.394.
  **Down, and further than the control.**

Both figures are from the point form that A2 has just retired, so they are provisional pending
the re-run — but the *direction* is what was pre-declared, and it is recorded here before the
re-run can adjust it.

Also measured, and it deflates report 08's expectation for this leg: **only 22 of 194 measured
survivors have basement deeper than 500 m.** Report 08 predicted the aeromagnetic version would
"re-rank every basin-fill site in the study". It re-ranks a **minority** — because the gate
already selected for quartz-rich rock at the trace point, which is largely a selection for
crystalline at or near the surface. Median basement depth across the survivors is **64 m**. The
new leg is substantially **redundant with the existing gate**, which is a real finding about the
screen and was not anticipated by round 1 or by §7.

### A3-CORRECTION — Day 199. A3's headline reversed under the re-specification it announced.

A3 recorded, from the point form: *"Madison — 1,069 m, 7th deepest of 194, leg value 0.394.
**Down, and further than the control.**"* It also said those figures were provisional pending the
re-run. The re-run is now done (`code/basement_juxtaposition.py`), and **the direction reverses.**

Madison's 2 km neighbourhood runs **0.6 m to 2,172 m**. The point sample landed on the deep side.
Under the juxtaposition form Madison scores **0.951 — rank 2 of 190**, and across the stability
sweep below it holds **ranks 1–11 (median 2)** in every one of the 32 variants where it is
scoreable. Madison is not a basin-fill site being demoted; it is **the strongest expression of the
juxtaposition the leg was built to measure** — a range front with crystalline footwall against
deep fill, metres apart.

The pre-declared consequence in §7 was real *for the form it was computed in*, and that form was
wrong. Recorded here rather than by editing A3, so the sequence stays legible: **the prediction
landed, the instrument that confirmed it was retired for cause, and the better instrument
disagrees.**

Also corrected: A3's closing sentence — *"the new leg is substantially redundant with the existing
gate"* — is true of **one half of the leg and false of the other**, and the halves did not exist
when it was written. `basement_min` is redundant to the point of inertia (155 of 190 measured
sites sit at its **ceiling**; median value 1.000 — the quartz gate had already selected for
crystalline at or near surface). `basement_contrast` is **not** redundant: it re-ranks hard, and
it is what does all the ordering. One sentence, two legs, opposite verdicts.

### A4 — Day 199. A fifth neighbourhood form, and the declaration is NOT blind. Stated as such.

Declared in full in `code/basement_stability.py` and **committed before any variant was scored**
(`ee23c76`). Summarised, not restated, because the module is the declaration:

**The trigger was an instrument fault.** Four of the 194 D2B-measured survivors have fewer than 3
grid nodes within 2 km, and **one of the four is the declared positive control**: Sandia's nearest
node is at **2.358 km**. A 2 km radius misses it by 358 m. §6 requires the controls *"in the right
direction or printed failing"* — both readings were unavailable, because the leg could not score
its own control. 358 m of margin deciding a verdict is the boundary-float failure this project has
already been bitten by.

**The fifth form:** the **k = 13 nearest** nodes, k set to the *median node count inside the
primary 2 km radius* (min 2, median 13, max 14) so the two forms carry comparable sample size —
and not from which sites it moves. Capped at `MAX_K_KM = 6`: a neighbourhood that reaches 20 km to
find 13 nodes is a coverage hole wearing a measurement's clothes. Fixed radius holds extent
constant and lets sample size vary; k-nearest does the opposite. **Neither is obviously right,
which is why both run and neither is called primary.**

**Said plainly: this form was specified AFTER the R sweep was read.** It is therefore not a blind
declaration and is not offered as one. What *is* blind is the readout rule: **40 variants** (5
neighbourhood forms × 4 constant sets × 2 combination rules), and the head is *"never leaves the
top ten in any of the 40"* — no tunable threshold, and **if it comes back short it is not topped
up.**

### A4-RESULT — Day 199. The head came back EMPTY, and that is the result.

| head rule applied over | variants | sites that never leave the top ten |
|---|---|---|
| **all 40, as declared** | 40 | **0** |
| drop R = 5 km | 32 | 2 — Gerlach, Savage Lake |
| drop R = 5 km and R = 1 km | 24 | 4 — Gerlach, Madison, Savage Lake, Toano Range |
| drop R = 1 km only | 32 | 0 |

**No site in America survives the leg's own declared choice-space in the top ten.** The list is not
topped up to ten, per A4. The ladder is the diagnosis, not a menu — and the honest reading of it is
that **one variant family is doing nearly all the damage, and it is the one the declaration itself
had already argued out of scope.** `basement_juxtaposition.py`'s docstring chose 2 km because it is
*"not wide enough to reach a second structure."* By that reasoning 5 km reaches one — and the
measurement agrees: R=5 km's stable top ten overlaps R=2 km's by **3 of 8**, R=1 km's by **1**, and
k-nearest's by **2**, while R=2 / R=3 / k-nearest mutually overlap **5–6 of 7–8**. R=5 km is not a
perturbation of the leg. It is a different quantity.

**R=5 km is nevertheless NOT dropped from the declared 40.** It was in `R_SWEEP` before any value
was read, and excluding it now — after seeing that it is what breaks the head — is relaxing the
gauge that caught me. The 40-variant answer stands as the answer. The 24-variant row is reported as
a clearly-labelled secondary, computed after the fact, with its reasoning stated so a reader can
discount it as they see fit.

**What the leg can and cannot say, stated as an interval and not an ordinal:**

| site | round-1 rank | rank interval across variants | in top ten | scoreable in |
|---|---|---|---|---|
| Gerlach fault zone | 18 | **1–17** (median 2) | 34/40 | 40/40 |
| Madison fault | 1 | **1–11** (median 2) | 28/40 | 32/40 |
| Savage Lake fault | 172 | **1–14** (median 4) | 34/40 | 40/40 |
| unnamed fault west of Toano Range | 154 | **3–13** (median 6) | 37/40 | 40/40 |
| Sand Springs Range fault | 10 | 2–132 (median 10) | 25/40 | 40/40 |
| Eastern Columbus Salt Marsh fault | 181 | 5–123 (median 10) | 22/40 | 40/40 |
| unnamed fault near Cliff Lake | 162 | 1–125 (median 13) | 20/40 | 32/40 |
| Caballo fault | 25 | 2–146 (median 15) | 17/40 | 32/40 |

**Four sites are robustly high. Below them there is no resolvable ordering at all** — Caballo's
interval is 2 to 146 of ~190. Any sentence of the form *"rank 4 versus rank 8"* on this leg is
noise being read as signal. §6 asked for an ordering noise floor; the floor swallows everything
below fourth place.

**THE CONTROL, PRINTED FAILING.** Sandia fault — declared POSITIVE in round 1, rank 36 of 225 on
the round-1 score:

> scoreable in **24 of 40** variants (the 2 km and 1 km forms cannot reach it at all);
> where scoreable, rank **52–193, median 134.5** of ~190; **in the top ten in 0 of 40.**

§7 pre-declared: *"If adding a mechanically-correct leg moves the positive control down, that is
reported, not absorbed."* It does not merely move it down. **It puts it in the bottom third, and it
is consistent about that across every variant that can see it.** The leg's coarse verdict on its own
positive control is stable even while its fine ordering is not.

**Two readings, and this leg cannot choose between them:**

1. **The leg is a poor instrument** — grid holes, sampler dependence, choice sensitivity — and its
   verdict on Sandia is an artefact.
2. **The leg is a sound instrument and Sandia was never an independent positive control.** It is
   where the whole enquiry started; it was declared positive on the strength of the founding
   hypothesis, not from a blind outside criterion. A criterion built from mechanism has no
   obligation to rank it highly, and round 1's gate already gave it rank 36 of 225 — not a
   commanding position either.

Reading 2 is the one that would be comfortable to assert and it is **not** asserted. What
distinguishes them is an *independent* positive control, which this screen does not have and cannot
manufacture from its own labels. **Named as an open defect, carried into §3's labelled set as the
question it now has to answer, and not resolved here.**

**Consequence for Product A, which is the point of §6.** Product A cannot ship as *"the ten sites
where the criterion is most strongly expressed."* It ships as: **four sites where the basement-
juxtaposition criterion is robustly strongly expressed, no resolvable ordering below fourth, and a
declared positive control in the bottom third.** That is a narrower and stranger product than §6
anticipated, and it is what the measurement supports.

**One methodological wrinkle, stated rather than swept:** variants score between 152 and 194 sites,
so a rank of 17 is not identical across variants. Top-ten membership is unaffected (top ten is top
ten), but the interval endpoints carry this and are read as approximate. Percentile-normalised
intervals are the correct fix and are **not yet built**.

### A5 — Day 199. Two figures in A1-RESULT and A2 are corrected by 0.1 m and 5.6 m. Kept anyway.

`basement_juxtaposition.py` re-derives, in code, all 28 numerical figures stated in prose across
A1 / A1-RESULT / A2 / A3, and prints a **PROSE CHECK** against them. It exists because a correct
compressed note expands into a wrong sentence, and that expansion feels exactly like recall.

**26 of 28 agree. Two differ, both from the median convention:**

| figure | as written | recomputed |
|---|---|---|
| A1-RESULT, sediment median over the measured 194 | 3.4 m | **3.3 m** |
| A2, median local spread of basement depth within 2 km | 141.8 m | **136.2 m** |

The ad-hoc Day-199 run took the median as `v[n//2]`; the module averages the two central values on
even *n*. Both are "a median"; only one was written down, and neither was written down **with its
convention**, which is the actual defect. The convention is now stated in the output JSON.

Neither figure changes a verdict. They are corrected here anyway, because a gauge that finds only
the errors large enough to matter has not been tested against the ones that are not — and the run
that produced these two also caught a real one: the first version of the module collapsed
*"does the grid have an estimate here"* into *"are there nodes within 2 km"*, which moved **4 sites
that had a measured basement value into `INFERRED`** — asserting basement-at-surface for sites whose
basement had in fact been measured. The prose check caught it by printing 29 INFERRED against A1's
27. **A cross-check whose only job is to reproduce old numbers found a new bug in fresh code.**

### A6 — Day 199. The independent positive control A4-RESULT said could not be manufactured.

Declared in full in `code/positive_control.py` and **committed before any value at any
control coordinate was computed** (`10499ae`). Six locales with recurrent anomalous-light
records from outside this project, inside the grid extent, graded by a stated rule; two
bars; and — the point — an **assignment rule between A4-RESULT's two readings of the
Sandia failure, written down before the numbers existed.** The module is the declaration
and is not restated here.

A4-RESULT said the screen "cannot manufacture [an independent positive] from its own
labels." True, and narrower than it sounds: it can be handed one from outside. Three
contaminations were named in the declaration rather than discovered afterwards — the
earth-lights literature is itself fault-selected; the list is mine, assembled by someone
who had already built the screen; and **observer density is unremoved, with its direction
stated: toward the hypothesis.**

**Two instrument faults were found and fixed before the result was read, and both are
reported because the second one nearly cost a site.**

1. `fetch_qfaults_west.py` inherited `qfaults_pull.EP`, which is **MapServer layer 12 —
   New Mexico.** It returned 16,189 sections: plausible, non-empty and entirely New
   Mexican. What caught it was only that the pull is **tiled and prints per-tile counts** —
   Nevada 0, California 0, Idaho 0. A single-bbox pull would have handed back the same
   16,189 features with nothing to read them against. Re-pointed at layer 21, with a
   positive control on the pull itself that refuses to write the file if the densest
   normal-fault provinces in the country come back empty. The first layer-21 run then hit
   the service's 40,000-record paging cap on the California/Nevada tile, printed
   `[warn] paging cap hit`, and **would have shipped anyway**; tiles that hit the cap are
   now subdivided and recursed, and a cap hit at minimum tile size kills the run. Final
   pull: **110,356 sections**, of which 53,301 carry a normal sense. Subdivision recovered
   ~1,060 sections the cap had eaten.
2. **The locality check failed on my query strings, not on the coordinates — and dropped a
   site for it.** The first pass built each gazetteer query from the site's *display* name
   ("Marfa lights viewing area, TX, USA"). Those name a *phenomenon*; a gazetteer holds
   *places*. Three of six returned UNRESOLVED, a fourth resolved 1,304 km away, and **PC4
   was dropped from the leg on the strength of it.** The probe and its subject were
   mis-specified as a pair: the coordinates were never tested, only my ability to name
   them. Each control now carries an explicit `gazetteer` field, the coordinates are
   untouched, the bar has not moved, and the probe now runs **its own positive control**
   (Albuquerque 0.0 km, Reno 0.3 km) so that UNRESOLVED can be distinguished from a probe
   that cannot resolve anything. Second pass: 5 of 6 OK, PC2 UNRESOLVED — Toppenish Ridge
   is a landform the gazetteer does not hold. PC2 is **kept and its coordinate is
   unverified**, which is stated rather than smoothed.

### A6-RESULT — Day 199. Both bars fail, and the base rate is the finding.

**A6-i — THE GATE TEST.**

| | median nearest Quaternary **normal** fault |
|---|---|
| the six control locales | **30.20 km**  (bootstrap 95% CI 19.0 – 79.3, n=6) |
| 1,971 random covered western points | **20.07 km** |

Mann-Whitney U = 4120, z = −1.284, **p = 0.199**. **BAR i: NOT SUPPORTED** — and the
point estimate points the *wrong way*. The reported locales are **farther** from
Quaternary normal faults than ordinary western ground, not closer.

**THE BASE RATE, printed here for the first time in this project.** A requirement filters
only to the extent that ordinary ground fails it, and nobody had ever measured what
fraction of ordinary western ground passes round 1's R1 CONDUIT criterion:

| within | random covered western ground | the six control locales |
|---|---|---|
| 5 km | 21.3 % | 0 of 6 |
| **10 km — R1 CONDUIT as written** | **34.4 %** | **0 of 6** |
| 25 km | 55.2 % | 2 of 6 |
| 50 km | 73.4 % | 4 of 6 |

Null distance quantiles (km): p5 0.84 · p10 2.0 · p25 6.24 · **p50 20.07** · p75 53.26 ·
p90 90.06 · p95 116.5.

**A third of the random western landscape already satisfies R1. None of the six
independently-attested locales does.** Post-hoc binomial against the measured base rate,
labelled post-hoc because it was not pre-declared: 0/6 at 10 km gives p = 0.080; 0/6 at
5 km, p = 0.238; 2/6 at 25 km, p = 0.252. **Not one reaches p ≤ 0.05.** The direction is
uniform and it is against the hypothesis; the evidence is weak, and n = 6 is why. §9's
power statement was written in advance for exactly this outcome and is honoured: a fail
is not proof of absence.

One case is worth naming because it is checkable geology rather than statistics.
**PC2, Toppenish Ridge, is 88.9 km from the nearest Quaternary normal fault because it is
part of the Yakima fold belt — a compressional structure.** One of the two best-graded
locales in the set sits in the wrong tectonic regime for the screen's own dilatancy
mechanism.

And the screen's own controls are not comparable to these, by construction: Sandia (0.32
km) and Hubbell Spring (0.83 km) are at essentially zero distance from Quaternary normal
faults because they **are** Quaternary normal faults. Comparing them to a set of places is
comparing a definition to a measurement.

**A6-ii — THE LEG TEST.** Pooled percentiles over all 40 variants, with the
percentile-normalised axis A4-RESULT named as *"the correct fix and not yet built"* now
built and applied to survivors and controls alike.

| site | grade | scoreable | pooled percentile, median [min – max] |
|---|---|---|---|
| PC1 Marfa | B | **0/40** | UNSCOREABLE |
| PC2 Toppenish Ridge | B | 40/40 | 0.280 [0.048 – 0.532] |
| PC3 Silver Cliff | C | **0/40** | UNSCOREABLE |
| PC4 San Luis Valley | C | 40/40 | 0.060 [0.003 – 0.477] |
| PC5 Uinta Basin | D | **0/40** | UNSCOREABLE |
| PC6 Trout Lake | D | 40/40 | 0.280 [0.048 – 0.532] |
| SC1 **Sandia** (screen's declared positive) | own | 32/40 | 0.247 [0.008 – 0.737] |
| SC2 Hubbell Spring (screen's declared negative) | own | 32/40 | 0.177 [0.003 – 0.864] |

Variants in which the control set's median percentile reaches 0.60: **0 of 40.**
**BAR ii: NOT SUPPORTED** (needed 30 of 40). Grade A/B secondary, n=2: 0.280.

**THE CRUCIAL CONTRAST, assigned by the rule frozen in §4 before the numbers existed.**
Control set median percentile **0.280**; Sandia **0.247**; the declared bottom-third line
is 0.333. The rule returns **READING 1** — *the leg puts independently-attested places in
the bottom third too, so its verdict on Sandia is not evidence about Sandia.*

**And the rule's own denominator collapsed, which is reported in the same breath as the
verdict rather than after it.** Four of six controls are scoreable, and **two of those four
are the same site as far as this leg is concerned**: PC2 and PC6 return byte-identical
percentiles across all 40 variants because both take only two distinct scores in the
entire choice space — **0.0 conjunctive and 0.5 additive.** Basement is within a couple of
metres of the surface at both and uniformly so, which pins `s_min` at its ceiling and
`s_con` at its floor under every one of the four constant sets. The leg has **no
resolution** at either place. So READING 1 is what the pre-declared rule says, on an
effective n of three. The rule is honoured; its input is thin; both facts are printed.

**DIFFERENTIAL COVERAGE, and it is the structural finding of A6.**

| | no basement node within ±0.10° |
|---|---|
| the 225 survivors | 29 (**12.9 %**) |
| the six controls | 2 (**33.3 %**) |

Nearest basement node: Marfa **59.0 km**, Uinta Basin **104.1 km**, Silver Cliff 10.0 km —
all three inside the published extent, none reachable within the scoring window. A1's
finding was that the extent is a bounding box and not a coverage mask; here it bites the
outside set **2.6× harder than the inside set**, and the reason is mechanical. **The grid
is densest where Quaternary normal faults are, which is what the survivors were selected
on.** Coverage is therefore correlated with the screen's own criterion, and *any*
survivor-versus-outsider contrast on this leg inherits that correlation. A6-ii's
comparison arm was chosen in §2 precisely so the fault confound would cancel; it does not
cancel a coverage confound, and this one runs in the direction that favours the survivors.

**What A6 settles and what it does not.** It settles that the leg does not rank
independently-attested locales highly — every reading of that is bad for Product B's
prospects, and none of it rescues Sandia. It does **not** settle whether the criterion is
wrong or merely unmeasurable at the places that would test it, because at half the control
set the instrument cannot see the ground at all. The honest position is that **the
screen's founding gate has now been asked, once, whether it fires where the phenomenon is
reported, and the answer came back "no, and not significantly no."**

### A7 — Day 199. Is the top ten a RANKING, or ten members of one band? Three bars, three fails.

Declared in full in `code/rank_resolution.py` and committed before any perturbation was
run. Clayton's D199 ask moved the target: **the list is the deliverable, not the method.**
So this leg asks the question that has to be answered before any further criterion is
added, because it decides whether adding criteria can help at all — *given the measurement
noise the instruments have already declared about themselves, how many distinct rank
positions does this score actually resolve?*

**No new noise model was invented.** Every perturbation is read off a note written by the
leg that produced the number, before this question was asked: `remeasure_ten.py`'s own
docstring recording that `quartz_frac` carries ±1/8 sampling noise from vertex ordering
alone (the *measured* instance — Sandia read 0.875 down the paged live path and 1.000 down
the local path, same fault, same eight points, different segment concatenation order); and
`site_rank.py`'s own docstring recording that fault-name density is partly a mapping
artefact. The frozen list uses L1 as a fifth **equal** scoring term anyway. That conflict
is what this leg prices.

**CONTROL, run first: PASSED.** The 5-term score plus the 50 km separation rule rebuilt
`data/top10_frozen.json` exactly — same ten faults, same order, scores within 1e-3. A
perturbation of a list I cannot rebuild is a perturbation of the wrong list.

**BAR i — MEMBERSHIP IS REAL. NOT SUPPORTED.** Needed Jaccard ≥ 0.7 against the frozen set
in ≥ 4 of 5 leave-one-leg-out variants. Achieved in **0 of 5.**

| leg dropped | Jaccard | kept of 10 |
|---|---|---|
| length | 0.667 | 8 |
| age | 0.538 | 7 |
| L1 quartz | 0.538 | 7 |
| slip | 0.429 | 6 |
| junction | **0.250** | **4** |

Removing junction density — the term whose own author recorded it as "partly a mapping
artefact" — replaces six of the ten. No leg can be removed without changing the list.

**BAR ii — MEMBERSHIP IS RESOLVED. NOT SUPPORTED.** Needed ≥ 7 of the frozen ten at
P(in top ten) ≥ 0.80 under one-vertex L1 resampling, 10,000 draws. Achieved: **4.**

| frozen rank | site | P(top 10) | P(gated out entirely) |
|---|---|---|---|
| 1 | Madison fault | **1.000** | 0 |
| 2 | Round Valley fault | **1.000** | 0 |
| 3 | Little Valley fault | **1.000** | 0 |
| 4 | Centennial fault | **1.000** | 0 |
| 5 | Antelope Valley fault zone | 0.672 | **0.327** |
| 6 | Fish Lake Valley fault zone | 0.541 | **0.334** |
| 7 | Red Rock fault | 0.674 | 0 |
| 8 | Helena valley fault | 0.746 | 0 |
| 9 | Sand Springs Range fault | 0.590 | **0.337** |
| 10 | Mosquito fault | 0.409 | 0 |

The `p_gated_out` column is a distinct failure from the `p_top10` one and is separated on
purpose. Three of the frozen ten sit at `quartz_frac` = 0.25 — exactly the gate — so a
one-vertex wobble does not demote them, it **removes them from the 225 altogether**, about
a third of the time. They are not marginal members of the list; they are marginal members
of the *population the list is drawn from*.

**And the intruders are the sharper half of this bar.** Sites outside the frozen ten that
enter it under the same wobble, P ≥ 0.05:

| site | P(enters top 10) | site | P(enters top 10) |
|---|---|---|---|
| **Sandia fault** | **0.505** | S. Sangre de Cristo fault | 0.341 |
| Bear River fault zone | 0.476 | Mono Lake fault | 0.272 |
| Teton fault | 0.453 | McAfee Canyon fault | 0.246 |
| | | Hunter Mtn–Saline Valley fz | 0.068 |

**Sandia — the screen's own declared positive control, and the site A4 and A6 spent two
legs failing to rescue — is a coin flip for membership in the top ten.** It is not on the
frozen list and it is in the top ten in 50.5% of draws. Nothing about the physics changed;
one vertex of one layer did.

**BAR iii — ORDER IS RESOLVED. NOT SUPPORTED.** Needed ≥ 5 of the 9 adjacent pairs holding
their printed order in ≥ 95% of draws *in which both sites were on the list at all.*
Achieved: **4 of 9** — and the conditioning is the finding.

| pair | P(order holds) | draws with both present |
|---|---|---|
| Madison > Round Valley | 1.000 | 10,000 |
| Round Valley > Little Valley | 0.667 | 10,000 |
| Little Valley > Centennial | 0.893 | 10,000 |
| Centennial > Antelope Valley | 1.000 | 6,724 |
| Antelope Valley > Helena valley | 1.000 | 4,831 |
| Helena valley > Fish Lake Valley | **0.342** | 3,888 |
| Fish Lake Valley > Red Rock | 0.811 | 3,552 |
| Red Rock > Sand Springs Range | 0.724 | 3,744 |
| Sand Springs Range > Mosquito | 1.000 | 2,280 |

**Three of the four pairs that "hold perfectly" hold on a shrinking subsample** — the last
one on 22.8% of draws. The denominator was split out precisely so a membership failure
could not launder itself into an order success, and here it earns its keep: a pair that
never once swaps, in the quarter of draws where both sites still exist, is a much weaker
statement than the 1.000 makes it look. The one unconditioned 1.000 is Madison > Round
Valley.

**A7-iv — WHY, and it is arithmetic rather than interpretation.** Effective degrees of
freedom of the five equally-weighted terms across all 225 survivors:

| term | distinct values | modal value | modal share | sd |
|---|---|---|---|---|
| slip | 4 | 0.0 | **86.2 %** | 0.164 |
| junction | 5 | 1.0 | 32.4 % | 0.369 |
| age | 6 | 0.2 | 37.3 % | 0.273 |
| L1 quartz | 7 | 0.25 | 30.7 % | 0.281 |
| length | **75** | 0.458 | 4.9 % | 0.170 |

**One of the five terms is the same number for 86% of the field.** Three more are coarse
ordinals with five to seven levels. Exactly one term — fault length, the one carrying the
least physical claim — is near-continuous. The composite is therefore a **coarse lattice**,
and a difference smaller than one lattice step is not a difference. This is not a
criticism of any one leg; each was built to *filter*, and four of the five are being asked
to *rank*, which is a strictly harder job that nothing ever checked they could do.

**A7-v — WHAT THE LIST ACTUALLY RESOLVES.** Rank 10 scores 0.6134. One L1 vertex is worth
0.025 of composite score. **23 of the 225 survivors sit within one vertex of the rank-10
line.** The top-ten cut is not a cut; it is a line drawn through the middle of a
23-member band by a quantity finer than the instrument.

**And the head of the raw ranking is one place.** Before the 50 km separation rule is
applied, ranks 1–3 of all 225 are:

| score | site | distance from Madison |
|---|---|---|
| 0.8370 | Madison fault | — |
| 0.7698 | Red Canyon fault | 13.7 km |
| 0.7670 | Hebgen fault | 11.6 km |

All three are the 1959 M7.3 **Hebgen Lake** surface rupture. Seven of the 225 survivors lie
within 50 km of Madison. The separation rule collapses them to one entry, correctly — but
it means the screen's single strongest signal is **one 1959 earthquake, counted three
times**, and the frozen list's ranks 2 and 3 are the second and third best scores *more than
50 km from a better one*, which is a different quantity from the second and third best
scores. Frozen rank 4, Centennial fault, clears the separation rule by **4.8 km**.

**WHAT A7 SETTLES.** Not "the ranking is wrong" — the ranking is *finer than the
measurement*. The defensible product is:

- **one resolved position**: Madison fault (Hebgen Lake), P(top 10) = 1.000, the only
  adjacent order relation that holds on a full denominator, and separated from the rest by
  0.10 of score — four lattice steps;
- **a head-set of four** (Madison, Round Valley, Little Valley, Centennial): membership
  certain under L1 wobble, **internal order not resolved** — Round Valley > Little Valley
  holds only 66.7% of the time;
- **a band of 23** the score cannot order, which includes Sandia, Teton and Bear River, and
  from which three current members can vanish entirely.

Printing 1..10 asserts nine order relations the instrument can support four of, three of
those on a quarter of the sample. **The report must print a head, a set and a band — not a
league table.** Any further criterion added to break the band's ties must be declared and
tested *as a tie-breaker*, against this measured resolution, or it will merely add a fifth
coarse ordinal to four others and move names around at random.

### A9 — Day 199. The deliverable, built to A7's measured resolution rather than the score's printed one.

Not a leg. It measures nothing new and must not. `code/candidate_list.py` renders the one
artefact Clayton asked for — the places, with their uncertainty attached rather than
stripped off — and it exists because A7 left the previous rendering indefensible.
Reprinting "rank 1..10" with "but see A7" underneath is not a fix; it is the shape of the
defect this project keeps catching in other people's work. The fix is to print the
structure that was measured.

**THREE RULES, declared in the module before it was first run.**

- **R-A — an integer position requires a full denominator.** A site gets a printed rank only
  if the order relations on *both* sides of it hold at ≥ 0.95 across all 10,000 draws with
  both sites present. A pair that never swaps in the 22.8% of draws where both still exist
  is a resolved order *conditional on a membership failure*, which is a different claim.
  The rule is derived, not fitted: if a future re-run resolves more pairs, more positions
  print with no edit. Applied to the current data it yields **exactly one integer: Madison
  fault = 1.**
- **R-B — tiers are membership, not rank.** HEAD = P(top ten) 1.000 and never gated out
  (**4 sites**). BAND = within one L1 vertex of the rank-10 line and not in HEAD
  (**19 sites**). FIELD = the remaining **202**. Rows are emitted **alphabetically** inside a
  tier. The score is still printed — hiding it would be its own dishonesty — but it does not
  set the row order and is labelled as not resolving one.
- **R-C — jurisdiction is a filter flag, never a score.** National Forest land raises no
  physical probability of anything. It can make a site *eligible* for the founding claim. It
  cannot make a site better.

**FIVE GUARDS, each present because its absence has already cost this project something.**
G1 aborts if A7's reproduction control did not pass. G2 aborts on any name present in one
source and missing from another, because a quiet inner-join drop shortens the deliverable
and looks like a shorter deliverable. **G3 — the absent column**: if a leg has not run, its
column is emitted as the literal `UNRUN` on every row plus a top-level status, and is never
omitted; an omitted constraint column reads as *no constraint applied*, which is the exact
shape of every absence-as-result defect logged here. **G4 — the order guard runs against the
emitted rows, not against my intention**: at most the sites R-A resolved may carry a
position, and no tier may come out in score order, so an edit that reintroduces the league
table fails the build instead of shipping. G5 records the path and byte length of every
input read.

**THE EMITTER'S OWN FIRST DEFECT, found and fixed in the same sitting, and reported because
it is the module's own lecture turned back on it.** A7 publishes membership probabilities in
*two* tables — `A7ii_membership` for the frozen ten and `A7ii_intruders_p_ge_005` for
everyone else above the 5% reporting floor. The first draft read only the first and printed
an em dash for the rest. That put a blank where a measurement existed, and it blanked it
hardest for **Sandia at 0.505** — the single most consequential cell in the file. Fixed:
both tables are read, and below the floor the cell reads `<0.05`, which means
measured-and-small rather than unknown.

**SEPARATION SUPPRESSION, now named per row.** A band member can carry a high score and
P(top ten) < 0.05 for a reason unrelated to its score: a better-scoring survivor sits within
50 km and the frozen rule keeps one per neighbourhood. **Red Canyon scores 0.7698 — second
highest of all 225 — and never appears, because Madison is 13.7 km away.** Printing `<0.05`
beside `0.7698` with no explanation invites the reader to conclude the score is noise. Six
band members carry this flag.

**AREAS — the coarser question, and the one Clayton actually asked.** The screen emits
faults; A7 says the fault-level order is not resolved. Single-linkage clustering of head and
band at **the frozen list's own 50 km separation scale** — deliberately not a new free
parameter — collapses the 23 named structures into **13 areas**, four of them containing a
head site:

| area | centroid | extent | structures |
|---|---|---|---|
| Madison fault (Hebgen Lake) | 44.844, −111.343 | 13.7 km | 4 |
| Round Valley fault (Sierra front / Walker Lane) | 37.759, −118.654 | **115.1 km** | 7 |
| Little Valley fault (Carson Range) | 39.190, −119.855 | 11.8 km | 2 |
| Centennial fault | 44.584, −112.066 | 0 km | 1 |

Nine further areas hold one structure each, including Sandia, Teton and Bear River.

**Two properties of that view are printed rather than smoothed.** First, **member count is
not evidence** — it inherits the identical mapping-density artefact A7-iv priced in the
junction term, so it never orders the areas. What clustering buys is the opposite: it stops
the same place being counted several times. Second, **single linkage chains**, and the chain
is visible in the extent column rather than hidden by it: the Round Valley "area" is 115 km
across, which is a **corridor, not a locality**, and is named as one. Sensitivity of the
area count to the link scale, printed because Centennial separates from Madison by 4.8 km of
margin:

| link | 30 km | 40 km | 50 km | 60 km | 75 km |
|---|---|---|---|---|---|
| areas | 16 | 14 | 13 | **10** | 9 |

**WHAT THE ARTEFACT CARRIES IN ITS HEADER, not in a footnote.** A6's verdict — the founding
gate was asked once whether it fires where anomalous lights are independently reported, and
0 of 6 control locales pass it while 34.4% of random western ground does. The list is
therefore **a search plan, not a finding**: places ranked by a geophysical criterion whose
predictive validity is undemonstrated and, on the one external test run so far, unsupported.

Output: `data/candidate_list.json`, `reports/CANDIDATE-LIST.md`. As of writing, the
jurisdiction column reads `UNRUN` on every row because A8 is still querying; `code/watch_a8.py`
is the trigger that rebuilds the deliverable when A8 lands, so the rebuild does not depend on
a future breath remembering to do it.

> **STATUS UPDATE, Day 199 15:46:54 — the trigger fired.** `work/a8_chain.log`: `data/jurisdiction_leg.json`
> landed at 164,850 bytes, `candidate_list.py` re-ran at exit 0, `HEAD 4 · BAND 19 · FIELD 202`,
> `jurisdiction: RUN`. The paragraph above is left standing as written rather than edited, because
> what it describes — a mechanism with a clock attached — is the thing that worked, and rewriting
> it to the past tense would erase the evidence that it did.

### A8 — Day 199. The founding constraint, applied for the first time. It is decisive and it does not discriminate.

The screen was born from a Forest Service observation. **It had never once been asked whether
Forest Service land is where its own survivors are.** `code/jurisdiction_leg.py`, two independent
USFS services — the administrative-boundary layer (`EDW_ForestSystemBoundaries_01`) and the basic
ownership layer (`EDW_BasicOwnership_01`) — against 400 random western points drawn inside the
survivors' own bounding box, seed 20260818.

**Both bars declared before the first query, and they split.**

| | survivors (n = 225) | random western ground (n = 400) | contrast |
|---|---|---|---|
| ADMIN boundary | 25.78% | 18.75% | **+7.0 pp** |
| OWNership | 25.78% | 19.25% | +6.5 pp |

**BAR i (discriminates): FAILS at +7.0 pp.** **BAR ii (decisive for the band): PASSES, and hard —
it removes 13 of the 23 contender-band sites**, including Madison (rank 1), Centennial, Antelope
Valley, Fish Lake Valley, Sand Springs Range, White Mountains, Bear River, Red Rock, Mono Lake,
McAfee Canyon, Teton, Helena valley and Southern Sangre de Cristo.

**That combination is the finding, and it is uncomfortable.** A criterion that barely separates
survivors from random ground but deletes 57% of the shortlist is not measuring the hypothesis —
it is measuring land tenure and then reshuffling the answer with it. **Recorded as a flag on each
row, never as a score and never as a gate**, which is rule 3 of A9's deliverable, now with the
measurement that earns it.

**The confound is stated in the artefact itself, not discovered later:** National Forest land is
mountainous public land, and Quaternary range-front normal faults are mountainous. The correlation
runs *toward* the hypothesis, which is the entire reason the matched null exists.

### A11 — Day 199. Drop the dead weight. One term dies, and dropping it is a TRADE, not a gain.

Clayton's direction: *"drop the dead weight and reweigh on terms with actual resolution."*
**Resolution measure declared before scoring:** `sep(term) = 1 − Σ share²` — exactly the probability
that two randomly drawn sites get different values from that term. No free parameter. **Dead-weight
bar: sep < 0.5**, justified as the best a perfectly balanced binary flag can do.

| term | sep | distinct | modal share | verdict |
|---|---|---|---|---|
| length | 0.9785 | 75 | 0.049 | RESOLVES |
| L1 (quartz) | 0.8156 | 7 | 0.307 | RESOLVES |
| junction | 0.7794 | 5 | 0.324 | RESOLVES |
| age | 0.7475 | 6 | 0.373 | RESOLVES |
| **slip** | **0.2445** | 4 | **0.862** | **DEAD WEIGHT** |

**The bar killed exactly one term and did not over-kill** — worth stating, because a bar that kills
everything is not a bar. `slip` separates 24% of site pairs; its value for 86.2% of the field is one
number, and the 14% that differ differ by a **USGS slip-rate reporting-class boundary**, which is a
mapper's binning decision rather than a measured rate.

**Both reweighings then failed to buy anything.** 10,000 draws, two variants — R1 equal-weight on
survivors, R2 separation-weighted:

| variant | BAR A (resolution gain) | BAR B (order gain) | BAR C (stealth shuffle) |
|---|---|---|---|
| R1 equal | **PASS** 4 → 5 resolved | **FAIL** — order pairs 6 → 4 | **TRIGGERED**, Jaccard 0.4286 |
| R2 sep-weighted | **PASS** 4 → 5 resolved | **FAIL** — order pairs 6 → 3 | **TRIGGERED**, Jaccard 0.4286 |

**Verdict: TRADE, NOT A GAIN.** One bar up, the other down, and **over half the shortlist changes
membership** for it. Removing a term that resolves nothing still moves names, because it was
contributing a constant that the other terms were being read against. Filed as measured; the frozen
list is not re-cut on this.

### A12 — Day 199. Jurisdiction on Clayton's four classes. The prediction held, and the class he named most confidently runs backwards.

Clayton's direction: *"it's very likely all sites will sit in either government, federal, military,
or Native land."* A8 (USFS only) stays; A12 widens to the four. Classes mapped onto **BLM National
Surface Management Agency layer 1** (`ADMIN_DEPT_CODE` / `ADMIN_AGENCY_CODE`) and **TIGERweb AIANNHA
layers 2/3/4**. **Layers 7–10 deliberately excluded**: Oklahoma Tribal / State Designated / Tribal
Designated *Statistical* Areas are census geographies, not land tenure, and counting them as Native
land would silently double the class across eastern Oklahoma. Null borrowed from A8 — same seed,
same bbox, same sequence — so the two legs stand on identical ground.

**The prediction, declared first, was that the filter would NOT discriminate**, because federal
ownership alone is roughly half the eleven western states.

**The positive control caught two defects before the leg ran.** (1) My own docstring was false: it
claimed the "without PriUnk" service excludes private parcels, so an empty response meant
no-public-agency — the service returns `PVT` as a feature, on 2 of 5 control points. (2) **I had
hand-guessed the agency codes and guessed wrong — `FS` where the service says `USFS`.** Every Forest
Service point, the founding claim's own class, would have scored `federal = False`. Fixed by pulling
`returnDistinctValues`: 33 authoritative (dept, agency) pairs. **One query removed the need to be
lucky**, and `unmapped_agency_codes` is emitted as a field — currently `[]` — so a future
classification miss cannot read as a class absence.

| class | survivors | random western ground | contrast |
|---|---|---|---|
| federal | 68.44% | 50.25% | **+18.19 pp** |
| **union of all four** | **74.22%** | **55.50%** | **+18.72 pp** |
| military | 3.56% | 1.75% | +1.81 pp |
| govt (state/local) | 4.89% | 3.75% | +1.14 pp |
| **tribal** | **1.78%** | **8.50%** | **−6.72 pp** |
| private | 26.22% | 32.00% | −5.78 pp |
| union **within 10 km** | **98.28%** | **69.10%** | **+29.18 pp** |

**BAR i (discriminates): PASSES.** **BAR ii (decisive): FAILS** — 5 of the 23-band removed, 21.7%.
**BAR iii (fallback becomes a class label): FAILS**, which is the good outcome: the 10 km buffer is
reported as its own field and never merged into `union`, because "on federal land" and "within 10 km
of federal land" are different claims and merging them launders the weaker one.

**Three consequences, two of them against the hypothesis as stated.**

1. **Tribal land is ANTI-correlated with this screen's survivors** — 1.78% against a base rate of
   8.50%, the only negative class, inverted by nearly a factor of five. Three of Clayton's four
   hold; the fourth does not. This is a real fact about where Quaternary normal faults sit, not a
   layer defect.
2. **The union cannot be decisive, exactly as predicted.** At 10 km it passes 98.28% of survivors.
   A filter that removes 1.7% of what it filters is a description, not a screen.
3. **And the strict version removes the head of the list.** The five it drops — **Madison (rank 1),
   Centennial (6), Antelope Valley (7), Bear River (14), Helena valley (43)** — are every one `PVT`
   at their own coordinate and every one `near10_union = True`, with BLM / State / USFS inside 10 km.
   The choice is between a filter that deletes the only site A7 resolves to an integer position and
   a filter that deletes almost nothing.

### A13 — Day 199. The charge term, generalised past quartz. All three bars fire, and the incumbent gate was excluding almost the whole top of the new term.

Clayton asked whether anything other than quartz is piezoelectrically or electromagnetically active.
**There is — and the answer is worse than "there are others": the strongest lab result in the
literature points at rock this screen currently scores as a NEGATIVE.** `code/lithology_probe.py:45`
lists `basalt`, `gabbro` and `ophiolite` among the terms a site is penalised for containing.

Freund and colleagues loaded air-dry tiles of granite, anorthosite, gabbro, limestone and marble and
measured stress-activated current out of the stressed volume; **anorthosite and gabbro produced
10–50× the current of granite.** The carriers are positive holes activated from **peroxy defects
`O₃X–OO–XO₃`, X = Si or Al** — a defect of the *silicate framework*, present in igneous and
high-grade metamorphic rock generally. Quartz is not required.

> **EVIDENCE GRADE: SECONDARY, carried as a field in `charge_term.json` rather than a footnote.**
> Two independent reads returned the same rock ordering and the same order of magnitude, but both
> paraphrase the same body of work and the primary text could not be read (ScienceDirect 403s; the
> arXiv PDF returned binary the fetcher could not decode). The 10–50× figure is **unconfirmed against
> primary source** and is deliberately **encoded at 2.5×**, because letting one unread paper set a
> weight would let it dominate the ranking. Enough to justify measuring the rock; not enough to rank on.

**A second incumbent defect nobody in this project had stated:** bulk piezoelectric response requires
crystallographic alignment. Randomly oriented quartz grains in a granite largely cancel. The
classifier already half-knows this — it separates `TIER_FABRIC` from `TIER_PLUTONIC` and says at
`lithology_probe.py:25` that the distinction is deliberate — **and then the screen collapses both
into one `quartz_frac` and ranks on the sum. The distinction was measured and then discarded.**

**Six pathways, weights declared before any node was scored**, scored as a **weighted max, not a sum**
(a sum would let a rock mediocre on four pathways outscore one excellent on the strongest, which is an
additivity claim nobody has evidence for):

| pathway | w | signature |
|---|---|---|
| P1a peroxy, mafic | 1.00 | gabbro, anorthosite, norite, diabase, basalt, granulite, amphibolite |
| P2 piezo, **aligned** | 0.75 | quartzite, mylonite, quartz vein, schist, orthogneiss, tourmaline pegmatite |
| P4 piezomagnetic | 0.50 | magnetite, iron formation, serpentinite, ultramafic, skarn |
| P5 conductive channel | 0.50 | graphite, black shale, sulphide, pyrite, serpentinite |
| P1b peroxy, felsic | 0.40 | granite, granodiorite, gneiss, monzonite, syenite |
| P3 piezo, **unaligned** | 0.25 | granite, rhyolite, aplite — the incumbent term at the weight its own cancellation argument implies |

**The P1 split was forced by the smoke test**, which is why it exists: on one P1 list granite scored
1.00 exactly as gabbro did, and BAR iii could never have fired.

**Population: all 507 stage-2 nodes (392 distinct faults), NOT the 225 gate survivors.** This is the
whole point and not an efficiency choice — scoring a generalised term only on rock that already passed
a *quartz* gate builds the fixture where the right and wrong answers agree.

**RESULTS. 384 of 392 scored; 8 errors, reported not absorbed.**

| bar | declared before scoring | measured | verdict |
|---|---|---|---|
| i — **distinct** from the incumbent | Spearman ρ(charge, quartz) < 0.7 | **ρ = 0.2547** | **PASSES** |
| ii — **consequential** | the terms disagree about the head | **49 of the top 50 by charge were gated OUT by quartz** | **PASSES** |
| iii — **mafic actually moves** | the rock Freund points at rises | **n = 157 mafic, median rank move = 132 places** | **PASSES** |

**ρ = 0.25 is the number that matters.** The two terms are very nearly orthogonal — not two
measurements of one property, two different properties, of which this screen has only ever measured
one. **49 of the top 50 sites on the new term never entered the old ranking at all**: not ranked low,
*gated out*.

**Every claim here is about which rock the term selects, which is measured. None of it is about how
much current that rock makes, which is not.**

**And the top site loses ground on its own generalisation.** Madison at `quartz = 1.00 → charge = 0.75`
— its gneiss is felsic-peroxy and aligned-piezo rather than mafic. The pre-registered prediction
survived contact with the site that had most to lose from it.

### A15 — Day 199. The radiogenic / radon term. Clayton asked for it; it comes back negative for radon and positive for granite.

Pre-registered in `code/radon_leg.py` before the first sample: mechanism, three populations,
a written prediction, and five bars. The prediction was that this leg would return a null on
every bar carrying new information. **It did, and then went one better — the radon-specific
statistic is significant in the direction OPPOSITE to the hypothesis.**

**THE INSTRUMENT, AND THE THREE WRONG TURNS IT SURVIVED.** All three return plausible numbers
rather than errors, and all three are recorded in `code/radiometric_grid.py` because the next
person will take them too.

1. **The service name that answers about a different dataset.** `mrdata.usgs.gov/services/nuresed?…GetCapabilities` returns a 349,783-byte well-formed WMS capabilities document — for the **mineral deposits** service, full of `mrds-` layers. A deliberately nonsense service name returns 1,511 bytes and no layers. So "it responded and it parsed" does **not** establish that you reached the dataset you named. The control is what separated them; the name actually used, `aerorad`, was read off the dataset's own page.
2. **The file that looks like data and is a picture.** `data/NArad_U_geog83.tif` is 42.8 MB, is served as `image/tiff`, and is named for the element and the datum. It is **PIL mode RGB, 8 bits per channel, with no GeoTIFF transform tags at all** — a rendered colour map. Sampling it returns legend colours that can be reported as ppm uranium. The data is `NAMrad_U.zip` → a 4-byte-float ESRI binary raster.
3. **The grid is not geographic.** `xllcorner -3501000, cellsize 2000` are metres in a projected frame. Parameters were read from the product's own `.flt.xml`, not assumed: spherical transverse Mercator, R = 6378206.4 m, k₀ = 0.926, central meridian −100°, datum NAD27 — the DNAG projection. The transform was then checked against ground truth **it was not built from**: the metadata separately declares the grid's geographic bounding box, and scanning the grid footprint recovers it to 0.51° against a 0.25° scan step. The discriminating fixture: **Grants NM, one of the largest uranium districts on the continent, returns 22.8 ppm eU = 15.8× the grid median**, and the deep Pacific returns no-data.

**WHY eTh IS THE WHOLE DESIGN.** Airborne gamma spectrometry cannot see uranium; it sees the
1.76 MeV line of Bi-214, a *daughter of Rn-222*, and back-calculates ppm assuming secular
equilibrium — hence *equivalent* uranium. Thorium's gaseous daughter is Rn-220, half-life
55 s against radon's 3.8 d, so thoron cannot migrate. eU and eTh track each other across rock
types. Therefore **high in both = felsic lithology, which A13 already scores; high in eU
*relative to* eTh = uranium decoupled from its rock-forming twin, which is the only new
signal available.** Raw eU is a rock-type map wearing a radon label, and reporting it as
"the radon term" would be this project's signature defect committed deliberately.

**RESULTS.** 225 survivors · 400 random western points (same seed and bbox as A8/A12) · 326
non-survivor stage-2 faults. Permutation test, 10,000 relabellings, difference of medians.

| statistic | survivors | random ground | other faults | p vs random | p vs faults |
|---|---|---|---|---|---|
| eU (ppm) | 2.164 | 1.979 | 2.130 | **0.020** | 0.731 |
| eU, 10 km mean | 2.318 | 2.051 | 2.164 | **0.0001** | 0.153 |
| eTh (ppm) | 8.533 | 7.175 | 6.984 | **0.0001** | **0.0005** |
| **eU/eTh** | **0.2619** | 0.2774 | 0.2710 | **0.015** | 0.149 |
| **eU/eTh, 10 km** | **0.2585** | 0.2767 | 0.2736 | **0.0018** | **0.0067** |

- **BAR 0 COVERAGE — passed, narrowly, and it is the bar that could have manufactured everything else.** The grid is 27.7% populated and the holes are not random: this is largely NURE-era flying, and **NURE flew where uranium was being prospected**, so coverage correlates with uranium prospectivity. Survivor coverage 98.7%, random ground 86.0% — a 12.7 pp gap against a 15 pp bar. It passes, but the gap is real and it runs one way only: the unflown ground excluded from the null is basin and plain, which is *low* in radioelements, so excluding it makes the null too high and the survivor contrast **conservative**. The direction is safe; the honesty is that it was checked before the values were compared, not after.
- **BAR i ELEVATED — PASSED.** Survivors carry more eU than random western ground.
- **BAR ii RADON-SPECIFIC — FAILED, and not by absence.** eU/eTh is **lower** on survivors than on random ground, p = 0.015 (10 km: p = 0.0018). Significant in the direction opposite to the hypothesis. "Failed" here does not mean "no effect"; it means the effect points the wrong way.
- **BAR iii NOT-JUST-FAULTS — FAILED the same way.** The 10 km ratio does differ from other Quaternary faults (p = 0.0067) — again *lower*. And raw eU does **not** differ from other faults at all (p = 0.731).
- **BAR iv INDEPENDENT — passed.** ρ(eU/eTh, screen score) = **−0.029** across survivors. The radiogenic term is essentially orthogonal to everything the screen already computes.

**WHAT IT MEANS.** The largest effect in the table is **eTh**, not eU: +1.36 ppm over random
ground and +1.55 over other faults, both at p ≤ 0.0005. Thorium is immobile and its daughter
cannot travel. A screen that selects strongly on thorium has selected **felsic and alkaline
crystalline rock** — which is a lithology finding, belongs to A13, and is not news. And
because eTh rises faster than eU, the *ratio falls*: on the screen's own ground, uranium is
**depleted relative to thorium**. Mechanistically that is the signature of uranium having
been mobilised as the uranyl ion by oxidising groundwater and carried away — a **loss** of
the radon parent, not a concentration of it.

So the leg answers Clayton's question cleanly and against the project's interest: **the
screen's sites are not radon-rich. They are thorium-rich, which is to say granitic, which the
screen was already selecting for by other means.** Per the pre-registered rule for a BAR ii
failure, this leg reports itself as **redundant with A13** and contributes no scoring term.

**AND ONE THING IT DOES CONTRIBUTE, which is worth more than a term.** ρ = −0.029 means the
radiogenic axis is genuinely independent of the screen. The top of the eU/eTh ordering
(Sheep-East Desert Ranges 0.483, Tinajas Altas 0.467, Nacimiento 0.453) is drawn almost
entirely from *low-ranked* survivors — ranks 166, 222, 39. Only **Sand Springs Range (rank
10)** appears in the top fifteen. Using this as a re-ranking criterion would therefore
reshuffle the list almost completely, and A7's tie-breaker rule forbids exactly that: a
criterion may not reorder the 23-member band unless it has been tested *as a tie-breaker*
against the band's measured resolution. It has not been, and on bars ii and iii it has no
warrant to be. **It is a label, not a rank.**

**A NOTE ON THE OTHER DIRECTION, because it is the honest half.** Radon is a documented
neurotoxicant whose decay products are retained alpha emitters. Had this leg found high-radon
ground, it would have strengthened the *ordinary* explanation for "places where people report
feeling strange", not the extraordinary one. It found the opposite, which removes a mundane
confound from the sites the screen names. That is a small, real, and unglamorous contribution.

---

# A14 — THE WATER / ELECTROKINETIC TERM

**Landed 2026-08-18 18:17:44 (Day 199), 2h05m after launch. Pre-registered in
`code/water_leg.py`'s docstring before the first query: mechanism, sign of sigma,
populations, prediction and five bars.** Filed by the evening-integration drive,
which found it had landed and found the amendment's own status table still saying
`RUNNING` — the mechanism-with-a-clock fired and logged, and nothing owned the
filing. Same shape as A8. Named here rather than quietly fixed.

## The declared prediction, and what happened to it

The docstring committed to this, in these words: *"Survivors will show substantially
more springs and more relief than NULL-RANDOM (near-tautological) and will show NO
significant difference from NULL-FAULT on any of the three terms. I expect this leg
to return a null on every bar that carries information."*

| bar | test | result |
|---|---|---|
| **i LEAKS** | springs vs NULL-RANDOM | **PASS** — 70 vs 30.0, p=0.0001. Expected; means little. |
| **ii DISCRIMINATES** | springs vs NULL-FAULT | **FAIL** — 70 vs 61.5, diff +8.5, **p=0.4051** |
| **iii GRADIENT** | relief vs NULL-FAULT | **PASS** — 733.1 m vs 439.1 m, +294 m, p=0.0001 |
| **iv PERENNIAL** | perennial flowlines vs NULL-FAULT | **PASS** — 55 vs 11, +44, p=0.0001 |
| **v INDEPENDENT** | rho(water, screen) below 0.7 | **PASS** — rho = **0.0832**, near-orthogonal |

n: survivors 225, NULL-FAULT 326, NULL-RANDOM 400 for the NHD terms and **370 for the
two 3DEP terms** — 30 random points returned no elevation sample. The denominators
differ *within one table* and are printed per row rather than stated once at the top.

Read off that table alone, A14 is the project's first strong positive: two of three
information-carrying bars fire hard against the matched control, and the term is
orthogonal to the incumbent score. **Both of the next two sections take that away.**

## THE TIE-BREAKER CLAIM IS DEAD — and it died of a units mismatch I wrote myself

A7 imposed a constraint on every new criterion: it may only reorder the 23-member
contender band if it separates that band by more than the band's own score wobble.
The leg's own emitted answer looked emphatic —

    water_score_spread = 0.6934      screen_score_spread = 0.2797

— a 2.5x separation. **It is not a comparison.** `water_score` is *rank-normalised
over the 225 survivors* (`rank_norm`, `code/water_leg.py:457`), so it spans 0 to 1 by
construction and is uniform by construction. `score` is the screen's raw composite.
The two spreads are in different units and their ratio means nothing. I wrote both
lines, in the same function, and the emitted note (*"Reported, not asserted"*) did
not save me from reading it as a result.

**The test it should have run, run now.** Permute `water_score` across the 225 and
recompute the band's spread — 20,000 draws, seed 20260818:

    observed band spread          0.6934
    null median                   0.6845      5th pct 0.5476   95th pct 0.8110
    P(random relabelling <= obs)  0.5404

The observed separation sits at the **54th percentile of a random relabelling of its
own values.** A14 does not separate the band. It is a **LABEL**, exactly as the
docstring's fallback clause required, and the incumbent ordering stands.

And there is a second, worse problem with the comparison as specified: the contender
band was *defined by A7 as the set of near-ties on the screen score.* Its screen-score
spread is small **by construction**. Any other variable on earth will look more
separating on that set. The comparison was circular before it was mis-united, and the
permutation null is the only version of it that carries information.

## AND BAR iv DOES NOT SURVIVE ITS OWN CONFOUND

Bars iii and iv are not two findings. Relief discriminates at +294 m; perennial water
follows relief, because water runs downhill from where the head is. Stratifying the
survivor / NULL-FAULT comparison by pooled relief quartile:

| relief quartile | n surv | n fault | surv median | fault median | diff | p |
|---|---|---|---|---|---|---|
| Q1 (below 300.8 m) | 22 | 116 | 27.5 | 0.0 | **+27.5** | **0.0037** |
| Q2 (300.8–559.8) | 43 | 95 | 8.0 | 18.0 | −10.0 | 0.4755 |
| Q3 (559.8–867.4) | 81 | 57 | 48.0 | 29.0 | +19.0 | 0.5183 |
| Q4 (above 867.4 m) | 79 | 58 | 111.0 | 88.0 | +23.0 | 0.3123 |

**Three of four strata are null and one points the wrong way.** The p=0.0001 in the
headline table is Simpson's paradox: 160 of 225 survivors sit in the top two relief
quartiles against 115 of 326 matched faults, and perennial mileage tracks relief. The
unstratified test was measuring *terrain*, and terrain is what A7 already knows the
screen selects. The one surviving stratum is the thinnest survivor bucket (n=22)
against a fault median of exactly **0.0** — a floor, not a contrast.

## What A14 actually returns

**The pre-registration was right and my first reading of the bar table was wrong, in
the direction that flattered the project.** The honest statement:

1. The screen did **not** select wetter faults. Spring density is a fault property,
   not a screen property (bar ii, p=0.41).
2. The perennial-water advantage is **terrain re-labelled**, and does not survive
   relief stratification.
3. The water score is genuinely orthogonal to the screen score (rho=0.08) and
   genuinely **useless as a tie-breaker** (permutation p=0.54). Orthogonality is not
   information; a fair coin is orthogonal to everything.
4. What remains standing is **relief**, which is not a water result. It is the
   observation that this screen selects high, steep ground — already priced by A7,
   and a confound that A8 (USFS land is mountainous) and A12 (jurisdiction tracks
   terrain) both flagged from their own directions. Three legs now converge on the
   same nuisance variable.

The correct use of A14 in the rewrite is one sentence in the methods and one line in
the limitations. **It does not change a single name or a single position on the list.**
Its value is that it was pre-registered, so its failure is interpretable — the sign of
sigma was declared before the query, and a version of this leg that scored salinity
positively would have produced a confident, ranked, physically-backwards result.

**A14 closes the leg set. Every leg is now landed and filed.**
