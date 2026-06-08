import os
import pickle
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
PREDICTION_DIR = ROOT_DIR.parent / "langchain-prediction"
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"

SCAN_LOCATION = os.getenv("SCAN_LOCATION", "Phoenix, AZ")
SCAN_MAX_RESULTS = int(os.getenv("SCAN_MAX_RESULTS", "50"))
FLAG_THRESHOLD = float(os.getenv("FLAG_THRESHOLD", "0.10"))
PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "").strip() or None
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip() or None
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

MODEL_MAPE = 0.225


def _load_valid_zips() -> set[int]:
    encoder_path = PREDICTION_DIR / "zip_encoder.pkl"
    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)
    zips = encoder.ordinal_encoder.mapping[0]["mapping"].index.tolist()
    return {
        int(z)
        for z in zips
        if pd.notna(z) and z not in (-1, -2)
    }


VALID_ZIPS: set[int] = _load_valid_zips()
