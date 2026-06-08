from scanner.nodes.filter import filter_valid


def test_filters_invalid_data():
    listings = [
        {
            "listing_id": "bad-1",
            "address": "0 Bad St",
            "zip": 85018,
            "listing_price": 0,
            "sqft": 1000,
            "beds": 2,
            "baths": 1.0,
            "baths_full": 1,
            "garage": 1,
            "raw_description": "",
        },
        {
            "listing_id": "good-1",
            "address": "1 Good St",
            "zip": 85018,
            "listing_price": 400000,
            "sqft": 1200,
            "beds": 2,
            "baths": 1.0,
            "baths_full": 1,
            "garage": 1,
            "raw_description": "Nice home.",
        },
    ]

    result = filter_valid({"raw_listings": listings})

    assert len(result["raw_listings"]) == 1
    assert result["raw_listings"][0]["listing_id"] == "good-1"
    assert any(s["reason"] == "invalid_data" for s in result["skipped_listings"])
