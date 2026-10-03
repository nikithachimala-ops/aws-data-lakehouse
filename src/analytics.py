from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PARQUET_FILE = PROJECT_ROOT / "output" / "cleaned_orders.parquet"


def run_analytics():
    if not PARQUET_FILE.exists():
        raise FileNotFoundError(
            "Cleaned Parquet file not found. Run the ETL pipeline first."
        )

    con = duckdb.connect(database=":memory:")

    print("\n=== Total Revenue ===")
    print(
        con.execute(
            "SELECT ROUND(SUM(total_amount), 2) AS total_revenue "
            "FROM read_parquet(?)",
            [str(PARQUET_FILE)],
        ).df().to_string(index=False)
    )

    print("\n=== Revenue by Region ===")
    print(
        con.execute(
            """
            SELECT region,
                   ROUND(SUM(total_amount), 2) AS revenue
            FROM read_parquet(?)
            GROUP BY region
            ORDER BY revenue DESC
            """,
            [str(PARQUET_FILE)],
        ).df().to_string(index=False)
    )

    print("\n=== Top-Selling Products by Revenue ===")
    print(
        con.execute(
            """
            SELECT product,
                   SUM(quantity) AS units_sold,
                   ROUND(SUM(total_amount), 2) AS revenue
            FROM read_parquet(?)
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 5
            """,
            [str(PARQUET_FILE)],
        ).df().to_string(index=False)
    )

    con.close()


if __name__ == "__main__":
    run_analytics()