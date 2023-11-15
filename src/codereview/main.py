import click
from .config import config_command
from .analyze import analyze_command
from .report import report_command
from .update import update_command
from .init import init_command
from .database import wipe_db_command


@click.group()
def cli():
    """Your code review tool."""
    pass


cli.add_command(config_command, name="config")
cli.add_command(analyze_command, name="analyze")
cli.add_command(report_command, name="report")
cli.add_command(update_command, name="update")
cli.add_command(init_command, name="init")
cli.add_command(wipe_db_command, name="wipe-db")

if __name__ == "__main__":
    cli()

