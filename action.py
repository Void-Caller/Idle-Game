from adventure import *
from data_types import Currency
from decimal import Decimal
import time
import random

# TODO do poprawy odejmowanie atrybutów pasywnych aktualnie różne typy (Decimal - Currency)

class Work:
    # czynność trwająca ileś sekund; zużywa atrybuty pasywne
    def __init__(self, dif_level, ended=False):
        self.dif_level = dif_level
        self.elapsed = 0.0

    def work(self, bohater, type=0, adventure=None):
        """
        Generowanie punktów doświadczenia dla 4 trybów:
            0 generuje might_exp
            1 generuje cunning_exp
            2 generuje psyche_exp
            3 generuje lore_exp
        """
        if (adventure is None) or (not adventure.in_action):
            if type == 0:
                self.nameExp = "might_exp"
                self.namePassive = "Stamina"
            elif type == 1:
                self.nameExp = "cunning_exp"
                self.namePassive = "Health"
            elif type == 2:
                self.nameExp = "psyche_exp"
                self.namePassive = "Ploy"
            elif type == 3:
                self.nameExp = "lore_exp"
                self.namePassive = "Spirit"
            self.cost = Currency(Decimal(random.randrange(1, 5, 1) / 500) * sum(self.dif_level), self.namePassive)
            self.reward = Currency(Decimal(random.randrange(5, 50, 1) / 500) * sum(self.dif_level), self.nameExp)
            if bohater.passive[type].val - self.cost < 0:
                print("Nie posiadasz wystarczająco staminy")
            else:
                # time.sleep(random.randrange(1, 10, 1))  # nie moze byc tych sleepow
                self.bohater = bohater
                # od 0.25 do 2 sekund
                self.work_time = random.random() * 1.75 + 0.25
                print(self.work_time)
        else:
            print("Aby skorzystać zakończ misje...")
        return 0

    def finish(self):
        self.bohater.passive[0].val -= self.cost.val
        self.bohater.riches += Currency(self.reward.val, 'gold')


class Act:
    # pojedyncza czynność; żużywa atrybuty pasywne, do wykorzystania w trakcie misji
    def __init__(self, dif_level):
        self.dif_level = dif_level
        # generuje Riches w zamian za Stamina
        self.cost = Currency(Decimal(random.randrange(1, 5, 1) / 500) * sum(dif_level), "Stamina")
        self.reward = Currency(Decimal(random.randrange(2, 10, 1) / 100) * sum(dif_level), 'gold')

    def act(self, bohater, adventure=None):
        if (adventure is not None) and (adventure.in_action):
            if bohater.passive[0].val - self.cost < 0:
                print("Nie posiadasz wystarczająco staminy")
            else:
                bohater.passive[0].val -= self.cost
                bohater.riches += self.reward
        else:
            print("Aby skorzystać rozpocznij misje...")


class Rest:
    # przywracanie atrybutów pasywnych co sekundę
    def __init__(self, dif_level):
        self.active = False
        self.dif_level = dif_level
        self.stamina = Currency(Decimal(random.randrange(100, 1000, 1) / 500) * sum(dif_level), "Stamina")

    def regeneration(self, bohater, time, adventure=None):
        if (adventure is None) or (not adventure.in_action):
            if bohater.passive[0].val + self.stamina > bohater.passive[0].max:
                bohater.passive[0].val = bohater.passive[0].max
            else:
                bohater.passive[0].val += self.stamina * Decimal(time)
        else:
            Camp(self.dif_level).regeneration(bohater, time, adventure)



class Camp:
    # camp działa jak rest; używany w trakcie misji
    def __init__(self, dif_level):
        self.dif_level = dif_level
        self.stamina = Currency(Decimal(random.randrange(100, 500, 1) / 500) * sum(dif_level), "Stamina")

    def regeneration(self, bohater, time, adventure=None):
        if (adventure is not None) and adventure.in_action:

            if bohater.passive[0].val + self.stamina > bohater.passive[0].max:
                bohater.passive[0].val = bohater.passive[0].max
            else:
                bohater.passive[0].val += self.stamina * Decimal(time)
        else:
            Rest(self.dif_level).regeneration(bohater, time, adventure)