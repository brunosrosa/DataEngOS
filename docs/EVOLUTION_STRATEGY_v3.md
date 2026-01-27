# DataEngOS Evolution Strategy: Towards v3.0

## 1. Vision Deep Dive

**Goal**: "Um processo fácil e completo que documenta e cria os artefatos para novos projetos de dados dos mais diversos tipos. De pequenos à enterprise. De um jeito fácil, de forma acompanhada, levando ao fim da criação ultra-refinada do entendimento da necessidade."

### Core Pillars

1. **Frictionless Entry**: Start simple, evolve to complex.
2. **Agentic Companionship**: The AI doesn't just check; it guides, suggests, and drafts.
3. **Unified Canvas**: One place to define business value, technical specs, and governance.
4. **Executable Governance**: Rules that are helpful guardrails, not blockers.

## 2. Gap Analysis (Current v2.0 vs Vision)

- **Current**: Folder-based structure, manual YAML editing, CLI gatekeeper. Good for engineers, hard for business/analysts.
- **Missing**: Visual wizard, "interview" mode for requirements, auto-generation of initial specs from natural language, dynamic templates (Small vs Enterprise).

## 3. Brainstorming Evolution (20+ Items)

### Category A: Agentic User Experience (The "Accompanied" Journey)

1. **Project Inception Wizard**: Interactive chat UI where the Agent interviews the user to fill the Product Canvas automatically.
2. **Smart Contract Drafter**: Agent that reads the "Product Canvas" and proposes the initial ODCS Contract (YAML) automatically.
3. **Context-Aware Linter**: Real-time suggestions in the IDE (e.g., "You added a 'CPF' field; should we apply the PII masking policy?").
4. **Auto-Documentation Agent**: Agent that watches dbt models and updates `logic.md` and `lineage.md` automatically.
5. **Governance Bot**: A friendly bot that comments on PRs explaining *why* a gatekeeper check failed and offering to fix it.
6. **Semantic Search & Q&A**: "Where is the customer churn data?" -> Returns the verified contract and usage examples.

### Category B: Flexibility (Small to Enterprise)

7. **Dynamic Templates**: `dataeng init --profile=startup` (Minimal) vs `dataeng init --profile=bank` (Full Gov).
2. **Progressive Governance**: Allow projects to start as "Incubation" (loose rules) and graduate to "Production" (strict contracts).
3. **Modular Features**: Enable/Disable components (e.g., "Enable LGPD Module" adds the security folder and hooks).
4. **Custom Archetypes**: Users define their own project templates (e.g., "Marketing Project", "Finance Project").
5. **One-Click Sandbox**: Instant local environment setup (Docker Compose) for any project type.

### Category C: Visual & Interactive (The "Easy" Part)

12. **Visual Contract Editor**: GUI to edit ODCS files without touching YAML. Drag-and-drop columns, pick quality rules.
2. **Lineage Visualizer**: Interactive graph showing how a change in "Input A" affects "Dashboard B".
3. **Policy Playground**: Test a dataset against policies to see if it passes compliance before committing.
4. **Canvas Dashboard**: Visual view of the `product-canvas` folder using Streamlit or similar.
5. **Live Data Preview**: Securely preview sample data (mocked/masked) while defining the contract.

### Category D: Advanced Enterprise (The "Refined" Part)

17. **Automated PII Scanning**: Agent scans raw data samples to detect likely PII that wasn't declared.
2. **Cost Estimation Agent**: Predicts cloud costs based on the proposed volume and retention policies in the spec.
3. **Impact Analysis Agent**: "If I change this column type, who breaks?" (Cross-project dependency check).
4. **Self-Healing Pipelines**: Agents that can auto-retry or rollback failed dbt runs based on error classification.
5. **Access Request Workflow**: UI for analysts to request access to masked columns (integrated with `project_plan.yaml`).

## 4. Proposed Roadmap to v3.0

### Phase 3.1: The Assistant (Now)

- Implement Items: 1, 2, 3 (Agentic drafting).

### Phase 3.2: The Visuals (Next)

- Implement Items: 12, 15 (Visual Editors).

### Phase 3.3: The Platform (Future)

- Implement Items: 7, 8 (Dynamic profiles).
