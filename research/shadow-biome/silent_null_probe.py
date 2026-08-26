#!/usr/bin/env python3
"""
SILENT NULL PROBE v2  --  shadow-biome, device branch, retention leg.
Governed by PREREG-SILENT-NULL.md, committed a8e10fb BEFORE any of this was written.

Question: does a public science archive, queried in the NAIVE way, silently answer a
NARROWER question than the one asked -- and is the narrowing visible anywhere in the
response?

Two axes, kept apart (prereg S1):
  A1 PAGINATION -- fewer ROWS than match. Detectable iff the body carries a true total.
  A2 SEMANTICS  -- fewer ELIGIBLE RECORDS. The total it reports is the true total OF THE
                   NARROWED QUESTION, so it is not detectable from one response at all.

Method: two or three requests per endpoint.
  NAIVE   -- minimum query that returns records.
  BOUNDED -- same query, every window/limit/threshold set explicitly to its widest LEGAL value.
  COUNT   -- where the endpoint supports it, `select count(*)`: the true eligible total,
             independent of any row cap.

E_true = COUNT leg if present, else BOUNDED's declared total, else BOUNDED's rows.

A2 is read off the NAIVE body's own declared total, because that is the number a real querier
would take away.  If naive declares no total at all, A2 is A2-INDETERMINATE -- never
A2-SILENT.  That is the conservative direction, against the hypothesis.

Writes SILENT_NULL_RESULTS.json. Every row is recorded, including failures: a denial that
leaves no row is the defect this program exists to study.

V1 DEFECTS, REPAIRED HERE -- all five found by reading the raw bodies, not the summary.
Three of the five made my own probe commit the failure it exists to measure:
  D1  non-2xx accepted. IRIS returned HTTP 410 + an HTML error page; the text parser counted
      172 HTML lines as 172 records and the row scored A2-NONE. A dead endpoint manufactured
      a clean null. FIX: status must be 2xx or the leg is UNREACHABLE.
  D2  a FAILED bounded leg scored as agreement. openFDA bounded 403 -> 0 rows; the comparator
      asked only `grew`, so 617935 -> 0 read as "within the 5% band". FIX: a shrink is its own
      verdict and a failed leg can never produce a concordance.
  D3  false DECLARATION. The token list for JPL cad.api contained `signature` -- a generic
      API-version key present in every response. It matched, and a 30 -> 516088 narrowing
      scored A2-DECLARED. FIX: A1 and A2 declarations are separate lists, and an A2 token must
      NAME THE APPLIED NARROWING, never a generic envelope key. (This fix moves a row TOWARD
      my hypothesis, so the evidence is recorded verbatim: the naive cad.api body has exactly
      four top-level keys -- signature, count, fields, data -- and zero hits for date-min,
      date-max, dist-max, or "default".)
  D4  illegal BOUNDED. Zenodo capped unauthenticated page size at 25 and rejected size=200;
      prereg S4.3 predicted this class in advance. FIX: legal maxima.
  D5  a bare-JSON-array TAP response was unparseable. FIX: accept both shapes.
"""

import json, re, sys, time, datetime, traceback
import requests

try:
    import truststore; truststore.inject_into_ssl()
except Exception:
    pass

UA = {"User-Agent": "shadow-biome-silent-null-probe/2.0 (research; clawdEFS@proton.me)"}
TIMEOUT = 90
BAND = 0.05   # prereg S1: stated in advance, not chosen after


# ----------------------------------------------------------------- parsers
# each returns (rows:int|None, declared_total:int|None, note:str)

def p_atom(body):
    rows = len(re.findall(r"<entry\b", body))
    m = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", body)
    return rows, (int(m.group(1)) if m else None), "atom/opensearch"

def p_crossref(body):
    d = json.loads(body)["message"]
    return len(d.get("items", [])), d.get("total-results"), "crossref"

def p_openalex(body):
    d = json.loads(body)
    return len(d.get("results", [])), d.get("meta", {}).get("count"), "openalex"

def p_gbif(body):
    d = json.loads(body)
    return len(d.get("results", [])), d.get("count"), "gbif"

def p_zenodo(body):
    d = json.loads(body)["hits"]
    t = d.get("total")
    if isinstance(t, dict):
        t = t.get("value")
    return len(d.get("hits", [])), t, "zenodo"

def p_pubmed(body):
    d = json.loads(body)["esearchresult"]
    return len(d.get("idlist", [])), (int(d["count"]) if "count" in d else None), "eutils"

def p_openfda(body):
    d = json.loads(body)
    return len(d.get("results", [])), d.get("meta", {}).get("results", {}).get("total"), "openfda"

def p_cad(body):
    d = json.loads(body)
    c = d.get("count")
    return len(d.get("data") or []), (int(c) if c is not None else None), "ssd-cad"

def p_tap(body):
    """TAP format=json comes in two shapes: {metadata,data} and a bare array of objects."""
    d = json.loads(body)
    if isinstance(d, list):
        return len(d), None, "tap/json bare-array (no total, no overflow marker by construction)"
    return len(d.get("data", [])), None, "tap/json envelope (no total field in this serialization)"

def p_tap_count(body):
    d = json.loads(body)
    if isinstance(d, list):
        return 1, int(list(d[0].values())[0]), "tap count(*) bare-array"
    return 1, int(d["data"][0][0]), "tap count(*)"

def p_datacite(body):
    d = json.loads(body)
    return len(d.get("data", [])), d.get("meta", {}).get("total"), "datacite"

def p_geojson_fdsn(body):
    d = json.loads(body)
    return len(d.get("features", [])), d.get("metadata", {}).get("count"), "fdsn/geojson"

def p_fdsn_text(body):
    if body.lstrip()[:1] == "<":
        raise ValueError("body is HTML, not FDSN text")
    lines = [l for l in body.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    return len(lines), None, "fdsn/text (no total by contract)"

def p_nwis(body):
    d = json.loads(body)
    n = 0
    for ts in d.get("value", {}).get("timeSeries", []):
        for v in ts.get("values", []):
            n += len(v.get("value", []))
    return n, None, "nwis/waterml-json (no total by contract)"


# ----------------------------------------------------------------- the frame
# Endpoint list fixed in PREREG-SILENT-NULL.md S2 BEFORE contact. `pred` is what is scored.
# a2_declares -- tokens that would NAME AN APPLIED ELIGIBILITY EDIT (a window, a cut, a mode).
#                A generic envelope key must never appear here (V1 defect D3).
# a1_declares -- tokens that would carry a TRUE TOTAL or an overflow flag.

SIMBAD_Q = "SELECT main_id FROM basic WHERE otype='G..'"
SIMBAD_C = "SELECT COUNT(*) AS n FROM basic WHERE otype='G..'"
PS_Q, PS_C = "select pl_name from ps", "select count(*) as n from ps"

SPEC = [
 dict(id="S1", tier="seed", name="USGS FDSN event", pred="A2-SILENT",
      url="https://earthquake.usgs.gov/fdsnws/event/1/query",
      naive={"format": "geojson", "minmagnitude": "6"},
      bounded={"format": "geojson", "minmagnitude": "6",
               "starttime": "1900-01-01T00:00:00", "endtime": "2026-08-27T00:00:00",
               "limit": "20000"},
      parse=p_geojson_fdsn,
      a2_declares=["starttime", "endtime", "timerange", "period", "last 30", "default"],
      a1_declares=["count"]),

 dict(id="P1", tier="sibling", name="EarthScope/IRIS FDSN event", pred="A2-SILENT",
      url="https://service.iris.edu/fdsnws/event/1/query",
      naive={"format": "text", "minmagnitude": "6"},
      bounded={"format": "text", "minmagnitude": "6",
               "starttime": "1900-01-01T00:00:00", "endtime": "2026-08-27T00:00:00"},
      parse=p_fdsn_text,
      a2_declares=["starttime", "endtime", "timerange", "default"], a1_declares=[]),

 dict(id="F1", tier="frame", name="arXiv API", pred="A2-NONE",
      url="http://export.arxiv.org/api/query",
      naive={"search_query": "all:electron"},
      bounded={"search_query": "all:electron", "start": "0", "max_results": "200"},
      parse=p_atom, a2_declares=["submittedDate", "default"],
      a1_declares=["totalResults", "itemsPerPage"]),

 dict(id="F2", tier="frame", name="Crossref works", pred="A2-NONE",
      url="https://api.crossref.org/works",
      naive={"query": "electron"},
      bounded={"query": "electron", "rows": "200"},
      parse=p_crossref, a2_declares=["filter", "from-index-date", "default"],
      a1_declares=["total-results", "items-per-page"]),

 dict(id="F3", tier="frame", name="OpenAlex works", pred="A2-NONE",
      url="https://api.openalex.org/works",
      naive={"search": "electron"},
      bounded={"search": "electron", "per_page": "200"},
      parse=p_openalex, a2_declares=["filter", "from_publication_date", "default"],
      a1_declares=["count", "per_page"]),

 dict(id="F4", tier="frame", name="GBIF occurrence", pred="A2-NONE",
      url="https://api.gbif.org/v1/occurrence/search",
      naive={"q": "Corvus"},
      bounded={"q": "Corvus", "limit": "300"},
      parse=p_gbif, a2_declares=["facet", "eventdate", "default"],
      a1_declares=["count", "endOfRecords"]),

 dict(id="F5", tier="frame", name="Zenodo records", pred="A2-NONE",
      url="https://zenodo.org/api/records",
      naive={"q": "electron"},
      bounded={"q": "electron", "size": "25"},          # D4: 25 is the unauthenticated max
      parse=p_zenodo, a2_declares=["all_versions", "default"], a1_declares=["total"]),

 dict(id="F6", tier="frame", name="PubMed esearch", pred="A2-NONE",
      url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
      naive={"db": "pubmed", "term": "electron", "retmode": "json"},
      bounded={"db": "pubmed", "term": "electron", "retmode": "json", "retmax": "200"},
      parse=p_pubmed, a2_declares=["datetype", "reldate", "mindate", "default"],
      a1_declares=["count", "retmax"]),

 dict(id="F7", tier="frame", name="openFDA drug event", pred="A2-SILENT",
      url="https://api.fda.gov/drug/event.json",
      naive={"search": "patient.drug.medicinalproduct:aspirin"},
      bounded={"search": "patient.drug.medicinalproduct:aspirin", "limit": "100"},  # D4
      parse=p_openfda, a2_declares=["receivedate", "default"],
      a1_declares=["total", "limit", "skip"]),

 dict(id="F8", tier="frame", name="JPL SSD close-approach", pred="A2-SILENT",
      url="https://ssd-api.jpl.nasa.gov/cad.api",
      naive={},
      bounded={"date-min": "1900-01-01", "date-max": "2100-01-01", "dist-max": "1"},
      parse=p_cad, a2_declares=["date-min", "date-max", "dist-max", "default"],
      a1_declares=["count"]),

 dict(id="F9", tier="frame", name="SIMBAD TAP", pred="A2-DECLARED",
      url="https://simbad.cds.unistra.fr/simbad/sim-tap/sync",
      naive={"request": "doQuery", "lang": "adql", "format": "json", "query": SIMBAD_Q},
      bounded={"request": "doQuery", "lang": "adql", "format": "json",
               "MAXREC": "20000000", "query": SIMBAD_Q},
      count={"request": "doQuery", "lang": "adql", "format": "json", "query": SIMBAD_C},
      count_parse=p_tap_count,
      parse=p_tap, a2_declares=["OVERFLOW", "MAXREC", "truncat"], a1_declares=["OVERFLOW"]),

 dict(id="F10", tier="frame", name="NASA Exoplanet Archive TAP", pred="A2-DECLARED",
      url="https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
      naive={"request": "doQuery", "lang": "adql", "format": "json", "query": PS_Q},
      bounded={"request": "doQuery", "lang": "adql", "format": "json",
               "MAXREC": "20000000", "query": PS_Q},
      count={"request": "doQuery", "lang": "adql", "format": "json", "query": PS_C},
      count_parse=p_tap_count,
      parse=p_tap, a2_declares=["OVERFLOW", "MAXREC", "truncat"], a1_declares=["OVERFLOW"]),

 dict(id="F11", tier="frame", name="DataCite DOIs", pred="A2-NONE",
      url="https://api.datacite.org/dois",
      naive={"query": "electron"},
      bounded={"query": "electron", "page[size]": "200"},
      parse=p_datacite, a2_declares=["registered", "default"],
      a1_declares=["total", "totalPages"]),

 dict(id="F12", tier="frame", name="USGS Water Services IV", pred="A2-SILENT",
      url="https://waterservices.usgs.gov/nwis/iv/",
      naive={"format": "json", "sites": "01646500", "parameterCd": "00060"},
      bounded={"format": "json", "sites": "01646500", "parameterCd": "00060",
               "startDT": "2026-05-01", "endDT": "2026-08-26"},
      parse=p_nwis, a2_declares=["mode=latest", "filter:timerange", "modifiedsince"],
      a1_declares=[]),
]


# ----------------------------------------------------------------- run
def fetch(url, params, retries=2):
    """D9: a transient 5xx must not be allowed to decide a verdict. USGS Water Services
    answered 200 at 11:5x, 503 at 12:0x and 200 again at 12:1x within one probe session; on
    the 503 it scored UNREACHABLE and its A2-DECLARED evidence vanished from the run. Retry
    5xx and transport errors; NEVER retry a 4xx, which is a real answer about the request."""
    t0, attempts = time.time(), []
    for i in range(retries + 1):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=TIMEOUT)
            attempts.append(r.status_code)
            if r.status_code < 500 or i == retries:
                return dict(ok=True, status=r.status_code, attempts=attempts,
                            ctype=r.headers.get("content-type", ""), bytes=len(r.content),
                            elapsed=round(time.time() - t0, 2), final_url=r.url, body=r.text)
        except Exception as e:
            attempts.append(f"{type(e).__name__}")
            if i == retries:
                return dict(ok=False, status=None, attempts=attempts, ctype="", bytes=0,
                            elapsed=round(time.time() - t0, 2), final_url=url, body="",
                            error=f"{type(e).__name__}: {e}")
        time.sleep(6)


def envelope(body, keep=3):
    """Everything a response says ABOUT itself: the body with its record arrays removed.

    A declaration of an applied edit is envelope furniture. A field name inside the records
    is not a declaration -- it is the data. Conflating them is v2 defect D7.
    Non-JSON bodies fall back to their first 4000 chars (headers/preamble live there).
    """
    def strip(o, depth=0):
        if isinstance(o, list):
            return [strip(x, depth + 1) for x in o[:keep]] + (
                [f"<{len(o) - keep} more rows elided>"] if len(o) > keep else [])
        if isinstance(o, dict):
            return {k: strip(v, depth + 1) for k, v in o.items()}
        return o
    try:
        return json.dumps(strip(json.loads(body)))[:40000]
    except Exception:
        return body[:4000]


def do_leg(spec, params, parser):
    r = fetch(spec["url"], params)
    rec = {k: v for k, v in r.items() if k != "body"}
    rec["params"] = params
    rec["usable"] = False
    if not r["ok"]:
        return rec, r["body"]
    # D1: transport success is not an answer.
    if not (200 <= r["status"] < 300):
        rec["parse_note"] = f"NON-2XX {r['status']} -- leg rejected (V1 defect D1)"
        rec["body_head"] = r["body"][:400]
        return rec, r["body"]
    try:
        rows, total, note = parser(r["body"])
        rec.update(rows=rows, declared_total=total, parse_note=note, usable=True)
    except Exception as e:
        rec.update(rows=None, declared_total=None,
                   parse_note=f"UNPARSEABLE {type(e).__name__}: {e}",
                   body_head=r["body"][:400])
    return rec, r["body"]


def measure(spec):
    row = dict(id=spec["id"], tier=spec["tier"], name=spec["name"],
               predicted_A2=spec["pred"],
               fetched_at=datetime.datetime.now(datetime.UTC).isoformat())

    rec, body = do_leg(spec, spec["naive"], spec["parse"])
    # D7 (v2 defect): the token scan used to read the whole body INCLUDING the data rows, where
    # a field name like `eventdate` matches on every record. A declaration lives in the
    # ENVELOPE. Strip long arrays and search what is left.
    env = envelope(body)
    rec["envelope_scanned_chars"] = len(env)
    low = env.lower()
    rec["a2_declaration_tokens_found"] = [t for t in spec["a2_declares"] if t.lower() in low]
    rec["a1_declaration_tokens_found"] = [t for t in spec["a1_declares"] if t.lower() in low]
    # P4: HTTP 200 whose body is an error, or is empty of the requested kind
    rec["http200_but_no_answer"] = bool(
        rec.get("status") == 200 and
        (rec.get("rows") in (0, None) or '"error"' in low[:4000] or "<error" in low[:4000]))
    rec["body_head"] = body[:700]
    row["naive"] = rec

    row["bounded"], _ = do_leg(spec, spec["bounded"], spec["parse"])
    if spec.get("count"):
        row["count_leg"], _ = do_leg(spec, spec["count"], spec["count_parse"])
    return row


def classify(row):
    n, b = row.get("naive", {}), row.get("bounded", {})
    c = row.get("count_leg")

    if not n.get("usable"):
        row.update(A2="A2-UNREACHABLE", A1="A1-UNREACHABLE",
                   why=f"naive leg unusable: {n.get('error') or n.get('parse_note')}")
        return row

    # ---- E_true, in preference order
    if c and c.get("usable") and c.get("declared_total") is not None:
        E_true, src = c["declared_total"], "count(*) leg"
    elif b.get("usable") and b.get("declared_total") is not None:
        E_true, src = b["declared_total"], "bounded declared total"
    elif b.get("usable"):
        E_true, src = b["rows"], "bounded rows returned"
    else:
        row.update(A2="A2-UNREACHABLE", A1="A1-UNREACHABLE",
                   why=f"bounded leg unusable and no count leg: "
                       f"{b.get('error') or b.get('parse_note')}")
        return row
    row["E_true"] = [E_true, src]

    nt, nr = n.get("declared_total"), n.get("rows")
    row["naive_declared_total"], row["naive_rows"] = nt, nr

    # D2: a bounded/count leg SMALLER than naive is a probe fault, never concordance.
    ref = nt if nt is not None else nr
    if ref and E_true < ref * (1 - BAND):
        row.update(A2="A2-PROBE-FAULT", A1="A1-PROBE-FAULT",
                   why=f"E_true ({E_true}, {src}) is SMALLER than naive ({ref}). The widest "
                       f"legal query returned less than the naive one -- BOUNDED is wrong, "
                       f"not the archive. Excluded from every rate.")
        return row

    # ---- A2: semantics, read off what a real querier would take away
    #
    # D6 (v2 defect, same family as D3): the declaration branch used to be tested FIRST, so an
    # endpoint that narrowed NOTHING scored A2-DECLARED merely because a token matched. The
    # declaration test was being run where both answers look identical -- a narrowing archive
    # that declares and an honest archive that never narrowed are indistinguishable to it.
    # A declaration is only meaningful about an edit that HAPPENED. Gate it on the narrowing.
    narrowed = nt is not None and E_true > nt * (1 + BAND)
    if narrowed and n["a2_declaration_tokens_found"]:
        row["A2"] = "A2-DECLARED"
        row["why"] = (f"narrowed {nt} -> {E_true}, AND the naive body names its own edit: "
                      f"{n['a2_declaration_tokens_found']}")
    elif nt is None and n["a2_declaration_tokens_found"]:
        row["A2"] = "A2-DECLARED"
        row["why"] = ("no total in the body, but the naive body names an applied edit: "
                      f"{n['a2_declaration_tokens_found']}")
    elif nt is None:
        row["A2"] = "A2-INDETERMINATE"
        row["why"] = ("naive body carries NO total, so its eligible set cannot be read from "
                      "inside one response; narrowing is not separable from row-capping")
    elif E_true > nt * (1 + BAND):
        row["A2"] = "A2-SILENT"
        row["why"] = (f"naive reports a total of {nt}; the true eligible total is {E_true} "
                      f"({E_true/nt:,.0f}x) and nothing in the naive body names the edit")
    else:
        row["A2"] = "A2-NONE"
        row["why"] = f"naive total {nt} vs E_true {E_true} within the {int(BAND*100)}% band"

    # ---- A1: pagination
    #
    # D8 (v2 defect): truncation was tested against E_true, the UN-narrowed total. That
    # conflates the two axes this probe exists to keep apart -- JPL returned all 30 records
    # eligible under its own narrowed question, i.e. it did not paginate at all, and scored
    # A1-DECLARED off a `count` token whose value was the narrowed 30. A1 must be judged
    # against the eligible set the NAIVE query itself acknowledged.
    naive_eligible = nt if nt is not None else E_true
    row["naive_eligible_set"] = naive_eligible
    truncated = nr is not None and nr < naive_eligible * (1 - BAND)
    if not truncated:
        row["A1"] = "A1-NONE"
    elif nt is not None:
        row["A1"] = "A1-DECLARED"   # the body carries the total of its own eligible set
    elif n["a1_declaration_tokens_found"]:
        row["A1"] = "A1-DECLARED"
    else:
        row["A1"] = "A1-SILENT"
    row["A1_detail"] = (f"naive returned {nr} of its own eligible {naive_eligible} "
                        f"(E_true {E_true}); naive-declared total {nt}")
    return row


def main():
    out = []
    for spec in SPEC:
        sys.stderr.write(f"[{spec['id']}] {spec['name']} ... "); sys.stderr.flush()
        try:
            row = classify(measure(spec))
        except Exception:
            row = dict(id=spec["id"], tier=spec["tier"], name=spec["name"],
                       A2="A2-UNREACHABLE", A1="A1-UNREACHABLE",
                       why="probe crashed", traceback=traceback.format_exc())
        out.append(row)
        sys.stderr.write(f"{row['A2']} / {row['A1']}\n")
        time.sleep(1.0)

    frame = [r for r in out if r["tier"] == "frame"]
    silent = [r for r in frame if r["A2"] == "A2-SILENT"]
    payload = dict(
        prereg="PREREG-SILENT-NULL.md @ a8e10fb", probe_version=2,
        run_at=datetime.datetime.now(datetime.UTC).isoformat(), tolerance_band=BAND,
        headline_A2_SILENT_over_frame=[len(silent), len(frame)],
        rows=out)
    with open("SILENT_NULL_RESULTS.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)
    for r in out:
        print(f"{r['id']:>3} {r['name'][:34]:<34} {r['A2']:<18} {r['A1']:<16} {r.get('why','')[:80]}")
    print(f"\nHEADLINE A2-SILENT over frame: {len(silent)}/{len(frame)}")


if __name__ == "__main__":
    main()
