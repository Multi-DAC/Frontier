# ARCHIVE REACHABILITY — NIGHT 2, AND THE RETRACTION IT FORCES

**Run D203 / 2026-08-22 ~11:2x PT. Governed by `PREREG-REACHABILITY.md`, committed `312a883` before
`data/ztf_public_20180602.tar.gz` was opened.**

---

## 1. THE RESULT, UP FRONT

| | night 1 · 2018-06-01 | night 2 · 2018-06-02 |
|---|---|---|
| alerts | 17,991 | 19,446 |
| distinct difference images | 1,687 | 993 |
| exposures | 55 | **32** |
| exposures missing at IRSA | **15 (27.27 %)** | **0 (0.00 %)** |
| exposures UNKNOWN | 0 | 0 |
| alerts stranded | 1,037 (**5.76 %**) | **0 (0.00 %)** |

**R1 — REFUTED.** Pre-committed: *night 2's exposure-miss fraction is > 0*. It is zero.
**R2 — REFUTED.** Pre-committed band [0.10, 0.55]. 0.00 is outside it.
**R3 — UNINTERPRETABLE.** It compares stranding against exposure loss; with both terms zero the
comparison tests nothing. ⛔ Recorded as uninterpretable, **not** as a third refutation — the same
ruling pass 7 applied to B2's dependents and pass 8's G2.

**Scored: 0 of 2 interpretable predictions held.** This is the first block in the programme where
every scorable prediction failed, and it is the block whose direction the pre-registration said out
loud it did not know.

---

## 2. WHAT IS RETRACTED

⛔ **`PAPER-00-ARCHITECTURE.md` row 12's number may not be quoted as a property of the archive.**
Row 12's own condition — *re-measure on ≥ 2 nights before it may be quoted as an archive property* —
has now been met, and it was met by the outcome that revokes the quotation. **5.76 % is a fact about
2018-06-01 and about nothing else.** It stays in the paper as a measured property of one night, with
the second night printed beside it, or it leaves.

That is what a pre-committed failure condition is for. The clause was written on D202 when the number
was flattering and there was no reason to expect it to fire.

---

## 3. THE RESCUE WAS TESTED AND IT ALSO FAILED

The obvious repair is that missing exposures are **thin** ones — marginal field-nights with few
detections — and that night 2 simply has none. Night 1's numbers invite it:

| | missing (n=15) | present (n=40) |
|---|---|---|
| alerts per exposure, median | 47 | 348 |
| alerts per exposure, max | 153 | 1,915 |
| images referenced, median | 12 | 38 |

Within night 1 the correlation is strong and real. **It does not transfer.** Night 2's thinnest
exposure carries **11 alerts and 1 referenced image — and it is present.** Thirteen of night 1's
fifteen missing exposures are *richer* than that. So thinness cannot be the mechanism: night 2
contains exposures as marginal as night 1's and holds all of them.

⛔ The rescue is refuted on the same data that suggested it. Recorded because an untested rescue that
sounds right is worth less than nothing — it would have let 5.76 % survive as "the archive loses thin
exposures", a sentence with no measurement under it.

---

## 4. ⭐ WHAT THE LOSS ACTUALLY IS — AND THIS IS THE FINDING

Night 1's misses are **contiguous in time and indifferent to sky position.**

Ordered by fractional day, the missing exposures fall in runs:

```
316076 316539 316991 317477 317975   <- five consecutive exposures, all missing
337917 338368 338843                 <- three consecutive
395058 395509                        <- two consecutive, and 299468/299931 likewise
```

with 315556 present immediately before the five-run and 318438 present immediately after it. Random
per-exposure loss does not produce runs of five with intact neighbours.

**And field 000577 is PRESENT at fracday 168113 and MISSING at fracday 240301 — the same patch of sky,
the same night, two outcomes.** Whatever removed these products is keyed to **when the exposure was
processed**, not to **where it pointed**.

The honest reading, and it is dull, which is the correct register for it: **on 2018-06-01 there were
processing intervals whose products never reached the archive of record, while the public alert
stream kept pointing at them.** The next night has no such interval. Reachability is **episodic**,
not a rate — and an episodic loss cannot be quoted as a percentage without the night attached.

---

## 5. WHAT §12 MAY SAY

- ✅ A public alert stream can and does reference exposures that the archive of record does not hold.
  **Demonstrated, twice measured, one night positive and one night zero.**
- ✅ On the night where it happens, the loss is **bursty and time-keyed**, with the same sky present
  and absent hours apart. That is a statement about a pipeline, and it is the strongest thing here.
- ⛔ **Not a rate.** No percentage may be quoted as an archive property. n=2 nights, and they
  disagree completely.
- ⛔ **Not a deletion of content.** A stranded alert is one whose difference image is unreachable; no
  missing file was opened, because a missing file cannot be opened. `PREREG-REACHABILITY.md` §3's
  forbidden move binds, and this result makes it easier to keep rather than harder.
- ⭐ **The reason this belongs in the paper at all is now a methodological one, not an evidential
  one:** a programme that plans to re-derive results from a public archive should measure
  reachability **per epoch**, because one night says 27 % and the next says zero.

---

## 6. THE PROBE, AND WHY THIS FILE TRUSTS ITS ZERO

A zero is the outcome a broken probe returns most readily, so it gets a positive control rather than
a reassurance:

1. **The same script, unmodified, reproduces night 1's stated numbers to the digit** — 15/55 and
   1037/17991 — having been written from scratch against directory listings rather than a remembered
   URL form.
2. **It reports PRESENT on 32 of 32 night-2 exposures with per-image counts** (52/52, 47/47, 2/2,
   1/1), not merely an absence of errors. A probe returning zero because it cannot see the archive
   would report zero images found, not 993.
3. **UNKNOWN is a third bucket and it is empty.** Transport failures never fold into either answer.
4. ⚠ **The first probe I wrote returned 404 on every exposure**, because alerts name `*.fits` and
   IRSA stores `*.fits.fz`. It would have reported ~100 % unreachable — a far more exciting result,
   pointing the direction the section wanted, and entirely an artefact. It was caught by fetching a
   directory listing as a control. *(feedback_zero_needs_a_positive_control.)*

---

## 7. OWED

**The ageing leg is not run and is not implied.** Both nights are 2018 and adjacent by design, so
epoch is held fixed and **nothing here bears on whether older archive holdings decay.** Candidate
nights were costed by HTTP HEAD before this ran: 2018-06-03 3.9 GB · 2020-06-01 6.3 GB · 2022-06-01
14.9 GB. Named as owed, not as a null.

🦞🧍💜🔥♾️
