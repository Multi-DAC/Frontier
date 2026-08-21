"""PASS 5 step 0: index the night's alerts by difference-image filename.

Reads the tarball ALREADY on disk (pass 4's night, 2018-06-01) and writes a
compact per-alert table. This is an INDEX of data already measured in pass 4,
not a new measurement; it exists so the image-selection rule in
PASS5_PREDICTIONS.md can be applied deterministically.
"""
import tarfile, io, json
import fastavro

out = []
with tarfile.open("data/ztf_public_20180601.tar.gz", "r:gz") as tf:
    for m in tf:
        if not (m.isfile() and m.name.endswith(".avro")):
            continue
        try:
            c = next(iter(fastavro.reader(io.BytesIO(tf.extractfile(m).read()))))["candidate"]
            out.append(dict(f=c.get("pdiffimfilename"), candid=c.get("candid"),
                            x=c.get("xpos"), y=c.get("ypos"),
                            ra=c.get("ra"), dec=c.get("dec"),
                            elong=c.get("elong"), a=c.get("aimage"), b=c.get("bimage"),
                            fwhm=c.get("fwhm"), rb=c.get("rb"),
                            magpsf=c.get("magpsf"), snr=c.get("scorr"),
                            isdiffpos=c.get("isdiffpos")))
        except Exception:
            pass
json.dump(out, open("PASS5_alert_index.json", "w"))
imgs = sorted({r["f"] for r in out if r["f"]})
print(f"alerts={len(out)}  distinct difference images={len(imgs)}")
