# Update and Delete Books Exercise

## Learning goals

- Explain how `PUT` updates a resource and `DELETE` removes one.
- Use a path parameter to identify a particular book by its `id`.
- Write SQL `UPDATE` and `DELETE` statements with parameter placeholders.
- Return a useful response when the requested book does not exist.

## Start by exploring

The books API already supports creating a book with `POST /create-book` and retrieving all books with `GET /get-books`. Use `GET /get-books` to inspect the JSON objects and notice that each book has an `id`. That ID identifies the row to change or remove.

An API request has a method, a URL, and sometimes a body:

| Action | Method | Suggested URL | Request body |
| --- | --- | --- | --- |
| Replace a book's title and author | `PUT` | `/books/{book_id}` | JSON with `title` and `author` |
| Delete one book | `DELETE` | `/books/{book_id}` | None |

For example, `/books/3` refers to the book whose `id` is `3`. The `{book_id}` part is a path parameter that FastAPI can convert to an integer. `PUT` uses the existing `BookCreate` schema because this exercise replaces both editable fields. `DELETE` needs no request body.

The current project uses `/create-book` and `/get-books` for its existing endpoints. The suggested URLs above use a resource-style pattern for the new endpoints. The exact path is a design choice; the method and behavior should make the operation clear.

## Plan the database operations

Before coding, describe these steps in plain language:

1. Read the book ID from the URL.
2. For an update, validate the new title and author from the JSON body.
3. Open a database connection and execute a parameterized SQL statement that targets only the row with that ID.
4. Commit a successful change, then close the connection.
5. Determine whether a row matched the ID. SQLite's cursor has a `rowcount` property that can help.
6. If no row matched, return HTTP `404 Not Found`. FastAPI's `HTTPException` can represent this error.

The SQL shapes to complete are:

```sql
UPDATE books
SET title = ?, author = ?
WHERE id = ?
```

```sql
DELETE FROM books
WHERE id = ?
```

The question marks are parameter placeholders. Pass their values separately to `connection.execute()` as a tuple, just as the create route does. Do not build SQL by inserting values directly into the SQL string.

## Exercise

Implement both endpoints in `app/routers/books.py`.

### Update endpoint

- Accept a `book_id` path parameter and a `BookCreate` request body.
- Update the title and author only for the row with that ID.
- Commit and close the database connection.
- If no row has that ID, return `404 Not Found`.
- On success, return the updated book's `id`, `title`, and `author` as JSON.

### Delete endpoint

- Accept a `book_id` path parameter and no request body.
- Delete only the row with that ID.
- Commit and close the database connection.
- If no row has that ID, return `404 Not Found`.
- On success, return a clear confirmation or use an empty `204 No Content` response.

Use `APIRouter` and the database helper already used by the other book endpoints. Import any FastAPI classes needed for errors or response status codes. Keep the SQL operation in the route and use placeholders for all values.

## Try the endpoints

Use `/docs` or another API client to check the behavior:

1. Create two books with different IDs.
2. Retrieve all books and note one ID.
3. Update that book, then retrieve all books to confirm only that row changed.
4. Try updating an ID that does not exist and confirm the API returns `404`.
5. Delete the updated book, then retrieve all books to confirm it is gone.
6. Try deleting the same ID again and confirm the API returns `404`.