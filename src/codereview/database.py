# src/codereview/database.py
import os
import sqlite3
import typing as t
from pathlib import Path

import click

from codereview.models import Run, Module, Snapshot, Message
from .utils import find_config_file, read_config


def initialize_database(db_path: str):
    # Ensure the directory for the database exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # Connect to the SQLite Database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Modules (
                        id INTEGER PRIMARY KEY,
                        path TEXT NOT NULL,
                        first_reviewed TIMESTAMP,
                        last_reviewed TIMESTAMP,
                        first_snapshot INTEGER,
                        last_snapshot INTEGER
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Runs (
                        id INTEGER PRIMARY KEY,
                        timestamp TIMESTAMP NOT NULL,
                        files_analyzed TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Snapshots (
                        id INTEGER PRIMARY KEY,
                        snapshot_id TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        summary TEXT,
                        module_id INTEGER,
                        FOREIGN KEY (module_id) REFERENCES Modules (id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Messages (
                        id INTEGER PRIMARY KEY,
                        timestamp TIMESTAMP NOT NULL,
                        content TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Reviews (
                        id INTEGER PRIMARY KEY,
                        timestamp TIMESTAMP NOT NULL,
                        content TEXT NOT NULL
                      )''')

    # Commit and close connection
    conn.commit()
    conn.close()


@click.command(name="wipe-db")
def wipe_db_command():
    """Wipe the database and reinitialize it."""
    try:
        config_file_path = find_config_file()
        config = read_config(config_file_path)
        db_path = config.get("database_path")

        if os.path.exists(db_path):
            print(f"Found database at {db_path}.")
            user_input = input("Are you sure you want to wipe the database? [y/N] ")
            if user_input.lower() != 'y':
                click.echo("Aborting.")
                return
            os.remove(db_path)
            click.echo("Database wiped.")

        initialize_database(db_path)
        click.echo("Database reinitialized.")
    except FileNotFoundError as e:
        click.echo(str(e))


class Database:

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def insert_run(self, timestamp: str, files_analyzed: str):
        self.cursor.execute("INSERT INTO Runs (timestamp, files_analyzed) VALUES (?, ?)", (timestamp, files_analyzed))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_module(
            self,
            path: str,
            first_reviewed: str,
            last_reviewed: str,
            first_snapshot: int,
            last_snapshot: t.Optional[int]) -> Module:
        """Insert a module into the database.

        Args:
            path (str):
            first_reviewed ():
            last_reviewed ():
            first_snapshot ():
            last_snapshot ():

        Returns:

        """
        self.cursor.execute(
            "INSERT INTO Modules (path, first_reviewed, last_reviewed, first_snapshot, last_snapshot) VALUES (?, ?, ?, ?, ?)",
            (path, first_reviewed, last_reviewed, first_snapshot, last_snapshot))
        self.conn.commit()
        module = self.get_module_by_filepath(path)
        return module

    def insert_snapshot(self, *, snapshot_id: str, timestamp: str, summary: str, module_id: int) -> Snapshot:
        self.cursor.execute("INSERT INTO Snapshots (snapshot_id, timestamp, summary, module_id) VALUES (?, ?, ?, ?)",
                            (snapshot_id, timestamp, summary, module_id))
        self.conn.commit()
        snapshot = self.get_snapshot_by_snapshot_id(snapshot_id)
        return snapshot

    def insert_message(self, timestamp: str, content: str):
        self.cursor.execute("INSERT INTO Messages (timestamp, content) VALUES (?, ?)", (timestamp, content))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_review(self, *, timestamp: str, content: str):
        self.cursor.execute("INSERT INTO Reviews (timestamp, content) VALUES (?, ?)", (timestamp, content))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_run(self, id: int) -> Run:
        self.cursor.execute("SELECT * FROM Runs WHERE id=?", (id,))
        result = self.cursor.fetchone()
        files_analyzed = result[2].split(',')
        files_analyzed = [file.strip() for file in files_analyzed]
        run = Run(id=result[0], timestamp=result[1], files_analyzed=files_analyzed)
        return run

    def get_module(self, id: int):
        self.cursor.execute("SELECT * FROM Modules WHERE id=?", (id,))
        result = self.cursor.fetchone()
        module = Module(id=result[0], path=result[1], first_reviewed=result[2], last_reviewed=result[3],
                        first_snapshot=result[4], last_snapshot=result[5])
        return module

    def get_module_by_filepath(self, filepath: str):
        self.cursor.execute("SELECT * FROM Modules WHERE path=?", (filepath,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        module = Module(id=result[0], path=result[1], first_reviewed=result[2], last_reviewed=result[3],
                        first_snapshot=result[4], last_snapshot=result[5])
        return module

    def get_snapshot(self, id: int):
        self.cursor.execute("SELECT * FROM Snapshots WHERE id=?", (id,))
        result = self.cursor.fetchone()
        snapshot = Snapshot(id=result[0], snapshot_id=result[1], timestamp=result[2], summary=result[3],
                            module_id=result[4])
        return snapshot

    def get_snapshot_by_snapshot_id(self, snapshot_id: str):
        self.cursor.execute("SELECT * FROM Snapshots WHERE snapshot_id=?", (snapshot_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        snapshot = Snapshot(id=result[0], snapshot_id=result[1], timestamp=result[2], summary=result[3],
                            module_id=result[4])
        return snapshot

    def get_message(self, id: int):
        self.cursor.execute("SELECT * FROM Messages WHERE id=?", (id,))
        result = self.cursor.fetchone()
        message = Message(id=result[0], timestamp=result[1], content=result[2])
        return message

    def get_review(self, id: int):
        self.cursor.execute("SELECT * FROM Reviews WHERE id=?", (id,))
        result = self.cursor.fetchone()
        review = Message(id=result[0], timestamp=result[1], content=result[2])
        return review
