import sqlite3
from pathlib import Path


# Creates a Path object holding the absolute path to the directory
# containing this script.
BASE_DIR = Path(__file__).resolve().parent

# Combines the directory path with a filename to create a complete
# path to the database file.
DATABASE_PATH = BASE_DIR / "books.db"


def get_connection():
    # Creates a link between this Python program and the books.db
    # database file and returns an sqlite3.Connection object.
    connection_obj = sqlite3.connect("books.db")

    # SQLite by default delivers the data as tuples
    # (1, 'Catch-22', 'Joseph Heller')

    # By writing sqlite3.Row, the data is being tansformed
    # into a hybrid that behaves like a tuple and a dictionary.

    # Without sqlite3.Row, you access the data by only using
    # numerical indexes:
    # print(row[0])
    # print(row[1])
    # print(row[2])

    # With sqlite3.Row, you can access the data by using both
    # numerical indexes and column names:
    # print(row["id"])
    # print(row["title"])
    # print(row["author"])

    connection_obj.row_factory = sqlite3.Row

    return connection_obj


def initialize_database():
    # First open a connection to the database.
    connection = get_connection()

    # Create the database if it does not already exist.

    # A SIN (social insurance number) is an example of a primary
    # key because it can be used to uniquely identify an individual.
    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    # Save the data to the database file.
    connection.commit()

    # Disconnect to release the file lock; when a connection is opened, the file 
    # is locked, and leaving it open will cause "database is locked" errors later.
    connection.close()