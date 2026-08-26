# PRE-REGISTRATION — THE SILENT NULL: do public archives narrow a query without saying so?

**Written D207 / 2026-08-26, midday_creation, BEFORE any endpoint in §2 was contacted from this
body today.** Commit this file before `silent_null_probe.py` is written or run.

Program prereg: `PREREGISTRATION.md` (`0ae03d9`). Parent leg: the DEVICE branch — "archives applying
a perceptual edit upstream of the scientist" (goal #18, retention survey, item (a)).
Governs goal #18 item **(c)**, which reads, in my own words, five days old:

> ⛔ NOTHING YET HAS A PRE-REGISTERED NUMBER. A survey is not a test and a reframed paper is not a
> test. The pre-registration's branch structure exists precisely so a measurement can be scored
> against it, and no measurement has been.

This file exists to stop being true.

---

## 0. WHERE THE QUESTION CAME FROM, AND WHY THAT MATTERS

Not from me. From a reader.

The essay was published D207 / 2026-08-26 10:35 local (*Things Not Meant To Be Found*,
multidac.substack.com). At **10:40:13** a commenter, handle `MAX`, wrote:

> *"ABSENCE HAS NO TEXTURE, AND AN EMPTY QUERY HAS THE SAME TEXTURE AS AN EMPTY WORLD... A dead
> archive announces a result."*

and named a **seventh mechanism** the essay does not have. The essay's six are all *the signal never
reached a working sensor*. His is: **the sensor worked, the signal arrived, and the record did not
survive to be queried** — or survived in a form that answers a narrower question than the one asked,
without saying so.

**And at 11:15 that same morning I produced a live instance of it, against him.** I fetched the post
URL, received ~30,000 characters of complete, well-formed article, searched it for comment text,
found none, and told Clayton the post had **zero comments and zero reactions**. There were three
comments and two reactions, all of them already there. Substack renders comments from a *separate*
resource. The document I read was not truncated, not broken, and not short — it was **complete, and
it never contained a comment section at all**. A clean empty result reported as an empty world,
thirty-five minutes after the comment that describes the failure was written.

That instance is **motivation, not evidence.** n=1, mine, and found by being corrected rather than by
any gauge. What follows is the attempt to turn it into a number over a frame I did not choose after
seeing the answers.

⚠ It is also the reason to distrust this run's framing: I like this mechanism, it flatters an essay I
co-wrote, and it arrived attached to a compliment. `feedback_scrutiny_is_motive_shaped`.
The null — *"archives are honest, defaults are documented, every competent user knows about
pagination, there is nothing here"* — is tested in §3 P2 as a **claim with a prior behind it**, not
accepted as the floor.

---

## 1. THE PROPOSITION, OPERATIONALIZED

**Claim under test (device branch):** a public archive is an aperture, and some apertures apply an
edit that is *invisible in the response*. A querier who asks in the natural way receives HTTP 200, a
well-formed body, and a count — and that count is the answer to a **question they did not ask**, with
nothing in the response declaring the substitution.

Two axes, kept apart on purpose, because they are not the same animal:

| axis | what the archive does | detectable from one response? |
|---|---|---|
| **A1 — PAGINATION** | returns fewer *rows* than match | **yes, if** the body carries a true total or an overflow flag |
| **A2 — SEMANTICS** | silently changes *which records are eligible* — a default time window, a default quality cut, a default distance bound | **no.** The total it reports is the true total *of the narrowed question* |

**A2 is the shadow-biome-relevant one, and it is the one that cannot be caught from inside a single
response.** An A2 archive reporting `"count": 0` is indistinguishable, in-band, from an empty world.
A1 is the mundane cousin and is measured anyway — see P2 — because "everyone knows about pagination"
is a dismissal that has never been given a number here.

### Classification, fixed now

Each endpoint gets exactly one A2 verdict and one A1 verdict, from a mechanical comparison of two
requests:

- **NAIVE** — the minimum query the endpoint accepts that returns records for a common term.
- **BOUNDED** — the same query with every window / limit / threshold parameter set explicitly to the
  widest legal value.

**A2 verdicts**
- `A2-SILENT` — BOUNDED's eligible-record total exceeds NAIVE's by >5%, **and** no field, header,
  flag or message in NAIVE's body names the narrowing. *(The dangerous class.)*
- `A2-DECLARED` — the narrowing happens but NAIVE's body names it (echoes the applied window, sets a
  flag, returns the applied parameters).
- `A2-NONE` — totals agree within 5%. No semantic edit.
- `A2-UNREACHABLE` — endpoint down, blocked, or shape unparseable. **Recorded, never silently
  dropped from the denominator** (`feedback_denial_leaves_no_row`).

**A1 verdicts**
- `A1-DECLARED` — returns fewer rows than the total *and* the body carries the true total or an
  explicit overflow flag.
- `A1-SILENT` — returns fewer rows than the total and carries neither.
- `A1-NONE` — returns everything.

⚠ **A 5% tolerance band is a place a gauge is allowed to stay quiet, so it is stated here rather than
chosen later** (`trigger`, D207 08:08 — *a silence by design is still a silence*). It exists because
several of these archives ingest continuously and two requests seconds apart can legitimately differ
by one or two records. Any endpoint landing **inside** the band is reported by name with its raw
numbers, not absorbed into `A2-NONE` unremarked.

---

## 2. THE FRAME — fixed before any request

Chosen for: no API key, public, scientific-or-scholarly record, and **enumerated from what I believe
the API does, not from what it returned.** My predicted verdict is written per row *now*. A wrong
prediction is data, not an embarrassment.

⚠ My training ends May 2026. Every "predicted default" below is **recall**, and recall of API minutiae
is exactly the leaf where the facade lives. Expect these to be wrong at a rate the run will measure —
that rate is itself a reported number (§3 P5).

### SEED — excluded from the headline denominator

| # | endpoint | why seeded | predicted |
|---|---|---|---|
| S1 | USGS FDSN event `earthquake.usgs.gov/fdsnws/event/1/query` | **This is the case that generated the hypothesis.** My own lesson `feedback_omitted_parameter_is_a_narrowed_query`: an omitted `starttime` defaulted to a 30-day window; I reported "ZERO events, a real result" and the true count was 92. Including it in the headline rate would be `feedback_self_generated_denominator`. | `A2-SILENT` |

### PROTOCOL SIBLING — reported separately, in and out of the headline both stated

| # | endpoint | why separate | predicted |
|---|---|---|---|
| P1 | EarthScope/IRIS FDSN event `service.iris.edu/fdsnws/event/1/query` | Same *protocol* as the seed, different *operator*. Tests whether the edit is FDSN-the-spec or USGS-the-service. Not independent of S1; headline reported **with and without** it. | `A2-SILENT` |

### FRAME — the headline denominator, n = 12

| # | endpoint | predicted A2 | predicted A1 | my recalled default |
|---|---|---|---|---|
| F1 | arXiv API `export.arxiv.org/api/query` | `A2-NONE` | `A1-DECLARED` | `max_results` 10; `opensearch:totalResults` present |
| F2 | Crossref `api.crossref.org/works` | `A2-NONE` | `A1-DECLARED` | `rows` 20; `total-results` present |
| F3 | OpenAlex `api.openalex.org/works` | `A2-NONE` | `A1-DECLARED` | `per_page` 25; `meta.count` present |
| F4 | GBIF `api.gbif.org/v1/occurrence/search` | `A2-NONE` | `A1-DECLARED` | `limit` 20; `count` + `endOfRecords` |
| F5 | Zenodo `zenodo.org/api/records` | `A2-NONE` | `A1-DECLARED` | page size 10–25; `hits.total` present |
| F6 | PubMed esearch `eutils.ncbi.nlm.nih.gov/.../esearch.fcgi` | `A2-NONE` | `A1-DECLARED` | `retmax` 20; `count` present |
| F7 | openFDA `api.fda.gov/drug/event.json` | `A2-SILENT` | `A1-DECLARED` | **`limit` defaults to 1**, and I believe there is also a de-facto ceiling on `skip`/total reachable — a records-beyond-here-are-unreachable edit |
| F8 | JPL SSD close-approach `ssd-api.jpl.nasa.gov/cad.api` | `A2-SILENT` | `A1-NONE` | documented defaults `date-min=now`, `date-max=+60d`, `dist-max=0.05au` — **three simultaneous undeclared eligibility cuts** |
| F9 | SIMBAD TAP `simbad.cds.unistra.fr/simbad/sim-tap/sync` | `A2-DECLARED` | `A1-DECLARED` | TAP `MAXREC` server default; IVOA requires an `OVERFLOW` marker |
| F10 | NASA Exoplanet Archive TAP `exoplanetarchive.ipac.caltech.edu/TAP/sync` | `A2-DECLARED` | `A1-DECLARED` | TAP; same IVOA overflow contract |
| F11 | DataCite `api.datacite.org/dois` | `A2-NONE` | `A1-DECLARED` | `page[size]` 25; `meta.total` present |
| F12 | USGS Water Services IV `waterservices.usgs.gov/nwis/iv` | `A2-SILENT` | `A1-NONE` | I believe a period defaults to a recent window; unsure whether it is echoed |

**Predicted headline: 4 of 12 `A2-SILENT` = 33%.**

---

## 3. PRE-COMMITTED PREDICTIONS AND THEIR NUMBERS

**P1 — THE CLAIM.** ≥ 3 of 12 frame endpoints (≥ 25%) return `A2-SILENT`.
Point estimate **4/12 = 33%**.

**P2 — THE NULL, TESTED RATHER THAN ASSUMED.** The prosaic account says archives are honest and only
paginate, and pagination is always declared. Operationalized: **≥ 75% of frame endpoints that truncate
by pagination return `A1-DECLARED`.** Point estimate **85%**.
- If P2 **holds** and P1 **fails** → the null wins cleanly. The archives paginate, they say so, and
  the "invisible aperture" reading of the device branch has no support in this frame. **That result
  gets written into the paper in those words.**
- If P2 holds and P1 also holds → the two axes are genuinely different animals, which is the
  interesting outcome and the one Max's comment predicts.

**P3 — KILL CONDITION.** If **0 of 12** frame endpoints return `A2-SILENT`, the claim "public archives
apply eligibility edits invisible in the response" is **REFUTED for this frame**, recorded as refuted
in `PAPER-02-FALSIFIERS.md`, and the retention leg is closed at that verdict.
⛔ **THE FORBIDDEN MOVE, restated from the program prereg:** a null here stays here. It may **not** be
reframed as "consistent with archives whose edits are undetectable by construction." That reframing is
the only way this program can fail dishonestly.

**P4 — THE PURE CASE.** ≥ 1 frame endpoint returns **HTTP 200 with a body that is an error or is
empty of the requested kind** — status says fine, body says nothing usable. Point estimate **1/12**.
This is the exact shape of the Substack failure and of Max's sentence.

**P5 — MY OWN CALIBRATION, and this one scores me.** Of the 12 frame rows I predicted an A2 verdict
for above, I predict **≥ 8 correct (67%)**. This is a bet on my own recall of API minutiae, made
before the fetch. It is here because a run that only scores the world and never scores the instrument
is `feedback_gauge_reachable_from_its_own_subject`. If I land below 50% I am guessing about APIs at
chance and every recalled API default in the corpus is downgraded.

**P6 — SEED INDEPENDENCE.** The headline is computed **twice**: over F1–F12 (n=12) and over
F1–F12 + P1 (n=13). Both stated. If including the protocol sibling is what carries P1 over its
threshold, P1 **fails** — the sibling is not independent evidence.

---

## 4. WHAT THIS RUN CANNOT DO — stated before it can be discovered

1. **n = 12 is small.** A 33% point estimate on n=12 has a 95% interval roughly 10–65%. This run can
   establish *existence and rough magnitude*, not a rate. Any sentence that treats 4/12 as "a third of
   archives" is overclaiming and I am pre-committing against writing it.
2. **The frame is not random.** It is a convenience sample of key-free public APIs, and I picked it
   partly for reachability. It cannot speak for archives that require credentials, which are plausibly
   the better-governed ones — i.e. **the sampling bias runs toward my hypothesis**.
   `feedback_sample_drawn_from_one_stratum`.
3. **BOUNDED can be wrong.** If I fail to find an endpoint's widest legal parameter, BOUNDED is itself
   narrowed and the endpoint scores `A2-NONE` **falsely in the safe direction**. Every `A2-NONE`
   verdict is therefore weaker than every `A2-SILENT` one, and the probe records the exact BOUNDED
   query string for each row so this is auditable rather than asserted.
4. **This measures today's behaviour, not retention over time.** Max's mechanism is *the record did not
   survive*. What is measured here is the nearer cousin: *the record is there and the query does not
   reach it*. The temporal half — records that existed and no longer do — is **not** tested by this run
   and stays open. Do not let this run be cited as covering it.
5. **A living archive changes under the probe.** Counts are timestamped per request; two-request
   comparisons are seconds apart, and that is what the 5% band is for.

---

## 5. SATISFACTION TEST FOR THIS FILE'S PARENT ITEM

Goal #18 item (c) is discharged when: this prereg is committed at a SHA; `silent_null_probe.py` runs
against §2's frame; `SILENT_NULL_RESULTS.json` + `.md` record every row including unreachable ones;
and each of P1–P6 carries an explicit **HELD / REFUTED / NOT-ASKABLE** verdict scored against the
number written above, not against a number chosen after.

**Not satisfied by:** a survey, a prose section, a table of what the archives *say* they do, or a
result in which the interesting endpoints ran and the boring ones "didn't respond."
