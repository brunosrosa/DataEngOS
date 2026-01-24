{{ config(
    materialized='view',
    tags=['gold', 'risk', 'regulatory']
) }}

WITH latest_legacy AS (
    SELECT 
        customer_hash, 
        SUM(debt_amount) as total_legacy_debt, -- Agrega dívidas se houver >1 contrato
        MAX(created_at) as legacy_updated_at
    FROM {{ ref('int_legacy_debt_monthly') }}
    WHERE ref_month = (SELECT MAX(ref_month) FROM {{ ref('int_legacy_debt_monthly') }})
    GROUP BY 1
),

latest_api AS (
    SELECT 
        customer_hash, 
        risk_score, 
        event_timestamp
    FROM {{ ref('int_live_risk_transactions') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_hash ORDER BY event_timestamp DESC) = 1
)

SELECT
    -- Key Unification
    COALESCE(L.customer_hash, A.customer_hash) as customer_hash,
    
    -- Business Metrics
    COALESCE(L.total_legacy_debt, 0) as legacy_debt_amount,
    A.risk_score as latest_risk_score,
    
    -- Lineage Logic
    GREATEST(L.legacy_updated_at, A.event_timestamp) as last_interaction_at,
    CASE
        WHEN L.customer_hash IS NOT NULL AND A.customer_hash IS NOT NULL THEN 'MERGED'
        WHEN L.customer_hash IS NOT NULL THEN 'LEGACY_ONLY'
        ELSE 'API_ONLY'
    END as data_source_origin

FROM latest_legacy L
FULL OUTER JOIN latest_api A ON L.customer_hash = A.customer_hash
