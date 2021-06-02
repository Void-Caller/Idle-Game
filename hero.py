from data_types import Currency, PassiveAttribute
from decimal import Decimal

active_names = ["Might", "Cunning", "Psyche", "Lore"]
passive_names = ["Stamina", "Health", "Ploy", "Spirit", "Clarity"]

class Hero:
    def __init__(self, name):
        # nazwa
        self.name = name
        # waluty
        # self.currency_might = Currency(0, 'might_exp')
        # self.currency_cunning = Currency(0, 'cunning_exp')
        # self.currency_psyche = Currency(0, 'psyche_exp')
        # self.currency_lore = Currency(0, 'lore_exp')
        self.active_exp = [Currency(0, 'might_exp'), Currency(0, 'cunning_exp'),
                           Currency(0, 'psyche_exp'), Currency(0, 'lore_exp')]
        self.treasures = Currency(0, 'treasure')
        self.riches = Currency(0, 'gold')
        # atrybuty czynne
        # wszystkie odwołania do atrybutów mają iść przez tablicę
        # 0-Might
        # 1-Cunning
        # 2-Psyche
        # 3-Lore
        self.train_active = [Currency(1, 'Might'), Currency(1, 'Cunning'), Currency(1, 'Psyche'), Currency(1, 'Lore')]
        self.active = [Currency(1, 'Might'), Currency(1, 'Cunning'), Currency(1, 'Psyche'), Currency(1, 'Lore')]
        # atrybuty pasywne
        # wszystkie odwołania do atrybutów mają iść przez tablicę
        # 0-Stamina
        # 1-Health
        # 2-Ploy
        # 3-Spirit
        # 4-Clarity
        self.passive = [PassiveAttribute(20, 'Stamina'), PassiveAttribute(20, 'Health'), PassiveAttribute(20, 'Ploy'),
                        PassiveAttribute(20, 'Spirit'), PassiveAttribute(20, 'Clarity')]

        self.passive_max = [PassiveAttribute(100, 'Stamina'), PassiveAttribute(100, 'Health'), PassiveAttribute(100, 'Ploy'),
                            PassiveAttribute(100, 'Spirit'), PassiveAttribute(100, 'Clarity')]
        # umiejetnosci
        self.skills = None  # jakies inne umiejetnosci, jeszcze nie utworzony typ.
        # ekwipunek
        self.eq = Equipment(5)
        # zalozony ekwipunek
        self.weapon = None
        self.helmet = None
        self.armor = None
        self.ring = None
        # caly set ubrany
        self.set = [self.weapon, self.helmet, self.armor, self.ring]
        self.updateActiveAttributes()

    def applyReward(self, reward):
        # otrzymanie nagrody za ukonczony challenge/adventure
        pass

    # Zaktualizowanie statystyk o wartosci zalozonych przedmiotow
    def updateActiveAttributes(self):
        for i in self.set:
            if i != None:
                for j in range(4):
                    self.active[j] += i.item_attr[j]

    # Wyposazenie bohatera w przedmiot z naszego ekwipunku
    def setActiveItem(self, it):
        if it in self.eq.all_items:
            for i in range(len(it.min_attr)):
                if it.min_attr[i] > self.active[i]:
                    raise Exception('You have too few ' + self.active[i].type + ' points to wear this item')
        if it.type == 'Weapon':
            if self.set[0] == None:
                self.weapon = it
                self.set[0] = it
            else:
                # usuwamy bonusy poprzedniego przedmiotu
                for i in range(4):
                    self.active[i] -= self.set[0].item_attr[i]

                # dopiero zamieniamy na nowy
                self.weapon = it
                self.set[0] = it
        elif it.type == 'Helmet':
            if self.set[1] == None:
                self.helmet = it
                self.set[1] = it
            else:
                # usuwamy bonusy poprzedniego przedmiotu
                for i in range(4):
                    self.active[i] -= self.set[1].item_attr[i]

                # dopiero zamieniamy na nowy
                self.helmet = it
                self.set[1] = it
        elif it.type == 'Armor':
            if self.set[2] == None:
                self.armor = it
                self.set[2] = it
            else:
                # usuwamy bonusy poprzedniego przedmiotu
                for i in range(4):
                    self.active[i] -= self.set[2].item_attr[i]
                # dopiero zamieniamy na nowy
                self.armor = it
                self.set[2] = it
        elif it.type == 'Ring':
            if self.set[3] == None:
                self.ring = it
                self.set[3] = it
            else:
                # usuwamy bonusy poprzedniego przedmiotu
                for i in range(4):
                    self.active[i] -= self.set[3].item_attr[i]
                # dopiero zamieniamy na nowy
                self.ring = it
                self.set[3] = it
        else:
            raise Exception('Not supported type of item')
        self.updateActiveAttributes()

    def printHeroActive(self):
        for i in range(4):
            print(self.active[i])

    def printHeroPassive(self):
        for i in range(5):
            print(self.passive[i])

    def get_attr(self):
        return [self.active[0].val, self.active[1].val, self.active[2].val, self.active[3].val]

    def equip(self, item_id):
        try:
            self.setActiveItem(self.eq.all_items[item_id])
            del self.eq.all_items[item_id]
        except Exception:
            pass

    def sell(self, item_id):
        item = self.eq.all_items[item_id]
        name = item.name
        value = item.value

        self.riches.val += self.eq.all_items[item_id].value
        del self.eq.all_items[item_id]
        return [name, value]

    def getNextUpgradeCost(self, attribute_id, active=True):
        cost = Decimal(100)  # todo
        return cost

    def train(self, attribute_id, active=True):
        value = None
        success = False
        cost = None

        if active:
            value = Decimal(0.5)
            cost = self.getNextUpgradeCost(attribute_id)
            if cost < self.active_exp[attribute_id]:
                self.train_active[attribute_id] += 1
                self.active_exp[attribute_id].val -= cost

                self.active[attribute_id].val += value
                success = True
        else:
            value = Decimal(20)
            cost = Decimal(100)

            if [cost < self.active_exp[i] for i in range(4)] == [True for i in range(4)]:
                for i in range(4):
                    self.active_exp[i].val -= cost

                self.passive_max[attribute_id].val += value
                success = True
                value = self.passive_max[attribute_id].val

        return success, cost, self.getNextUpgradeCost(attribute_id, False), value

class Item:
    def __init__(self, name, type, minimum=[0, 0, 0, 0], m=0, c=0, p=0, l=0, value=0):
        self.name = name
        self.type = type
        self.value = value

        # tablica minimalnych atrybutów aktywnych ktore musi miec bohater aby zalozyc przedmiot
        self.min_attr = []
        for i in range(len(minimum)):
            self.min_attr.append(Decimal(minimum[i]))

        self.item_might = Currency(m, "Might")
        self.item_cunning = Currency(c, "Cunning")
        self.item_psyche = Currency(p, "Psyche")
        self.item_lore = Currency(l, 'Lore')
        # wszystkie odwołania do atrybutów mają iść przez tablicę
        self.item_attr = [self.item_might, self.item_cunning, self.item_psyche, self.item_lore]

    # Ustawienie minimalnych atrybutow potrzebnych do zalozenia przedmiotu
    def setMinAttr(self, new):
        for i in range(len(new)):
            self.min_attr[i] = Decimal(new[i])

    def printItem(self):
        print(self.name)
        print(self.type)
        print(self.min_attr)
        for i in range(4):
            print('+', self.item_attr[i])


class Equipment:

    def __init__(self, size):
        self.size = size
        self.all_items = []
        self.weapons = []
        self.helmets = []
        self.armors = []
        self.rings = []

    # Dodaje przedmiot do ekwipunku
    def addItem(self, i):
        if self.getFreeSpace():
            if i.type == 'Weapon':
                self.weapons.append(i)
            elif i.type == 'Helmet':
                self.helmets.append(i)
            elif i.type == 'Armor':
                self.armors.append(i)
            elif i.type == 'Ring':
                self.rings.append(i)
            else:
                raise Exception('Not supported type of item')
            self.all_items.append(i)

    # Oblicza ilosc wolnego miejsca w ekwipunku
    def getFreeSpace(self):
        if self.size - len(self.all_items) > 0:
            return True
        else:
            raise Exception('Too many items in equipment')

    # Jesli jest w eq przedmiot o danej nazwie, usuwa go z listy konkretnych przedmiotow oraz z ogolnej listy
    def removeItem(self, it):
        tmp_list = self.all_items.copy()
        for i in tmp_list:
            if i.name == it:
                if i.type == 'Weapon':
                    self.weapons.remove(i)
                elif i.type == 'Helmet':
                    self.helmets.remove(i)
                elif i.type == 'Armor':
                    self.armors.remove(i)
                elif i.type == 'Ring':
                    self.rings.remove(i)
                self.all_items.remove(i)


if __name__ == '__main__':
    print('UWAGA TESTY')
    h1 = Hero('Andrzej')
    print('Oto ', h1.name)
    print('')
    i1 = Item('Dziadek do orzechow', 'Weapon', minimum=[1, 2, 1, 1], m=2, c=3, p=0, l=6)
    i1.printItem()
    print('')
    i2 = Item('Durszlak Spaczenia', 'Helmet')
    i2.setMinAttr([11, 112, 23, 4])
    i2.item_might = 5
    i2.item_cunning = 13
    i2.item_psyche = 8
    i2.item_lore = 0
    i2.printItem()
    print('')

    h1.eq.addItem(i1)
    h1.eq.addItem(i2)
    print(h1.eq.weapons)
    print(h1.eq.helmets)
    print(h1.eq.armors)
    print(h1.eq.rings)
    # h1.eq.addItem(i1)
    # h1.eq.addItem(i1)
    # h1.eq.addItem(i1)
    # h1.eq.addItem(i1)
    print('Wiecej przedmiotow nie wejdzie do eq niz jest w nim miejsca')
    print('')
    print('Rozdaje postaci jakies poczatkowe punkty umiejetnosci')
    h1.active[0].val += 10
    h1.active[1].val += 10
    h1.active[2].val += 10
    h1.active[3].val += 10

    h1.printHeroActive()
    print('')
    print(h1.eq.all_items)
    print('Jeszcze w secie nic nie ma zalozonego')
    print(h1.set[0])
    h1.setActiveItem(i1)
    print('A teraz juz ma ')
    h1.set[0].printItem()
    print('')
    print('Zwiekszyly sie statystyki naszego bohatera')
    h1.printHeroActive()
    print('')
    h1.printHeroPassive()
    print('A to ponizej nie zadziala bo nasz bohater nie ma wystarczajacej ilosci punktow')
    # h1.setActiveItem(i2)
    print('Podmiana przedmiotu')
    i3 = Item('Maaaczuga', 'Weapon')
    i3.setMinAttr([1, 1, 1, 1])
    i3.item_might = 1
    i3.item_cunning = 1
    i3.item_psyche = 1
    i3.item_lore = 1
    i3.printItem()
    h1.setActiveItem(i3)
    h1.printHeroActive()
    print('Po zmianie usuney sie bonusy starej broni a zostaly dodane nowe')

    '''
    for i in h1.active:
        print(i.currency)
    for i in h1.set:
        print(i)
    for i in h1.passive:
        print(i.actual)
    '''
