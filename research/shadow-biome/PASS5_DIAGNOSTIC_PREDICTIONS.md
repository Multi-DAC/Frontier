# PASS 5 — DIAGNOSTIC D1 PREDICTIONS (post-hoc, labelled as such)

**Written:** D201 / 2026-08-20 ~22:3x PT, **after** the pass-5 scoring and **before** the
diagnostic is run. These are NOT part of the pass-5 pre-registration and are not scored
alongside P1-P7. They exist because the pass-5 result has an obvious boring explanation and
the explanation is testable inside the data already on disk.

## The objection this tests
Pass 5 found **48.5 %** of an uncut re-extraction sits past `elong = 1.6`, against a control
recovery of only **59.3 %** of ZTF's own alerts. 8,528 detections were produced on 20 images
carrying 376 alerts — a 23 : 1 ratio. A `sep` 5 sigma aperture detection is far looser than
ZTF's PSF-fit S/N >= 5 plus packaging. **At low S/N the second-moment axis ratio a/b is
bounded below by 1 and inflated by noise, so a noise-dominated catalogue shows high
elongation for free.** P6 already refuted in the direction that predicts: the far side is
FAINTER, not brighter.

If that is the whole story, restricting to high S/N should collapse the effect.

## Predictions, before running
- **D1a** — restricting to `peak / globalrms >= 20`, the fraction past 1.6 drops **below 25 %**.
- **D1b** — recovery of ZTF alerts, computed only against high-S/N detections, **exceeds 75 %**.
- **D1c** — the no-truncation check survives: `n[1.6,1.7)/n[1.5,1.6) > 0.5` still holds at high S/N.
- **D1d** — fewer than **8 %** of my `elong > 1.6` detections lie within 2 px of a ZTF alert.
  (ZTF packaged nothing above 1.6, so a match means my `elong` disagrees with theirs.)

**If D1a holds, pass 5's 48.5 % is an upper bound dominated by noise and must be reported as
one.** If D1a is refuted, the far side survives an S/N cut and the number means more.

Branch A only, either way. `PREREGISTRATION.md` §2 governs.
