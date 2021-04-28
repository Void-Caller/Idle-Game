from decimal import getcontext, Decimal
import random

class CurrencyContainer:
    def __init__(self, dif_level, forclass):
        # todo generowanie treasures
        temp = ['might_exp', 'cunning_exp', 'psyche_exp', 'lore_exp']

        if forclass == 'Challenge':
            self.exp = [Currency(Decimal(random.randrange(100,300,1)/100)*dif_level[i], i) for i in range(4)]
            self.gold = Currency(Decimal(random.randrange(200,500,1)/100)*sum(dif_level), 'gold')
            self.treasures = Currency(0,'treasure')

        #nagrody 3-5 razy wieksze niz w challenge
        if forclass == 'Adventure':
            self.exp = [Currency(Decimal(random.randrange(300,1500,1)/100)*dif_level[i], i) for i in range(4)]
            self.gold = Currency(Decimal(random.randrange(600,2500,1)/100)*sum(dif_level), 'gold')
            self.treasures = Currency(0,'treasure')

        #interfejs wypisuje tylko niezerowe nagrody
        self.print_list = [i for i in self.exp if i.val > Decimal(0)]
        if self.gold.val > Decimal(0):
            self.print_list.append(self.gold)
        if self.treasures.val > Decimal(0):
            self.print_list.append(self.treasures)

    pass

class ItemContainer:
    #przechowywanie itemow do zdobycia i losowanie ich na nagrode
    #wywolanie ItemContainer(dif_level, 'challenge')
    #self.waluta = ItemContainer(dif_level, 'adventure')
    #dif_level [0,0,0,0]
    pass



class RewardChallenge:
    def __init__(self, dif_level):
        self.waluta = CurrencyContainer(dif_level, 'Challenge')
        self.eq = ItemContainer(dif_level, 'Challenge')

class RewardAdventure:
    def __init__(self, dif_level):
        self.waluta = CurrencyContainer(dif_level, 'Adventure')
        self.eq = ItemContainer(dif_level, 'Adventure')


#todo ustawienie parametrów losowania oraz
# aktualizacja wraz z postepem gry (coraz wyzsze przedzialy losowania)
# i generowanie coraz lepszych przedmiotow - tutaj czy w klasie Item????? - Lukasz wie

challenge_names = ["Wyzwanie1", "Walka z niedzwiedziem", "Przeplyniecie rzeki"]
adventure_names = ["Przygoda1", "Wyprawa w gory"]

class ObozException(Exception):
    pass

class Challenge: #wyzwanie
    def __init__(self, dif_level):
        self.name = random.choice(challenge_names);
        self.difficulty = [Decimal(random.randrange(50, 150, 1)/100)*dif_level[i] for i in range(4)]
        self.reward = RewardChallenge(self.difficulty)
        #self.type = type            #[False,False,False,False]
        self.cost = [Decimal(random.randrange(50, 100, 1)/500)*self.difficulty[i] for i in range(4)]

    def onClock(self, bohater):
        temp_list = [bohater.passive[i].actual - self.cost[i] for i in range(4)]
        for i in temp_list:
            if i<=0:
                raise ObozException
        self.difficulty = temp_list
        for i in range(4):
            if self.difficulty[i] - bohater.active[i].points > 0:
                self.difficulty[i] -= bohater.active[i].points
            else: self.difficulty[i] = 0
        return self.difficulty == [0,0,0,0] #true if completed challenge
        #todo zwracanie nagrody

class Adventure: #przygoda
    def __init__(self, dif_level):
        self.name = random.choice(adventure_names)
        self.amount = random.randint(4,20)
        self.challenges = [Challenge(dif_level) for i in range(self.amount)]
        self.challenge_index = 0
        self.in_action = False
        self.reward = RewardAdventure(dif_level)
        #todo pasek postepu przygody - gdzie? czy rzeba dodatkowe parametry initial_cost, initial_difficulty?
        #todo pasek postepu danego wyzwania - gdzie?

    def start(self):
        self.in_action = True


    # '''Zwraca bool czy bohater moze kontynuowac przygode.'''
    '''Zwraca bool czy przygoda zostala ukonczona.'''
    def onClock(self, bohater):
        if self.in_action:
            try:
                if self.challenges[self.challenge_index].onClock(bohater):
                    bohater.getChallengeReward(self.challenges[self.challenge_index].reward)
                    if self.challenge_index + 1 == self.amount:
                        self.challenge_index += 1
                        return False
                    else:
                        bohater.getAdventureReward(self.reward)
                        self.in_action = False
                        return True
            except ObozException:
                raise #do nadrzednej metody
            except Exception as e:
                print(e)
                print("ADVENTURE EXCEPTION")
        #todo zwracanie nagrody




#class Item:
#        pass



"""
Work, Act

Trening postaci odbywa się za pomocą akcji typu Work i Act z karty Main. 
Trening odbywa się dwufazowo.

	Pierwsza faza - niektóre akcje Work i Act zdobywają punkty doświadczenia
	 po każdym użyciu. Doświadczenie to jest reprezentowane jako procentowa
	  miara do następnego poziomu. Każde wykonanie akcji zwiększa ją 
	  o2%, 4% lub 10% w zależności od złożoności czynności. 
	  Gdy miara dojdzie do 100%, akcja wchodzi na nowy poziom, 
	  z wyzerowaną miarą postępu.
	  
	Faza druga - część akcji Work i Act generują waluty doświadczenia, 
	które można wykorzystać do aktywowania akcji upgrade zwiększających 
	atrybuty postaci lub na zakup umiejętności postaci z karty Skills.

"""

class Work:
    def __init__(self):
        #wg specyfikacji przygoda blokuje wszystkie akcje work
        pass

class Act:
    def __init__(self, block_on_adventure = True):
        self.block_on_adventure = block_on_adventure
        pass





class ActiveAttribute:
    #todo
    def __init__(self, nazwa, currency):
        self.name = nazwa
        self.exp_to_next_level = Decimal(0)
        self.level = Decimal(0)
        self.points = Decimal(0) #nazwa uzywana w klasie Adventure
        self.currency = Currency(currency)

class PassiveAttribute:
    #todo
    def __init__(self, nazwa, max):
        self.name = nazwa
        self.exp_to_next_level = Decimal(50)
        self.level = Decimal(0)             #trzeba ten atrybut?
        self.max = Decimal(max)
        self.actual = Decimal(max)  #nazwa uzywana w klasie Adventure

    #def increase_max(self, increment):
    #    self.max += increment



class Currency:
    #def __init__(self, amount=0):
    #    self.set = Decimal(amount)
    pass

class Bohater:
    def __init__(self):
        #waluty
        self.currency_might = Currency(0)
        self.currency_cunning = Currency(0)
        self.currency_psyche = Currency(0)
        self.currency_lore = Currency(0)
        self.treasures = Currency(0)
        self.riches = Currency(0)
        #atrybuty czynne
        self.might = ActiveAttribute('Might', self.currency_might)
        self.cunning = ActiveAttribute('Cunning', self.currency_cunning)
        self.psyche = ActiveAttribute('Psyche', self.currency_psyche)
        self.lore = ActiveAttribute('Lore', self.currency_lore)
        #atrybuty pasywne
        self.stamina = PassiveAttribute('Stamina')
        self.health = PassiveAttribute('Health')
        self.ploy = PassiveAttribute('Ploy')
        self.spirit = PassiveAttribute('Spirit')
        self.clarity = PassiveAttribute('Clarity')
        #potrzebne sa listy z referencjami do atrybutow czynnych i pasywne, najlepiej z uwzglednionymi bonusami, modyfikatorami
        self.passive = [self.might, self.cunning, self.psyche, self.lore]
        self.active = [self.stamina, self.health, self.ploy, self.spirit, self.clarity]

    def getChallengeReward(self, challenge_reward):
        #otrzymanie nagrody za ukonczony challenge, nazwa metody taka?? uzyta w klasie Adventura
        pass

    def getAdventureReward(self, adventure_reward):
        pass



#trik przekazywanie wartosci przez referencje
'''
class x:
    def __init__(self):
        self.q=1
a = x()
b = [a]
a.q = 2
print(a.q)
print(b[0].q)
b[0].q=3
print(a.q)
print(b[0].q)

wynik 2 2 3 3
'''

def main():


if __name__ == "__main__":
    main()

    