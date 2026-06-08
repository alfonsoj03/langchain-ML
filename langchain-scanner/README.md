# LangChain Investment Opportunity Scanner

LangChain LCEL pipeline that scrapes Arizona property listings, predicts sale prices using the model in [`langchain-prediction`](../langchain-prediction/), and flags properties where the predicted price exceeds the listing price by more than 10%. Gemini enriches flagged listings with investment summaries.

Part of the [langchain-ML](https://github.com/alfonsoj03/langchain-ML) monorepo. See the [root README](../README.md) for an overview of both packages.

## Setup

From the monorepo root:

```bash
cd langchain-scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### API key

Edit `.env` and set your Gemini key:

```env
GOOGLE_API_KEY=your-key-here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey). Without it, the pipeline still runs but skips LLM summaries and uses default values for missing fields.

### Prediction model

Ensure these files exist in the sibling directory (they are committed in this repo):

- `../langchain-prediction/modelo.pkl`
- `../langchain-prediction/zip_encoder.pkl`

By default the scanner loads the model directly from `langchain-prediction`. Set `PREDICTION_API_URL` in `.env` to use the HTTP API instead (local or [Hugging Face Space](https://huggingface.co/spaces/alfonsoj03/langchain-prediction)).

## Run tests

```bash
cd langchain-scanner
source .venv/bin/activate
pytest tests/ -v
```

## Run scanner

```bash
cd langchain-scanner
source .venv/bin/activate
python main.py --location "Phoenix, AZ" --max-results 20
```

Outputs `scanner_report.json` and `scanner_report.csv` in `langchain-scanner/` (or the path passed to `--report-path`).

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

## Related

- [langchain-prediction/README.md](../langchain-prediction/README.md) — prediction API and local deployment
