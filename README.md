AWS Data Lakehouse with Automated ETL Pipeline

Project Overview

This project implements an automated data engineering pipeline that extracts raw e-commerce transaction data, cleans and transforms it using Python, and stores the processed data in CSV and Parquet formats for analytics.

The pipeline is designed with an AWS data lakehouse architecture in mind and is developed and tested locally using free, open-source tools.

Architecture

Raw E-commerce CSV
        |
   Python ETL Pipeline
        |
 Data Cleaning & Validation
        |
 Revenue & Date Features
        |
 Processed Data
    /        \      
  CSV       Parquet
        |
 Analytics & Reporting

Planned AWS Architecture

- Amazon S3: Store raw and processed datasets.
- AWS Glue: Run managed ETL jobs.
- Amazon Athena: Query data using SQL.
- AWS IAM: Manage access permissions.

These AWS integrations are planned architecture components; the current implementation runs locally and does not require paid AWS services.

Technologies Used

- Python
- Pandas
- PyArrow
- Pytest
- Boto3
- Amazon S3, AWS Glue and Amazon Athena (planned integration)
- Git and GitHub

Features

- Extracts raw CSV transaction data.
- Removes duplicate order IDs.
- Validates required fields and numeric values.
- Handles invalid dates and missing values.
- Calculates order-level revenue.
- Extracts year and month for analytics.
- Exports cleaned data to CSV and Parquet.
- Logs pipeline execution.
- Includes automated tests using Pytest.

Project Structure

aws-data-lakehouse/
├── data/
│   └── raw_data.csv
├── src/
│   ├── etl_pipeline.py
│   └── transformations.py
├── tests/
│   └── test_etl.py
├── output/
│   ├── cleaned_orders.csv
│   └── cleaned_orders.parquet
├── docs/
│   └── architecture.md
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

Installation

Create and activate a Python virtual environment.

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Run the Pipeline

python -m src.etl_pipeline

Run Automated Tests

python -m pytest tests -v

Output

The pipeline generates:

- "output/cleaned_orders.csv"
- "output/cleaned_orders.parquet"

The sample dataset contains 15 transaction records. The pipeline calculates revenue for each order and generates date-based analytics columns.

Future Enhancements

- Integrate Amazon S3 for cloud data storage.
- Automate managed transformations using AWS Glue.
- Create an AWS Glue Data Catalog database and table.
- Query processed Parquet data using Amazon Athena.
- Add data-quality metrics and pipeline monitoring.
- Add scheduled execution and partitioned datasets.

Cost Considerations

The current pipeline runs locally using free, open-source software. AWS services are not provisioned by the current implementation. Cloud integration should be configured only after reviewing the applicable pricing and free-tier limits.

Author

Chimala Nikhitha

Developed as a data engineering portfolio project to demonstrate ETL development, data quality, Parquet processing, automated testing, and cloud data architecture concepts.