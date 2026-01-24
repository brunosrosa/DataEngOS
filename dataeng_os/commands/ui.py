import typer
import subprocess
import os
import sys
from rich.console import Console

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def main():
    """
    Launch the DataEngOS Cockpit (Streamlit UI).
    """
    console.print("[bold green]Starting DataEngOS Cockpit...[/bold green]")
    
    # Locate the streamlit app file relative to this script
    # This assumes dataeng_os/commands/ui.py -> dataeng_os/ui/main.py
    # We need to find the package path
    
    import dataeng_os
    package_dir = os.path.dirname(dataeng_os.__file__)
    ui_path = os.path.join(package_dir, "ui", "main.py")
    
    if not os.path.exists(ui_path):
        console.print(f"[red]Error: UI entrypoint not found at {ui_path}[/red]")
        raise typer.Exit(1)
        
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", ui_path], check=True)
    except KeyboardInterrupt:
        console.print("\n[yellow]UI Stopped.[/yellow]")

if __name__ == "__main__":
    app()
