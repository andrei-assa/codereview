# src/codereview/analyze.py
import glob
import os
import hashlib
from datetime import datetime

import click

from .context import Context
from .database import Database
from .reviewer import Reviewer
from .utils import read_config, find_config_file


@click.group()
@click.pass_context
def analyze_command(ctx):
    if ctx.obj is None:
        ctx.obj = Context()

    config_file_path = find_config_file()
    config = read_config(config_file_path)
    ctx.obj.set_config(config)
    filepath = config.get("database_path")
    ctx.obj.initialize_database(filepath)


@analyze_command.command(name="run")
@click.option("--path", default=None, help="The path to the file or directory to analyze.")
@click.pass_context
def analyze_run_command(ctx, path: str):
    """Analyze the given file or directory."""
    try:
        config = ctx.obj.config
        analyze_path = path if path else config.get("source_directory", os.getcwd())
        reviews = perform_analysis(analyze_path, config, ctx.obj.db)
    except FileNotFoundError as e:
        click.echo(str(e))


def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def perform_analysis(base_path, config, db: Database):
    """Perform analysis on the given path.

    Args:
        base_path ():
        config ():
        db ():

    Returns:

    """
    # Define the pattern for files to scan
    pattern = config.get('default_files_to_scan', '*.py')
    excluded_dirs = config.get('excluded_directories', [])

    # Log the new run
    filepaths = get_filepaths(base_path, pattern, excluded_dirs)
    run_id = db.insert_run(datetime.now().isoformat(), ','.join(filepaths))

    # Initialize the reviewer
    reviewer = Reviewer()  # Add API key and model if needed

    # Traverse and analyze files
    new_filepaths = []
    path_to_module_id = {}
    for filepath in filepaths:
        module = db.get_module_by_filepath(filepath)  # This method needs to be implemented in Database class
        if module is None:
            module = db.insert_module(filepath, datetime.now().isoformat(), datetime.now().isoformat(), run_id, None)
        path_to_module_id[filepath] = module['id']

        module_hash = hash_file(filepath)
        snapshot = db.get_snapshot_by_snapshot_id(module_hash)  # This method needs to be implemented in Database class
        if snapshot is None:
            new_filepaths.append(filepath)
        else:
            continue

    if new_filepaths:
        reviews = reviewer.review_batch(new_filepaths)
        for review in reviews:
            db.insert_snapshot(
                snapshot_id=hash_file(review['path']),
                summary=review['review'],
                timestamp=datetime.now().isoformat(),
                module_id=path_to_module_id[review['path']]
            )
            db.insert_review(
                timestamp=datetime.now().isoformat(),
                content=review['review'])
        return reviews


def get_filepaths(base_path, pattern, excluded_dirs):
    filepaths = []
    for root, dirs, files in os.walk(base_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]  # Exclude specified directories
        for file in files:
            if glob.fnmatch.fnmatch(file, pattern):
                file_path = os.path.join(root, file)
                filepaths.append(file_path)
    return filepaths
