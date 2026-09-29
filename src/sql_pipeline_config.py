TRANSFORMATION_FILES = [
    "01_stg_adzuna_jobs_json.sql",
    "02_stg_adzuna_jobs_extracted.sql",
    "03_stg_adzuna_jobs_typed.sql",
]

UPSERT_FILES = [
    "04_create_jobs_table.sql",
    "05_upsert_core_jobs_table.sql",
]