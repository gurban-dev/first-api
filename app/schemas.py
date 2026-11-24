# ConfigDict changes how a Pydantic model processes data as seen
# with ConfigDict(str_strip_whitespace=True) below.

# Field defines validation rules for model fields as seen below
# with Field(min_length=1, max_length=200).
from pydantic import BaseModel, ConfigDict, Field


# FastAPI needs a way to validate the JSON data received from
# the client.

# The BookCreate class is inheriting from BaseModel.

# Without BaseModel, a standard Python class is not capable of
# identifying invalid data.

# FastAPI converts the JSON text into a Python dictionary, and 
# BaseModel ensures that it matches the predefined structure.

# The predefined structure requires two incoming pieces of data
# to use the exact lowercase keys "title" and "author", and both
# values must be strings.
class BookCreate(BaseModel):
    # ConfigDict(str_strip_whitespace=True) removes leading
    # and trailing spaces from all input strings automatically
    # before validating them.
    model_config = ConfigDict(str_strip_whitespace=True)

    # Ensures fields aren't blank: title allows 1 to 200 characters, 
    # while author allows 1 to 120 characters.
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)


class BookPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=120)
