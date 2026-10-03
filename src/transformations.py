import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform raw e-commerce order data."""

    # Work on a copy so the original data remains unchanged
    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Convert data types
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )

    # Remove records missing essential values
    required_columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product",
        "quantity",
        "unit_price",
    ]
    df = df.dropna(subset=required_columns)

    # Remove invalid order values
    df = df[
        (df["order_id"] > 0)
        & (df["quantity"] > 0)
        & (df["unit_price"] >= 0)
    ]

    # Convert quantity and order ID to integers
    df["order_id"] = df["order_id"].astype("int64")
    df["quantity"] = df["quantity"].astype("int64")

    # Standardize text fields
    for column in ["customer_id", "product", "category", "region"]:
        df[column] = df[column].astype("string").str.strip()

    # Calculate total revenue for each order
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # Add year and month for analytics
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month

    # Return a clean DataFrame
    return df.reset_index(drop=True)