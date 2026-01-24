import typer
import os
from pathlib import Path
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def project(name: str):
    """
    Initialize a new DataEngOS Project structure.
    """
    base_path = Path(f"projects/{name}")
    
    dirs = [
        "product-canvas",
        "contracts/inputs",
        "contracts/outputs",
        "pipelines",
        "dbt"
    ]
    
    console.print(f"[bold green]Initializing project: {name}[/bold green]")
    
    for d in dirs:
        target = base_path / d
        target.mkdir(parents=True, exist_ok=True)
        console.print(f"  Created: {target}")
        
    console.print("[bold blue]Project initialized successfully![/bold blue]")

if __name__ == "__main__":
    app()
