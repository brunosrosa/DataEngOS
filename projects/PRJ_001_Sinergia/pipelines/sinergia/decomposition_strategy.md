# FASE 0: DECOMPOSITION STRATEGY
## Projeto: Sinergia (Legacy "CredFácil" Integration)

**Arquiteto:** DataEngOS Architect
**Data:** 24/01/2026

---

### 1. Análise de Complexidade (The "Chaos" Factor)
Este projeto possui **Alta Complexidade Acidental** devido à fonte Legada (Excel/Sharepoint) e requisitos conflitantes de latência (Batch Mensal vs Real-time).

**Riscos Identificados:**
1.  **Acoplamento Temporal:** Tentar unir um processo D-5 (Excel) com um Real-time (API) em um único pipeline monolítico causará falhas. Se o Excel atrasar, o Real-time para.
2.  **Qualidade de Dados:** O Excel é instável ("Schema Drift"). A API é estruturada mas aninhada.
3.  **Compliance:** PII deve ser tratado *antes* da unificação para evitar vazamento em logs ou tabelas finais.

---

### 2. Estratégia de Decomposição (Sub-Products)
Para garantir a **Resiliência** solicitada, aplicaremos o padrão **Lambda Architecture (Simplificado)** ou **Multi-Speed Pipelines**.

Não construiremos "um pipeline". Construiremos **3 Sub-Produtos de Dados Independentes**:

#### 🟦 SUB-PRODUTO A: "Legacy Debt Foundation" (Batch)
*Foco: Robustez e Limpeza*
*   **Input:** Arquivo Excel (Sharepoint/Email).
*   **Contrato:** `legacy_debt.yaml` (Definição estrita do schema esperado).
*   **Tratamento (Bronze -> Silver):**
    *   **Higienização de CPF:** Remover `.` e `-`. Resolver conflito `Doc_ID` vs `CPF_Cliente`.
    *   **Schema Drift Guard:** Validação pré-ingestão. Se mudar colunas -> Alerta e *não* processa (Fail Fast), mas **não** para o Sub-Produto B.
    *   **Anonimização:** Hash SHA256 do CPF.
*   **Output:** Tabela Silver `int_legacy_debt_monthly` (Particionada por Mês de Referência).

#### 🟩 SUB-PRODUTO B: "Live Risk Events" (Streaming/Micro-Batch)
*Foco: Velocidade e Disponibilidade*
*   **Input:** API REST (`GET /transactions`).
*   **Contrato:** `transactions_api.yaml`.
*   **Tratamento (Bronze -> Silver):**
    *   **Flattening:** Desanichar JSON.
    *   **Anonimização:** Hash SHA256 do customer_id (CPF).
*   **Output:** Tabela Silver `int_live_risk_transactions` (Append Only).

#### 🟨 SUB-PRODUTO C: "Unified Risk View" (The Golden Record)
*Foco: Regra de Negócio e Consumo*
*   **Input:** `int_legacy_debt_monthly` + `int_live_risk_transactions`.
*   **Lógica:**
    *   `UNION ALL` ou `COALESCE` baseado no *Customer Hash*.
    *   Cálculo de exposição total (Dívida Histórica + Transações do Dia).
*   **Materialização:** View ou Tabela Incremental (Hourly).
*   **Resiliência:** Se o Sub-Produto A estiver desatualizado (D-10), o C continua mostrando a dívida velha + transações novas. O sistema não para.

---

### 3. Plano de Governança
1.  **PII Gate:** NENHUM dado chega na camada Gold sem Hash. A função de Hash deve ser padronizada (`macros/hash_cpf.sql`).
2.  **Observabilidade:**
    *   Monitor de "Schema Change" no Excel (Great Expectations ou Soda).
    *   Monitor de Latência na API.

---

### Próximos Passos (Aprovação)
Você concorda com essa separação em **3 Pipelines Independentes**?
Se sim, avançaremos para a **Fase 1 (Shape-Spec)** do primeiro Sub-Produto (A ou B?).
