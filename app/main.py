import logging

# closing() guarantees that database connections are closed,
# including when an exception occurs.
from contextlib import asynccontextmanager

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
from fastapi import FastAPI

# StaticFiles serves CSS, JavaScript, images, and other static files.
# "Serving" means delivering these pre-made resources (stylesheets,
# client-side scripts, and media files) directly to the user's browser.

# Client-side scripts almost always mean JavaScript files.
# static/js/app.js in this case.
from fastapi.staticfiles import StaticFiles

from app.database import initialize_database
from app.routers import books, examples, pages

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

BASE_DIR = Path(__file__).resolve().parent.parent

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

app.include_router(books.router)
app.include_router(pages.router)
app.include_router(examples.router)