import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

def test_add_new_book(collector):
    # добавляем новую книгу
    collector.add_new_book("Война и мир")
    assert collector.books_genre == {"Война и мир": ""}
    # добавляем книгу с длиной 40 символов
    name = "a" * 40
    collector.add_new_book(name)
    assert name in collector.books_genre
    # добавление книги с именем больше 40 символов
    name_long = "a" * 41
    collector.add_new_book(name_long)
    assert name_long not in collector.books_genre
    # добавление книги, уже существующей
    collector.add_new_book("Война и мир")
    # книга не должна повторяться
    assert list(collector.books_genre.keys()).count("Война и мир") == 1

@pytest.mark.parametrize("name, genre", [
    ("Книга1", "Фантастика"),
    ("Книга2", "Ужасы"),
    ("Книга3", "Детективы"),
])
def test_set_book_genre_and_get_book_genre(collector, name, genre):
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == genre

def test_set_book_genre_invalid(collector):
    # жанр не в списке
    collector.add_new_book("Некоторая книга")
    result = collector.set_book_genre("Некоторая книга", "Некорректный жанр")
    # жанр не изменит значение
    assert collector.get_book_genre("Некоторая книга") == ''

def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Книга1")
    collector.set_book_genre("Книга1", "Фантастика")
    collector.add_new_book("Книга2")
    collector.set_book_genre("Книга2", "Ужасы")
    result = collector.get_books_with_specific_genre("Фантастика")
    assert result == ["Книга1"]
    result = collector.get_books_with_specific_genre("Ужасы")
    assert result == ["Книга2"]
    # жанр, которого нет
    result = collector.get_books_with_specific_genre("Детективы")
    assert result == []

def test_get_books_for_children(collector):
    # добавим книги с разными жанрами
    collector.add_new_book("Детская книга")
    collector.set_book_genre("Детская книга", "Мультфильмы")
    collector.add_new_book("Взрослая книга")
    collector.set_book_genre("Взрослая книга", "Ужасы")
    collector.add_new_book("Поп-культура")
    collector.set_book_genre("Поп-культура", "Комедии")
    result = collector.get_books_for_children()
    # книга с жанром "Мультфильмы" подходит, "Ужасы" и "Комедии" тоже
    assert "Детская книга" in result
    # книги с возрастным рейтингом не должны в списке
    assert "Взрослая книга" not in result
    assert "Поп-культура" not in result

def test_add_and_delete_book_in_favorites(collector):
    collector.add_new_book("Книга для избранных")
    collector.set_book_genre("Книга для избранных", "Фантастика")
    # добавить в избранное
    collector.add_book_in_favorites("Книга для избранных")
    assert "Книга для избранных" in collector.favorites
    # повторно добавлять нельзя
    collector.add_book_in_favorites("Книга для избранных")
    assert collector.favorites.count("Книга для избранных") == 1
    # удаляем из избранных
    collector.delete_book_from_favorites("Книга для избранных")
    assert "Книга для избранных" not in collector.favorites
    # удаление несуществующей книга — не должно вызвать ошибку
    collector.delete_book_from_favorites("Некое название")

def test_get_list_of_favorites_books(collector):
    collector.add_new_book("Книга1")
    collector.set_book_genre("Книга1", "Фантастика")
    collector.add_book_in_favorites("Книга1")
    collector.add_new_book("Книга2")
    collector.set_book_genre("Книга2", "Ужасы")
    collector.add_book_in_favorites("Книга2")
    favs = collector.get_list_of_favorites_books()
    assert set(favs) == {"Книга1", "Книга2"}

def test_get_books_genre_returns_dict(collector):
    collector.add_new_book("Книга А")
    collector.set_book_genre("Книга А", "Фантастика")
    genre_dict = collector.get_books_genre()
    assert isinstance(genre_dict, dict)
    assert genre_dict["Книга А"] == "Фантастика"

def test_edge_cases():
    c = BooksCollector()
    # добавить книгу с пустым именем
    c.add_new_book("")
    assert "" not in c.books_genre
    # добавить книгу с именем длиной 40 символов
    name = "a" * 40
    c.add_new_book(name)
    assert name in c.books_genre
    # установить жанр для ненарокпосованной книги
    c.set_book_genre("Несуществующая книга", "Фантастика")
    # получить жанр несуществующей книги
    assert c.get_book_genre("Несуществующая книга") is None
    