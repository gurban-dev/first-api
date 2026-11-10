const bookForm = document.getElementById("book-form");
const titleInput = document.getElementById("title");
const authorInput = document.getElementById("author");

const submitButton = document.getElementById("submit-button");
const buttonText = document.getElementById("button-text");
const buttonSpinner = document.getElementById("button-spinner");

const feedback = document.getElementById("feedback");

// This file is where the frontend communicates with the backend.

function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    buttonSpinner.hidden = !isLoading;

    buttonText.textContent = isLoading
        ? "Adding book..."
        : "Add book";
}


function showFeedback(message, type) {
    feedback.textContent = message;
    feedback.className = `feedback ${type}`;
    feedback.hidden = false;
}


function getErrorMessage(data) {
    if (Array.isArray(data.detail)) {
        return data.detail
            .map(error => {
                const field = error.loc?.at(-1) ?? "Field";
                return `${field}: ${error.msg}`;
            })
            .join(". ");
    }

    if (typeof data.detail === "string") {
        return data.detail;
    }

    return "Something went wrong. Please try again.";
}

// addEventListener() allows us to listen for an event that happens
// on an HTML element.

// Examples of what an event could be:
// click: When someone clicks an element.
// submit: When someone submits a form.
// input: When someone changes the contents of an input field.
// mouseover: When someone moves their mouse over an element.

// The async keyword is necessary because it allows us to use await
// inside the function.

// event is a parameter that contains information about the event
// that occurred.
bookForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();
    const author = authorInput.value.trim();

    if (!title || !author) {
        showFeedback(
            "Please enter both the book title and author.",
            "error"
        );
        return;
    }

    setLoading(true);
    feedback.hidden = true;

    // fetch() is a built-in JavaScript function that allows us to
    // communicate with a server by sending HTTP requests and receiving
    // responses.

    // "/create-book" is the URL of the backend endpoint we want to
    // communicate with.

    // await tells JavaScript to wait until the server responds before
    // moving on to the next line of code.

    // The variable 'response' stores the response received from the
    // server.
    try {
        const response = await fetch("/create-book", {
            // A POST request sends information to the server to create
            // a new record in the database.
            method: "POST",
            headers: {
                // Tells the backend that the data we are sending in the
                // request body is formatted as JSON.
                "Content-Type": "application/json"
            },
            // The body property contains the actual information we want
            // to send to the backend.

            // JSON.stringify() is a built-in JavaScript method that
            // converts a JavaScript object into a JSON string.
            body: JSON.stringify({
                title: title,
                author: author
            })
        });

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            throw new Error(
                data ? getErrorMessage(data) :
                `The server returned an error (${response.status}).`
            );
        }

        if (
            !data ||
            !Number.isInteger(data.id) ||
            typeof data.title !== "string" ||
            typeof data.author !== "string"
        ) {
            throw new Error(
                "The server returned an unexpected response."
            );
        }

        showFeedback(
            `Successfully added "${data.title}" by ${data.author}. Book ID: ${data.id}.`,
            "success"
        );

        bookForm.reset();
        titleInput.focus();

    } catch (error) {
        console.error("Error creating book:", error);

        showFeedback(
            error.message === "Failed to fetch"
                ? "Unable to connect to the server. Please check your connection and try again."
                : error.message,
            "error"
        );

    } finally {
        setLoading(false);
    }
});