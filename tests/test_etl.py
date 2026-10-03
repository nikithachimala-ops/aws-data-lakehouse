import pandas as pd

from src.transformations import transform_data


def test_transform_data_calculates_revenue():
    raw_data = pd.DataFrame(
        {
            "order_id": [1, 2],
            "order_date": ["2026-09-01", "2026-09-02"],
            "customer_id": ["C101", "C102"],
            "product": ["Laptop", "Mouse"],
            "category": ["Electronics", "Accessories"],
            "quantity": [1, 2],
            "unit_price": [1000, 500],
            "region": ["South", "North"],
        }
    )

    result = transform_data(raw_data)

    assert len(result) == 2
    assert result["total_amount"].tolist() == [1000, 1000]
    assert result["year"].tolist() == [2026, 2026]


def test_transform_data_removes_duplicate_orders():
    raw_data = pd.DataFrame(
        {
            "order_id": [1, 1],
            "order_date": ["2026-09-01", "2026-09-01"],
            "customer_id": ["C101", "C101"],
            "product": ["Laptop", "Laptop"],
            "category": ["Electronics", "Electronics"],
            "quantity": [1, 1],
            "unit_price": [1000, 1000],
            "region": ["South", "South"],
        }
    )

    result = transform_data(raw_data)

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 1


def test_transform_data_removes_invalid_orders():
    raw_data = pd.DataFrame(
        {
            "order_id": [1, 2],
            "order_date": ["2026-09-01", "2026-09-02"],
            "customer_id": ["C101", "C102"],
            "product": ["Laptop", "Mouse"],
            "category": ["Electronics", "Accessories"],
            "quantity": [1, 0],
            "unit_price": [1000, 500],
            "region": ["South", "North"],
        }
    )

    result = transform_data(raw_data)

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 1