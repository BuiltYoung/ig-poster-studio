# Pattern library: 12 poster archetypes

Built from 2026 public research on Meta/Instagram e-commerce creative (sources at the end). There is no single public "Instagram poster database"; the closest primary source is Meta's free Ad Library (see "Finding real references" below). These archetypes are the recurring static formats that research and ad libraries keep surfacing, adapted for teen-built products (mostly apps, some physical goods).

Each entry: what it is, when to use it, the copy fields it takes, and a one-line **Lesson** for teaching the GTM idea behind it.

## Awareness (stop the scroll)

### bold-claim
Oversized type on a solid brand colour. One sharp point of view.
- Use for: cold audiences, contrarian takes, launch teasers.
- Copy: `headline` (the claim), `sub` (the payoff, names the product), `note` (url or availability).
- Lesson: a brand needs a point of view; a claim people can disagree with earns attention.
- Pitfall: a claim you can't back up. Keep it true and defensible.

### lofi-note
Handwritten notebook page, almost no branding. Reads as a post, not an ad.
- Use for: founder voice, "things I wish I knew", tips lists, top of funnel.
- Copy: `headline` (note title), `items` (3 to 5 short lines; `{"text":..., "done":false}` for unchecked), optional `sign`.
- Lesson: native-looking content gets read because it doesn't look like advertising.
- Pitfall: over-polishing it. Real notes are short, choppy and imperfect. Never copy a real app's interface (Notes-style is fine; Instagram/Facebook/WhatsApp screens are not).

### problem-solution
The pain, crossed out, then the product as the fix.
- Use for: products that solve a pain people already feel.
- Copy: `problem_label` (handwritten context), `problem`, `bridge` (handwritten, e.g. "so we built this"), `headline` (the solution), `sub`, `cta`. Image optional.
- Lesson: sell the problem before the product; people buy relief.

## Consideration (explain and compare)

### hero
Product front and centre (phone mockup for apps), headline, CTA.
- Use for: launch posts, retargeting, any time the product is visual.
- Copy: `headline`, `sub`, `badge` (e.g. New), `sticker` (price or "Free"), `cta`. Image required.
- Lesson: show the product being used; real screens beat abstract graphics.

### feature-callouts
Product in the middle, handwritten notes with arrows pointing at it.
- Use for: explaining what's inside without a wall of text.
- Copy: `headline`, `callouts` (2 to 4, each 2 to 5 words). Image required.
- Lesson: translate features into benefits a 15-year-old would say out loud.
- Pitfall: feature soup. Four callouts maximum.

### listicle
"3 reasons..." numbered list.
- Use for: scannable benefits, saves.
- Copy: `headline`, `items` (3 to 5; string or `{"title","sub"}`).
- Lesson: numbers promise a short, finite read, so people start reading.

### us-vs-them
Comparison table: your product vs the usual alternative.
- Use for: crowded categories, objection handling.
- Copy: `headline`, `us_label`, `them_label`, `rows` (3 to 5 of `{"label", "us", "them"}`; `true`/`false` draw ticks and crosses, strings show values).
- Lesson: control the comparison before the customer makes it. Compare against a behaviour ("rereading notes") rather than naming a competitor.
- Pitfall: rigged rows. Include one row where the alternative also wins; it builds trust.

### before-after
Two panels: life before vs after the product.
- Use for: time saved, money saved, results.
- Copy: `headline`, `before_label`, `before_big`, `before` (list), `after_label`, `after_big`, `after` (list). Optional `before_image`/`after_image` keys.
- Lesson: people buy the transformation, not the tool.
- Pitfall: invented numbers. Use the student's own measured example or describe it without numbers.

### carousel
Cover hook, one idea per slide, CTA slide. Renders one PNG per slide, all the same ratio.
- Use for: education, step-by-step, saves and shares.
- Slides: `{"role":"cover","headline","sub"}`, point slides `{"headline","body","image"?}`, `{"role":"cta","headline","sub","cta"}`. 5 to 8 slides.
- Lesson: teach something useful and the product earns trust; the product only appears near the end.

## Conversion (give a reason to act now)

### offer
Launch deal or discount on a dark background with a date sticker.
- Use for: launch week, early-bird pricing, limited codes.
- Copy: `kicker`, `headline` (the offer), `sub`, `badge` (dates), `fine` (terms), `cta`. Set `"show_image": true` to add the product.
- Lesson: urgency needs a real deadline; a fake countdown burns trust.

### testimonial
Big quote, stars, name and role.
- Use for: retargeting, landing-page-adjacent posts.
- Copy: `quote`, `name`, `role`, `stars`, `verified` (true only for a real, permissioned quote), optional `avatar` image key.
- Lesson: social proof works because it's someone other than the founder talking.
- Rule: unverified quotes render with a SAMPLE stamp. Never publish one.

### stat
One big number with a hand-drawn ring, a label and a source line.
- Use for: traction, credibility, a surprising fact about the problem.
- Copy: `number`, `label`, `sub`, `source` (required).
- Lesson: a number is only as credible as its source.

## Finding real references (class activity)
Meta's Ad Library (facebook.com/ads/library) shows ads currently running on Facebook and Instagram and can be searched without an account. Filter by media type (images) and active status. Have students pull 10 to 15 live ads from brands in their category and tag each with: format (which archetype above), hook, offer, CTA. Ads that have been running for a long time are the ones worth studying.

## Research basis
- Static images are a large share of what DTC brands run: one analysis of 67,852 ads from 106 brands found statics were 55.6% of all ads and 64.8% for DTC brands (segwise.ai/blog/dtc-ad-creative-hooks, citing Curtis Howland).
- Five recurring Meta formats for DTC: Us vs Them, Problem-Solution, Product Demo, Testimonials, Reasons Why (segwise.ai/blog/100m-meta-ads-5-formats-dtc).
- Common static types: text overlay, product hero, before/after, testimonial cards, problem-agitate-solution, listicle, lifestyle (sovran.ai/blog/static-ads-examples).
- Notes-app style is a static, top-to-mid-funnel native format (motionapp.com/library/formats/notes-app); it fails when over-produced (creativeos.beehiiv.com/p/123-when-native-tries-too-hard). Native posts may look like Notes, email or a text thread but not a Facebook, Instagram or WhatsApp screen (admakeai.com/blog/static-ads).
- Software ads: demo the outcome, avoid "feature soup" (flowjam.com/blog/best-saas-ads-2026-examples-teardowns).
- Products shown in use convert better than isolated product shots (imagine.art/business/resources/ecommerce-marketing-trends).
- Fake testimonials and fake authenticity break Meta's ad standards and FTC native-advertising guidance regardless of format (adlibrary.com/guides/native-image-ads-guide).
- Meta Ad Library usage (segwise.ai/blog/meta-ad-library-competitor-research; postplanify.com/blog/meta-ads-library).
