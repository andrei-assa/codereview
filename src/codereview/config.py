"""This module contains the command line interface for the config command.

"""
import click
from .utils import read_config, write_config, find_config_file

@click.group()
def config_command():
    """This function implements the config command.

    Returns:

    """
    pass

@config_command.command(name='list')
def list_config():
    """List all configuration values."""
    try:
        config_file_path = find_config_file()
        config_data = read_config(config_file_path)
        for key, value in config_data.items():
            click.echo(f"{key}: {value}")
    except FileNotFoundError as e:
        click.echo(str(e))

@config_command.command(name='set')
@click.argument('key')
@click.argument('value')
def set_config(key, value):
    """Set a configuration value."""
    try:
        config_file_path = find_config_file()
        config_data = read_config(config_file_path)

        # Update the configuration
        config_data[key] = value
        write_config(config_file_path, config_data)

        click.echo(f"Configuration updated: {key} = {value}")
    except FileNotFoundError as e:
        click.echo(str(e))


@config_command.command(name='get')
@click.argument('key')
def get_config(key):
    """Get a configuration value."""
    try:
        config_file_path = find_config_file()
        config_data = read_config(config_file_path)
        value = config_data.get(key, "Key not found")
        click.echo(f"{key}: {value}")
    except FileNotFoundError as e:
        click.echo(str(e))



