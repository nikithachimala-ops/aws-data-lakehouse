import pandas as pd


def validate_data(df: pd.DataFrame) -> dict:
    """Validate transformed order data."""

    required_columns = [
        "order_id",
        "quantity",
        "unit_price",
        "total_amount",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        checks = {
            "required_columns_present": False,
            "no_missing_order_ids": False,
            "unique_order_ids": False,
            "positive_quantities": False,
            "non_negative_prices": False,
            "correct_total_amount": False,
        }

        return {
            "passed": False,
            "checks": checks,
            "passed_count": 0,
            "total_checks": len(checks),
            "missing_columns": missing_columns,
        }

    checks = {
        "required_columns_present": True,
        "no_missing_order_ids": bool(
            not df["order_id"].isna().any()
        ),
        "unique_order_ids": bool(
            not df["order_id"].duplicated().any()
        ),
        "positive_quantities": bool(
            (df["quantity"] > 0).all()
        ),
        "non_negative_prices": bool(
            (df["unit_price"] >= 0).all()
        ),
        "correct_total_amount": bool(
            (
                df["total_amount"]
                == df["quantity"] * df["unit_price"]
            ).all()
        ),
    }

    return {
        "passed": all(checks.values()),
        "checks": checks,
        "passed_count": sum(checks.values()),
        "total_checks": len(checks),
    }