# Non-Functional Requirements (NFRs) - Sinergia

## 1. Disponibilidade & Confiabilidade

- **SLA**: 99.9% de uptime para a camada Gold.
- **RTO (Recovery Time Objective)**: 4 horas.
- **RPO (Recovery Point Objective)**: 24 horas (batch D-1).

## 2. Latência & Performance

- Pipelines devem concluir ingestão e processamento até 08:00 AM (D+1).
- Consultas na camada Gold devem retornar em < 5s para queries padrão.

## 3. Observabilidade

- Todo job deve emitir logs estruturados (JSON).
- Métricas de Data Quality devem ser publicadas no dashboard do DataEngOS.

## 4. Custo

- Orçamento mensal de cloud estimado: $500.
- Retenção de logs quentes: 30 dias.
