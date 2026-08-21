"""PASS 5 DIAGNOSTIC D1 — is the far side just low-S/N noise?
Governed by PASS5_DIAGNOSTIC_PREDICTIONS.md, committed before this ran.
Re-extracts the same 20 images already on disk; downloads nothing.
"""
import json, os, glob
import numpy as np, truststore, sep
from astropy.io import fits

SNR_HI, THRESH, MINAREA, MATCH = 20.0, 5.0, 5, 2.0
alerts = json.load(open("PASS5_alert_index.json"))
by_img = {}
for a in alerts: by_img.setdefault(a["f"], []).append(a)

E=[]; SN=[]; MATCHED=[]
rec_hi=tot_hi=0
for p in sorted(glob.glob("diffimg/*.fz")):
    fn = os.path.basename(p)[:-3]
    with fits.open(p) as h:
        hdu = next(x for x in h if getattr(x,"data",None) is not None)
        img = np.ascontiguousarray(hdu.data.astype(np.float32))
    bad = ~np.isfinite(img); img[bad]=0.0
    xs=[];ys=[];es=[];ss=[]
    for sign,arr in ((1,img),(-1,-img)):
        bkg=sep.Background(arr,mask=bad); sub=arr-bkg.back()
        o=sep.extract(sub,THRESH,err=bkg.globalrms,minarea=MINAREA,mask=bad)
        ok=o["b"]>0
        xs.append(o["x"][ok]); ys.append(o["y"][ok])
        es.append(o["a"][ok]/o["b"][ok]); ss.append(o["peak"][ok]/bkg.globalrms)
    X=np.concatenate(xs);Y=np.concatenate(ys);Ei=np.concatenate(es);Si=np.concatenate(ss)
    al=by_img.get(fn,[])
    m=np.zeros(len(Ei),bool)
    hi=Si>=SNR_HI
    for a in al:
        d=np.hypot(X+1-a["x"],Y+1-a["y"])
        k=int(np.argmin(d))
        if d[k]<=MATCH: m[k]=True
        if hi.any():
            dh=np.hypot(X[hi]+1-a["x"],Y[hi]+1-a["y"])
            if dh.min()<=MATCH: rec_hi+=1
        tot_hi+=1
    E.append(Ei);SN.append(Si);MATCHED.append(m)

E=np.concatenate(E);SN=np.concatenate(SN);M=np.concatenate(MATCHED)
N=len(E)
def frac_past(mask):
    n=mask.sum(); return (E[mask]>1.6).sum(), n, ((E[mask]>1.6).sum()/n if n else np.nan)
print(f"n total detections = {N}")
for lab,mask in [("ALL",np.ones(N,bool)),("S/N>=10",SN>=10),("S/N>=20",SN>=20),
                 ("S/N>=50",SN>=50),("S/N>=100",SN>=100)]:
    k,n,f=frac_past(mask); print(f"  {lab:10s} n={n:6d}  past 1.6: {k:6d}  = {100*f:6.2f}%")

hi=SN>=SNR_HI
b56=int(((E[hi]>=1.5)&(E[hi]<1.6)).sum()); b67=int(((E[hi]>=1.6)&(E[hi]<1.7)).sum())
step=b67/b56 if b56 else float("nan")
d1a=frac_past(hi)[2]<0.25
d1b=(rec_hi/tot_hi if tot_hi else np.nan)>0.75
d1c=step>0.5
past=E>1.6
d1d=(M[past].sum()/past.sum())<0.08
print(f"\n  D1a frac past 1.6 at S/N>=20 : {100*frac_past(hi)[2]:.2f}%  -> {'HELD' if d1a else 'REFUTED'} (<25%)")
print(f"  D1b recovery vs high-S/N only : {100*rec_hi/tot_hi:.2f}% (n={tot_hi})  -> {'HELD' if d1b else 'REFUTED'} (>75%)")
print(f"  D1c step ratio at S/N>=20     : {step:.4f} ({b67}/{b56})  -> {'HELD' if d1c else 'REFUTED'} (>0.5)")
print(f"  D1d matched share of past-1.6 : {100*M[past].sum()/past.sum():.2f}% ({int(M[past].sum())}/{int(past.sum())})  -> {'HELD' if d1d else 'REFUTED'} (<8%)")
json.dump(dict(n=N, snr_ladder={lab:[int(frac_past(m)[0]),int(frac_past(m)[1]),float(frac_past(m)[2])]
    for lab,m in [("all",np.ones(N,bool)),("snr10",SN>=10),("snr20",SN>=20),("snr50",SN>=50),("snr100",SN>=100)]},
    D1a=bool(d1a),D1b=bool(d1b),D1c=bool(d1c),D1d=bool(d1d),
    recovery_high_snr=float(rec_hi/tot_hi), step_hi=float(step),
    matched_share_past=float(M[past].sum()/past.sum())),
    open("PASS5_DIAG.json","w"),indent=2)
print("wrote PASS5_DIAG.json")
