from typing import Literal


class ClassTest:
    def instance_method(self):
        print(f"Called instance_method of {self}")

    @classmethod
    def class_method(cls):
        print(f"Called class of {cls}")

    @staticmethod
    def static_method():
        print(f"Called static method")


class Book:
    def __init__(
            self,
            name: str,
            book_type: Literal["hardcover", "paperback"],
            weight: int
    ) -> None:
        self.name = name
        self.book_type = book_type
        self.weight = weight

    def __repr__(self) -> str:
        return f"<Book {self.name}, {self.book_type}, weighing {self.weight}g>"

    @classmethod
    def hardcover(cls, name: str, page_weight: int) -> "Book":
        return cls(name, "hardcover", page_weight + 100)

    @classmethod
    def paperback(cls, name: str, page_weight: int) -> "Book":
        return cls(name, "paperback", page_weight)


hardcover = Book.hardcover("Hard", 10)
print(hardcover)
