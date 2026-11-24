Understand the difference between PUT and PATCH

Imagine your database contains this book:
{
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin"
}


The user wants to change only the author.

With PUT, your current implementation expects both fields:
{
    "title": "Clean Code",
    "author": "Robert Martin"
}


With PATCH, the user can send only the field they want to change:
{
    "author": "Robert Martin"
}


The distinction:
PUT	Replaces the resource by supplying all fields.
PATCH	Modifies only the supplied fields.


How to Implement a PATCH Request

1. Create a Pydantic model for partial updates

A Pydantic model is a Python class that defines the rules for valid data and checks whether the data follows those rules.

For instance, the BookCreate Pydantic model checks whether the title field contains at least 1 character and not more than 200 characters.

class BookCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)


For a PATCH request, we'll create another model in schemas.py:

class BookUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, max_length=200)
    author: str | None = Field(default=None, max_length=120)

How do you think the BookUpdate Pydantic model differs from BookCreate?

The difference is that both the title and author fields are optional because of the keyword argument default=None.

str | None is a Python type annotation that Pydantic reads to determine which types of values the field is allowed to accept.

| None is necessary because we want the field to be able to hold None when the user does not provide a value.

Python itself does not enforce this annotation at runtime. Pydantic uses it to perform runtime validation.

For instance, suppose the user types the book title 1984. Pydantic will attempt to convert 1984 into a string, resulting in "1984".

If a dictionary such as `{"title": "1984"}` is passed as the value of the `title` field somewhere in the source code, Pydantic raises a `ValidationError` because it does not accept a dictionary where a string is expected.

```python
book = BookUpdate(title={"title": "1984"})
```

This allows the client to send:
{
    "title": "Animal Farm"
}

Or:

{
    "author": "J. K. Rowling"
}


# Implementing a PATCH Request

## 1. Frontend (JavaScript): Send the PATCH Request

Suppose the user wants to change the title of a book.

```javascript
async function updateBook() {
    await fetch("/books/1", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: "The Pragmatic Programmer"
        })
    });
}
```

There are four important things to understand:

| Code | Purpose |
|---|---|
| `fetch()` | Sends an HTTP request from the frontend to the backend. |
| `method: "PATCH"` | Specifies that we want to partially update a resource. |
| `headers` | Tells the backend that the request body contains JSON. |
| `JSON.stringify()` | Converts a JavaScript object into a JSON string. |

The request sends the following information:

- **URL:** `/books/1`
- **HTTP method:** `PATCH`
- **Request body:** `{"title": "The Pragmatic Programmer"}`

Notice that we aren't sending the author because we don't want to change it.

---

## 2. Backend (FastAPI/Python): Receive the PATCH Request

FastAPI is the backend web framework.

Python is the programming language used to implement the API endpoint.

In `books.py`:

```python
@router.patch("/books/{book_id}")
def update_book(book_id: int, book: dict):
    connection = get_connection()

    connection.execute(
        "UPDATE books SET title = ? WHERE id = ?",
        (book["title"], book_id)
    )

    connection.commit()
    connection.close()

    return {"message": "Book updated successfully"}
```

There are several important concepts here:

| Code | Purpose |
|---|---|
| `@router.patch()` | Registers an API endpoint that accepts PATCH requests. |
| `book_id: int` | Extracts the book ID from the URL. |
| `book: dict` | Receives the JSON request body as a Python dictionary. |
| `get_connection()` | Establishes a connection to SQLite. |
| `connection.execute()` | Executes the SQL statement. |
| `connection.commit()` | Saves the database changes. |
| `connection.close()` | Closes the database connection. |

---

## 3. Database (SQLite): Update the Database

SQLite is a relational database management system (RDBMS).

SQL is not a programming language.

SQL is a database or query language used to communicate with relational databases.

sqlite3 is a Python module that allows Python programs to communicate with SQLite databases.

This is the actual SQL statement:

```sql
UPDATE books
SET title = ?
WHERE id = ?
```

Python supplies the values through sqlite3:

connection.execute(
    "UPDATE books SET title = ? WHERE id = ?",
    ("1984", 1)
)

If the user sends the example request, SQLite effectively executes:

```sql
UPDATE books
SET title = 'The Pragmatic Programmer'
WHERE id = 1;
```

The existing author remains unchanged.

---

## 4. The PATCH Request Lifecycle

Understanding the sequence of events is essential.

### Step 1: JavaScript

```javascript
fetch("/books/1", {...})
```

Sends the PATCH request containing the new title.

### Step 2: FastAPI

```python
update_book(book_id, book)
```

Receives the book ID and the submitted data.

### Step 3: SQLite

```sql
UPDATE books SET title = ? WHERE id = ?
```

Updates the matching database record.

### Step 4: FastAPI returns a response

```python
return {"message": "Book updated successfully"}
```

Sends an HTTP response back to the client.

### Step 5: JavaScript receives the response

The frontend can use the response to display a success message or refresh the interface.

**The overall process:**

JavaScript -> FastAPI -> SQLite -> FastAPI -> JavaScript