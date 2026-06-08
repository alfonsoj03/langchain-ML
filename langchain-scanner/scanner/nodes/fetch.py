import json
from typing import Any

import httpx

from scanner.config import FIXTURES_DIR
from scanner.state import ListingRaw, ScannerState

REALTOR_SEARCH_URL = "https://www.realtor.com/api/v1/rdc_search_srp"
REALTOR_CLIENT_ID = "rdc-search-new-communities"


def load_fixture_listings() -> list[ListingRaw]:
    fixture_path = FIXTURES_DIR / "sample_listings.json"
    with open(fixture_path) as f:
        return json.load(f)


def _build_search_payload(location: str, max_results: int) -> dict[str, Any]:
    return {
        "client_id": REALTOR_CLIENT_ID,
        "limit": max_results,
        "offset": 0,
        "search_location": {"location": location},
        "status": ["for_sale"],
    }


def _parse_api_results(data: dict[str, Any]) -> list[ListingRaw]:
    results = data.get("data", {}).get("home_search", {}).get("results", [])
    listings: list[ListingRaw] = []

    for item in results:
        address = item.get("location", {}).get("address", {})
        description = item.get("description", {})
        line = address.get("line", "")
        city = address.get("city", "")
        state = address.get("state_code", "")
        postal = address.get("postal_code", "")
        full_address = f"{line}, {city}, {state} {postal}".strip(", ")

        listings.append(
            ListingRaw(
                listing_id=str(item.get("property_id", item.get("listing_id", ""))),
                address=full_address,
                zip=int(postal) if postal else 0,
                listing_price=float(item.get("list_price", 0)),
                sqft=int(description.get("sqft", 0) or 0),
                beds=int(description.get("beds", 0) or 0),
                baths=float(description.get("baths", 0) or 0),
                baths_full=description.get("baths_full"),
                garage=description.get("garage"),
                raw_description=item.get("description", {}).get("text", "")
                if isinstance(item.get("description"), dict)
                else str(item.get("description", "")),
            )
        )

    return listings


def _fetch_from_api(location: str, max_results: int) -> list[ListingRaw]:
    payload = _build_search_payload(location, max_results)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = httpx.post(
        REALTOR_SEARCH_URL,
        json=payload,
        headers=headers,
        timeout=30.0,
    )
    response.raise_for_status()
    return _parse_api_results(response.json())


def fetch_listings(state: ScannerState) -> dict:
    location = state.get("location", "Phoenix, AZ")
    max_results = state.get("max_results", 50)

    try:
        listings = _fetch_from_api(location, max_results)
        if not listings:
            listings = load_fixture_listings()[:max_results]
    except Exception:
        listings = load_fixture_listings()[:max_results]

    return {"raw_listings": listings}
