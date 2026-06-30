CREATE OR REPLACE VIEW stg.adzuna_jobs_typed AS (
    SELECT
        -- identifiers
        job_id,
        job_title,

        -- job details
        description,
        redirect_url,
        adref,

        -- company
        company_name,
        company_area,

        -- location
        location_name,
        location_area,

        -- category
        category_tag,
        category_label,

        -- contract / salary
        contract_type,
        contract_time,
        NULLIF(salary_min, '')::numeric AS salary_min,
        NULLIF(salary_max, '')::numeric AS salary_max,
        NULLIF(salary_is_predicted, '')::boolean AS salary_is_predicted,

        -- geo / timestamps
        NULLIF(created, '')::timestamptz AS created,
        NULLIF(latitude, '')::double precision AS latitude,
        NULLIF(longitude, '')::double precision AS longitude

    FROM stg.adzuna_jobs_extracted
);
