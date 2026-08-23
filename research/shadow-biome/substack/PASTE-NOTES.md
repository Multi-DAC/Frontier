# PASTE NOTES -- THINGS NOT MEANT TO BE FOUND

## 1. The two fields, so the post does not announce its own name

**Title (paste into Substack's title field):**

    THINGS NOT MEANT TO BE FOUND

**Subtitle (paste into Substack's subtitle field) -- 137 characters:**

    A speculative essay on what shares the world with us — and on the possibility that some of it is unfound because finding it would cost us

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
- **Element set:** ['blockquote', 'br', 'code', 'em', 'h2', 'h3', 'hr', 'li', 'p', 'strong', 'ul'] -- nothing else. 0 style attributes, 0 class
  attributes, asserted at build time.
- **Italic-inside-italic citations** (the Allen / Chisholm parentheticals) render as
  em -> roman -> em, which is the correct typography for a journal name inside an
  italic parenthetical, and is what the markdown was already doing.

## 4. Gauge

Unique-token set-diff, source markdown vs emitted HTML, computed in Python:

- tokens LOST : 1  ['unfound']
- tokens GAINED: 0  

## 5. Email clipping -- READ THIS BEFORE SENDING TO THE LIST

Gmail truncates any email over **102 KB of HTML** with a "[Message clipped]" link.

- essay body, plain text : 38.2 KB
- emitted HTML body      : 41.6 KB
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
