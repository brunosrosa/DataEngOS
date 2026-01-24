!ARCHITECT_PROTOCOL_INIT

**CONTEXTO:**
Estamos iniciando o DataEngOS do zero. O Kernel está carregado, mas a "Constituição" (Governança) ainda não foi escrita. Eu sou o Head de Dados e você é o Arquiteto Principal.

**OBJETIVO:**
Criar um plano de implementação robusto para o framework, definindo padrões "Ouro" antes de escrevermos qualquer template.

**SUA MISSÃO EM 3 ETAPAS (STOP & GO):**
*Você deve executar a Etapa 1, apresentar o resultado e PARAR. Só avance para a Etapa 2 quando eu disser "APROVADO".*

---

### ETAPA 1: PESQUISA E DEFINIÇÃO TÉCNICA (The Gold Standard)
Realize uma análise crítica (simulada com base no seu conhecimento de corte) sobre os seguintes pilares e proponha a nossa Stack Oficial:

1.  **Padrão de Contratos (ODCS vs Custom):**
    - Analise o *Open Data Contract Standard* (v2.2+). Ele é verboso demais para um MVP? Devemos usar uma versão simplificada ou o padrão completo?
    - **Deliverable:** Proposta da estrutura YAML ideal para nossos arquivos em `specs/contracts/`.

2.  **Nomenclatura e Camadas:**
    - Devemos usar a abordagem clássica (Bronze/Silver/Gold) ou a moderna (Staging/Intermediate/Marts)? Por que?
    - Defina a convenção de nomes para tabelas, views e colunas temporais.

3.  **Automação (Stack da Fase 2):**
    - Para validar esses YAMLs futuramente, qual a melhor biblioteca Python? (Pydantic V2? Marshmallow?)
    - Qual CLI framework usar? (Typer? Click?)

**SAÍDA DA ETAPA 1:** Um documento chamado **"DataEngOS Technical Foundation Proposal"**.

---

### ETAPA 2: O ROADMAP DE PRODUTO (Tasks & Subtasks)
Baseado na proposta aprovada na Etapa 1, crie um plano de projeto detalhado em `docs/ROADMAP.md` dividido em 4 Fases:
- **Fase 1 (MVP Manual):** Foco em Templates Markdown/YAML e fluxo via Chat.
- **Fase 2 (CLI & CI/CD):** Automação Python (`dataeng-os validate`) e Pydantic.
- **Fase 3 (Interface Visual):** App Streamlit para gestão de contratos.
- **Fase 4 (Agnosticismo):** Integração com LiteLLM para múltiplos modelos.

**SAÍDA DA ETAPA 2:** O conteúdo do arquivo `ROADMAP.md` com tasks quebradas (ex: "Criar template Jinja base", "Definir validador Pydantic").

---

### ETAPA 3: EXECUÇÃO DA FUNDAÇÃO (Materialização)
Somente após a aprovação do Roadmap, você criará os arquivos físicos:
1.  `specs/governance/naming.json` (Com as regras aprovadas).
2.  `specs/governance/stack.md` (Com a stack aprovada).
3.  `templates/contract.yaml` (O template ODCS aprovado).
4.  `templates/canvas.md` (O roteiro de entrevista).

**INICIE AGORA A ETAPA 1.** Apresente sua proposta técnica.