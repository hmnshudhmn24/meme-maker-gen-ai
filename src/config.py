# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_OPENAI = os.getenv("USE_OPENAI", "true").lower() in ("true","1","yes")
SD_MODEL_ID = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-v1-5")
DEVICE = os.getenv("DEVICE", "cpu")
FONT_PATH = os.getenv("FONT_PATH", "") or None
