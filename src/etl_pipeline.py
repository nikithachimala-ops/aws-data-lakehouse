import logging
from pathlib import Path

import pandas as pd

from src.transformations import transform_data


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_pipeline():
    """Extract, transform, and load the e-commerce dataset."""

    logging.info("Starting ETL pipeline")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Extract
    logging.info("Extracting raw data")
    raw_df = pd.read_csv(RAW_DATA_PATH)
    input_rows = len(raw_df)

    # 2. Transform
    logging.info("Transforming data")
    clean_df = transform_data(raw_df)

    if clean_df.empty:
        raise ValueError("No valid records remain after transformation")

    # 3. Load
    logging.info("Saving transformed data")
    parquet_path = OUTPUT_DIR / "cleaned_orders.parquet"
    csv_path = OUTPUT_DIR / "cleaned_orders.csv"

    clean_df.to_parquet(parquet_path, index=False)
    clean_df.to_csv(csv_path, index=False)

    # 4. Report
    summary = {
        "input_rows": input_rows,
        "output_rows": len(clean_df),
        "rejected_rows": input_rows - len(clean_df),
        "total_revenue": round(
            float(clean_df["total_amount"].sum()), 2
        ),
        "parquet_file": str(parquet_path),
        "csv_file": str(csv_path),
    }

    logging.info("ETL pipeline completed successfully")
    logging.info("Summary: %s", summary)

    return summary


if __name__ == "__main__":
    run_pipeline()