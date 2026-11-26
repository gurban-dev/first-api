from pathlib import Path

from fastapi import APIRouter, Request

# See lesson-notes/jinja2.md.
from fastapi.templating import Jinja2Templates

from app.database import get_connection

# This is for HTML page endpoints.

# parents[0] is routers/
# parents[1] is app/
# parents[2] is the project's first-api/ directory.
BASE_DIR = Path(__file__).resolve().parents[2]

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

router = APIRouter()


@router.get("/view-books", include_in_schema=False)
def view_books(request: Request):
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

    all_books = []

    for book in books:
        all_books.append(dict(book))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"books": all_books}
    )
