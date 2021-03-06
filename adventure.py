from hero import Hero, Item
from data_types import Currency
from decimal import Decimal
import random


class CurrencyContainer:
    def __init__(self, dif_level, forclass):
        # todo generowanie treasures - balans
        temp = ['might_exp', 'cunning_exp', 'psyche_exp', 'lore_exp']

        if forclass == 'Challenge':
            # sum_dif_level = dif_level[0].val + dif_level[1].val + dif_level[2].val + dif_level[3].val
            self.exp = [Currency(Decimal(random.randrange(100, 300, 1) / 100) * dif_level[i], i) for i in range(4)]
            self.riches = Currency(Decimal(random.randrange(200, 500, 1) / 100) * sum(dif_level), 'gold')
            self.treasures = Currency(0, 'treasure')

        # nagrody 3-5 razy wieksze niz w challenge
        if forclass == 'Adventure':
            self.exp = [Currency(Decimal(random.randrange(300, 1500, 1) / 100) * dif_level[i], i) for i in range(4)]
            self.riches = Currency(Decimal(random.randrange(600, 2500, 1) / 100) * sum(dif_level), 'gold')
            self.treasures = Currency(0, 'treasure')

        # interfejs wypisuje tylko niezerowe nagrody
        self.print_list = [i for i in self.exp if i.val > Decimal(0)]
        if self.riches.val > Decimal(0):
            self.print_list.append(self.riches)
        if self.treasures.val > Decimal(0):
            self.print_list.append(self.treasures)


itemNames = [['Sword', 'Axe', 'Spear', "Club"], ['Helmet', 'Coif', 'Mask', 'Hood'], ['Mail', 'Furs', 'Scale', 'Hamata'],
             ['Ring', 'Band', 'Cuff', 'Braclet']]
itemPrefixes = ['Crimmerian', 'Scythian', 'Ancient', 'Aquilonian', 'Stygian', 'Bloody']
itemTypes = ['Weapon', 'Helmet', 'Armor', 'Ring']


class ItemContainer:
    # lista przedmiotow za ukonczenie przygody. Dla challenge lista bedzie pusta
    def __init__(self, dif_level, challenges_count):
        self.items = []

        amount = random.randint(8, 12) * challenges_count // 50  # 1 item na 4-6 wyzwan
        for i in range(amount):
            # losowanie nazwy przedmiotu
            type_ind = random.randint(0, 3)
            name = random.choice(itemPrefixes) + ' ' + random.choice(itemNames[type_ind])
            # losowanie typu przedmiotu
            type = itemTypes[type_ind]

            # klasa przedmiotu 75% zwyk??y, 15% rzadki, 9% mistrzowski, 1% legendarny
            rarity = 0
            rar = random.random()
            if rar < 0.75:
                rarity = Decimal('1')
            elif 0.75 <= rar < 0.9:
                rarity = Decimal('1.25')
                name = 'Strong ' + name
            elif 0.9 <= rar < 0.99:
                rarity = Decimal('1.5')
                name = 'Masterwork ' + name
            else:
                rarity = Decimal('2.5')
                name = 'Legendary ' + name

            # tablica pomocnicza do losowania atrybut??w
            tmp = [0, 1, 2, 3]
            atributes = [0, 0, 0, 0]

            # losowanie atrybutu wzmacnianego przez przedmiot
            # losowanie i zapisanie bonusu
            atributes[tmp.pop(random.randrange(len(tmp)))] = (Decimal(random.randrange(5, 15, 1)) / Decimal(
                50)) * dif_level[0] * rarity
            # sprawdzanie czy wzmacniany jest drugi atrybut, trzeci i czwarty
            if random.random() < 0.4:
                atributes[tmp.pop(random.randrange(len(tmp)))] = (Decimal(random.randrange(5, 15, 1)) / Decimal(
                    50)) * dif_level[1] * rarity
                if random.random() < 0.4:
                    atributes[tmp.pop(random.randrange(len(tmp)))] = (Decimal(random.randrange(5, 15, 1)) / Decimal(
                        50)) * dif_level[2] * rarity
                    if random.random() < 0.4:
                        atributes[tmp.pop(random.randrange(len(tmp)))] = (Decimal(random.randrange(5, 15, 1)) / Decimal(
                            50)) * dif_level[3] * rarity

            minimum = [0, 0, 0, 0]
            for j in range(4):
                minimum[j] = (Decimal(random.randrange(5, 15, 1)) / Decimal(50)) * dif_level[j]
            sell_price = sum(atributes)
            self.items.append(
                Item(name, type, minimum=minimum,
                     m=atributes[0], c=atributes[1], p=atributes[2], l=atributes[3], value=sell_price))


class Reward:
    # generowanie i przechowywanie nagrody za adventure/challenge
    def __init__(self, diff_level, type, challengesCount=0):
        self.waluta = CurrencyContainer(diff_level, type)
        self.items = ItemContainer(diff_level, challengesCount)

    def getItems(self):
        return self.items.items


challenge_names = ["Bandits", "Wild beast", "Crossing the treacherous river", "Cultists' trap",
                   "Ancient Riddle", "Hostile nomads", "Barbarian chief", "Cursed Tablet",
                   "Dangerous corridor", "Dark labyrinth", "Poisonous snakes", "Dark monolith"]
adventure_names = ["Temple of Doom", "Temple of the Black Pharaoh", "Stygian Depths", "Forsaken City",
                   "Ancient Tomb", "Atlantean Ruins", "Uncharted Wilderness", "Untamed Jungle",
                   "Deepest Forest", "Barbarian Citadel"]


class CampException(Exception):
    pass


class Challenge:  # wyzwanie
    def __init__(self, dif_level):
        self.name = random.choice(challenge_names)
        self.difficulty = [Decimal(random.randrange(50, 150, 1) / 10) * dif_level[i] for i in range(4)]
        self.reward = Reward(self.difficulty, 'Challenge')
        self.cost = []
        # testowane 4 atrybuty aktywne
        for i in range(4):
            self.cost.append(Decimal(random.randrange(50, 100, 1) / 500) * self.difficulty[i])
        # piaty atrybut nieodpowiadajacy testowanym atrybutom todo balans
        self.cost.append(Decimal(random.randrange(50, 100, 1) / 1800) * sum(dif_level))

        # do progress baru
        self.progress_current = Decimal(0)
        self.progress_maximum = Decimal(0)
        # self.cost_per_sec = [cost/diff for cost in self.cost for diff in self.difficulty]
        # self.cost / self.difficulty
        self.time = None

    def get_time(self, hero):
        self.time = self.difficulty[0] / hero.active[0].val
        for i in range(1, 4):
            tmp = self.difficulty[i] / hero.active[i].val
            if tmp > self.time:
                self.time = tmp
        self.progress_maximum = self.time
        return self.time

    def get_cost(self):
        cost = []
        for i in range(4):
            cost.append(self.cost[i])
        return cost

    def can_hero_start(self, hero):
        for i in range(5):
            if hero.passive[i].val < self.cost[i]:
                print("false {} < {}".format(hero.passive[i], self.cost[i]))
                return False
        return True

    def update(self, bohater, d_time):
        """return true if completed challenge, false if not"""
        d_time = Decimal(d_time)
        # for i in range(5):
        #     bohater.passive[i].val -= self.cost[i] * d_time

        self.progress_current += d_time

        for i in range(4):
            value = bohater.active[i].val * d_time
            # self.cost[i] -= value

        for i in range(4):
            value = bohater.active[i].val * d_time

            if self.difficulty[i] != 0 and (self.difficulty[i] - value > 0):
                self.difficulty[i] -= value
            else:
                self.difficulty[i] = 0

            bohater.passive[i + 1].val -= (self.cost[i] / self.time) * d_time

        return self.difficulty == [0, 0, 0, 0]

    '''return true if completed challenge, false if not'''
    def onClock(self, bohater):
        temp_list = [bohater.passive[i].val - self.cost[i] for i in range(5)]
        for i in temp_list:
            if i < 0:
                raise CampException
        for i in range(5):
            bohater.passive[i].val -= self.cost[i]
        for i in bohater.passive:
            if i.val == 0:
                raise CampException
        for i in range(4):
            if self.difficulty[i] - bohater.active[i].val > 0:
                self.difficulty[i] -= bohater.active[i].val
            else:
                self.difficulty[i] = 0
        return self.difficulty == [0, 0, 0, 0]


class Adventure:  # przygoda
    def __init__(self, diff_level):
        self.dif_level = diff_level
        self.name = random.choice(adventure_names)
        self.amount = random.randint(4, 20)
        self.challenges = [Challenge(diff_level) for i in range(self.amount)]
        self.challenge_index = 0
        self.reward = Reward(diff_level, 'Adventure', self.amount)
        # todo pasek postepu przygody - gdzie?
        # todo pasek postepu danego wyzwania - gdzie?

    def get_remaining_challenges(self):
        return len(self.challenges) - self.challenge_index

    def get_total_costs(self):
        cost = [Decimal(0), Decimal(0), Decimal(0), Decimal(0)]
        for challenge in self.challenges:
            for i in range(4):
                cost[i] += challenge.cost[i]
        return cost

    '''Zwraca bool czy przygoda zostala ukonczona. 
    rzuca blad CampException jezeli trzeba zastopowac przygode, bo wyczerpaly sie atrybuty pasywne.'''

    def onClock(self, bohater):
        try:
            if self.challenges[self.challenge_index].onClock(bohater):
                bohater.applyReward(self.challenges[self.challenge_index].reward)
                self.challenge_index += 1
                if self.challenge_index != self.amount:
                    return False
                bohater.applyReward(self.reward)
                return True
        except CampException:
            raise  # do nadrzednej metody
        except Exception as e:
            print(e)
            print("ADVENTURE EXCEPTION")


if __name__ == "__main__":
    test_items = ItemContainer(10, 50)

    for item in test_items.items:
        print(item.name + ' ' + str(item.min_attr[0]))
