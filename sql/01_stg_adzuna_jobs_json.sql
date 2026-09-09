CREATE OR REPLACE VIEW stg.adzuna_jobs_json AS (
    SELECT
        job
    FROM {raw_table}
    CROSS JOIN LATERAL jsonb_array_elements(page_results -> 'results') AS job
);
