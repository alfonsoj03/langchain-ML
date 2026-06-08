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

## Endpoints

- `GET /` — API info
- `GET /valid-zips` — List of valid ZIP codes
- `POST /predict` — Run prediction

## Example request

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

Model MAPE: 22.5%
