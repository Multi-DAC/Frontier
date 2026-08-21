"""Is my elong SYSTEMATICALLY biased against ZTF's? A signed offset of +0.08 would
manufacture part of the far side. |delta| alone cannot see this. Post-hoc, disclosed."""
import json, os, glob
import numpy as np, sep
from astropy.io import fits
alerts=json.load(open("PASS5_alert_index.json")); by={}
for a in alerts: by.setdefault(a["f"],[]).append(a)
d=[]
for p in sorted(glob.glob("diffimg/*.fz")):
    fn=os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu=next(x for x in h if getattr(x,"data",None) is not None)
        img=np.ascontiguousarray(hdu.data.astype(np.float32))
    bad=~np.isfinite(img); img[bad]=0.0
    xs=[];ys=[];es=[]
    for sign,arr in ((1,img),(-1,-img)):
        bkg=sep.Background(arr,mask=bad); o=sep.extract(arr-bkg.back(),5.0,err=bkg.globalrms,minarea=5,mask=bad)
        ok=o["b"]>0; xs.append(o["x"][ok]);ys.append(o["y"][ok]);es.append(o["a"][ok]/o["b"][ok])
    X=np.concatenate(xs);Y=np.concatenate(ys);E=np.concatenate(es)
    for a in by.get(fn,[]):
        dd=np.hypot(X+1-a["x"],Y+1-a["y"]); k=int(np.argmin(dd))
        if dd[k]<=2.0: d.append(E[k]-a["elong"])
d=np.array(d)
print(f"matched n = {len(d)}")
print(f"median SIGNED (mine - ZTF) = {np.median(d):+.4f}")
print(f"mean   SIGNED              = {d.mean():+.4f}   sd {d.std():.4f}")
print(f"median |delta|             = {np.median(np.abs(d)):.4f}")
print(f"share of matched where mine > ZTF : {100*(d>0).mean():.1f}%")
# how much of the far side could a +median bias explain?
print(f"\nIf every elong were corrected by the median signed offset, the 1.6 boundary")
print(f"moves to {1.6+np.median(d):.4f} in my units.")
json.dump(dict(n=len(d),median_signed=float(np.median(d)),mean_signed=float(d.mean()),
               sd=float(d.std()),median_abs=float(np.median(np.abs(d))),
               share_mine_higher=float((d>0).mean())),open("PASS5_BIAS.json","w"),indent=2)
