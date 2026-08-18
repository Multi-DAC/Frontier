#!/usr/bin/env python3
"""
build_substack.py — turn dossier.html into something that survives a Substack paste.

The dossier is designed HTML: 47 tables, custom CSS, coloured tier badges, a
two-column grid, cards with shadows. Substack's paste handler keeps almost none
of that. Measured behaviour (Day 139, publishing *The Curvature of Good and Evil*):

  * <img> with a base64 data URI  -> TRANSFERS (may need a second paste)
  * rendered math                 -> does NOT transfer
  * tables                        -> do NOT transfer cleanly
  * everything in a <style> block -> gone

So the rule here is: emit ONLY the element set Substack renders natively
(h2/h3, p, strong/em, ul/li, blockquote, hr, code, img), and decide per table
whether the grid is load-bearing.

  grid load-bearing (3 tables)  -> screenshot at the dossier's own CSS, embed as PNG
  grid incidental  (44 tables)  -> reflow into bullet lists / labelled paragraphs

That is the whole trick. 47 imaged tables would be unreadable on a phone and
unsearchable everywhere; 3 is a figure count.

Outputs into substack/:
  POST.html      self-contained, open in a browser, Ctrl-A Ctrl-C, paste
  assets/        every image also on disk, numbered in paste order, as a fallback
  PASTE-NOTES.md the checklist
"""

import base64
import io
import json
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dossier.html"
OUT = ROOT / "substack"
ASSETS = OUT / "assets"

# Substack's content column renders ~1200 px wide on desktop retina.
IMG_WIDTH = 1456
JPEG_Q = 82

# ---------------------------------------------------------------- inline text


KEEP_INLINE = {"b", "strong", "i", "em", "br", "a", "code", "sup", "sub"}


def inline(node) -> str:
    """Render a node's children keeping only inline tags Substack honours.

    Everything else (span.mono, span.tier, span.dl, span.coord) collapses to its
    text, except .mono and .tier which become <code> — Substack keeps <code>, and
    it is the only way left to say 'this is a literal' once the CSS is gone.
    """
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(esc(str(c)))
        elif isinstance(c, Tag):
            if c.name in KEEP_INLINE:
                if c.name == "br":
                    out.append("<br>")
                elif c.name == "a":
                    out.append(f'<a href="{c.get("href", "")}">{inline(c)}</a>')
                else:
                    out.append(f"<{c.name}>{inline(c)}</{c.name}>")
            else:
                cls = set(c.get("class") or [])
                inner = inline(c)
                if {"mono", "tier"} & cls:
                    out.append(f"<code>{inner}</code>")
                elif "rk" in cls:
                    # rank badge: CSS supplied the gap, so the text must now
                    out.append(f"{inner} · ")
                else:
                    out.append(inner)
    return collapse(" ".join("".join(out).split(" ")))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def collapse(s: str) -> str:
    return re.sub(r"[ \t\n]+", " ", s).strip()


def text_of(node) -> str:
    return collapse(node.get_text(" ", strip=True))


# ------------------------------------------------------------ table rendering

TABLE_CSS = """
body{margin:0;background:#fff;font:15px/1.55 "Iowan Old Style",Georgia,serif;color:#16181d}
table{border-collapse:collapse;width:100%;font-size:.95rem}
th,td{text-align:left;padding:9px 13px;border-bottom:1px solid #d8dce3;vertical-align:top}
th{font-weight:600;background:#f2f3f6;border-bottom:1.5px solid #c3c8d1}
td.num,th.num{text-align:right;font-family:Consolas,monospace;font-size:.9em}
.mono{font-family:Consolas,monospace}
.dl{color:#5d646f;font-size:.86rem}
.wrap{padding:14px 18px}
caption{caption-side:top;text-align:left;font-weight:700;padding:0 13px 10px;font-size:1rem}
"""


def shoot_tables(jobs, width=980):
    """Screenshot each (slug, caption, table_html) with the dossier's own styling."""
    from playwright.sync_api import sync_playwright

    made = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": 600}, device_scale_factor=2
        )
        for slug, caption, html in jobs:
            doc = (
                "<!doctype html><meta charset='utf-8'><style>"
                + TABLE_CSS
                + "</style><div class='wrap'>"
                + (f"<div style='font-weight:700;padding:0 0 10px'>{caption}</div>" if caption else "")
                + html
                + "</div>"
            )
            page.set_content(doc)
            shot = page.locator(".wrap").screenshot(type="png")
            made[slug] = shot
        browser.close()
    return made


# ------------------------------------------------------------- table handlers


def hdr_cells(table):
    first = table.find("tr")
    return [text_of(c).lower() for c in first.find_all(["th", "td"])]


def classify(table) -> str:
    h = hdr_cells(table)
    if h[:2] == ["leg", "hypothesis"]:
        return "img:legs"
    if h[:2] == ["#", "fault"]:
        return "img:ten"
    if h[:1] == ["fault"] and any("suppressed" in x for x in h):
        return "img:suppressed"
    if h[:3] == ["leg", "status", "measured"]:
        return "measurements"
    if h[:1] == ["role"]:
        return "lorepair"
    if h[:1] == ["artifact"]:
        return "twocol"
    if len(h) == 2:
        return "ladder"
    return "twocol"


def rows_of(table, skip_header=True):
    trs = table.find_all("tr")
    return trs[1:] if skip_header else trs


def render_measurements(table) -> str:
    """leg | status | measured  ->  bullet list, one leg per bullet."""
    items = []
    for tr in rows_of(table):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 3:
            continue
        leg, status, meas = inline(tds[0]), text_of(tds[1]), inline(tds[2])
        items.append(f"<li><strong>{leg}</strong> — <strong>{status}</strong><br>{meas}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def render_lorepair(table) -> str:
    """role | site | sighted | blind | evidence  ->  two labelled paragraphs.

    The 'observer-density matched, >=100 km away, identical rubric' gloss is
    identical in all 30 of these and is stated once in the section intro instead.
    """
    out = []
    for tr in rows_of(table):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 5:
            continue
        role = text_of(tds[0]).split("observer-density")[0].strip()
        site = text_of(tds[1])
        sighted, blind = text_of(tds[2]), text_of(tds[3])
        ev = inline(tds[4])
        out.append(
            f"<p><strong>{esc(role)} · {esc(site)}</strong> — sighted "
            f"<code>{esc(sighted)}</code>, blind <code>{esc(blind)}</code><br>"
            f"<em>{ev}</em></p>"
        )
    return "".join(out)


def render_ladder(table) -> str:
    items = []
    for tr in rows_of(table, skip_header=False):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 2:
            continue
        items.append(f"<li><code>{text_of(tds[0])}</code> — {inline(tds[1])}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def render_twocol(table) -> str:
    items = []
    for tr in rows_of(table):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 2:
            continue
        items.append(f"<li><strong>{inline(tds[0])}</strong> — {inline(tds[1])}</li>")
    return "<ul>" + "".join(items) + "</ul>"


# ------------------------------------------------------------------ the walk


class Builder:
    def __init__(self, soup):
        self.soup = soup
        self.blocks = []
        self.images = []  # (order, filename, bytes, mime, alt, caption)
        self.table_jobs = []
        self.table_slots = {}
        self.dropped_gloss = 0
        self.title = ""
        self.subtitle = ""

    def emit(self, html):
        if html:
            self.blocks.append(html)

    def walk(self, node):
        for child in node.children:
            if isinstance(child, NavigableString):
                continue
            if not isinstance(child, Tag):
                continue
            self.handle(child)

    def handle(self, el):
        name = el.name
        cls = set(el.get("class") or [])

        if name in ("div", "section", "header"):
            if "banner" in cls:
                inner = "".join(f"<p>{inline(p)}</p>" for p in el.find_all("p", recursive=False))
                self.emit(f"<blockquote>{inner}</blockquote>")
                return
            if "site" in cls:
                self.emit("<hr>")
            self.walk(el)
            return

        if name in ("h1", "h2", "h3", "h4"):
            txt = inline(el)
            if name == "h1":
                # the document title belongs in Substack's own title field, not
                # in the body — pasting it makes the post start with its own name
                self.title = text_of(el)
                return
            level = {"h2": "h2", "h3": "h3", "h4": "h3"}[name]
            parent_cls = set((el.parent.get("class") or [])) if el.parent else set()
            if "hd" in parent_cls:
                level = "h2"  # site titles arrive as h3 inside .hd
            elif re.match(r"^H[123] ·", text_of(el)):
                # the three per-site leg headings sit UNDER 'History, lore…' and
                # Substack has only three heading levels — demote to bold prose
                self.emit(f"<p><strong>{txt}</strong></p>")
                return
            self.emit(f"<{level}>{txt}</{level}>")
            return

        if name == "p":
            txt = inline(el)
            if "sub" in cls and not self.subtitle:
                # The deck is 58 words — far past what Substack's subtitle field
                # holds. Keep it in the body as the opening paragraph and hand
                # PASTE-NOTES a short subtitle cut from its own first clause.
                self.subtitle = text_of(el)
            if txt:
                self.emit(f"<p>{txt}</p>")
            return

        if name == "figure":
            self.handle_figure(el)
            return

        if name == "table":
            self.handle_table(el)
            return

        if name in ("ul", "ol"):
            items = "".join(f"<li>{inline(li)}</li>" for li in el.find_all("li", recursive=False))
            self.emit(f"<{name}>{items}</{name}>")
            return

        if name == "footer":
            self.emit("<hr>")
            self.walk(el)
            return

        if name in ("style", "script", "meta", "title", "link"):
            return

        self.walk(el)

    def handle_figure(self, fig):
        img = fig.find("img")
        cap = fig.find("figcaption")
        if img is None:
            return
        src = img.get("src", "")
        m = re.match(r"data:image/(\w+);base64,(.+)$", src, re.S)
        if not m:
            return
        mime, data = m.group(1), base64.b64decode(m.group(2))
        data, mime = normalise_image(data, mime)
        n = len(self.images) + 1
        alt = img.get("alt", "")
        fname = f"{n:02d}_{slugify(alt) or 'figure'}.{'jpg' if mime == 'jpeg' else mime}"
        caption = inline(cap) if cap else ""
        self.images.append((n, fname, data, mime, alt, caption))
        b64 = base64.b64encode(data).decode()
        self.emit(
            f'<p><img alt="{esc(alt)}" src="data:image/{mime};base64,{b64}"></p>'
            + (f"<p><em>{caption}</em></p>" if caption else "")
        )

    def handle_table(self, table):
        kind = classify(table)
        if kind.startswith("img:"):
            slug = kind.split(":", 1)[1]
            caption = ""
            prev = table.find_previous(["h2", "h3"])
            if prev is not None:
                caption = text_of(prev)
            self.table_jobs.append((slug, caption, str(table)))
            token = f"@@TABLE:{slug}@@"
            self.table_slots[slug] = len(self.blocks)
            self.emit(token)
            return
        if kind == "measurements":
            self.emit(render_measurements(table))
        elif kind == "lorepair":
            self.dropped_gloss += 1
            self.emit(render_lorepair(table))
        elif kind == "ladder":
            self.emit(render_ladder(table))
        else:
            self.emit(render_twocol(table))


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48]


def normalise_image(data: bytes, mime: str):
    """Cap width at IMG_WIDTH and re-encode as JPEG. Substack recompresses anyway;
    the point is keeping the clipboard payload survivable."""
    from PIL import Image

    im = Image.open(io.BytesIO(data))
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    if im.width > IMG_WIDTH:
        h = round(im.height * IMG_WIDTH / im.width)
        im = im.resize((IMG_WIDTH, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    return buf.getvalue(), "jpeg"


# ---------------------------------------------------------------------- main


PAGE_CSS = """
body{margin:0;background:#fff;color:#16181d;
     font:18px/1.65 "Iowan Old Style",Georgia,"Times New Roman",serif}
.paste{max-width:760px;margin:0 auto;padding:40px 24px 120px}
h1{font-size:2rem;line-height:1.2}
h2{font-size:1.45rem;margin:2em 0 .4em}
h3{font-size:1.1rem;margin:1.5em 0 .3em}
img{width:100%;height:auto;display:block}
code{font-family:Consolas,"DejaVu Sans Mono",monospace;font-size:.86em;
     background:#f2f3f6;padding:1px 5px;border-radius:3px}
blockquote{margin:1.4em 0;padding:2px 0 2px 20px;border-left:3px solid #16181d}
blockquote p{margin:.5em 0}
ul{padding-left:1.3em}
li{margin:.45em 0}
hr{border:0;border-top:1px solid #d8dce3;margin:3em 0}
.chrome{max-width:760px;margin:0 auto;padding:18px 24px;background:#fff5ee;
        border-bottom:1px solid #e6c3aa;font:14px/1.5 system-ui,sans-serif;color:#7a3d12}
"""

BANNER = """<div class='chrome'><b>PASTE ME.</b> Click anywhere below the line, then
Ctrl-A, Ctrl-C, and paste into the Substack editor. Everything above the line is
scaffolding and is excluded from the selection. If figures do not come through on
the first paste, undo and paste a second time — that is the known behaviour, not a
failure. Fallback: <code>substack/assets/</code> holds every image numbered in
paste order.</div>"""


NOTES = """# Substack paste — Place-Threshold Screen

Built by `code/build_substack.py` from `dossier.html`. Rebuild any time the
dossier changes; nothing here is hand-edited.

## Do this

1. Open **`substack/POST.html`** in a browser (double-click it).
2. Click anywhere in the body, **Ctrl-A**, **Ctrl-C**.
3. New Substack post → click in the body → **Ctrl-V**.
4. **Check the images came through.** If any are missing: Ctrl-Z, paste again.
   The first paste dropping images is known behaviour (Day 139, *The Curvature
   of Good and Evil*), and the second paste usually carries them.
5. Anything still missing → drag it in from `substack/assets/`, numbered in
   paste order.

## The title field — do NOT paste this, type it

The document title is deliberately **not** in the paste body, so the post does
not open by announcing its own name.

**Title:** {title}

**Subtitle** — the dossier's deck is {deck_words} words, which Substack's subtitle
field will not hold, so it stays in the body as the opening paragraph. Type one
of these instead:

- A CONUS-wide physics screen for ten dilatant faults, with the folklore held out
  until the physics was frozen — and all three lore legs came back NOT SUPPORTED.
- Ten faults, four geophysical layers each, three pre-registered lore experiments,
  and the null result printed in full.

## What changed from the dossier, and why

| | dossier | this |
|---|---|---|
| tables | 47 | 3 (as images) + 44 reflowed to text |
| CSS | ~60 rules | none — Substack strips every one |
| tier badges | coloured `<span>` | `code` spans: `T0`, `NT1`, `HT3` |
| two-column grid | `.cols` | linear, because phones |
| banners | `.banner` cards | blockquotes |
| plates | 10 base64 JPEGs | same, capped at 1456 px |

The three tables kept as images are the ones where the grid *is* the argument —
the three lore legs at a glance, the ten with their five scoring terms, and the
nine faults suppressed by the 100 km rule. The other 44 are two- and three-column
lists, and they read better as bullets than as pictures: searchable, selectable,
legible on a phone, and they don't cost a page-load each.

## ⚠ Email will almost certainly clip this

{words:,} words, {images} images, ~{text_kb:.0f} KB of text before Substack's own
markup. Gmail truncates any email over 102 KB with a *"[Message clipped] View
entire message"* link. This post goes over. The web version is unaffected.

Three ways out, your call:

- **Ship it as one.** The clip link works; readers who care click through.
- **Split it.** Framing + the three legs + the ten table as post 1, then the ten
  dossiers as post 2 (or as a 10-part series). I can cut the build either way in
  a few minutes — the script already knows where the site boundaries are.
- **Web-only.** Publish with email delivery off and announce it in a short note.

## Assets, in paste order

| # | file | size | what |
|---|---|---|---|
{assets}
"""


def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    wrap = soup.find("div", class_="wrap")

    b = Builder(soup)
    b.walk(wrap)

    # render the three grid-load-bearing tables
    shots = shoot_tables(b.table_jobs)
    for slug, png in shots.items():
        png2, mime = normalise_image(png, "png")
        n = len(b.images) + 1
        fname = f"{n:02d}_table_{slug}.jpg"
        b.images.append((n, fname, png2, mime, f"table: {slug}", ""))
        b64 = base64.b64encode(png2).decode()
        token = f"@@TABLE:{slug}@@"
        idx = b.blocks.index(token)
        b.blocks[idx] = f'<p><img alt="table: {slug}" src="data:image/{mime};base64,{b64}"></p>'

    # the gloss stripped from 30 identical decoy cells, stated once instead
    for i, blk in enumerate(b.blocks):
        if blk == "<h2>The ten dossiers</h2>":
            b.blocks.insert(
                i + 1,
                "<p><em>Each site is printed with its matched decoy: a fault "
                "matched on observer density, at least 100 km away, scored under "
                "the identical rubric by the same scorers. <strong>sighted</strong> "
                "is the original tier; <strong>blind</strong> is the tier assigned "
                "by scorers who could not see which site was which. The evidence "
                "text is verbatim from the frozen result file.</em></p>",
            )
            break

    OUT.mkdir(exist_ok=True)
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    ASSETS.mkdir()
    for n, fname, data, mime, alt, cap in b.images:
        (ASSETS / fname).write_bytes(data)

    body = "\n".join(b.blocks)
    page = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Place-Threshold Screen — Substack paste copy</title>"
        f"<style>{PAGE_CSS}</style></head><body>{BANNER}"
        f"<div class='paste'>{body}</div></body></html>"
    )
    (OUT / "POST.html").write_text(page, encoding="utf-8")

    # stats
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    stats = {
        "blocks": len(b.blocks),
        "images": len(b.images),
        "tables_imaged": len(shots),
        "tables_reflowed": 47 - len(shots),
        "words": words,
        "post_bytes": len(page.encode()),
        "text_only_bytes": len(re.sub(r'src="data:[^"]+"', 'src="X"', page).encode()),
    }
    (OUT / "_build_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    asset_lines = "\n".join(
        f"| {n:02d} | `{fname}` | {len(data)/1024:.0f} KB | {alt} |"
        for n, fname, data, mime, alt, cap in b.images
    )
    (OUT / "PASTE-NOTES.md").write_text(
        NOTES.format(
            title=b.title,
            deck_words=len(b.subtitle.split()),
            words=stats["words"],
            images=stats["images"],
            text_kb=stats["text_only_bytes"] / 1024,
            assets=asset_lines,
        ),
        encoding="utf-8",
    )
    print(json.dumps(stats, indent=2))
    for n, fname, data, mime, alt, cap in b.images:
        print(f"  {n:02d}  {len(data)/1024:7.0f} KB  {fname}")


if __name__ == "__main__":
    main()
