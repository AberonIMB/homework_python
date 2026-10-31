class MyDict:
    def __init__(self, size=8):
        if size <= 0:
            raise ValueError("size должен быть положительным")
        self._buckets = [[] for _ in range(size)]
        self._len = 0


    def __setitem__(self, key, value):
        bucket = self._buckets[self._get_bucket_index(key)]
        for i in range(len(bucket)):
            k, v = bucket[i]
            if k == key:
                bucket[i] = (key, value)
                return

        if self._len + 1 > len(self._buckets) * 2 / 3:
            self._resize()

        bucket = self._buckets[self._get_bucket_index(key)]
        bucket.append((key, value))
        self._len += 1


    def __getitem__(self, key):
        bucket_index = self._get_bucket_index(key)
        for k, v in self._buckets[bucket_index]:
            if k == key:
                return v
        raise KeyError(key)


    def __delitem__(self, key):
        bucket_index = self._get_bucket_index(key)
        bucket = self._buckets[bucket_index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                del bucket[i]
                self._len -= 1
                return

        raise KeyError(key)


    def __contains__(self, key):
        bucket_index = self._get_bucket_index(key)
        for k, v in self._buckets[bucket_index]:
            if k == key:
                return True
        return False


    def __len__(self):
        return self._len


    def get(self, key, default=None):
        bucket_index = self._get_bucket_index(key)
        for k, v in self._buckets[bucket_index]:
            if k == key:
                return v
        return default


    def stats(self):
        max_len = 0
        for bucket in self._buckets:
            if len(bucket) > max_len:
                max_len = len(bucket)

        return (len(self._buckets), self._len, max_len)


    def __repr__(self):
        result = ", ".join(f"{repr(key)}: {repr(value)}" for bucket in self._buckets for key, value in bucket)
        return f"MyDict({{{result}}})"


    def _resize(self):
        new_buckets = [[] for _ in range(len(self._buckets) * 2)]
        for bucket in self._buckets:
            for key, value in bucket:
                bucket_index = self._get_bucket_index(key, len(new_buckets))
                new_buckets[bucket_index].append((key, value))

        self._buckets = new_buckets


    def _get_bucket_index(self, key, buckets_len = None):
        if buckets_len is None:
            buckets_len = len(self._buckets)
        return hash(key) % buckets_len


if __name__ == '__main__':
    from time import perf_counter

    d = MyDict()
    start = perf_counter()
    for i in range(1000):
        d[f'key{i}'] = i
    string_time = perf_counter() - start
    string_stats = d.stats()
    assert len(d) == 1000
    print(f"Строковые ключи: stats={string_stats}, вставка 1000 ключей: {string_time:.6f} с")
    assert d['key42'] == 42
    assert 'key7' in d and 'nope' not in d
    d['key42'] = -1
    assert d['key42'] == -1 and len(d) == 1000
    del d['key42']
    assert 'key42' not in d and len(d) == 999
    assert d.get('nope') is None and d.get('nope', 0) == 0
    for bad in (lambda: d['nope'], lambda: d.__delitem__('nope')):
        try:
            bad()
            assert False, 'ожидали KeyError'
        except KeyError:
            pass
    buckets, size, longest = d.stats()
    assert size == 999 and size <= buckets * 2 / 3
    print(d.stats())

    class CollisionKey:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return 42

        def __eq__(self, other):
            return isinstance(other, CollisionKey) and self.value == other.value

    same_hash = MyDict()
    start = perf_counter()
    for i in range(1000):
        same_hash[CollisionKey(i)] = i
    collision_time = perf_counter() - start
    collision_stats = same_hash.stats()
    assert collision_stats == (2048, 1000, 1000)
    print(f"Одинаковый хеш: stats={collision_stats}, вставка 1000 ключей: {collision_time:.6f} с")

# При увеличении таблицы индексы корзин меняются, потому что вычисляются как hash(key) % число_корзин.
# Поэтому все пары нужно перераспределить, иначе поиск будет проверять не ту корзину.
# Для 1000 строковых ключей stats() показал (2048, 1000, 4), вставка заняла 0.001526 с.
# Для 1000 разных ключей с хешем 42 stats() показал (2048, 1000, 1000), а вставка заняла 0.058392 с.
# Все пары попали в одну корзину.