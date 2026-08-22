"""SECTION 15 — GATE C5, run FIRST and alone.

PREREG-CORPUS-F2.md section 2 pre-commits this gate before any other prediction may
be scored: compute the share of total corpus mass (WORDS, not files) held by the
single largest source document and by the largest five. If one source holds >50% of
mass, the corpus is one document, C1-C4 are VOID, and the answer to Clayton becomes
"the Corpus cannot carry this weight."

This script reads ONLY file sizes and word counts. It does not read for content, and
it scores no prediction. That separation is the point: the gate must be able to
close the door before anything downstream has a chance to like what it sees.

The prereg also requires the corpus roster to be RE-MEASURED here rather than cited
from its own contract, which no longer reproduces (feedback_filed_defect_misprices_its_own_subject).
"""
import os, json, re

ROOT = r"C:/Users/mercu/clawd/repo-staging/Corpus-Perspectival"

# The prereg's own partition: files under an `archive` or `_superseded` path are not live.
ARCHIVE = re.compile(r"(^|[\\/])(archive|_superseded)([\\/]|$)", re.IGNORECASE)


def walk():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            if f.lower().endswith(".md"):
                yield os.path.join(dp, f)


rows, unreadable = [], []
for p in walk():
    rel = os.path.relpath(p, ROOT)
    try:
        t = open(p, encoding="utf-8", errors="strict").read()
    except Exception:
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception as e:
            # prereg section 1: an unreadable file is a MISS, never a skip
            unreadable.append({"file": rel, "error": f"{type(e).__name__}: {e}"})
            continue
    rows.append({"file": rel, "words": len(t.split()), "bytes": len(t.encode("utf-8")),
                 "archived": bool(ARCHIVE.search(rel))})

live = [r for r in rows if not r["archived"]]
total_w = sum(r["words"] for r in live)
ranked = sorted(live, key=lambda r: -r["words"])

top1 = ranked[0]["words"] / total_w
top5 = sum(r["words"] for r in ranked[:5]) / total_w
top20 = sum(r["words"] for r in ranked[:20]) / total_w

# A directory is a better proxy for "source document" than a file in a corpus that
# splits one work across many .md. Reported BESIDE the file-level number, never
# instead of it, because the prereg says "source document" and the file-level
# reading is the one that could close the gate.
bydir = {}
for r in live:
    top = r["file"].replace("\\", "/").split("/")[0]
    bydir[top] = bydir.get(top, 0) + r["words"]
dir_ranked = sorted(bydir.items(), key=lambda kv: -kv[1])
dir_top1 = dir_ranked[0][1] / total_w

VOID = top1 > 0.50

out = {
    "governed_by": "PREREG-CORPUS-F2.md section 2 (gate C5)",
    "root": ROOT,
    "roster": {"md_total": len(rows) + len(unreadable), "archived": len(rows) - len(live),
               "live": len(live), "unreadable_counted_as_miss": len(unreadable),
               "note": "re-measured here; the D186 counting contract is stale and was not cited"},
    "unreadable": unreadable,
    "total_live_words": total_w,
    "top1_share": top1, "top5_share": top5, "top20_share": top20,
    "largest_files": [{"file": r["file"], "words": r["words"],
                       "share": r["words"] / total_w} for r in ranked[:10]],
    "top_level_dir_shares": [{"dir": d, "words": w, "share": w / total_w}
                             for d, w in dir_ranked],
    "dir_top1_share": dir_top1,
    "GATE": "VOID -- corpus is one document; C1-C4 may not be scored" if VOID else "OPEN -- C1-C4 may be scored",
    "threshold": "top1 > 0.50 voids, pre-committed in PREREG-CORPUS-F2.md before opening",
}
json.dump(out, open("CORPUS_C5_GATE.json", "w"), indent=1)

print(f"roster: {out['roster']['md_total']} md · {out['roster']['archived']} archived · "
      f"{len(live)} live · {len(unreadable)} unreadable")
print(f"total live words: {total_w:,}")
print(f"top-1 file share : {top1:.4%}   (VOID threshold > 50%)")
print(f"top-5 file share : {top5:.4%}")
print(f"top-20 file share: {top20:.4%}")
print(f"top-1 DIRECTORY  : {dir_ranked[0][0]} {dir_top1:.4%}")
print("\nlargest files:")
for r in ranked[:8]:
    print(f"  {r['words']:>8,}  {r['words']/total_w:6.2%}  {r['file'][:78]}")
print("\ntop-level directories:")
for d, w in dir_ranked:
    print(f"  {w:>9,}  {w/total_w:6.2%}  {d}")
print(f"\nGATE C5: {out['GATE']}")
