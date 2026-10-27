import json

# Importing the class named FastAPI this way we can create a
# FastAPI application.
from fastapi import FastAPI, Response

# This creates an instance/object of the FastAPI class.

# Create the application.
app = FastAPI()

# Register an endpoint.

# @ indicates that that line 17 is a decorator.
# Tells FastAPI to call the say_hello() function when a client sends
# GET request to /hello.

# A GET request is sent to retrieve information.
@app.get("/hello")
def say_hello():
    return {"message": "Hello, world!"}

# The say_hello() function contains the logic for the endpoint.

# The {name} part if a path parameter, meaning a value supplied
# as part of the URL path.

# If the client visits /greet/john, FastAPI passes "john" to the
# function as name.

@app.get("/greet/{name}")
def greet_person(name: str):
    return {"message": f"Hello, {name.capitalize()}!"}

# The client will send a GET request to the endpoint /square/5,
# and should receive back:
# {"number": 5, "square": 25}

# Implmement a function that handles not only this particular
# example, but any number that is passed as a path parameter.

@app.get("/square/{num}")
def greet_person(num: int):
    # FastAPI extracts num from the URL and converts it to an integer.
    # For example, a request to /square/5 sets num to 5.
    square = num**2

    data = {
        "number": num,
        "square": square
    }

    # Double braces {{ and }} produce literal braces in an f-string.
    # The resulting string must follow JSON syntax.
    dict_in_f_str = f'{{"number": {num}, "square": {square}}}'

    return Response(
        # json.dumps() converts a Python object into a JSON-formatted
        # string. It can serialize the dictionary directly.
        # content=json.dumps(data, indent=2),

        # Return the manually constructed JSON string instead.
        # This works here, but json.dumps() is safer for general data
        # because it correctly escapes strings and other special values.
        content=dict_in_f_str,

        # Tell the client that the response contains JSON.
        media_type="application/json"
    )