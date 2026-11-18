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
HTTP method	Purpose
PUT	Replace the resource by supplying all fields.
PATCH	Modify only the supplied fields.


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

The important difference is that both the title and author fields are optional because of the keyword argument default=None.

| None is necessary because we want the field to be able to hold None when the user does not provide a value.

This allows the client to send:
{
    "title": "The Pragmatic Programmer"
}

Or:

{
    "author": "Andrew Hunt"
}