import logging

from src.etl_pipeline import run_pipeline
from src.analytics import run_analytics


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    print("Starting Data Lakehouse Pipeline...")

    summary = run_pipeline()

    print("\n=== ETL Pipeline Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== SQL Analytics ===")
    run_analytics()

    print("\nComplete workflow finished successfully!")


if __name__ == "__main__":
    main()