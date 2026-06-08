from scanner.nodes.score import score_opportunities


def test_gap_pct_calculation():
    predictions = [
        {
            "listing_id": "a",
            "address": "addr",
            "listing_price": 500_000,
            "predicted_price": 600_000,
            "confidence": "high",
        }
    ]
    result = score_opportunities({"predictions": predictions})
    scored = result["scored_listings"][0]
    assert scored["gap_pct"] == 0.2
    assert scored["flagged"] is True


def test_not_flagged_below_threshold():
    predictions = [
        {
            "listing_id": "b",
            "address": "addr",
            "listing_price": 500_000,
            "predicted_price": 540_000,
            "confidence": "high",
        }
    ]
    result = score_opportunities({"predictions": predictions})
    assert result["scored_listings"][0]["flagged"] is False
    assert result["flagged_listings"] == []


def test_sorted_by_gap_descending():
    predictions = [
        {
            "listing_id": "low",
            "address": "a",
            "listing_price": 100_000,
            "predicted_price": 115_000,
            "confidence": "high",
        },
        {
            "listing_id": "high",
            "address": "b",
            "listing_price": 100_000,
            "predicted_price": 150_000,
            "confidence": "low",
        },
    ]
    result = score_opportunities({"predictions": predictions})
    assert result["scored_listings"][0]["listing_id"] == "high"
    assert result["flagged_listings"][0]["listing_id"] == "high"


def test_preserves_confidence():
    predictions = [
        {
            "listing_id": "c",
            "address": "addr",
            "listing_price": 100_000,
            "predicted_price": 130_000,
            "confidence": "low",
        }
    ]
    result = score_opportunities({"predictions": predictions})
    assert result["scored_listings"][0]["confidence"] == "low"
