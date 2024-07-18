import json
import os
from typing import List, Dict, Any

FILE_NAME = "library.json"


class Book:
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: str,
        status: str = "в наличии",
    ) -> None:
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Book":
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    def __init__(self, filename: str = FILE_NAME) -> None:
        self.filename = filename
        self.books = self.load_data()

    def load_data(self) -> List[Book]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
            except json.JSONDecodeError:
                return []

    def save_data(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def generate_id(self) -> int:
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1

    def add_book(self, title: str, author: str, year: str) -> None:
        for book in self.books:
            if book.title == title and book.author == author and book.year == year:
                print(f"Книга '{title}' уже существует в библиотеке.")
                return
        new_book = Book(
            book_id=self.generate_id(), title=title, author=author, year=year
        )
        self.books.append(new_book)
        self.save_data()
        print(f"Книга '{title}' добавлена с ID {new_book.id}.")

    def delete_book(self, book_id: int) -> None:
        if any(book.id == book_id for book in self.books):
            self.books = [book for book in self.books if book.id != book_id]
            self.save_data()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, search_by: str, search_value: str) -> List[Book]:
        results = [
            book
            for book in self.books
            if str(getattr(book, search_by)).lower() == str(search_value).lower()
        ]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print(f"Книги по запросу {search_by} = '{search_value}' не найдены.")
        return results

    def display_books(self) -> None:
        if self.books:
            for book in self.books:
                print(book.to_dict())
        else:
            print("Библиотека пуста.")

    def update_status(self, book_id: int, status: str) -> None:
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_data()
                print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")


def main() -> None:
    library = Library()
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "3":
            search_by = input("Искать по (title/author/year): ").lower()
            if search_by in ["title", "author", "year"]:
                search_value = input(f"Введите значение для поиска по {search_by}: ")
                library.find_books(search_by, search_value)
            else:
                print("Некорректный параметр поиска.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
                status = input("Введите новый статус (в наличии/выдана): ").lower()
                if status in ["в наличии", "выдана"]:
                    library.update_status(book_id, status)
                else:
                    print("Некорректный статус.")
            except ValueError:
                print("Некорректный ID.")
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
