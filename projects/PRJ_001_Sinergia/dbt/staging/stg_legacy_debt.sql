
{{ config(materialized='view') }}

WITH source AS (
    SELECT * FROM {{ source('sinergia', 'base_inadimplencia_historica_vFinal_REAL.xlsx') }}
)

SELECT
    -- Scaffolding columns from contract
    contract_id, -- Identificador único da dívida.
    tax_id, -- CPF do cliente. Deve ser higienizado (dots/dashes) e hashed.
    debt_amount, -- Valor total da dívida no momento da extração.
    due_date, -- Data original do vencimento. Requer parse dd/mm/yyyy.
    status, -- Status operacional (ex: Aberto, Renegociado).

FROM source