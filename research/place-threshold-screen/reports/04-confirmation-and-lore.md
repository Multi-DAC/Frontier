# Hubbell Spring / Sandia–Manzano — confirmation layers and the lore record

*Day 196 · 2026-08-15, night · goal #5*
*Clayton: "Is there any further research we can do on the area to confirm? Also, what is the
local lore of the area? What about the Native lore for the area, historically? Let's add
this to the report!"*

Third document of the night. It supersedes **§5 and §6 of the CORRECTION** and **§4/§6.1 of
the dossier**, because the first primary source I pulled tonight moved the number the whole
scoring rests on by an order of magnitude — in the direction that closes a leg rather than
opens one.

**Two things happened. Both are demotions of my own instruments, and one of them hands the
star to the pin you said wasn't a bust.**

---

## A. CONFIRMATION — what was run and pulled tonight

### A1. The trench. The driver rate is wrong by 10×, and it is *my* number that is wrong.

Both prior documents scored the pin on **`slip_rate = "Between 0.2 and 1.0 mm/yr"` (mid 0.6)**
— the USGS Qfaults *attribute*. Nobody in this program had read the primary paleoseismology.
It exists, it is on this exact fault, and the trench was dug **on Isleta Pueblo land, 1 km
south of the Kirtland boundary**:

> **Personius & Mahan (2003)**, *Paleoearthquakes and eolian-dominated fault sedimentation
> along the Hubbell Spring fault zone*, BSSA 93(3) 1355–1369, doi:10.1785/0120020031.
> Four surface ruptures. The last three dated by luminescence to **56 ± 6, 29 ± 3, and
> 12 ± 1 ka**. Recurrence **27 and 17 kyr**. Elapsed since last event **12 kyr**.
> Vertical displacement **1–2 m per event**, rupture length 34–43 km, paleomagnitude
> **M 6.8–7.1**. And: *"our preferred average slip rate since rupture event 2 (post-56 ka)
> is **0.05 mm/yr**, and interval slip rates between the last three events are **0.06 and
> 0.09 mm/yr**."*

| quantity | what I used | what the trench measured | ratio |
|---|---|---|---|
| slip rate | 0.6 mm/yr (Qfaults class mid) | **0.05–0.09 mm/yr** | **~10×** |
| implied fault-normal extension (60° dip) | ~0.35 mm/yr | **~0.03–0.05 mm/yr** | ~10× |
| geodetic 2σ floor at fault aperture | 0.578 mm/yr | unchanged | — |
| **bound ÷ signal** | 1.7× short | **~12–19× short** | — |

**Consequences, in order of how much they cost me:**

1. **§5 of the CORRECTION is withdrawn.** "One additional GPS monument in the Manzano
   footwall moves this from undecidable to decided" was sized against an inflated
   prediction. Against 0.04 mm/yr it would take on the order of **10³ independent
   monuments per side**. Not one. Not twenty-four.
2. **The geodetic leg at Hubbell Spring is CLOSED, not deferred.** Sentinel-1 InSAR —
   including the new open **OPERA DISP-S1** time-series product, which does cover CONUS and
   is downloadable from ASF — reaches a few tenths of a mm/yr on 10–40 km baselines at best.
   That is still ~5–10× above the signal. **No instrument I can reach decides this fault's
   interseismic creep.** I should stop writing "cheap discriminator" next to it.
3. **The +0.25 mm/yr fault-normal extension I measured last night is not this fault.** It is
   5–8× the fault's own long-term rate. It is distributed rift extension crossing the whole
   basin. The UNDECIDED verdict stands; its *meaning* changes from "we can't tell if it
   creeps" to "its signal was always a factor of fifteen under our floor."
4. **Finding A is now dead with a primary number rather than an argument.** Recurrence
   17–27 kyr, last event 12 ka: zero M≥2.5 in a 46-year catalogue is not a null result, it
   is the only possible result. The paper says it directly — *no earthquake larger than
   ML 5.5 in the last 150 years in this region.*
5. **One thing survives and it is the piece Fork 1 needed.** 12 kyr elapsed against a 17–27
   kyr recurrence puts the fault **roughly half to two-thirds through its cycle: locked,
   loaded, releasing nothing.** That is precisely Fork 1's picture — residual stress without
   seismicity. The picture is intact; the *magnitude* is an order of magnitude smaller than
   the mechanism was implicitly assuming.

> **The general lesson, and it is the expensive one: a database attribute is a
> classification, not a measurement.** I built two nights of argument, a bound comparison,
> a resolvability criterion and a national screen on `slip_rate` from a GIS field, with the
> trench paper one query away the entire time. *[[feedback_filed_defect_misprices_its_own_subject]]*
> — the row is a measurement and it rots, or in this case was never the measurement at all.

### A2. Lithology from a geologic map, not a density proxy — and the star moves

`work/lithology_probe.py`, Macrostrat geologic-unit queries on a polar grid
(rings 0/2/5/10/15/25/40 km × 8 azimuths). This pays §6.1's named debt.

| site | Bouguer proxy said | **geologic map says** | at the point |
|---|---|---|---|
| ★ Hubbell Spring PIN | granite 2.3 km | **plutonic granite 10 km · fabric 10 km** | Cenozoic sedimentary |
| ◆ **Sandia W scarp** | granite 2.0 km | **plutonic granite 2.0 km** · no fabric ≤40 km | Quaternary sedimentary |
| ○ Tijeras CONTROL | — | plutonic 10 km · "gneiss" 2 km ⚠ | Paleozoic sedimentary |
| Socorro | 12.1 km best | plutonic 15 km · **rhyolite 5 km** | Neogene sedimentary |

**Finding D. On the piezo layer measured against an actual geologic map, the PRIMARY pin is
5× worse than the SECONDARY pin, and the ranking inverts.** The density proxy was right at
Sandia and wrong by ~4–5× at Hubbell Spring — exactly the failure mode §6.1 predicted, but
it flipped the star rather than Socorro. The Llano de Manzano is basin fill over dense
buried basement; **a Bouguer high is depth-to-basement, not distance-to-outcrop**, and the
D137/D138 instrument silently equated them.

**So: you were right that Sandia is not a bust, and the confirming layer supports the Sandia
scarp specifically.** What died is the star's position *within* the cell.

Three honesty items that cut against my own new finding:

- ⚠ **Ring quantization.** "10 km" means *nothing found at 0/2/5, found at 10*. The true
  distance is somewhere in (5, 10]. The 5:1 ratio could be as small as 2.5:1.
- ⚠ **The Tijeras "gneiss" at 2 km is a false positive** — the matched unit is
  *Paleoproterozoic mafic metavolcanic rock*, which is not quartz-rich. The classifier
  matched a term in the lithology string. One known false positive in twelve rows.
- ⚠ **The physics does not love either pin.** The probe's own docstring says it: α-quartz is
  piezoelectric *as an oriented crystal*; in an equigranular pluton the moments randomize
  and the bulk tensor averages toward zero. The tier that carries real physics is
  **TIER_FABRIC** (foliated, aligned quartz). At the Sandia pin fabric is **absent within
  40 km**; at Hubbell it is 10 km. **Both Hessdalen and Brown Mountain sit on fabric at
  0 km.** The re-ranking is real but it happens inside a layer whose physics I have already
  flagged as flattering itself.

### A3. The base rate for A2 — running now, and it is the part that decides whether A2 means anything

Four classic anomaly sites (Hessdalen, Brown Mountain, Marfa, Piedmont MO) all returned
quartz-rich rock within 0–5 km. That *looks* like convergence. It is not a result without a
denominator: "granite within 5 km" may simply be what the western US is made of.
`work/lithology_baserate.py` runs the identical instrument on 40 random western-CONUS land
points and reports the percentile each site sits at. Result appended when it lands.

*This morning's pushed lesson row fired here verbatim — "repeated output across independent
units is a SHARED CAUSE, not agreement." I ran the detector over several sites, got
suspiciously tight agreement, and stopped to build the denominator before reading the
answer. Logging it as a genuine fire, not a coverage miss.*

### A4. What is left that CAN still decide something — ranked by whether it can fail

| # | layer | decides what | verdict on cost |
|---|---|---|---|
| 1 | **Aeromagnetic depth-to-basement** (USGS national mag grid) | the *right* version of the piezo question for a buried source: **how deep is crystalline rock under the pin**, not how far sideways. Gravity + magnetics answer it together and both are public. | cheap, on-machine, **and it is the correct fix for §6.1** |
| 2 | **NURE aeroradiometric eU/eTh/K grids** | independent test of near-surface crystalline rock, *and* a uranium/radon channel along the trace — an ionization proxy that is directly relevant to the plasma reading of Hessdalen | cheap, public, unrun |
| 3 | **Fault-line spring geochemistry** (NM OSE well records, He/Rn) | whether the fault is a live crustal fluid pathway — which is the mechanism that makes the springs exist at all | medium |
| 4 | **USArray/EarthScope MT** | crustal conductor under the pin | medium, and genuinely novel here |
| 5 | Historic report record (NUFORC/Blue Book) by county, **normalised by population and by Falcon-9 twilight-plume dates** | whether the area's modern report rate is anomalous at all | cheap; expect null (see §B7) |
| ~~6~~ | ~~GPS / InSAR creep~~ | ~~Fork 1 vs Fork 2~~ | **RETIRED — 12–19× under the floor (A1)** |

---

## B. LOCAL LORE — the Hispano and Anglo record, graded

The dossier already carried Manzano Base and Bennewitz. This is the rest, and it turns out
to have a structure worth more than any individual item.

1. **Manzano's apple trees.** "Manzano" is *apple*; local tradition says 17th-century
   Spanish missionaries planted the orchards. **Tree-ring dating says after 1800.** A dated
   legend, corrected by a measurement, in the exact valley in question. Keep it as the
   house calibration story.
2. **The rising coffin of Padre Padilla, Isleta.** Fray Juan José de Padilla died at Isleta
   in 1756 and was buried under the church floor. In **1819** the cottonwood coffin rose
   through the floor with the body reportedly intact and flexible; the corpse was treated as
   an *incorruptible* and the church became a pilgrimage site; the coffin surfaced again and
   was examined in **1959**. Mundane reading, and it is a good one: the old church sits on
   the Rio Grande floodplain and the water table lifts a buoyant log coffin. Also routinely
   confused with the 16th-century martyr Fray Juan de Padilla, who is a different person by
   two centuries. **Grade: documented recurring physical event, mundane mechanism, accreted
   narrative.** The template for everything else in this section.
3. **Sandia Cave and "Sandia Man."** Frank Hibben, 1934–1940, claimed a pre-Folsom culture
   at ~25,000 BP; *Time*, 1940. Douglas Preston's 1995 *New Yorker* piece laid out the fraud
   allegations — mammoth bone from a modern gravel pit, artifacts likely emplaced.
   **No longer accepted by professional archaeologists.**
4. **The Los Lunas Decalogue Stone**, Hidden Mountain, ~30 km west of the pin: an 80-ton
   basalt boulder with nine lines of paleo-Hebrew Decalogue. First put into the literature
   **by Frank Hibben, 1933**. Judged a hoax on epigraphic grounds (post-19th-century script
   knowledge, modern tooling, implausible siting); UNM oral tradition points at nearby
   bedrock reading *"Eva and Hobe 3-13-30."*
5. **Manzano Weapons Storage Area / Kirtland**, and **Bennewitz 1979–80** — real lights,
   real AFOSI/Doty disinformation, an alien-base narrative, and a man destroyed. Carried
   forward unchanged from the dossier.
6. **Ambient**: La Llorona along this reach of the Rio Grande; general haunted-place
   inventory around Manzano village. Unweighted.
7. **The modern reporting record.** New Mexico currently ranks top-in-nation for per-capita
   reports, and a large share of recent "mystery light" waves in this exact corridor are
   **Vandenberg Falcon 9 twilight plumes** — sunlit exhaust visible for a thousand-plus km.
   **Any future observation run at this site needs a launch-schedule cross-check before it
   records a single light.** That is a concrete field-protocol item, not a caveat.

### B8. The structural finding, which is the actual payload of this section

> Within ~40 km of the pin, the two most-cited claims of anomalous antiquity — **Sandia Man**
> and the **Los Lunas Decalogue Stone** — trace to **one author, Frank Hibben**, and both are
> now judged fabrications. The most-cited modern anomaly case — **Bennewitz** — is documented
> to have been deliberately fed disinformation by a US counterintelligence office.
> **Three headline anomalies, three identified contamination mechanisms, two named agents.**

This area's lore is not merely weak evidence. It is evidence with a **known adversarial
generator**, twice over — one man building a career, one agency running an operation.
Lore therefore contributes **zero** weight to the pin score, and its function in this
programme is as a **map of failure modes**. The dossier's "THE SITE'S OWN WARNING" section
now has three instances instead of one, and it should be promoted to the front of the file.

---

## C. NATIVE LORE — the rule comes before the content

**The rule.** The pin is on **Isleta Pueblo trust land**. The governing precedent is not
abstract: Elsie Clews Parsons commissioned 189 paintings of ceremonial life from an Isleta
man (Joe B. Lente) under a **written promise never to publish them**; after her death her
student Esther Goldfrank published 140 of them as *Isleta Paintings* (BAE, 1962). The artist
had written *"I don't want any soul to know as long as I live that I have drawn these
pictures."* The American Philosophical Society designated the collection culturally
sensitive and restricted, and **formally deaccessioned and removed it in December 2023.**

So: **this programme does not seek, cite, or score restricted ceremonial knowledge.** Only
what the Pueblos and the NPS publish themselves. A survey that would mine a Pueblo's
religion for coordinates has already become the thing it claims to be studying. And the
practical note is not hypothetical — **the 1997 trench happened on Isleta land, with the
Pueblo's cooperation.** The channel exists and it is the front door.

**What is public, and it is a lot:**

1. **Isleta** — Southern Tiwa, established ~AD 1300 on a lava bench on the west bank; Tiwa
   name published as *Tsugwevaga*, "kick flint" (also rendered *Shiewhibak*); Mission San
   Antonio founded 1612 by Fray Juan de Salas, later San Agustín. The Pueblo holds **329+
   square miles**, bounded east by the Manzanos and west by the Rio Puerco — **the pin is
   inside that, not adjacent to it.**
2. **Sandia Pueblo** — Tiwa *Tuf Shur Tia*, "green reed place"; older records give *Nafiat*,
   "place where the wind blows dust." Sandia Tiwa speakers call the range **Bien Mur**, "big
   mountain." In Tewa the range is **Oku P'in / Oekuu P'in, "turtle mountain" — the sacred
   mountain of the SOUTH** in Tewa directional cosmology. The Pueblo has an active claim to
   the mountain itself.
3. **Springs and lakes as passages.** Pan-Pueblo and published in the general ethnographic
   literature: surface water is one manifestation of a continuous linkage of rivers, springs
   and lakes *in the underworld*; the spirits of the emergence lake can be propitiated at
   other springs because of that aquatic connection; shrines are the points where contact
   between levels of existence is possible. **The pin sits 180 m from a mapped fault-line
   spring.** See §D — this is named precisely so it will not be scored.
4. **Tomé Hill / El Cerro de Tomé**, ~20 km SSW: a 3.5-Myr volcanic remnant carrying
   **1,800+ petroglyphs spanning ~3000 BC to the 17th century**, a landmark for Isleta and
   other Native groups and later for El Camino Real. Since 1947–48 the summit carries three
   crosses and a Good Friday **Penitente** procession. **One landform treated as a threshold
   by three consecutive religious systems** — which is a fact about landforms and human
   attention, and is exactly the fact a portal survey is at risk of misreading.
5. **The Manzano east flank is a landscape of depopulation.** The Salinas pueblos — Quarai
   (Tiwa), Abó, Gran Quivira and Tabirá (Tompiro) — were abandoned through the 1660s–70s
   under drought, famine (450 starved at Gran Quivira), Apache raiding and Spanish
   exploitation; Quarai went last, 1675. Survivors moved to the Rio Grande pueblos,
   **including Isleta**. Isleta had already absorbed refugees from outlying pueblos from
   ~1629. **Any inference from "density of old stories here" must carry this**: the record
   was concentrated by catastrophe and forced movement, not by what happened at a place.
6. **The stage/fraud overlap.** Sandia Cave sits in Sandia Pueblo's ancestral landscape and
   was the stage for Hibben's fabrication. The Native site was used as the setting for an
   Anglo career. That is worth stating in the same breath as §B8.

---

## D. What the lore does to the evidence — the convergence I am refusing to score

There is a real coincidence here and pretending otherwise would be worse than naming it:

> Pueblo cosmology treats **springs as passages between worlds**. The D138 instrument,
> scoring on geophysics with no knowledge of any of this, put its star **180 metres from a
> fault-line spring** — on a fault whose mapped strands are *named for their springs*
> (Hubbell Spring, Carrizo Spring).

**This is a shared cause, not an agreement, and the shared cause is boring and physical.**
A normal fault in a desert basin dams and channels groundwater; water appears at the trace;
springs mark the fault. Therefore:

- ancestral and historic settlement clusters at the springs — **because there is water**;
- the sacred siting attaches to the springs — **because there is water**;
- the geologists mapped and *named* the fault by its springs — **because there is water**;
- and my instrument, scoring "active Quaternary fault," landed on the same line.

One hydrological mechanism generates all four. It is a better explanation than a portal, it
explains the coincidence completely, and — unlike a portal — **it is testable** (§A4 row 3:
spring geochemistry, He/Rn, does the fault carry crustal fluid). The category-convergence
adds **zero** evidential weight and is recorded here so that a future breath finds it already
graded rather than discovering it fresh at 3am and mistaking it for a signal.

---

## E. Net effect on goal #5

**Withdrawn tonight:** the 0.6 mm/yr driver (→ 0.05–0.09); "one more GPS monument decides
it" (→ ~10³); the geodetic/InSAR leg as a live discriminator (→ retired, 12–19× under floor);
the density-proxy piezo ranking (→ inverted, Sandia scarp over Hubbell Spring).

**Standing:** the fault is real, active, **mid-cycle at 12 ka into a 17–27 kyr interval**,
capable of M 6.8–7.1, and locked — which is Fork 1's picture at one-tenth the amplitude.
Sandia is not a bust; on the one layer measured properly tonight it is the **better** pin.

**The honest summary of three documents in one night:** every instrument I pointed at this
site was measuring something other than what its label said — the wrong velocity component,
the wrong aperture, a density high read as an outcrop distance, a GIS class read as a slip
rate. **None of that came from the site. All of it came from me not reading the primary
source before building on the derived one.** The site is exactly where it was on Day 138.
My confidence in the instruments is not.

**Next action, and it is one command's worth of reading, not a survey:** the 2011 GSA chapter
on the *other* Hubbell Spring splays (Carrizo Spring site, "noncharacteristic ruptures,"
large per-event slip variation) — because if the splays differ by an order of magnitude the
"0.05 mm/yr" I just corrected *to* has its own spread, and I would rather find that myself
than have it found for me.

---

*Supersedes §5–§6 of [[hubbell-spring-CORRECTION-2026-08-15]] and §4/§6.1 of
[[hubbell-spring-evidence-dossier-2026-08-15]]. Related:
[[portal-sandia-pin-RESULTS-2026-06-18]], [[feedback_novelty_gauge_counts_the_harm]],
[[feedback_scrutiny_is_motive_shaped]], goal #5.*

**Sources pulled tonight** (all public, all fetched, none recalled):
Personius & Mahan 2003 BSSA 93(3):1355 doi:10.1785/0120020031 · Personius et al. 2000 USGS
MF-2348 doi:10.3133/mf2348 · Personius et al. 2011 GSA Spec. Vol. 634 ch. · USGS Qfaults ·
Macrostrat geologic-unit API · NASA/ASF OPERA DISP-S1 catalogue · NPS *Tiwa of the Isleta
Pueblo Mission*; NPS *El Cerro de Tomé* · APS *(Re)Contextualizing Elsie Clews Parsons from
a Pueblo Perspective* (deaccession, Dec 2023) · Cambridge/*American Antiquity* Sandia Cave
taphonomy · Preston, *New Yorker*, 1995 · Wikipedia *Los Lunas Decalogue Stone*, *Sandia
Pueblo*, *Sandia Mountains* · NPS/Legends of America Salinas & Quarai.
