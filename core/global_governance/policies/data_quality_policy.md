# Data Quality Policy

## 1. Visão Geral

Esta política define os padrões mínimos de qualidade para todos os produtos de dados geridos pelo DataEngOS.

## 2. Princípios

1. **Fail-Fast**: Dados ruins não devem propagar para camadas de consumo.
2. **Propriedade**: Todo dado tem um Data Owner e um Data Steward.
3. **Observabilidade**: Falhas de qualidade devem gerar alertas e incidentes.

## 3. Requisitos Mínimos por Camada

### 3.1 Camada Bronze (Raw)

- Validação de schema na ingestão.
- Monitoramento de volume e freshness.

### 3.2 Camada Prata (Trusted/Silver)

- Dedupicação obrigatória.
- Integridade referencial.
- Padronização de tipos e domínios.

### 3.3 Camada Ouro (Gold/Consumption)

- Regras de negócio complexas validadas.
- Contratos de dados (ODCS) aplicados na saída.

## 4. Métricas Obrigatórias

- **Completeness**: % de nulos em campos chave.
- **Uniqueness**: % de duplicatas em chaves primárias.
- **Freshness**: Tempo desde a última atualização vs. SLA.
