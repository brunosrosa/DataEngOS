# Airflow DAGs

This directory contains the Python files for Apache Airflow DAGs.

## Structure
- Generated DAGs should be placed here.
- Shared logic should be in `plugins/` or `include/`.

## DataEngOS Workflow
1. Agent reads `slas.yaml`.
2. Agent reads `pipelines/[domain]/flow.mermaid`.
3. Agent generates a DAG file here (e.g., `churn_prediction_dag.py`).
