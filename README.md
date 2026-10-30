# IG Poster Studio

A Claude skill from BuiltYoung that turns one product brief into a batch of finished Instagram posters. Use it to teach GTM: students bring their product details, and the class critiques the posters it produces.

- 12 layouts drawn from 2026 e-commerce ad research: hero, bold claim, problem→solution, us vs them, testimonial, listicle, feature callouts, before/after, lo-fi note, offer, stat, carousel
- 4 sizes: feed 4:5 (1080×1350), feed 3:4 (1080×1440), square 1:1, Story 9:16 (1080×1920) with safe zones built in
- Each run writes PNGs, `captions.csv` (caption and alt text for every poster), `qa.txt` (overflow, safe-zone and contrast warnings) and a contact sheet
- Honesty guardrails: an unverified testimonial is stamped SAMPLE, and a stat without a source is stamped SOURCE NEEDED

## Install in Claude
1. Download this repo as a ZIP. GitHub names the folder `ig-poster-studio-main`, so rename it to `ig-poster-studio`; the folder name must match the skill name. Re-zip the folder.
2. In claude.ai, go to Customize → Skills → + → Create skill → Upload a skill, and upload the ZIP.
3. Code execution must be on. On Free, Pro and Max it's under Settings → Capabilities. On Team and Enterprise, an owner turns it on in Organization settings.

Claude requires users to be 18+, so in class an instructor runs the skill on the students' briefs.

## Run it directly
```bash
pip install jinja2 playwright
python3 -m playwright install chromium
python3 scripts/render.py examples/studyfox/brief.json --out out/
# options: --sizes 4x5,9x16   --only hero,offer   --no-sheet
```

## Layout
| Path | What it holds |
|---|---|
| `SKILL.md` | Instructions Claude follows |
| `scripts/` | Renderer (`render.py`) and contact-sheet builder |
| `templates/` | One HTML template per layout |
| `references/` | Pattern library, Instagram specs, copy rules, brief schema |
| `fonts/` | Fonts under the SIL Open Font License; each one's licence is in `fonts/OFL-*.txt` |
| `examples/studyfox/` | Demo brief for a fictional product. Names, quotes and numbers are placeholders. |
