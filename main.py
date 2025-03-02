from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, get_db, Base
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Add any cleanup code here if needed


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/books/")
async def read_books(db: AsyncSession = Depends(get_db)):
    return {"books": "books"}


@app.get("/books/{book_id}")
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return {"book_id": book_id}
