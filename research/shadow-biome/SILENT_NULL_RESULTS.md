# SILENT NULL — RESULTS

**Run D207 / 2026-08-26, ~11:5x–12:2x local.** Scored against `PREREG-SILENT-NULL.md`, committed
`a8e10fb` **before the probe was written**. Instrument: `silent_null_probe.py` (v2). Raw:
`SILENT_NULL_RESULTS.json`. The defective first pass is kept at
`SILENT_NULL_RESULTS_V1_DEFECTIVE.json` — see §5, it is the most useful thing in this run.

---

## 1. HEADLINE — MY CLAIM IS REFUTED AT ITS OWN THRESHOLD

**P1 predicted ≥ 3 of 12 (25%), point estimate 4/12 (33%). Measured: 1 of 12 = 8.3%. REFUTED.**

**P2 — the prosaic null, which I tested rather than assumed — HELD at 80%** (predicted ≥75%).

Per the pre-registration's own words, written before the data: *"If P2 holds and P1 fails → the null
wins cleanly. The archives paginate, they say so, and the 'invisible aperture' reading of the device
branch has no support in this frame. **That result gets written into the paper in those words.**"*

That is what happened. It is written here in those words.

⛔ **The forbidden move is not taken.** This null stays in this branch. It is not reframed as
"consistent with archives whose edits are undetectable by construction."

### The full frame, n = 12

| # | archive | A2 (semantics) | A1 (pagination) | naive said | true total | ratio |
|---|---|---|---|---|---|---|
| F1 | arXiv | `A2-NONE` | `A1-DECLARED` | 185,365 | 185,365 | 1.00 |
| F2 | Crossref | `A2-NONE` | `A1-DECLARED` | 1,069,570 | 1,069,570 | 1.00 |
| F3 | OpenAlex | `A2-NONE` | `A1-DECLARED` | 9,692,815 | 9,692,815 | 1.00 |
| F4 | GBIF | `A2-NONE` | `A1-DECLARED` | 64,203,640 | 64,203,640 | 1.00 |
| F5 | Zenodo | `A2-NONE` | `A1-DECLARED` | 42,125 | 42,125 | 1.00 |
| F6 | PubMed | `A2-NONE` | `A1-DECLARED` | 1,085,475 | 1,085,475 | 1.00 |
| F7 | openFDA | `A2-NONE` | `A1-DECLARED` | 617,935 | 617,935 | 1.00 |
| **F8** | **JPL SSD close-approach** | **`A2-SILENT`** | `A1-NONE` | **30** | **516,088** | **17,203×** |
| F9 | SIMBAD TAP | `A2-INDETERMINATE` | **`A1-SILENT`** | *no total* | 6,501,946 | 130× |
| F10 | NASA Exoplanet Archive TAP | `A2-INDETERMINATE` | `A1-NONE` | *no total* | 40,106 | 1.00 |
| F11 | DataCite | `A2-NONE` | `A1-DECLARED` | 8,325,745 | 8,325,745 | 1.00 |
| F12 | USGS Water Services | `A2-DECLARED` | `A1-SILENT` | *no total* | 33,833 | 33,833× |

**Seed (excluded from the headline by pre-commitment, because it generated the hypothesis):**

| S1 | USGS FDSN earthquake | `A2-SILENT` | `A1-NONE` | **13** | **14,514** | **1,116×** |

**Protocol sibling:** P1, EarthScope/IRIS FDSN event — `A2-UNREACHABLE`. **HTTP 410 Gone**, an HTML
error page. See §4; it is a finding in its own right.

---

## 2. EVERY PREDICTION, SCORED

| | prediction | measured | verdict |
|---|---|---|---|
| **P1** | ≥3/12 `A2-SILENT` (pt. 33%) | **1/12 = 8.3%** | ⛔ **REFUTED** |
| **P2** | ≥75% of truncating endpoints `A1-DECLARED` (pt. 85%) | **8/10 = 80%** | ✅ **HELD** |
| **P3** | kill if 0/12 | 1/12 | **does not fire** — see §3 |
| **P4** | ≥1 endpoint HTTP 200 with no usable answer | **0/12** | ⛔ **REFUTED** |
| **P5** | ≥8/12 of my own A2 predictions correct | **8/12 = 66.7%** | ✅ **HELD, at the boundary** |
| **P6** | headline must not depend on the sibling | 1/12 vs 1/13; sibling unreachable | ✅ **satisfied** |

**P1 — the strongest form the claim can take on this data.** Both `A2-INDETERMINATE` rows would have
to resolve to `A2-SILENT` to reach 3/12, which is *exactly* the threshold — so under the resolution
maximally favourable to me, P1 only just scrapes in. It cannot be rescued.

**P4 refuted, and this is the one I most expected to hold**, because the essay's whole motivating
anecdote is a 200-with-no-answer. Not one frame endpoint did it. Every failure in this run was
**loud**: 410, 503, 400 with a message naming the offending parameter. The archives in this frame
fail honestly.

**P5 held on the count and is worthless as stated.** Stratified:

- predictions of `A2-NONE` (the boring default): **7 of 7 correct**
- predictions of anything else: **1 of 5 correct** (only F8)

My 67% is carried entirely by the stratum where guessing "nothing interesting" wins. On the five rows
the run existed to decide, I was **20%**. `feedback_sample_drawn_from_one_stratum`, applied to my own
scorecard. The honest downgrade: **a recalled API default from this body is worth about one in five
when it predicts something interesting**, and every such recall in the corpus inherits that.

⚠ 8/12 = 66.7%, and I glossed the threshold "≥ 8 correct (67%)". The binding clause is the count, so
it holds — but a percentage and a count disagreed at the boundary and the count is what I wrote
first. `feedback_float_decides_a_verdict_at_the_boundary`.

---

## 3. WHAT SURVIVES — existence, not rate

P3 does not fire, and the distinction is exact: **the phenomenon exists and is severe where it
occurs; the rate I predicted is refuted.**

**F8 — JPL SSD close-approach, 17,203×.** The naive response is four keys: `signature`, `count`,
`fields`, `data`. It reports `count: 30` and that is the whole answer a caller receives. The true
eligible total is 516,088. Zero occurrences of `date-min`, `date-max`, `dist-max` or `default`
anywhere in the body.

**And the necessary qualification, which is most of the point:** the defaults *are* documented.
`ssd-api.jpl.nasa.gov/doc/cad.html` states `date-min` default `"now"` and `date-max` default `"+60"`.
So the correct claim is not *undocumented* — it is **undeclared in-band**: the record you receive
does not carry the fact that it is a narrowed record. A reader with the docs open is fine. A script,
a pipeline, or a person who queried and got a number is not. Any sentence that slides from "the
response doesn't say" to "nobody says" is overclaiming, and I am pre-committing against writing it.

**S1 — USGS FDSN, 1,116×.** Excluded from the headline as promised, and worth stating anyway because
it is worse than F8 in one specific way: its `metadata.url` field **echoes the URL as submitted** —
which contains no time parameters. The response actively confirms that you asked for everything,
while answering for one month. `count: 13`. True: 14,514.

**F12 — USGS Water Services, the counter-example, and it is instructive.** Same agency as S1, same
class of default (a time window), and it **declares it**: `{"value": "[mode=LATEST, modifiedSince=null]",
"title": "filter:timeRange"}`, in the `queryInfo` envelope. One agency, two services, opposite
behaviour. This refutes my F12 prediction and it refutes any story about institutions.

### The sharpest result in the run, and it was not predicted at all

**F9 — SIMBAD TAP: the honesty is *serialization*-dependent.** Identical server, identical ADQL,
identical truncation at 50,000 of 6,501,946 rows (0.77% returned):

| `format=` | bytes | overflow marker |
|---|---|---|
| `votable` | 1,527,157 | **`<INFO name="QUERY_STATUS" value="OVERFLOW"/>`** |
| `json` | 1,177,318 | **none** |
| `csv` | 1,077,139 | **none** |

The truncation is the same in all three. Only your ability to *know about it* changes, and it
disappears in exactly the two formats a scripting user reaches for. Note also that in VOTable the
marker is the **final element of the document** — after 1.5 MB of base64 — so a streaming parser that
stops at the last `</TR>`, or a human who reads the head, misses it too.

⚠ Recalled, not verified here: that the IVOA TAP standard *requires* an overflow indication. The
contrast above is measured; the claim about the spec is not, and is left open.

### A structural split, generated by this data and therefore not tested by it

Every clean row is a **bibliographic or biodiversity** archive (arXiv, Crossref, OpenAlex, Zenodo,
PubMed, DataCite, GBIF, openFDA): 8 of 8 `A2-NONE`, 8 of 8 `A1-DECLARED`. Every narrowing row is a
**physical-observation archive with a time axis** (USGS FDSN, JPL close-approach, USGS water):
2 silent, 1 declared.

Candidate mechanism: a catalogue of *events* has a natural "now" and therefore a natural default
window; a catalogue of *records* does not, so it never grows one. That is a hypothesis this run
**generated and did not test** — the frame was not built to separate those strata and n is 3 on one
side. It is written here as the next pre-registration, not as a finding.

---

## 4. FOUND BY ACCIDENT — the sibling is dead

`service.iris.edu/fdsnws/event/1/query` returns **HTTP 410 Gone** with an HTML page reading
*"NGF: Service Unavailable"*. The FDSN event endpoint of a major seismological data centre does not
answer.

This is closer to the mechanism Max named — *the record did not survive to be queried* — than
anything the probe was designed to catch, and the probe found it only by trying to use it. It is the
sibling row, so it enters no rate. Whether the service moved rather than died is **not established
here**; 410 is a claim by the server about itself and I did not chase it.

---

## 5. THE INSTRUMENT WAS THE BEST SUBJECT IN THE RUN

Nine defects, `D1`–`D9`, all in `silent_null_probe.py`, all found by reading raw response bodies
rather than the summary table. **Five of the nine are the failure this probe exists to measure,
committed by the probe.** The v1 output is preserved unedited.

| | defect | what it produced |
|---|---|---|
| **D1** | non-2xx accepted as an answer | IRIS's HTTP 410 **HTML error page** was parsed as **172 records** and scored `A2-NONE`. **A dead endpoint manufactured a clean null** — the exact sentence Max wrote |
| **D2** | a failed BOUNDED leg scored as agreement | openFDA 617,935 → 0 read as *"within the 5% band"*. A collapse to zero reported as concordance |
| **D3** | false declaration | token list contained `signature`, a generic envelope key in every JPL response. A 17,203× narrowing scored **`A2-DECLARED`** |
| **D6** | declaration tested before narrowing | 5 endpoints that narrowed **nothing** scored `A2-DECLARED` because a token matched. The test was run where both answers look identical |
| **D7** | token scan read the data rows | `eventdate` matches on every GBIF record. A field name read as a declaration |
| **D8** | A1 judged against the un-narrowed total | conflated the two axes the probe exists to separate |
| D4 | illegal BOUNDED (Zenodo size>25) | predicted in advance by prereg §4.3 |
| D5 | bare-array TAP unparseable | — |
| D9 | a transient 5xx decided a verdict | USGS water: 200 at 11:5x, **503** at 12:0x, 200 at 12:1x. On the 503 it scored `A2-UNREACHABLE` and its `A2-DECLARED` evidence vanished from the run |

**D3, D6, D7 and D8 are one defect wearing four faces:** a guard that returns *"declared — nothing to
see"* from a check that could not have distinguished the two cases. D6 is the purest — the
declaration branch ran *before* asking whether any narrowing had occurred, so an honest archive and a
narrowing one produced the same verdict.

Every one of those four biased the result **toward the safe reading**, and three of them would have
shipped as "the archives are fine." Had I read only the summary table, this document would have
reported **1 silent, 5 declared, archives largely honest** with the same headline number and a
completely false table under it.

**The direction matters and is stated against my interest:** repairing D3 moved F8 from `A2-DECLARED`
to `A2-SILENT` — *toward* my hypothesis. That is why §3 quotes the four top-level keys verbatim and
why the JPL documentation was fetched rather than recalled.

---

## 6. LIMITS — the ones from §4 of the prereg, plus what the run added

1. **n = 12.** 1/12 has a 95% interval of roughly 0.2%–38%. This run establishes existence and refutes
   a rate; it does not measure one.
2. **The frame is a convenience sample of key-free APIs**, and the bias runs toward my hypothesis.
   It came out against me anyway, which is worth something but not much.
3. **`A2-NONE` is a weaker verdict than `A2-SILENT`** — a BOUNDED query I got wrong scores safe. The
   exact BOUNDED parameters are in the JSON for every row so this is auditable.
4. **The temporal half is untouched.** Max's mechanism is *the record did not survive*. This run
   measures the nearer cousin: *the record is there and the query does not reach it*. Do not cite this
   as covering retention over time. The 410 in §4 is the only thing in this run that even points at it.
5. **`A2-INDETERMINATE` is a real limit, not a rounding.** Two of twelve endpoints return no total in
   any serialization I asked for, so a caller cannot tell narrowing from row-capping from inside the
   response at all. That is the structural point the run makes best — and it is *why* those two rows
   cannot be counted in the headline in either direction.

---

## 7. WHAT THIS DISCHARGES, AND WHAT IT DOES NOT

**Goal #18 item (c) is discharged.** A pre-registered number existed before the data
(`PREREG-SILENT-NULL.md` @ `a8e10fb`); a measurement ran against the frame it fixed; every row is
recorded including the unreachable ones; and P1–P6 each carry an explicit verdict scored against the
number written first. **The headline prediction was refuted by its own instrument**, which is the only
outcome that proves the apparatus was load-bearing.

**Not discharged:** items (a) — the retention survey across the remaining archives — and the temporal
half of Max's mechanism, which no measurement here touches.

**Next pre-registration, named now so it cannot be tuned later:** the event-vs-record split in §3, on
a frame stratified in advance, with ≥8 endpoints per stratum and the prediction written before the
list is fixed.
