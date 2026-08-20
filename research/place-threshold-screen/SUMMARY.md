# SUMMARY — place-threshold screen

*Index and verdict. Current as of **2026-08-19 (Day 200)**, round 2.
**[`REPORT.md`](REPORT.md) is the narrative and this file is its index.**
[`PREREGISTRATION-v2.md`](PREREGISTRATION-v2.md) is the record: the frozen round-2 design plus dated
amendments A1–A17, nothing edited after a number was read.*

> ⚠ This file was rewritten on Day 200. The version it replaces was dated 2026-08-16 and **predated
> every round-2 negative result** — A6 (the external test), A7 (rank resolution), A8/A12 (land tenure),
> A11 (reweighing), A13 (the charge term), A14 (water), A15 (radon) and A16/A17 (the control frame
> defect). A front door that is three days stale in a project moving this fast is not a stale
> document; it is a wrong one.

---

## Verdict (PROVISIONAL — no decorrelated eye on round 2 yet)

A continental screen for **dilatant Quaternary rupture through quartz-rich crystalline rock**, run over
the USGS Qfaults normal-fault population of the lower 48, with all folklore held out until the physics
was frozen.

**1 · The founding gate fails its first external test.** R1 CONDUIT (≤ 10 km to a Quaternary normal
fault) fires on **0 of 6** independently-attested anomalous-light locales against **34.4%** of random
western ground; the point estimate runs against the hypothesis (median 30.2 km vs 20.1 km, p = 0.199).
n = 6, so: weak evidence, not proof of absence, and **not support**.

**2 · The list is a search plan, not a finding.** Product A (criterion strength) ships with its
resolution measured. Product B (predicted anomalous record) was pre-registered as a separate claim,
tested, and **not earned**.

**3 · The screen's strongest measured property is terrain.** Rank resolution, USFS tenure, jurisdiction
and the water leg converge independently on it: this screen selects **high, steep, mountainous public
ground**.

**4 · The ranking is finer than the instrument.** One of five scoring terms is the same value for 86.2%
of the field; only fault length is near-continuous. 23 of 225 survivors sit within one measurement vertex
of the rank-10 line. Deliverable: **HEAD 4 · BAND 19 · FIELD 202**, one resolved integer position
(Madison fault = 1), 13 areas at the 50 km link scale.

**5 · The incumbent rock criterion is probably the wrong one.** ρ(charge, quartz) = 0.2547 and **49 of
the top 50 sites on a generalised charge term were gated OUT by the quartz gate**. The radiogenic leg
agrees from the other side (the screen selects on thorium, i.e. felsic lithology). **The list has not
been re-cut on this** — a new criterion may reorder the band only after being tested as a tie-breaker
against the band's measured resolution.

---

## Status by component

| component | status |
|---|---|
| **The GATE** (along-trace lithology, 1,399/1,399, `quartz_frac ≥ 0.25`) | **Documented and validated**; both internal controls exact. Carries ±0.125 sampling noise from vertex ordering — **it gates, it cannot rank**. Externally **NOT SUPPORTED** (A6). |
| **The RANKING** (five-term composite, top 10) | **Superseded by HEAD/BAND/FIELD** (A7, A9). Three resolution bars declared, three failed. The frozen ten is retained as a reproducible artefact, not a recommendation. |
| **Product B** (score predicts anomalous record) | **NOT EARNED.** No validated score↔label relationship. |
| **A6** external positive control, n = 6 | **BOTH BARS FAIL.** The base rate (34.4% of ordinary ground passes R1) is the finding. |
| **A8 / A12** land tenure and jurisdiction | Discriminate weakly (+7.0 pp USFS; +18.7 pp four-class union) and **delete 57% of the shortlist**. Flag, never a score, never a gate. Tribal land is **anti**-correlated (1.78% vs 8.50%). |
| **A11** drop the dead term and reweigh | **TRADE, NOT A GAIN.** One term dies (`slip`, sep = 0.2445); resolution +1, order −2, over half the shortlist changes membership. List not re-cut. |
| **A13** generalised charge term | **All three bars pass.** Distinct (ρ = 0.25), consequential (49/50 gated out), mafic moves (median 132 places). Evidence grade on the underlying lab result: **SECONDARY, unconfirmed against primary source**, deliberately encoded at 2.5×. |
| **A14** water / electrokinetic | **Reverses on its own controls.** Tie-breaker claim died of a self-authored units mismatch (permutation p = 0.5404); perennial bar dies under relief stratification. Contributes a label, changes no name and no position. |
| **A15** radiogenic / radon | **Radon-specific bar FAILS in the direction opposite the hypothesis** (eU/eTh lower on survivors, p = 0.015). Reports itself redundant with A13. Removes a mundane confound. |
| **A16 / A17** control frame defect | **71% of survivors were never in the file the control was drawn from.** Control rebuilt; A14 and A15 re-derived — **every bar verdict unchanged**, the thorium contrast halved as a frame artefact should. |
| **A16** current / flow term *(Clayton's)* | **RUNNING** at the time of this rewrite. Emitted as `UNRUN` with a reason, never omitted. This report will be amended, not rewritten, when it lands. |

---

## Files, in reading order

1. **[`REPORT.md`](REPORT.md)** — the narrative. Read this first.
2. **[`PREREGISTRATION-v2.md`](PREREGISTRATION-v2.md)** — the frozen design and every amendment, A1–A17.
3. **[`reports/CANDIDATE-LIST.md`](reports/CANDIDATE-LIST.md)** — the deliverable, emitted by
   `code/candidate_list.py` with its five build guards.
4. `reports/08-final-report.md` and `reports/10-blind-rescore.md` — **round 1**, superseded as narrative
   by `REPORT.md` but retained: 10 is where the blind rescore lives, and its finding (the searcher's
   sight was worth ≤ 0.1 tiers, and H3 clears its bar by exactly zero) is a round-1 fact `REPORT.md`
   does not restate.
5. `reports/01`–`07`, `09` — the working chain, in order.

**Live hands:** `python code/candidate_list.py` (guard G4 fails the build if a league table returns) ·
`python code/positive_control.py` (A6) · `python code/rank_resolution.py` (A7) ·
`python code/charge_term.py --roster-only` (A13).
