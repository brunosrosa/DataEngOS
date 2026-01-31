import typer
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from pydantic import ValidationError
from dataeng_os.models.odcs import DataContract

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def main(
    file_path: Path = typer.Argument(..., help="Path to the contract YAML file", exists=True),
):
    """
    Validate a Data Contract YAML against the ODCS Specification.
    """
    console.print(f"Validating: [bold]{file_path}[/bold]")
    
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            
        contract = DataContract(**data)
        
        console.print(Panel(
            f"[green]SUCCESS[/green]\n"
            f"Dataset: {contract.spec.dataset.logical_name}\n"
            f"Version: {contract.version}",
            title="Validation Passed"
        ))
        
    except ValidationError as e:
        console.print(Panel(
            f"[red]VALIDATION FAILED[/red]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
