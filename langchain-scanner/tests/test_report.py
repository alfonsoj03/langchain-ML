import csv
import json
from pathlib import Path

from scanner.nodes.report import generate_report


def test_generate_report_writes_json_and_csv(tmp_path):
    scored = [
        {
            "listing_id": "r1",
            "address": "100 Test St",
            "listing_price": 400000,
            "predicted_price": 500000,
            "gap_pct": 0.25,
            "flagged": True,
            "confidence": "high",
            "llm_summary": "Strong upside based on model gap.",
        }
    ]
    result = generate_report(
        {
            "scored_listings": scored,
            "flagged_listings": scored,
            "skipped_listings": [],
            "raw_listings": [{"listing_id": "r1"}],
            "report_path": str(tmp_path),
        }
    )

    json_path = Path(result["report_path"]) / "scanner_report.json"
    csv_path = Path(result["report_path"]) / "scanner_report.csv"
    assert json_path.exists()
    assert csv_path.exists()

    with open(json_path) as f:
        report = json.load(f)
    assert report["summary"]["scanned"] == 1
    assert report["summary"]["flagged"] == 1
    assert len(report["flagged_listings"]) == 1

    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["listing_id"] == "r1"
    assert rows[0]["flagged"] == "True"
