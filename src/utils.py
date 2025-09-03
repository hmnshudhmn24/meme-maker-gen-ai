# src/utils.py
from PIL import Image, ImageDraw, ImageFont
import os

def load_font(size=48, font_path=None):
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size=size)
        except Exception:
            pass
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except Exception:
        return ImageFont.load_default()

def draw_text_with_outline(img, text, pos, font, fill=(255,255,255), outline=(0,0,0), outline_width=2):
    draw = ImageDraw.Draw(img)
    x, y = pos
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x+dx, y+dy), text, font=font, fill=outline, align="center")
    draw.text((x, y), text, font=font, fill=fill, align="center")

def wrap_text_for_width(text, font, max_width, draw=None):
    if draw is None:
        from PIL import ImageDraw, Image
        draw = ImageDraw.Draw(Image.new("RGB", (10,10)))
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for w in words:
            t = f"{line} {w}".strip()
            wbox = draw.textsize(t, font=font)
            if wbox[0] <= max_width:
                line = t
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
    return "\n".join(lines)
