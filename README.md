# Job API to PostgreSQL Pipeline

A Python-based ELT pipeline that extracts UK job listings from the Adzuna API, stores and transforms the data in PostgreSQL, and uses Apache Airflow for scheduled orchestration.

## Tech Stack

- **Languages:** Python, SQL
- **Database:** PostgreSQL
- **Orchestration:** Apache Airflow
- **Infrastructure:** Docker
- **Testing:** pytest
- **Other:** REST API, requests, psycopg2, Git, GitHub

## Features & Implementation

- **API Ingestion:** Extracts job listings from the Adzuna REST API using Python, with pagination support for multiple pages of results.
- **Raw Data Storage:** Preserves original API responses as JSONB in PostgreSQL landing tables.
- **SQL Transformations:** Uses staging views to extract, clean and type fields including job IDs, titles, companies, locations and salaries.
- **Database Architecture:** Organises data into raw, staging and core layers.
- **Data Validation:** Checks for missing, blank and duplicate job IDs before updating the core dataset.
- **Upsert Logic:** Inserts new job records and updates existing records using PostgreSQL `ON CONFLICT`, with job IDs as primary keys.
- **Workflow Orchestration:** Uses Apache Airflow to coordinate pipeline tasks and schedule daily execution, including ingestion retries with exponential backoff.
- **Testing & Logging:** Implements Python logging, error handling and unit tests using pytest.
- **Containerisation:** Uses Docker to run local services and configure connections between Airflow and PostgreSQL.

## Current Status

The pipeline supports end-to-end extraction, loading, transformation, validation and scheduled orchestration.

Currently, each execution retrieves up to five pages of results and updates the core jobs table.

## Data Source

Job listing data is provided by the [Adzuna API](https://developer.adzuna.com/).
