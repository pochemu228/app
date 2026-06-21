from fastapi import (
    FastAPI,
    HTTPException,
    Query,
)
from typing import (
    List,
    Dict,
    Optional,
)
from models import (
    Book,
    BookCreate,
)
import uvicorn

app = FastAPI(
    title="API Каталога библиотеки",
    description="API для управления каталогом книг библиотеки.",
    tags=[
        "Books",
    ],
)


books_db: Dict[str, Book] = {
    "prestuplenie-i-nakazanie-dostoevsky": Book(
        slug="prestuplenie-i-nakazanie-dostoevsky",
        title="Преступление и наказание",
        author="Ф.М. Достоевский",
        isbn="978-5-17-010001-5",
        year=1866,
        genre="Роман",
    ),
    "mertvye-dushi-gogol": Book(
        slug="mertvye-dushi-gogol",
        title="Мёртвые души",
        author="Н.В. Гоголь",
        isbn="978-5-04-010002-9",
        year=1842,
        genre="Поэма",
    ),
}


@app.get(
    "/books/",
    response_model=List[Book],
)
def get_books():
    all_books = list(books_db.values())
    return all_books



@app.get(
    "/books/filter/",
    response_model=List[Book],
)
def filter_books(
        author: Optional[str] = Query(None),
        genre: Optional[str] = Query(None),
):
    filtered = []
    for book in books_db.values():
        if author and author.lower() not in book.author.lower():
            continue
        if genre and genre.lower() not in book.genre.lower():
            continue
        filtered.append(book)
    return filtered


@app.get(
    "/books/{slug}",
    response_model=Book,
)
def get_book_by_slug(
        slug: str,
):
    if slug not in books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return books_db[slug]


@app.post(
    "/books/",
    response_model=Book,
    status_code=201,
)
def create_book(
        book_in: BookCreate,
):
    # 1. Проверка уникальности slug
    if book_in.slug in books_db:
        raise HTTPException(status_code=400, detail="Slug уже существует")

    # 2. Проверка уникальности ISBN
    for existing in books_db.values():
        if existing.isbn == book_in.isbn:
            raise HTTPException(status_code=400, detail="ISBN уже существует")


    new_book = Book(**book_in.model_dump())

    books_db[new_book.slug] = new_book
    return new_book


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
