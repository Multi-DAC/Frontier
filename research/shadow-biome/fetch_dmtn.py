"""Fetch DMTN-006 and DMTN-007 as primary text and run the PREREG-DMTN-PRIMARY.md probes.

Governed by PREREG-DMTN-PRIMARY.md (commit f253aa6), registered before the fetch.

Procedure §3 of that prereg, implemented literally:
  step 2 — positive control on the extractor BEFORE any null is believed
  step 4 — both spellings and both hyphenations, case-insensitive
  step 3 — a rate is only recorded if a denominator is stated in the same document

Writes: _src_dmtn006.txt, _src_dmtn007.txt, DMTN_PRIMARY_PROBES.json
"""
import json
import re
import sys
import html as _html
from pathlib import Path

try:
    import truststore
    truststore.inject_into_ssl()          # reference_norton_tls_interception
except Exception as e:                     # noqa: BLE001
    print(f"[warn] truststore not injected: {e}")

import requests

HERE = Path(__file__).resolve().parent
DOCS = {
    "DMTN-006": "https://dmtn-006.lsst.io/",
    "DMTN-007": "https://dmtn-007.lsst.io/",
}

# --- prereg §3 step 2: positive control terms. A null from an extractor that read
# --- nothing is not a null.
CONTROL = ["LSST", "difference", "image"]

# --- prereg §3 step 4: both spellings, both hyphenations, case-insensitive.
SPELLINGS = [
    "artifact", "artefact",
    "false positive", "false-positive", "falsepositive",
    "purity", "completeness", "reliability",
    "per square degree", "deg^2", "deg2",
]


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = _html.unescape(raw)
    raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n\n", raw)
    return raw.strip()


def fetch(url: str) -> tuple[str, str, int]:
    r = requests.get(url, timeout=60, headers={"User-Agent": "shadow-biome/1.0"})
    r.raise_for_status()
    # prereg §3 step 5: a redirect IS the finding — record where we actually landed.
    return strip_html(r.text), r.url, r.status_code


def contexts(text: str, pattern: str, width: int = 260) -> list[str]:
    out = []
    for m in re.finditer(pattern, text, flags=re.I):
        a, b = max(0, m.start() - width), min(len(text), m.end() + width)
        out.append(re.sub(r"\s+", " ", text[a:b]).strip())
    return out


def main() -> int:
    report: dict = {"docs": {}, "prereg": "PREREG-DMTN-PRIMARY.md @ f253aa6"}

    for name, url in DOCS.items():
        text, final_url, status = fetch(url)
        (HERE / f"_src_{name.lower().replace('-', '')}.txt").write_text(text, encoding="utf-8")

        # step 2 — POSITIVE CONTROL FIRST.
        control = {t: len(re.findall(re.escape(t), text, flags=re.I)) for t in CONTROL}
        control_ok = sum(1 for v in control.values() if v > 0) >= 3

        # Title, verbatim from the document itself (Q1) — first non-empty line.
        title = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")

        doc = {
            "url_requested": url,
            "url_final": final_url,
            "redirected": final_url.rstrip("/") != url.rstrip("/"),
            "http_status": status,
            "chars": len(text),
            "title_verbatim_first_line": title,
            "positive_control": control,
            "positive_control_passed": control_ok,
            "spelling_counts": {
                s: len(re.findall(re.escape(s), text, flags=re.I)) for s in SPELLINGS
            },
        }

        # Every number-with-a-unit that could be a rate, plus its surroundings, so the
        # denominator question (step 3) is answerable by reading, not by trusting.
        doc["rate_candidates"] = contexts(
            text, r"[\d,]+(?:\.\d+)?\s*(?:%|per\s+square\s+degree|per\s+deg)", 300
        )[:60]

        # Q4 — the 90/95 requirement. Is it HERE, or somewhere else?
        doc["q4_purity_hits"] = contexts(text, r"\b(purity|complete(?:ness)?)\b", 300)[:40]
        doc["q4_ninety_five"] = contexts(text, r"\b9[05]\s*%", 300)[:40]
        doc["q4_snr"] = contexts(text, r"\b(SNR|S/N|signal-to-noise)\b\s*[=of ]*\s*\d", 300)[:20]

        # Q5 — the ~100x claim.
        doc["q5_multiplier_hits"] = contexts(
            text, r"\b\d+\s*(?:times|x|×)\s+(?:higher|larger|greater|more|above|the)", 300
        )[:30]
        doc["q5_decam"] = len(re.findall(r"decam", text, flags=re.I))

        # Q6 — DMTN-007 must contain a METHOD, not merely a discussion.
        doc["q6_method_hits"] = contexts(
            text, r"\b(classif|flag(?:s|ged|ging)?|threshold|criterion|criteria)\b", 200
        )[:30]

        report["docs"][name] = doc
        print(f"{name}: {len(text)} chars · control={control} ok={control_ok}")
        print(f"   title: {title[:90]}")

    (HERE / "DMTN_PRIMARY_PROBES.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("wrote DMTN_PRIMARY_PROBES.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
