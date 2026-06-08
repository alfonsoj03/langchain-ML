from scanner.nodes.predict import predict_prices


def test_predict_known_listing(valid_listing):
    from scanner.nodes.normalize import normalize_listings

    normalized = normalize_listings({"raw_listings": [valid_listing]})
    listing = normalized["valid_listings"][0]
    result = predict_prices({"valid_listings": [listing]})

    prediction = result["predictions"][0]
    assert prediction["listing_id"] == "test-001"
    assert 750_000 < prediction["predicted_price"] < 850_000
    assert prediction["listing_price"] == 500_000.0
