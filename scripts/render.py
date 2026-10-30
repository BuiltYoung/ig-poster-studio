#!/usr/bin/env python3
"""Batch-render Instagram posters from a JSON brief.

Usage:
  python3 scripts/render.py BRIEF.json --out OUTDIR [--sizes 4x5,9x16] [--only hero,offer] [--no-sheet]

Output in OUTDIR:
  png/            one PNG per poster (carousels: one PNG per slide)
  html/           the HTML each PNG was rendered from (edit + re-render if needed)
  captions.csv    file, post id, archetype, size, headline, caption, alt text
  qa.txt          warnings: overflowing text, missing sources, low contrast, long headlines
  contact_sheet.png  every poster on one labelled sheet (for review / teaching)
"""
import argparse, csv, json, pathlib, re, sys, copy as _copy

SKILL = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
FONTS = SKILL / "fonts"

# Canvas sizes. ss = side crop of the 3:4 profile-grid thumbnail; st/sb = Story UI zones.
SIZES = {
    "4x5":  dict(W=1080, H=1350, st=0,   sb=0,   ss=34,  m=72, label="Feed 4:5"),
    "3x4":  dict(W=1080, H=1440, st=0,   sb=0,   ss=0,   m=72, label="Feed 3:4"),
    "1x1":  dict(W=1080, H=1080, st=0,   sb=0,   ss=135, m=44, label="Square 1:1"),
    "9x16": dict(W=1080, H=1920, st=270, sb=384, ss=65,  m=24, label="Story 9:16"),
}

FONT_PAIRS = {
    # display family, weight, tracking, line-height, transform, stretch | body family
    "grotesk":   dict(display="'Bricolage'", dw=800, track="-0.015em", lh=0.92, tt="none", stretch="75%", body="'InterV'"),
    "editorial": dict(display="'InstrumentSerif'", dw=400, track="-0.02em", lh=0.95, tt="none", stretch="100%", body="'InterV'"),
    "friendly":  dict(display="'Jakarta'", dw=800, track="-0.04em", lh=0.98, tt="none", stretch="100%", body="'Jakarta'"),
    "tech":      dict(display="'SpaceG'", dw=700, track="-0.04em", lh=0.95, tt="none", stretch="100%", body="'SpaceG'"),
    "loud":      dict(display="'Anton'", dw=400, track="0em", lh=0.98, tt="uppercase", stretch="100%", body="'InterV'"),
}

ARCHETYPES = ["hero", "bold-claim", "problem-solution", "us-vs-them", "testimonial", "listicle",
              "feature-callouts", "before-after", "lofi-note", "offer", "stat", "carousel"]


# ---------- colour helpers ----------
def _rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lum(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def on_color(bg, ink, paper):
    """Pick ink or paper (whichever reads better) for text on bg."""
    return ink if contrast(bg, ink) >= contrast(bg, paper) else paper


def build_palette(p):
    p = dict(p)
    p.setdefault("muted", p["ink"])
    for k in ("primary", "accent", "ink"):
        p["on_" + k] = on_color(p[k], p["ink"], p["paper"])
    return p


# ---------- brief expansion ----------
def deep_merge(base, over):
    out = _copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


_HYPHEN = re.compile(r"(?<=\w)-(?=\w)")


def keep_hyphens(v):
    """Stop lines breaking at hyphens ("30-|minute") by wrapping them in word joiners."""
    if isinstance(v, str):
        return _HYPHEN.sub("⁠-⁠", v)
    if isinstance(v, list):
        return [keep_hyphens(x) for x in v]
    if isinstance(v, dict):
        return {k: (keep_hyphens(x) if k not in ("image", "avatar", "role", "id") else x) for k, x in v.items()}
    return v


def expand_jobs(brief, sizes_override=None, only=None):
    brand = brief["brand"]
    palettes = [brand["palette"]] + list(brand.get("alt_palettes", []))
    defaults = brief.get("defaults", {})
    jobs = []
    for n, post in enumerate(brief["posts"], 1):
        arch = post["archetype"]
        if arch not in ARCHETYPES:
            raise SystemExit(f"Unknown archetype '{arch}' in post {post.get('id', n)}. Use one of: {', '.join(ARCHETYPES)}")
        if only and arch not in only:
            continue
        variants = post.get("variants") or [{}]
        use_pal = post.get("palettes", defaults.get("palettes", [0]))
        if use_pal == "all":
            use_pal = list(range(len(palettes)))
        sizes = sizes_override or post.get("sizes") or defaults.get("sizes", ["4x5"])
        for vi, var in enumerate(variants, 1):
            merged = deep_merge(post, var)
            merged.pop("variants", None)
            for key in ("copy", "slides"):
                if key in merged:
                    merged[key] = keep_hyphens(merged[key])
            for pi in use_pal:
                for size in sizes:
                    if size not in SIZES:
                        raise SystemExit(f"Unknown size '{size}'. Use one of: {', '.join(SIZES)}")
                    base = f"{n:02d}_{post.get('id', arch)}_v{vi}_p{pi + 1}_{size}"
                    slides = merged.get("slides") if arch == "carousel" else [None]
                    for si, slide in enumerate(slides or [None], 1):
                        name = base + (f"_s{si:02d}" if arch == "carousel" else "")
                        jobs.append(dict(name=name, post=merged, arch=arch, size=size, pal=palettes[pi],
                                         slide=slide, si=si, sc=len(slides or [None])))
    return jobs


# ---------- QA on copy ----------
def copy_checks(job):
    w = []
    c = job["post"].get("copy", {})
    hl = (job["slide"] or {}).get("headline") if job["slide"] else c.get("headline")
    if hl and len(hl.split()) > 9:
        w.append(f"headline has {len(hl.split())} words; aim for 8 or fewer: '{hl}'")
    if job["arch"] == "stat" and not c.get("source"):
        w.append("stat poster has no source; rendered with a SOURCE NEEDED tag")
    if job["arch"] == "testimonial" and not c.get("verified"):
        w.append("testimonial not marked verified:true; rendered with a SAMPLE tag. Use only real, permissioned quotes")
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sizes", help="comma list, overrides the brief, e.g. 4x5,9x16")
    ap.add_argument("--only", help="comma list of archetypes to render")
    ap.add_argument("--no-sheet", action="store_true")
    a = ap.parse_args()

    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        raise SystemExit("Missing jinja2: pip install jinja2 --break-system-packages")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Missing playwright: pip install playwright --break-system-packages && python3 -m playwright install chromium")

    brief_path = pathlib.Path(a.brief).resolve()
    brief = json.loads(brief_path.read_text())
    brief_dir = brief_path.parent
    out = pathlib.Path(a.out).resolve()
    (out / "png").mkdir(parents=True, exist_ok=True)
    (out / "html").mkdir(parents=True, exist_ok=True)

    sizes = a.sizes.split(",") if a.sizes else None
    only = set(a.only.split(",")) if a.only else None
    jobs = expand_jobs(brief, sizes, only)
    if not jobs:
        raise SystemExit("Nothing to render.")

    brand = brief["brand"]
    fp = FONT_PAIRS.get(brand.get("font_pair", "grotesk"))
    if not fp:
        raise SystemExit(f"Unknown font_pair. Use one of: {', '.join(FONT_PAIRS)}")
    product = brief.get("product", {})
    images = {k: (brief_dir / v).resolve().as_uri() for k, v in product.get("images", {}).items()}
    logo = (brief_dir / brand["logo"]).resolve().as_uri() if brand.get("logo") else None

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True,
                      trim_blocks=True, lstrip_blocks=True)
    qa_lines, rows, done = [], [], []

    pal_warned = set()
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            raise SystemExit(f"Chromium failed to start ({e}). Try: python3 -m playwright install chromium")
        page = browser.new_page(device_scale_factor=1)
        for job in jobs:
            S = dict(SIZES[job["size"]], key=job["size"])
            S["pt"], S["pb"], S["px"] = S["st"] + S["m"], S["sb"] + S["m"], S["ss"] + S["m"]
            P = build_palette(job["pal"])
            key = json.dumps(job["pal"], sort_keys=True)
            if key not in pal_warned:
                pal_warned.add(key)
                cr = contrast(P["ink"], P["paper"])
                if cr < 4.5:
                    qa_lines.append(f"[palette] ink/paper contrast {cr:.1f}:1 is below 4.5:1")
                for k in ("primary", "accent"):
                    c2 = contrast(P[k], P["on_" + k])
                    if c2 < 3:
                        qa_lines.append(f"[palette] text on {k} only reaches {c2:.1f}:1; avoid long text on {k}")
            post = job["post"]
            c = post.get("copy", {})
            img_key = post.get("image")
            ctx = dict(S=S, P=P, F=fp, fonts=FONTS.resolve().as_uri(), brand=brand, product=product,
                       post=post, c=c, slide=job["slide"] or {}, si=job["si"], sc=job["sc"],
                       img=images.get(img_key) if img_key else None, images=images, logo=logo,
                       is_app=product.get("kind", "app") == "app",
                       sample=(job["arch"] == "testimonial" and not c.get("verified")) or post.get("sample", False),
                       source_needed=(job["arch"] == "stat" and not c.get("source")),
                       cta=c.get("cta") or brief.get("defaults", {}).get("cta", ""))
            html = env.get_template(f"{job['arch']}.html").render(**ctx)
            hp = out / "html" / f"{job['name']}.html"
            hp.write_text(html)
            page.set_viewport_size({"width": S["W"], "height": S["H"]})
            page.goto(hp.as_uri())
            page.evaluate("document.fonts.ready.then(() => true)")
            page.evaluate("window.__fit && window.__fit()")
            issues = page.evaluate("window.__qa ? window.__qa() : []")
            png = out / "png" / f"{job['name']}.png"
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": S["W"], "height": S["H"]})
            for w in copy_checks(job) + issues:
                if job["si"] <= 1 or "slide" in w or "overflow" in w or "safe" in w:
                    qa_lines.append(f"[{job['name']}] {w}")
            if job["si"] <= 1:
                rows.append(dict(file=png.name, post_id=post.get("id", ""), archetype=job["arch"], size=job["size"],
                                 headline=(c.get("headline") or (job["slide"] or {}).get("headline")
                                           or " ".join(x for x in (c.get("number"), c.get("label")) if x)
                                           or c.get("quote") or c.get("problem") or "").replace("⁠", ""),
                                 caption=post.get("caption", ""),
                                 alt_text=post.get("alt", ""),
                                 slides=job["sc"] if job["arch"] == "carousel" else 1))
            done.append((png, job))
            print(f"rendered {png.name}")
        browser.close()

    with open(out / "captions.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    (out / "qa.txt").write_text("\n".join(dict.fromkeys(qa_lines)) + "\n" if qa_lines else "No issues found.\n")
    if not a.no_sheet:
        sys.path.insert(0, str(SKILL / "scripts"))
        from contact_sheet import make_sheet
        make_sheet([d[0] for d in done], [f"{d[1]['arch']} · {d[1]['size']}" + (f" · slide {d[1]['si']}" if d[1]['arch'] == 'carousel' else "") for d in done],
                   out / "contact_sheet.png", title=f"{brand.get('name', '')} — {len(done)} posters", note=brief.get("sheet_note", ""))
    print(f"\n{len(done)} PNGs -> {out/'png'}")
    print(f"QA: {out/'qa.txt'}  ({len(set(qa_lines))} notes)")


if __name__ == "__main__":
    main()
