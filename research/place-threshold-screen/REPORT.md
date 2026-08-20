# The Places, and What They Are Worth

### A geophysical screen for anomalous-light locales — round 2, and the external test that came back against it

*Place-threshold screen · Day 200 / 2026-08-19 · supersedes `SUMMARY.md` and `README.md`, both of which
predate every negative result in this document*

---

## Read this part or none of it

Three sentences carry the whole report. They are here rather than in a conclusion because a reader who
stops at the list will otherwise take away the opposite of what was measured.

**1 · The founding gate has now been tested against the outside world, once, and it failed.**
The screen's first criterion — *R1 CONDUIT: within 10 km of a Quaternary normal fault* — fires on
**0 of 6** independently-attested anomalous-light locales, against **34.4%** of random western ground.
The point estimate runs the wrong way: the reported locales are *farther* from Quaternary normal faults
than ordinary land is (median 30.2 km vs 20.1 km, Mann-Whitney p = 0.199). With n = 6 that is weak
evidence and it is not proof of absence — but it is the only external test this project has run, and it
is not support either.

**2 · The list is a search plan, not a finding.** It ranks places by a geophysical criterion whose
predictive validity is undemonstrated. Nothing below licenses the sentence *"these are the places most
likely to carry an anomalous record."* That claim was pre-registered as a separate product, was tested,
and was not earned.

**3 · The strongest structural result in the project is a confound, not a signal.** Five independent
legs — rank resolution, land tenure, jurisdiction, static water, and now flow (§9) — converge on the same
nuisance variable: **this screen selects high, steep, mountainous public ground.** Every apparent positive
so far has, on stratification or residualisation, turned out to be terrain wearing a different label. The
newest one is the cleanest example: stream power separated survivors from the control at p = 0.0025 and
went to p = 0.121 the moment drainage area and relief were held fixed.

What survives all three is a modest thing and it is stated plainly: **a set of places where a specific
piece of physics is most strongly expressed, with its uncertainty attached rather than stripped off.**
That is worth publishing. It is not worth over-reading.

---

## 1 · What was built, and what "ranking" was allowed to mean

Round 1 shipped ten sites and said, correctly, that they were *"ten members of a qualifying class, not
the top ten places in America."* Round 2 was asked to turn that into an actual ranking. Before anything
was computed, the pre-registration split the word in two:

| | claim | what it needs | outcome |
|---|---|---|---|
| **Product A** | these sites express the dilatant-rupture-through-quartz-fabric criterion most strongly | only that the score be internally sound | **ships, with its resolution measured** |
| **Product B** | these sites are most likely to carry an anomalous record | an outcome label and a validated score↔label relationship | **not earned** |

They are printed under different headings here and are never merged. **Any sentence that ranks sites by
criterion strength and is then read as a likelihood claim is the specific error this round exists not to
repeat.**

Everything in this report was declared in `PREREGISTRATION-v2.md` (95 KB, frozen 2026-08-18 before the
first round-2 lookup) or in a dated amendment appended to it. No bar was moved after a number was read.
Where a first reading was wrong, the correction is printed next to it rather than replacing it.

---

## 2 · The external test (A6) — the one that could kill it, run first

The screen's own controls cannot test it. Sandia sits 0.32 km from a Quaternary normal fault and Hubbell
Spring 0.83 km, because **they are Quaternary normal faults**. Comparing them to the criterion is
comparing a definition to a measurement.

So six locales with recurrent anomalous-light records from *outside* this project were assembled, graded
by a stated rule, and committed to code before any value at any control coordinate was computed. Three
contaminations were named in the declaration rather than discovered afterwards: the earth-lights
literature is itself fault-selected; the list is mine, assembled by someone who had already built the
screen; and **observer density is unremoved, with its direction stated — toward the hypothesis.**

### The base rate, printed here for the first time in this project

A requirement filters only to the extent that ordinary ground fails it. Nobody had ever measured what
fraction of ordinary western ground passes R1.

| within | random covered western ground | the six control locales |
|---|---|---|
| 5 km | 21.3 % | 0 of 6 |
| **10 km — R1 CONDUIT as written** | **34.4 %** | **0 of 6** |
| 25 km | 55.2 % | 2 of 6 |
| 50 km | 73.4 % | 4 of 6 |

A third of the random western landscape already satisfies the founding gate. None of the six locales
does. Post-hoc binomials against the measured base rate (labelled post-hoc because they were not
pre-declared): 0/6 at 10 km → p = 0.080; 0/6 at 5 km → p = 0.238; 2/6 at 25 km → p = 0.252. **Not one
reaches p ≤ 0.05.** The direction is uniform and it is against the hypothesis. The evidence is weak, and
n = 6 is why — the pre-registration's power statement was written in advance for exactly this outcome and
is honoured here: *a fail is not proof of absence.*

**One case is checkable geology rather than statistics.** PC2, Toppenish Ridge, is 88.9 km from the
nearest Quaternary normal fault because it belongs to the Yakima fold belt — a *compressional* structure.
One of the two best-graded locales in the set sits in the wrong tectonic regime for the screen's own
dilatancy mechanism.

### And half the control set could not be measured at all

| | no basement-depth node within ±0.10° |
|---|---|
| the 225 survivors | 29 (**12.9 %**) |
| the six controls | 2 (**33.3 %**) |

The USGS basement grid is densest where Quaternary normal faults are — which is what the survivors were
selected on. Coverage is therefore correlated with the screen's own criterion, and it bites the outside
set **2.6× harder** than the inside set. So A6 settles that the leg does not rank independently-attested
locales highly. It does **not** settle whether the criterion is wrong or merely unmeasurable at the
places that would test it.

> **The honest summary of A6:** the screen's founding gate has been asked, once, whether it fires where
> the phenomenon is reported. The answer came back *"no, and not significantly no."*

---

## 3 · What the list actually resolves (A7, A9)

Before adding any further criterion, one question had to be answered: **given the measurement noise the
instruments have already declared about themselves, how many distinct rank positions does this score
resolve?**

No new noise model was invented. Every perturbation was read off a note written by the leg that produced
the number — `quartz_frac` carries ±1/8 sampling noise from vertex ordering alone, a *measured* instance
(Sandia read 0.875 down one path and 1.000 down another: same fault, same eight points, different segment
concatenation order). Ten thousand draws. Three bars, declared first.

| bar | needed | achieved | verdict |
|---|---|---|---|
| **i — membership is real** | Jaccard ≥ 0.7 in ≥ 4 of 5 leave-one-leg-out variants | **0 of 5** | NOT SUPPORTED |
| **ii — membership is resolved** | ≥ 7 of the ten at P(top ten) ≥ 0.80 | **4** | NOT SUPPORTED |
| **iii — order is resolved** | ≥ 5 of 9 adjacent pairs holding at ≥ 95% | **4 of 9** | NOT SUPPORTED |

**Why, and it is arithmetic rather than interpretation.** Effective degrees of freedom of the five
equally-weighted terms across all 225 survivors:

| term | distinct values | modal value | modal share |
|---|---|---|---|
| slip | 4 | 0.0 | **86.2 %** |
| junction | 5 | 1.0 | 32.4 % |
| age | 6 | 0.2 | 37.3 % |
| L1 quartz | 7 | 0.25 | 30.7 % |
| length | **75** | 0.458 | 4.9 % |

One of the five terms is the same number for 86% of the field. Three more are coarse ordinals with five
to seven levels. **Exactly one term — fault length, the one carrying the least physical claim — is
near-continuous.** The composite is a coarse lattice, and a difference smaller than one lattice step is
not a difference. Rank 10 scores 0.6134; one quartz vertex is worth 0.025 of composite score; **23 of the
225 survivors sit within one vertex of the rank-10 line.** The top-ten cut is not a cut. It is a line
drawn through the middle of a 23-member band by a quantity finer than the instrument.

Two further facts the old ranking hid:

- **Three of the frozen ten sit exactly at the gate** (`quartz_frac` = 0.25). A one-vertex wobble does
  not demote them — it removes them from the 225 altogether, about a third of the time. They are not
  marginal members of the list; they are marginal members of the population the list is drawn from.
- **Sandia — the screen's own declared positive control — is a coin flip.** It is not on the frozen list
  and it enters the top ten in **50.5%** of draws. Nothing about the physics changed; one vertex of one
  layer did.

### So the deliverable prints a head, a set and a band — not a league table

Three rules, declared in `code/candidate_list.py` before it was first run, with five guards. **R-A:** an
integer position requires a full denominator — a pair that never swaps in the 22.8% of draws where both
sites still exist is a resolved order *conditional on a membership failure*, which is a different claim.
Applied to the data it yields **exactly one integer.** **R-B:** tiers are membership, not rank; rows are
emitted alphabetically inside a tier. **R-C:** jurisdiction is a filter flag, never a score.

**HEAD — 4 sites. P(top ten) = 1.000, never gated out. Internal order NOT resolved.**

| site | lat, lon | score *(not an order)* | eligible | note |
|---|---|---|---|---|
| **Madison fault** — *position 1, the only resolved integer* | 44.792, −111.438 | 0.8370 | NEAR (≤10 km) | basement-scoreable in only 32/40 variants |
| Round Valley fault | 37.542, −118.726 | 0.7324 | IN | |
| Little Valley fault | 39.237, −119.886 | 0.7112 | IN | basement-scoreable in only 32/40 variants |
| Centennial fault | 44.584, −112.066 | 0.6812 | NEAR (≤10 km) | clears the 50 km separation rule by 4.8 km |

Round Valley > Little Valley holds in only 66.7% of draws. **The head is a set of four, not a ranking of
four.**

**BAND — 19 sites the score cannot order.** Alphabetical. `P(top10)` is measured, not asserted; a blank
means suppressed by the separation rule rather than by score.

| site | lat, lon | score | P(top 10) | eligible | why it is here |
|---|---|---|---|---|---|
| Antelope Valley fz | 38.677, −119.548 | 0.6244 | 0.672 | NEAR | falls out of the 225 entirely in 32.7% of draws |
| Bear River fz | 41.091, −110.812 | 0.6064 | 0.476 | OUT | not on the frozen ten; basement UNSCOREABLE |
| Fish Lake Valley fz | 37.694, −118.114 | 0.6174 | 0.541 | NEAR | falls out of the 225 in 33.4% of draws |
| Hartley Springs fz | 37.644, −119.003 | 0.6368 | — | IN | suppressed: Round Valley at 26.9 km |
| **Hebgen fault** | 44.858, −111.324 | **0.7670** | — | IN | suppressed: Madison at 11.6 km |
| Helena valley fault | 46.759, −112.049 | 0.6240 | 0.746 | OUT | |
| Kings Canyon fz | 39.143, −119.823 | 0.6542 | — | IN | suppressed: Little Valley at 11.8 km |
| McAfee Canyon fault | 37.686, −117.968 | 0.5962 | 0.246 | OUT | not on the frozen ten |
| Mono Lake fault | 38.079, −119.181 | 0.5918 | 0.272 | NEAR | not on the frozen ten |
| Mosquito fault | 39.327, −106.140 | 0.6134 | 0.409 | IN | basement UNSCOREABLE (no node in window) |
| **Red Canyon fault** | 44.864, −111.297 | **0.7698** | — | IN | **second-highest score of all 225** — suppressed: Madison at 13.7 km |
| Red Rock fault | 44.660, −112.698 | 0.6168 | 0.674 | NEAR | |
| Sand Springs Range fault | 39.190, −118.338 | 0.6160 | 0.590 | OUT | falls out of the 225 in 33.7% of draws |
| **Sandia fault** | 35.153, −106.472 | 0.6108 | **0.505** | IN | the screen's own positive control; basement-scoreable in 24/40 variants |
| Silver Lake fault | 37.800, −119.121 | 0.6592 | — | IN | suppressed: Round Valley at 45.1 km |
| S. Sangre de Cristo fault | 36.849, −105.551 | 0.5936 | 0.341 | NEAR | basement UNSCOREABLE |
| Teton fault | 44.013, −110.682 | 0.6016 | 0.453 | NEAR | basement UNSCOREABLE |
| West Fork fault | 44.863, −111.313 | 0.6382 | — | IN | suppressed: Madison at 12.6 km |
| White Mountains fz | 37.867, −118.465 | 0.6008 | — | NEAR | suppressed: Round Valley at 42.8 km |

**FIELD — the remaining 202 survivors.** Measured, ranked below the band, not printed here.

### The head of the raw ranking is one earthquake

Before the 50 km separation rule is applied, ranks 1–3 of all 225 are Madison (0.8370), Red Canyon
(0.7698, 13.7 km away) and Hebgen (0.7670, 11.6 km away) — **all three are the 1959 M7.3 Hebgen Lake
surface rupture.** Seven of the 225 survivors lie within 50 km of Madison. The separation rule collapses
them to one entry, correctly, but the consequence should be said out loud: **the screen's single
strongest signal is one 1959 earthquake, counted three times.**

### Areas, which is the coarser question and the one actually asked

Single-linkage clustering of head and band at the frozen list's own 50 km scale — deliberately not a new
free parameter — collapses 23 named structures into **13 areas**, four containing a head site:

| area | centroid | extent | structures |
|---|---|---|---|
| Madison fault (Hebgen Lake) | 44.844, −111.343 | 13.7 km | 4 |
| Round Valley (Sierra front / Walker Lane) | 37.759, −118.654 | **115.1 km** | 7 |
| Little Valley (Carson Range) | 39.190, −119.855 | 11.8 km | 2 |
| Centennial fault | 44.584, −112.066 | 0 km | 1 |

Nine further areas hold one structure each, including Sandia, Teton and Bear River. Two properties are
printed rather than smoothed. **Member count is not evidence** — it inherits the same mapping-density
artefact that the junction term does, so it never orders the areas. And **single linkage chains**: the
Round Valley "area" is 115 km across, which is a **corridor, not a locality**, and is named as one.
Sensitivity to the link scale, printed because Centennial separates from Madison by only 4.8 km of
margin: 30 km → 16 areas · 40 → 14 · **50 → 13** · 60 → 10 · 75 → 9.

---

## 4 · The terrain confound — four legs, one nuisance variable

This is the strongest structural result the project has, and it is not a result anyone wanted. Four legs
built for four different reasons all land on the same place.

**A7 (rank resolution).** Of the five scoring terms, the only near-continuous one is fault *length*.
The screen's ordering is substantially an ordering by how long a mapped fault trace is.

**A8 (land tenure).** The screen was born from a Forest Service observation and had never once been asked
whether Forest Service land is where its own survivors are. Two independent USFS services against 400
random western points drawn inside the survivors' own bounding box:

| | survivors (n = 225) | random western ground (n = 400) | contrast |
|---|---|---|---|
| USFS administrative boundary | 25.78 % | 18.75 % | **+7.0 pp** |
| USFS basic ownership | 25.78 % | 19.25 % | +6.5 pp |

**Bar i (does it discriminate?) FAILS at +7.0 pp. Bar ii (is it decisive?) PASSES, and hard — it removes
13 of the 23 band sites**, including Madison, Centennial, Teton, Bear River and Helena valley. That
combination *is* the finding, and it is uncomfortable: **a criterion that barely separates survivors from
random ground but deletes 57% of the shortlist is not measuring the hypothesis — it is measuring land
tenure and then reshuffling the answer with it.** Recorded as a per-row flag, never as a score, never as
a gate. The confound is stated in the artefact itself: National Forest land is mountainous public land,
and Quaternary range-front normal faults are mountainous.

**A12 (jurisdiction, on the four classes Clayton named).** The prediction — declared first — was that
this filter would *not* discriminate, because federal ownership alone is roughly half the eleven western
states.

| class | survivors | random western ground | contrast |
|---|---|---|---|
| federal | 68.44 % | 50.25 % | **+18.19 pp** |
| **union of all four** | **74.22 %** | **55.50 %** | **+18.72 pp** |
| military | 3.56 % | 1.75 % | +1.81 pp |
| govt (state / local) | 4.89 % | 3.75 % | +1.14 pp |
| **tribal** | **1.78 %** | **8.50 %** | **−6.72 pp** |
| private | 26.22 % | 32.00 % | −5.78 pp |
| union **within 10 km** | **98.28 %** | **69.10 %** | **+29.18 pp** |

Three consequences, two of them against the hypothesis as stated. **(1) Tribal land is anti-correlated**
with this screen's survivors — inverted by nearly a factor of five. Three of the four classes hold; the
fourth runs backwards, and it is a real fact about where Quaternary normal faults sit, not a layer
defect. **(2) The union cannot be decisive**, exactly as predicted: at 10 km it passes 98.28% of
survivors, and a filter that removes 1.7% of what it filters is a description, not a screen. **(3) The
strict version removes the head of the list** — the five it drops are Madison (the only resolved
position), Centennial, Antelope Valley, Bear River and Helena valley, every one of them `PVT` at its own
coordinate and every one within 10 km of BLM, State or USFS land. The choice is between a filter that
deletes the one site resolved to an integer and a filter that deletes almost nothing.

**A14 (water / electrokinetic).** Detail in §6; the part that belongs here is its residue. What survives
A14 is **relief**: survivors sit at a median 733.1 m of local relief against 487.25 m for matched
Quaternary faults, p = 0.0001. That is not a water result. It is the observation that this screen selects
high, steep ground — already priced by A7 and flagged independently by A8 and A12.

**Four legs, one variable.** Terrain is the strongest thing this screen measures, and terrain is not the
hypothesis.

---

## 5 · The rock question — the largest open problem in the project

Clayton asked whether anything other than quartz is piezoelectrically or electromagnetically active.
There is, and the answer is worse than *"there are others."*

**The strongest lab result in the literature points at rock this screen currently scores as a NEGATIVE.**
`code/lithology_probe.py:45` lists `basalt`, `gabbro` and `ophiolite` among the terms a site is
*penalised* for containing. Freund and colleagues loaded air-dry tiles of granite, anorthosite, gabbro,
limestone and marble and measured stress-activated current out of the stressed volume; **anorthosite and
gabbro produced 10–50× the current of granite.** The carriers are positive holes activated from peroxy
defects `O₃X–OO–XO₃` (X = Si or Al) — a defect of the *silicate framework*, present in igneous and
high-grade metamorphic rock generally. **Quartz is not required.**

> **Evidence grade: SECONDARY, carried as a field in the data rather than as a footnote.** Two
> independent reads returned the same rock ordering and the same order of magnitude, but both paraphrase
> the same body of work and the primary text could not be read (ScienceDirect 403s; the arXiv PDF
> returned binary the fetcher could not decode). The 10–50× figure is **unconfirmed against primary
> source** and is deliberately encoded at **2.5×** — enough to justify measuring the rock, not enough to
> rank on. Letting one unread paper set a weight would let it dominate the ranking.

A second incumbent defect nobody in this project had stated: **bulk piezoelectric response requires
crystallographic alignment**, and randomly oriented quartz grains in a granite largely cancel. The
classifier already half-knows this — it separates fabric from plutonic and says the distinction is
deliberate — **and then the screen collapses both into one `quartz_frac` and ranks on the sum. The
distinction was measured and then discarded.**

So a generalised **charge term** was built: six pathways, weights declared before any node was scored,
combined as a **weighted max rather than a sum** (a sum would let a rock mediocre on four pathways
outscore one excellent on the strongest, which is an additivity claim nobody has evidence for). Scored
over all stage-2 nodes, **not** over the 225 gate survivors — scoring a generalised term only on rock
that already passed a quartz gate builds the fixture where the right and wrong answers agree.

| bar | declared before scoring | measured | verdict |
|---|---|---|---|
| i — **distinct** from the incumbent | Spearman ρ(charge, quartz) < 0.7 | **ρ = 0.2547** | **PASSES** |
| ii — **consequential** | the terms disagree about the head | **49 of the top 50 by charge were gated OUT by quartz** | **PASSES** |
| iii — **mafic actually moves** | the rock Freund points at rises | n = 157 mafic, **median rank move 132 places** | **PASSES** |

**ρ = 0.25 is the number that matters.** The two terms are very nearly orthogonal — not two measurements
of one property, but two different properties, of which this screen has only ever measured one. Forty-nine
of the top fifty sites on the new term never entered the old ranking at all: not ranked low, **gated
out**. And the top site loses ground on its own generalisation — Madison goes from `quartz = 1.00` to
`charge = 0.75`, because its gneiss is felsic-peroxy and aligned-piezo rather than mafic. The
pre-registered prediction survived contact with the site that had most to lose from it.

**Every claim here is about which rock the term selects, which is measured. None of it is about how much
current that rock makes, which is not.**

**And a second leg agrees from the other side.** The radiogenic leg (A15) was pre-registered to test
radon, and the largest effect in its table is not uranium but **thorium**: survivors carry +1.36 ppm eTh
over random ground (p = 0.0001) and, after the control rebuild described in §7, +0.894 ppm over matched
faults (p = 0.014). Thorium is immobile and its daughter cannot travel. **A screen that selects strongly
on thorium has selected felsic and alkaline crystalline rock** — which is a lithology finding, and which
the screen was already selecting for by other means.

**The state of the question, stated as an open problem rather than a result:** two legs, built for
different reasons, agree that the incumbent classifier is selecting on the wrong mineral criterion. **The
list in §3 is still ranked on the incumbent term.** It has not been re-cut, because A7's tie-breaker rule
forbids it: any new criterion may reorder the 23-member band only if it has been declared and tested *as
a tie-breaker* against the band's measured resolution. The charge term has not been. Re-ranking on it now
would be adding a fifth coarse ordinal to four others and moving names around at random.

---

## 6 · The legs that failed, printed failing

A screen with no negative results has not been tested. These are reported at the same weight as the
positives because that is the only way the positives mean anything.

**Dropping the dead term bought nothing (A11).** Resolution measure declared before scoring —
`sep(term) = 1 − Σ share²`, the probability that two randomly drawn sites get different values, no free
parameter; dead-weight bar `sep < 0.5`, justified as the best a perfectly balanced binary flag can do.
The bar killed **exactly one term** (`slip`, sep = 0.2445, one value across 86.2% of the field, and the
14% that differ differ by a USGS reporting-class boundary — a mapper's binning decision rather than a
measured rate) **and did not over-kill**, which is worth stating, because a bar that kills everything is
not a bar. Both reweighings then failed: one bar up (4 → 5 resolved positions), the other down (order
pairs 6 → 4), and **over half the shortlist changes membership** for it (Jaccard 0.4286). **Verdict:
TRADE, NOT A GAIN.** The frozen list is not re-cut on this. Removing a term that resolves nothing still
moves names, because it was contributing a constant the other terms were being read against.

**The water leg reversed on its own controls (A14).** Pre-registered — mechanism, sign of σ, populations,
prediction and five bars — before the first query. Read off its headline table alone it was the project's
first strong positive. Two things took that away, and both were self-inflicted.

*The tie-breaker claim died of a units mismatch I wrote myself.* The leg emitted
`water_score_spread = 0.6934` against `screen_score_spread = 0.2797` — an apparent 2.5× separation. It is
not a comparison: `water_score` is rank-normalised over the 225 survivors, so it spans 0 to 1 by
construction, and the screen score is a raw composite. Both lines were written in the same function, and
the emitted note *"Reported, not asserted"* did not stop me reading it as a result. The test it should
have run, run now — permute the water score across the 225, 20,000 draws — puts the observed separation
at the **54th percentile of a random relabelling of its own values (p = 0.5404)**. A14 does not separate
the band. And the comparison was circular before it was mis-united: the band was *defined* as the set of
near-ties on the screen score, so its screen-score spread is small by construction and any variable on
earth looks more separating on it.

*And the perennial-water bar does not survive its own confound.* Stratifying by relief quartile,
**three of four strata are null and one points the wrong way**; the headline p = 0.0001 is Simpson's
paradox, because 160 of 225 survivors sit in the top two relief quartiles and perennial mileage tracks
relief. The unstratified test was measuring terrain.

What A14 returns: the screen did **not** select wetter faults (springs vs matched faults, p = 0.64); the
water score is genuinely orthogonal to the screen score (ρ = 0.083) and genuinely **useless as a
tie-breaker** — orthogonality is not information, a fair coin is orthogonal to everything. **It changes no
name and no position on the list.** Its value is that it was pre-registered, so its failure is
interpretable: the sign of σ was declared before the query, and a version of this leg that scored
salinity positively would have produced a confident, ranked, physically-backwards result.

**The radon leg came back significant in the wrong direction (A15).** Pre-registered with a written
prediction that it would return a null on every bar carrying information. It did, and then went one
better. Airborne gamma spectrometry cannot see uranium; it sees the 1.76 MeV line of Bi-214, a *daughter
of Rn-222*, and back-calculates ppm assuming secular equilibrium — hence *equivalent* uranium. Thorium's
gaseous daughter has a 55-second half-life against radon's 3.8 days, so thoron cannot migrate. Therefore
high in both = felsic lithology, which the charge term already scores; **high in eU relative to eTh is
the only new signal available.**

Medians, permutation test, 10,000 relabellings. **Read off the rebuilt control** (`radon_leg.json`, Day
200), not the old one — n: survivors 222, random ground 344, matched faults 393.

| statistic | survivors | random ground | matched faults | p vs random | p vs faults |
|---|---|---|---|---|---|
| eU (ppm) | 2.164 | 1.979 | 2.205 | **0.020** | 0.675 |
| eTh (ppm) | 8.533 | 7.175 | 7.639 | **0.0001** | **0.014** |
| **eU/eTh** | **0.2619** | 0.2774 | 0.2763 | **0.015** | 0.067 |
| **eU/eTh, 10 km** | **0.2585** | 0.2767 | 0.2733 | **0.0018** | **0.0075** |

**The radon-specific ratio is *lower* on the screen's sites than on ordinary ground, p = 0.015.** "Failed"
here does not mean "no effect" — it means the effect points the wrong way. Because eTh rises faster than
eU, the ratio falls: on the screen's own ground, uranium is **depleted relative to thorium**, which is
mechanistically the signature of uranium having been mobilised as the uranyl ion by oxidising groundwater
and carried away. **A loss of the radon parent, not a concentration of it.** Per the pre-registered rule
for that failure, the leg reports itself as redundant with the charge term and contributes no scoring
term.

**And the honest half of that result:** radon is a documented neurotoxicant whose decay products are
retained alpha emitters. Had this leg found high-radon ground, it would have strengthened the *ordinary*
explanation for "places where people report feeling strange." It found the opposite, which removes a
mundane confound from the sites the screen names. Small, real, unglamorous.

---

## 7 · Errors found in our own instruments

Every one of these was caught by a control, a guard, or a positive control that existed *because* an
earlier version of this project got burned. They are printed because a methods section that lists only
what worked is a sales document.

**The service that answers about the wrong dataset.** A USGS radiometric endpoint returned a
349,783-byte well-formed capabilities document — for the *mineral deposits* service. A deliberately
nonsense service name returned 1,511 bytes and no layers. **"It responded and it parsed" does not
establish that you reached the dataset you named.**

**The file that looks like data and is a picture.** A 42.8 MB file served as `image/tiff`, named for the
element and the datum, is PIL mode RGB, 8 bits per channel, with **no GeoTIFF transform tags at all** — a
rendered colour map. Sampling it returns legend colours that can be reported as ppm uranium. The
discriminating fixture that settled it: Grants, New Mexico — one of the largest uranium districts on the
continent — returns 22.8 ppm eU, **15.8× the grid median**, and the deep Pacific returns no-data.

**The fault pull that returned one state.** The national Quaternary-fault pull inherited a MapServer
endpoint pointing at **layer 12 — New Mexico**. It returned 16,189 sections: plausible, non-empty, and
entirely New Mexican. What caught it was only that the pull is *tiled and prints per-tile counts* —
Nevada 0, California 0, Idaho 0. **A single-bbox pull would have handed back the same 16,189 features
with nothing to read them against.** Re-pointed, and the pull now refuses to write the file if the
densest normal-fault provinces in the country come back empty. The first corrected run then hit the
service's 40,000-record paging cap, printed a warning, and **would have shipped anyway**; tiles that hit
the cap are now subdivided and recursed. Final pull: 110,356 sections, of which 53,301 carry a normal
sense — subdivision recovered ~1,060 sections the cap had eaten.

**The locality probe that tested my vocabulary instead of my coordinates.** The first control pass built
each gazetteer query from a site's *display* name — "Marfa lights viewing area, TX, USA". Those name a
*phenomenon*; a gazetteer holds *places*. Three of six returned UNRESOLVED, a fourth resolved 1,304 km
away, and **one control locale was dropped from a leg on the strength of it.** The probe and its subject
were mis-specified as a pair: the coordinates were never tested, only my ability to name them. The probe
now runs its own positive control (Albuquerque 0.0 km, Reno 0.3 km) so that UNRESOLVED can be
distinguished from a probe that cannot resolve anything.

**The hand-guessed code that would have zeroed the founding class.** The jurisdiction leg's agency codes
were hand-guessed — `FS` where the service says `USFS`. **Every Forest Service point, the founding
claim's own class, would have scored `federal = False`.** Fixed by pulling the authoritative distinct
values: 33 (dept, agency) pairs. One query removed the need to be lucky.

**The control drawn from the wrong sampling frame — the largest of them.** Two landed legs declared their
control as *"stage-2 nodes that FAILED the gate — the bar that matters."* The code took survivors from
stage 5 and built the control by subtracting survivor *names* from stage 2. Those are different draws:
**159 of 225 survivors — 71% — were never in the file the control was drawn from.** A membership test
cannot tell *"tested and failed"* from *"never on the roster."* The gate's real 1,157 failures were never
used; the control that was used is a **27.5% subset from an earlier, narrower, regionally-concentrated
draw** — precisely the shape that manufactures a terrain difference out of nothing.

It survived a re-read because **a population defect has no signature at the row level**: same schema,
same field names, plausible values, nothing empty, nothing erroring. It was caught by an abort written
for an *unrelated* reason — a coverage guard on a join, which fired at 65/225 and made someone ask why
65. **Write the coverage guard even when the join is obviously fine; it reads a variable nothing else in
the pipeline reads.**

Both legs were re-derived on the true control (`null_fault_true.json`, n rose 314 → 393, coverage
0.963 → 0.983). **Every bar verdict is unchanged.** The numbers moved exactly as a frame artefact should
when it is removed: the thorium contrast survives but is **halved** (p 0.0005 → 0.014), because the old
control was thorium-poor relative to the true failure population. An independent confirmation came from a
quantity nobody was watching and no bar was declared on — control-arm over treatment-arm coverage
collapsed from **3.38× to 0.87×**. A covariate that covers 98% of one arm and 29% of the other is not a
covariate with missing data; **it is a proxy for arm membership.**

**And a correction this section makes to its own first draft.** The memo diagnosing that defect recorded
that the gate's 1,157 failures were *"not stored as a roster anywhere on disk"* — written next to the
word *checked*. **False.** The search was scoped to one project directory; the full join table had been
on disk the whole time in another repository, where the pipeline originally ran before the project moved.
**A negative existence claim silently inherits the scope of the search that produced it.** It cost a
correct diagnosis an incorrect price tag: hours of refetching were quoted for something that was a file
read away, and the rebuild then took four minutes.

---

## 8 · Limitations

- **n = 6 on the only external test.** A6 is the test that matters and it is badly underpowered. A fail
  is not proof of absence; it is also not support.
- **The outcome label is folklore.** Blinding the collector removes *our* thumb. It does not remove the
  world's patchiness.
- **Observer density is unremoved throughout**, and its direction is toward the hypothesis.
- **Coverage correlates with the criterion.** The basement grid is densest where Quaternary normal faults
  are; the radiometric grid is 27.7% populated and NURE flew where uranium was being prospected. Both
  were checked before the values were compared, and both run in directions that are stated per leg.
- **The water leg's relief-quartile stratification has not been re-run on the rebuilt control.** The
  headline relief contrast was re-derived and held (733.1 m vs 487.25 m, p = 0.0001); the stratified
  re-analysis that killed the perennial bar was computed on the old control and is carried forward as-is.
  Named here rather than left for a reader to find.
- **The list is ranked on a term two other legs now say is the wrong one.** See §5.
- **Product A can be honest and still be uninteresting.** A criterion ranking with no demonstrated
  predictive content is a well-documented sort order. That was written into the pre-registration as a
  real possible outcome, and it remains the most likely reading of this round.

---

## 9 · The current term — landed, and it is a third negative result

*This section was written as "still running" and amended in place at 22:30 on Day 200 when the leg
landed, per the convention below. Nothing above the amendment line was retracted.*

**A16 — the current / electrokinetic-flow term.** Clayton's contribution, arrived Day 200: *rushing
water, rivers, anything with a current, alongside electromagnetically active minerals — hydroelectricity,
as it were.* That is, independently and cold, the leading prosaic hypothesis for Hessdalen (Hauge and
colleagues have argued a variant of it for years), and it is a sharper question than the static-water leg
A14 asked, because it puts the *flow* rather than the *presence* of water in the mechanism.

Pre-registered before it ran. Its coverage guards pass — charge coverage 92.0% on survivors against 92.8%
on the control, an asymmetry of **1.01×** against a guard that fires above 2.0×, which is itself the clean
confirmation that the control rebuild in §7 worked. Populations, seed and radii inherited unchanged from
A14; two-tailed by declaration; 20,000 permutations; 225 survivors against 400 null-fault and 400
null-random. Flow terms are NHDPlus HR EROM within 10 km: peak velocity, peak discharge, and stream power
Ω = ρg·Q·S paired **on the same reach**, because taking max(Q) against max(S) across different reaches
invents a reach that does not exist.

### The result

**No bar passed, and no name moves.** The declared guard was that A16 may not reorder the list unless bars
ii, iii and v all pass. Velocity does not separate survivors from the fault control (median 1.578 vs 1.487
ft/s, *p* = 0.087), and it does not leak against the random control either (*p* = 0.205), which is the
clean half — a flow term that separated survivors from *random ground* but not from *other faults* would
have been measuring faults, not flow.

One contrast did come out positive, and it is the reason this section is longer than a null deserves.
**Stream power separates survivors from the fault control at *p* = 0.0025** — median 471 W/m against
173 W/m, a factor of 2.7. Taken alone that is the strongest single number Clayton's hypothesis has
produced anywhere in this project.

**It does not survive its own confound control.** Stream power is discharge times slope; both scale with
catchment size and terrain, which is the same nuisance variable §4 spent four legs on. Residualised on
drainage area and relief, the contrast falls to ***p* = 0.121** (n = 966 pooled points). The 2.7× was
mountains.

### The deviation, declared rather than buried

The pre-registration froze the residual control set as [log₁₀(area), **petma**, relief] — petma being
NHDPlus HR's mean annual potential evapotranspiration, the precipitation proxy. **That field is served as
literal zero on every reach in the country.** A count query returns 24,264,177 rows where `petma IS NOT
NULL`, and every one of them is 0. The pipeline's own NODATA guard reads 0 as *not a measurement* rather
than as *no evapotranspiration* — correctly — so the control was `None` on 1,025 of 1,025 rows in all
three arms, the regression excluded every point, and **the primary declared statistic returned n = 0 and
labelled itself `insufficient n`.**

That is the shape this project is most afraid of: the leg would have read as a clean null while the one
significant number sat in it with its control silently unrun. It did not fabricate — it reported its own
gap — but a reader seeing five failed bars would not have gone looking.

**The deviation: PET is dropped and the residual is fitted on the two controls that exist in the data**
(area and relief). That is a departure from the frozen design and is recorded as such in
`data/current_leg_a16b.json`, with both fits printed — the pre-registered three-control model at n = 0,
and the two-control model at n = 966. It does not touch the bar arithmetic: bars i, ii, iii and v all read
velocity, not stream power, so `may_reorder_list` was already `false` before this amendment and is `false`
after it. **The deviation changes an untested null into a tested one. It does not change the verdict.**

### Bar iv — run on Day 201, and the reason it was carried as unrun was already stale

*This subsection replaces a paragraph that said bar iv "remains `UNRUN`" because the A13 charge population
was stage-2 rather than the gate survivors, "priced at a ~1,003-fault rebuild." **That paragraph
contradicted this section's own opening 47 lines above it,** which reports the coverage guards passing at
92.0% / 92.8%. Both sentences could not be true. The rebuild it priced had already been done — Day 200,
14:53, a 1,405-fault roster — four and a half hours before A16 ran. The guard did not fire and bar iv did
not stop there. The correction is recorded rather than silently swapped, because a wrong reason on a
shipped page is worse than a missing result: it tells the next reader the repair is expensive when it is
already paid for.*

**What actually stopped it was `petma` — the same defect, one consumer further down.** Bar iv is built on
`omega_max_wpm_resid`, the residual the amendment above rebuilt. The amendment refit the *contrast* on the
two controls that exist and did not propagate to bar iv, which is the only other consumer of that field.
So the interaction inherited the n = 0 residual and emitted `{"n": 0, "beta": null, "insufficient n"}` —
and `current_leg.py` then rendered that as `bar_iv_status: "FAIL"` rather than `UNRUN`, because the status
line tests `bar_iv is None` while the comparison had already collapsed a null *p* to `False`. **An
untestable statistic printed as a failed test.** That mapping is a defect in a frozen file; it is filed,
not silently patched, and it is named here because the reader is entitled to know the data file and this
prose disagreed.

Run under the amendment's already-declared deviation — no new fetch, no new deviation, an offline refit of
the frozen construction with the control set changed and nothing else — **bar iv comes out PASS at
*p* = 0.0086** (n = 207 survivors against 363 controls). That would be the first bar in A16 to pass
anything.

**It is an artefact, and the control that says so was built before the result was believed.** The frozen
construction rank-normalises both marginals, multiplies them, and regresses log₁₀ of the product on the
two marginals *unlogged*. Since log(a·b) = log a + log b, the residual is a curved deterministic function
of the marginals — and the marginals are wildly unbalanced between arms (median charge score 0.5625 on
survivors against 0.0938 on the control). Evaluating a curve at systematically different places in two
groups produces a difference with no interaction present.

The test for that corrupts exactly one thing: permute `charge_score` **within each arm**, which preserves
every arm's charge distribution, its coverage count and all flow values, and destroys only the pairing
between a fault's charge and its own flow residual. Under that shuffle the interaction is zero by
construction. **In 200 such runs the test fired at *p* < 0.05 two hundred times** — median null *p* =
0.0005, the permutation floor. The observed 0.0086 sits at the **98th percentile** of a null distribution
built from data with no interaction in it; 196 of 200 no-signal runs were *more* significant than the real
one.

**So bar iv's honest status is neither `UNRUN` nor `PASS`: the statistic as pre-registered cannot
distinguish an interaction from a marginal shift, and on this data it does not.** Water × charge is a
null, reported as one. `data/current_leg_a16c.json` and `data/current_leg_a16c_calibration.json` carry both
fits and the full calibration; `code/a16c_bar_iv_calibration.py` is a two-sided instrument that could have
cleared the bar and did not.

One suspicion of mine died in the same pass and is recorded because it was wrong: I expected the marginal
charge gap to be circular — the control arm is drawn from the 1,157 faults that *failed* the L1 quartz
gate, and the charge term scores quartz-bearing rock among its five pathways. A13 had already measured
that and declared a bar on it: Spearman ρ between `charge_score` and `quartz_frac` is **0.2802**, against
an independence bar set at < 0.7. The charge term is not the quartz gate restated. The marginal gap is
reported, as before, without a causal reading — but not for the reason I assumed.

Per this project's convention, an unrun bar is emitted as `UNRUN` with a reason on every row and is never
silently omitted, because an omitted constraint column reads as *no constraint applied*. Bar iv is no
longer unrun; it is run, calibrated, and null.

**So: Clayton asked for the water and the rock, and got three negative results.** The flow hypothesis is
not refuted as physics — Hessdalen is one valley and this is a screen over 1,399 American fault sections
with no anomaly labels on it. What is refuted is that flow, measured this way at this scale, carries any
signal that reorders this list.

---

## 10 · Provenance

Every physics input is a published, citable product. No proprietary layer, no hand-digitised anything.

- **Quaternary faults** — USGS Quaternary Fault and Fold Database, MapServer layer 21 (national), tiled
  pull with recursion on paging-cap hits: 110,356 sections, 53,301 normal-sense.
- **Depth to basement** — Shah, A.K. & Boyd, O.S., 2018, *Depth to basement and thickness of
  unconsolidated sediments for the western United States*, USGS Open-File Report 2018-1115,
  [doi:10.3133/ofr20181115](https://doi.org/10.3133/ofr20181115). 1 km node spacing, WGS84.
- **Lithology** — Macrostrat.
- **Radiometrics** — NURE-era airborne gamma-ray survey, USGS North American radiometric compilation
  (4-byte-float ESRI binary grid; DNAG projection parameters read from the product's own metadata and
  verified against an independent declared bounding box to 0.51° at a 0.25° scan step).
- **Hydrography and relief** — USGS NHD (springs FTYPE 458, perennial flowlines FCODE 46006) and 3DEP.
- **Land tenure** — USFS `EDW_ForestSystemBoundaries_01` and `EDW_BasicOwnership_01`; BLM National
  Surface Management Agency layer 1; TIGERweb AIANNHA layers 2/3/4 (layers 7–10 deliberately excluded —
  those are census statistical geographies, not land tenure, and counting them as Native land would
  silently double the class across eastern Oklahoma).

**Reproducibility, stated as it is rather than as it should be.** Round 1's provenance paragraph claimed
anyone could re-run the pipeline. As of Day 199 that was true of the *sources* and false of the
*pipeline* — four intermediates were referenced by path and absent from the repository. The full
1,399-row stage-5 join has since been recovered and committed (`data/stage5_join_rows.json`), along with
the true control population (`data/null_fault_true.json`). Every leg emits the path, byte length and
mtime of every input it read. Legs that cannot currently be re-run end-to-end from a clean checkout are
named in the pre-registration rather than papered over.

**The full record**, including every bar that was declared and every one that failed, is
`PREREGISTRATION-v2.md` in this directory: the frozen design plus dated amendments A1–A17. Nothing above
this line was edited after a number was read; where a first reading was wrong, the correction sits beside
it with its date.

---

*Place-threshold screen, round 2. Written Day 200, 2026-08-19. Clawd Iggulden-Schnell, with Clayton
Iggulden-Schnell, who asked for the water and the rock and got three negative results
for his trouble.*

🦞🧍💜🔥♾️
