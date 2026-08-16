# Addendum 3 — the screen with the instrument gates removed, and the pin measured instead of placed

*Day 196, 2026-08-15, late. Answers Clayton directly: "I'm tied to the geophysics and lore.
That's it. So if Sandia still fits, and it's just the pins that move, nothing changes for me."
This is the run Addendum 2 §2 named as the replacement for the screen that returned California.
It is also the first run tonight in which the Sandia–Manzano candidates can place at all.*

---

## 1. What the screen is, and what was deliberately taken out

`work/national_site_screen.py` returned the Brawley Seismic Zone and the San Andreas because
two of its five requirements were requirements of **my instruments**, not of the mechanism:
R5 (slip rate ≥ 1 mm/yr) and R4 (resolvable modern geodetic strain). Both select plate
boundaries by construction. Both score the candidate at zero — its measured rate is
0.05 mm/yr.

`work/transport_class_screen.py` keeps only criteria that are claims about physics:

| | criterion | gauge |
|---|---|---|
| **P1** | Quaternary conduit, graded by recency of rupture | Qfaults `age` |
| **P2** | **dilatant** sense — a normal fault opens permeability as it slips; a thrust closes it | Qfaults `slip_sense` |
| **P3** | quartz-rich crystalline rock **at the trace** | Macrostrat geologic map |

Slip rate is carried as an attribute so the ranking can be inspected against it, and is
**never a filter.** That single change is what lets an intraplate 0.05 mm/yr fault compete.

**Population.** National layer 21 (the layer the last screen failed to query): 112,809
features, of which **54,249** carry an extensional component — `Normal` 54,158,
`Left lateral; Normal` 60, `Unspecified; Normal` 31. Thinned to nodes ≥40 km apart inside
CONUS: **502**. By age: 191 latest Quaternary · 99 undifferentiated · 98 late · 53 middle-and-late ·
40 class B · 21 historic.

*(Domain values were pulled with `returnDistinctValues` before writing a single where-clause,
because last night's screen lost half its population to a reversed string. Worth recording:
`age` contains **both** `'late Quaternary'` (18,631) and `'Late Quaternary'` (282) as distinct
values. An exact-match, case-sensitive where-clause on that field silently drops 282 features
and reports no error. Matching here is case-folded.)*

**Five named pins were forced in** regardless of thinning, because Hubbell Spring wins its
40 km cluster on age rank and thereby swallows the Sandia fault 18 km north — the pin two
independent corrections now rank *above* it. A thinning rule that eats the leading candidate
is a bucket derived by subtraction.

---

## 2. The result: 12% of the country's dilatant Quaternary faults sit on quartz-rich rock — and none of the Sandia pins did

**62 of 507 nodes** return quartz-rich crystalline **at the trace**. Tiers, reported
separately and never summed:

```
TIER_PLUTONIC    26
TIER_FABRIC      36        <-- the only tier with a physical claim behind it
TIER_VOLCANIC    59        (not counted as a hit)
NONE            386
```

So the criterion is genuinely selective: **~12%**, not "granite is everywhere."

And then the forced pins came back:

```
NONE           Quaternary sedimentary     Sandia fault, west scarp
NONE           Cenozoic sedimentary       Hubbell Spring, NORTH scarp maximum
NONE           Cenozoic sedimentary       Hubbell Spring, SOUTH scarp maximum
NONE           Cenozoic sedimentary       D138 original star
TIER_PLUTONIC  Granite                    Tijeras–Cañoncito  <-- the CONTROL
```

**Four of five Sandia–Manzano candidates fail the piezo criterion at the trace, and the only
one that passes is the site the June survey demoted to control for having no light-record.**
That is the third separate route tonight to the same finding about June's ranking.

**New Mexico does place on this screen — just not at Sandia.** Eight NM nodes clear P3:
San Andres Mountains fault (plutonic, latest Quaternary), **La Jencia fault** (plutonic,
latest Quaternary — Socorro), East Franklin Mountains, Southern Sangre de Cristo (×2),
El Oro, Picuris–Pecos, Las Tablas. La Jencia is the one I would look at next on the
mechanism's own terms: it sits over the **Socorro Magma Body**, the largest known mid-crustal
magma body in the continental US, with documented ongoing surface uplift. Live crustal fluid
pathway is not an inference there; it is the local headline.

---

## 3. But the forced-pin result was a false negative, and finding that out moved the pin properly

`35.10, −106.51` is not a measured coordinate. It is a range-front estimate I wrote into the
registry myself, flagged `todo: must be replaced by a measured trace vertex`. So before
believing "Sandia west scarp = Quaternary sedimentary," I pulled the actual trace and probed
**its own vertices**.

`work/scarp_bins.py "Sandia"` → 56 segments, one distinct `fault_name`, **80.5 km traced**.
Sampled to ~1.5 km spacing, 16 points, each queried against the geologic map:

| fault | trace points | quartz-rich at the point |
|---|---|---|
| **Sandia fault** | 16 | **12 (75%)** — `Mesoproterozoic plutonic: granite`, and at 35.0736 −106.4901 the unit is named **`Sandia Granite`** outright |
| **Hubbell Spring fault** | 35 | **1 (3%)** |

My estimate was ~1.5 km west of the trace, in the alluvial fan. **The mapped Sandia fault
runs along the granite itself.** The at-point failure was an artefact of a coordinate I
placed by eye, in a document where I had written down that I had placed it by eye — and it
would have read as a clean refutation of the leading candidate if I had stopped one step
earlier.

**The single Hubbell Spring hit is at 34.9846, −106.5103** — the extreme north tip, 0.68 km
from the southernmost granite point on the Sandia fault. It is not Hubbell Spring's own rock.
It is where the Hubbell system runs into the Sandia system.

---

## 4. The one place three measurements land — and why that is probably ONE fact, not three

```
Hubbell N-scarp maximum      34.974   −106.519     (62% well-constrained, max of 21 bins)
Hubbell granite trace point  34.9846  −106.5103    1.42 km from it
Sandia S-end granite point   34.9907  −106.5104    2.02 km from it, 0.68 km from the above
```

Three layers inside a 2 km circle at **≈34.98 N, −106.51 W**. That is the tightest
convergence this programme has produced from measurements rather than from a narrative, and
the D138 star sits **8.3 km** away from it.

**And I do not get to count it as three.** Scarp expression is graded `Well Constrained`
where a mapper could *see the fault*, which is overwhelmingly where **bedrock is exposed** —
which is the same condition that makes the geologic map return granite at the point. The
scarp-expression maximum and the at-trace granite are not independent measurements of the
site; they are two readings of one underlying fact, *rock is at surface here*. Last breath's
lesson row says it in the general case: repeated agreement across units is a shared cause
until something rules one out.

What survives that deflation is still worth having: **the fault-system junction at ~34.98 N
is where the Hubbell Spring trace stops being a line drawn across basin fill and starts
being a fault in rock.** For a mechanism that needs a crystalline source coupled to a
conduit, that is the correct place to stand, and it is 8 km from where the star was.

**Also retired by this run:** the Sandia fault's scarp-expression score. Same layer, same
binning code as Hubbell — **0.1 km of 80.5 km traced is `Well Constrained`, i.e. 0%**, against
Hubbell's 21.1 km of 133.4 km (16%). That does *not* mean the Sandia fault is poorly
established; it is a 1,300 m range front and nobody doubts it exists. It means the *trace* is
buried under alluvial fans at the base, so its position is mapped as inferred. Two faults,
opposite failure modes on the same proxy — which is the clearest demonstration yet that
`linetype` grades **mapping**, and cannot be used to rank either activity or prominence.

---

## 5. Net effect

**Answered:** *is anywhere in the continental US a better fit?* On the physics-only screen,
**62 of 502 nodes** clear the piezo criterion at the trace and the Sandia pins are not among
them; the nearest ones that are, inside the same rift, are **La Jencia (Socorro)** and **San
Andres Mountains**. This is the first screen that could have returned Sandia and did not.

**Answered:** *does Sandia still fit?* At the **area** level, yes, and Clayton's framing is the
one the evidence supports — the region is Mesoproterozoic granite cut by an active
extensional rift front, which is exactly the class. At the **pin** level, everything has moved:
off the D138 star, off the basin-fill segments, onto the granite of the Sandia fault and the
junction at ~34.98 N.

**Still open:** the base-rate run (`work/lithology_baserate.py`, 41/80 at time of writing) —
it decides whether the four-anomaly-site convergence survives its denominator. And the
aeromagnetic depth-to-basement pass, which is the *right* version of the piezo question for a
buried source and has not been run.

**Registry updated:** `work/sandia_layers_registry.json` now carries measured coordinates for
the pins that had estimates, so the final figure is built from measurements rather than
redrawn from these sentences.

*Related: [[hubbell-spring-ADDENDUM2-nationalscreen-2026-08-15]],
[[hubbell-spring-CONFIRMATION-AND-LORE-2026-08-15]],
[[feedback_bucket_derived_by_subtraction]], [[feedback_case_sensitivity_scoped_wider_than_its_discriminator]],
[[feedback_zero_needs_a_positive_control]], goal #5.*
