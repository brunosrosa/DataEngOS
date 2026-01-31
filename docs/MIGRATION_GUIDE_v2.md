# DataEngOS v2.0 Migration Guide

## Overview

This guide details how to upgrade existing DataEngOS v1 projects to the v2.0 Enterprise standard.

## 1. Project Structure

Move your artifacts into the standard folder structure:

```bash
projects/<Your_Project>/
├── contracts/          # ODCS YAMLs
├── dbt/               # SQL models
├── pipelines/         # Documentation
├── product-canvas/    # Requirements
├── security_privacy/  # [NEW] LGPD Plan
└── architecture/      # [NEW] NFRs
```

## 2. Governance Requirements

### Contracts

Every output table in Gold layer MUST have a corresponding contract in `contracts/outputs/`.
Ensure `metadata.owner` is defined.

```yaml
metadata:
  owner:
    business: "Area"
    technical: "Team"
```

### Security Plan

Create `security_privacy/project_plan.yaml`. Even if empty of PII, the file must exist explicitly stating no PII.

```yaml
contracts: []
# or list contracts with PII
```

## 3. Running Validation

Use the new Gatekeeper script to verify compliance:

```bash
python3 scripts/gatekeeper.py
```
