# DataEngOS v1.0

> **Specification-Driven Data Engineering Operating System**

**DataEngOS** é um framework governado para construção de plataformas de dados modernas. Ele inverte a lógica tradicional: *"Nenhum código é escrito sem antes haver um Contrato e uma Especificação aprovados".*

---

## 🏗 Arquitetura Multi-Tenant

O DataEngOS organiza o caos dos dados em uma estrutura rígida de diretórios:

```bash
DataEngOS/
├── core/                   # O "Kernel" do Sistema (Prompts & Behavioral Rules)
├── global_governance/      # "A Constituição" (Leis Universais)
│   ├── naming.json         # Regras de Nomenclatura (Machine Readable)
│   ├── stack.md            # Stack Oficial (ODCS + Typer + dbt)
│   └── templates/          # Templates Padronizados (Banking Standards)
└── projects/               # Container de Projetos Isolados
    └── PRJ_001_Sinergia/   # Exemplo: Integração de Risco
        ├── product-canvas/ # "O Porquê" (SLA, Visão, Personas)
        ├── contracts/      # "A Lei" (Inputs/Outputs em ODCS v2.2)
        ├── pipelines/      # "O Como" (Narrativa Técnica, Topologia)
        └── dbt/            # "O Código" (SQL Jinja, Models)
```

---

## 🛡 Governança & Stack

### 1. Data Contracts (ODCS v2.2)
Adotamos o **Open Data Contract Standard** (subset pragmático) como interface única entre produtores e consumidores.
- **Inputs:** Definem estritamente o que entra (ex: `legacy_debt.yaml`).
- **Outputs:** Definem estritamente o que é entregue (ex: `fct_unified_risk.yaml`).

### 2. Automação (Python + Pydantic V2)
Nossa engine de validação e geração de código é construída sobre:
- **Pydantic V2:** Validação de schemas com performance Rust.
- **Typer:** Interface CLI robusta para desenvolvedores.

### 3. Transformação (dbt Core)
- **Camadas:** Staging (Bronze) -> Intermediate (Silver) -> Marts (Gold).
- **PII:** Higienização obrigatória na camada Silver (SHA256).

---

## 🚀 Getting Started

### 1. Iniciar um Novo Projeto
O **DataEngOS Architect** (Agente IA) deve ser invocado para criar a estrutura:
> "Inicie o projeto PRJ_002_AntiFraud usando os padrões bancários."

### 2. O Ciclo de Vida (The Workflow)
1.  **Shape-Spec (Fase 1):** Entrevista socrática e criação do `Product Canvas`.
2.  **Write-Contract (Fase 2):** Definição dos YAMLs de Contrato (Input/Output).
3.  **Architect-Pipeline (Fase 3):** Desenho da Topologia e Estratégia de Join.
4.  **Implementation (Fase 4):** Geração automática dos modelos dbt.

---

## 📚 Projetos Ativos

### [PRJ_001] Sinergia (Legacy Integration) (Exemplo de projeto fictício).
Integração de dados de risco da Fintech adquirida "CredFácil". 
- **Desafio:** Unir Excel Batch (D-30) com API Real-time.
- **Solução:** Lambda Architecture com Unificação na Camada Gold via Hash.
- **Status:** **CONCLUÍDO**.
