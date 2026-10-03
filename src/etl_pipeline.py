import logging
from pathlib import Path

import pandas as pd

from src.transformations import transform_data
from src.data_quality import validate_data


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"

PARQUET_PATH = OUTPUT_DIR / "cleaned_orders.parquet"
CSV_PATH = OUTPUT_DIR / "cleaned_orders.csv"
STATE_PATH = OUTPUT_DIR / "processed_order_ids.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_pipeline():
    """Extract, validate, and incrementally load order data."""

    logging.info("Starting incremental ETL pipeline")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Extract
    raw_df = pd.read_csv(RAW_DATA_PATH)
    input_rows = len(raw_df)

    # 2. Transform
    clean_df = transform_data(raw_df)

    if clean_df.empty:
        raise ValueError(
            "No valid records remain after transformation"
        )

    # 3. Validate
    quality_report = validate_data(clean_df)
    logging.info("Data quality report: %s", quality_report)

    if not quality_report["passed"]:
        raise ValueError(
            f"Data quality validation failed: {quality_report}"
        )

    # 4. Load processing state
    if STATE_PATH.exists():
        state_df = pd.read_csv(STATE_PATH)

        if "order_id" not in state_df.columns:
            raise ValueError(
                "Processing state file must contain order_id"
            )

        processed_ids = set(
            pd.to_numeric(
                state_df["order_id"], errors="raise"
            ).astype(int)
        )
    else:
        processed_ids = set()

    # 5. Identify new orders
    new_df = clean_df[
        ~clean_df["order_id"].isin(processed_ids)
    ].copy()

    # 6. Read and combine existing output
    if PARQUET_PATH.exists():
        existing_df = pd.read_parquet(PARQUET_PATH)

        combined_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True,
        )

        combined_df = combined_df.drop_duplicates(
            subset=["order_id"],
            keep="last",
        )
    else:
        combined_df = new_df.copy()

    # 7. Save cumulative output
    if not combined_df.empty:
        combined_df.to_parquet(
            PARQUET_PATH,
            index=False,
        )
        combined_df.to_csv(
            CSV_PATH,
            index=False,
        )

    # 8. Update state after writing output
    all_processed_ids = sorted(
        processed_ids
        | set(new_df["order_id"].astype(int))
    )

    pd.DataFrame(
        {"order_id": all_processed_ids}
    ).to_csv(
        STATE_PATH,
        index=False,
    )

    # 9. Generate summary
    summary = {
        "input_rows": input_rows,
        "valid_rows": len(clean_df),
        "new_rows_added": len(new_df),
        "total_rows_stored": len(combined_df),
        "rejected_rows": input_rows - len(clean_df),
        "quality_checks_passed": quality_report["passed_count"],
        "quality_checks_total": quality_report["total_checks"],
        "total_revenue": round(
            float(combined_df["total_amount"].sum()), 2
        ),
        "parquet_file": str(PARQUET_PATH),
        "csv_file": str(CSV_PATH),
        "state_file": str(STATE_PATH),
    }

    logging.info(
        "Incremental ETL completed successfully"
    )
    logging.info("Summary: %s", summary)

    return summary


if __name__ == "__main__":
    run_pipeline()