# Template: Five HTTP Methods for the Books API

This template covers the five methods used in this lesson: **GET, POST, PUT, PATCH, and DELETE**. Each route uses a method and URL to describe the requested action.

| Method | Purpose | Route in this app | Body |
| --- | --- | --- | --- |
| GET | Retrieve all books | `/api/books` | None |
| POST | Create a book | `/create-book` | Title and author |
| PUT | Replace a book's title and author | `/books/{book_id}` | Title and author |
| PATCH | Change only supplied fields | `/books/{book_id}` | One or both fields |
| DELETE | Remove a book | `/books/{book_id}` | None |

`book_id` identifies a particular row. For update and delete routes, return `404 Not Found` if no book has that ID. The current GET and POST routes are already implemented; use their code as a guide while completing their TODO notes and adding PUT, PATCH, and DELETE.

## Request model for PATCH

In `app/schemas.py`, add a model with optional fields and the same validation limits as `BookCreate`. Decide how to handle whitespace and a PATCH request with no fields.

```python
class BookUpdate(BaseModel):
    # TODO: Configure whitespace handling.
    # TODO: Add optional title and author fields with validation limits.
    pass
```

## Route templates

In `app/routers/books.py`, use `get_connection()` for database access. Add any imports needed, then complete the TODOs. The `BookCreate` model already validates title and author for POST and PUT.

```python
@router.get("/api/books")
def get_all_books():
    # TODO: Select all books, fetch the rows, close the connection,
    #       and return the rows as JSON-friendly dictionaries.
    pass


@router.post("/create-book")
def create_book(book: BookCreate):
    # TODO: Insert the book using SQL placeholders, commit, close,
    #       and return the created book.
    pass


@router.put("/books/{book_id}")
def replace_book(book_id: int, book: BookCreate):
    # TODO: Replace both fields for this ID; handle a missing row.
    pass


@router.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    # TODO: Change only supplied fields; handle an empty body and
    #       a missing row.
    pass


@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    # TODO: Delete this ID; handle a missing row and choose a success response.
    pass
```

Use `WHERE id = ?` and pass values separately to `connection.execute()`. A cursor's `rowcount` can tell whether an update or delete matched a row. For PATCH, `model_dump(exclude_unset=True)` returns only fields the client sent. Use `HTTPException` for a 404.

## Check your work in `/docs`

1. Create two books and retrieve them; confirm GET returns both.
2. Try POST with valid and invalid data.
3. PUT both fields for one ID; confirm the other book is unchanged.
4. PATCH one field; confirm the other stays the same. Decide what an empty PATCH should do.
5. DELETE one book and retrieve the list to confirm it is gone.
6. Try PUT, PATCH, and DELETE with an ID that does not exist; confirm each returns 404.

Close database connections after use and use SQL placeholders for values.
