from decimal import Decimal

class Multipier():
    '''
    Klasa tiered multiplier

    inicjalizacja:
    val - wartość wprowadzana multiplikatora
    tier - poziom w hierarchii
    div - dzielnik wartości, przez właściwości catowania typów, najłatwiejszą formą uzyskiwania dokładnych wartości
    Decimal przy inicjacji jest notacja val/div. Przykładowo, modyfikator 1.05 poziomu 2 uzyskujemy Multipier(105,2,100)

    Atrybuty:
    val - wartość modyfikatora, już podzielona, wartość typu Decimal
    tier - poziom w hierarhii wartość typu int

    Metody:
    Przecioążony operator mnożenia dla obiektów Multipier, Currency, Decimal i int.
    Przeciążone operatory porównania dla obiektów Multipier, Decimal i int.
    Przeciążona str().

    Jedyną operacją arytmetyczną na obiektach Multipier jest mnożenie.
    Przy przemnożeniu obiektu Multipier przez drugi Multipier sprawdzane są ich poziomy tier.

    Jeśli są równe, to zwracana jest wartość val1+val2-1, co odpowiada potraktowaniu wartości modyfikatorów jako procentowych
    100%+val1% i 100%+val2%, gdzie val1% i val2% to część wartości obydwu modyfikatorów powyżej 1, i dodanie ich do siebie
    jako 100%++val1%+val2%. Funkcja zwraca nowy Multipier zavierający podaną wartość i ten sam tier co składowe.

    Jeśli są różne, to zwracany jest iloraz val1*val2.

    Przemnożenie obiektu Currency zwróci obiekt Currency, którego wartość została przemnożona przez wartość obiektu Multipier

    Przemnożenie obiektu int lub Decimal zwróci Multipier o identycznym tier i val przemnożonym przez wartość int lub Decimal.

    '''
    def __init__(self, val=0, tier=1, div=1):
        self.val = Decimal(val)/Decimal(div)
        self.tier = tier

    def __str__(self):
        return str(self.val)+", t="+str(self.tier)

    def __mul__(self, other):
        if isinstance(other, Multipier):
            if other.tier == self.tier:
                return Multipier(self.val+other.val-1, self.tier)
            else:
                return self.val*other.val
        elif isinstance(other, Currency):
            return Currency(self.val*other.val, other.type)
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Multipier(self.val*other, self.tier)
        else:
            raise TypeError

    __rmul__ = __mul__

    def __lt__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val < other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val < other
        else:
            raise TypeError

    def __le__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val <= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val <= other
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val == other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val == other
        else:
            raise TypeError

    def __ne__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val != other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val != other
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val > other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val > other
        else:
            raise TypeError

    def __ge__(self, other):
        if isinstance(other, Multipier):
            if other.type == self.type:
                return self.val >= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val >= other
        else:
            raise TypeError

class Currency():
    '''
    Klasa definiująca typ walut gry, takich jak złoto i punkty doświadczenia

    Atrybuty:
    val - wartość typu Decimal
    type - string z typem waluty

    Waluty:
    gold - złoto, podstawowa waluta pieniężna
    treasure - specjalne zasoby, oddzielne od złota
    might_exp - punkty doświadczenia atrybutu Might
    cunning_exp - punkty doświadczenia atrybutu Cunning
    psyche_exp - punkty doświadczenia atrybutu Psyche
    lore_exp - punkty doświadczenia atrybutu Lore

    Metody:
    Przeciążony operator mnożenia dla Multipier.
    Przeciążone podstawowe operatory matematyczne dla Currency, int i Decimal.
    Przeciążone operatory poównań dla Currency, int i Decimal.
    Przeciążona str().

    Operatory arytmetyczne zwracają wartości Currency o tym samym typie co ich składniki.
    Operacje arytmetyczne wielu obiektów Currency można wykonywać tylko na obiektach o tym samym typie waluty.

    '''
    def __init__(self, val=0, type='gold'):
        self.val = Decimal(val)
        self.type = type

    def __str__(self):
        return str(self.type) + " " + str(self.val)

    def __mul__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val*other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Multipier):
            return Currency(self.val * other.val, self.type)
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val * other, self.type)
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val+other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val+other, self.type)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val-other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val-other, self.type)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(other.val - self.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(other - self.val, self.type)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val/other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val/other, self.type)
        else:
            raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(other.val/self.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(other/self.val, self.type)
        else:
            raise TypeError

    def __lt__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val < other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val < other
        else:
            raise TypeError

    def __le__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val <= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val <= other
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val == other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val == other
        else:
            raise TypeError

    def __ne__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val != other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val != other
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val > other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val > other
        else:
            raise TypeError

    def __ge__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val >= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val >= other
        else:
            raise TypeError

    __rmul__ = __mul__
    __radd__ = __add__

class PassiveAttribute(Currency):
    '''
    Operatory zarządzają obecnym poziomem atrybutu val.
    Jego maksymalny poziom, max trzeba zmieniać poprzez odwołania do atrybutu.

    '''
    def __init__(self, val=0, max=100, type='Spirit'):
        self.type = type
        self.val = Decimal(val)
        self.max = Decimal(100)

    def __str__(self):
        return str(self.type) + "Max: " + str(self.max) + "Current: " + str(self.val)

    def __mul__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val*other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Multipier):
            return Currency(self.val * other.val, self.type)
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val * other, self.type)
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val+other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val+other, self.type)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val-other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val-other, self.type)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(other.val - self.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(other - self.val, self.type)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(self.val/other.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(self.val/other, self.type)
        else:
            raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return Currency(other.val/self.val, self.type)
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return Currency(other/self.val, self.type)
        else:
            raise TypeError

    def __lt__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val < other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val < other
        else:
            raise TypeError

    def __le__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val <= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val <= other
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val == other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val == other
        else:
            raise TypeError

    def __ne__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val != other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val != other
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val > other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val > other
        else:
            raise TypeError

    def __ge__(self, other):
        if isinstance(other, Currency):
            if other.type == self.type:
                return self.val >= other.val
            else:
                raise TypeError
        elif isinstance(other, Decimal) or isinstance(other, int):
            return self.val >= other
        else:
            raise TypeError

    __rmul__ = __mul__
    __radd__ = __add__


if __name__ == '__main__':
    mult1 = Multipier(11, 1)
    mult2 = Multipier(11, 1, 10)
    mult3 = Multipier(11, 2)

    gold1 = Currency(100)
    gold2 = Currency(2)
    mult = Multipier(11, 2, 10)


    print('test mnożenia')
    print(gold1*3)
    print(3*gold1)
    print(gold2*gold1)

    print('\ntest dodawania')
    print(gold1 + 3)
    print(3 + gold1)
    print(gold2 + gold1)

    print('\ntest odejmowania')
    print(gold1 - 3)
    print(300 - gold1)
    print(gold1 - gold2)

    print('\ntest dzielenia')
    print(gold1/3)
    print(300/gold1)
    print(gold1/gold2)

    print('\ntest >')
    print(gold1 > 3)
    print(300 > gold1)
    print(gold1 > gold2)

    print('\ntest >=')
    print(gold1 >= 3)
    print(300 >= gold1)
    print(gold1 >= gold2)

    print('\ntest <=')
    print(gold1 < 3)
    print(300 < gold1)
    print(gold1 < gold2)

    print('\ntest <=')
    print(gold1 <= 3)
    print(300 <= gold1)
    print(gold1 <= gold2)

    print('\ntest ==')
    print(gold1 == 3)
    print(300 == gold1)
    print(gold1 == gold2)

    print('\ntest modyfikatora')
    print(gold1 * mult)
    print(mult * gold1)

    print(mult1 * mult2)
    print(mult1 * mult3)
    print(mult2 * 2)
    print(2 * mult2)