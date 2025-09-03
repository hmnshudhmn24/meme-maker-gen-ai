# 😂 Generative AI Meme Maker — gen-ai

Create shareable memes automatically: type a prompt or upload an image, let the model generate (or you upload) an image, and have an LLM suggest witty captions. Compose the final meme with top/bottom text and download it as PNG.

---

## ✨ Highlights

- 🎨 **Stable Diffusion** image generation (text → image).  
- 🧠 **LLM-powered captioning** (OpenAI by default) for witty meme text.  
- 🖼️ **Image upload support** (place captions over your own photos).  
- 🧩 **Streamlit UI** — simple, interactive, shareable.  
- 🛡️ Safety notes & content guidance included.

---

## 🚀 Quickstart

1. Clone repo:
```bash
git clone https://github.com/yourname/generative-ai-meme-maker-gen-ai.git
cd generative-ai-meme-maker-gen-ai
```

2. Create environment & install deps:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

3. Configure `.env`:
```
cp .env.example .env
# edit .env and set OPENAI_API_KEY and optionally FONT_PATH, DEVICE
```

4. Run Streamlit:
```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501`.

---

## 🔧 Configuration

- `.env` variables:
  - `OPENAI_API_KEY` — (optional) for caption generation via OpenAI.
  - `SD_MODEL_ID` — Hugging Face model id to use for Stable Diffusion.
  - `DEVICE` — `"cuda"` or `"cpu"`.
  - `FONT_PATH` — path to a TTF font to use for top/bottom text (optional).

---

## 🧠 How it works (short)

1. **Image generation** — The app uses `diffusers` Stable Diffusion pipeline to produce an image from your text prompt.  
2. **Caption generation** — The `captions` module asks an LLM to produce a small list of witty captions (or you can type your own).  
3. **Meme composition** — `compose_meme` overlays the chosen caption(s) on the generated/uploaded image using PIL, with outline, wrapping, and simple layout heuristics.  
4. **Download** — You can download the final meme as a PNG.

---

## ✅ Tips & Tricks

- Use short, visual prompts: `"grumpy corgi wearing sunglasses, photorealistic, studio lighting"`.  
- For bold captions, choose all-caps text — it's classic meme style.  
- If you find generation slow, use smaller image sizes (512×512) or use a GPU.  
- Want different caption styles? change `tone` in the sidebar to get sarcastic/vulgar/wholesome variants (be mindful of policy and safety).

---

## ⚠️ Safety & Policy

- **No illegal or harmful content.** Don't generate hateful, harassing, sexual, or copyrighted-face deepfakes.  
- **Be careful with public figures** — generating synthetic images of real people, especially public figures, can be unethical and/or prohibited depending on your jurisdiction or hosting platform.  
- **Content moderation**: you should add a moderation step in production to detect disallowed content.

---

## 🛠️ Extensibility (ideas)

- Add a small gallery / history of memes with bookmarking.  
- Add multi-caption layouts, memes with stickers, or multi-panel meme composition.  
- Replace LLM with on-device model (Llama, Mistral) for privacy.  
- Fine-tune an SD model for a consistent meme aesthetic (e.g., pixel-art or comic style).

---

## 🔁 Troubleshooting

- **Diffusers errors** — ensure `transformers`, `diffusers`, and `torch` are compatible. On CUDA machines install the matching torch wheel from PyTorch site.  
- **OpenAI errors** — set `OPENAI_API_KEY` in `.env`. If not provided, the app falls back to canned captions.  
- **Font issues** — if text looks tiny or missing, set a `FONT_PATH` to a TTF file on your machine.

---

## 📜 License

MIT — use freely for prototypes and demos. Respect people & copyright.
