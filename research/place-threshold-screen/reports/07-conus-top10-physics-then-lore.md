# The continental top 5 — ranked on physics alone, with the lore held out

*Day 196, 2026-08-15, late. Answers Clayton directly: "narrow down the list to the top 5
sites… take into account any local or Native American lore… our report can be more than
just Sandia." It is built on `work/transport_screen_stage2.json` (Addendum 3) and adds one
criterion, one stability test, and a held-out lore pass.*

---

## 1. The one design decision that makes this a test instead of a curation

June's survey demoted **Tijeras–Cañoncito** for having no light-record. That is ranking a
site on the thing the mechanism is supposed to *predict*, and it makes the prediction
unfalsifiable — every winner has lights because having lights is how you win.

So the score here contains **no lore, no sighting count, no light-record, no proximity to
any facility.** Four physics terms only:

| | criterion | source | weight |
|---|---|---|---|
| **P1** | recency of Quaternary rupture (conduit currency) | Qfaults `age` | 0–3 |
| **P2** | dilatant sense — normal faults open permeability, thrusts close it | Qfaults `slip_sense` | gate, not a term |
| **P3** | quartz-rich crystalline at the trace | Macrostrat geologic map | 0–2 |
| **P4** | **junction density** — distinct dilatant systems with trace inside 15 km | same cached pull | 0–2, capped |

**P3 weights fabric above pluton** (`TIER_FABRIC` 2.0, `TIER_PLUTONIC` 1.4), which inverts
the intuition that granite is the piezo rock. Bulk piezoelectric moment in an equigranular
pluton averages toward zero because the c-axes point everywhere; a tectonic fabric —
gneiss, quartzite, mylonite — is the case where they don't. That is `lithology_probe`'s own
docstring, applied instead of quoted.

**P4 is new here** and is the property that survived Addendum 3's deflation at Sandia: the
result there wasn't "granite," it was *where the Hubbell system runs into the Sandia
system.* A fault intersection is a permeability maximum. ⚠ Its bias is stated and not
corrected: fault-*name* density is partly a mapping artefact, so a valley mapped at
1:24,000 out-scores an identical one mapped once at 1:250,000. Capped at 2.0 for that
reason, never allowed to dominate.

Then the lore is looked up **afterward, per site, including the sites where I expected to
find nothing.** That ordering is the whole point: it converts "these places have lore" from
a selection effect into a prediction that could have failed.

---

## 2. The list

`work/site_rank.py` over the 62 nodes that cleared P3, deduplicated to one node per fault
system:

| # | score | site | age | rock | rate | sys≤15 km |
|---|---|---|---|---|---|---|
| **1** | **8.99** | **Madison fault**, 44.792 −111.438 — Hebgen Lake, MT | **historic** | gneiss | 0.2–1.0 mm/yr | 6 |
| **2** | **8.19** | **Centennial fault**, 44.584 −112.066 — Centennial Valley, MT | latest Q | quartzite | 0.2–1.0 | 5 |
| **3** | **8.17** | **Teton fault**, 43.557 −110.862 — Grand Teton, WY | latest Q | gneiss | 0.2–1.0 | 7 |
| **4** | **7.72** | **Sawatch fault**, 39.094 −106.380 — Upper Arkansas graben, CO | late Q | gneiss | <0.2 | 5 |
| **5** | **7.38** | **S. Sangre de Cristo fault**, 36.849 −105.551 — Questa/Taos, NM | latest Q | gneiss | <0.2 | 3 |
| 6 | 7.38 | Mount Rose fault zone, 39.214 −119.816 — Tahoe/Reno, NV | latest Q | granodiorite | 1.0–5.0 | 13 |
| 7 | 7.10 | Helena valley fault, 46.759 −112.049 — MT | late Q | quartzite | <0.2 | 5 |
| 8 | 6.95 | East Pintwater Range fault, 37.036 −115.548 — Desert NWR, NV | late Q | quartzite | <0.2 | 7 |
| 9 | 6.90 | Wasatch fault zone, 40.871 −111.855 — UT | latest Q | gneiss | 1.0–5.0 | 2 |
| 10 | 6.90 | N. Sangre de Cristo fault, 38.344 −105.950 — San Luis Valley, CO | latest Q | gneiss | <0.2 | 2 |

**Madison is #1 on a fact, not a weighting: it is one of the very few faults in the country
whose `age` field reads `historic`** — the 1959 M7.3 Hebgen Lake earthquake put a scarp on
the ground that people photographed. Everything else in the top ten last ruptured before
writing.

### 2b. How much of that ordering is the weights?

400 trials with every weight drawn uniformly over a ±50% band, re-ranking each time.
Share of trials in which each system is top-5:

```
100.0%  Madison fault          <- unconditional
100.0%  Centennial fault       <- unconditional
100.0%  Teton fault            <- unconditional
 57.8%  Sawatch fault
 51.5%  Mount Rose fault zone
 40.8%  Southern Sangre de Cristo
 24.2%  East Pintwater Range
 20.0%  Wasatch fault zone
  5.2%  Helena valley fault
```

So the honest statement is: **the top three are a result, and slots 4–5 are a coin-flip
between five sites.** Anyone who reports "the top 5" without that second sentence is
reporting their own weight choices. Sawatch and Southern Sangre de Cristo hold the printed
slots; Mount Rose beats one of them in half of all reasonable weightings.

---

## 3. The deflation that has to come before the lore — three of the top five are ONE fact

Madison, Centennial and Teton are 44.79/−111.44, 44.58/−112.07 and 43.56/−110.86. They sit
inside a ~150 km triangle around the **Yellowstone hotspot's tectonic parabola** — the belt
of young, large, basement-cored normal faults that the migrating hotspot leaves flanking
its track. Their agreement is **not three independent confirmations of the profile. It is
one fact about one province,** reported three times because the thinning rule counts
faults, not provinces.

Last breath's lesson row states the general case: repeated output across supposedly
independent units is a shared cause until something rules one out. Here nothing rules it
out.

Regrouped by province, the country's answer is shorter and more useful:

| province | members in the top 10 | best score |
|---|---|---|
| **Yellowstone parabola** (MT/WY/ID) | Madison, Centennial, Teton *(+Blacktail, Lemhi below)* | 8.99 |
| **Rio Grande rift, northern arm** (CO/NM) | Sawatch, S. Sangre de Cristo, N. Sangre de Cristo | 7.72 |
| **Walker Lane / Sierra front** (NV/CA) | Mount Rose *(+Fort Sage, Granite Springs)* | 7.38 |
| **Lewis & Clark line** (MT) | Helena valley *(+Canyon Ferry, Mission, Bitterroot)* | 7.10 |
| **Southern Basin & Range** (NV) | East Pintwater *(+Black Mountains)* | 6.95 |
| **Wasatch front** (UT) | Wasatch fault zone | 6.90 |

**On a province basis the Rio Grande rift places second in the continental United States** —
and that is the province Sandia is in.

---

## 4. Where Sandia actually lands

Scored on its **trace** lithology (75% of 16 sampled trace points quartz-rich, one unit
literally named *Sandia Granite*) rather than the at-point probe that failed it:

```
6.65   Sandia/Hubbell junction  ~34.98N −106.51   6 systems within 15 km   -> ~9th nationally
6.27   Hubbell Spring fault (own rock, 3% quartz along trace)
5.65   Sandia fault, granite trace point 35.074 −106.490 (only 3 systems)
5.43   La Jencia fault, Socorro
```

**The junction is roughly ninth in the country on these criteria, not first.** It loses on
exactly one term — P1. Its faults last ruptured in the late Quaternary at 0.05–0.2 mm/yr;
Madison ruptured in 1959. Nothing about the rock or the structure is inferior; the *clock*
is slower. Clayton's own framing survives this untouched — the geophysics of the area is
the right class, and the class is well represented at the top of the list. What does not
survive is "the best site in the continental US," which was never measured before tonight
and is not what the measurement says.

**And the list is provisional in a specific, known direction.** It is drawn from the 62
nodes that passed the at-point probe — the probe that gave **Sandia itself a false
negative** by landing 1.5 km off-trace in fan gravel. 445 nodes failed that probe and have
not been re-measured along their traces. `work/trace_lithology_national.py` is running now
(queued behind the base-rate job, 8 trace points per fault, ~445 faults) with **Sandia as
the declared positive control and Hubbell Spring as the declared negative** — if Sandia
isn't rescued and Hubbell is, the pass is void and says so. Until it lands, **the recall of
this top-5 is unmeasured and the true number of qualifying sites is a lower bound.**

---

## 5. The held-out variable: lore, graded

Grades: **A** = documented ethnography or a named primary/official source · **B** = local
folklore with a traceable publication · **C** = internet-repeated claim with no source I
could reach. Most "the Indians called it the place of the spirits" material on the open web
is grade C and is settler invention; it is graded, not laundered.

**1 · Madison fault — Hebgen Lake / Madison Canyon, MT.**
*Native:* the Madison headwaters were the summer range of the **Tukudika (Mountain
Shoshone / "Sheepeaters")**, hunting bighorn to high elevation and wintering low, removed
to Wind River in 1868 — **grade A** for the occupation, **grade C** for any specific site
lore, which I could not source. *Local:* the 1959 quake is the lore — 28 dead under the
Madison Canyon slide, a new lake (Earthquake Lake) that still holds a drowned forest, and
a stack of contemporaneous accounts of **light and noise during the shaking**. Historic
earthquake lights over a gneiss-cored normal fault is the single closest thing in the
country to the mechanism's own claim, and it is documented rather than folkloric.

**2 · Centennial fault — Centennial Valley, MT.** *Native:* Shoshone-Bannock and Blackfeet
travel corridor between the Snake plain and the Madison — **grade A** for use, **nothing
above grade C** for site-specific lore. *Local:* thin — Red Rock Lakes, trumpeter swans,
almost no anomalous record I could find. **This is the site that fails the held-out test,
and it should be reported as loudly as the ones that pass.** A profile that only ever
lands on famous places would be measuring fame.

**3 · Teton fault — Grand Teton, WY.** *Native:* **the Enclosure** — a horseshoe of set
granite slabs ~530 ft below the Grand's summit, found by the Hayden Survey in 1872,
understood as a **Shoshone vision-quest structure**, i.e. a purpose-built site for seeking
revelatory experience placed on top of the range this fault raised — **grade A/B**
(structure and survey date documented; attribution well-attested, not first-hand). *Local:*
Jackson Hole carries a continuous light-in-the-sky folklore, all **grade C**.

**4 · Sawatch fault — Upper Arkansas graben, CO.** *Native:* Ute, and specifically **the
hot springs**. Ute tradition treats both hot and cold springs as *"grandmother water," the
life-giver*, sacred rather than merely useful — **grade A**, and stated by the Southern Ute
Tribe itself, not by a tourism page. The Mount Princeton / Chalk Creek geothermal system
sits directly on this fault. *Local:* Chalk Cliffs, St. Elmo ghost-town folklore — **B/C**.
Worth noting the mechanism reading: this is the top-5 site with **active hydrothermal
upflow on the fault**, i.e. the fluid pathway is not inferred, it is visible and hot.

**5 · Southern Sangre de Cristo fault — Questa/Taos, NM.** *Native:* Taos Pueblo, and
**Blue Lake** — sacred, closed to outsiders, and returned to the Pueblo by act of Congress
in 1970, which is about as documented as sacred status gets — **grade A**. *Local:* **the
Taos Hum.** In 1993, at Rep. Bill Richardson's request, a team from **UNM, Los Alamos,
Phillips Air Force Lab and Sandia National Laboratories** — Mullins, Whitaker, Leher,
Poteet, Kelly — put infrasound mics, **seismic ground sensors** and EM antennas into Taos.
~2% of respondents (161 of 1,440) heard it; the instruments found no source. **Grade A** for
the study, and note what it is: a *federally-convened geophysical investigation of an
unexplained low-frequency phenomenon*, sited on a fault this screen independently ranked
top-5 on rock and rupture alone.

**Near-misses where the held-out variable is loudest:**

- **#8 East Pintwater Range fault, NV** — the node at 37.036/−115.548 sits in the **Desert
National Wildlife Refuge**, which is overlaid by the Nevada Test and Training Range and is
~40 km from Groom Lake. **Pintwater Cave**, on the same range, is a stratified dry cave
with dart and arrow shafts radiocarbon-dated **9,300–3,000 BP**, religiously significant to
the **Moapa Band and Southern Paiute generally**, and it has been **shot at and bombed** —
missile fragments at the entrance, walls collapsed by ordnance. **Grade A** on every clause.
The trifecta Clayton named at Sandia — active dilatant fault in quartz-rich rock, documented
Native sacred site, secretive military overlay — reproduces here **without anyone having
gone looking for it**, on a screen that could not see any of the last two.
- **#10 Northern Sangre de Cristo fault, CO** — the San Luis Valley. **Blanca Peak /
Sisnaajiní**, the Diné **Sacred Mountain of the East**, eastern boundary of the traditional
Navajo homeland, fastened to the earth with lightning and dressed in white shell — **grade
A**. It is also the densest anomalous-report basin in the interior US (1967 "Snippy," the
mutilation cluster, O'Brien's survey work) — **grade B/C**, and I have not audited it.

**Score of the held-out test, stated plainly:** of the five printed sites, **four** carry
grade-A or grade-A/B lore that the ranking could not see, and **one (Centennial) carries
almost none.** Two of the five near-misses carry the strongest grade-A material of all. That
is a real result and it is not a strong one — the base rate of Native sacred sites and
light folklore across the mountain West is high, and I have not measured it. **The correct
control — how often does a randomly drawn Quaternary normal fault in the same provinces
carry grade-A sacred-site documentation? — has not been run, and until it is, section 5 is
suggestive and nothing more.**

---

## 6. What would move this list

1. **`trace_lithology_national.py` finishing.** 445 unmeasured faults; every Sandia-shaped
   false negative in there is a site missing from section 2. Controls declared in advance.
2. **The base-rate run** (`lithology_baserate.py`, 74/80 at writing) — whether four-anomaly
   convergence survives its denominator.
3. **A lore base rate.** Draw 30 dilatant Quaternary faults at random from the same
   provinces, look each up blind, and count grade-A hits. Without that number section 5 is
   a story.
4. **Aeromagnetic depth-to-basement**, which is the correct version of P3 for a *buried*
   crystalline source and would change the ranking of every basin-fill site including
   Hubbell Spring.

*Related: [[hubbell-spring-ADDENDUM3-physics-screen-2026-08-15]],
[[hubbell-spring-ADDENDUM2-nationalscreen-2026-08-15]],
[[feedback_zero_needs_a_positive_control]], [[feedback_novelty_gauge_counts_the_harm]],
[[feedback_sample_drawn_from_one_stratum]], goal #5.*

**Sources (section 5):** [The Enclosure, Grand Teton](https://www.flatcreekinn.com/the-enclosure-the-ancient-structure-on-the-grand-teton/) ·
[Sheep Eaters / Mountain Shoshone](https://www.intermountainhistories.org/items/show/887) ·
[Taos Hum 1993 team](https://www.bibliotecapleyades.net/scalar_tech/the_hum/taos.htm) ·
[Taos Hum coverage](https://www.krqe.com/fox-new-mexico/the-legend-of-the-taos-hum-continues/amp/) ·
[Ute sacred springs — Southern Ute Indian Tribe](https://www.southernute-nsn.gov/2025/10/17/colorado-experience-sacred-hot-springs/) ·
[Blanca Peak / Sisnaajiní](https://en.wikipedia.org/wiki/Four_Sacred_Mountains_of_the_Navajo) ·
[Navajo Prep — Mount Blanca](https://navajoprep.libguides.com/c.php?g=1024484&p=7421337) ·
[Pintwater Cave excavation report](https://escholarship.org/uc/item/5xx4k29b) ·
[Desert NWR and the Nuwu](https://www.intermountainhistories.org/items/show/589) ·
[Desert Refuge is sacred](https://thenevadaindependent.com/article/the-desert-refuge-is-sacred-dont-bomb-it)
