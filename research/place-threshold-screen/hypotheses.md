# Hypotheses — place-threshold screen

Each hypothesis declares its **kill condition up front**. A hypothesis stays class *Hypothesized*
until a dated line in `../../MEASUREMENTS.md` moves it. Nothing here gets promoted quietly.

Proposers so far: **Clawd** (all), **Clayton** (H-1's framing, and the constraint that produced
H-0). The third seat stands empty on this topic.

---

## H-0 — the screen may only measure its own instruments *(method hypothesis)*

**Claim.** A national site screen returns whatever its filters select for, and the earlier version
of this one demonstrated exactly that: requiring slip rate ≥1 mm/yr and resolvable modern geodetic
strain returned the Brawley Seismic Zone and the San Andreas, because both requirements select
plate boundaries by construction.

**Status: VALIDATED, 2026-08-15.** Removing the two instrument requirements changed the answer
from the plate boundary to intraplate crystalline-cored rift and hotspot-flank faults. The screen
that produced the top ten therefore carries only criteria that make claims about physics.

**Residual.** Removing a filter cannot remove a weighting. H-0 stands satisfied for the *gates*
and unsatisfied for the *weights* — see the ±50% perturbation in the README, where seven of ten
slots move.

---

## H-1 — the piezoelectric-conduit hypothesis *(the load-bearing one)*

**Claim.** Anomalous light and low-frequency sound reports cluster preferentially at sites where a
**dilatant Quaternary fault** ruptures through **quartz-rich crystalline rock with tectonic
fabric**, because the two conditions supply a permeability pathway and a coherent piezoelectric
source volume in the same crustal column.

**Kill condition (declared before the base rate runs).** Draw 30 dilatant Quaternary faults at
random from the same physiographic provinces as the ranked ten. Look each up blind for an
anomalous light/sound record. **Should the blind-drawn base rate match the top-ten hit rate within
its own sampling error, H-1 dies as a *predictor*** — it would then describe the mountain West
rather than any particular place in it.

**Second, sharper kill.** Fabric outranking pluton (P3: 2.0 vs 1.4) makes a directional
prediction. Should gneiss/quartzite/mylonite sites carry *no* excess anomalous record over
equigranular granite sites at matched rupture age, the specific piezoelectric mechanism loses its
best discriminator, whatever survives of the correlation.

**Standing: Hypothesized. Untested.** The lore pass in report 07 returned four grade-A or A/B hits
among five printed sites and one clear miss (Centennial) — a result with **no denominator**, and
therefore not evidence for H-1 yet.

---

## H-2 — the lore convergence reflects sampling, not physics *(the null, and the one to beat)*

**Claim.** Native sacred-site documentation and light folklore saturate the mountain West densely
enough that any list of ten scenic, fault-bounded ranges would return grade-A material at a
comparable rate. The convergence would then measure the density of the *record*, and partly the
density of *settler invention*, rather than anything the rock does.

**Kill condition.** The same blind base-rate draw as H-1, read in the opposite direction: a
top-ten hit rate exceeding the blind rate beyond sampling error kills H-2.

**Standing: Hypothesized, and currently favoured on grounds of parsimony.** Grading the lore A/B/C
by source rather than accepting it whole (report 07 §5) limits the damage but does not remove it.

---

## H-3 — the province, not the site, carries the signal

**Claim.** The correct unit of analysis names a *province* (Yellowstone parabola, Rio Grande rift,
Walker Lane, Lewis & Clark line), not an individual fault. Three of the top five sit inside one
~150 km triangle, so the fault-level ranking triple-counted a single tectonic fact.

**Kill condition.** Re-run the screen with province as the deduplication unit. Should the
province-level ordering track the fault-level ordering, H-3 adds nothing and dies.

**Standing: Hypothesized, partially supported.** The province regrouping already exists in report
07 §3 and it changed the answer — it moved the Rio Grande rift to second nationally, which the
fault-level table concealed.

---

## H-4 — the starting site ranks first in the continental US

**Claim as originally stated.** The Sandia / Hubbell Spring junction near Albuquerque supplies the
best convergence of the required geophysical conditions in the continental United States.

**Status: DISCONFIRMED as stated, 2026-08-15.** Measured on its own trace lithology against 507
thinned CONUS nodes, the junction scores 6.65 and lands **~9th**. It loses on exactly one term —
rupture recency — and on nothing about rock or structure.

**What survives, and gets kept as a separate, weaker claim.** The junction belongs to the right
*class* of terrain, and that class dominates the top of the national list; on a province basis the
Rio Grande rift places second in the country. A re-promotion of H-4 as stated requires a dated
line in the ledger showing what changed.

---

## Open instruments that will move these

1. `code/trace_lithology_national.py` — 445 unmeasured faults, controls declared in advance
   (Sandia positive, Hubbell Spring negative). Governs **recall**.
2. The blind lore base rate — 30 random draws, same provinces. Governs **H-1 vs H-2**, and until
   it lands neither hypothesis moves.
3. Aeromagnetic depth-to-basement — the correct P3 for a *buried* source. Re-ranks every
   basin-fill site.
