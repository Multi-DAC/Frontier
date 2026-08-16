# Hubbell Spring / Sandia–Manzano — compiled evidence dossier

*Day 196 · 2026-08-15 · goal #5 · Clayton asked "how much could we compile as evidence"*

**Spelling, for the record:** the fault is **Hubbell Spring** (after the Hubbell family of Pajarito/Isleta),
not *Hubble*. It matters only because the USGS Qfaults query is exact-match.

---

## 0. What this document is

Clayton asked for a compilation. A compilation of a two-day sprint from eight weeks ago is a
re-narration, and re-narration is how a site like this one goes wrong. So this does two things:

1. **Indexes and grades everything that exists** (§1–§3) — 43 files, one published paper, one live goal.
2. **Adds two layers the D138 survey never measured** (§4–§5), because the honest test of a pin is a
   measurement it could fail. It failed one of them.

---

## 1. The corpus that exists (inventory, not summary)

All in `Corpus-Perspectival/Unreleased-Work/` (old repo, mercu tree), Day 137–138, 2026-06-17/18.

**Site survey chain (the geography):**
| file | what it settles |
|---|---|
| `portal-transport-site-search-2026-06-17.md` | why northern NM at all — the US-wide narrowing |
| `portal-yakima-field-survey-2026-06-17.md` | the METHOD, and the first cell to FAIL (no piezo) |
| `portal-sandia-manzano-survey-2026-06-17.md` | cells C1/C2 named; the graded documented-vs-lore activity report |
| `sandia_pin_analysis.py` + `sandia_qfaults.geojson` | the reproducible pin instrument (31 faults, 38,915 vertices, 378 Bouguer pts) |
| `portal-sandia-pin-RESULTS-2026-06-18.md` | **the pins**, land status, secrecy context |

**Mechanism chain (the physics the geography is scoring against):**
`place-threshold-mechanism.tex/.pdf` (the published paper) plus 14 computational result files —
ω_pin extremum-localization, the Q-ball/soliton existence work, the Mathieu cavity, the coherence
threshold, the bulk geodesic, the "one number" and the three-residuals closeout.

**Live continuation in this body:** `palace/south/hessdalen-S5B-ionization-discriminator-2026-08-15.md`
(today), `palace/south/portal-plasma-convergence-2026-06-16.md`, `radion-portal-derivation-2026-06-16.md`.

---

## 2. The evidence, graded

The grade is the point. Nothing here is upgraded by sitting next to something better-graded.

### DOCUMENTED — verifiable against a public record
- **Active rift faulting.** 31 named Quaternary faults in the Albuquerque bbox (USGS Qfaults, pulled).
  Hubbell Spring is **latest Quaternary** — the most recently active structure in the dataset.
- **Density structure.** 378 USGS Bouguer points, −234 to −160 mGal. Basin low and range-core high
  both located. Pulled and processed on-machine; reproducible from the committed script.
- **Granite proximity.** Hubbell Spring 2.3 km, Sandia fault 2.0 km from the dense range core.
  *(By a Bouguer-density proxy, not a geologic map — see §6.1. This is the weakest DOCUMENTED line.)*
- **Manzano Weapons Storage Area** is a real underground nuclear-weapons complex ("Site Able", 1947,
  AFSWP), beside Kirtland and the Coyote Test Field.
- **Bennewitz observed recurring lights over Manzano, 1979–80.** The observations happened.
- **The AFOSI / Richard Doty disinformation campaign against Bennewitz** is documented.
- **Land status.** Hubbell Spring pin falls on **Isleta Pueblo** trust land (Census AIANNH + BLM SMA,
  cross-checked). Sandia and Tijeras pins are private. **None are on Kirtland/DOD land.**
- **Atomic Energy Act "Restricted Data" / born-secret system** — documented law.

### TESTIMONY-GRADE — a person said it; the system it describes is real
- Sarbacher's "two levels higher than the hydrogen bomb"; the Malmgren interview; the claim that
  UAP-adjacent physics sits under the AEA umbrella. The *regime* is documented; **this specific
  application of it is not.**

### INFERENCE, held as such
- That place-threshold physics would fall under the same born-secret umbrella, and that this explains
  its absence from the open literature. This motivates the open-reconstruction method. **It adds zero
  empirical weight to the mechanism.**

### LORE — named so it stops circulating as evidence
- Dulce base; "Sandia underground alien tech"; the *occult motive* for Epstein's (documented)
  petroglyph removal at Zorro Ranch. Documented act ≠ documented motive.

### THE SITE'S OWN WARNING
Bennewitz saw **real lights**, was fed **real disinformation**, built an **alien-base narrative**, and
was institutionalized. Real anomaly → narrative accretion → unmoored. This is not a footnote; it is the
failure mode this dossier is structured to avoid.

---

## 3. What the D138 pin actually claimed

> ★ PRIMARY Hubbell Spring ~34.88–34.95 N, −106.53 W — the only cell scoring on **all** layers
> including the empirical one (documented prior + most-active fault + granite + adjacent basin).

Four scored layers: low density · density **extremum** · quartz-rich granite (piezo) · active fault.
Plus a fifth, unscored: a documented recurring-anomaly record.

---

## 4. NEW LAYER A — modern seismicity. **The pins fail it.**

`work/sandia_seismicity_layer.py`, `work/sandia_seismicity_robust.py` (USGS ComCat, pulled today)

**Why this layer.** The mechanism's piezo term needs **strain release now**. D138 scored faults on a
Quaternary clock — 10⁴–10⁶ years — and never checked whether anything is moving. Independently,
Paiva & Taft's dusty-plasma reading of the Hessdalen spectrum (today's §5(B) note) invokes a *tectonic
stress field* E ≈ 1.5×10⁵ V/m. Seismicity is the shared driver of both my mechanism and the leading
competing explanation of the only instrumented analogue site on Earth.

**Controls first, per standing discipline.** Socorro magma body → must be HOT. Mid-Pacific → must be
EMPTY. Both behaved. The query is sound.

Regional magnitude histogram (120 km, 1980–2026, N=171) **peaks at M2.5** — the catalog is not
complete below that, so only the M≥2.5 rows are admissible.

| site | M≥2.5, r=15 km | M≥2.5, r=25 km | M≥3.0, r=40 km |
|---|---|---|---|
| ★ PRIMARY Hubbell Spring | **1** | **1** | 3 |
| ◆ SECONDARY Sandia scarp | **0** | **0** | 2 |
| ○ CONTROL Tijeras | **0** | **0** | 0 |
| FLOOR Bouguer low | 2 | 2 | 2 |
| **POSCTRL Socorro** | **19** | **30** | **32** |
| NEGCTRL mid-Pacific | 0 | 0 | 0 |

**Binomial test, PRIMARY vs SECONDARY, equal areas: p = 1.000 / 1.000 / 0.812. Not significant at any
cut.** The layer does not rank the pins. It also does not rank them *above the FLOOR-class site the
D138 survey explicitly rejected.*

**Finding A. On the layer most directly coupled to the piezo driver, all three Albuquerque-rift pins
are indistinguishable from zero and from each other — while the site included only to prove the
instrument worked outscored every one of them by 11–30×** (19/1, 30/1, 32/3 at the three cuts).

---

## 5. NEW LAYER B — running the pins' own instrument on Socorro. **Socorro fails the piezo layer.**

`work/socorro_pin_analysis.py` — identical scoring to D138 (Qfaults + Bouguer, same rules), new bbox.

641 Bouguer points, 25 named Quaternary faults, 10,366 late-Quaternary vertices. Conduit layer: **passes
easily.** Density layer: **passes** (−232 mGal regional low).

Piezo layer, granite distance:

| point | granite (km) | vs. Hubbell Spring 2.3 km |
|---|---|---|
| Socorro town | 20.2 | ✗ |
| seismicity centroid | 17.7 | ✗ |
| Zamora arroyo (approx.) | 21.8 | ✗ |
| best convergence in the whole cell | 12.1 | ✗ |

**Finding B. Socorro reproduces the Yakima failure exactly: unscreening and conduit without the
amplifier.** It is FLOOR-class on the D138 criteria.

---

## 6. What the two findings say together — the actual result of the day

> **In the Rio Grande rift, the piezo layer and the modern-strain layer are anti-correlated, and no
> site scores on both.** The quartz-rich Precambrian range-front blocks (Sandia, Manzano) are exactly
> the rigid, locked structures that are *not* releasing strain. The strain is being released 90 km
> south in the Socorro basin, where the crust is hot, the magma body sits — and there is no granite.

The D138 pin was not wrong on its own criteria. It is that **the criteria contained a driver nobody
measured**, and when measured, the driver is not running at the pinned coordinates.

This is falsifiable and it forks cleanly:

- **Fork 1 — the piezo term does not need seismicity.** Aseismic creep, or the residual stress field
  of a locked fault, supplies the electric field without measurable earthquakes. *Then the D138 pin
  stands and Finding A is irrelevant — but the mechanism must say so explicitly, and currently it
  does not.* **This is the fork I expect to be right, and it costs a paper edit, not a re-survey.**
- **Fork 2 — it does.** Then the pin set is scoring a dead driver, and the survey needs a strain layer
  (GPS/InSAR velocity, not earthquake counts) before any coordinate is worth instrumenting.

**The discriminator is cheap and neither leg has been run:** UNAVCO/NOTA GPS velocities and Sentinel-1
InSAR both cover this rift. Aseismic creep at Hubbell Spring would show as a velocity gradient across
the trace with no seismicity — which is *precisely* Fork 1's signature, and it is measurable from
public data on this machine.

### 6.1 Where this is weak — stated, not buried

1. **The granite proxy is density, not lithology.** Both surveys call "granite" = densest Bouguer
   quartile. At Socorro, low-density Tertiary volcanics overlie the Precambrian; the proxy would score
   real granite as absent. **This could flip Finding B on its own.** Fix: a state geologic map or MRDS
   lithology pull. Named as the next hop, not waved past.
2. **Small N.** 1 vs 0 vs 2 events. The *null* is well-supported (the positive control proves
   detection); the *ordering among the nulls* is not, and I have not claimed one.
3. **The Zamora arroyo coordinate is approximate.** Sources place it "in an arroyo south of Socorro";
   no published lat/lon was found. The row is flagged in the script and carries no weight in Finding B.
   **I have deliberately not built anything on the Zamora case** — the temptation to fuse "most
   seismically active cell" with "best-documented physical-trace case in the record" is exactly the
   Bennewitz arc, and the geophysics says Socorro is FLOOR-class anyway.
4. **Catalog completeness is regional, not per-site.** A local network gap at Hubbell Spring
   specifically would mimic the null. Not checked.

---

## 7. Answering Clayton's question directly

**How much can we compile as evidence?** For *the geophysics*: a great deal, and it is real —
reproducible pulls from USGS faults and gravity, a published mechanism, a graded documentary record,
and now two more layers. For *the portal*: **still nothing, and today made that slightly more honest
rather than less.** The strongest candidate got weaker in the one place a candidate can honestly get
weaker — a measurement it was free to pass.

That is what a live programme looks like. The pin survived eight weeks; it did not survive the first
layer that could have killed it, and the correct response is a paper edit and a GPS pull, not a
louder claim.

**On visiting.** Unchanged and it is the part that matters: **the Hubbell Spring pin is Isleta Pueblo
sovereign land.** The path is a request to the Pueblo, not an approach. Public Cibola National Forest
vantages on the Sandia/Manzano front allow observation toward the pins without entering tribal,
private, or DOD land. Nothing here changes that, and nothing here is a reason to hurry.

---

*Related: [[portal-sandia-pin-RESULTS-2026-06-18]], [[portal-yakima-field-survey-2026-06-17]],
[[hessdalen-S5B-ionization-discriminator-2026-08-15]], goal #5.*
