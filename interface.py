import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from threading import Thread, Event
import adventure

import decimal

import data_types
from Network.client import Client
import hero
import action


class Application(tk.Tk):
    # Tutaj przekazujemy logikę
    # def __init__(self, game, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        """Konstruktor dla Application.
        Tworzy wszystkie strony oraz kontener, w którym będą one umieszczone. Ustawia
        i konfiguruje domyślne wartości, umieszcza kontener oraz strony na ekranie.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.hero = hero.Hero('Qwe')

        self.main_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_frames()
        self.show_frame("MenuView")

    def create_frames(self):
        """zainicjalizuj wszystkie strony i umieść je jedna na drugiej"""
        for F in (MenuView, GameView, GameEndView, LoginView, RegisterView, EquipmentView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # umieść wszystkie strony w tym samym miejscu
            # widoczna będzie ta strona, która jest na wierzchu
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Umieść daną stronę na wierzchu stosu, tak aby była widoczna
        Args:
            page_name: str, nazwa strony
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def reset_all(self):
        """zresetuj wszystkie strony"""
        pass

    def update_frame(self, page_name):
        """Uaktualnij daną stronę
        Args:
            page_name: str, nazwa strony
        """
        frame = self.frames[page_name]
        frame.update()


class MenuView(tk.Frame):
    def __init__(self, parent, controller):
        """Konstruktor dla MenuView.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # background:
        # bg_image = tk.PhotoImage(\
        #     file=r"C:\Users\matht\Downloads\Materiały_Monaker_UI_1\validation.png")
        # x = tk.Label(self, image=bg_image)
        # x.place(x=0, y=0, relwidth=1, relheight=1)
        # x.image = bg_image

        # some_lb = tk.Label(self, text='Menu', font=controller.main_font)
        # newGame_btn = tk.Button(self, text="New Game", font=controller.main_font,
        #                        command=lambda: controller.show_frame("GameView"))

        debug_btn = tk.Button(self, text="Debug Start", font=controller.main_font,
                              command=lambda: switch_to_game(self, controller))
        login_btn = tk.Button(self, text="Login", font=controller.main_font,
                              command=lambda: controller.show_frame("LoginView"))
        register_btn = tk.Button(self, text="Register", font=controller.main_font,
                                 command=lambda: controller.show_frame("RegisterView"))
        exitGame_btn = tk.Button(self, text="Exit", font=controller.main_font,
                                 command=lambda: exit())

        # some_lb.grid(row=2, column=2, sticky='nesw')
        debug_btn.grid(row=2, column=2, sticky='nesw')
        login_btn.grid(row=4, column=2, sticky='ew')
        register_btn.grid(row=5, column=2, sticky='ew')
        exitGame_btn.grid(row=6, column=2, sticky='ew')

        for x in range(10):
            self.rowconfigure(x, weight=1)
        for y in range(5):
            self.columnconfigure(y, weight=1)

    def update(self):
        """Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass


class GameView(tk.Frame):

    def __init_gui__(self):
        self.game_font = tkfont.Font(
            family='Helvetica', size=10, weight="bold")

        self.__init_currencies()
        self.__init_attributies()
        self.__init_passive_attributies()
        self.__init_passive_attributies_progress_bars()
        self.__init_buttons()
        self.__init_adventures()
        self.__init_challenges()

        # Koszt Ulepszenia
        self.might_upgrade_cost = tk.Label(self, text='1.00')
        self.might_upgrade_cost.grid(row=4, column=3, sticky="w")
        self.cunning_upgrade_cost = tk.Label(self, text='1.00')
        self.cunning_upgrade_cost.grid(row=5, column=3, sticky="w")
        self.psyche_upgrade_cost = tk.Label(self, text='1.00')
        self.psyche_upgrade_cost.grid(row=6, column=3, sticky="w")
        self.lore_upgrade_cost = tk.Label(self, text='1.00')
        self.lore_upgrade_cost.grid(row=7, column=3, sticky="w")

        # Status
        self.status_label = tk.Label(self, text="Idle",
                                     font=tkfont.Font(family='Helvetica', size=12, weight="bold"),
                                     anchor='center')
        self.status_label.grid(row=14, column=4, sticky="nwse", columnspan=1)

        # Hero name
        tk.Label(self, text=self.controller.hero.name,
                 font=tkfont.Font(family='Helvetica', size=12, weight="bold"),
                 anchor='center').grid(row=14, column=2, sticky="nwse", columnspan=1)
        self.hero_level_label = tk.Label(self, text="Lv " + str(self.controller.hero.level),
                                         font=tkfont.Font(family='Helvetica',
                                                          size=12, weight="bold"), anchor='center')
        self.hero_level_label.grid(row=14, column=3, sticky="nwse", columnspan=1)

        # some_lb.grid(row=0, column=0)

        for x in range(20):
            self.rowconfigure(x, weight=1)
        for y in range(7):
            self.columnconfigure(y, weight=1)

    def __init_currencies(self):
        tk.Label(self, text='Riches', bg='#ccfffc').grid(
            row=0, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Gold:', anchor='w', font=self.game_font).grid(
            row=1, column=0, sticky="nwse")
        self.gold_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.gold_value.grid(row=1, column=1, sticky="nwse")

        tk.Label(self, text='Treasures:', anchor='w', font=self.game_font).grid(
            row=2, column=0, sticky="nwse")
        self.treasures_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.treasures_value.grid(row=2, column=1, sticky="nwse")

    def __init_attributies(self):
        # Atrybuty
        tk.Label(self, text='Active', bg='#ccfffc').grid(
            row=3, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Might:', anchor='w', font=self.game_font).grid(
            row=4, column=0, sticky="nwse")
        self.might_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.might_value.grid(row=4, column=1, sticky="nwse")
        tk.Label(self, text='Cunning:', anchor='w', font=self.game_font).grid(
            row=5, column=0, sticky="nwse")
        self.cunning_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.cunning_value.grid(row=5, column=1, sticky="nwse")
        tk.Label(self, text='Psyche:', anchor='w', font=self.game_font).grid(
            row=6, column=0, sticky="nwse")
        self.psyche_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.psyche_value.grid(row=6, column=1, sticky="nwse")
        tk.Label(self, text='Lore:', anchor='w', font=self.game_font).grid(
            row=7, column=0, sticky="nwse")
        self.lore_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.lore_value.grid(row=7, column=1, sticky="nwse")

    def __init_passive_attributies(self):
        # Atrybuty
        tk.Label(self, text='Passive', bg='#ccfffc').grid(
            row=9, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Stamina:', anchor='w', font=self.game_font).grid(
            row=10, column=0, sticky="nwse")
        self.stamina_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.stamina_value.grid(row=10, column=1, sticky="nwse")
        tk.Label(self, text='Health:', anchor='w', font=self.game_font).grid(
            row=11, column=0, sticky="nwse")
        self.health_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.health_value.grid(row=11, column=1, sticky="nwse")
        tk.Label(self, text='Ploy:', anchor='w', font=self.game_font).grid(
            row=12, column=0, sticky="nwse")
        self.ploy_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.ploy_value.grid(row=12, column=1, sticky="nwse")
        tk.Label(self, text='Spirit:', anchor='w', font=self.game_font).grid(
            row=13, column=0, sticky="nwse")
        self.spirit_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.spirit_value.grid(row=13, column=1, sticky="nwse")
        tk.Label(self, text='Clarity:', anchor='w', font=self.game_font).grid(
            row=14, column=0, sticky="nwse")
        self.clarity_value = tk.Label(
            self, text="0", font=self.game_font, anchor='e')
        self.clarity_value.grid(row=14, column=1, sticky="nwse")

    def __init_passive_attributies_progress_bars(self):
        # Atrybuty Pasywne
        tk.Label(self, text='Stamina', bg='#ccfffc').grid(
            row=0, column=5, sticky="nwse", columnspan=2)
        self.stamina_prbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.stamina_prbar.grid(row=1, column=5, sticky="ew")
        tk.Label(self, text='Health', bg='#ccfffc').grid(
            row=2, column=5, sticky="nwse", columnspan=2)
        self.health_prbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.health_prbar.grid(row=3, column=5, sticky="ew")
        tk.Label(self, text='Ploy', bg='#ccfffc').grid(
            row=4, column=5, sticky="nwse", columnspan=2)
        self.ploy_prbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.ploy_prbar.grid(row=5, column=5, sticky="ew")
        tk.Label(self, text='Spirit', bg='#ccfffc').grid(
            row=6, column=5, sticky="nwse", columnspan=2)
        self.spirit_prbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.spirit_prbar.grid(row=7, column=5, sticky="ew")
        tk.Label(self, text='Clarity', bg='#ccfffc').grid(
            row=8, column=5, sticky="nwse", columnspan=2)
        self.clarity_prbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.clarity_prbar.grid(row=9, column=5, sticky="ew")

    def __init_buttons(self):
        # Buttons
        self.work_btn = tk.Button(self, text="Work", command=lambda: self.button_click(
            "Work")).grid(row=0, column=2, sticky="nwse", rowspan=2)
        self.rest_btn = tk.Button(self, text="      Rest      ", command=lambda: self.button_click(
            "Rest")).grid(row=0, column=4, sticky="nwse", rowspan=2)
        # Equipment
        self.equipment_btn = tk.Button(self, text="Equipment",
                                       command=lambda: self.controller.show_frame("EquipmentView")) \
            .grid(row=3, column=2, sticky="nwse", padx=2, pady=2)
        # Upgrade Buttons
        self.might_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train("Might")) \
            .grid(row=4, column=2, sticky="nwse", padx=2, pady=2)
        self.cunning_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train("Cunning")) \
            .grid(row=5, column=2, sticky="nwse", padx=2, pady=2)
        self.psyche_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train("Psyche")) \
            .grid(row=6, column=2, sticky="nwse", padx=2, pady=2)
        self.lore_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train("Lore")) \
            .grid(row=7, column=2, sticky="nwse", padx=2, pady=2)

        self.exit_btn = tk.Button(self, text="Logout", command=lambda: logout(self, self.controller)) \
            .grid(row=14, column=5, sticky="nwse", columnspan=3, padx=2, pady=2)
        # self.adventure_btn = tk.Button(self, text="Adventure", command=lambda: self.button_click(
        #     "Adventure")).grid(row=0, column=4, sticky="nwse", padx=2, pady=2)
        # self.challenge_btn = tk.Button(self, text="Challenge", command=lambda: self.button_click(
        #     "Challenge")).grid(row=1, column=2, sticky="nwse", padx=2, pady=2)

    def __init_adventures(self):
        # Adventures
        self.adventure_label = tk.Label(self, text='Adventures', bg='#ccfffc')
        self.adventure_label.grid(row=9, column=3, sticky="nwse", columnspan=1)

        self.adv_1_btn = tk.Button(self, text="Adventure", command=lambda: self.adv_start('Adventure', 0))
        self.adv_1_btn.grid(row=10, column=2, sticky="nwse", rowspan=2)
        self.adv_2_btn = tk.Button(self, text="Adventure", command=lambda: self.adv_start('Adventure', 1))
        self.adv_2_btn.grid(row=10, column=3, sticky="nwse", rowspan=2)
        self.adv_3_btn = tk.Button(self, text="Adventure", command=lambda: self.adv_start('Adventure', 2))
        self.adv_3_btn.grid(row=10, column=4, sticky="nwse", rowspan=2)

        self.adventures_btns = []
        self.adventures_btns.append(self.adv_1_btn)
        self.adventures_btns.append(self.adv_2_btn)
        self.adventures_btns.append(self.adv_3_btn)

        self.adventure_entry = tk.Entry(self, text='Username', font=self.game_font, width=5)
        self.adventure_entry.grid(row=12, column=3, sticky='ew')

        self.adventure_generate_btn = tk.Button(self, text="Generate",
                  command=lambda: self.generate_adventures(self.adventure_entry.get()))
        self.adventure_generate_btn.grid(row=12, column=4, sticky="nwse")

    def __init_challenges(self):
        # Challenges
        self.challenge_label = tk.Label(self, text='Adventure Challenge', bg='#ccfffc')
        self.challenge_label.grid(row=9, column=3, sticky="nwse", columnspan=1)

        self.challenge_btn = tk.Button(self, text="Test Challenge", command=lambda: self.adv_start('Challenge', 0))
        self.challenge_btn.grid(row=11, column=3, sticky="nwse", rowspan=2)

        self.challenge_progressbar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=300, mode='determinate')  # variable=?
        self.challenge_progressbar.grid(row=10, column=2, columnspan=3)
        self.challenge_progressbar.grid_remove()

        self.challenge_rem_label = tk.Label(self, text='Remaining: 5', bg='#ccfffc')
        self.challenge_rem_label.grid(row=13, column=3, sticky="nwse", columnspan=1)

        self.challenge_label.grid_remove()
        self.challenge_rem_label.grid_remove()
        self.challenge_btn.grid_remove()
        self.challenge_progressbar.grid_remove()

    def __init__(self, parent, controller):
        """Konstruktor dla GameView.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.elapsed = time.time()
        self.resting = False
        self.working = False
        self.in_adventure = False
        self.in_challenge = False
        self.active_adventure = None
        self.active_challenge = None
        self.adventures = []

        self.__init_gui__()

        self.start()
        self.refresh()
        # self.set_challenges()

    def train(self, attribute_name):
        bohater = self.controller.hero
        cost = decimal.Decimal(2) ** (bohater.get_attribute(attribute_name).val - 1)
        if cost < bohater.riches:
            bohater.train(attribute_name)
            bohater.riches -= data_types.Currency(cost, 'gold')

            self.might_upgrade_cost.config(text=large_number_format(
                decimal.Decimal(2) ** (bohater.might_base.val - 1)))
            self.cunning_upgrade_cost.config(text=large_number_format(
                decimal.Decimal(2) ** (bohater.cunning_base.val - 1)))
            self.lore_upgrade_cost.config(text=large_number_format(
                decimal.Decimal(2) ** (bohater.lore_base.val - 1)))
            self.psyche_upgrade_cost.config(text=large_number_format(
                decimal.Decimal(2) ** (bohater.psyche_base.val - 1)))

    def work_timeout(self, work):
        time.sleep(work.work_time)
        work.finish()

        self.status_label['text'] = 'Idle'
        self.working = False

    def generate_adventures(self, level):
        try:
            level = int(level)
        except ValueError:
            return
        self.adventures = []
        for i in range(3):
            self.adventures.append(adventure.Adventure(level))
            self.adventures_btns[i]['text'] = self.adventures[i].name

    def button_click(self, name):

        bohater = self.controller.hero
        if name == "Work":
            if not self.resting and not self.working:
                work = None

                if self.in_adventure:
                    work = action.Act(bohater.level)
                else:
                    work = action.Work(bohater.level)

                if not work.act(self.controller.hero):
                    return

                work_thread = Thread(target=self.work_timeout, args=(work,))
                work_thread.start()

                self.working = True
                self.status_label['text'] = 'Working'

        elif name == "Rest":
            self.resting = not self.resting
            if not self.working:
                if self.resting:
                    self.status_label['text'] = 'Resting'
                else:
                    self.status_label['text'] = 'Idle'

    def adv_start(self, type, id):

        # Hide Adventures
        self.adventure_entry.grid_remove()
        self.adventure_label.grid_remove()
        self.adventure_generate_btn.grid_remove()
        for i in range(3):
            self.adventures_btns[i].grid_remove()

        # Show Challenge
        self.challenge_label.grid()
        self.challenge_rem_label.grid()
        self.challenge_btn.grid()
        self.challenge_progressbar.grid()

    def start(self):
        self.stamina_prbar['maximum'] = self.controller.hero.stamina.max
        self.health_prbar['maximum'] = self.controller.hero.health.max
        self.ploy_prbar['maximum'] = self.controller.hero.ploy.max
        self.spirit_prbar['maximum'] = self.controller.hero.spirit.max
        self.clarity_prbar['maximum'] = self.controller.hero.clarity.max

        self.generate_adventures(1)

    def refresh(self):
        """Uaktualnij dane na stronie"""
        self.after(33, self.refresh)  # 30 fpsow

        d_time = time.time() - self.elapsed
        self.elapsed = time.time()

        if self.in_adventure:
            pass
            self.active_challenge.elapsed += d_time
            self.challenge_progressbar['value'] = self.active_challenge.elapsed

        if self.resting:
            rest = action.Rest(self.dif_level)
            rest.regeneration(self.controller.hero, d_time)

        # update text
        self.gold_value['text'] = large_number_format(
            self.controller.hero.riches.val)
        self.treasures_value['text'] = large_number_format(
            self.controller.hero.treasures.val)

        self.might_value['text'] = large_number_format(
            self.controller.hero.might.val)
        self.cunning_value['text'] = large_number_format(
            self.controller.hero.cunning.val)
        self.psyche_value['text'] = large_number_format(
            self.controller.hero.psyche.val)
        self.lore_value['text'] = large_number_format(
            self.controller.hero.lore.val)

        self.stamina_value['text'] = large_number_format(
            self.controller.hero.stamina.val)
        self.health_value['text'] = large_number_format(
            self.controller.hero.health.val)
        self.ploy_value['text'] = large_number_format(
            self.controller.hero.ploy.val)
        self.spirit_value['text'] = large_number_format(
            self.controller.hero.spirit.val)
        self.clarity_value['text'] = large_number_format(
            self.controller.hero.clarity.val)

        # update progress bar
        self.stamina_prbar['value'] = self.controller.hero.stamina.val
        self.health_prbar['value'] = self.controller.hero.health.val
        self.ploy_prbar['value'] = self.controller.hero.ploy.val
        self.spirit_prbar['value'] = self.controller.hero.spirit.val
        self.clarity_prbar['value'] = self.controller.hero.clarity.val

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass

    def set_challenges(self, clr=False):
        if clr:
            for i in range(3):
                self.challenges_btns[i].grid_remove()
                self.adventures_btns[i].grid_remove()
            self.adventure_label.grid_remove()
            self.challenge_label.grid_remove()
            self.challenge_progressbar.grid()
            return
        else:
            for i in range(3):
                self.challenges_btns[i].grid()
                self.adventures_btns[i].grid()
            self.adventure_label.grid()
            self.challenge_label.grid()
            self.challenge_progressbar.grid_remove()

        hero_lv = self.controller.hero.level

        self.challenges = []
        for i in range(3):
            self.challenges.append(adventure.Challenge(hero_lv + random.randint(0, 1)))
            string = self.challenges[i].name + "\n"
            for j in range(4):
                string = string + large_number_format(self.challenges[i].cost[j]) + ", "
            self.challenges_btns[i]['text'] = string

        self.adventures = []
        for i in range(3):
            self.adventures.append(adventure.Adventure(hero_lv + random.randint(0, 1)))
            string = self.adventures[i].name + "\n"
            for j in range(4):
                sum_stat = decimal.Decimal(0)
                for challenge in self.adventures[i].challenges:
                    sum_stat += self.challenges[i].difficulty[j]
                string = string + large_number_format(sum_stat) + " "
            self.adventures_btns[i]['text'] = string


class GameEndView(tk.Frame):
    """Okno ekranu końcowego.
    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
    """

    def __init__(self, parent, controller):
        """Konstruktor dla GameEndView.
        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        some_lb = tk.Label(self, text='Game Over', font=controller.main_font)
        MenuView_btn = tk.Button(self, text="Restart", font=controller.main_font,
                                 command=lambda: controller.show_frame("MenuView"))

        some_lb.grid(row=0, column=0)
        MenuView_btn.grid(row=1, column=0)

    def update(self):
        """Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass


class LoginView(tk.Frame):
    """Okno Logowania
    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
    """

    def __init__(self, parent, controller):
        """Konstruktor dla LoginView.
        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        login_lb = tk.Label(self, text='Login', font=controller.main_font)
        password_lb = tk.Label(self, text='Password',
                               font=controller.main_font)

        login_entry = tk.Entry(self, text='Username',
                               font=controller.main_font)
        password_entry = tk.Entry(
            self, text='Password', font=controller.main_font, show="*")

        login_btn = tk.Button(self, text='Login', font=controller.main_font,
                              command=lambda:
                              login(self, controller,
                                    login_entry.get(), password_entry.get()))
        back_btn = tk.Button(self, text="Back", font=controller.main_font,
                             command=lambda: controller.show_frame("MenuView"))

        login_lb.grid(row=1, column=2, sticky='ew')
        login_entry.grid(row=2, column=2, sticky='ew')
        password_lb.grid(row=3, column=2, sticky='ew')
        password_entry.grid(row=4, column=2, sticky='ew')

        # register_form.grid(row=2, column=2, sticky='ew')
        login_btn.grid(row=5, column=2, sticky='ew')
        back_btn.grid(row=6, column=2, sticky='ew')

        for x in range(10):
            self.rowconfigure(x, weight=1)
        for y in range(5):
            self.columnconfigure(y, weight=1)

    def update(self):
        """Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass


class RegisterView(tk.Frame):
    """Okno Logowania
    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
    """

    def __init__(self, parent, controller):
        """Konstruktor dla LoginView.
        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        client = Client().get_instance()

        login_lb = tk.Label(self, text='Login', font=controller.main_font)
        password_lb = tk.Label(self, text='Password',
                               font=controller.main_font)
        email_lb = tk.Label(self, text='Email', font=controller.main_font)

        login_entry = tk.Entry(self, text='Username',
                               font=controller.main_font, )
        password_entry = tk.Entry(self, text='Password', font=controller.main_font,
                                  show="*")
        email_entry = tk.Entry(self, text='Email', font=controller.main_font)

        register_btn = tk.Button(self, text='Register', font=controller.main_font,
                                 command=lambda: register(self, controller,
                                                          login_entry.get(), password_entry.get(), email_entry.get()))
        back_btn = tk.Button(self, text="Back", font=controller.main_font,
                             command=lambda: controller.show_frame("MenuView"))

        login_lb.grid(row=1, column=2, sticky='ew')
        login_entry.grid(row=2, column=2, sticky='ew')
        password_lb.grid(row=3, column=2, sticky='ew')
        password_entry.grid(row=4, column=2, sticky='ew')
        email_lb.grid(row=5, column=2, sticky='ew')
        email_entry.grid(row=6, column=2, sticky='ew')

        # register_form.grid(row=2, column=2, sticky='ew')
        register_btn.grid(row=7, column=2, sticky='ew')
        back_btn.grid(row=8, column=2, sticky='ew')

        for x in range(10):
            self.rowconfigure(x, weight=1)
        for y in range(5):
            self.columnconfigure(y, weight=1)

    def update(self):
        """Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass


class EquipmentView(tk.Frame):
    def __init__(self, parent, controller):
        """Konstruktor dla LoginView.
        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        back_btn = tk.Button(self, text="Back", font=controller.main_font,
                             command=lambda: controller.show_frame("GameView")).grid(row=9, column=4)

        for x in range(10):
            self.rowconfigure(x, weight=1)
        for y in range(5):
            self.columnconfigure(y, weight=1)


def login(view, controller, username, password):
    cl = Client().get_instance()
    return_value = cl.login(username, password)
    error_lb = tk.Label(
        view, text='Invalid username or password', font=controller.main_font)
    print(return_value)
    if return_value:
        switch_to_game(view, controller)
        error_lb.grid(row=0, column=2, sticky='ew')
    else:
        error_lb.grid(row=7, column=2, sticky='ew')


def register(view, controller, username, password, email):
    cl = Client().get_instance()
    return_value = cl.register(username, password, email)
    error_lb = tk.Label(view, text='Tmp', font=controller.main_font)
    if return_value == 1:
        switch_to_game(view, controller)
        error_lb.grid(row=0, column=2, sticky='ew')
        return
    elif return_value == 2:
        print("user exist")
        error_lb['text'] = 'Username already exists.'
    elif return_value == 3:
        print("email exist")
        error_lb['text'] = 'Email already exists.'

    error_lb.grid(row=9, column=2, sticky='ew')


def logout(view, controller):
    cl = Client().get_instance()
    # TODO save variables to db
    cl.logout()


def switch_to_game(view, controller):
    view.reset()
    controller.show_frame("GameView")


def large_number_format(number):
    def _round(num, div, let=''):
        return str(round(num / div, 2)) + let

    if number.__class__.__name__ == "Currency":
        number = str(number.val)

    try:
        number = decimal.Decimal(number)  # z decimal do string do int
    except ValueError as e:
        print(e)
        print(number.__class__.__name__)

    letters = ['K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx',
               'Sp', 'Oct', 'Non', 'Dec', 'Und', 'Duo']
    i = len(letters) - 1
    f = decimal.Decimal(999_999_999_999_999_999_999_999_999_999_999_999_999)
    div = decimal.Decimal(
        1_000_000_000_000_000_000_000_000_000_000_000_000_000)
    while i >= 0:
        if number > f:
            return _round(number, div, letters[i])
        f, div, i = f / 1000, div / 1000, i - 1

    return str(round(number, 2))


def main():
    # app = Application(game)
    app = Application()
    app.geometry("800x500")

    app.mainloop()


if __name__ == "__main__":
    main()
