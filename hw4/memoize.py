def memoize(func):
    cache = dict()

    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))

        try:
            hash(key)
        except TypeError:
            return func(*args, **kwargs)

        if key in cache:
            wrapper.hits += 1
            return cache[key]

        wrapper.misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    def cache_clear():
        wrapper.hits = 0
        wrapper.misses = 0
        cache.clear()

    wrapper.cache_clear = cache_clear

    wrapper.hits = 0
    wrapper.misses = 0

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper


if __name__ == '__main__':
    calls = []

    def slow_square(x, power=2):
        '''Возводит в степень.'''
        calls.append(x)
        return x ** power

    sq = memoize(slow_square)
    assert sq(3) == 9 and sq(3) == 9 and sq(3, power=3) == 27
    assert calls == [3, 3]
    assert (sq.hits, sq.misses) == (1, 2)
    assert sq.__name__ == 'slow_square' and sq.__doc__ == 'Возводит в степень.'
    total = memoize(sum)
    assert total([1, 2, 3]) == 6 and total([1, 2, 3]) == 6   # нехешируемый аргумент: вызов без кэша
    assert (total.hits, total.misses) == (0, 0)
    sq.cache_clear()
    assert (sq.hits, sq.misses) == (0, 0)
    sq(3)
    assert calls[-1] == 3
    from time import perf_counter

    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    fast_fib = memoize(fib)  # вариант A
    start = perf_counter()
    fast_fib(30)
    time_a = perf_counter() - start
    print(f"Вариант A: misses={fast_fib.misses}, время={time_a:.6f} с")

    # Обёртка fast_fib вызывает исходную функцию fib.
    # При этом глобальное имя fib всё ещё указывает на исходную функцию.
    # Поэтому рекурсивные вызовы внутри неё обращаются напрямую к исходной функции, минуя кэш.
    # Согласно правилу LEGB, имя fib ищется в глобальной области видимости во время выполнения рекурсивного вызова.

    fib = memoize(fib)  # вариант B
    start = perf_counter()
    fib(30)
    time_b = perf_counter() - start
    print(f"Вариант B: misses={fib.misses}, время={time_b:.6f} с")

    # Теперь глобальное имя fib указывает на обёртку с кэшем.
    # Исходная функция при каждом рекурсивном вызове ищет имя fib по правилу LEGB и находит уже обёртку.
    # Поэтому все рекурсивные вызовы проходят через кэш.

    # Результаты запуска эксперимента:
    # Вариант A: misses=1, время=0.187505 с
    # Вариант B: misses=31, время=0.000102 с