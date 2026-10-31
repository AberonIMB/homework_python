class Money:
    __slots__ = ('amount', 'currency')

    def __init__(self, amount, currency):
        if type(amount) is not int:
            raise TypeError("amount должен быть целым числом копеек")
        if not isinstance(currency, str):
            raise TypeError("currency должна быть строкой")
        
        object.__setattr__(self, 'amount', amount)
        object.__setattr__(self, 'currency', currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __setattr__(self, key, value):
        raise AttributeError(f"Нельзя изменить или создать поле {key}")

    def __delattr__(self, item):
        raise AttributeError(f"Нельзя удалить поле {item}")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Невозможно сложить разные валюты")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"Money({repr(self.amount)}, {repr(self.currency)})"

def total_by_currency(pays: list[Money]) -> dict[str, Money]:
    result = {}

    for pay in pays:
        if pay.currency in result:
            result[pay.currency] += pay
        else:
            result[pay.currency] = pay

    return result

if __name__ == '__main__':
    assert len({Money(100, 'RUB'), Money(100, 'RUB'), Money(100, 'USD')}) == 2
    prices = {Money(100, 'RUB'): 'сто рублей'}
    assert prices[Money(100, 'RUB')] == 'сто рублей'
    assert Money(100, 'RUB') + Money(50, 'RUB') == Money(150, 'RUB')
    for action in (lambda m: setattr(m, 'amount', 5), lambda m: setattr(m, 'extra', 1)):
        try:
            action(Money(1, 'RUB'))
            assert False, 'ожидали AttributeError'
        except AttributeError:
            pass
    try:
        Money(1, 'RUB') + Money(1, 'USD')
        assert False, 'ожидали ValueError'
    except ValueError:
        pass
    pays = [Money(100, 'RUB'), Money(5, 'USD'), Money(250, 'RUB')]
    assert total_by_currency(pays) == {'RUB': Money(350, 'RUB'), 'USD': Money(5, 'USD')}

# Если изменить amount или currency после добавления Money в dict или set, изменится его хеш.
# Объект останется в месте, выбранном при вставке по старому хешу, и поиск по новому хешу может его не найти.
# Как в примере с Point из лекции, после изменения поля, участвующего в хеше, проверка p in visited возвращает False.
# Поэтому поля Money, участвующие в равенстве и вычислении хеша, должны оставаться неизменными.

