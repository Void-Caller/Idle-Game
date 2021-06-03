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
    level = Decimal(1)

    def __init__(self, hero, work_type=-1):
        self.elapsed_time = 0.0
        self.work_time = random.randint(4, 6)
        self.work_type = work_type

        self.cost = ((Decimal(random.randrange(5, 10, 1) / 100) * sum(hero.get_attr()))
                     * Work.level) / Decimal(self.work_time)
        self.reward = ((Decimal(random.randrange(5, 50, 1) / 100) * sum(hero.get_attr()))
                       * Work.level) / Decimal(self.work_time)

    def update(self, hero, d_time, adventure=None):
        """
        Returns:
            1 - work ended
            0 - work in progress
            -1 - not enough stamina
        """
        ret = 0
        if self.elapsed_time + d_time > self.work_time:
            d_time = self.elapsed_time - self.work_time
            ret = 1
        else:
            self.elapsed_time += d_time

        # if hero.passive[self.work_type + 1].val - self.cost < 0:
        if hero.passive[0].val - self.cost < 0:
            print("Nie posiadasz wystarczająco staminy")
            ret = -1
        else:
            # TODO zuzywa stamine czy odpowiedni zasob pasywny?
            # hero.passive[self.work_type + 1].val -= self.cost
            hero.passive[0].val -= self.cost
            hero.active_exp[self.work_type].val += self.reward

        return ret

    def upgrade(self, bohater):
        cost = Decimal(100)  # *self.level
        next_cost = Decimal(100)
        succ = False

        if bohater.riches.val > cost:  # *self.level
            bohater.riches.val -= cost
            Work.level += 1
            succ = True

        return succ, cost, next_cost, Work.level


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
    level = Decimal(1)

    def __init__(self):
        # jakie wlasciwosci, ulepszenia ma miec ta klasa?

        # przyrost na sekunde #todo kto sie orientuje cotu trzeba - passiveatribute czy currency i jaki string
        self.passive = [Currency('1', "Stamina"),
                        Currency('1', "Health"),
                        Currency('1', "Ploy"),
                        Currency('1', "Spirit"),
                        Currency('1', "Clarity")]

    # Do usuniecia?
    def onClock(self, bohater):
        counter = 0
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[i].val = bohater.passive[i].max
                counter += 1
            else:
                bohater.passive[i].val += self.passive[i].val
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
                bohater.passive[i].val += self.passive[i].val * Rest.level * Decimal(d_time)

        ret = [True if bohater.passive[i].val == Decimal(100) else False for i in range(5)]
        return ret ==[True for i in range(5)]

    def upgrade(self, bohater):
        cost = Decimal(100)  # *self.level
        next_cost = Decimal(100)
        succ = False

        if bohater.riches.val > cost:  # *self.level
            bohater.riches.val -= cost
            Rest.level += 1
            succ = True

        return succ, cost, next_cost, Rest.level


class Camp:
    # camp działa jak rest; używany w trakcie misji
    def __init__(self):
        # jakie wlasciwosci, ulepszenia ma miec ta klasa?

        # przyrost na sekunde #todo kto sie orientuje cotu trzeba - passiveatribute czy currency i jaki string
        self.passive = [Currency('0.75', "Stamina"),
                        Currency('0.75', "Health"),
                        Currency('0.75', "Ploy"),
                        Currency('0.75', "Spirit"),
                        Currency('0.75', "Clarity")]

    def onClock(self, bohater):
        counter = 0
        for i in range(5):
            if bohater.passive[i].val + self.passive[i].val >= bohater.passive[i].max:
                bohater.passive[i].val = bohater.passive[i].max
                counter += 1
            else:
                bohater.passive[i].val += self.passive[i].val
        return counter == 5
