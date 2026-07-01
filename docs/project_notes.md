# Project Notes

## Project goal

Build a small end-to-end data pipeline that extracts job data from the Adzuna API, loads it into PostgreSQL, and transforms semi-structured JSON data into queryable outputs.

## Key design decisions

### Store raw API responses first

I chose to load the API response into PostgreSQL before transforming it.

Reason:

- Preserves the original source response.
- Makes debugging easier.
- Allows transformations to be changed later without calling the API again .

### Use Docker for PostgreSQL

I used Docker to run PostgreSQL locally.

Reason:

- Easier to recreate the database environment
- Keeps the project setup separate from my machine
- More realistic than relying on a manually installed local database

## Learning for Bugs

### psycopg2 parameter issue

I had an issue where psycopg2 did not treat a single value as a sequence because the tuple did not have a trailing comma.

Example:

```python
(Json(response))
```

### jsonb in PostgreSQL

Data is stored as `jsonb` by PostgreSQL, important to note how databases decided to store responses so right function can be used.