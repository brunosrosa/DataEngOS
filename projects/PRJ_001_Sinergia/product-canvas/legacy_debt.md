# Product Canvas: Sinergia Legacy Debt (Sub-Product A)

> **Status:** Draft
> **Source:** `base_inadimplencia_historica_vFinal_REAL.xlsx`

## 1. Visão & Valor
**Quem é o consumidor principal?**
- Time de Risco (Credit Score Model).
- Time Regulatório (Relatório Bacen).

**Qual a Pergunta de Negócio (Business Question) a ser respondida?**
- "Qual é o histórico consolidado de inadimplência dos clientes adquiridos da CredFácil?"

**Qual a ação tomada com este dado?**
- O dado servirá de *baseline* para o cálculo de exposição total na camada unificada. Sem ele, o Score de Crédito nasce "cego" para o passado do cliente.

## 2. Requisitos de Dados (SLA)
- [x] **Latência:** Mensal (O arquivo chega em D-5).
- [x] **Histórico Necessário:** Carga Full inicial + Deltas mensais (se houver).
- [x] **Frescor:** O dado deve estar disponível na Silver até 4h após a chegada do arquivo no Sharepoint/Lake.

## 3. Entidades Envolvidas
- **Cliente:** Identificado por CPF (campo problemático).
- **Dívida:** Valor, Data de Vencimento, Status.

## 4. Segurança & Privacidade (PII)
- **Existirão dados de clientes?** Sim.
- **Quais campos são sensíveis?**
    - `CPF` (Exige tratamento severo: Sanitização de `.`/`-` e Hashing SHA256 na camada Silver).
    - `Nome` (Se existir, deve ser mascarado).

## 5. Qualidade & Riscos (Known Issues)
- **Schema Drift:** O Excel pode mudar colunas (cabeçalhos duplos).
- **Inconsistência de PK:** A coluna de documento varia entre "Doc_ID" e "CPF_Cliente".
- **Formato de Data:** Brasileiro (`DD/MM/AAAA`).
