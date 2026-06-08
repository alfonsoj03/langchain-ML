# LangChain Investment Opportunity Scanner

LangChain LCEL pipeline that scrapes Arizona property listings, predicts sale prices using the model in `langchain-prediction`, and flags properties where the predicted price exceeds the listing price by more than 10%. Gemini enriches flagged listings with investment summaries.

## Setup

```bash
cd langchain-scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### API key

Edit `langchain-scanner/.env` and set your Gemini key:

```env
GOOGLE_API_KEY=your-key-here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey). Without it, the pipeline still runs but skips LLM summaries and uses default values for missing fields.

Ensure `langchain-prediction/modelo.pkl` and `langchain-prediction/zip_encoder.pkl` exist (sibling directory).

## Run tests

```bash
pytest tests/ -v
```

## Run scanner

```bash
python main.py --location "Phoenix, AZ" --max-results 20
```

Outputs `scanner_report.json` and `scanner_report.csv` in the project root (or `--report-path`).

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | _(empty)_ | Gemini API key for LLM enrichment |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model name |
| `SCAN_LOCATION` | `Phoenix, AZ` | Realtor.com search location |
| `SCAN_MAX_RESULTS` | `50` | Max listings per run |
| `FLAG_THRESHOLD` | `0.10` | Flag when predicted/listing gap exceeds this |
| `PREDICTION_API_URL` | _(empty)_ | Use HTTP API instead of direct model import |

## Pipeline (LCEL)

1. **fetch_listings** — Realtor.com API (fixture fallback on error)
2. **filter_valid** — drop listings with price/sqft/beds = 0
3. **normalize_listings** — ZIP validation, field inference, Gemini extraction fallback
4. **predict_prices** — price prediction per listing
5. **score_opportunities** — gap calculation and flagging
6. **summarize_flagged** — Gemini investment rationale for flagged listings
7. **generate_report** — JSON/CSV report
