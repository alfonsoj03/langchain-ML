from langchain_core.runnables import RunnableLambda

from scanner.nodes.fetch import fetch_listings
from scanner.nodes.filter import filter_valid
from scanner.nodes.normalize import normalize_listings
from scanner.nodes.predict import predict_prices
from scanner.nodes.report import generate_report
from scanner.nodes.score import score_opportunities
from scanner.nodes.summarize import summarize_flagged
from scanner.state import ScannerState


def _merge_step(step_fn):
    def run(state: ScannerState) -> ScannerState:
        update = step_fn(state)
        return {**state, **update}

    return run


def build_pipeline():
    return (
        RunnableLambda(_merge_step(fetch_listings))
        | RunnableLambda(_merge_step(filter_valid))
        | RunnableLambda(_merge_step(normalize_listings))
        | RunnableLambda(_merge_step(predict_prices))
        | RunnableLambda(_merge_step(score_opportunities))
        | RunnableLambda(_merge_step(summarize_flagged))
        | RunnableLambda(_merge_step(generate_report))
    )
