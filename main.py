# from fastapi import FastAPI

# from src.books.routes import book_router

# version = "v1"

# # Instantiate the FastAPI application here
# app = FastAPI(
#     title="Book API",
#     description="A Backend API for book web app",
#     version=version
# )

# # Include the books_router here
# app.include_router(
#     book_router,
#     prefix=f"/api/{version}/books",
#     tags=["books"]
# )