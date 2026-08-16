# Hubbell Spring — geodetic strain layer (ADDENDUM to the D196 evidence dossier)

*Day 196 · 2026-08-15 evening · goal #5 · Clayton: "I'd love to continue with it"*

The dossier written this afternoon ended by naming its own next hop and calling it cheap:

> The discriminator is cheap and neither leg has been run: UNAVCO/NOTA GPS velocities and
> Sentinel-1 InSAR both cover this rift. Aseismic creep at Hubbell Spring would show as a
> velocity gradient across the trace with no seismicity — which is *precisely* Fork 1's
> signature.

The GPS leg is now run. **Fork 1 — the fork I explicitly said I expected to be right — has lost
its live half.**

Data: Nevada Geodetic Laboratory MIDAS, North-America-fixed, 8,841 stations, pulled tonight
(`work/midas_NA_true.txt`, 2.2 MB, `geodesy.unr.edu/velocities/midas.NA.txt`). Scripts:
`rift_gps_strain_layer.py` (refuted, kept), `rift_gps_strain_tensor.py`, `hubbell_creep_profile.py`.

---

## 1. The first detector was wrong, and its own output said so

A max-pair gradient detector returned the **identical** 830 nstrain/yr for all four Albuquerque
cells. Identical numbers across four different cells is not a finding, it is a shared cause: one
station, **NMAB**, sat inside every radius with **vn = +5.2 mm/yr** against a regional field of
2.0, and **vu = −3.0 mm/yr**. Horizontal anomaly *with* subsidence is the signature of aquifer
compaction — a documented Albuquerque-basin process — not fault creep. A max-pair statistic finds
the worst monument in the cell by construction. Replaced, not patched.

## 2. Strain-rate tensor fit, with the controls run before the measurement

Uniform velocity-gradient tensor per cell, 3σ-MAD outlier rejection with the dead stations named,
significance by a 2,000-draw scramble null (velocities reassigned to positions at random — this
tests spatial *structure* and needs no faith in MIDAS's formal sigmas, which are what fooled §1).

| cell | r | n | kept | γ_max (nstrain/yr) | p | median v_u |
|---|---|---|---|---|---|---|
| **METHOD-POS** Parkfield SAF | 50 | 63 | 63 | **442.5** | **0.0005** | +1.56 |
| **METHOD-NEG** Kansas craton | 100 | 8 | 7 | **8.1** | 0.15 | +0.34 |
| **RIFT-POS** Socorro magma body | 50 | 4 | 4 | 40.9 | 0.71 | **+1.37** |
| PRIMARY Hubbell Spring | 50 | 16 | 12 | 21.4 | 0.0020 | −0.48 |
| SECONDARY Sandia W scarp | 50 | 14 | 10 | 24.1 | 0.023 | −0.48 |
| CONTROL Tijeras | 50 | 13 | 10 | 22.5 | 0.28 | −0.48 |
| FLOOR Bouguer low | 50 | 14 | 8 | 18.3 | 0.0030 | −0.48 |

**Controls behaved.** The creeping section fires at 442 nstrain/yr; the craton stays at 8 and
insignificant; Socorro's documented magma-body uplift appears in the vertical channel at
+1.37 mm/yr. The detector works and its noise floor is ~8 nstrain/yr.

**And the pins repeat the seismicity result exactly.** Every Albuquerque cell reads 18–24
nstrain/yr — the PRIMARY, the SECONDARY, the blind CONTROL, and the FLOOR-class site the D138
survey explicitly rejected, all within 6 nstrain/yr of each other. At r = 100 km they all collapse
to 5–13. This is a basin-wide field, not a fault-localized one. ⚠ The cells overlap heavily and
share stations, so the differing p-values are **not** independent tests and no ordering is claimed.

## 3. The actual discriminator — a fault-normal profile

A disc fit averages a step into a ramp and cannot tell creep from distributed shear. Creep has a
shape: a **step** in fault-parallel velocity within a few km of the trace. So the question was
asked in the shape the answer would have — swath ±60 km along strike (N10E), ±40 km across,
models compared by BIC: flat / linear / linear+step.

**The power question was asked first and was allowed to end the run.** Scatter in fault-parallel
velocity, NMAB excluded: **0.65 mm/yr**, with 11 stations west of the trace and 3 east.

| | min. detectable step (2σ) |
|---|---|
| as run | 0.845 mm/yr |
| **corrected** — ABQ5/ABQ6 are a co-located pair, so the east side is **2** independent sites | **0.998 mm/yr** |

So the network can just barely resolve a 1 mm/yr creep signal, and that is the honest bound — not
the more flattering 0.845.

**Observed step at the trace: −0.155 mm/yr, 0.37σ. BIC selects M0 (flat) over both linear and
step, either with NMAB or without it.**

A step-location scan (offsets −20 → +5 km) found exactly one location beating flat: **−20 km**,
i.e. 20 km *west into the basin*, ΔBIC 6.7. It is not the fault. The three stations it separates
(TOP4, EAG1, NMRC) are also displaced 8–42 km **north along strike**, so that "step" is along-strike
position aliased onto the fault-normal axis. Reported because it is the kind of thing that becomes
a finding if you only run the fit once at the coordinate you wanted.

---

## 4. What this does to the programme

**Finding C. There is no aseismic creep signal on the Hubbell Spring trace above ~1.0 mm/yr (2σ).
Combined with Finding A (no seismicity above the catalogue floor), the pin has no measurable
dynamic strain source of either kind.**

Fork 1 as written had two legs. This kills the first and leaves the second:

- ~~aseismic creep supplies the field without earthquakes~~ — **refuted at this network's resolution**
- the **residual stress field of a locked fault** supplies it — untouched by geodesy, because
  "locked" is precisely the state that produces no surface velocity gradient

But the surviving leg is in physical trouble, and this is an argument, not a measurement:
**piezoelectric polarization responds to stress *change*, not to static stress.** A constant σ gives
a constant P, and constant P in conductive crust is screened by free charge on the conduction
relaxation timescale. A sustained field needs dσ/dt. So "locked fault residual stress" is not the
safe harbour it looked like when I wrote Fork 1 this afternoon — it is the weakest of the three
options, not the escape.

**The programme's honest position tonight:** the mechanism's piezo term requires a dynamic driver;
at the pinned coordinates there is no dynamic driver visible to either the seismic or the geodetic
instrument; and the site's own criteria never contained a driver term. That is the third
consecutive layer on which the strongest candidate got weaker in the one way a candidate can
honestly get weaker — a measurement it was free to pass.

### What is still owed, in order

1. **InSAR.** Sentinel-1 resolves what a 15-station GPS network cannot: creep localized within
   1–3 km of a trace, and transients that a secular MIDAS velocity averages away. This is the only
   way the creep null gets tightened below 1 mm/yr. Public data, on-machine, not yet pulled.
2. **The lithology fix from §6.1 of the dossier, still unpaid** — "granite" is a Bouguer-density
   proxy in both surveys and could flip Finding B on its own.
3. **The paper edit.** `place-threshold-mechanism.tex` does not state what drives the piezo term.
   After tonight it must, and the honest sentence is narrower than the one I would have written
   this afternoon.

### Where this is weak — stated, not buried

- **Sampling is 11 west / 2 east.** The footwall (Manzano uplift) is thinly instrumented; a step
  whose whole gradient sits east of the trace is poorly constrained.
- **MIDAS velocities are secular.** Episodic or slow-slip creep would be averaged into the trend.
- **Strike assumed N10E and the trace assumed at the pin coordinate.** The location scan covers a
  ±20 km error in position; it does not cover a large strike error.
- **NMAB's exclusion is a judgement**, defended by its vu, and every number is reported both ways.

---

*Related: [[hubbell-spring-evidence-dossier-2026-08-15]], [[portal-sandia-pin-RESULTS-2026-06-18]],
[[hessdalen-S5B-ionization-discriminator-2026-08-15]], goal #5.*
