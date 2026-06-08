from langchain_core.tools import tool


@tool
def infer_garage_from_description(description: str) -> int:
    """Infer garage spaces from a property description. Return 0 if unknown."""
    import re

    match = re.search(
        r"(\d+)\s*[- ]?\s*car\s+garage|garage[:\s]+(\d+)|(\d+)\s+car",
        description,
        re.IGNORECASE,
    )
    if match:
        value = next(g for g in match.groups() if g is not None)
        return int(value)
    return 0
