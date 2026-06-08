# langchain-ML

Monorepo for Arizona real estate machine learning: a price-prediction API and a LangChain scanner that finds investment opportunities from live listings.

| Package | Role |
|---|---|
| [`langchain-prediction/`](langchain-prediction/) | FastAPI service that predicts Arizona home sale prices from property features |
| [`langchain-scanner/`](langchain-scanner/) | LangChain LCEL pipeline that scores listings and flags undervalued properties |

The scanner uses the prediction model from `langchain-prediction/` by default (local import). You can optionally point it at the deployed Hugging Face Space or a locally running API instead.

## Repository layout

```
langchain-ML/
├── langchain-prediction/   # FastAPI + model artifacts (modelo.pkl, zip_encoder.pkl)
├── langchain-scanner/      # LangChain pipeline, CLI, and tests
├── .gitignore
└── .gitattributes        # Git LFS for *.pkl model files
```

## Quick start

Clone the repo, then set up each package in its own virtual environment:

```bash
git clone https://github.com/alfonsoj03/langchain-ML.git
cd langchain-ML
```

### Run the scanner (typical workflow)

```bash
cd langchain-scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add GOOGLE_API_KEY for Gemini summaries
python main.py --location "Phoenix, AZ" --max-results 20
```

Reports are written to `langchain-scanner/scanner_report.json` and `scanner_report.csv`.

### Run the prediction API locally (optional)

Only needed if you want a standalone HTTP service or set `PREDICTION_API_URL` in the scanner.

```bash
cd langchain-prediction
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

Deployed instance: [alfonsoj03-langchain-prediction on Hugging Face Spaces](https://huggingface.co/spaces/alfonsoj03/langchain-prediction).

## Documentation

- [langchain-prediction/README.md](langchain-prediction/README.md) — API endpoints, local run, and deployment
- [langchain-scanner/README.md](langchain-scanner/README.md) — pipeline stages, environment variables, and tests

## Development notes

- `.env` files are gitignored; copy from `.env.example` where provided.
- Model artifacts in `langchain-prediction/` are tracked with Git LFS.
- Scanner report outputs are gitignored.
