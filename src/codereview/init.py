import os
import click
import yaml
from .database import initialize_database

@click.command(name="init")
def init_command():
    project_root = os.getcwd()
    config_dir = os.path.join(project_root, '.codereview')
    config_file_path = os.path.join(config_dir, 'config.yaml')
    database_path = os.path.join(config_dir, 'database.db')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        click.echo("Created configuration directory.")

    # Initialize the database
    initialize_database(database_path)

    # Create default configuration
    default_config = {
        'project_name': os.path.basename(project_root),
        'project_root': project_root,
        'default_files_to_scan': '*.py',  # Or another default
        'excluded_directories': ['venv', 'node_modules', '.idea'],
        'database_path': database_path,
        # Add other configuration fields as needed
    }

    with open(config_file_path, 'w') as config_file:
        yaml.dump(default_config, config_file, default_flow_style=False)

    click.echo("Project initialized successfully.")