from data_types import Currency, PassiveAttribute
from decimal import Decimal


class Hero:
    def __init__(self, name):
        # nazwa
        self.name = name
        # waluty
        self.currency_might = Currency(0, 'might_exp')
        self.currency_cunning = Currency(0, 'cunning_exp')
        self.currency_psyche = Currency(0, 'psyche_exp')
        self.currency_lore = Currency(0, 'lore_exp')
        self.treasures = Currency(0, 'treasure')
        self.riches = Currency(0, 'gold')
        # atrybuty czynne
        self.might = Currency(1, 'Might')
        self.cunning = Currency(1, 'Cunning')
        self.psyche = Currency(1, 'Psyche')
        self.lore = Currency(1, 'Lore')
        self.active = [self.might, self.cunning, self.psyche, self.lore]
        # atrybuty pasywne
        self.stamina = PassiveAttribute(20, 'Stamina')
        self.health = PassiveAttribute(20, 'Health')
        self.ploy = PassiveAttribute(20, 'Ploy')
        self.spirit = PassiveAttribute(20, 'Spirit')
        self.clarity = PassiveAttribute(20, 'Clarity')
        self.passive = [self.stamina, self.health, self.ploy, self.spirit, self.clarity]
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
                self.might += i.item_might
                self.cunning += i.item_cunning
                self.psyche += i.item_psyche
                self.lore += i.item_lore

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
                #usuwamy bonusy poprzedniego przedmiotu
                self.might -= self.set[0].item_might
                self.cunning -= self.set[0].item_cunning
                self.psyche -= self.set[0].item_psyche
                self.lore -= self.set[0].item_lore
                #dopiero zamieniamy na nowy
                self.weapon = it
                self.set[0] = it
        elif it.type == 'Helmet':
            if self.set[1] == None:
                self.helmet = it
                self.set[1] = it
            else:
                #usuwamy bonusy poprzedniego przedmiotu
                self.might -= self.set[1].item_might
                self.cunning -= self.set[1].item_cunning
                self.psyche -= self.set[1].item_psyche
                self.lore -= self.set[1].item_lore
                #dopiero zamieniamy na nowy
                self.helmet = it
                self.set[1] = it
        elif it.type == 'Armor':
            if self.set[2] == None:
                self.armor = it
                self.set[2] = it
            else:
                #usuwamy bonusy poprzedniego przedmiotu
                self.might -= self.set[2].item_might
                self.cunning -= self.set[2].item_cunning
                self.psyche -= self.set[2].item_psyche
                self.lore -= self.set[2].item_lore
                #dopiero zamieniamy na nowy
                self.armor = it
                self.set[2] = it
        elif it.type == 'Ring':
            if self.set[3] == None:
                self.ring = it
                self.set[3] = it
            else:
                #usuwamy bonusy poprzedniego przedmiotu
                self.might -= self.set[3].item_might
                self.cunning -= self.set[3].item_cunning
                self.psyche -= self.set[3].item_psyche
                self.lore -= self.set[3].item_lore
                #dopiero zamieniamy na nowy
                self.ring = it
                self.set[3] = it
        else:
            raise Exception('Not supported type of item')
        self.updateActiveAttributes()

    def printHeroActive(self):
        print(self.might)
        print(self.cunning)
        print(self.psyche)
        print(self.lore)

    def printHeroPassive(self):
        print(self.stamina)
        print(self.health)
        print(self.ploy)
        print(self.spirit)
        print(self.clarity)


class Item:
    def __init__(self, name, type, minimum=[0, 0, 0, 0], m=0, c=0, p=0, l=0):
        self.name = name
        self.type = type

        # tablica minimalnych atrybutów aktywnych ktore musi miec bohater aby zalozyc przedmiot
        self.min_attr = []
        for i in range(len(minimum)):
            self.min_attr.append(Decimal(minimum[i]))

        self.item_might = Currency(m,"Might")
        self.item_cunning = Currency(c,"Cunning")
        self.item_psyche = Currency(p,"Psyche")
        self.item_lore = Currency(l,'Lore')
        self.item_attr = [self.item_might, self.item_cunning, self.item_psyche, self.item_lore]

    # Ustawienie minimalnych atrybutow potrzebnych do zalozenia przedmiotu
    def setMinAttr(self, new):
        for i in range(len(new)):
            self.min_attr[i] = Decimal(new[i])

    def printItem(self):
        print(self.name)
        print(self.type)
        print(self.min_attr)
        print('+', self.item_might)
        print('+', self.item_cunning)
        print('+', self.item_psyche)
        print('+', self.item_lore)


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
    i1 = Item('Dziadek do orzechow', 'Weapon')
    i1.setMinAttr([1, 2, 1, 1])
    i1.item_might = 2
    i1.item_cunning = 3
    i1.item_psyche = 0
    i1.item_lore = 6
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
    h1.might.val += 10
    h1.cunning.val += 10
    h1.psyche.val += 10
    h1.lore.val += 10

    h1.printHeroActive()
    print('')
    print(h1.eq.all_items)
    print('Jeszcze w secie nic nie ma zalozonego')
    print(h1.set[0])
    h1.setActiveItem(i1)
    print('A teraz juz ma ')
    print(h1.set[0])
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