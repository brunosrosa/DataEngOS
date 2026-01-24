# DataEngOS Product Roadmap

**Status:** Draft  
**Owner:** Head of Data  
**Architect:** DataEngOS Architect  
**Last Updated:** 24/01/2026

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
- [ ] **Definição de Nomenclatura:** Criar `specs/governance/naming.json` com regras de Staging/Marts.
- [ ] **Definição de Stack:** Criar `specs/governance/stack.md` documentando a decisão por Pydantic/Typer.
- [ ] **Kernel Update:** Atualizar `system_kernel.md` com as novas definições (se necessário).

### 1.2. Templates Essenciais
- [ ] **Product Canvas Template:** Criar Roteiro de Entrevista em `templates/canvas.md`.
- [ ] **Contract Template:** Criar `templates/contract.yaml` (ODCS v2.2 Subset).
- [ ] **Pipeline Logic Template:** Criar `templates/logic.md` para narrativa técnica.

### 1.3. Workflow de Chat
- [ ] **Protocolo de Entrevista:** Validar com o Architect via chat o preenchimento de um Canvas real (Mock).

---

## FASE 2: CLI & CI/CD (The Engine)
**Objetivo:** Reduzir o atrito manual. O "Chat" gera o arquivo, o "CLI" valida e materializa.

### 2.1. Core CLI (`dataeng-os`)
- [ ] **Setup do Projeto Python:** `pyproject.toml` com Poetry/Rye.
- [ ] **Typer App Skeleton:** Estrutura base do comando `dataeng-os`.
- [ ] **Comando `init`:** `dataeng-os init` para criar estrutura de pastas em novos projetos.

### 2.2. Validator Engine
- [ ] **Modelagem Pydantic:** Mapear o schema ODCS v2.2 para classes Python (`DataContract`, `SchemaField`).
- [ ] **Comando `validate`:** `dataeng-os validate <arquivo.yaml>` para checar sintaxe e regras de governança (ex: PII mandatory fields).

### 2.3. Generator Engine
- [ ] **Comando `scaffold`:** `dataeng-os scaffold <contract.yaml>` para gerar:
    - Model SQL dbt (Staging/Marts).
    - Schema YML dbt.

---

## FASE 3: Interface Visual (The Cockpit)
**Objetivo:** Democratizar a criação de contratos para não-técnicos (PMs, Stakeholders).

### 3.1. Contract Editor
- [ ] **Streamlit App:** Formulário visual para preencher metadata do contrato.
- [ ] **YAML Preview:** Visualização em tempo real do YAML gerado.

### 3.2. Catalog Viewer
- [ ] **Search:** Buscar contratos existentes no repositório.
- [ ] **Lineage Graph:** Visualizar dependências (Canvas -> Contract -> Pipeline).

---

## FASE 4: Agnosticismo (The Brain)
**Objetivo:** Desacoplar do modelo de IA (Gemini/OpenAI) e permitir execução local.

### 4.1. LLM Abstraction
- [ ] **Integração LiteLLM:** Camada de abstração para trocar de provider.
- [ ] **Local Mode:** Suporte a Ollama/Llama.cpp para rodar o Architect localmente.

---

## Critérios de Aceite para Etapa 3 (Execução)
A próxima etapa focará exclusivamente nas tasks da **Fase 1.1 e 1.2**:
1. `specs/governance/naming.json`
2. `specs/governance/stack.md`
3. `templates/contract.yaml`
4. `templates/canvas.md`
