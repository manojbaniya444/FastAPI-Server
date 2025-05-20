## FastAPI Backend Server

- [Basic HTTP Methods with fastapi concepts](./concepts/basic_request_response.py)
- [Basic CRUD with fastapi](./concepts/books_crud_app.py)
- [Server Start](./src/__init__.py)
- [Manage configurations file for env variables](./src/config.py)

## Async SQL Connection

- [Async SQL with SQL Alchemy and SQL Model](./src/db/main.py)

## Async Redis Connection

- [RedisIO Async Connection aioredis](./src/db/redis.py)

## Books Service

All the logic for getting, updating, deleting and inserting book in our database.

- [BOOK Service](./src/books/service.py)
- [BOOK Model](./src/books/models.py)
- [BOOK Schema](./src/books/schemas.py)
- [API Endpoints for Book Service](./src/books/routes.py)

## Auth Service

- [Auth Service](./src/auth/service.py)
- [Auth Model](./src/auth/models.py)
- [Auth Schema](./src/auth/schemas.py)
- [API Endpoints for Auth Service](./src/auth/routes.py)
- [Role Base Access Control to authrize](./src/auth/dependencies.py)

## Dependency Injection

Dependency Injection in FastAPI allows for the sharing of state among multiple API routes by providing a mechanism to create Python objects, referred to as dependencies, and accessing them only when necessary within dependant method.

- Aysnc Session Dependency
- Auth Dependency
- Role Base Access Control Dependency to check assign role to update, delete, get method

## Database Migration with Alembic (SQLModel, SQL Alchemy)

- [Alembic Setup](./migrations/)

Initialize migration
`alembic init -t async migrations`

Apply Migration here
`alembic revision --autogenerate -m "init"`

Use Migration
`alembic upgrade head`
