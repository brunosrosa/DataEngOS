# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-24

### Added
- **Multi-Tenancy Architecture:** Refactored file system to support `projects/<ID>/` isolation.
- **Global Governance:** Centralized `naming.json` and `stack.md` in `global_governance/`.
- **kernel v1.0:** Updated System Kernel to enforce Specification-Driven Development.
- **Project Sinergia (PRJ_001):**
    - Completed full lifecycle (Shape -> Contract -> Pipeline -> Implementation).
    - Implemented "Lambda View" for Batch/Stream unification.
    - Implemented PII Hashing (SHA256) in Silver Layer.
- **Validation Spikes:** Confirmed ODCS v2.2 and Pydantic V2 + Typer stack via Deep Research.

### Changed
- Moved `specs/` and `implementation/` content to `projects/PRJ_001_Sinergia/`.
- Updated `contract.yaml` template to `odcs_contract_v1.yaml` including Banking Standards (Cost Center, Classification).
- Updated `.gitignore` to exclude `.agent` and Python cache files.
