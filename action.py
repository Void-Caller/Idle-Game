from adventure import *
from data_types import Currency
from decimal import Decimal
import time
import random


# TODO do poprawy odejmowanie atrybutów pasywnych aktualnie różne typy (Decimal - Currency)

def RestException(Exception):
    pass

class Work:
    # czynność trwająca ileś sekund; zużywa atrybuty pasywne
    def __init__(self, level):
        self.level = level #Decimal lub int
        self.work_time = random.randint(4,6)

    def onClock(self, bohater):
        #ulepszenia statow bohatera
        self.work_time -= 1
        if self.work_time == 0:
            return True
        return False

    #todo lub usunac
    def act(self, bohater, type=0, adventure=None):
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

            self.cost = (Decimal(random.randrange(5, 10, 1) / 100) * sum(self.dif_level))
            self.reward = (Decimal(random.randrange(5, 50, 1) / 100) * sum(self.dif_level))

            if bohater.passive[type].val - self.cost < 0:
                print("Nie posiadasz wystarczająco staminy")
            else:
                self.bohater = bohater
                return True
        else:
            print("Aby skorzystać zakończ misje...")
        return False

    #todo lub usunac
    def finish(self):
        self.bohater.passive[0].val -= self.cost * Decimal(self.work_time)
        self.bohater.riches += Currency(self.reward * Decimal(self.work_time), 'gold')


class Act:
    # pojedyncza czynność; żużywa atrybuty pasywne, do wykorzystania w trakcie misji
    def __init__(self, dif_level):
        self.dif_level = dif_level
        # generuje Riches w zamian za Stamina

        self.cost = Currency(Decimal(random.randrange(10, 15, 1) / 100) * sum(dif_level), "Stamina")
        self.reward = Currency(Decimal(random.randrange(2, 10, 1) / 100) * sum(dif_level), 'gold')

    def act(self, bohater, adventure=None):
        if (adventure is not None) and (adventure.in_action):
            if bohater.passive[0].val - self.cost < 0:
                print("Nie posiadasz wystarczająco staminy")
            else:
                self.bohater = bohater
        else:
            print("Aby skorzystać rozpocznij misje...")

    def finish(self):
        self.bohater.passive[0].val -= self.cost * Decimal(self.act_time)
        self.bohater.riches += Currency(self.reward * Decimal(self.act_time), 'gold')


class Rest:
    # przywracanie atrybutów pasywnych co sekundę
    def __init__(self):
        #jakie wlasciwosci, ulepszenia ma miec ta klasa?

        #przyrost na sekunde
        self.stamina = Currency('1', "Stamina")
        self.health = Currency('1', "Health")
        self.ploy = Currency('1', "Ploy")
        self.spirit = Currency('1', "Spirit")
        self.clarity = Currency('1', "Clarity")
        self.passive = [self.stamina, self.health, self.ploy, self.spirit, self.clarity]

    def onClock(self, bohater):
        counter = 0
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[0].val = bohater.passive[0].max
                counter += 1
        return counter == 5


class Camp:
    # camp działa jak rest; używany w trakcie misji
    def __init__(self):
        #jakie wlasciwosci, ulepszenia ma miec ta klasa?

        #przyrost na sekunde
        self.stamina = Currency('0.75', "Stamina")
        self.health = Currency('0.75', "Health")
        self.ploy = Currency('0.75', "Ploy")
        self.spirit = Currency('0.75', "Spirit")
        self.clarity = Currency('0.75', "Clarity")
        self.passive = [self.stamina, self.health, self.ploy, self.spirit, self.clarity]

    def onClock(self, bohater):
        counter = 0
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[0].val = bohater.passive[0].max
                counter += 1
        return counter == 5
