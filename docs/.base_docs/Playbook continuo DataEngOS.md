Excelente, Bruno — vou te deixar **pronto** para, quando voltar ao Antigravity, disparar uma **revisão 360º do DataEngOS** (do começo ao fim), cobrindo **regras de negócio, padrões, estrutura, templates, fluxos, modelos, arquivos de exemplo, UI e documentação**. Também trago **como orientar o uso de MCP, RLM e TOON** no arsenal do agente.

Abaixo estão:

1. **Setup rápido** no Antigravity (para você não perder tempo quando chegar)
2. **Prompt Mestre** (System + Orquestração) para pedir a **revisão total**
3. **Playbook detalhado** (fases, outputs e critérios de aceite)
4. **Como garantir que ele revise _TUDO_** (inventário + varredura recursiva + evidências)
5. **Integrações agênticas**: arquitetura (Antigravity vs. agente autônomo), **MCPs essenciais** e **exemplos de configuração**
6. **Como reforçar o uso de MCP, RLM e TOON** (diretivas do agente e checks)
7. **Pós‑execução**: evidências, PRs, follow‑ups

> Tudo está em **Português** e com **exemplos prontos para colar**. Ajuste nomes/paths se necessário.

---

## 1) Quando você chegar ao Antigravity — Setup rápido

**Objetivo:** abrir o monorepo do DataEngOS com **contexto workspace‑wide**, garantindo que o agente “veja” `core/`, `projects/`, `scripts/`, `src/dataeng_os/`, `docs/`.

**Passos:**

- Abrir o **workspace raiz** do repo (pasta que contém `core/`, `projects/`, `src/`, `scripts/`, `docs/`).
- Confirmar que o Antigravity (ou extensão equivalente) está com **contexto de agente “workspace_wide”**.
- Preparar **secrets locais** necessários (tokens do LiteLLM e credenciais mínimas para dbt/warehouse/airflow, caso vá rodar checks).

> Se você quiser, mais tarde eu te gero um **arquivo de workspace** com essa configuração.

---

## 2) **Prompt Mestre** — peça a **Revisão 360º** (de ponta a ponta)

### 2.1 **System Prompt** (coloque como diretiva do agente ou do “Architect”)

Você é o DataEngOS Architect, responsável por revisar e evoluir um monorepo DataEngOS.

Diretriz principal: “Nenhum código sem contrato e especificação aprovados”.

Trate governança como código: naming, classificação/PII, estilo SQL, qualidade, LGPD.

Use MCPs para agir no mundo (dbt, airflow, docker, postgres, filesystem, git-history, catalog).

Aplique RLM (varredura recursiva + resumo iterativo) e TOON (compactar JSON/manifest grandes).

Nunca opere fora do escopo do workspace autorizado. Gere evidências de cada ação.

Saídas SEMPRE exigidas:

  1) RELATÓRIO_360.md (achados, riscos, plano),

  2) CHANGES_SUMMARY.md (diff lógico),

  3) TODO_ISSUES.md (tarefas rastreáveis por fase),

  4) PR_DESCRIPTION.md (texto de PR com escopo e testes),

  5) EVIDENCES/ (logs, resultados de compile/test, capturas de lineage/docs).

Definição de “Done”: compile/test ok, contratos e policies cobrindo PII, docs e UI atualizados,

valores de negócio por release registrados e RACI/SLAs claros.

### 2.2 **Comando/Prompt de Orquestração** (cole como mensagem do usuário)

Quero uma REVISÃO 360º do projeto DataEngOS, sem exceções, cobrindo:  

(1) Inventário e Reconhecimento

- Mapear toda a árvore: core/global_governance, projects/*, src/dataeng_os, scripts, docs.

- Gerar INVENTARIO.md com todos os artefatos críticos e lacunas.

(2) Governança Organizacional (core/global_governance)

- Validar naming-conventions.json, classification.yaml, stack-standards.md, templates.

- Sugerir/pousar policies corporativas (data_quality_policy.md, privacy_lgpd_policy.md, security_access_policy.md) em core/global_governance/policies/ (se ausentes), com exemplos mínimos.

(3) Projetos (ex.: projects/PRJ_001_Sinergia)

- Conferir product-canvas/ (visão, SLAs, RACI, business case — se ausentes, criar seções no canvas).

- Contratos ODCS inputs/outputs: validar, enriquecer quality_rules, owners, PII.

- Pipelines: revisar pipelines/<domínio>/logic.md e decomposition_strategy.md.

- dbt: checar staging/silver/gold; gerar/ajustar .yml de testes; assegurar mascaramento PII na Silver.

- (Opcional) Criar architecture/nfrs.md, semantics/{conceptual_model.mermaid,glossary.md}, security_privacy/project_plan.yaml e roadmap/releases.yaml.

(4) Qualidade (dbt + política)

- A partir dos contratos, gerar/alinhar testes dbt mínimos (estruturais + 1 regra de negócio por tabela).

- Criar plano de qualidade (métricas/SLOs) aderente à policy.

(5) Segurança & Privacidade (LGPD)

- Cruza classification.yaml com contratos; para PII: exigir security_privacy/project_plan.yaml por projeto

(base legal, finalidade, retenção/purge, matriz de acesso, evidências).

(6) Orquestração/Execução

- Se possível, rodar dbt compile/test via MCP e registrar EVIDENCES/ (ou simular validações se sem credencial).

- Preparar DAGs (Airflow) conforme SLAs do canvas (cron derivado).

(7) UI/UX do DataEngOS (src/dataeng_os/ui/)

- Ajustar labels, tooltips e fluxos para refletir os novos padrões (contratos, policies, PII).

- Atualizar quaisquer componentes que referenciem nomes antigos, sem quebrar navegação.

(8) Documentação & Onboarding

- Atualizar README(s) e docs/ROADMAP.md conforme a visão enterprise evoluída.

- Garantir que DATAENGOS_v2_ENTERPRISE_EVOLUTION.md esteja referenciado no README raiz.

(9) Entrega

- Preparar PR_DESCRIPTION.md com escopo, testes e impactos.

- Sugerir branches e plano de rollout (se houver breaking changes).

Regras de execução:

- Use MCPs para ler/compilar/listar/rodar o que for possível.

- Aplique RLM: não carregue o repo inteiro de uma vez; faça varredura por pastas, produza “context_memory.md”, resuma, limpe o contexto e avance.

- Use TOON para manifest.json e JSONs grandes.

- Trabalhe em modo “propor + gerar” (sugira e, quando autorizado, gere arquivos ou patches).

Saídas obrigatórias nesta revisão:

- RELATÓRIO_360.md, CHANGES_SUMMARY.md, TODO_ISSUES.md, PR_DESCRIPTION.md, pasta EVIDENCES/

- Pull request draft (se autorizado a abrir branch) ou pacote de patches.

> Dica: mantenha esse prompt salvo como **“Playbook — Revisão 360º”** no Antigravity.

---

## 3) **Playbook detalhado** (fases, o que fazer, como validar)

### Fase 0 — Calibrar ambiente

- **MCP**: `filesystem`, `git-history`, `dbt`, `airflow`, `docker`, `postgres` (read‑only se for o caso).
- Checar `core/global_governance/*`, `projects/*`, `src/dataeng_os/*`.

**Saída:** `INVENTARIO.md` (árvore, arquivos críticos, o que falta).

---

### Fase 1 — Governança organizacional

- Validar `naming-*.json`, `classification.yaml`, `stack-standards.md`, `templates/`.
- Se `policies/` não existe, **propor** criação com os 3 arquivos (data_quality, privacy_lgpd, security_access).

**Saída:** diffs sugeridos + trechos de policies (exemplos mínimos prontos para colar).

---

### Fase 2 — Projeto(s) (ex.: `PRJ_001_Sinergia`)

- Canvas: garantir **RACI, SLAs, perguntas de negócio e valor** (estender `legacy_debt.md` se necessário).
- Contratos ODCS: enriquecer `quality_rules`, revisar `owner`, `schema`, `accepted_values`, PII.
- Pipelines: validar `logic.md` e `decomposition_strategy.md` (joins, chaves, particionamento).
- dbt: garantir **mascaramento PII na Silver**, testes estruturais + 1 regra de negócio/tabela.

**Saída:** patches em `contracts/`, `pipelines/` e `dbt/` + testes .yml.

---

### Fase 3 — Qualidade & LGPD

- Plano de qualidade do projeto + mapeamento PII → `security_privacy/project_plan.yaml` (base legal, finalidade, retenção/purge, matriz de acesso, aprovações).

**Saída:** `project_plan.yaml` (se aplicável) e `policy → plan` alinhados.

---

### Fase 4 — Orquestração/Execução

- Rodar `dbt compile/test` via MCP (ou simular validações).
- Gerar `EVIDENCES/` com logs/artefatos.

**Saída:** `EVIDENCES/` + relatório de execução.

---

### Fase 5 — UI/UX e Documentação

- Ajustar `src/dataeng_os/ui/` (labels, caminhos, ajudas) para refletir governança e contratos.
- Atualizar `README.md`, `docs/ROADMAP.md`, referenciar `DATAENGOS_v2_ENTERPRISE_EVOLUTION.md`.

**Saída:** PR pronto com **PR_DESCRIPTION.md** e **CHANGES_SUMMARY.md**.

---

## 4) Como garantir que ele revise **TUDO MESMO**?

Peça explicitamente:

- **Inventário recursivo**:\ “_Liste e categorize todos os arquivos sob `core/`, `projects/`, `scripts/`, `src/`, `docs/`. Marque ‘crítico/faltando/obsoleto’._”

- **Mapa de dependências**:\ “_Construa um grafo simples: contratos → models dbt → DAGs → docs → UI. Liste pontos de acoplamento e impactos._”

- **Checklist de coverage**:\ “_Para cada domínio/tabela, comprove: contrato ODCS, testes dbt, PII/mascaramento, docs, owner/RACI, métricas/SLOs, NFRs._”

- **Evidências**:\ “_Publique em `EVIDENCES/` os logs de compile/test, screenshots/exports do lineage/docs, e um `coverage_matrix.md` com ✓/✗._”

- **Estratégia de “double‑check”**:\ “_Ao concluir cada fase, gere um sumário e peça minha autorização para aplicar patches. Só então gere os arquivos e diffs._”

---

## 5) Integrações agênticas — arquitetura e MCPs

> **Seu cenário**: Antigravity é o **espaço de criação**, mas o agente do DataEngOS é **autônomo** (roda fora, via **LiteLLM → Gemini**). Ótimo. Você pode usar **MCPs** no Antigravity **e/ou** expor **MCPs** ao agente autônomo (dependendo do orquestrador).

### 5.1 _Quem faz o quê?_

- **Antigravity**: IDE agent‑first para **planejar, revisar, editar e “orquestrar”** a sessão.
- **Agente autônomo (DataEngOS Agent)**: serviço próprio, com **API (LiteLLM)**, que **executa o playbook** e usa MCPs (quando disponíveis) para agir.

### 5.2 **MCPs essenciais** (mínimo recomendável)

- `filesystem` (limite aos diretórios do repo) — listar/ler/escrever patches.
- `git-history-reader` — contexto de histórico/decisões.
- `dbt-mcp` — `compile`, `run`, `test`, `get_lineage`.
- `astro-airflow-mcp` (ou equivalente) — `list_dags`, `trigger_dag`, `get_task_logs`.
- `docker-mcp` — `list_containers`, `inspect_logs`, `restart` (local).
- `postgres-mcp` (ou do warehouse alvo) — `list_tables`, `query`, `explain`.
- (Opcional) `openmetadata-mcp` / `datahub-mcp` — sincronizar glossário/catalogo.

### 5.3 **Exemplo de configuração MCP** _(conceitual, ajuste para o seu runtime)_

{

  "mcpServers": {

    "filesystem-dev": { "command": "node", "args": ["fs-mcp", "--root", "/workspaces/dataengos"] },

    "dbt-core":       { "command": "uvx",  "args": ["dbt-mcp", "--project-dir", "projects/PRJ_001_Sinergia/dbt/sinergia"] },

    "airflow-local":  { "command": "uvx",  "args": ["astro-airflow-mcp", "--url", "http://localhost:8080", "--username", "admin", "--password", "admin"] },

    "docker":         { "command": "uvx",  "args": ["docker-mcp"] },

    "postgres-dw":    { "command": "uvx",  "args": ["postgres-mcp", "postgresql://user:pwd@localhost:5432/dw"] },

    "git-history":    { "command": "uvx",  "args": ["git-history-reader", "--repo", "/workspaces/dataengos"] }

  }

}

``

> **Importante**: **escopo** do `filesystem` deve apontar **somente** para o workspace do projeto; nunca dê root global.

---

## 6) Como **reforçar** MCP + RLM + TOON no agente do DataEngOS

### 6.1 **Diretivas do agente** (adicione ao _system prompt_ do serviço autônomo)

Uso de Ferramentas:

    1) MCP é obrigatório para qualquer ação de I/O (listar/ler/escrever arquivos, rodar dbt, acionar Airflow, consultar DB).

    2) RLM: varra o repositório em etapas. Nunca carregue tudo de uma vez.

        - Passo A: liste diretórios e arquivos → gere INVENTARIO.md

        - Passo B: selecione subconjuntos relevantes → resuma em context_memory.md

        - Passo C: limpe contexto e prossiga para o próximo subconjunto, sempre consultando resumos anteriores.

    3) TOON: ao lidar com JSONs grandes (ex.: manifest.json do dbt), converta para TOON antes de análise.

    4) Gatekeeper mental: recuse gerar artefatos sem contratos/policies quando PII estiver marcado.

    5) Evidências: toda ação crítica gera outputs em EVIDENCES/ e resumo no RELATÓRIO_360.md.

### 6.2 **Checks automáticos** (você pede explicitamente no prompt)

- **“Demonstre que usou MCP”**: peça para logar no RELATÓRIO_360.md as chamadas MCP (sem secrets), com timestamp e propósito.
- **“Demonstre RLM”**: peça uma **tabela de iterações** (Passo, Pasta, Achados, Resumo gravado em `context_memory.md`).
- **“Demonstre TOON”**: peça o **diff do tamanho** antes/depois de converter manifest.json → TOON (estimativa).

---

## 7) Pós‑execução — o que você deve exigir como **entregáveis**

- `RELATÓRIO_360.md` (achados por dimensão: governança, contratos, qualidade, LGPD, pipelines, UI, docs, riscos)
- `CHANGES_SUMMARY.md` (lista de arquivos alterados/criados + justificativa)
- `TODO_ISSUES.md` (tarefas por prioridade, com links/paths)
- `PR_DESCRIPTION.md` (pronto para abrir PR: escopo, testes, riscos, checklists DoR/DoD)
- `EVIDENCES/` (logs dbt compile/test, prints/exports de lineage/docs, snapshot do coverage)
- **Opcional**: branch criada com patches; se não autorizado, **zip** com patches

---

## TL;DR — **Comando curto** para você colar quando voltar

> **No Antigravity (ou no seu agente autônomo via API)**

```
Rodar “Playbook — Revisão 360º DataEngOS” no workspace atual.
- Revisar TUDO: core/global_governance, projects/** (canvas, contratos ODCS, pipelines, dbt), src/dataeng_os/ui, scripts, docs.
- Complementar lacunas (policies corporativas, plano LGPD por projeto, NFRs, glossário, roadmap/releases).
- Enforçar PII/mascaramento na Silver e testes dbt mínimos (estruturais + 1 regra de negócio).
- Atualizar UI/labels/ajudas conforme novos padrões.
- Atualizar README(s) e referenciar DATAENGOS_v2_ENTERPRISE_EVOLUTION.md.
- Usar MCP (filesystem, dbt, airflow, docker, postgres, git-history); aplicar RLM e TOON.
- Entregar: RELATÓRIO_360.md, CHANGES_SUMMARY.md, TODO_ISSUES.md, PR_DESCRIPTION.md e EVIDENCES/.
- Sugerir PR (ou gerar patches) e plano de rollout.
```

---

Se você quiser, eu já **empacoto esses prompts** em arquivos de **playbook** (ex.: `core/prompts/playbooks/revisao_360.md`) e um **script de CI** que verifica a presença dos entregáveis. Quando você voltar ao ambiente, é colar/rodar. Quer que eu gere esses artefatos também?
