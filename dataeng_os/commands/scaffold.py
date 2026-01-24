import typer
import yaml
from pathlib import Path
from rich.console import Console
from dataeng_os.models.odcs import DataContract

app = typer.Typer()
console = Console()

@app.command()
def dbt(
    contract_path: Path = typer.Argument(..., help="Path to contract YAML", exists=True),
    output_dir: Path = typer.Option(Path("dbt"), help="Output directory for dbt models")
):
    """
    Scaffold dbt models based on an ODCS Contract.
    """
    console.print(f"Scaffolding dbt models from: [bold]{contract_path}[/bold]")
    
    with open(contract_path, "r") as f:
        data = yaml.safe_load(f)
    
    contract = DataContract(**data)
    entity = contract.spec.dataset.logical_name
    
    # Auto-detect project context
    project_root = None
    try:
        # Assuming structure: .../projects/<project_name>/contracts/...
        # We want to find the LAST occurrence of 'projects' to avoid home/user/projects conflicts
        path_parts = contract_path.resolve().parts
        
        # Search from the end to find the inner-most 'projects' folder
        # (Where our repo structure lives)
        reversed_parts = list(reversed(path_parts))
        if "projects" in reversed_parts:
            # Index in reversed list
            rev_idx = reversed_parts.index("projects")
            
            # The project name is the item BEFORE 'projects' in reversed list (which is AFTER in normal list)
            # path: [... 'projects', 'PRJ_001', 'contracts' ...]
            # reversed: [... 'contracts', 'PRJ_001', 'projects' ...]
            if rev_idx > 0:
                project_name = reversed_parts[rev_idx - 1]
                
                # Reconstruct path
                # Identify the index in the original tuple
                # We can't easily map back from reversed index if duplicates exist, so let's find the index from the right in the original tuple
                # rindex equivalent for list/tuple
                true_projects_idx = len(path_parts) - 1 - rev_idx
                
                # Project root is up to project_name (projects_idx + 2 segments)
                # parts[0 : projects_idx + 2] -> /.../projects/PRJ_001
                project_root = Path(*path_parts[:true_projects_idx + 2])
    except Exception:
        pass

    # Determine Output Directory
    if str(output_dir) == "dbt": # Default value was passed
        if project_root:
            output_dir = project_root / "dbt"
            console.print(f"[yellow]Auto-detected Project Root:[/yellow] {project_root}")
            console.print(f"[yellow]Targeting Output:[/yellow] {output_dir}")
        else:
            # Fallback to current dir if not in a project structure
            console.print("[yellow]Warning:[/yellow] Could not detect project context. Generating in ./dbt")
            
    # Create output structure
    (output_dir / "staging").mkdir(parents=True, exist_ok=True)
    (output_dir / "marts").mkdir(parents=True, exist_ok=True)
    
    # Generate Staging Model (SQL)
    stg_content = f"""
{{{{ config(materialized='view') }}}}

WITH source AS (
    SELECT * FROM {{{{ source('{contract.spec.dataset.domain}', '{contract.spec.dataset.physical_name}') }}}}
)

SELECT
    -- Scaffolding columns from contract
"""
    for col in contract.spec.schema_def.columns:
        stg_content += f"    {col.name}, -- {col.description}\n"
        
    stg_content += "\nFROM source"
    
    stg_file_sql = output_dir / "staging" / f"stg_{entity}.sql"
    with open(stg_file_sql, "w") as f:
        f.write(stg_content)
    console.print(f"[green]Created SQL:[/green] {stg_file_sql}")

    # Generate Staging Schema (YML)
    schema_content = {
        "version": 2,
        "models": [
            {
                "name": f"stg_{entity}",
                "description": contract.spec.dataset.description,
                "columns": []
            }
        ]
    }

    for col in contract.spec.schema_def.columns:
        col_def = {
            "name": col.name,
            "description": col.description or ""
        }
        tests = []
        if col.primary_key:
            tests.append("unique")
            tests.append("not_null")
        # Add basic PII tag if present (dbt convention)
        if col.pii:
            col_def["tags"] = ["pii"]
            
        if tests:
            col_def["tests"] = tests
            
        schema_content["models"][0]["columns"].append(col_def)

    stg_file_yml = output_dir / "staging" / f"stg_{entity}.yml"
    with open(stg_file_yml, "w") as f:
        yaml.dump(schema_content, f, sort_keys=False)
    console.print(f"[green]Created YML:[/green] {stg_file_yml}")

    console.print("[blue]Scaffold complete![/blue]")

if __name__ == "__main__":
    app()
