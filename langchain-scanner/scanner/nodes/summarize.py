from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from scanner.config import GEMINI_MODEL, GOOGLE_API_KEY, MODEL_MAPE
from scanner.state import ScannerState


def _build_summary_chain():
    prompt = PromptTemplate.from_template(
        "You are a real estate investment analyst. "
        "Write a 2-sentence investment rationale for this listing.\n\n"
        "Address: {address}\n"
        "Listing price: ${listing_price:,.0f}\n"
        "Predicted value: ${predicted_price:,.0f}\n"
        "Estimated upside: {gap_pct:.1%}\n"
        f"Model error (MAPE): {MODEL_MAPE:.1%}"
    )
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.2)
    return prompt | llm | StrOutputParser()


def summarize_flagged(state: ScannerState) -> dict:
    scored_listings = state.get("scored_listings", [])
    if not scored_listings or not GOOGLE_API_KEY:
        return {}

    chain = _build_summary_chain()
    summaries: dict[str, str] = {}

    for item in scored_listings:
        if not item.get("flagged"):
            continue
        summaries[item["listing_id"]] = chain.invoke(
            {
                "address": item["address"],
                "listing_price": item["listing_price"],
                "predicted_price": item["predicted_price"],
                "gap_pct": item["gap_pct"],
            }
        )

    updated_scored = []
    for item in scored_listings:
        updated = dict(item)
        updated["llm_summary"] = summaries.get(item["listing_id"], item.get("llm_summary", ""))
        updated_scored.append(updated)

    flagged_listings = [item for item in updated_scored if item["flagged"]]
    return {"scored_listings": updated_scored, "flagged_listings": flagged_listings}
