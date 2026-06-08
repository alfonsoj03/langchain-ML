import math
import re

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from scanner.config import GEMINI_MODEL, GOOGLE_API_KEY, VALID_ZIPS
from scanner.state import ListingRaw, NormalizedListing, ScannerState

_GARAGE_RE = re.compile(
    r"(\d+)\s*[- ]?\s*car\s+garage|garage[:\s]+(\d+)|(\d+)\s+car",
    re.IGNORECASE,
)
_YEAR_BUILT_RE = re.compile(
    r"built\s+in\s+(\d{4})|year\s+built[:\s]+(\d{4})|built\s+(\d{4})",
    re.IGNORECASE,
)
_STORIES_RE = re.compile(
    r"(\d+)[\s-]story|single[\s-]story|two[\s-]story|three[\s-]story",
    re.IGNORECASE,
)

DEFAULT_YEAR_BUILT = 1990
DEFAULT_STORIES = 1


def _infer_baths_full(baths: float, baths_full: int | None) -> int:
    if baths_full is not None:
        return baths_full
    return int(math.floor(baths))


def _infer_garage(description: str, garage: int | None) -> tuple[int, str]:
    if garage is not None:
        return garage, "high"
    match = _GARAGE_RE.search(description)
    if match:
        value = next(g for g in match.groups() if g is not None)
        return int(value), "high"
    return 0, "low"


def _infer_year_built(description: str) -> int | None:
    match = _YEAR_BUILT_RE.search(description)
    if not match:
        return None
    year = next(g for g in match.groups() if g is not None)
    return int(year)


def _infer_stories(description: str) -> int | None:
    match = _STORIES_RE.search(description)
    if not match:
        return None
    token = match.group(0).lower()
    if "single" in token:
        return 1
    if "two" in token:
        return 2
    if "three" in token:
        return 3
    digit = next(g for g in match.groups() if g is not None)
    return int(digit)


def _build_extraction_chain():
    prompt = PromptTemplate.from_template(
        "Extract year_built and stories from this listing description. "
        "Return ONLY valid JSON with keys year_built (int) and stories (int). "
        "If unknown, use null.\n\nDescription: {description}"
    )
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0)
    return prompt | llm | JsonOutputParser()


def _extract_with_llm(description: str) -> dict:
    chain = _build_extraction_chain()
    return chain.invoke({"description": description})


def _resolve_year_and_stories(description: str) -> tuple[int, int]:
    year_built = _infer_year_built(description)
    stories = _infer_stories(description)

    if GOOGLE_API_KEY and description.strip() and (year_built is None or stories is None):
        try:
            extracted = _extract_with_llm(description)
            if year_built is None and extracted.get("year_built"):
                year_built = int(extracted["year_built"])
            if stories is None and extracted.get("stories"):
                stories = int(extracted["stories"])
        except Exception:
            pass

    return year_built or DEFAULT_YEAR_BUILT, stories or DEFAULT_STORIES


def normalize_listings(state: ScannerState) -> dict:
    raw_listings: list[ListingRaw] = state.get("raw_listings", [])
    valid: list[NormalizedListing] = []
    skipped: list[dict] = []

    for listing in raw_listings:
        if listing["zip"] not in VALID_ZIPS:
            skipped.append(
                {
                    "listing_id": listing["listing_id"],
                    "address": listing["address"],
                    "reason": "invalid_zip",
                }
            )
            continue

        garage, garage_confidence = _infer_garage(
            listing["raw_description"], listing.get("garage")
        )
        baths_full = _infer_baths_full(listing["baths"], listing.get("baths_full"))
        year_built, stories = _resolve_year_and_stories(listing["raw_description"])
        confidence = "high" if garage_confidence == "high" else "low"

        valid.append(
            NormalizedListing(
                listing_id=listing["listing_id"],
                address=listing["address"],
                zip=listing["zip"],
                listing_price=float(listing["listing_price"]),
                sqft=int(listing["sqft"]),
                beds=int(listing["beds"]),
                baths=int(listing["baths"]),
                baths_full=baths_full,
                garage=garage,
                year_built=year_built,
                stories=stories,
                raw_description=listing["raw_description"],
                confidence=confidence,
            )
        )

    return {"valid_listings": valid, "skipped_listings": skipped}
