#import interfejs as gui
import tkinter as tk
import adventure
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
        #flagi
        self.at_work = False
        self.at_act = False
        self.at_rest = False
        self.at_adventure = False

        self.at_camp = False


        #referencja do bohatera
        self.bohater = hero.Hero("Qw")

        #tablica na przygody do rozpoczecia, w trakcie wykonywania, ukonczone
        self.available_adventures = [] #usuwamy czy chcemy?
        self.adventure = [adventure.Adventure([0,0,0,0]) for i in range(4)]
        self.completedAdventures = []

        #timer
        self.clock_started = False
        self.continue_clock = False
        self.drop_timers = 0
        self.seconds = 0
        self.gui = Inter(self)
        self.gui.mainloop()
        #referencja do interfejsu
        #self.gui = gui

    #trzeba wywolac z interfejsu gdy chcemy zaczac gre
    def set_clock(self):
        if not self.clock_started:
            self.clock_started = True
            if not self.drop_timers:
                self.continue_clock = True
            #self.clock_working = True
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
        #if self.at_rest:
        #    pass
        if self.at_adventure:
            try:
                for i in self.adventure:
                    if i.onClock(self.bohater):
                        self.adventure.remove(i)
                        i.in_action = False
                        self.completedAdventures.append(i)
            except adventure.CampException:
                for i in self.adventure:
                    i.in_action = False
                self.at_adventure = False
                self.at_camp = True
                #akcja camp
        #przykladowe zwracanie czasu gry - przerobic na nasz  interfejs
        self.gui.set_title(self.seconds)

if __name__ == '__main__':
    start = Main()

