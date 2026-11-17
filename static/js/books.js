const bookList = document.getElementById("book-list");
const libraryStatus = document.getElementById("library-status");
const bookDetails = document.getElementById("book-details");
const selectedBookTitle = document.getElementById("selected-book-title");
const selectedBookAuthor = document.getElementById("selected-book-author");
const selectedBookId = document.getElementById("selected-book-id");

function selectBook(book) {
    selectedBookTitle.textContent = book.title;
    selectedBookAuthor.textContent = `by ${book.author}`;
    selectedBookId.textContent = `Book ID: ${book.id}`;
    bookDetails.hidden = false;
}

function displayBooks(books) {
    bookList.replaceChildren();

    if (books.length === 0) {
        libraryStatus.textContent = "There are no books in your collection yet.";
        return;
    }

    libraryStatus.textContent = `${books.length} book${books.length === 1 ? "" : "s"} in your collection.`;

    for (const book of books) {
        const item = document.createElement("li");
        const button = document.createElement("button");
        const title = document.createElement("span");
        const author = document.createElement("span");

        button.type = "button";
        button.className = "book-list-item";
        title.className = "book-list-title";
        author.className = "book-list-author";
        title.textContent = book.title;
        author.textContent = book.author;

        button.append(title, author);
        button.addEventListener("click", () => selectBook(book));
        item.append(button);
        bookList.append(item);
    }
}

async function loadBooks() {
    try {
        const response = await fetch("/api/books");

        if (!response.ok) {
            throw new Error(`The server returned an error (${response.status}).`);
        }

        const books = await response.json();

        if (!Array.isArray(books)) {
            throw new Error("The server returned an unexpected response.");
        }

        displayBooks(books);
    } catch (error) {
        console.error("Error loading books:", error);
        libraryStatus.textContent =
            "Could not load your books. Please try again later.";
    }
}

loadBooks();
