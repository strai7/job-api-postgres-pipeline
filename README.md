# job-api-postgres-pipeline

## What does this project do?

This project is a Python data pipeline that extracts job data from the Adzuna API, loads the data into a local PostgreSQL database, and applies SQL transformations to make the data easier to query and analyse.

The goal was to practise the core data engineering workflow:

1. Extract data from an external API
2. Load raw/semi-structured data into a database
3. Transform the data using SQL
4. Document and version-control the project using Git

## Data source

The data comes from the Adzuna Job Search API.

The API returns paginated JSON responses containing job posting data such as job title, company, location, category, salary information, description, and redirect URLs.

## Data attribution

This project uses data from The Adzuna API for personal learning and portfolio purposes.

Adzuna is the source of the salary and vacancy data used in this project.  
Source: The Adzuna API - https://www.adzuna.co.uk/

Raw API response data is not included in this repository. The pipeline can be run locally by users with their own Adzuna API credentials.

## How does the pipeline work?

The pipeline follows a simple ELT-style process:

1. A Python script sends requests to the Adzuna API using the `requests` library.
2. The script handles paginated API responses.
3. The returned JSON data is loaded into a local PostgreSQL database using `psycopg2`.
4. SQL transformations extract useful values from the JSON response and convert them into structured columns.
5. The transformed data can then be queried in PostgreSQL.

## Where is the data stored?

The data is stored in a local PostgreSQL database.

Docker is used to run the PostgreSQL database locally, making it easier to recreate the database environment when needed.

## What SQL transformations did you create?

The SQL transformations include:

- Extracting values from JSON responses into structured rows and columns
- Casting fields into appropriate data types
- Handling null values
- Creating cleaner queryable outputs from the raw API data

## What did I learn?

### API interaction

I practised working with an external API, including:

- Sending parameterised requests
- Handling paginated responses
- Reading JSON responses
- Moving API data into a database

### PostgreSQL and SQL

I improved my understanding of:

- Loading data into PostgreSQL
- Querying JSON data
- Extracting nested values from JSON fields
- Structuring semi-structured data into cleaner relational outputs

### Git and project workflow

I practised a more professional Git workflow, including:

- Creating and switching branches
- Checking changes with `git status` and `git diff`
- Staging and committing changes
- Pushing branches to GitHub
- Protecting the main branch using pull requests

### Data engineering design

This project helped me understand why ELT can be useful.

By loading the API response first and applying transformations later, the ingestion step stays simpler and the raw source data is preserved for debugging or future transformation changes.

## What would I improve in v2?

In a future version, I would improve the project by:

- Adding incremental loading so the pipeline only loads new or changed job records
- Adding more robust error handling and logging
- Adding tests for the API extraction and transformation logic
- Loading additional datasets to make the project more useful analytically
- Adding a scheduled run so the pipeline can update automatically
