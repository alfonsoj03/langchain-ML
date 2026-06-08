import argparse
from pathlib import Path

from dotenv import load_dotenv

from scanner.config import ROOT_DIR, SCAN_LOCATION, SCAN_MAX_RESULTS
from scanner.pipeline import build_pipeline


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Arizona investment opportunity scanner")
    parser.add_argument("--location", default=SCAN_LOCATION)
    parser.add_argument("--max-results", type=int, default=SCAN_MAX_RESULTS)
    parser.add_argument("--report-path", default=str(ROOT_DIR))
    args = parser.parse_args()

    pipeline = build_pipeline()
    result = pipeline.invoke(
        {
            "location": args.location,
            "max_results": args.max_results,
            "report_path": args.report_path,
        }
    )

    flagged = len(result.get("flagged_listings", []))
    print(f"\nDone. {flagged} investment opportunities flagged.")
    print(f"Report: {Path(args.report_path) / 'scanner_report.json'}")


if __name__ == "__main__":
    main()
