import os
import sys

import httpx

from scanner.config import PREDICTION_API_URL, PREDICTION_DIR
from scanner.state import NormalizedListing, PredictionResult, ScannerState


def _ensure_prediction_path() -> None:
    path = str(PREDICTION_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)
    os.chdir(PREDICTION_DIR)


def _predict_direct(listing: NormalizedListing) -> float:
    _ensure_prediction_path()
    from app import PredictRequest, modelo, prepare_data

    request = PredictRequest(
        year_built=listing["year_built"],
        sqft=listing["sqft"],
        stories=listing["stories"],
        beds=listing["beds"],
        baths=listing["baths"],
        baths_full=listing["baths_full"],
        garage=listing["garage"],
        zip=listing["zip"],
    )
    data = prepare_data(request)
    return float(modelo.predict(data)[0])


def _predict_http(listing: NormalizedListing) -> float:
    payload = {
        "year_built": listing["year_built"],
        "sqft": listing["sqft"],
        "stories": listing["stories"],
        "beds": listing["beds"],
        "baths": listing["baths"],
        "baths_full": listing["baths_full"],
        "garage": listing["garage"],
        "zip": listing["zip"],
    }
    response = httpx.post(f"{PREDICTION_API_URL}/predict", json=payload, timeout=30.0)
    response.raise_for_status()
    return float(response.json()["prediction"])


def predict_price(listing: NormalizedListing) -> float:
    if PREDICTION_API_URL:
        return _predict_http(listing)
    return _predict_direct(listing)


def predict_prices(state: ScannerState) -> dict:
    predictions: list[PredictionResult] = []

    for listing in state.get("valid_listings", []):
        predicted_price = predict_price(listing)
        predictions.append(
            PredictionResult(
                listing_id=listing["listing_id"],
                address=listing["address"],
                listing_price=listing["listing_price"],
                predicted_price=predicted_price,
                confidence=listing["confidence"],
            )
        )

    return {"predictions": predictions}
