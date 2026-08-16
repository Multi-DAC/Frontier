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

**Standing: NOT SUPPORTED, 2026-08-16.** Three pre-registered legs ran against 10 ranked
winners and 10 decoys matched on observer density, every rubric and query string committed to
git before any lookup. All three landed short of the declared +1.0 bar:

| leg | subject | separation | sign test | verdict |
|---|---|---|---|---|
| H1 | anomalous light / sound record | +0.7 | 6/7, p=0.125 | NOT SUPPORTED |
| H2 | Native sacred / anomaly lore | +0.3 | 4/7, p=1.0 | NOT SUPPORTED |
| H3 | settler-history record | +0.9 | 6/8, p=0.289 | NOT SUPPORTED |

**The base rate the kill condition asked for was answered by a substituted design, and the
substitution is not a straight upgrade.** Instead of 30 unlabelled random draws, we used 10
decoys drawn from the same physiographic provinces and matched on census places within 50 km.
That is **stronger on matching** and **weaker on two axes the original named**: n=10 rather than
30, and — decisively — the original said *look each up **blind***, and this scorer was not.
The `ANY`-level base rate came back **20/20 for both winners and decoys**, exactly as
pre-declared, which is what "the record saturates the mountain West" looks like.

**The second, sharper kill (fabric over pluton) remains untested.** No leg separated
gneiss/quartzite/mylonite sites from equigranular granite at matched rupture age.

**What this is and is not.** Three underpowered legs failing to clear a pre-declared bar is a
**failure to detect, not a refutation.** But the corrections all run one way: distance-to-town
matching cuts H1 from +0.7 to +0.4; the three legs correlate at rho 0.32-0.48 and so are closer
to one weak fact than three; the pooled test reaches p = 0.0525 and is optimistic because its
nominal n=22 rests on 10 independent site pairs. And the scorer was **not blind** — see
`reports/08-final-report.md` §7.1, the largest uncontrolled term in the whole lore program and
absent from all three design documents.

---

## H-2 — the lore convergence reflects sampling, not physics *(the null, and the one to beat)*

**Claim.** Native sacred-site documentation and light folklore saturate the mountain West densely
enough that any list of ten scenic, fault-bounded ranges would return grade-A material at a
comparable rate. The convergence would then measure the density of the *record*, and partly the
density of *settler invention*, rather than anything the rock does.

**Kill condition.** The same blind base-rate draw as H-1, read in the opposite direction: a
top-ten hit rate exceeding the blind rate beyond sampling error kills H-2.

**Standing: NOT KILLED, and now more strongly favoured, 2026-08-16.** Its kill condition — a
top-ten hit rate exceeding the blind rate beyond sampling error — did not fire in any of the
three legs. The `ANY`-level base rate came back **20/20 on both sides**, which is the saturation
this hypothesis predicts. Grading the lore A/B/C by source rather than accepting it whole
(report 07 §5) limits the damage but does not remove it.

H-2 cannot be promoted to *confirmed* either: it is favoured because the alternative failed to
detect, which is a weaker footing than a positive result of its own would be.

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

1. ~~`code/trace_lithology_national.py`~~ — **CLOSED 2026-08-16.** 1,399/1,399 measured, zero
   errors, both controls exact (0.875 / 0.000). Recall is no longer the limiting factor.
2. ~~The blind lore base rate~~ — **CLOSED 2026-08-16**, answered by matched decoys across three
   legs. See H-1 above.
3. **A BLIND lore protocol** — labels stripped, 20 sites shuffled into one list, scored cold,
   unblinded at readout. This is now the load-bearing open instrument: pre-registration froze
   the questions and left the reader sighted.
4. **Distance-to-nearest-place as a design-time matching axis.** Winners sat at a median 7.5 km
   from a census place, decoys 19.3 km, and all three rubrics band on distance.
5. **A labelled set of 20-30 sites**, or the written admission that this screen is a filter with
   no ranking capacity — the four scoring legs separate the two controls by 0.19 in the *wrong*
   direction, so the latter is currently better supported.
6. Aeromagnetic depth-to-basement — the correct P3 for a *buried* source. Re-ranks every
   basin-fill site.
