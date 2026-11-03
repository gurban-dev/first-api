# FastAPI Development Foundations

## Core Concepts

### Framework
A framework is a collection of reusable tools that provide a structure for building software.

### Backend Framework
A backend framework helps you build the server-side of an application. This includes HTTP request handling, HTTP responses, data processing, and validation. **FastAPI** is an example of a backend framework.

### API (Application Programming Interface)
An API is a defined way for one piece of software to communicate with another. A web API lets a client send requests to a server and receive data in return, acting as the intermediary between the client and the server.

### API Endpoint
An API endpoint is a specific URL or web address where an API receives requests and sends responses.

### Client
A client is a program that sends a request to another program to obtain information or perform an action. A web browser, mobile app, or even another backend service can be a client.

### Server
A server is a program that receives requests, processes them, and sends back responses. In this project, the server is a Python application running FastAPI.

### Virtual Environment
A virtual environment is an isolated environment for a Python project that keeps its installed packages separate from other Python projects. This prevents dependency conflicts.

---

## Environment Setup & Commands (Windows PowerShell)

### 1. Create a Virtual Environment
Create an isolated virtual environment folder named `.first-api-venv`:
```powershell
python -m venv .first-api-venv
```
> **Note:** On Windows, the virtual environment folder will have a `Scripts` subdirectory, whereas on Linux, it will contain a subdirectory called `bin`.

### 2. View Project Directory
View both visible and hidden items to verify the folder structure:
```powershell
Get-ChildItem -Force
```

### 3. Activate the Virtual Environment
Always activate your virtual environment before installing project dependencies:
```powershell
.first-api-venv\Scripts\Activate.ps1
```

### 4. Install FastAPI
Install the framework along with its standard development tools:
```powershell
pip install "fastapi[standard]"
```

### 5. Verify Installation
Verify that FastAPI has been successfully downloaded and check its version:
```powershell
fastapi --version
```

---

## Managing Dependencies

### The requirements.txt File
A `requirements.txt` file is a plain-text file used in Python projects to list all of the external dependencies required for the project to run.

* **Populate the file** with all dependencies currently installed in your active virtual environment:
  ```powershell
  pip freeze > requirements.txt
  ```
* **Reproduce the environment** easily on another system using a single command:
  ```powershell
  pip install -r requirements.txt
  ```
  *(Note: If the `requirements.txt` file is empty, running this command will not install anything since no dependencies are listed).*

---

## Running the Application

### Start the Development Server
Launch the local development server by pointing it to your main Python file:
```powershell
fastapi dev main.py
```

* **Local Development Link:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Port Configuration:** The server listens for incoming HTTP requests on port number **8000**.