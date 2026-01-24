# DataEngOS Stack Standards

## SQL Standards (dbt)

### General
- **Dialect**: Postgres / Snowflake (Target dependent)
- **Casing**:
  - Keywords: `UPPER_CASE` (e.g., `SELECT`, `FROM`, `WHERE`)
  - Identifiers: `snake_case` (e.g., `customer_id`, `first_name`)
- **Indentation**: 4 spaces.
- **Commas**: Leading commas are preferred for easier diffing.

### CTEs (Common Table Expressions)
- **Mandatory**: Use CTEs for all logical steps.
- **Structure**:
    1.  **Import CTEs**: `with source as (...)`
    2.  **Logical CTEs**: `renamed as (...)`, `filtered as (...)`
    3.  **Final CTE**: `select * from final`
- **Avoid**: Subqueries in `JOIN` clauses.

### Example
```sql
WITH source_data AS (
    SELECT * FROM {{ source('shopify', 'orders') }}
)

, cleaned_data AS (
    SELECT
        id as order_id
        , user_id
        , total_price
        , created_at
    FROM source_data
    WHERE total_price > 0
)

SELECT * FROM cleaned_data
```

## Python Standards (Airflow)

### General
- **Style Guide**: PEP 8.
- **Linter**: `ruff` or `flake8`.
- **Formatter**: `black`.

### DAG Definitions
- **Declarative**: Prefer generating DAGs from configuration where possible.
- **Task Groups**: Use `TaskGroup` to organize complex graphs.
- **Idempotency**: Ensure all tasks can be re-run without side effects.
- **Variables**: Avoid hardcoded values; use Airflow Variables or Environment Variables.

### Docstrings
- All DAGs and Tasks must have a docstring explaining their purpose and owner.
