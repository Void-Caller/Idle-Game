#import interfejs as gui
from decimal import Decimal
import tkinter as tk
from adventure import *
from action import *
import hero

class Inter(tk.Tk):
    def __init__(self, main):
        tk.Tk.__init__(self)
        self.x = main
        self.geometry("500x400")
        self._panellewy = tk.Frame(self, bg='blue', width=160, height=400, padx=3, pady=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._panellewy.grid(row=0, sticky="nsw")
        self._panellewy.grid_propagate(0)

        self._bstart = tk.Button(self._panellewy, text="start", command=lambda: self.x.set_clock())
        self._bstart2 = tk.Button(self._panellewy, text="stop", command=lambda: self.x.stop_clock())
        self._bstart.grid(row=0, padx=3, pady=3, rowspan=2)
        self._bstart2.grid(row=3, padx=3, pady=3, rowspan=2)
        #self.mainloop()

    def set_title(self,seconds):
        self.title("{}".format(seconds))

class Main():
    def __init__(self):
        #flagi bohatera - byc moze powinny byc utworzone w bohaterze
        self.at_work = False
        self.at_rest = False
        self.at_adventure = False
        self.at_camp = False

        #referencja do bohatera
        self.bohater = hero.Hero("Qw")

        #tablica na przygody i prace aktualne i ukonczone
        self.current_adventure = Adventure([Decimal(0),Decimal(0),Decimal(0),Decimal(0)])
        self.current_work = Work([Decimal(0),Decimal(0),Decimal(0),Decimal(0)])
        self.rest = Rest()
        self.camp = Camp()

        self.completedAdventures = []
        self.completedWorks = []



        self.preparedAdventures = []
        self.completedWorks = []

        #timer
        self.clock_started = False
        self.continue_clock = False
        self.drop_timers = 0
        self.seconds = 0
        self.gui = Inter(self)
        self.gui.mainloop()

    #trzeba wywolac z interfejsu gdy chcemy zaczac gre
    def set_clock(self):
        if not self.clock_started:
            self.clock_started = True
            if not self.drop_timers:
                self.continue_clock = True
            self.gui.after(1000, self.update_clock)

    def stop_clock(self):
        if self.clock_started:
            self.clock_started = False
            self.continue_clock = False
            self.drop_timers +=1



    def update_clock(self):
        if not self.continue_clock:
            self.drop_timers -= 1
            if self.drop_timers == 0:
                self.continue_clock = True
            return
        self.seconds += 1
        self.gui.after(1000, self.update_clock)

        #rest na zyczenie gracza lub w ramach worka po zmeczeniu
        if self.at_rest:
            if self.rest.onClock(self.bohater):
                self.at_rest = False

        elif self.at_work:
            try:
                if self.current_work.onClock(self.bohater):
                    self.completedWorks.append(self.current_work)
                    self.at_work = False
            except RestException:
                self.at_rest = True

        elif self.at_camp:
            if self.camp.onClock(self.bohater):
                self.at_camp = False

        elif self.at_adventure:
            try:
                if self.current_adventure.onClock(self.bohater):
                    self.completedAdventures.append([self.current_adventure.name, self.current_adventure.dif_level])
                    self.at_adventure = False
            except CampException:
                self.at_camp = True

        #przykladowe zwracanie czasu gry - przerobic na nasz  interfejs
        self.gui.set_title(self.seconds)



#-----------------przykladowe funkcje-------------------------------


    def prepareAdventures(self):
        #pobrac z interfejsu wpisane wartosci dif_level
        dif_level = [1,2,3,4]
        self.preparedAdventures = [Adventure(dif_level) for i in range(3)]

    def startAdventure(self, index):
        if self.at_adventure or self.at_work:
            #return false
            pass
        self.current_adventure = self.preparedAdventures[index]
        self.at_adventure = True
        #z pozostalymi przygodami robcie co chcecie, co latwiej
        self.preparedAdventures = []




if __name__ == '__main__':
    start = Main()

