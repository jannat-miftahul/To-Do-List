# To-Do List API

A simple To-Do List app for managing to-do items and creating users. The project is built with FastAPI, SQLAlchemy, Pydantic, and SQLite.

## Features

- Create, read, update, and delete to-do items
- Create users with bcrypt-hashed passwords
- Request validation with Pydantic
- Automatic SQLite database setup
- Interactive API documentation with FastAPI

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Open `http://127.0.0.1:8000/docs` to use the interactive Swagger documentation.

## Endpoints

| Method | Endpoint            | Description    |
| ------ | ------------------- | -------------- |
| GET    | `/`                 | Get all to-dos |
| GET    | `/todo/{todo_id}`   | Get one to-do  |
| POST   | `/create/`          | Create a to-do |
| PUT    | `/edit/{todo_id}`   | Update a to-do |
| DELETE | `/delete/{todo_id}` | Delete a to-do |
| POST   | `/create-user/`     | Create a user  |

### Create a to-do

Example request body:

```json
{
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Build a small API",
    "priority": 3,
    "completed": false
}
```

Priority must be between 1 and 5, and the description can contain up to 100 characters.

## Database

The application uses SQLite and creates `todolistapp.db` in the project directory. This local database is ignored by Git. The tables are created automatically when the application starts.
