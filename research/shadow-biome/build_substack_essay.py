#!/usr/bin/env python3
"""
build_substack_essay.py -- PAPER-07-SHORT.md -> a paste copy that survives Substack.

Same rules as Frontier/research/place-threshold-screen/code/build_substack.py, which
was written against MEASURED Substack paste behaviour (Day 139, *The Curvature of Good
and Evil*; Day 199, the place-threshold dossier):

  * <img> base64                  -> transfers (sometimes needs a second paste)
  * rendered math                 -> does NOT transfer
  * <table>                       -> does NOT transfer cleanly
  * anything in <style>/class/attr-> gone

So: emit ONLY {h2, h3, p, strong, em, br, ul/li, blockquote, hr, code}, and decide
per table whether the GRID is the argument. Neither table here is a numeric matrix --
both are two-column label->consequence maps -- so both REFLOW to lists. Reflowed beats
imaged: selectable, searchable, readable on a phone.

The h1 stays OUT of the body (it goes in Substack's title field, or the post opens by
announcing its own name). The deck line goes in the subtitle field.

Outputs into substack/:
  POST.html        self-contained -- open in a browser, Ctrl-A, Ctrl-C, paste
  PASTE-NOTES.md   title/subtitle text + the checklist + the email-clip number
"""

import html as _html
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "PAPER-07-SHORT.md"
OUT = ROOT / "substack"

ALLOWED_TAGS = {"h2", "h3", "p", "strong", "em", "br", "ul", "li", "blockquote", "hr", "code"}


# ---------------------------------------------------------------- inline

def inline(text: str) -> str:
    """Markdown inline -> the small tag set Substack keeps.

    Order matters: ** before *, so bold is not eaten by the italic toggle. The
    italic pass is a SEQUENTIAL non-greedy pair match, which is what makes the
    italic-inside-italic citations render correctly --
        *(field attempt: L. Allen,* Science News Explores*, 29 Sept 2025)*
    pairs as em / roman / em, which is the intended typography.
    """
    t = _html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t, flags=re.S)
    if "*" in t:
        raise SystemExit(f"UNPAIRED ASTERISK left in: {t[:160]!r}")
    return t


# ---------------------------------------------------------------- blocks

def split_row(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_table(rows):
    """Two-column label->consequence table -> <ul>. Grid is not the argument here."""
    header = split_row(rows[0])
    body = [split_row(r) for r in rows[2:]]  # rows[1] is the |---|---| rule
    if len(header) != 2:
        raise SystemExit(f"table is not 2-column, decide it by hand: {header}")
    label = header[1]
    items = []
    for cells in body:
        left, right = cells[0], cells[1]
        items.append(
            f"  <li>{inline(left)}<br />\n"
            f"      <em>{_html.escape(label)}:</em> {inline(right)}</li>"
        )
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def render_quote(lines):
    """> lines, with a bare '>' meaning a paragraph break inside the quote."""
    paras, cur = [], []
    for ln in lines:
        stripped = ln.lstrip(">").strip()
        if not stripped:
            if cur:
                paras.append(" ".join(cur))
                cur = []
        else:
            cur.append(stripped)
    if cur:
        paras.append(" ".join(cur))
    inner = "\n".join(f"  <p>{inline(p)}</p>" for p in paras)
    return f"<blockquote>\n{inner}\n</blockquote>"


def build():
    src = io.open(SRC, encoding="utf-8").read()
    lines = src.split("\n")

    title = None
    deck = None
    out = []

    i = 0
    seen_h2 = False
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            i += 1
            continue

        if line.startswith("### ") and not seen_h2 and deck is None:
            deck = line[4:].strip()          # the deck -> Substack subtitle field
            i += 1
            continue

        if line.startswith("## "):
            seen_h2 = True
            out.append(f"<h2>{inline(line[3:].strip())}</h2>")
            i += 1
            continue

        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:].strip())}</h3>")
            i += 1
            continue

        if line.strip() == "---":
            out.append("<hr />")
            i += 1
            continue

        if line.startswith(">"):
            blk = []
            while i < len(lines) and lines[i].startswith(">"):
                blk.append(lines[i])
                i += 1
            out.append(render_quote(blk))
            continue

        if line.startswith("|"):
            blk = []
            while i < len(lines) and lines[i].startswith("|"):
                blk.append(lines[i])
                i += 1
            out.append(render_table(blk))
            continue

        # plain paragraph: join the wrapped lines
        blk = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||---\s*$)", lines[i]):
            blk.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(blk))}</p>")

    body = "\n\n".join(out)

    # ---- gauges, in Python, before anything is written -------------------
    # 1. no forbidden tags, no style/class attributes
    tags = set(t.lower() for t in re.findall(r"<\s*/?\s*([a-zA-Z0-9]+)", body))
    bad = tags - ALLOWED_TAGS
    if bad:
        raise SystemExit(f"FORBIDDEN TAGS EMITTED: {sorted(bad)}")
    if re.search(r'\b(style|class)\s*=', body):
        raise SystemExit("style/class attribute emitted")

    # 2. unique-token set-diff, source vs output. This is what proves nothing
    #    was dropped -- re-reading it is not a gauge.
    def toks(s):
        s = re.sub(r"<[^>]+>", " ", s)
        s = _html.unescape(s)
        return set(w.lower() for w in re.findall(r"[\wÀ-ɏ]+", s))

    src_plain = re.sub(r"[*`|>#]", " ", src)
    lost = toks(src_plain) - toks(body)
    gained = toks(body) - toks(src_plain)

    OUT.mkdir(exist_ok=True)
    page = (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">\n"
        f"<title>{_html.escape(title)}</title>\n"
        "<style>body{max-width:44em;margin:3em auto;padding:0 1.5em;"
        "font:18px/1.62 Georgia,'Iowan Old Style',serif;color:#111}"
        "h2{margin-top:2em;font-size:1.25em;letter-spacing:.02em}"
        "h3{margin-top:1.6em;font-size:1.05em}"
        "blockquote{margin:1.4em 0 1.4em 1.2em;padding-left:1em;"
        "border-left:3px solid #ccc;color:#333}"
        "hr{border:0;border-top:1px solid #ddd;margin:2.4em 0}"
        "li{margin:.7em 0}code{font-size:.9em;background:#f2f2f2;padding:.1em .3em}"
        "</style></head>\n<body>\n\n" + body + "\n\n</body></html>\n"
    )
    (OUT / "POST.html").write_text(page, encoding="utf-8")

    body_bytes = len(body.encode("utf-8"))
    notes = f"""# PASTE NOTES -- {title}

## 1. The two fields, so the post does not announce its own name

**Title (paste into Substack's title field):**

    {title}

**Subtitle (paste into Substack's subtitle field) -- {len(deck)} characters:**

    {deck}

Neither is in POST.html's body. That is deliberate: an h1 inside the body means the
post opens by saying its own title twice.

## 2. The paste

1. Open `substack/POST.html` in a browser (double-click it).
2. Click in the text, **Ctrl-A**, **Ctrl-C**.
3. In the Substack editor, click into the body and **Ctrl-V**.
4. Skim for: the two reflowed lists (SS4 'Who this reaches', SS9 'Where one would
   point'), the block quotes, and the horizontal rules. Those are the four things
   a paste handler is most likely to mangle.

There are **no images** in this post, so the image-drop failure mode does not apply
and no assets/ fallback folder is needed.

## 3. What was converted, and why

- **Both tables were REFLOWED to lists, not imaged.** Measured rule from Day 199:
  image a table only when the GRID is the argument (numeric matrices). Both tables
  here are two-column label -> consequence maps, so a list carries the same content
  and is selectable, searchable and readable on a phone. Imaged tables are none of
  those things.
- **Element set:** {sorted(tags)} -- nothing else. 0 style attributes, 0 class
  attributes, asserted at build time.
- **Italic-inside-italic citations** (the Allen / Chisholm parentheticals) render as
  em -> roman -> em, which is the correct typography for a journal name inside an
  italic parenthetical, and is what the markdown was already doing.

## 4. Gauge

Unique-token set-diff, source markdown vs emitted HTML, computed in Python:

- tokens LOST : {len(lost)}  {sorted(lost) if lost else ''}
- tokens GAINED: {len(gained)}  {sorted(gained) if gained else ''}

## 5. Email clipping -- READ THIS BEFORE SENDING TO THE LIST

Gmail truncates any email over **102 KB of HTML** with a "[Message clipped]" link.

- essay body, plain text : {len(src.encode('utf-8')) / 1024:.1f} KB
- emitted HTML body      : {body_bytes / 1024:.1f} KB
- Substack's own email wrapper (header, footer, subscribe/share buttons, per-paragraph
  markup) adds an amount I **cannot measure from here**.

This post is 6,523 words. My Day-199 note put the trip point near 6,700 words -- but
that number was itself an ESTIMATE I never checked against a real clipped email, so
quoting it back is quoting my own guess. I do not know which side of the line this
lands on.

**The gauge that actually answers it, with an owner and a trigger:** send yourself the
test email from Substack before you hit send-to-all, scroll to the bottom, and look for
"[Message clipped] View entire message". If it is there, the fix is to split the post
or trim; if it is not, nothing else needs doing. The web version is unaffected either
way -- only the emailed copy clips. Tell me the answer and I will replace the estimate
above with a measurement.
"""
    (OUT / "PASTE-NOTES.md").write_text(notes, encoding="utf-8")

    print(f"title  : {title}")
    print(f"deck   : {len(deck)} chars")
    print(f"blocks : {len(out)}")
    print(f"tags   : {sorted(tags)}")
    print(f"body   : {body_bytes} bytes ({body_bytes/1024:.1f} KB)")
    print(f"LOST   : {len(lost)} {sorted(lost)}")
    print(f"GAINED : {len(gained)} {sorted(gained)}")


if __name__ == "__main__":
    build()
