# FastAPI Learning Projects

A collection of FastAPI examples covering basic routing, request validation, CRUD operations, authentication, SQLAlchemy, Alembic migrations, templates, and a Todo application.

## Projects

- **books.py** demonstrates routes, path and query parameters, and in-memory CRUD operations.
- **books_advanced.py** adds Pydantic models, validation, status codes, and HTTP exceptions.
- **todo_app/** contains a larger Todo application with routers, database models, authentication, templates, and static assets.

## Requirements

- Python 3.10 or newer
- Dependencies listed in **requiremnts.txt**

## Setup

Create and activate a virtual environment, then install the dependencies:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requiremnts.txt

## Run the examples

Run the basic books API:

    uvicorn books:app --reload

Run the validated books API:

    uvicorn books_advanced:app --reload

Run the Todo application:

    uvicorn todo_app.main:app --reload

Open http://127.0.0.1:8000/docs for the interactive Swagger API documentation.

## Database migrations

The repository includes Alembic configuration for database schema migrations. Review the configured database URL before running migrations:

    alembic upgrade head

## Notes

The book examples keep data in memory, so changes reset when the server restarts. The Todo application demonstrates persistent storage and authentication concepts and should be configured with appropriate secrets before production use.
