from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import BookCreate, BookPatch

# This is for book-related endpoints.

# Create an APIRouter to group related endpoints together,
# keeping the application organised across multiple files.
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

@router.get("/get-all-books")
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

# How the Client and Server Update a Book
# 1. The client sends a PUT request

# 2. FastAPI identifies the book by looking at the ID.

# 3. The server executes the SQL UPDATE

# 4. The server returns the updated book.
@router.put("/replace-book/{book_id}")
def replace_book(book_id: int, book: BookCreate):
    # cursor is an object that provides information about the
    # operation that was performed.
    connection = get_connection()

    # UPDATE is an SQL command used to modify existing records
    # in a database.

    # SET specifies which columns we want to change and what
    # their new values should be.

    # The question mark (?) represents a parameter placeholder.
    # The actual values are supplied in the tuple which is the
    # second argument.

    # Checks whether the SQL operation affected any rows in the
    # database.
    cursor = connection.execute(
        """
        UPDATE books
        SET title = ?, author = ?
        WHERE id = ?
        """,
        (book.title, book.author, book_id)
    )

    # The rowcount attribute reveals how many rows were affected
    # by the SQL operation.

    # If cursor.rowcount is equal to zero, it means that no database
    # rows were affected by the SQL query.
    if cursor.rowcount == 0:
        # Closes the connection between this Python program and
        # thee SQLite database.
        connection.close()

        # Stop processing the current request and return an HTTP
        # error response to the client.
        raise HTTPException(status_code=404, detail="Book not found")

    connection.commit()
    connection.close()

    return {
        "id": book_id,
        "title": book.title,
        "author": book.author
    }


@router.patch("/update-book/{book_id}")
def update_book(book_id: int, book: BookPatch):
    updates = book.model_dump(exclude_unset=True)

    if len(updates) != 1:
        raise HTTPException(
            status_code=422,
            detail="Provide exactly one field: title or author"
        )

    field, value = next(iter(updates.items()))

    if field not in {"title", "author"} or value is None:
        raise HTTPException(
            status_code=422,
            detail="Provide a non-null title or author"
        )

    connection = get_connection()
    cursor = connection.execute(
        f"UPDATE books SET {field} = ? WHERE id = ?",
        (value, book_id)
    )

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Book not found")

    connection.commit()
    updated_book = connection.execute(
        "SELECT id, title, author FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()
    connection.close()

    return dict(updated_book)