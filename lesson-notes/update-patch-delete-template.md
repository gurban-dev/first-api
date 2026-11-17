# Template: Update and Delete Books

Use this template to implement three endpoints in this project. The route shells are provided; fill in the TODOs and test each endpoint in `/docs`.

The existing `BookCreate` model in `app/schemas.py` requires both `title` and `author`. Use it for `PUT`, which replaces both editable fields. For `PATCH`, first create a `BookUpdate` model whose fields may be omitted. Decide how to prevent an empty PATCH request from silently succeeding.

## Request and response plan

| Operation | Method and path | Example request body | Success result |
| --- | --- | --- | --- |
| Replace title and author | `PUT /books/{book_id}` | `{"title": "New title", "author": "New author"}` | Return the updated book as JSON |
| Change supplied fields only | `PATCH /books/{book_id}` | `{"title": "New title"}` | Return the updated book as JSON |
| Remove a book | `DELETE /books/{book_id}` | No body | Return a confirmation or `204 No Content` |

If the ID does not identify a book, each endpoint should return `404 Not Found`.

## Part 1: Add a PATCH request model

In `app/schemas.py`, add a model for partial book updates. Use optional fields with the same length limits as `BookCreate`. Consider how the model should handle whitespace and what the route should do if neither field was provided.

```python
class BookUpdate(BaseModel):
    # TODO: Configure whitespace handling.
    # TODO: Add optional title and author fields with validation limits.
    pass
```

## Part 2: Add route shells

In `app/routers/books.py`, update the imports to include the model and FastAPI types you need. Complete the route functions below.

```python
@router.put("/books/{book_id}")
def replace_book(book_id: int, book: BookCreate):
    # TODO: Open a database connection.
    # TODO: Update both title and author for this ID using SQL placeholders.
    # TODO: Check whether a row matched; if not, return HTTP 404.
    # TODO: Commit, close the connection, and return the updated book.
    pass


@router.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    # TODO: Get only the fields the client supplied.
    # TODO: Decide how to handle a request with no fields.
    # TODO: Open a database connection and update only supplied fields
    #       for this ID, using SQL placeholders.
    # TODO: Check whether a row matched; if not, return HTTP 404.
    # TODO: Commit, close the connection, and return the updated book.
    pass


@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    # TODO: Open a database connection.
    # TODO: Delete only the row with this ID.
    # TODO: Check whether a row matched; if not, return HTTP 404.
    # TODO: Commit, close the connection, and return a confirmation
    #       or an empty 204 response.
    pass
```

### Hints

- Follow the existing book routes' use of `get_connection()`.
- Use `WHERE id = ?` so only the selected row is affected.
- Pass values to `connection.execute()` separately from the SQL string.
- A cursor's `rowcount` can tell you whether an update or delete matched a row.
- For PATCH, Pydantic's `model_dump(exclude_unset=True)` can return only fields the client sent. Build the SQL update from those fields and bind the values as parameters.
- Use FastAPI's `HTTPException` to return a `404` response.

## Part 3: Test your implementation

Use `/docs` or another API client:

1. Create two books and record their IDs.
2. Use PUT on one ID with both fields; verify the other book is unchanged.
3. Use PATCH on that ID with only `title`; verify its author is unchanged.
4. Use PATCH with only `author`; verify its title is unchanged.
5. Try PATCH with an empty JSON object and confirm your chosen behavior.
6. Use DELETE on that ID; verify it no longer appears in `GET /get-books`.
7. Try each operation with a nonexistent ID and confirm it returns `404`.

## Before you finish

- [ ] PUT requires both editable fields and replaces them.
- [ ] PATCH changes only fields included in the request.
- [ ] DELETE removes only the requested book.
- [ ] All SQL values use placeholders.
- [ ] Each route handles an ID that does not exist.
- [ ] Connections are closed after database work.
- [ ] The success response matches the behavior documented above.
