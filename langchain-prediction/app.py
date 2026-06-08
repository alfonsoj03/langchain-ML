import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Arizona Home Price Prediction API")

# Load model artifacts once at startup
with open("modelo.pkl", "rb") as f:
    modelo, variables, min_max_scaler = pickle.load(f)

with open("zip_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

COLUMNAS_MODELO = list(variables)

VALID_ZIPS = [
    z
    for z in encoder.ordinal_encoder.mapping[0]["mapping"].index.tolist()
    if pd.notna(z) and z not in (-1, -2)
]


class PredictRequest(BaseModel):
    year_built: int = Field(..., ge=1850, le=2026)
    sqft: int = Field(..., ge=150, le=18000)
    stories: int = Field(..., ge=1, le=4)
    beds: int = Field(..., ge=1, le=12)
    baths: int = Field(..., ge=0, le=20)
    baths_full: int = Field(..., ge=0, le=20)
    garage: int = Field(..., ge=0, le=20)
    zip: int


def prepare_data(request: PredictRequest) -> pd.DataFrame:
    """Mirror the notebook preprocessing pipeline before prediction."""
    data = pd.DataFrame(
        [
            [
                request.year_built,
                request.sqft,
                request.stories,
                request.beds,
                request.baths,
                request.baths_full,
                request.garage,
                request.zip,
            ]
        ],
        columns=[
            "year_built",
            "sqft",
            "stories",
            "beds",
            "baths",
            "baths_full",
            "garage",
            "zip",
        ],
    )

    data_preparada = data.copy()
    data_preparada["zip_encoded"] = encoder.transform(data_preparada[["zip"]])["zip"]
    data_preparada.drop(columns=["zip"], inplace=True)
    data_preparada[COLUMNAS_MODELO] = min_max_scaler.transform(
        data_preparada[COLUMNAS_MODELO]
    )

    return data_preparada[COLUMNAS_MODELO]


@app.get("/")
async def root():
    return {
        "message": "ML Model API",
        "endpoints": {
            "predict": "POST /predict",
            "valid_zips": "GET /valid-zips",
        },
        "model_error_mape": "22.5%",
    }


@app.get("/valid-zips")
async def valid_zips():
    return {"valid_zips": [int(z) for z in VALID_ZIPS]}


@app.post("/predict")
async def predict(request: PredictRequest):
    if request.zip not in VALID_ZIPS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid zip code: {request.zip}. Use GET /valid-zips for accepted values.",
        )

    data_preparada = prepare_data(request)
    prediccion_numerica = modelo.predict(data_preparada)
    prediction = float(prediccion_numerica[0])

    return {
        "prediction": prediction,
        "input": request.model_dump(),
        "model_error_mape": "22.5%",
    }
