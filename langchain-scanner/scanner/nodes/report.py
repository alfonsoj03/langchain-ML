import csv
import json
from pathlib import Path

from scanner.config import ROOT_DIR
from scanner.state import ScannerState


def generate_report(state: ScannerState) -> dict:
    report_dir = Path(state.get("report_path", ROOT_DIR))
    report_dir.mkdir(parents=True, exist_ok=True)

    scored_listings = state.get("scored_listings", [])
    flagged_listings = state.get("flagged_listings", [])
    skipped_listings = state.get("skipped_listings", [])
    raw_listings = state.get("raw_listings", [])

    report = {
        "summary": {
            "scanned": len(raw_listings),
            "scored": len(scored_listings),
            "skipped": len(skipped_listings),
            "flagged": len(flagged_listings),
        },
        "flagged_listings": flagged_listings,
        "scored_listings": scored_listings,
        "skipped_listings": skipped_listings,
    }

    json_path = report_dir / "scanner_report.json"
    csv_path = report_dir / "scanner_report.csv"

    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    fieldnames = [
        "listing_id",
        "address",
        "listing_price",
        "predicted_price",
        "gap_pct",
        "flagged",
        "confidence",
        "llm_summary",
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in scored_listings:
            writer.writerow({k: row.get(k) for k in fieldnames})

    _print_summary(report)
    return {"report_path": str(report_dir)}


def _print_summary(report: dict) -> None:
    summary = report["summary"]
    print("\n=== Investment Scanner Report ===")
    print(f"Scanned:  {summary['scanned']}")
    print(f"Scored:   {summary['scored']}")
    print(f"Skipped:  {summary['skipped']}")
    print(f"Flagged:  {summary['flagged']}")
    if report["flagged_listings"]:
        print("\nTop opportunities:")
        for item in report["flagged_listings"][:5]:
            gap = item["gap_pct"] * 100
            print(
                f"  - {item['address']}: "
                f"list ${item['listing_price']:,.0f} | "
                f"pred ${item['predicted_price']:,.0f} | "
                f"gap {gap:.1f}%"
            )
            if item.get("llm_summary"):
                print(f"    Summary: {item['llm_summary']}")
