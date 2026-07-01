CREATE OR REPLACE VIEW stg.adzuna_jobs_json AS (
    SELECT
        job
    FROM raw.adzuna_jobs
    CROSS JOIN LATERAL jsonb_array_elements(page_results -> 'results') AS job
);
