from scanner.config import FLAG_THRESHOLD, SCAN_LOCATION, SCAN_MAX_RESULTS, VALID_ZIPS


def test_valid_zips_count():
    assert len(VALID_ZIPS) == 292


def test_valid_zips_range():
    assert min(VALID_ZIPS) == 85003
    assert max(VALID_ZIPS) == 86444


def test_valid_zips_contains_phoenix():
    assert 85018 in VALID_ZIPS


def test_defaults():
    assert SCAN_LOCATION == "Phoenix, AZ"
    assert SCAN_MAX_RESULTS == 50
    assert FLAG_THRESHOLD == 0.10
