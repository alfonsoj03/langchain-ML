import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_listings():
    with open(FIXTURES_DIR / "sample_listings.json") as f:
        return json.load(f)


@pytest.fixture
def valid_listing():
    return {
        "listing_id": "test-001",
        "address": "123 E Camelback Rd, Phoenix, AZ 85018",
        "zip": 85018,
        "listing_price": 500000.0,
        "sqft": 1800,
        "beds": 3,
        "baths": 2.0,
        "baths_full": 2,
        "garage": 2,
        "raw_description": "Beautiful 3 bed home with 2-car garage.",
    }
