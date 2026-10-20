# Importing the class named FastAPI this way we can create a
# FastAPI application.
from fastapi import FastAPI

# This creates an object of the FastAPI class.

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

@app.get("/greet/{name}")
def greet_person(name: str):
    return {"message": f"Hello, {name}!"}