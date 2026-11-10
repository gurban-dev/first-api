import logging
import json
import sqlite3

# closing() guarantees that database connections are closed,
# including when an exception occurs.
from contextlib import asynccontextmanager, closing

# The Path class is imported from Python's built-in pathlib module 
# so that we can create a path object to locate the database file. 
# This is preferable over hardcoding a string path, which breaks if 
# someone else pulls the project or if you move the project folder.
from pathlib import Path

# Importing the class named FastAPI this way we can create a
# FastAPI application.

# HTTPException returns HTTP errors with appropriate status
# codes and messages.

# status provides readable names for HTTP status codes.
from fastapi import FastAPI, HTTPException, Request, Response, status

# StaticFiles serves CSS, JavaScript, images, and other static files.
# "Serving" means delivering these pre-made resources (stylesheets,
# client-side scripts, and media files) directly to the user's browser.

# Client-side scripts almost always mean JavaScript files.
# static/js/app.js in this case.
from fastapi.staticfiles import StaticFiles

# See lesson-notes/jinja2.md.
from fastapi.templating import Jinja2Templates

# ConfigDict changes how a Pydantic model processes data as seen
# with ConfigDict(str_strip_whitespace=True) below.

# Field defines validation rules for model fields as seen below
# with Field(min_length=1, max_length=200).
from pydantic import BaseModel, ConfigDict, Field

# Enables logging so that status updates are outputted while the
# application runs.
logging.basicConfig(level=logging.INFO)

# Creates an instance of the Logger class that prefixes every
# outputted message with the module's name so you know exactly
# which file sent it.

# The module's name is '__main__' when run directly and 'main'
# when this file is imported. The dunder variable __name__
# references the module's name.
logger = logging.getLogger(__name__)

# Creates a Path object holding the absolute path to the directory
# containing this script.
BASE_DIR = Path(__file__).resolve().parent

# Combines the directory path with a filename to create a complete
# path to the database file.
DATABASE_PATH = BASE_DIR / "books.db"

# A lifespan function is a special function in FastAPI that manages
# the entire lifecycle of the application. It defines exactly what
# must happen when the application starts up and when it shuts down.

# An Asynchronous Context Manager is a tool that enforces a strict
# three-step sequence:
# 1. (Setup): Runs code before 'yield' (e.g., opens a database
#             connection).

# 2. (Pause): Pauses at 'yield' and hands control to the app to
#             handle requests.

# 3. (Teardown): Automatically runs code after 'yield' when the
#                server turns off (e.g., closes the database
#                connection), guaranteeing cleanup even if the app
#                crashes.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs exactly once when the server starts up.
    initialize_database()

    yield

    # Any code written here runs when the server completely
    # shuts down.

# This creates an instance/object of the FastAPI class.

# Create the application.
app = FastAPI(lifespan=lifespan)

# FastAPI does not automatically know where to find or serve
# frontend assets such as CSS, JavaScript, images, and fonts.
# We mount a static file-serving application so that browsers
# can request these files through HTTP.

# "/static" defines the URL prefix for accessing these files.
# For example, static/css/styles.css becomes /static/css/styles.css.

# StaticFiles serves files from the specified directory.

# BASE_DIR / "static" constructs the absolute path to the
# project's static directory, regardless of where the app starts.

# name="static" allows Jinja2 templates to generate static file
# URLs using url_for("static", ...).
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Create a Jinja2Templates instance that allows FastAPI to render
# HTML files using the Jinja2 templating engine.

# Rendering means taking an HTML template, inserting dynamic data
# into it if there is any and returning the resulting HTML to the
# client's browser.

# The directory parameter specifies where FastAPI should look
# for HTML template files.

# BASE_DIR / "templates" constructs an absolute path to the
# templates directory located inside the project directory.
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

# Register a GET endpoint at /add-book to display the book
# creation form.

# Exclude this endpoint from /docs because it serves an HTML
# page for users, not an API operation intended for API consumers.
@app.get("/add-book", include_in_schema=False)
def add_book(request: Request):

    # Convert index.html into an HTML page and send it to the browser.
    return templates.TemplateResponse(

        # Pass the incoming HTTP request because Jinja2Templates
        # needs it to generate the HTML page.
        request=request,

        # Specify the HTML file that should be used for the page.
        name="index.html",

        # Pass data from Python to the HTML file.
        # An empty dictionary {} means no additional data is needed.
        context={}
    )

# Register an endpoint.

# @ indicates that line 161 is a decorator.
# Tells FastAPI to call the say_hello() function when a client sends
# GET request to /hello.

# A GET request is sent to retrieve information.
@app.get("/hello")
def say_hello():
    # In Python, a dictionary is being returned.

    # When it reaches the user's web browser, it becomes a JSON
    # string (raw text):
    # '{"message": "Hello, world!"}'
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

initialize_database()

# FastAPI needs a way to validate the JSON data received from
# the client.

# The BookCreate class is inheriting from BaseModel.

# Without BaseModel, a standard Python class is not capable of
# identifying invalid data.

# FastAPI converts the JSON text into a Python dictionary, and 
# BaseModel ensures that it matches the predefined structure.

# The predefined structure requires two incoming pieces of data
# to use the exact lowercase keys "title" and "author", and both
# values must be strings.
class BookCreate(BaseModel):
    # ConfigDict(str_strip_whitespace=True) removes leading
    # and trailing spaces from all input strings automatically
    # before validating them.
    model_config = ConfigDict(str_strip_whitespace=True)

    # Ensures fields aren't blank: title allows 1 to 200 characters, 
    # while author allows 1 to 120 characters.
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)

# The following type annotation/hint forces the data to conform
# to the BookCreate model:
# book: BookCreate
@app.post("/create-book")
def create_book(book: BookCreate):
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
    # by accessing the lastrowid property.
    book_id = cursor.lastrowid

    connection.close()

    # Sending the book's information back to the client.
    return {
        "id": book_id,
        "title": book.title,
        "author": book.author
    }

@app.get("/get-books")
def get_all_books():
    # Establish a database connection.
    connection = get_connection()

    # Execute the SQL query and get back a sqlite3.Cursor object
    # containing the results.
    cursor = connection.execute("SELECT * FROM books")

    # Retrieve all rows from the sqlite3.Cursor object and store
    # them in a list.
    books = cursor.fetchall()

    # Close the database connection.
    connection.close()

    books_list = []

    for book in books:
        books_list.append(dict(book))

    return books_list