# src/generator.py
from typing import Optional
from PIL import Image
import torch
from .config import SD_MODEL_ID, DEVICE
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from .utils import load_font, draw_text_with_outline, wrap_text_for_width

_PIPELINE = None

def get_pipeline(model_id: str = None, device: str = None):
    global _PIPELINE
    if _PIPELINE is not None:
        return _PIPELINE
    mid = model_id or SD_MODEL_ID
    dev = device or DEVICE
    # Load pipeline (will download weights first time)
    pipe = StableDiffusionPipeline.from_pretrained(mid, torch_dtype=torch.float16 if torch.cuda.is_available() and dev.startswith("cuda") else torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(dev)
    pipe.enable_attention_slicing()
    _PIPELINE = pipe
    return _PIPELINE

def generate_image_from_prompt(prompt: str, width: int = 512, height: int = 512, num_inference_steps: int = 25, guidance_scale: float = 7.5):
    pipe = get_pipeline()
    generator = torch.Generator(device=DEVICE) if torch.cuda.is_available() and DEVICE.startswith("cuda") else None
    out = pipe(prompt, height=height, width=width, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale, generator=generator)
    image = out.images[0]
    return image

def compose_meme(image: Image.Image, top_text: Optional[str] = None, bottom_text: Optional[str] = None, font_path: Optional[str] = None, font_size: int = 48):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    w, h = image.size
    font = load_font(size=font_size, font_path=font_path)
    canvas = Image.new("RGBA", (w, h + int(0.2*h)), (255,255,255,0))
    canvas.paste(image, (0,0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(canvas)

    max_text_width = int(w * 0.95)
    # Top text
    if top_text:
        wrapped_top = wrap_text_for_width(top_text.upper(), font, max_text_width, draw=draw)
        lines = wrapped_top.split("\n")
        for i, line in enumerate(lines):
            lw, lh = draw.textsize(line, font=font)
            px = (w - lw) // 2
            py = int(h * 0.02) + i * (lh + 4)
            draw_text_with_outline(canvas, line, (px, py), font, fill=(255,255,255), outline=(0,0,0), outline_width=3)

    # Bottom text
    if bottom_text:
        wrapped_bottom = wrap_text_for_width(bottom_text.upper(), font, max_text_width, draw=draw)
        lines = wrapped_bottom.split("\n")
        last_line_h = draw.textsize(lines[-1], font=font)[1]
        block_h = len(lines) * (last_line_h + 4)
        start_y = h - block_h - int(0.02*h) + int(0.2*h)
        for i, line in enumerate(lines):
            lw, lh = draw.textsize(line, font=font)
            px = (w - lw) // 2
            py = h + i * (lh + 4) - int(0.02*h)
            draw_text_with_outline(canvas, line, (px, py), font, fill=(255,255,255), outline=(0,0,0), outline_width=3)

    return canvas.convert("RGB")
