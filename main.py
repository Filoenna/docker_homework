from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/books/")
async def read_books():
    return {"books": "books"}


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_id": book_id}
