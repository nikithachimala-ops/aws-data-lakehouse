Data Lakehouse Architecture

1. Overview

The project implements a Python-based ETL pipeline for processing e-commerce transaction data. The current implementation runs locally and produces analytics-ready CSV and Parquet files.

2. Data Flow

1. Extract: Read raw transaction data from "data/raw_data.csv".
2. Transform: Standardize columns, remove duplicate orders, validate fields, handle invalid records, and calculate total revenue.
3. Load: Save the processed dataset to CSV and Parquet files in the "output/" directory.
4. Validate: Run automated tests using Pytest.
5. Analyze: Use the processed dataset for SQL-based analytics or reporting extensions.

3. Planned AWS Architecture

Component| Responsibility
Amazon S3| Store raw and processed data
AWS Glue| Execute managed ETL jobs
AWS Glue Data Catalog| Maintain table metadata
Amazon Athena| Query data using SQL
AWS IAM| Control permissions

The AWS architecture describes the planned cloud extension. The current Python implementation does not provision or execute these AWS services.

4. Data Zones

- Raw zone: Original CSV data, preserved as the input.
- Processed zone: Cleaned, validated, analytics-ready Parquet data.
- Analytics layer: SQL queries and reporting built on processed data.

In a future AWS deployment, these zones can be represented by separate Amazon S3 prefixes.

5. Data Quality

The pipeline currently supports duplicate removal, required-field validation, numeric conversion, invalid-record filtering, and revenue calculation. Automated tests validate key transformation behavior.

6. Cost-Aware Development

Local development uses Python and open-source libraries. Cloud deployment is optional and must be evaluated against the current pricing, usage limits, and applicable account terms before provisioning resources.