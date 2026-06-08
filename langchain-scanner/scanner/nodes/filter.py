from scanner.state import ListingRaw, ScannerState


def filter_valid(state: ScannerState) -> dict:
    raw_listings: list[ListingRaw] = state.get("raw_listings", [])
    kept: list[ListingRaw] = []
    skipped = list(state.get("skipped_listings", []))

    for listing in raw_listings:
        if listing["listing_price"] <= 0 or listing["sqft"] <= 0 or listing["beds"] <= 0:
            skipped.append(
                {
                    "listing_id": listing["listing_id"],
                    "address": listing["address"],
                    "reason": "invalid_data",
                }
            )
            continue
        kept.append(listing)

    return {"raw_listings": kept, "skipped_listings": skipped}
