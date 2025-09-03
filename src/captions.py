# src/captions.py
from typing import List
import os

from .config import OPENAI_API_KEY, USE_OPENAI

def generate_captions(prompt: str, tone: str = "witty", n: int = 3) -> List[str]:
    prompt = (prompt or "").strip() or "A funny situation"

    if USE_OPENAI and OPENAI_API_KEY:
        try:
            import openai, json
            openai.api_key = OPENAI_API_KEY
            system = (
                "You are a clever meme-writer. Produce short, punchy meme captions (one-line). "
                "Return exactly the number of captions requested as a JSON array."
            )
            user = (
                f"Context: {prompt}\n"
                f"Tone: {tone}\n"
                f"Return {n} captions as a JSON array of strings, no additional text."
            )
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini" if "gpt-4o-mini" else "gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":system},
                    {"role":"user","content":user}
                ],
                temperature=0.9,
                max_tokens=200
            )
            text = resp["choices"][0]["message"]["content"].strip()
            try:
                arr = json.loads(text)
                if isinstance(arr, list):
                    return [str(a) for a in arr][:n]
            except Exception:
                lines = [l.strip().strip('"- ') for l in text.splitlines() if l.strip()]
                if lines:
                    return lines[:n]
        except Exception:
            pass

    # Fallback captions
    base = [
        f"When you realize: {prompt}",
        f"{prompt} — that moment when you...",
        f"Me trying to handle {prompt}"
    ]
    return base[:n]
