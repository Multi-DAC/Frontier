"""Fetch the USGS National Crustal Model depth-to-Mesozoic-basement grid, resumably.

Shah, A.K. & Boyd, O.S., 2018, USGS OFR 2018-1115, doi:10.3133/ofr20181115.
ScienceBase item 5b0d85eee4b0c39c934b0429. 1 km node spacing, WGS84.
Extent -124.72..-102.73 E, 28.99..49.0 N -- confirmed Day 199 to contain 225/225 survivors.

WHY THIS FILE EXISTS RATHER THAN A ONE-LINER. Two failures on the way in, both silent-ish:

  1. `urlretrieve` truncated at 77,344,024 of 100,617,554 bytes. It DID raise
     ContentTooShortError, which is the only reason this was caught -- a hand-rolled
     read loop would have written a short file and returned success. The link here
     drops packets (see the WPA3 re-key note); any pull of this size will be resumed.

  2. The resume then CORRUPTED the file, and this is the instructive one. The retry
     sent `Range: bytes=77344024-` and accepted `if status not in (200, 206)`. The
     server answered **200** -- it ignored the range and sent the whole body from
     byte 0 -- and the loop appended it to the 77 MB already on disk. The guard was
     written where both answers agree: 200 and 206 both mean "here is data", and they
     mean OPPOSITE things when the file handle is open in append mode. 206 is the only
     status under which appending is correct.

So: 206 or start over, and verify the byte count and a checksum at the end. A
size-only check would pass a file that is right-length and wrong-content.
"""
import hashlib
import os
import sys
import time
import urllib.request

try:
    import truststore
    truststore.inject_into_ssl()
except Exception:                                                       # noqa: BLE001
    pass

ITEM = "5b0d85eee4b0c39c934b0429"
URL = ("https://www.sciencebase.gov/catalog/file/get/" + ITEM +
       "?f=__disk__75%2Fa5%2Fec%2F75a5ece8058a0be128425e910ff016088dfb13d1")
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work",
                    "Dep2MzBasement_LLz.csv")
EXPECT_BYTES = 100_617_554
CHUNK = 1 << 20
MAX_ATTEMPTS = 60


def fetch(url=URL, dest=DEST, expect=EXPECT_BYTES):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(MAX_ATTEMPTS):
        have = os.path.getsize(dest) if os.path.exists(dest) else 0
        if have == expect:
            break
        if have > expect:
            print(f"[reset] {have} > expected {expect}; a prior resume was appended to "
                  f"a 200 response. Starting over.", file=sys.stderr)
            os.remove(dest)
            have = 0

        req = urllib.request.Request(url)
        mode = "wb"
        if have:
            req.add_header("Range", f"bytes={have}-")
            mode = "ab"
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                # THE GUARD. 200 on a ranged request means the server ignored the range
                # and is resending from byte 0. Appending that is corruption, not resume.
                if have and r.status != 206:
                    print(f"[no-range] status {r.status}; restarting from zero",
                          file=sys.stderr)
                    os.remove(dest)
                    continue
                with open(dest, mode) as f:
                    while True:
                        b = r.read(CHUNK)
                        if not b:
                            break
                        f.write(b)
        except Exception as e:                                          # noqa: BLE001
            print(f"[retry {attempt}] {type(e).__name__} at "
                  f"{os.path.getsize(dest) if os.path.exists(dest) else 0} bytes",
                  file=sys.stderr)
            time.sleep(2)

    size = os.path.getsize(dest)
    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for b in iter(lambda: f.read(CHUNK), b""):
            h.update(b)
    ok = size == expect
    print(f"[basement] {size} bytes ({'OK' if ok else 'SHORT/LONG, expected ' + str(expect)})",
          file=sys.stderr)
    print(f"[basement] sha256 {h.hexdigest()}", file=sys.stderr)
    if not ok:
        sys.exit("[abort] incomplete download; do NOT join this file")
    return dest, h.hexdigest()


if __name__ == "__main__":
    fetch()
