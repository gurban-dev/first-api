const bookList = document.getElementById("book-list");
const replacePanel = document.getElementById("replace-panel");
const patchPanel = document.getElementById("patch-panel");
const replaceBookForm = document.getElementById("replace-book-form");
const patchBookForm = document.getElementById("patch-book-form");
const replaceTitleInput = document.getElementById("replace-title");
const replaceAuthorInput = document.getElementById("replace-author");
const patchField = document.getElementById("patch-field");
const patchValueLabel = document.getElementById("patch-value-label");
const patchValue = document.getElementById("patch-value");
const updateStatus = document.getElementById("update-status");
let selectedBook = null;

function hideEditPanels() {
    replacePanel.hidden = true;
    patchPanel.hidden = true;
}

function selectBook(button) {
    selectedBook = {
        id: Number(button.dataset.bookId),
        title: button.dataset.title,
        author: button.dataset.author
    };

    document.querySelectorAll(".book-actions").forEach((actions) => {
        actions.hidden = actions.parentElement !== button.closest(".book-item");
    });

    hideEditPanels();
    updateStatus.textContent = `Selected "${selectedBook.title}".`;
}

bookList.addEventListener("click", (event) => {
    const bookButton = event.target.closest("button[data-book-id]");

    if (bookButton) {
        selectBook(bookButton);
        return;
    }

    const actionButton = event.target.closest("button[data-action]");

    if (!actionButton || !selectedBook) {
        return;
    }

    hideEditPanels();

    if (actionButton.dataset.action === "put") {
        document.getElementById("put-selected-book").textContent =
            `Selected: ${selectedBook.title} (ID: ${selectedBook.id})`;
        replaceTitleInput.value = selectedBook.title;
        replaceAuthorInput.value = selectedBook.author;
        replacePanel.hidden = false;
    } else if (actionButton.dataset.action === "patch") {
        document.getElementById("patch-selected-book").textContent =
            `Selected: ${selectedBook.title} (ID: ${selectedBook.id})`;
        patchField.value = "title";
        updatePatchField();
        patchPanel.hidden = false;
    } else {
        sendUpdate("DELETE", null);
    }
});
function updatePatchField() {
    const field = patchField.value;
    const fieldLabel = field === "title" ? "title" : "author";

    patchValueLabel.textContent = `New ${fieldLabel}`;
    patchValue.maxLength = field === "title" ? 200 : 120;
    patchValue.value = "";
    patchValue.placeholder = `Enter a new ${fieldLabel}`;
}

patchField.addEventListener("change", updatePatchField);

async function sendUpdate(method, body) {
    if (!selectedBook) {
        updateStatus.textContent = "Select a book first.";
        return;
    }

    const endpoint = method === "PUT"
        ? "replace-book"
        : method === "PATCH"
            ? "update-book"
            : "delete-book";

    try {
        const options = { method };
        if (body !== null) {
            options.headers = { "Content-Type": "application/json" };
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`/${endpoint}/${selectedBook.id}`, options);
        const data = await response.json();

        if (!response.ok) {
            const message = typeof data.detail === "string"
                ? data.detail
                : `Request failed (${response.status}).`;
            throw new Error(message);
        }

        const bookButton = document.querySelector(
            `button[data-book-id="${selectedBook.id}"]`
        );

        if (method === "DELETE") {
            bookButton.closest(".book-item").remove();
            const bookCount = document.getElementById("book-count");
            const newCount = Number(bookCount.dataset.count) - 1;
            bookCount.dataset.count = newCount;
            bookCount.textContent = newCount === 0
                ? "There are no books in your collection yet."
                : `${newCount} book${newCount === 1 ? "" : "s"} in your collection.`;

            if (newCount === 0) {
                const emptyMessage = document.createElement("li");
                emptyMessage.id = "empty-books-message";
                emptyMessage.textContent = "There are no books in your collection yet.";
                bookList.append(emptyMessage);
            }

            selectedBook = null;
            hideEditPanels();
            updateStatus.textContent = "Book deleted successfully.";
            return;
        }

        selectedBook = data;
        bookButton.dataset.title = data.title;
        bookButton.dataset.author = data.author;
        bookButton.querySelector(".book-list-title").textContent = data.title;
        bookButton.querySelector(".book-list-author").textContent = data.author;
        replaceTitleInput.value = data.title;
        replaceAuthorInput.value = data.author;
        updateStatus.textContent = `Book ${method} request succeeded.`;
    } catch (error) {
        updateStatus.textContent = error.message;
    }
}

replaceBookForm.addEventListener("submit", (event) => {
    event.preventDefault();

    sendUpdate("PUT", {
        title: replaceTitleInput.value.trim(),
        author: replaceAuthorInput.value.trim()
    });
});

patchBookForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const value = patchValue.value.trim();
    if (!value) {
        updateStatus.textContent = "Enter a new value for the selected field.";
        return;
    }

    sendUpdate("PATCH", { [patchField.value]: value });
});

