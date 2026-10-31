import re
from collections import Counter


class SearchIndex:
    """
    Инвертированный индекс для поиска документов по словам.
    _index хранит для каждого слова множество ID документов, а _documents - слова каждого документа.
    Так можно выполнять поиск по индексным множествам, а при удалении обходить только слова нужного документа.
    Список слов также сохраняет повторы для подсчёта частот в top_words().
    """
    def __init__(self):
        self._index = dict[str, set[int]]()
        self._documents = dict[int, list[str]]()

    def add(self, doc_id: int, text: str):
        words = re.findall(r'\w+', text.lower())
        self.remove(doc_id)
        self._put_words_in_index(words, doc_id)
        self._save_document(doc_id, words)

    def search_all(self, *words: str):
        if not words:
            return set()

        sets = []
        for word in words:
            word = word.lower()
            if word not in self._index:
                return set()
            sets.append(self._index[word])

        return set.intersection(*sets)


    def search_any(self, *words: str):
        result = set()
        for word in words:
            word = word.lower()
            if word in self._index:
                result.update(self._index[word])
        return result


    def top_words(self, n: int):
        count = Counter()
        for words in self._documents.values():
            count.update(words)
        return count.most_common(n)

    def remove(self, doc_id: int):
        if doc_id not in self._documents:
            return

        for word in set(self._documents[doc_id]):
            if word not in self._index:
                continue
            self._index[word].remove(doc_id)
            if not self._index[word]:
                del self._index[word]

        del self._documents[doc_id]


    def _put_words_in_index(self, words: list[str], doc_id: int):
        for word in words:
            if word not in self._index:
                self._index[word] = {doc_id}
            else:
                self._index[word].add(doc_id)


    def _save_document(self, doc_id: int, words: list[str]):
        self._documents[doc_id] = words


if __name__ == '__main__':
    idx = SearchIndex()
    idx.add(1, 'Python is a programming language.')
    idx.add(2, 'A dict is a hash table; a set is a hash table too!')
    idx.add(3, 'Python dict and set are fast.')
    assert idx.search_all('python') == {1, 3}
    assert idx.search_all('dict', 'set') == {2, 3}
    assert idx.search_all('python', 'hash') == set()
    assert idx.search_any('language', 'fast') == {1, 3}
    assert idx.search_all('PYTHON') == {1, 3}
    assert idx.search_all('nothing') == set()
    assert idx.top_words(2) == [('a', 5), ('is', 3)]
    idx.remove(1)
    assert idx.search_all('python') == {3}
    assert idx.search_any('language', 'programming') == set()
    idx.add(3, 'Totally new text')
    assert idx.search_all('python') == set()
    assert idx.search_all('new') == {3}
