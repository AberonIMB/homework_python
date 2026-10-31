books_by_id = {}
issued_books = set()
journal = []


def add_book(book_id: int, book_name: str, author: str, year: int) -> None:
    if book_id in books_by_id:
        raise ValueError(f"Книга id={book_id} уже существует")

    books_by_id[book_id] = (book_id, book_name, author, year)
    journal.append((book_id, "added"))


def delete_book(book_id: int) -> None:
    if book_id not in books_by_id:
        raise ValueError(f"Книга id={book_id} не существует")

    if book_id in issued_books:
        raise ValueError(f"Невозможно удалить книгу id={book_id}, т.к. она выдана")

    books_by_id.pop(book_id)
    journal.append((book_id, "deleted"))


def get_book(book_id: int) -> tuple | None:
    return books_by_id.get(book_id)


def issue_book(book_id: int) -> None:
    if book_id not in books_by_id:
        raise ValueError(f"Книга id={book_id} не существует")

    if book_id in issued_books:
        raise ValueError(f"Книга id={book_id} уже выдана")

    issued_books.add(book_id)
    journal.append((book_id, "issued"))


def return_book(book_id: int) -> None:
    if book_id not in issued_books:
        raise ValueError(f"Книга id={book_id} не выдана")

    issued_books.remove(book_id)
    journal.append((book_id, "returned"))


def books() -> list:
    return list(books_by_id.values())

def history() -> list:
    return journal.copy()

if __name__ == "__main__":
    add_book(1, "Мастер и Маргарита", "Михаил Булгаков", 1940)
    add_book(2, "Война и мир", "Лев Толстой", 1869)
    add_book(3, "Гарри Поттер и узник Азкабана", "Джоан Роулинг", 1997)

    print(books())

    issue_book(1)
    issue_book(2)
    issue_book(3)

    return_book(1)
    return_book(2)

    print(get_book(3))

    delete_book(1)

    print(history())