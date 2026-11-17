from pathlib import Path

from fastapi import APIRouter, Request

# See lesson-notes/jinja2.md.
from fastapi.templating import Jinja2Templates

# This is for HTML page endpoints.

# - Is there a better way to do this?
BASE_DIR = Path(__file__).resolve().parent.parent.parent

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


@router.get("/get-books", include_in_schema=False)
def books_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="books.html",
        context={}
    )


# Register a GET endpoint at /add-book to display the book
# creation form.

# Exclude this endpoint from /docs because it serves an HTML
# page for users, not an API operation intended for API consumers.
@router.get("/add-book", include_in_schema=False)
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
