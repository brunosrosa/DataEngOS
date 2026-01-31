import typer
from dataeng_os.commands import validate, init, scaffold, ui

app = typer.Typer(
    name="dataeng-os",
    help="Specification-Driven Data Engineering Operating System CLI",
    add_completion=False,
)

app.add_typer(validate.app, name="validate")
app.add_typer(init.app, name="init")
app.add_typer(scaffold.app, name="scaffold")
app.add_typer(ui.app, name="ui")

if __name__ == "__main__":
    app()
