"""Lay every rendered poster out on one labelled sheet for review or class discussion."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"


def _font(size, weight=500):
    f = ImageFont.truetype(str(FONTS / "Inter.ttf"), size)
    try:
        f.set_variation_by_axes([14 if size < 20 else 32, weight])
    except Exception:
        pass
    return f


def make_sheet(paths, labels, out, title="", note="", thumb_w=260, cols=6, gap=28, pad=56):
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        h = round(im.height * thumb_w / im.width)
        thumbs.append(im.resize((thumb_w, h), Image.LANCZOS))
    rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
    row_labels = [labels[i:i + cols] for i in range(0, len(labels), cols)]
    label_h = 30
    head_h = 120 if note else 90
    W = pad * 2 + cols * thumb_w + (cols - 1) * gap
    H = pad + head_h + sum(max(t.height for t in r) + label_h + gap for r in rows) + pad
    sheet = Image.new("RGB", (W, H), (246, 246, 244))
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad), title, fill=(20, 20, 20), font=_font(34, 700))
    if note:
        d.text((pad, pad + 50), note, fill=(110, 110, 110), font=_font(18, 450))
    y = pad + head_h
    for r, ls in zip(rows, row_labels):
        x = pad
        rh = max(t.height for t in r)
        for t, l in zip(r, ls):
            sheet.paste(t, (x, y))
            d.rectangle([x, y, x + t.width - 1, y + t.height - 1], outline=(215, 215, 210))
            d.text((x, y + t.height + 8), l, fill=(90, 90, 90), font=_font(15, 500))
            x += thumb_w + gap
        y += rh + label_h + gap
    sheet.save(out)
    return out
