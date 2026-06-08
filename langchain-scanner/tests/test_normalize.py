from scanner.nodes.normalize import normalize_listings


def test_filters_invalid_zip(sample_listings):
    result = normalize_listings({"raw_listings": sample_listings})
    zips = {l["zip"] for l in result["valid_listings"]}
    assert 90001 not in zips
    assert len(result["skipped_listings"]) >= 1
    assert any(s["reason"] == "invalid_zip" for s in result["skipped_listings"])


def test_infers_baths_full_from_baths(sample_listings):
    result = normalize_listings({"raw_listings": sample_listings})
    az001 = next(l for l in result["valid_listings"] if l["listing_id"] == "az-001")
    assert az001["baths_full"] == 1


def test_infers_baths_full_floor_for_half_bath(sample_listings):
    result = normalize_listings({"raw_listings": sample_listings})
    az002 = next(l for l in result["valid_listings"] if l["listing_id"] == "az-002")
    assert az002["baths_full"] == 2


def test_garage_from_explicit_field(sample_listings):
    result = normalize_listings({"raw_listings": sample_listings})
    az003 = next(l for l in result["valid_listings"] if l["listing_id"] == "az-003")
    assert az003["garage"] == 2
    assert az003["confidence"] == "high"


def test_garage_defaults_to_zero_with_low_confidence(sample_listings):
    result = normalize_listings({"raw_listings": sample_listings})
    az004 = next(l for l in result["valid_listings"] if l["listing_id"] == "az-004")
    assert az004["garage"] == 0
    assert az004["confidence"] == "low"


def test_garage_parsed_from_description(valid_listing):
    listing = dict(valid_listing)
    listing["garage"] = None
    result = normalize_listings({"raw_listings": [listing]})
    assert result["valid_listings"][0]["garage"] == 2
    assert result["valid_listings"][0]["confidence"] == "high"
