## FastAPI Backend Server
Learning to build backend application with fastapi

- [Basic HTTP Methods with fastapi concepts](./concepts/basic_request_response.py)
- [Basic CRUD with fastapi](./concepts/books_crud_app.py)
- [Server Start](./src/__init__.py)

## Async SQL Connection
- [Async SQL with SQL Alchemy and SQL Model](./src/db/main.py)

## Books Service
All the logic for getting, updating, deleting and inserting book in our database.
- [BOOK Service](./src/books/service.py)
- [BOOK Model](./src/books/models.py)
- [BOOK Schema](./src/books/schemas.py)
- [API Endpoints for Book Service](./src/books/routes.py)

## Dependency Injection
Dependency Injection in FastAPI allows for the sharing of state among multiple API routes by providing a mechanism to create Python objects, referred to as dependencies, and accessing them only when necessary within dependant method.

- Aysnc Session Dependency
- Auth Dependency