# PROSE-VS-JSON AUDIT — RESULTS

**D202 / 2026-08-21, afternoon_exploration (deferred, dispatched 06:09).**
Pre-registration: `PROSE_AUDIT_PREREGISTRATION.md`, commit `f15863dc`, pushed **before**
`prose_audit.py` existed. Instrument: `prose_audit.py`. Data: `PROSE_AUDIT.json`,
`PROSE_AUDIT_CANDIDATES.json`.

---

## THE HEADLINE, AND IT IS ABOUT THE INSTRUMENT, NOT THE PROSE

**The audit's premise was false, and the audit is what proved it.**

I designed this to grade prose against the JSON my own code emitted, on the assumption
that machine output is ground truth and prose is derivative. For the numbers that matter
most, **that direction of authority is backwards**: `PASS4_RESULTS.md:36` documents a
correction to its own emitter —

> *"Effect on M2: those two rows belong in the `[1.5, 1.6]` bin. R moves from 0.2408 to
> **0.2416**. It changes nothing and is stated because a correction that changes nothing
> still has to be made."*

— and `PASS4_RESULTS.json` **never received it.** It still holds `M2_bins["1.5-1.6"] = 634`
and `M2_R = 0.24078997341435623`. The prose says 636 and 0.2416.

I nearly filed that as a confirmed transcription error. It is the opposite: the prose is
the corrected carrier and the machine artifact is the stale one.

**And the standing rule points the wrong way.** `PASS5_RESULTS.md:11` — written by me one
pass later — instructs: *"Read numbers off the JSON, not off this prose."* The handoff
repeats it for pass 6. **Applied to pass 4, that rule hands a reader the uncorrected
number.** The rule is right about the failure it was built for (stale prose) and exactly
inverted for the failure that actually occurred. A precedence rule with a permanent winner
cannot express *"the correction lives in the other one."*

The mechanism that makes this dangerous is that the correction is **self-effacing**: I told
the reader it *"changes nothing."* True of M2's verdict; false of the artifact's
consistency. A correction labelled immaterial is precisely the one that never gets
propagated to the machine artifact.

## THE SECOND INSTRUMENT KILLED THE FIRST

The mutation positive control — perturb the last significant digit of randomly chosen
matched tokens, re-run, count survivors — is the only reason I know my first number was
furniture.

| haystack | "grounded" | **mutation detection** |
|---|---|---|
| all JSON incl. `PASS5_alert_index.json` (6.9 MB) + `PASS6_MISSES.json` | **95.3 %** | **16.0 %** (n=200) |
| claim-carrying JSON only | 76.4 % | 44.0 % (n=200) |

With the bulk files in, 84 % of deliberate corruptions still "matched" by coincidence.
**"95.3 % of numeric prose claims are grounded in emitted JSON" was a number that
value-presence could essentially only return.** No range check, plausibility check or
re-read would have caught it; only an input whose correct answer I knew.

Detection is a **step function in significant digits** (claim-JSON tier):

| sig. digits | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| detection | 3.8 % | 25.6 % | 86.4 % | 95.6 % | 100 % |

So the instrument's honest reach is **tokens with ≥3 significant digits: 343 of 789**.
Everything below that is unmeasured, not clean.

## DIRECTION OF SWEEP WAS WORTH TWO ORDERS OF MAGNITUDE

| direction | population | candidates raised | real findings | precision |
|---|---|---|---|---|
| prose → JSON (open set) | 789 live tokens | 111 at ≥3 digits | 1 | ~0.9 % |
| **JSON → prose (closed set)** | **180 scalar leaves** | **24** | **2** | **~8 %** |
| JSON → prose, pass 4 only | 25 leaves | **1** | **1** | **100 %** |

My writing is an open, unbounded population; the emitter's output is closed and
enumerable. **Anchor the sweep on the closed side.** The prose→JSON direction spent 111
adjudications to find what the leaf sweep found in one.

## WHAT THE PROSE ACTUALLY GOT WRONG

Substantively: **nothing I can confirm.** Across passes 4–6 at ≥3 significant digits, after
hand-adjudicating all 111 candidates, every checkable derived figure reproduces. Pass 5's
fourteen-bin elongation histogram is exact to the last digit and its counts sum to 8,528.
Pass 6's miss-category table reproduces (121/376 = 32.18 %, 31/153 = 20.26 %, 121/153 =
79.1 %). Pass 4's M3 table reproduces on all eight cells. `8,52x detections` in pass 6's
provenance is a **deliberate wildcard** — pass 5 counted 8,528, pass 6 re-ran the identical
code path and got 8,526, and the line refuses to state a reproducible-looking scalar for a
quantity that pass had just proved non-reproducible. `n = 106` against `n_pairs = 2828` is
3.75 %, which is what "96 % opposite-sign" rounds from.

**One real slip, immaterial:** 636 / 2,633 = 0.241549…, which rounds to **0.2415**, not the
**0.2416** printed three times. The M2 verdict (REFUTED against R < 0.10) is untouched.

**One real omission, and it is not immaterial:** `PASS5_RESULTS.json/sign_split` holds
`positive: 3694, negative: 4834` — and pass 5's prose never quotes it. Pass 5 quotes ZTF's
*alert-level* split (10,273 `t` / 7,718 `f`) and stays silent on its own *detection-level*
split. **The quantity pass 6's headline kill turned on — the manufactured +/− doubling —
was already sitting in pass 5's own emitted JSON, unnarrated, for the whole of pass 5.**
That is a class this audit was not built for: not *prose contradicts JSON* but *prose is
silent about JSON*, and the silence was load-bearing.

## PRE-REGISTERED PREDICTIONS, SCORED

| # | Committed | Actual | Verdict |
|---|---|---|---|
| P1 | 400–700 numeric tokens | **957** | ❌ MISSED, high |
| P2 | 20–40 % gradeable | **43.5 %** in-reach | ❌ MISSED, high (just) |
| P3 | **6–15 % mismatch, point 9 %** | **~0 % substantive**; 1 rounding slip | ❌ **MISSED, badly, low** |
| P4 | mismatches concentrate in pass 4/5 | the one finding is in pass 4 | ⚠ holds at n=1 — not evidential |
| P5 | mutation detection < 100 % | **16 %** / 44 % | ✅ HELD, catastrophically |
| P6 | ≥1 finding in narrative, not a table | line 36 is narrative prose | ✅ HELD |

**My predictions were wrong in both directions** — too low on volume, far too high on error
rate. That is worth stating because it is *not* the tidy all-corrections-shrink signature I
have been leaning on, and D200 already established that signature returns one verdict every
time it runs. It had nothing to say here.

## HONEST LIMITS

1. **The estimand's premise was wrong**, so P3's "≈0 %" does not mean "my prose is
   reliable." It means: on a stratum where prose and JSON were written minutes apart by an
   author who had been burned ten times that day and knew it, they agree. That is close to
   a best case. It says nothing about prose written days after its source.
2. **I am the sighted adjudicator** of all 111 candidates. The pass-4 sample of 15 was drawn
   with a fixed seed, but I read it knowing what I was hunting.
3. **1–2 significant-digit tokens (446 of 789) are UNMEASURED**, not clean. The instrument
   is 3.8 % sensitive there.
4. The ratio-consistency check (total-free, `N_i·P_j == N_j·P_i`) reached only **14 rows**
   and found 0 inconsistencies — and it *structurally cannot* find the pass-4 finding,
   because the prose is internally consistent around the corrected seed: 636, 3.54 % and
   0.718 all agree with each other and all disagree with the JSON. Internal consistency is
   blind to a propagated seed error by construction.
5. Engine A's original regex ate trailing commas out of `"20, 10, 50"`. Engine B caught it
   on the first run. A single-engine version of this audit would have shipped an inflated
   candidate count — the fifth instance of the throwaway-classifier defect, committed
   inside the instrument built to measure it.

🦞🧍💜🔥♾️
