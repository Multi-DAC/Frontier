"""PASS 8 block N -- the FRESH-PROCESS child. One image, one structure, exit.

Launched once per (image, structure, replicate) by nondet_pass8.py. One image
per process is not an optimisation choice, it is the measurement: PASS7_DIAG
Q2 found the variation lives in REPEATED IN-PROCESS CALLS, so a child that
looped over 20 images would reintroduce exactly the state it is meant to
exclude and N2 would be measuring the wrong thing.

Structures are transcribed from the two scripts, not paraphrased:
  M  measure_pass6.py:84-92  -- bkg0 = Background(img) FIRST (for local S/N at
                                alert positions), then per-sign Background,
                                then ONE extract at minarea=5.
  D  diag_pass6.py:114-127   -- per-sign Background into a contiguous `prep`,
                                NO bkg0 call, then FIVE extracts from that same
                                prep (the ladder), of which rung 5 is read.
"""
import sys, json
import numpy as np
import sep
from astropy.io import fits

THRESH, WALL, MINAREA = 5.0, 1.6, 5
MINAREA_LADDER = [2, 3, 5, 8, 12]

path, structure = sys.argv[1], sys.argv[2]

with fits.open(path) as h:
    hdu = next(z for z in h if getattr(z, "data", None) is not None)
    img = np.ascontiguousarray(hdu.data.astype(np.float32))
bad = ~np.isfinite(img)
img[bad] = 0.0

n = n_far = 0

if structure == "M":
    # measure_pass6.py:84-92, verbatim in sequence
    bkg0 = sep.Background(img, mask=bad)          # the extra call D does not make
    _sub0, _rms0 = img - bkg0.back(), bkg0.globalrms
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        o = sep.extract(arr - bkg.back(), THRESH, err=bkg.globalrms,
                        minarea=MINAREA, mask=bad)
        ok = o["b"] > 0
        e = o["a"][ok] / o["b"][ok]
        n += len(e)
        n_far += int((e > WALL).sum())

elif structure == "D":
    # diag_pass6.py:114-127, verbatim in sequence -- including the FIVE
    # extracts from one prep, which is the in-process repetition itself
    prep = []
    for sign, arr in ((+1, img), (-1, -img)):
        bkg = sep.Background(arr, mask=bad)
        prep.append((np.ascontiguousarray(arr - bkg.back()), bkg.globalrms))
    for ma in MINAREA_LADDER:
        es = []
        for sub, rms in prep:
            o = sep.extract(sub, THRESH, err=rms, minarea=ma, mask=bad)
            ok = o["b"] > 0
            es.append(o["a"][ok] / o["b"][ok])
        e = np.concatenate(es)
        if ma == MINAREA:                          # rung 5 is the comparable one
            n = len(e)
            n_far = int((e > WALL).sum())
else:
    raise SystemExit("unknown structure %r" % structure)

print(json.dumps({"n": int(n), "n_far": int(n_far)}))
