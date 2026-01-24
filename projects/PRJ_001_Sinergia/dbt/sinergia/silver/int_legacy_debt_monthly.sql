{{ config(
    materialized='incremental',
    partition_by={'field': 'ref_month', 'data_type': 'date'},
    unique_key='contract_id'
) }}

WITH source AS (
    SELECT * FROM {{ source('sinergia', 'stg_legacy_debt') }}
),

cleaned AS (
    SELECT
        ID_Contrato as contract_id,
        
        -- Logic: Resolver ambiguidade de colunas (Schema Drift handling)
        COALESCE(
            NULLIF(REGEXP_REPLACE(Doc_ID, '[^0-9]', ''), ''), 
            NULLIF(REGEXP_REPLACE(CPF_Cliente, '[^0-9]', ''), '')
        ) as tax_id_clean,

        -- Parse de formatos (DD/MM/AAAA -> DATE)
        PARSE_DATE('%d/%m/%Y', Data_Vencimento) as due_date,
        
        CAST(Valor_Devido as NUMERIC) as debt_amount,
        Status_Divida as status,
        DATE_TRUNC(CURRENT_DATE(), MONTH) as ref_month, -- Assumindo carga mensal corrente
        created_at

    FROM source
)

SELECT
    contract_id,
    
    -- PII BARRIER: Hashing (Nenhum CPF cru sai daqui)
    SHA256(tax_id_clean) as customer_hash,
    
    debt_amount,
    due_date,
    status,
    ref_month,
    created_at

FROM cleaned
WHERE tax_id_clean IS NOT NULL -- descarta registros órfãos de doc
