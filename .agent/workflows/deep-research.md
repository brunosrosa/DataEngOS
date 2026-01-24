---
description: Initiates a deep research session using the STORM architecture.
---

1. Ask the User for the research topic: "Qual é o tópico central da pesquisa? Especifique o nível de profundidade desejado (ex: Overview Executivo vs. Deep Dive Técnico)."
2. Ask the User: "Existem documentos locais ou especificações no projeto que devem ser considerados como contexto base?"
3. If the user indicates local documents:
    - Read the indicated files (grounding).
    - Look for `llms.txt` in `docs/context/` if available.
4. Invoke the skill `@deep-research-architect` to perform the research.
   - Pass the topic and any gathered context.
   - Explicitly instruct it to use the `research_saver.py` script for output.
5. Wait for the skill to report that the file has been saved.
6. Verify the file exists in `docs/researchs/`.
7. Present the relative path of the generated report to the User.
8. Ask: "Deseja que eu refine alguma seção específica do relatório gerado?"
