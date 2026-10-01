"""Typographic attack on the home page photo, scored by a real CLIP model.

Pastes a handwritten-style sticky note onto the photo and runs zero-shot
CLIP classification on the clean photo and on each stickered version.
Writes the images to assets/img/attack/ and the scores to
_data/clip_attack.json, which the home page reads.

Run from the repo root:
    ~/.venvs/clip/bin/python manim/clip_attack.py
"""

import json
from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import CLIPModel, CLIPProcessor

ROOT = Path(__file__).resolve().parents[1]
# photo id -> (file, where the name tag goes as fractions of width/height)
PHOTOS = {
    "beach": (ROOT / "assets/img/prof_pic_beach.jpg", (0.15, 0.63)),
}
OUT_IMG = ROOT / "assets/img/attack"
OUT_JSON = ROOT / "_data/clip_attack.json"
MODEL = "openai/clip-vit-base-patch32"

# What the sticky note says, keyed by a short id.
STICKERS = {
    "potato": "POTATO",
    "retriever": "GOLDEN\nRETRIEVER",
    "toaster": "TOASTER",
}

# Zero-shot label set. CLIP picks among exactly these.
LABELS = [
    "a photo of a college student",
    "a photo of a person at the beach",
    "a photo of a sunset",
    "a photo of a potato",
    "a photo of a golden retriever",
    "a photo of a toaster",
]

FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def load_font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def add_sticker(img, text, at):
    """Stick a 'HELLO my name is' name tag on Ben's chest."""
    w, h = img.size
    tag_w, tag_h = int(w * 0.30), int(h * 0.20)
    band = int(tag_h * 0.36)
    tag = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tag)
    r = int(tag_h * 0.08)
    d.rounded_rectangle((0, 0, tag_w - 1, tag_h - 1), radius=r, fill=(214, 40, 40, 255))
    d.rounded_rectangle((int(tag_w * 0.04), band, tag_w - 1 - int(tag_w * 0.04), tag_h - 1 - int(tag_h * 0.07)), radius=r // 2, fill=(255, 255, 255, 255))
    hello = load_font(int(band * 0.52))
    small = load_font(int(band * 0.26))
    for txt, f, y in (("HELLO", hello, band * 0.08), ("my name is", small, band * 0.66)):
        bb = d.textbbox((0, 0), txt, font=f)
        d.text(((tag_w - bb[2]) / 2, y), txt, font=f, fill=(255, 255, 255, 255))
    lines = text.split("\n")
    body_h = tag_h - band - int(tag_h * 0.07)
    size = int(body_h * (0.62 if len(lines) == 1 else 0.38))
    font = load_font(size)
    while max(d.textbbox((0, 0), ln, font=font)[2] for ln in lines) > tag_w * 0.86:
        size -= 2
        font = load_font(size)
    heights = [d.textbbox((0, 0), ln, font=font)[3] for ln in lines]
    y = band + (body_h - sum(heights) - 4 * (len(lines) - 1)) / 2
    for ln, lh in zip(lines, heights):
        bb = d.textbbox((0, 0), ln, font=font)
        d.text(((tag_w - bb[2]) / 2, y), ln, font=font, fill=(20, 20, 30, 255))
        y += lh + 4
    tag = tag.rotate(-6, expand=True, resample=Image.BICUBIC)
    shadow = Image.new("RGBA", tag.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 60), mask=tag.split()[3])
    out = img.convert("RGBA")
    x0, y0 = int(w * at[0]), int(h * at[1])
    out.alpha_composite(shadow, (x0 + 5, y0 + 7))
    out.alpha_composite(tag, (x0, y0))
    return out.convert("RGB")


def scores(model, proc, img, device):
    inputs = proc(text=LABELS, images=img, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits_per_image[0]
    probs = logits.softmax(-1).cpu().tolist()
    return sorted(
        ({"label": LABELS[i].replace("a photo of ", ""), "p": round(p, 4)} for i, p in enumerate(probs)),
        key=lambda r: -r["p"],
    )


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = CLIPModel.from_pretrained(MODEL).to(device).eval()
    proc = CLIPProcessor.from_pretrained(MODEL)
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    results = {
        "model": MODEL,
        "labels": [l.replace("a photo of ", "") for l in LABELS],
        "stickers": {k: t.replace("\n", " ").lower() for k, t in STICKERS.items()},
        "photos": {},
    }
    for pid, (path, at) in PHOTOS.items():
        photo = Image.open(path).convert("RGB")
        versions = {"clean": scores(model, proc, photo, device)}
        photo.save(OUT_IMG / f"{pid}-clean.jpg", quality=85)
        for key, text in STICKERS.items():
            stuck = add_sticker(photo, text, at)
            stuck.save(OUT_IMG / f"{pid}-{key}.jpg", quality=85)
            versions[key] = scores(model, proc, stuck, device)
        results["photos"][pid] = versions
        for k, v in versions.items():
            print(f"{pid:7s} {k:10s} -> {v[0]['label']} ({v[0]['p']:.2f})")
    OUT_JSON.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
