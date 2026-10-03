import pandas as pd

from src.transformations import transform_data
from src.data_quality import validate_data


def test_transform_calculates_total_amount_and_date_fields():
    df = pd.DataFrame({
        "order_id": [1001],
        "order_date": ["2026-09-01"],
        "customer_id": ["C101"],
        "product": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [2],
        "unit_price": [100.0],
        "region": ["South"],
    })

    result = transform_data(df)

    assert len(result) == 1
    assert result.iloc[0]["total_amount"] == 200.0
    assert result.iloc[0]["year"] == 2026
    assert result.iloc[0]["month"] == 9


def test_transform_removes_duplicate_orders():
    df = pd.DataFrame({
        "order_id": [1001, 1001],
        "order_date": ["2026-09-01", "2026-09-01"],
        "customer_id": ["C101", "C101"],
        "product": ["Laptop", "Laptop"],
        "category": ["Electronics", "Electronics"],
        "quantity": [1, 1],
        "unit_price": [100.0, 100.0],
        "region": ["South", "South"],
    })

    result = transform_data(df)

    assert len(result) == 1
    assert result["order_id"].is_unique


def test_transform_removes_invalid_orders():
    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "order_date": ["2026-09-01", "2026-09-02"],
        "customer_id": ["C101", "C102"],
        "product": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 0],
        "unit_price": [100.0, 50.0],
        "region": ["South", "North"],
    })

    result = transform_data(df)

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 1001


def test_valid_data_passes_all_quality_checks():
    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "quantity": [2, 1],
        "unit_price": [100.0, 250.0],
        "total_amount": [200.0, 250.0],
    })

    report = validate_data(df)

    assert report["passed"] is True
    assert report["passed_count"] == report["total_checks"]
    assert report["total_checks"] == 6


def test_duplicate_order_ids_fail_validation():
    df = pd.DataFrame({
        "order_id": [1001, 1001],
        "quantity": [1, 2],
        "unit_price": [100.0, 100.0],
        "total_amount": [100.0, 200.0],
    })

    report = validate_data(df)

    assert report["passed"] is False
    assert report["checks"]["unique_order_ids"] is False


def test_incorrect_total_amount_fails_validation():
    df = pd.DataFrame({
        "order_id": [1001],
        "quantity": [2],
        "unit_price": [100.0],
        "total_amount": [150.0],
    })

    report = validate_data(df)

    assert report["passed"] is False
    assert report["checks"]["correct_total_amount"] is False