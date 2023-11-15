from .database import Database


class Context:
    db: Database

    def __init__(self):
        pass

    def set_config(self, config):
        self.config = config

    def initialize_database(self, db_path):
        # Assuming you have a function to initialize and return the database connection
        self.db = Database(db_path)
