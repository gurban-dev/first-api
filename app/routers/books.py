from fastapi import APIRouter

from app.database import get_connection
from app.schemas import BookCreate

# This is for book-related endpoints.

router = APIRouter()


# The following type annotation/hint forces the data to conform
# to the BookCreate model:
# book: BookCreate
@router.post("/create-book")
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

@router.get("/api/books")
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


# 1. Client sends a PUT request

# 2. FastAPI identifies the book by looking at the ID.

# 3. The server executes the SQL UPDATE

# 4. The server returns the updated book.
