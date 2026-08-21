"""PROSE-VS-JSON AUDIT — see PROSE_AUDIT_PREREGISTRATION.md (committed first, f15863dc).

Estimand: of the numeric claims in PASS{4,5,6}_RESULTS.md, how many disagree with the
JSON this body emitted?

INSTRUMENT SHAPE, deliberately chosen (feedback_orphan_is_silent_dangle_is_loud):
  Do NOT match prose-number -> JSON-key -> compare. That design fails SILENTLY: a key it
  cannot resolve produces "ungraded", which reads as clean.
  Instead: ask only "does this exact value appear ANYWHERE in the emitted JSON, at any
  plausible rendering?" A matcher failure then lands in the CANDIDATE pile, which is loud
  and which I adjudicate by hand. The leak direction is inverted on purpose.

TWO ENGINES on extraction (D201: a throwaway classifier is an instrument):
  A: regex.
  B: hand-rolled character state machine, no regex at all.
  Their token lists are diffed. A disagreement voids the count.

MUTATION POSITIVE CONTROL, rate not chosen by me: perturb the last significant digit of
randomly chosen MATCHED tokens and re-run. Anything still "matched" is a coincidental
collision = the instrument's false-clean rate, measured against the real corpus in its
real state (D201: the control must run at the state that actually occurs).
"""
import json, re, sys, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MDS = ["PASS4_RESULTS.md", "PASS5_RESULTS.md", "PASS6_RESULTS.md"]

# ---------------------------------------------------------------- JSON haystack
def leaves(o, out):
    if isinstance(o, dict):
        for v in o.values():
            leaves(v, out)
    elif isinstance(o, list):
        for v in o:
            leaves(v, out)
    elif isinstance(o, bool):
        pass
    elif isinstance(o, (int, float)):
        out.append(o)
    elif isinstance(o, str):
        out.append(o)
    return out


def renderings(v):
    """Every plausible way I might have written this value in prose."""
    r = set()
    if isinstance(v, str):
        for m in re.finditer(r"\d+(?:\.\d+)?", v):
            r.add(m.group(0))
            try:
                r |= renderings(float(m.group(0)))
            except ValueError:
                pass
        return r
    try:
        f = float(v)
    except (TypeError, ValueError):
        return r
    if f != f:
        return r
    for scale in (1.0, 100.0):
        s = f * scale
        for dp in range(0, 7):
            r.add(f"{s:.{dp}f}")
            r.add(f"{s:.{dp}f}".rstrip("0").rstrip(".") or "0")
        if abs(s - round(s)) < 1e-12:
            r.add(str(int(round(s))))
            r.add(f"{int(round(s)):,}")
    r.discard("")
    return r


# Bulk data products, NOT claim carriers: 6.9 MB of alert ids and 122 KB of miss records.
# Leaving them in the haystack is what drove the first run's mutation-detection rate to
# 7.5% -- with them present, almost any short numeric string is "grounded" by coincidence.
# Removing them is fixing the instrument's discriminator, not relaxing the gauge: the
# mutation control is RE-RUN at every tier and reported, and it is the thing that decides
# whether any grounding number below is worth reading.
BULK = {"PASS5_alert_index.json", "PASS6_MISSES.json"}


def build_haystack(include_misses):
    files, hay = [], set()
    for p in sorted(HERE.glob("*.json")):
        if p.name.startswith("PROSE_AUDIT"):
            continue
        if not include_misses and p.name in BULK:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:                       # noqa: BLE001
            print(f"  !! unparsed {p.name}: {e}", file=sys.stderr)
            continue
        files.append(p.name)
        for v in leaves(data, []):
            hay |= renderings(v)
    return files, hay


def build_haystack_for(prefix):
    hay = set()
    for p in sorted(HERE.glob(f"{prefix}*.json")):
        if p.name in BULK or p.name.startswith("PROSE_AUDIT"):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:                            # noqa: BLE001
            continue
        for v in leaves(data, []):
            hay |= renderings(v)
    return hay


# ---------------------------------------------------------------- engine A: regex
# NOTE D202: the first version was `\d[\d,]*(?:\.\d+)?`, which greedily eats a TRAILING
# comma out of "20, 10, 50" and yields the token "20,". Those malformed tokens then miss
# the haystack and inflate the candidate count. Engine B caught it on the first run.
TOKEN_RE = re.compile(r"\d(?:[\d,]*\d)?(?:\.\d+)?")


def extract_a(text):
    return [(m.start(), m.group(0)) for m in TOKEN_RE.finditer(text)]


# ------------------------------------------- engine B: character state machine
def extract_b(text):
    out, i, n = [], 0, len(text)
    while i < n:
        if not text[i].isdigit():
            i += 1
            continue
        start = i
        while i < n and (text[i].isdigit() or (text[i] == "," and i + 1 < n and text[i + 1].isdigit())):
            i += 1
        if i < n and text[i] == "." and i + 1 < n and text[i + 1].isdigit():
            i += 1
            while i < n and text[i].isdigit():
                i += 1
        out.append((start, text[start:i]))
    return out


# ---------------------------------------------------------------- classification
CTX = 90
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{2}:\d{2}(:\d{2})?")


def context_of(text, pos, tok):
    a = max(0, pos - CTX)
    b = min(len(text), pos + len(tok) + CTX)
    return text[a:b].replace("\n", " ")


def excuse(text, pos, tok):
    """Reasons a token is not a claim about my own emitted numbers.
    These are COUNTED AND REPORTED, never silently dropped."""
    line_start = text.rfind("\n", 0, pos) + 1
    line_end = text.find("\n", pos)
    line = text[line_start: line_end if line_end != -1 else len(text)]
    before = text[max(0, pos - 30):pos]
    after = text[pos + len(tok): pos + len(tok) + 30]
    for m in DATE_RE.finditer(text[max(0, pos - 12):pos + len(tok) + 12]):
        s = max(0, pos - 12) + m.start()
        if s <= pos < s + len(m.group(0)):
            return "date-or-time"
    if re.search(r"[0-9a-f]{6,}$", before) or re.match(r"^[0-9a-f]{5,}", after):
        return "hex/commit-hash"
    if re.search(r"(§|Pass |PASS|P|D|A|item |#)\s*$", before) and len(tok) <= 2:
        return "section/label-index"
    if line.strip().startswith(("|", "> ")) and False:
        return "table"
    if re.search(r"(GB|MB|KB|bytes)\s*$", after.strip()[:6] or "") or re.match(r"^\s*(GB|MB|KB|B)\b", after):
        return "file-size"
    return None


def audit(include_misses=True, mutate_n=0, seed=20260821):
    files, hay = build_haystack(include_misses)
    rows = []
    engine_disagreements = 0
    for name in MDS:
        text = (HERE / name).read_text(encoding="utf-8", errors="replace")
        ta, tb = extract_a(text), extract_b(text)
        if [t for _, t in ta] != [t for _, t in tb]:
            engine_disagreements += 1
            sa, sb = {(p, t) for p, t in ta}, {(p, t) for p, t in tb}
            print(f"  !! ENGINE DISAGREEMENT in {name}: A-only={sorted(sa - sb)[:6]} "
                  f"B-only={sorted(sb - sa)[:6]}", file=sys.stderr)
        own = build_haystack_for(name.split("_")[0])
        for pos, tok in ta:
            rows.append({
                "file": name, "pos": pos, "tok": tok,
                "excuse": excuse(text, pos, tok),
                "in_all": tok in hay or tok.replace(",", "") in hay,
                "in_own": tok in own or tok.replace(",", "") in own,
                "ctx": context_of(text, pos, tok),
            })

    if mutate_n:
        rng = random.Random(seed)
        pool = [r for r in rows if r["in_all"] and not r["excuse"]]
        picks = rng.sample(pool, min(mutate_n, len(pool)))
        survived = []
        for r in picks:
            t = r["tok"]
            digits = [i for i, c in enumerate(t) if c.isdigit()]
            i = digits[-1]
            newd = str((int(t[i]) + rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])) % 10)
            mut = t[:i] + newd + t[i + 1:]
            if mut == t:
                continue
            still = mut in hay or mut.replace(",", "") in hay
            survived.append((t, mut, still))
        return rows, files, engine_disagreements, survived
    return rows, files, engine_disagreements, None


def sigdigits(tok):
    return len(tok.replace(",", "").replace(".", "").lstrip("0")) or 1


def run(inc, mutate_n=200):
    rows, files, dis, surv = audit(include_misses=inc, mutate_n=mutate_n)
    tier = "ALL-JSON (incl. bulk)" if inc else "CLAIM-JSON only (bulk excluded)"
    live = [r for r in rows if not r["excuse"]]
    m_all = [r for r in live if r["in_all"]]
    det = [s for s in surv if not s[2]]
    print(f"\n=== TIER: {tier} — {len(files)} file(s)")
    print(f"    grounded {len(m_all)}/{len(live)} = {len(m_all)/max(1,len(live)):.1%}")
    print(f"    MUTATION DETECTION {len(det)}/{len(surv)} = {len(det)/max(1,len(surv)):.1%}"
          f"   <-- read THIS before the line above")
    from collections import defaultdict
    by = defaultdict(lambda: [0, 0])
    for t, m, still in surv:
        b = min(sigdigits(t), 5)
        by[b][0] += 1
        by[b][1] += (0 if still else 1)
    print("    detection by significant digits in the token:")
    for b in sorted(by):
        n, d = by[b]
        lab = f"{b}" if b < 5 else "5+"
        print(f"       {lab} digit(s): {d:3d}/{n:3d} = {d/max(1,n):5.1%}")
    return rows, files, dis, surv, live, m_all, det


if __name__ == "__main__":
    print("PROSE-VS-JSON AUDIT — prereg f15863dc")
    run(True)
    rows, files, dis, surv, live, m_all, det = run(False)
    inc = False
    print(f"\nhaystack files ({len(files)}): {', '.join(files)}")
    print(f"engine disagreements: {dis}")
    print(f"total numeric tokens: {len(rows)}")
    ex = [r for r in rows if r["excuse"]]
    live = [r for r in rows if not r["excuse"]]
    print(f"  excused (counted, not dropped): {len(ex)}")
    from collections import Counter
    for k, v in Counter(r["excuse"] for r in ex).most_common():
        print(f"     {k:24s} {v}")
    print(f"  live claim tokens: {len(live)}")
    m_all = [r for r in live if r["in_all"]]
    m_own = [r for r in live if r["in_own"]]
    print(f"  grounded in SOME emitted JSON: {len(m_all)} ({len(m_all)/max(1,len(live)):.1%})")
    print(f"  grounded in its OWN pass JSON: {len(m_own)} ({len(m_own)/max(1,len(live)):.1%})")
    print(f"  CANDIDATES (grounded nowhere) : {len(live)-len(m_all)}")
    for name in MDS:
        f = [r for r in live if r["file"] == name]
        c = [r for r in f if not r["in_all"]]
        print(f"     {name:22s} live={len(f):4d} candidates={len(c):4d} ({len(c)/max(1,len(f)):.1%})")
    out = HERE / "PROSE_AUDIT.json"
    out.write_text(json.dumps({
        "haystack_files": files, "engine_disagreements": dis,
        "total_tokens": len(rows), "excused": len(ex), "live": len(live),
        "grounded_all": len(m_all), "grounded_own": len(m_own),
        "candidates": [{k: r[k] for k in ("file", "pos", "tok", "in_own", "ctx")}
                       for r in live if not r["in_all"]],
        "mutation_control": [{"orig": t, "mutant": m, "survived": s} for t, m, s in (surv or [])],
    }, indent=1), encoding="utf-8")
    print(f"wrote {out.name}")
