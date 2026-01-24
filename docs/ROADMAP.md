# DataEngOS Product Roadmap

**Status:** Draft  
**Owner:** Head of Data  
**Architect:** DataEngOS Architect  
**Last Updated:** 24/01/2026 (Phase 4 Completed)

Este documento define o plano de entrega do **DataEngOS**, transformando a fundação técnica aprovada em entregáveis tangíveis.

---

## FASE 0: Validation Spikes (Deep Research)
**Objetivo:** Validar hipóteses arquiteturais críticas antes da implementação para evitar dívida técnica e garantir alinhamento com o estado da arte (2025/2026).

### 0.1. Contract Standard Validation
- [x] **ODCS Market Check:** Investigar a adoção atual do ODCS v2.2 vs alternativas emergentes (Google Data Contracts, SQLMesh Contracts).
- [x] **Verdict:** Confirmar se o ODCS mantém sua posição como padrão de indústria ou se há opções mais leves/robustas.

### 0.2. Stack Integration Tests (POCs)
- [x] **Pydantic V2 + CLI:** Criar script mínimo (POC) para validar a Developer Experience (DX) da integração Pydantic V2 com Typer.
- [x] **Alternative Stacks:** Scan rápido por novas ferramentas de "Contract-as-Code" que possam substituir componentes customizados.

---

## FASE 1: O "MVP Manual" (Foundation & Culture)
**Objetivo:** Estabelecer a cultura de contratos e specs via templates e chat, sem automação pesada. Validar o fluxo de trabalho antes de automatizar.

### 1.1. Governança & Standards
- [x] **Definição de Nomenclatura:** Criar `specs/governance/naming.json` com regras de Staging/Marts.
- [x] **Definição de Stack:** Criar `specs/governance/stack.md` documentando a decisão por Pydantic/Typer.
- [x] **Kernel Update:** Atualizar `system_kernel.md` com as novas definições (se necessário).

### 1.2. Templates Essenciais
- [x] **Product Canvas Template:** Criar Roteiro de Entrevista em `templates/canvas.md`.
- [x] **Contract Template:** Criar `templates/contract.yaml` (ODCS v2.2 Subset).
- [x] **Pipeline Logic Template:** Criar `templates/logic.md` para narrativa técnica.

### 1.3. Workflow de Chat
- [x] **Protocolo de Entrevista:** Validar com o Architect via chat o preenchimento de um Canvas real (Mock).

---

## FASE 2: CLI & CI/CD (The Engine)
**Objetivo:** Reduzir o atrito manual. O "Chat" gera o arquivo, o "CLI" valida e materializa.

### 2.1. Core CLI (`dataeng-os`)
- [x] **Setup do Projeto Python:** `pyproject.toml` com Poetry/Rye.
- [x] **Typer App Skeleton:** Estrutura base do comando `dataeng-os`.
- [x] **Comando `init`:** `dataeng-os init` para criar estrutura de pastas em novos projetos.

### 2.2. Validator Engine
- [x] **Modelagem Pydantic:** Mapear o schema ODCS v2.2 para classes Python (`DataContract`, `SchemaField`).
- [x] **Comando `validate`:** `dataeng-os validate <arquivo.yaml>` para checar sintaxe e regras de governança (ex: PII mandatory fields).

### 2.3. Generator Engine
- [x] **Comando `scaffold`:** `dataeng-os scaffold <contract.yaml>` para gerar:
    - [x] Model SQL dbt (Staging/Marts).
    - [x] Schema YML dbt (Priorizado para v1.1).

### 2.4. Installation Robustness (Novo)
- [x] **Setup Script:** Criar `scripts/setup_dev.sh` para detectar e corrigir dependências de ambiente (venv, pip).
- [x] **Documentation:** Reforçar pré-requisitos Linux/WSL no README.

---

## FASE 3: Interface Visual (The Cockpit)
**Objetivo:** Democratizar a criação de contratos para não-técnicos (PMs, Stakeholders) com foco em UX Premium e Localização.

### 3.1. Core Experience (MVP)
- [x] **Streamlit App skeleton:** Navegação por abas funcional.
- [x] **Internationalization (i18n):** Suporte nativo a **PT-BR** e EN-US (auto-detect ou toggle).
- [x] **Catalog Viewer Real:** Scan recursivo de contratos existentes e carregamento no editor.
- [x] **Dynamic Schema Editor:** Adicionar/Remover colunas dinamicamente (superando o loop estático).

### 3.2. "DesignOS" Workflow (UX & AI)
- [x] **Hybrid Home (Cockpit + Architect):**
    - **Top Bar (Cockpit):** Métricas, Atividade Recente e "Quick Actions" (Novo Contrato, Auditoria).
    - **Main Area (Architect Chat):** Interface conversacional para dúvidas e exploração do projeto.
- [x] **Contract Wizard (The Builder):**
    - **Trigger:** Acionado via Chat ou Botão "Novo Contrato".
    - **Passo 1 (Canvas):** Chat focado em cenário ("Descreva seu problema").
    - **Passo 2 (Refinement):** Proposta automática de Schema/SLA.
    - **Templates:** Cards de exemplos rápidos na Home/Wizard.

### 3.3. Advanced Viz
- [x] **Lineage Graph:** Visualizar dependências com `graphviz` (com fallback para Mermaid.js).
- [x] **Diff Viewer:** Visual Check de alterações antes de salvar.


---

## FASE 4: Agnosticismo (The Brain)

**Objetivo:** Desacoplar do modelo de IA (Gemini/OpenAI) e permitir execução local.

### 4.1. LLM Abstraction
- [x] **Integração LiteLLM:** Camada de abstração para trocar de provider (Gemini/OpenAI implementados).
- [x] **Configuration UI:** Página de Settings para gestão segura de API Keys.

### 4.2. Model Optimization (2026)
- [x] **Tiered Architecture:** Separação de modelos para custo/performance.
    - Intent Detection: `gemini-3-flash-preview` (Fast).
    - Generation: `gemini-3-pro-preview` (Reasoning).
- [x] **Graceful Fallback:** Sistema opera com Mock se a API falhar.

---
