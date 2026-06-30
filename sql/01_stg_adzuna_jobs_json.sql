CREATE OR REPLACE VIEW stg.adzuna_jobs_json AS (
    SELECT
        jobs
    FROM raw.adzuna_jobs
    CROSS JOIN LATERAL json_array_elements(page_results -> 'results') AS jobs
);
