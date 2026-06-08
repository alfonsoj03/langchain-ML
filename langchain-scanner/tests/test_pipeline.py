from unittest.mock import patch

from scanner.pipeline import build_pipeline


@patch("scanner.nodes.summarize.summarize_flagged", return_value={})
@patch("scanner.nodes.fetch._fetch_from_api")
def test_full_pipeline_produces_flagged_listings(mock_fetch, mock_summarize, sample_listings, tmp_path):
    mock_fetch.return_value = sample_listings

    pipeline = build_pipeline()
    result = pipeline.invoke(
        {
            "location": "Phoenix, AZ",
            "max_results": 10,
            "report_path": str(tmp_path),
        }
    )

    assert "scored_listings" in result
    assert len(result["scored_listings"]) >= 1
    assert "flagged_listings" in result
    assert (tmp_path / "scanner_report.json").exists()
    assert (tmp_path / "scanner_report.csv").exists()
