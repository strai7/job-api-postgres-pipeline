CREATE OR REPLACE VIEW stg.adzuna_jobs_extracted AS (
    SELECT
        -- identifiers
        job ->> 'id' AS job_id,
        job ->> 'title' AS job_title,

        -- job details
        job ->> 'description' AS description,
        job ->> 'redirect_url' AS redirect_url,
        job ->> 'adref' AS adref,

        -- company
        job -> 'company' ->> 'display_name' AS company_name,
        job -> 'company' ->> 'area' AS company_area,

        -- location
        job -> 'location' ->> 'display_name' AS location_name,
        job -> 'location' ->> 'area' AS location_area,

        -- category
        job -> 'category' ->> 'tag' AS category_tag,
        job -> 'category' ->> 'label' AS category_label,

        -- contract / salary
        job ->> 'contract_type' AS contract_type,
        job ->> 'contract_time' AS contract_time,
        job ->> 'salary_min' AS salary_min,
        job ->> 'salary_max' AS salary_max,
        job ->> 'salary_is_predicted' AS salary_is_predicted,

        -- geo / timestamps
        job ->> 'created' AS created,
        job ->> 'latitude' AS latitude,
        job ->> 'longitude' AS longitude

    FROM stg.adzuna_jobs_json
);
