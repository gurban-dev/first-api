# Project Structure

This overview starts at the `first-api` project directory. The project is a small FastAPI application that stores books in SQLite and serves an HTML form with CSS and JavaScript.

```text
first-api/
├── app/                       # Python application package
│   ├── main.py                # Creates the FastAPI app and connects its routers
│   ├── database.py            # SQLite connection and books table setup
│   ├── schemas.py             # Pydantic models used to validate book data
│   └── routers/               # HTTP endpoints grouped by purpose
│       ├── books.py           # Create a book and retrieve all books
│       ├── pages.py           # Serves the add-book HTML page
│       └── examples.py        # Small API examples: hello, greet, and square
├── templates/
│   └── index.html             # Add-book page template
├── static/
│   ├── css/styles.css         # Page appearance
│   └── js/app.js              # Form behavior and POST request to the API
├── lesson-notes/              # Learning notes and exercises
├── requirements.in            # Top-level dependency input (currently empty)
├── requirements.txt           # Pinned Python packages
└── .gitignore                 # Files and folders Git should ignore
```

## How a book is added

1. The browser displays `templates/index.html`, styled by `static/css/styles.css`.
2. `static/js/app.js` handles the form submission and sends a JSON `POST` request to `/create-book`.
3. The books router validates the request with `BookCreate` from `app/schemas.py`.
4. The router uses functions in `app/database.py` to insert the book into SQLite and returns the created book as JSON.

## How books are retrieved

The books router handles `GET /get-books`. It selects rows from the `books` table and returns them as JSON. A browser page can request that endpoint and use the response to display the books.

## Application startup

`app/main.py` creates the FastAPI application, initializes the database during startup, serves files under `/static`, and includes the books, pages, and examples routers. Start the app from the project directory with:

```bash
uvicorn app.main:app --reload
```

The database and template locations are configured in their respective Python modules. Since those modules are nested under `app/`, keep their paths consistent with the project-root locations shown above when changing how the app is launched or organized.

## Lesson notes

The `lesson-notes/` directory contains topic notes for getting started, HTTP, dependencies, HTML/CSS/JavaScript, Jinja2, logging, Git, and the exercise for retrieving books. These notes provide background for the code in `app/`, `templates/`, and `static/`.
