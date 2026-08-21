"""Shared circular/spatial statistics for pass 6.

Extracted from measure_pass6.py so that diag_pass6.py can reuse the SAME code
by import rather than by copy -- PASS6_DIAGNOSTIC_PREDICTIONS.md says the
controls carry, and that is only true if the functions are literally the same
ones.

AMENDED after verify_pass6.py V1. This docstring used to claim the refactor
"was verified by re-running measure_pass6.py and diffing PASS6_RESULTS.json,
identical". That check did run and did return identical -- and it is WORTHLESS
as evidence: sep 1.4.1 does not return the same catalogue twice on some of
these images (687_zr_c14_o_q1 gave 1012-1016 across repeated runs of identical
code, buffers 64-byte aligned throughout). A re-run-and-diff gauge on a
non-deterministic library can pass a broken refactor and fail a correct one.
The refactor is almost certainly correct because the functions were moved
verbatim -- which is a different and weaker claim than the one this docstring
used to make, and is now the only claim it makes. See PASS6_RESULTS.md sec.4.

Angles are AXIAL (mod 180 deg). All circular statistics are on 2*theta; a
Rayleigh test on raw theta would be meaningless for elongation directions.
"""
import numpy as np

AXIS_DEG   = 10.0     # +/- window around 0 and 90 deg; chance = 22.22%
BRIGHT_PCT = 95.0     # per-frame percentile of peak defining "bright"
NN_RADIUS  = 100.0    # px, collinearity neighbour search


def axial_R(theta):
    """Resultant length of the AXIAL distribution (Rayleigh on 2*theta)."""
    t = np.asarray(theta, float)
    if t.size == 0:
        return float("nan")
    return float(abs(np.mean(np.exp(2j * t))))


def axial_mean(theta):
    """Mean axial direction in degrees, in [0, 180)."""
    t = np.asarray(theta, float)
    if t.size == 0:
        return float("nan")
    return float(np.degrees(np.angle(np.mean(np.exp(2j * t))) / 2.0) % 180.0)


def axis_fraction(theta):
    """Fraction within AXIS_DEG of a PIXEL AXIS (0 or 90 deg). Chance=22.22%."""
    d = np.abs(np.degrees(np.asarray(theta, float)))      # 0..90
    if d.size == 0:
        return float("nan")
    return float((np.minimum(d, 90.0 - d) <= AXIS_DEG).mean())


def axial_delta_deg(phi):
    """Axial angular difference folded to [0, 90], degrees. phi in radians."""
    return np.degrees(np.abs(np.angle(np.exp(2j * np.asarray(phi, float))))) / 2.0


def collinearity(x, y, theta, radius=NN_RADIUS):
    """Median |theta - (angle to nearest neighbour)|, axial, folded to [0,90].

    A streak fragmented into several detections has its elongation pointing
    ALONG the chain -> near 0. Uniform expectation = 45 deg. Immune to
    pixel-grid quantisation: the grid aligns theta to axes, not to a neighbour
    direction. C3 exercises THIS function, not a reimplementation of it.
    """
    x = np.asarray(x, float); y = np.asarray(y, float); th = np.asarray(theta, float)
    n = x.size
    if n < 2:
        return float("nan"), 0
    out = []
    for i in range(n):
        dx = x - x[i]; dy = y - y[i]
        d = np.hypot(dx, dy); d[i] = np.inf
        j = int(np.argmin(d))
        if d[j] > radius:
            continue
        out.append(float(axial_delta_deg(np.arctan2(dy[j], dx[j]) - th[i])))
    if not out:
        return float("nan"), 0
    return float(np.median(out)), len(out)


def nearest_neighbour_table(x, y, theta, sign, radius):
    """For each point: index of nearest neighbour, its distance, the axial
    delta to it, and whether its sign is opposite. Returns arrays masked to
    pairs inside `radius`. Used by D2a."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    th = np.asarray(theta, float); sg = np.asarray(sign)
    n = x.size
    idx, dist, delta, opp = [], [], [], []
    for i in range(n):
        dx = x - x[i]; dy = y - y[i]
        d = np.hypot(dx, dy); d[i] = np.inf
        j = int(np.argmin(d))
        if d[j] > radius:
            continue
        idx.append(i); dist.append(d[j])
        delta.append(float(axial_delta_deg(np.arctan2(dy[j], dx[j]) - th[i])))
        opp.append(bool(sg[j] != sg[i]))
    return (np.array(idx, int), np.array(dist, float),
            np.array(delta, float), np.array(opp, bool))


def bright_proximity(x, y, peak, side_mask):
    """Distances from each side_mask detection to the nearest BRIGHT detection
    in the same frame (self excluded)."""
    side_mask = np.asarray(side_mask, bool)
    x = np.asarray(x, float); y = np.asarray(y, float); peak = np.asarray(peak, float)
    if side_mask.sum() == 0 or x.size < 2:
        return np.array([])
    thr = np.percentile(peak, BRIGHT_PCT)
    bi = np.flatnonzero(peak >= thr)
    if bi.size == 0:
        return np.array([])
    out = []
    for i in np.flatnonzero(side_mask):
        d = np.hypot(x[bi] - x[i], y[bi] - y[i])
        d[bi == i] = np.inf                      # a bright source is not near itself
        m = d.min()
        if np.isfinite(m):
            out.append(m)
    return np.array(out)
