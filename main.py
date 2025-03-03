from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db, Base
from models import Book as BookModel
from contextlib import asynccontextmanager
from fastapi import HTTPException, status
from schemas import BookCreate, Book


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
    result = await db.execute(select(BookModel))
    books = result.scalars().all()
    return books


@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
