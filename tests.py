import unittest
import os
import json
from main import Book, Library


class TestLibrary(unittest.TestCase):

    def setUp(self) -> None:
        self.library = Library(filename="test_library.json")
        self.book1 = Book(1, "Test Book 1", "Author 1", "2020")
        self.book2 = Book(2, "Test Book 2", "Author 2", "2021")
        self.library.books = [self.book1, self.book2]
        self.library.save_data()

    def tearDown(self) -> None:
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    def test_load_data(self) -> None:
        books = self.library.load_data()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Test Book 1")
        self.assertEqual(books[1].title, "Test Book 2")

    def test_save_data(self) -> None:
        self.library.save_data()
        with open("test_library.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["title"], "Test Book 1")
            self.assertEqual(data[1]["title"], "Test Book 2")

    def test_generate_id(self) -> None:
        new_id = self.library.generate_id()
        self.assertEqual(new_id, 3)

    def test_add_book(self) -> None:
        self.library.add_book("New Book", "New Author", "2022")
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[-1].title, "New Book")

        self.library.add_book("New Book", "New Author", "2022")
        self.assertEqual(
            len(self.library.books), 3
        )  # Длина списка книг не должна измениться

    def test_delete_book(self) -> None:
        self.library.delete_book(1)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book 2")

        self.library.delete_book(99)
        self.assertEqual(len(self.library.books), 1)

    def test_find_books(self) -> None:
        results = self.library.find_books("title", "Test Book 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book 1")

        results = self.library.find_books("title", "Non-existent Book")
        self.assertEqual(len(results), 0)

    def test_display_books(self) -> None:
        self.library.display_books()
        self.assertEqual(len(self.library.books), 2)

    def test_update_status(self) -> None:

        self.library.update_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        self.library.update_status(99, "в наличии")
        self.assertEqual(len(self.library.books), 2)


if __name__ == "__main__":
    unittest.main()
