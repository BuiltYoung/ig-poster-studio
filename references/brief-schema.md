# brief.json schema

```jsonc
{
  "sheet_note": "optional line printed under the contact-sheet title",
  "brand": {
    "name": "Studyfox",
    "logo_text": "studyfox",          // wordmark used when no logo image
    "logo": "assets/logo.png",         // optional, transparent PNG, shown 56 px tall
    "handle": "@studyfox.app",
    "font_pair": "grotesk",            // grotesk | editorial | friendly | tech | loud
    "palette": {"paper": "#F4F2FF", "ink": "#1C1A3A", "primary": "#FF5B2E", "accent": "#C9F04D", "muted": "#6E6A8C"},
    "alt_palettes": [ { ...same keys... } ]   // optional, for colour variants
  },
  "product": {
    "name": "Studyfox",
    "kind": "app",                     // app = phone mockup; anything else = rounded photo
    "one_liner": "...",
    "price": "Free",
    "images": {"quiz": "assets/screen-quiz.png"}   // keys used by posts
  },
  "defaults": {"sizes": ["4x5"], "cta": "Try it free", "palettes": [0]},
  "posts": [
    {
      "id": "hero",                    // used in file names
      "archetype": "hero",
      "image": "quiz",                 // key from product.images
      "sizes": ["4x5", "9x16"],        // optional, overrides defaults
      "palettes": "all",               // or a list of indexes: 0 = main palette, 1+ = alt_palettes
      "copy": { ...archetype fields... },
      "variants": [ {"copy": {"headline": "alt hook"}} ],   // optional; each variant = another poster
      "caption": "...",
      "alt": "..."
    }
  ]
}
```

## Font pairs
- `grotesk` Bricolage Grotesque condensed + Inter: loud, modern, startup
- `editorial` Instrument Serif + Inter: calm, premium, fashion, books
- `friendly` Plus Jakarta Sans: approachable, kids, edtech
- `tech` Space Grotesk: dev tools, AI, fintech
- `loud` Anton caps + Inter: sport, drops, sales

## Palette
Five colours. `paper` background, `ink` text, `primary` the brand colour (large areas, CTAs), `accent` small highlights and stickers, `muted` secondary text. Text colour on primary/accent is picked automatically for contrast. Keep ink on paper at 4.5:1 or better (the renderer warns).

## Copy fields per archetype
| archetype | fields |
|---|---|
| hero | headline, sub, badge, sticker, cta (image) |
| bold-claim | headline, sub, note, cta |
| problem-solution | problem_label, problem, bridge, headline, sub, cta (image optional) |
| us-vs-them | headline, us_label, them_label, rows[{label, us, them}], cta |
| testimonial | quote, name, role, stars, verified, avatar, cta |
| listicle | headline, items[str or {title, sub}], cta |
| feature-callouts | headline, callouts[2-4], cta (image) |
| before-after | headline, before_label, before_big, before[], after_label, after_big, after[], before_image, after_image, cta |
| lofi-note | headline, items[str or {text, done}], sign |
| offer | kicker, headline, sub, badge, fine, cta; post-level show_image: true (image) |
| stat | number, label, sub, source, cta |
| carousel | post-level slides[]: cover {role, headline, sub, swipe}, point {headline, body, image, n, unnumbered}, cta {role, headline, sub, cta} |

## Output names
`NN_<id>_v<variant>_p<palette>_<size>[_sNN].png`, e.g. `01_hero_v1_p2_9x16.png`.
