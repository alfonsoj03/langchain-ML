from typing import TypedDict


class ListingRaw(TypedDict):
    listing_id: str
    address: str
    zip: int
    listing_price: float
    sqft: int
    beds: int
    baths: float
    baths_full: int | None
    garage: int | None
    raw_description: str


class NormalizedListing(TypedDict):
    listing_id: str
    address: str
    zip: int
    listing_price: float
    sqft: int
    beds: int
    baths: int
    baths_full: int
    garage: int
    year_built: int
    stories: int
    raw_description: str
    confidence: str


class PredictionResult(TypedDict):
    listing_id: str
    address: str
    listing_price: float
    predicted_price: float
    confidence: str


class ScoredListing(TypedDict):
    listing_id: str
    address: str
    listing_price: float
    predicted_price: float
    gap_pct: float
    flagged: bool
    confidence: str
    llm_summary: str


class ScannerState(TypedDict, total=False):
    location: str
    max_results: int
    raw_listings: list[ListingRaw]
    valid_listings: list[NormalizedListing]
    skipped_listings: list[dict]
    predictions: list[PredictionResult]
    scored_listings: list[ScoredListing]
    flagged_listings: list[ScoredListing]
    report_path: str
