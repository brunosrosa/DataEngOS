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

## 3. Brainstorming Evolution (20+ Items) - *Refined post-UI Deep Dive*

### Category A: Agentic User Experience ("The Assistant")

1. **Fix Project Inception Wizard**: (Critical Gap) The current "Create New" wizard is non-functional. Connect it to the backend.
2. **Smart Contract Drafter**: Enable LLM to draft contracts (Fix Auth/Quota issues identified in testing).
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

### Category C: Visual & Interactive ("The Easy Part")

12. **Visual Contract Editor 2.0**: Upgrade current form-based editor to **Drag-and-Drop**.
2. **Lineage Visualizer**: Interactive graph showing how a change in "Input A" affects "Dashboard B".
3. **Policy Playground**: Test a dataset against policies to see if it passes compliance before committing.
4. **Canvas Dashboard**: Visual view of the `product-canvas` folder using Streamlit or similar.
5. **Live Data Preview**: Securely preview sample data (mocked/masked) while defining the contract.

### Category D: Advanced Enterprise ("The Refined Part")

17. **Automated PII Scanning**: Agent scans raw data samples to detect likely PII that wasn't declared.
2. **Cost Estimation Agent**: Predicts cloud costs based on the proposed volume and retention policies in the spec.
3. **Impact Analysis Agent**: "If I change this column type, who breaks?" (Cross-project dependency check).
4. **Self-Healing Pipelines**: Agents that can auto-retry or rollback failed dbt runs based on error classification.
5. **Access Request Workflow**: UI for analysts to request access to masked columns (integrated with `project_plan.yaml`).

## 4. Proposed Roadmap to v3.0

### Phase 3.1: The Repair (Immediate) - *Timeline: 1 Week*

**Goal**: Make the current Agentic features usable.

- **Fix Wizard**: Ensure "Create New Project" actually creates the folder structure.
- **Fix LLM Auth**: Streamline the API Key setup in Settings so the Chatbot works.
- **Release**: v2.1 (Patch).

### Phase 3.2: The Visuals (Next) - *Timeline: 2 Weeks*

**Goal**: Reduce friction for non-technical users.

- **Visual Editor 2.0**: Implement Drag-and-Drop for columns.
- **Canvas Dashboard**: Read-only view of Product Canvas in UI.
- **Release**: v2.5 (Minor).

### Phase 3.3: The Platform (Evolution) - *Timeline: 1 Month*

**Goal**: Enterprise flexibility and robustness.

- **Dynamic Templates**: Startup vs Bank profiles.
- **Gatekeeper UI**: Show gatekeeper failures inside the "Project Audit" page.
- **Release**: v3.0 (Major).
