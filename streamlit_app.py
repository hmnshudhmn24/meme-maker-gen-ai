# streamlit_app.py
import streamlit as st
from PIL import Image
import io, os

from src.captions import generate_captions
from src.generator import generate_image_from_prompt, compose_meme
from src.config import FONT_PATH

st.set_page_config(page_title="Generative AI Meme Maker", page_icon="😂", layout="centered")
st.title("😂 Generative AI Meme Maker — gen-ai")

st.sidebar.header("Settings")
use_sd = st.sidebar.checkbox("Enable Stable Diffusion generation", value=True)
tone = st.sidebar.selectbox("Caption tone", ["witty", "sarcastic", "wholesome", "dry"], index=0)
font_size = st.sidebar.slider("Font size", min_value=28, max_value=96, value=48, step=2)
custom_caption = st.sidebar.text_input("Or enter your own caption (leave empty to use AI)")

st.header("1) Choose input")
input_mode = st.radio("", ["Text prompt → SD generate image", "Upload your image (use SD not required)"])

gen_image = None
uploaded_image = None
if input_mode.startswith("Text"):
    prompt = st.text_input("Enter a text prompt for the image (e.g., 'cat wearing sunglasses, cinematic')", value="a surprised cat wearing sunglasses, photorealistic")
    width = st.selectbox("Width", [512, 768, 1024], index=0)
    height = width
    steps = st.slider("SD steps", 10, 50, 25)
    guidance = st.slider("Guidance scale", 3.0, 12.0, 7.5)
    if st.button("Generate image") and use_sd:
        with st.spinner("Generating image (Stable Diffusion) — this may take a minute..."):
            try:
                img = generate_image_from_prompt(prompt, width=width, height=height, num_inference_steps=steps, guidance_scale=guidance)
                st.image(img, caption="Generated image", use_column_width=True)
                gen_image = img
            except Exception as e:
                st.error(f"Image generation failed: {e}")
elif input_mode.startswith("Upload"):
    uploaded_file = st.file_uploader("Upload an image (png/jpg)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image_bytes = uploaded_file.read()
        uploaded_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        st.image(uploaded_image, caption="Uploaded image", use_column_width=True)

st.write("---")
st.header("2) Captions")
captions = []
if custom_caption:
    captions = [custom_caption]
    st.write("Using your custom caption.")
else:
    prompt_for_caption = st.text_input("Caption idea / context (used by caption generator)", value="funny cat that just learned calculus")
    if st.button("Generate captions (LLM)"):
        with st.spinner("Asking the meme-writer LLM..."):
            captions = generate_captions(prompt_for_caption, tone=tone, n=5)
            st.session_state.captions = captions
            for i, c in enumerate(captions):
                st.write(f"{i+1}. {c}")
# restore session captions if present
if not captions and st.session_state.get('captions'):
    captions = st.session_state.get('captions', [])

chosen_idx = None
if captions:
    chosen_idx = st.selectbox("Choose caption", list(range(len(captions))), format_func=lambda i: captions[i])

st.write("---")
st.header("3) Compose meme and download")
base_img = gen_image if gen_image is not None else uploaded_image if uploaded_image is not None else None

if base_img is None:
    st.info("Generate or upload an image first.")
else:
    top_text = st.text_input("Top text (optional)", value="")
    bottom_text = st.text_input("Bottom text (optional)", value=captions[chosen_idx] if chosen_idx is not None and captions else "")
    if st.button("Create meme"):
        with st.spinner("Composing meme..."):
            try:
                meme = compose_meme(base_img, top_text=top_text, bottom_text=bottom_text, font_path=FONT_PATH, font_size=font_size)
                st.image(meme, caption="Final meme", use_column_width=True)
                buf = io.BytesIO()
                meme.save(buf, format="PNG")
                st.download_button("⬇️ Download meme (PNG)", data=buf.getvalue(), file_name="meme.png", mime="image/png")
            except Exception as e:
                st.error(f"Failed to compose meme: {e}")
