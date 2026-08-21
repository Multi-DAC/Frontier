# THE REJECTION BIN — paper architecture

**Opened D202 / 2026-08-21, ~12:0x PT, on Clayton's word: *"Then we can start the shadow biome paper."***
**Premise author:** Clayton Iggulden-Schnell (D201, 18:52/18:55/18:58/19:02 PT). **Drafting:** Clawd.
**Governed by** `PREREGISTRATION.md` (`0fa1a62` lineage), whose Branch-A/Branch-B fork and forbidden
crossing bind this document exactly as they bind the passes.

---

## 0. THE ONE RULE THIS FILE EXISTS TO ENFORCE

**A paper is where a program's hedges go to die.** Six passes produced numbers with qualifiers
attached — `minarea`-dependent, one-night, non-deterministic-library, JSON-stale-against-prose — and
prose is the medium in which a qualifier silently falls off. So every claim below carries its
**artifact** and its **grade** before a sentence of the paper is drafted, and the grade is written
**now**, while the disappointment is fresh, rather than at composition time when the argument wants
to be strong.

⛔ **`frac_far` MAY NOT APPEAR AS A SCALAR ANYWHERE IN THIS PAPER.** Pass 6 measured a 10.63-point
span across `minarea` 2–12 — a parameter *I* chose and ZTF never imposed. It is a curve. Anywhere it
is printed as one number, that is a defect, and this line is the citation for saying so.

---

## 1. THE THESIS AS CURRENTLY SUPPORTED — and it is not the exciting one

**Not:** *there is a shadow biome.*
**Not:** *the archives contain a discarded population.*

**The thesis the evidence actually carries:**

> A class defined by **relation to the observer** rather than by shared mechanism is a legitimate
> scientific kind with a track record, and if such a class exists its evidence is already captured
> — sitting in the **rejection bins** of sensor networks built to look at something else. That makes
> the premise testable without new instruments. We state the test, pre-register the fork that would
> otherwise make it unfalsifiable, and run it at one locus. **At that locus the bin is mostly what
> the classifier said it was.** The apparatus survives the null; the null is the point.

**Why this is worth writing rather than filing.** The historical case that runs the other way is not
speculative and not ours: NEXRAD's "clutter" bin was full of birds, bats and insects for decades,
somebody took it seriously, and it became radar aeroecology and the BirdCast forecasts. **The bin was
kept, the bin was full, and what was in it was ordinary life nobody was looking at.** That is the
paper's existence proof, and our ZTF null is the paper's honesty.

---

## 2. SECTION MAP — HAVE / OWED, with the artifact named

| § | Section | State | Rests on |
|---|---|---|---|
| **1** | The premise, and the one repair it needs | ✅ **HAVE** | `PREREGISTRATION.md §1, §1a` — not-selected-*for* replaces selected-*against*; three mechanisms, all producing Clayton's observable |
| **2** | Observer-relative kinds are legitimate | ✅ **HAVE** | cryptic species · dark taxa · Candidate Phyla Radiation (visible ~2013 because a device finally looked) |
| **3** | The fork, and why it is written before the data | ✅ **HAVE** | `PREREGISTRATION.md §2`. **This is the transferable contribution** — two live branches let a null in one be reassigned to the other, each half stays falsifiable, the pair becomes unfalsifiable, and it happens *after* the data comes back and *feels like reasoning* |
| **4** | IMAGING vs PERTURBATION | ✅ **HAVE** | `PREREGISTRATION.md §3`. A perturbation cannot be promoted to an object claim by accumulation, only by independent imaging. Costs nothing; the anomalous-phenomena literature almost never does it |
| **5** | Who keeps the bin — the retention survey | ✅ **HAVE**, ⚠ mixed grades | `RETENTION_SURVEY.md`, 31 KB, tiered by *where the classifier sits relative to the archive*. Labels are per-row ✅/⚠/❓ and must be carried into the paper, not flattened |
| **6** | NEXRAD / radar aeroecology as the existence proof | ◐ **PARTIAL** | Survey Tier 0. **OWED: primary sources.** Currently the strongest claim in the paper resting on the thinnest citation — it is the one a hostile reader checks first |
| **7** | The ZTF test, pre-registered | ✅ **HAVE** | `PASS4/5/6_PREDICTIONS.md` + `*_DIAGNOSTIC_PREDICTIONS.md`, every one committed and pushed **before** the code that scored it ran |
| **8** | Result: the far side of `elong <= 1.6` | ✅ **HAVE** | ⚠ **Artifact is `PASS6_VERIFY.json` `/V2/far` and `PASS6_DIAG.json` `/D2a` — NOT `PASS6_RESULTS.json`, which does not contain these numbers.** Re-read off the JSON D202: `opp_share_of_side` 0.6581 · `null` 0.47207 · `opp_rate` 0.96252, so the excess is **+49.04 pp** by subtraction. Difference-image dipoles, counted twice by pass 5's `+data`/`-data` union. **On this evidence ZTF's cut is doing its job** |
| **9** | What the instrument did to the result | ✅ **HAVE** — and it is a section, not a footnote | `minarea` span **0.10632** (`PASS6_DIAG.json` `/D2b/span`) and **U-shaped, direction predicted wrong** · `sep` 1.4.1 non-deterministic on these images, voiding the gauge used to certify my own refactor · `PASS4_RESULTS.json` stale against a correction its own prose documents (634/0.2408 vs 636/0.2416), so the standing "read the JSON not the prose" rule hands a reader the uncorrected number — `CORRECTIONS.json` is the carrier that never existed |
| **9a** | ★ **The non-determinism is measurable inside our own two carriers** — found D202 while checking §8 | ✅ **HAVE**, new | At the *same* `minarea=5`, `PASS6_RESULTS.json` `/frac_far` = **0.4849906** and `PASS6_DIAG.json` `/D2b/ladder/5/frac_far` = **0.4845179**. One parameter, two runs, **0.047 pp apart.** So it is not merely that `frac_far` is a curve over `minarea` — **a single point on that curve is not a fixed number either.** Any digit past the second decimal in this program is run-dependent, and the paper must round to where the runs agree |
| **10** | Scoring: 8 of 16 held | ✅ **HAVE** | The paper prints the refutations at the same size as the confirmations, including P2 refuted in the *opposite* direction (far side anti-collinear, 62.8° vs 45° uniform) |
| **11** | The residual — the only live number left | ⛔ **OWED — PASS 7** | (a) single-sign extraction, `+data` only, no union, `frac_far` **pre-registered before looking**; (b) pair-collapse and re-measure the residual elongation distribution; (c) the unexplained 27% of alerts still unrecovered at `minarea=2` — `minarea` explains most of the 41% miss and demonstrably not all (D2b-1 refuted at 73.14%, needed 80%) |
| **12** | Archive reachability as a finding in its own right | ⛔ **OWED** | 15 of 55 exposures referenced by one night's alerts are 404 at IRSA, stranding 5.76% of alerts. **n=55, one night.** Re-measure on ≥2 nights before it may be quoted as an archive property |
| **13** | What this does and does not bear on | ✅ **HAVE**, load-bearing | Branch A only. **The null stays in Branch A.** Any sentence in the finished paper that explains this null by appeal to Branch B violates `PREREGISTRATION.md §2` and is to be cut |

---

## 3. WHAT WOULD MAKE THIS A DIFFERENT PAPER

Stated now so that later enthusiasm has to argue with a dated sentence rather than with a mood.

**Pass 7(a) is the whole ballgame.** If single-sign extraction leaves a far side that is still large
after the manufactured doubling is removed, §8 stops being a null and §11 becomes the paper. If it
collapses — which is the way the evidence currently points — the paper is what §1 says it is, and
that is a paper worth publishing because **the pre-registration is what makes the null mean
anything.** An unregistered null is indistinguishable from not having looked.

⚠ **The temptation to look before predicting is maximal at 7(a), because I already know which way it
goes.** That is precisely the condition the pre-registration discipline exists for and the condition
under which it is hardest to keep. `PASS7_PREDICTIONS.md` gets committed and pushed before
`measure_pass7.py` exists, same as the six before it.

---

## 4. ORDER OF WORK

1. **`PASS7_PREDICTIONS.md`** — pre-registered, committed, pushed. Nothing else starts first.
2. Pass 7 (a) → (b) → (c). Compute, not conversation.
3. §6 primary sources — the NEXRAD/aeroecology citations, because it is the paper's existence proof
   and currently its weakest citation.
4. §12 second night, so reachability is a measurement rather than an anecdote.
5. Draft §1–§5 and §13 **now**, in parallel with the compute — they are already fully supported and
   they do not move on pass 7's result. Drafting them early also means the frame is fixed *before*
   the last number lands, which is the only order in which a result cannot quietly choose its own
   framing.
6. ⛔ **NOT** replication across years. Cost is measured (2019: 8.85 GB · 2022: 14.9 GB · 2026: 9.89
   GB by HTTP HEAD) and replicating a number that is two-thirds artefact buys nothing.

---

## 5. AUTHORSHIP

**Premise: Clayton.** Not "inspired by" — stated, twice extended, and the operative definition
(*"It doesn't have to fit in one category, except not easily identified or perceived by humans"*) is
his sentence and is the definition the whole program tests. **Program design, pre-registration,
instruments, measurement and drafting: Clawd.** Both go on it, in that order of origin, and the
premise is quoted verbatim with its timestamps in §1 rather than paraphrased into the passive voice.
