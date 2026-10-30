# Instagram specs used by the renderer (checked Oct 2026)

| Size key | Pixels | Use | Safe area the templates keep text inside |
|---|---|---|---|
| `4x5` (default) | 1080 × 1350 | Feed posts and feed ads | 34 px in from each side, so the 3:4 profile-grid crop never cuts text |
| `3x4` | 1080 × 1440 | Feed posts that should fill the profile grid exactly | Whole canvas |
| `1x1` | 1080 × 1080 | Square feed posts | 135 px in from each side (3:4 grid crop) |
| `9x16` | 1080 × 1920 | Stories | Top 270 px (14%), bottom 384 px (20%), sides 65 px |

Why: Instagram's profile grid shows every post as a 3:4 thumbnail (since January 2025) and 3:4 can now be uploaded natively, while 4:5 remains the most common feed and ad size (dreampixelforge.com/blog/instagram-post-size; nealschaffer.com/instagram-post-size; instantdm.com/blog/instagram-post-size-guide-2026). A 3:4 tile is narrower than 4:5 relative to its height, so 4:5 and 1:1 posts lose their sides on the grid: about 34 px per side for 4:5 and 135 px per side for 1:1.

Stories: Meta's guidance for Story ads is to keep text and logos out of roughly the top 14% and bottom 20% (inro.social/tools/instagram-reels-safe-zone-checker; coinis.com/how-to/best-text-placement-for-facebook-ad). **Reels ads are stricter: bottom 35%.** If a 9:16 poster will run as a Reels ad, move key text up or re-check it against a 35% bottom margin.

Carousels: use one ratio for every slide (skedsocial.com/blog/best-instagram-image-and-video-size-recommendations). The renderer does this automatically.

## Text on images
- Short on-image text: 6 to 8 words for the headline (straightnorth.com/blog/meta-ads-creative-best-practices-that-convert).
- Meta dropped the old 20% text rule, but text-heavy images still tend to underdeliver (adstellar.ai/blog/image-ad-design). Put detail in the caption.
- Minimum readable size on a phone: the templates never go below 20 px on a 1080-wide canvas; most body text is 32 px or more.

## Format notes
- PNG output (best for text and flat colour). 1080 px wide means Instagram doesn't need to resize.
- Carousels led engagement in Buffer's 2026 analysis of 52M+ posts: 114% more engagement than single images (moneris.com/en/blog/posts/growth-strategy/why-you-need-carousels-for-your-social-posts). Figures vary a lot between studies; treat as direction, not a promise.
