from pydantic import (
    BaseModel,
    field_validator,
    ValidationError,
)
from typing import Optional


class Book(BaseModel):
    slug: str
    title: str
    author: str
    isbn: str
    year: int
    genre: Optional[str] = None

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, isbn: str) -> str:
        digits = isbn.replace("-", "")
        if len(digits) != 13 or not digits.isdigit():
            raise ValueError("ISBN должен содержать ровно 13 цифр (с дефисами или без)")
        return isbn

    @field_validator("year")
    @classmethod
    def validate_year(cls, year: int) -> int:
        if not (1800 <= year <= 2026):
            raise ValueError("Год издания должен быть в диапазоне 1800-2026")
        return year


class BookCreate(Book):
    pass


if __name__ == "__main__":
    try:
        book = BookCreate(
            slug="master-i-margarita-bulgakov",
            title="Мастер и Маргарита",
            author="М.А. Булгаков",
            isbn="978-5-17-090000-3",
            year=1967,
            genre="Роман",
        )
        print("Валидация прошла:", book)
    except ValidationError as e:
        print("Ошибка валидации:", e)

    print("---")

    try:
        bad_book = BookCreate(
            slug="bad-book",
            title="Плохая книга",
            author="Автор",
            isbn="123",
            year=1750,
        )
    except ValidationError as e:
        print("Ошибка валидации:", e)
