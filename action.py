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
    # work_type wybieramy z interfacu czy random??
    def __init__(self, level, hero, work_type=-1, adventure=None):
        self.level = level #Decimal lub int
        self.elapsed_time = 0.0
        self.work_time = random.randint(4, 6)

        if work_type == -1:
            work_type = random.randint(0, 3)
        print(work_type)

        self.work_type = work_type
        self.cost = (Decimal(random.randrange(5, 10, 1) / 100) * sum(hero.get_attr())) / Decimal(self.work_time)
        self.reward = (Decimal(random.randrange(5, 50, 1) / 100) * sum(hero.get_attr())) / Decimal(self.work_time)

    def update(self, hero, d_time, adventure=None):
        """
        Returns:
            True - work ended
            False - work in progress
        """
        ret = False
        if self.elapsed_time + d_time > self.work_time:
            d_time = self.elapsed_time - self.work_time
            ret = True
        else:
            self.elapsed_time += d_time

        if hero.passive[self.work_type + 1].val - self.cost < 0:
            print("Nie posiadasz wystarczająco staminy")
            ret = True
        else:
            hero.passive[self.work_type + 1].val -= self.cost
            hero.active_exp[self.work_type].val += self.reward

        return ret


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

    # Do usuniecia?
    def onClock(self, bohater):
        counter = 0
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[0].val = bohater.passive[0].max
                counter += 1
        return counter == 5

    def update(self, bohater, d_time):
        """
        Parameters:
            bohater
            d_time - czas który upłynął od ostatniej regenracji
        """
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[i].val = bohater.passive[i].max
            else:
                bohater.passive[i].val += self.passive[i].val * Decimal(d_time)


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
