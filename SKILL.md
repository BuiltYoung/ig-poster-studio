---
name: ig-poster-studio
description: Batch-produce Instagram posters (feed 4:5, 3:4, 1:1, Stories 9:16 and carousels) for a student's product from one short brief, using 12 layouts drawn from 2026 e-commerce ad research. Use when asked to make Instagram or social posters, ad creatives, a launch content batch, or to teach GTM creative with real examples.
---

# IG Poster Studio

Turns one product brief into dozens of finished, on-brand PNG posters plus captions, alt text and a labelled contact sheet. Built for BuiltYoung GTM classes: an instructor runs it, students supply their product details and then critique the batch.

Claude writes the copy and picks the layouts; `scripts/render.py` renders every poster with real fonts in headless Chromium, so text is always exact and nothing is AI-drawn.

## Workflow

### 1. Intake (ask only for what's missing)
- Product name, one-line description, who it's for, the problem it solves
- 3 concrete benefits; price or offer, with dates if any
- Proof the student actually has: real user quotes (with permission), real numbers with a source
- Brand: colours (5 hex: paper, ink, primary, accent, muted) or a vibe to pick from; handle; logo file if any
- Images: app screenshots or product photos (portrait screenshots work best)

If there are no brand colours, propose a palette and check `qa.txt` for contrast warnings after the first render.

### 2. Pick angles
Read `references/pattern-library.md`. Choose archetypes by goal: awareness (bold-claim, lofi-note, problem-solution), consideration (hero, feature-callouts, listicle, carousel, us-vs-them, before-after), conversion (offer, testimonial, stat). A launch batch usually uses 8 to 12 of the 12.

### 3. Write the copy
Follow `references/copy-rules.md`. Non-negotiables:
- Headline 8 words or fewer, one idea per poster. Long copy goes in the caption.
- Never invent testimonials, reviews, user counts or statistics. Quotes need `"verified": true` only when real and permissioned; otherwise the poster is stamped SAMPLE. A `stat` without `source` is stamped SOURCE NEEDED.
- Never imitate Instagram, Facebook or WhatsApp interface screens. The lo-fi note style is fine.
- Claims must be true for the product today (no "#1", no "AI-powered" unless it is).

### 4. Build the brief
Write `brief.json` following `references/brief-schema.md` (field list per archetype). Start from `examples/studyfox/brief.json`. Put image files next to the brief and reference them by relative path.

### 5. Render
```bash
python3 <skill-dir>/scripts/render.py brief.json --out out/
# options: --sizes 4x5,9x16   --only hero,offer   --no-sheet
```
Needs Python 3, `jinja2` and `playwright` with Chromium. If missing:
`pip install jinja2 playwright --break-system-packages && python3 -m playwright install chromium`

### 6. QA (always)
- Read `out/qa.txt`. Fix every overflow (shorten the copy, don't shrink the design), safe-zone and contrast note, then re-render.
- Open `out/contact_sheet.png` and look at it. Open at least 3 full-size PNGs, including any 9:16.
- Check every claim on every poster against what the student told you.

### 7. Deliver
Send the contact sheet, a zip of `out/png/`, and `out/captions.csv` (file, headline, caption, alt text). For class, walk through the contact sheet using the "Lesson" line for each archetype in the pattern library.

## Volume
Output count = posts × variants × palettes × sizes (carousels add one PNG per slide). Example: 12 posts × 2 headline variants × 2 palettes × 2 sizes = 96 posters from one brief. Use `variants` to A/B test hooks, not to pad: each variant should test a different angle.

## Files
- `scripts/render.py` renderer; `scripts/contact_sheet.py` review sheet
- `templates/` one HTML template per archetype, shared `base.html` (fonts, palette tokens, auto-fit, QA) and `_macros.html`
- `fonts/` open-licence fonts (OFL) bundled so output is identical everywhere
- `references/` pattern library, specs, copy rules, brief schema
- `examples/studyfox/` fictional demo brief and screenshots
