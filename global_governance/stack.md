# DataEngOS Technical Stack Standards

**Version:** 1.0.0
**Status:** Approved (Phase 0 Spike Authenticated)

## 1. Data Contracts Protocol
**Standard:** [Open Data Contract Standard (ODCS) v2.2+](https://github.com/bitol-io/open-data-contract-standard)
**Subset Strategy:** Pragmatic.
- **Mandatory:** `dataset`, `schema` (types, PII), `quality`.
- **Optional:** `slas`, `terms`.

## 2. Automation Engine
**Runtime:** Python 3.10+
**CLI Framework:** [Typer](https://typer.tiangolo.com/)
- **Reasoning:** Superior Developer Experience (DX) with Type Hints vs Click/Argparse.
**Validation Framework:** [Pydantic V2](https://docs.pydantic.dev/)
- **Reasoning:** Rust-based core for performance; industry standard for data validation.

## 3. Transformation Layer
**Engine:** dbt Core
**Modelling Strategy:** Staging -> Intermediate -> Marts (Star Schema).
