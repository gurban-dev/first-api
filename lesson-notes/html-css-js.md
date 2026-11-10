# HTML, CSS, and JavaScript

## 1. HTML is a Markup Language

HTML (HyperText Markup Language) is **not a programming language**. It is a markup language used to define the structure and content of a web page.

HTML uses elements (also called tags) to describe different parts of a web page, such as:

- Headings.
- Paragraphs.
- Images.
- Links.
- Forms.
- Buttons.
- Input fields.

Unlike programming languages, HTML does not provide programming logic such as loops, conditional statements, or functions.

## 2. The Relationship Between HTML, CSS, and JavaScript

HTML, CSS, and JavaScript work together to create interactive web pages. Each has a different responsibility.

### HTML: Structure and Content

HTML defines the structure and content of a web page.

For example, HTML determines whether a page contains a heading, paragraph, form, or button.

### CSS: Appearance and Styling

CSS (Cascading Style Sheets) controls how HTML elements look.

It allows us to specify:

- Colors.
- Fonts and text sizes.
- Backgrounds.
- Spacing and positioning.
- Borders.
- Element dimensions.

### JavaScript: Behavior and Interactivity

JavaScript allows us to add behavior and interactivity to a web page.

For example, JavaScript can:

- Respond to button clicks.
- Validate information entered into forms.
- Display messages to users.
- Send HTTP requests to a backend.
- Update the content of a web page.

**In simple terms:**

- HTML defines what appears on the page.
- CSS defines how it looks.
- JavaScript defines how it behaves.

## 3. The `<form>` Element

The `<form>` element is used to create a form that allows users to enter and submit information.

Forms are commonly used when collecting information from users, such as:

- Registration details.
- Login credentials.
- Contact information.
- Book titles and authors.
- Search queries.

Example:

```html
<form id="book-form">
    <label for="title">Book title</label>

    <input
        type="text"
        id="title"
        name="title"
        required
    >

    <button type="submit">Add book</button>
</form>
```

When a user submits a form, the browser triggers a `submit` event.

JavaScript can listen for this event using `addEventListener()` and handle the submission.

For example:

```javascript
const bookForm = document.getElementById("book-form");

bookForm.addEventListener("submit", (event) => {
    event.preventDefault();

    console.log("Form submitted!");
});
```

Here, `event.preventDefault()` prevents the browser's default form submission behavior, allowing JavaScript to handle the submission instead.

## 4. The `<label>` Element

The `<label>` element provides a descriptive caption for an input field or another form control.

It helps users understand what information they are expected to enter.

For example:

```html
<label for="title">Book title</label>

<input type="text" id="title">
```

In this example, "Book title" is the label describing the input field.

Labels also improve accessibility because assistive technologies, such as screen readers, can use them to identify form controls.

Additionally, clicking a label associated with an input field moves focus to that input field.

## 5. The `for` Attribute

The `for` attribute is used with a `<label>` element to associate the label with a particular form control.

Its value must match the `id` of the input element it describes.

For example:

```html
<label for="author">Author</label>

<input type="text" id="author">
```

Notice that:

- The label has `for="author"`.
- The input has `id="author"`.

Because these values match, the browser knows that the label belongs to that input field.

**Important:** The `for` attribute on a label is not the same as the `name` attribute on an input.

- `for` connects a label to a form control.
- `id` uniquely identifies an HTML element within the document.
- `name` identifies a form field when its data is submitted.

Always associate labels with their corresponding input fields whenever possible.