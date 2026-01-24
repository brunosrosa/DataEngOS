# Arquitetura de Pipeline: Sinergia Integration

**Status:** Draft
**Pattern:** Lambda Architecture (Simplified)

## 1. O Desafio da Impedância
Precisamos unir duas realidades temporais distintas:
1.  **Legacy Debt (Batch Mensal):** Alta latência, carga completa ou deltas grandes.
2.  **Transaction API (Streaming):** Baixa latência, eventos discretos.

**Solução:** Pipeline Desacoplado com Unificação na Camada Gold (Read-Time Integration).

---

## 2. Topologia de Dados (Data Flow)

### Camada Bronze (Ingestion)
*   **`stg_legacy_debt`**: Carrega o Excel "como está".
    *   *Quality Gate:* Valida schema. Se houver colunas novas não mapeadas, falha a task (Proteção contra Schema Drift).
*   **`stg_transaction_events`**: Stream direto do Webhook/Kafka.

### Camada Silver (Transformation & Privacy)
Aqui aplicamos as regras de negócio e Governança (PII).

#### A. Pipeline Batch (`int_legacy_debt_monthly`)
1.  **Select & Cast:** Seleciona colunas `contract_id`, `debt_amount`, `due_date`, `status`.
2.  **Sanitization:**
    *   `tax_id` (CPF) -> Remove `.` e `-`.
    *   Lógica `COALESCE(Doc_ID, CPF_Cliente)` para resolver a ambiguidade da coluna.
3.  **Hashing (Crucial):**
    *   Aplica `SHA256(cleaned_tax_id)` -> Gera `customer_hash`.
    *   *Descarte:* O CPF original é descartado desta tabela.
4.  **Materialização:** Tabla particionada por `ref_month`.

#### B. Pipeline Streaming (`int_live_risk_transactions`)
1.  **Flatten:** Extrai `data.customer.id` e `data.customer.risk_score`.
2.  **Hashing:**
    *   Aplica `SHA256(data.customer.id)` -> Gera `customer_hash` (Mesmo sal/algoritmo do Batch).
3.  **Materialização:** Tabela Append-Only ou Delta Table.

### Camada Gold (Unified View)
Aqui resolvemos a pergunta de negócio: "Qual o risco total?".

#### `fct_unified_risk_exposure`
Implementada como uma **View** (para garantir frescor) ou **Materialized View** (para performance), fazendo um **FULL OUTER JOIN** entre as Silvers.

```sql
WITH latest_legacy AS (
    SELECT customer_hash, debt_amount, created_at
    FROM int_legacy_debt_monthly
    WHERE ref_month = (SELECT MAX(ref_month) FROM int_legacy_debt_monthly) -- Pega o último snapshot
),

latest_api AS (
    SELECT customer_hash, risk_score, timestamp
    FROM int_live_risk_transactions
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_hash ORDER BY timestamp DESC) = 1 -- Pega o último evento
)

SELECT
    COALESCE(L.customer_hash, A.customer_hash) as customer_hash,
    L.debt_amount as legacy_debt_amount,
    A.risk_score as latest_risk_score,
    GREATEST(L.created_at, A.timestamp) as last_interaction_at,
    CASE
        WHEN L.customer_hash IS NOT NULL AND A.customer_hash IS NOT NULL THEN 'MERGED'
        WHEN L.customer_hash IS NOT NULL THEN 'LEGACY_ONLY'
        ELSE 'API_ONLY'
    END as data_source_origin
FROM latest_legacy L
FULL OUTER JOIN latest_api A ON L.customer_hash = A.customer_hash
```

---

## 3. Garantias de Governança
1.  **Resiliência:** Se o Excel atrasar, a CTE `latest_legacy` continua pegando o mês anterior. O pipeline não quebra. A API continua atualizando os Scores.
2.  **Privacidade:** O Join é feito EXCLUSIVAMENTE via Hash. O CPF cru nunca toca a camada Gold.
3.  **Schema Drift:** A validação ocorre na entrada do Pipeline A. Se falhar, o Pipeline B e a View C continuam operando (apenas com dados legados "vencidos", o que é aceitável pelo SLA mensal).
