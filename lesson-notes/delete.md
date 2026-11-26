# How deleting a book works

This lesson follows one book from the moment the user clicks **Delete Book** to the SQL operation and the response in the browser. By the end, a student should be able to explain the request and implement the same flow for another resource.

## The flow at a glance

```text
Click a book -> click Delete Book
  -> JavaScript reads the selected book ID
  -> fetch sends DELETE /delete-book/{id}
  -> FastAPI matches the route and calls delete_book(id)
  -> SQLite deletes the matching row
  -> FastAPI returns JSON (or a 404 error)
  -> JavaScript removes the book from the page and updates the count
```

## 1. The page identifies each book

In `templates/index.html`, every book is rendered with its ID in a data attribute:

```html
<button
    type="button"
    class="book-list-item"
    data-book-id="{{ book.id }}"
    data-title="{{ book.title }}"
    data-author="{{ book.author }}"
>
    <span class="book-list-title">{{ book.title }}</span>
    <span class="book-list-author">{{ book.author }}</span>
</button>
```

The **Delete Book** action is in the same book item:

```html
<button type="button" data-action="delete">
    Delete Book <span>(DELETE request)</span>
</button>
```

The book ID is important: titles and authors can repeat, but the database ID identifies one particular row. Clicking a book first reveals its actions and stores its ID in `selectedBook` in `static/js/books.js`.

## 2. JavaScript handles the click

`books.js` registers one click listener on the list. This is called **event delegation**: clicks on buttons inside the list bubble up to the list, where the handler checks which button was clicked.

```javascript
const actionButton = event.target.closest("button[data-action]");

if (!actionButton || !selectedBook) {
    return;
}

if (actionButton.dataset.action === "delete") {
    sendUpdate("DELETE", null);
}
```

The selected book was saved when its title button was clicked:

```javascript
selectedBook = {
    id: Number(button.dataset.bookId),
    title: button.dataset.title,
    author: button.dataset.author
};
```

So clicking **Delete Book** calls `sendUpdate` with the HTTP method `DELETE`. The `null` means this request has no JSON body: the ID in the URL is enough to say which book to delete.

## 3. `fetch` sends the HTTP request

Inside `sendUpdate`, JavaScript maps the method to the endpoint name and constructs the URL:

```javascript
const endpoint = method === "PUT"
    ? "replace-book"
    : method === "PATCH"
        ? "update-book"
        : "delete-book";

const options = { method };
const response = await fetch(`/${endpoint}/${selectedBook.id}`, options);
const data = await response.json();
```

For a selected book whose ID is `12`, the browser sends:

```http
DELETE /delete-book/12
```

There is no request body and no `Content-Type` header. The `await` pauses this function until the server responds. `response.json()` reads the response body as JSON.

## 4. FastAPI matches the route

In `app/routers/books.py`, FastAPI connects the URL and HTTP method to a Python function:

```python
@router.delete("/delete-book/{book_id}")
def delete_book(book_id: int):
```

`{book_id}` is a path parameter. For `/delete-book/12`, FastAPI converts `12` to an integer and calls `delete_book(book_id=12)`. The `@router.delete` decorator means this function handles DELETE requests for that path.

## 5. The route asks SQLite to delete one row

The route opens a database connection and executes a parameterized SQL statement:

```python
connection = get_connection()
cursor = connection.execute(
    "DELETE FROM books WHERE id = ?",
    (book_id,)
)
```

`WHERE id = ?` limits the deletion to the row with the requested ID. The question mark is a placeholder; `(book_id,)` supplies its value safely. Without the `WHERE` condition, a `DELETE` could remove every row in the table.

The cursor reports how many rows were affected. If no row matched, the API returns a 404 response. Otherwise, it commits the change so it is saved in the database, closes the connection, and returns JSON:

```python
if cursor.rowcount == 0:
    connection.close()
    raise HTTPException(status_code=404, detail="Book not found")

connection.commit()
connection.close()

return {"id": book_id, "message": "Book deleted successfully"}
```

For a successful deletion, FastAPI serializes the returned dictionary as a JSON response with status `200 OK`:

```json
{
  "id": 12,
  "message": "Book deleted successfully"
}
```

If the ID does not exist, FastAPI sends status `404 Not Found` and an error body similar to:

```json
{"detail": "Book not found"}
```

## 6. JavaScript handles the response

After parsing the response, JavaScript checks `response.ok`. A status outside the successful range becomes an error message displayed on the page:

```javascript
if (!response.ok) {
    const message = typeof data.detail === "string"
        ? data.detail
        : `Request failed (${response.status}).`;
    throw new Error(message);
}
```

For success, the DELETE branch removes the matching book item from the page, reduces the displayed count, and shows an empty-state message if no books remain. It also clears the selected book and reports success. The database change happens on the server; removing the list item updates the current page without requiring a full reload.

## 30-minute lesson plan

| Time | Student activity |
| --- | --- |
| 0–4 min | Ask: what information must the server receive to delete exactly one book? Establish that it needs the book ID. |
| 4–9 min | Trace `data-book-id`, `selectedBook`, and the delegated click handler. Have the student predict which branch runs when `data-action` is `delete`. |
| 9–14 min | Read the `fetch` call. Identify the method, URL, path ID, and why there is no request body. Write the example request `DELETE /delete-book/12`. |
| 14–20 min | Trace the FastAPI decorator, path parameter, SQL `WHERE` clause, row count, commit, and 404 case. Ask what would happen if the `WHERE` clause were missing. |
| 20–25 min | Follow the response back to JavaScript: `response.ok`, JSON, removing the row, updating the count, and showing success or error. |
| 25–30 min | Student implements the endpoint and client call from a small checklist below, then explains the whole trip in their own words. |

## Student implementation checklist

Try implementing this flow in a small practice route or another resource before copying the existing code. Check that your solution:

1. Gives each rendered item a unique ID the browser can read.
2. Sends a DELETE request to a URL containing that ID when the delete action is clicked.
3. Defines a FastAPI DELETE route with a typed path parameter.
4. Executes a parameterized SQL `DELETE` with a `WHERE` condition.
5. Returns 404 when no row was deleted; otherwise commits and returns a useful response.
6. Checks the HTTP response in JavaScript and updates the page only after success.

### Questions to check understanding

- Why does the request put the book ID in the URL?
- Why is `DELETE FROM books WHERE id = ?` safer and more precise than deleting without a condition?
- What does `cursor.rowcount == 0` tell the route?
- What is the difference between deleting the database row and removing its HTML element?
- If the server returns 404, should JavaScript remove the item from the page? Why?
