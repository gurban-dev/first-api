import json
import sqlite3

# Importing the class named FastAPI this way we can create a
# FastAPI application.
from fastapi import FastAPI, Response
from pydantic import BaseModel

# This creates an instance/object of the FastAPI class.

# Create the application.
app = FastAPI()

# Register an endpoint.

# @ indicates that that line 17 is a decorator.
# Tells FastAPI to call the say_hello() function when a client sends
# GET request to /hello.

# A GET request is sent to retrieve information.
@app.get("/hello")
def say_hello():
    return {"message": "Hello, world!"}

# The say_hello() function contains the logic for the endpoint.

# The {name} part if a path parameter, meaning a value supplied
# as part of the URL path.

# If the client visits /greet/john, FastAPI passes "john" to the
# function as name.

@app.get("/greet/{name}")
def greet_person(name: str):
    return {"message": f"Hello, {name.capitalize()}!"}

# The client will send a GET request to the endpoint /square/5,
# and should receive back:
# {"number": 5, "square": 25}

# Implmement a function that handles not only this particular
# example, but any number that is passed as a path parameter.

@app.get("/square/{num}")
def calculate_square(num: int):
    # FastAPI extracts num from the URL and converts it to an integer.
    # For example, a request to /square/5 sets num to 5.
    square = num**2

    data = {
        "number": num,
        "square": square
    }

    # Double braces {{ and }} produce literal braces in an f-string.
    # The resulting string must follow JSON syntax.
    dict_in_f_str = f'{{"number": {num}, "square": {square}}}'

    return Response(
        # json.dumps() converts a Python object into a JSON-formatted
        # string. It can serialize the dictionary directly.
        # content=json.dumps(data, indent=2),

        # Return the manually constructed JSON string instead.
        # This works here, but json.dumps() is safer for general data
        # because it correctly escapes strings and other special values.
        content=dict_in_f_str,

        # Tell the client that the response contains JSON.
        media_type="application/json"
    )

def get_connection():
    # Creates a link between this Python program and the books.db
    # database file and returns an sqlite3.Connection object.
    connection_obj = sqlite3.connect("books.db")

    # SQLite by default delivers the data as tuples
    # (1, 'Catch-22', 'Joseph Heller')

    # By writing sqlite3.Row, the data is being tansformed
    # into a hybrid that behaves like a tuple and a dictionary.
    connection_obj.row_factory = sqlite3.Row

    return connection_obj

def initialize_database():
    # First open a connection to the database.
    connection = get_connection()

    # Create the database if it does not already exist.

    # SIN (social insurance number) is an example of a primary
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

    # Disconnect the program from the database file.
    connection.close()

initialize_database()

# FastAPI needs a way to validate the JSON data received from
# the client.

# The BookCreate class is inheriting from BaseModel.

# Without BaseModel, a standard Python class is not capable of
# identifying invalid data.

# BaseModel takes JSON text and makes sure that it matches the
# predefined structure.

# The predefined structure requires that two pieces of information
# are provided, the incoming data must use exact lowercase keys
# "title" and "author" and must be strings.
class BookCreate(BaseModel):
    title: str
    author: str

# The following type annotation/hint forces the data to conform
# to the BookCreate model:
# book: BookCreate
@app.post("/create-book")
def create_book(book: BookCreate):
    book = BookCreate(
        title="The Hobbit",
        author="J.R.R. Tolkien"
    )

    # Open a connection to the database file.
    connection = get_connection()

    # A database cursor is an object used to execute SQL statements.

    # "object" is an instance of a Python class.

    # The object returned by connection.execute() is an instance
    # of the sqlite3.Cursor class.

    # The ID is not manually inserted because SQLite was configured
    # to generate it automatically. The keyword AUTOINCREMENT specifies
    # that SQLite will automatically generate an ID for each inserted
    # book. Configure means to write an instruction that alters how
    # a system behaves.

    # Insert a new row into the books table.
    # Put the first supplied value into title column.
    # Put the second supplied value into author column.
    # The question marks act as placeholders.
    cursor = connection.execute(
        """
        INSERT INTO books (title, author)
        VALUES (?, ?)
        """,
        (book.title, book.author)
    )

    connection.commit()

    # Get the ID that SQLite automatically created on its own
    # by invoking the lastrowid property.
    book_id = cursor.lastrowid

    connection.close()

    # Sending the book's information back to the client.
    return {
        "id": book_id,
        "title": book.title,
        "author": book.author
    }