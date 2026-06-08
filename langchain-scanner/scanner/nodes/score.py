from scanner.config import FLAG_THRESHOLD
from scanner.state import PredictionResult, ScoredListing, ScannerState


def score_opportunities(state: ScannerState) -> dict:
    predictions: list[PredictionResult] = state.get("predictions", [])
    scored: list[ScoredListing] = []

    for pred in predictions:
        listing_price = pred["listing_price"]
        predicted_price = pred["predicted_price"]
        gap_pct = (predicted_price - listing_price) / listing_price if listing_price else 0.0
        flagged = gap_pct > FLAG_THRESHOLD
        scored.append(
            ScoredListing(
                listing_id=pred["listing_id"],
                address=pred["address"],
                listing_price=listing_price,
                predicted_price=predicted_price,
                gap_pct=gap_pct,
                flagged=flagged,
                confidence=pred["confidence"],
                llm_summary="",
            )
        )

    scored.sort(key=lambda item: item["gap_pct"], reverse=True)
    flagged_listings = [item for item in scored if item["flagged"]]

    return {"scored_listings": scored, "flagged_listings": flagged_listings}
