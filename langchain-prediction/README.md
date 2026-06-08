---
title: Langchain Prediction
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: cc
short_description: Prediction of list pricing for properties in Arizona.
---

# Arizona Home Price Prediction API

FastAPI service that predicts Arizona home sale prices from property features.

Part of the [langchain-ML](https://github.com/alfonsoj03/langchain-ML) monorepo. The sibling package [`langchain-scanner`](../langchain-scanner/) consumes this model to score live listings.

Model MAPE: 22.5%

## Endpoints

- `GET /` — API info
- `GET /valid-zips` — list of valid ZIP codes
- `POST /predict` — run prediction

## Run locally

From the monorepo root:

```bash
cd langchain-prediction
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

Test with curl:

```bash
curl -X POST "http://localhost:7860/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "year_built": 1990,
    "sqft": 300,
    "stories": 1,
    "beds": 1,
    "baths": 1,
    "baths_full": 1,
    "garage": 1,
    "zip": 85018
  }'
```

## Deployed API

Production instance on Hugging Face Spaces:

```bash
curl -X POST "https://alfonsoj03-langchain-prediction.hf.space/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "year_built": 1990,
    "sqft": 300,
    "stories": 1,
    "beds": 1,
    "baths": 1,
    "baths_full": 1,
    "garage": 1,
    "zip": 85018
  }'
```

## Used by the scanner

By default, `langchain-scanner` imports this package directly from `../langchain-prediction` (no API server required). To use HTTP instead, set in `langchain-scanner/.env`:

```env
PREDICTION_API_URL=http://localhost:7860
# or
PREDICTION_API_URL=https://alfonsoj03-langchain-prediction.hf.space
```

See [langchain-scanner/README.md](../langchain-scanner/README.md) for the full scanner workflow.
