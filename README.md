AWS Data Lakehouse with Automated ETL Pipeline

Project Overview

A data engineering project that extracts, cleans, validates, and transforms sales data into CSV and Parquet datasets. DuckDB provides SQL-based analytics, while incremental processing tracks previously processed order IDs.

The current implementation runs locally and does not require paid cloud services.

Architecture

1. Source: Read raw sales data from a CSV file.
2. Extract: Load the source data using Pandas.
3. Transform: Clean records, remove duplicates, validate data types, and calculate order totals.
4. Data Quality: Check required columns, unique order IDs, positive quantities, non-negative prices, and correct totals.
5. Incremental Processing: Track processed order IDs to avoid adding the same orders again.
6. Storage: Save cumulative datasets in CSV and Parquet formats.
7. Analytics: Query processed Parquet data using DuckDB and SQL.
8. Testing: Verify transformations and data quality rules using pytest.

Planned AWS Architecture

- Amazon S3: Store raw and processed datasets.
- AWS Glue: Run managed ETL jobs.
- Amazon Athena: Query data using SQL.
- AWS IAM: Manage access permissions.

These AWS integrations are planned enhancements. The current project runs locally and does not deploy or integrate these AWS services.

Technologies Used

- Python
- Pandas
- DuckDB
- SQL
- Apache Parquet
- Pytest
- Git and GitHub

Features

- Extract raw CSV sales data.
- Remove duplicate order IDs.
- Clean and validate records.
- Calculate order-level revenue.
- Extract year and month for analytics.
- Validate data quality before loading.
- Support incremental processing by order ID.
- Export processed data to CSV and Parquet.
- Perform revenue, regional, and product analytics using SQL.
- Log pipeline execution.
- Include automated tests.

Project Structure

aws-data-lakehouse/
├── data/
│   └── raw_data.csv
├── src/
│   ├── transformations.py
│   ├── etl_pipeline.py
│   ├── data_quality.py
│   └── analytics.py
├── tests/
│   ├── conftest.py
│   └── test_etl.py
├── output/
├── run_project.py
├── requirements.txt
└── README.md

Installation

Create a virtual environment:

python -m venv .venv

Activate it in Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Run the Project

Run the complete workflow:

python run_project.py

Run the ETL pipeline separately:

python -m src.etl_pipeline

Run SQL analytics separately:

python -m src.analytics

Run automated tests:

pytest -q

Output

The pipeline generates processed datasets and incremental-processing state files in the "output/" directory:

- "cleaned_orders.csv"
- "cleaned_orders.parquet"
- "processed_order_ids.csv"

Current Limitations

- AWS S3, AWS Glue, and Amazon Athena are not yet integrated.
- Incremental processing identifies new order IDs but does not yet handle updates to previously processed orders.
- Output data and processing state are saved separately, so failure recovery and transactional consistency need improvement.
- The sample dataset is intended for demonstration.

Future Enhancements

- Integrate AWS cloud storage and managed ETL services.
- Handle updates to existing records.
- Improve recovery and transactional processing.
- Add pipeline scheduling and monitoring.

License

This project is intended for learning and portfolio demonstration. Add a formal open-source license if you want to grant others specific reuse rights.

Author

Chimala Nikhitha