{{ config(
    materialized='incremental',
    unique_key='transaction_id'
) }}

WITH source AS (
    SELECT * FROM {{ source('sinergia', 'stg_transaction_events') }}
),

flattened AS (
    SELECT
        data.transaction_id as transaction_id,
        
        -- JSON Extraction (syntax example for BigQuery/StandardSQL)
        data.customer.id as raw_customer_id,
        CAST(data.customer.risk_score as FLOAT64) as risk_score,
        
        TIMESTAMP(data.timestamp) as event_timestamp,
        ingested_at

    FROM source
)

SELECT
    transaction_id,
    
    -- PII BARRIER: Hashing
    SHA256(REGEXP_REPLACE(raw_customer_id, '[^0-9]', '')) as customer_hash,
    
    risk_score,
    event_timestamp,
    ingested_at

FROM flattened
WHERE raw_customer_id IS NOT NULL
