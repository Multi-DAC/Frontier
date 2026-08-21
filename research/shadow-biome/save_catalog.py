"""Persist the pass-5 uncut catalogue so pass 6 need not re-extract, and compute
the bias-corrected far-side fraction exactly rather than by interpolation."""
import json, os, glob
import numpy as np, sep
from astropy.io import fits
E=[];S=[];PK=[];IM=[]
for p in sorted(glob.glob("diffimg/*.fz")):
    fn=os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu=next(x for x in h if getattr(x,"data",None) is not None)
        img=np.ascontiguousarray(hdu.data.astype(np.float32))
    bad=~np.isfinite(img); img[bad]=0.0
    for sign,arr in ((1,img),(-1,-img)):
        bkg=sep.Background(arr,mask=bad); o=sep.extract(arr-bkg.back(),5.0,err=bkg.globalrms,minarea=5,mask=bad)
        ok=o["b"]>0
        E.append(o["a"][ok]/o["b"][ok]); PK.append(o["peak"][ok])
        S.append(np.full(ok.sum(),sign)); IM.append(np.full(ok.sum(),fn))
E=np.concatenate(E);PK=np.concatenate(PK);S=np.concatenate(S);IM=np.concatenate(IM)
np.savez_compressed("PASS5_catalog.npz",elong=E,peak=PK,sign=S,image=IM)
N=len(E)
for thr in (1.6,1.6375,1.6556,1.7):
    print(f"  far side at elong > {thr:.4f} : {int((E>thr).sum()):5d} / {N} = {100*(E>thr).mean():.2f}%")
json.dump({"n":int(N),
  "frac_past_1.6":float((E>1.6).mean()),
  "frac_past_1.6375_median_bias_corrected":float((E>1.6375).mean()),
  "frac_past_1.6556_mean_bias_corrected":float((E>1.6556).mean())},
  open("PASS5_BIASCORR.json","w"),indent=2)
print("wrote PASS5_catalog.npz + PASS5_BIASCORR.json  (n=%d)"%N)
