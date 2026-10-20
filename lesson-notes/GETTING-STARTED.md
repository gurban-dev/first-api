A framework is a collection of reusable tools that provide a structure for building software.

A backend framework helps you build the server-side of an application. This includes HTTP request handling, HTTP responses, data processing and validation. FastAPI is an example of a backend framework.

An API or Application Programming Interface is a defined way for one piece of software to communicate with another. A web API lets a client send requests to a server and receive data in return. Think of this as the intermediary between the client and the server.

An endpoint is a specific URL or web address where an API can be accessed by a client to retrieve data or perform a specific action.

A client is a program that sends a request to another program to obtain information or perform an action. A web browser, mobile app or even another backend service can be a client.

A server is a program that receives requests, processes them and sends back responses. In this project, the server is a Python application running FastAPI.

A virtual environment is an isolated environment for a Python project that keeps its installed packages separate from other Python projects. This prevents dependency conflicts.

Windows PowerShell

Create a virtual environment folder:

python -m venv .first-api-venv

.venv will be the name of the virtual environment folder.

Activate the virtual environment:

.first-api-venv\Scripts\Activate.ps1

You always want to first activate your virtual environment before you install dependencies for your Python project.

Install FastAPI:

pip install "fastapi[standard]"

To verify that FastAPI has been downloaded, you can run the following command:

fastapi --version

A requirements.txt is a plain-text file used in Python projects to list all of the external dependencies required for a project to run.

To populate the requirements.txt file with all of the external dependencies installed in your virtual environment:

pip freeze > requirements.txt

This makes reproducing a project convenient since only one command is required to install of the dependencies:

pip install -r requirements.txt

If the requirements.txt file is empty, running the above command will not install anything since there aren't any dependencies listed in this file.

To start the local development server:

fastapi dev main.py