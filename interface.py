import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from MessagesQueue import ErrorMessage
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
        # self.__init_passive_attributies_progress_bars()
        self.__init_buttons()
        self.__init_adventures()
        self.__init_challenges()

        # Koszt Ulepszenia
        self.might_upgrade_cost = tk.Label(self, text='1.00')
        self.might_upgrade_cost.grid(row=4, column=2, sticky="e", padx=5)
        self.cunning_upgrade_cost = tk.Label(self, text='1.00')
        self.cunning_upgrade_cost.grid(row=5, column=2, sticky="e", padx=5)
        self.psyche_upgrade_cost = tk.Label(self, text='1.00')
        self.psyche_upgrade_cost.grid(row=6, column=2, sticky="e", padx=5)
        self.lore_upgrade_cost = tk.Label(self, text='1.00')
        self.lore_upgrade_cost.grid(row=7, column=2, sticky="e", padx=5)

        self.costs_labels = []
        self.costs_labels.append(self.might_upgrade_cost)
        self.costs_labels.append(self.cunning_upgrade_cost)
        self.costs_labels.append(self.psyche_upgrade_cost)
        self.costs_labels.append(self.lore_upgrade_cost)

        # init upgrades cost
        for i in range(4):
            self.train(i)
        self.messages.clear()

        # Status
        self.status_label = tk.Label(self, text="Idle",
                                     font=tkfont.Font(family='Helvetica', size=12, weight="bold"),
                                     anchor='center')
        self.status_label.grid(row=14, column=4, sticky="nwse", columnspan=1)

        # Hero name
        tk.Label(self, text=self.controller.hero.name,
                 font=tkfont.Font(family='Helvetica', size=12, weight="bold"),
                 anchor='center').grid(row=14, column=2, sticky="nwse", columnspan=1)

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

        self.active = []
        self.active.append(self.might_value)
        self.active.append(self.cunning_value)
        self.active.append(self.psyche_value)
        self.active.append(self.lore_value)

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

        self.passive = []
        self.passive.append(self.stamina_value)
        self.passive.append(self.health_value)
        self.passive.append(self.ploy_value)
        self.passive.append(self.spirit_value)
        self.passive.append(self.clarity_value)

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

        self.passive_bars = []
        self.passive_bars.append(self.stamina_prbar)
        self.passive_bars.append(self.health_prbar)
        self.passive_bars.append(self.ploy_prbar)
        self.passive_bars.append(self.spirit_prbar)
        self.passive_bars.append(self.clarity_prbar)

    def __init_buttons(self):
        # Buttons
        tk.Button(self, text="Work", command=lambda: self.button_click("Work", 0)).grid(row=4, column=3, sticky="nwse")
        tk.Button(self, text="Work", command=lambda: self.button_click("Work", 1)).grid(row=5, column=3, sticky="nwse")
        tk.Button(self, text="Work", command=lambda: self.button_click("Work", 2)).grid(row=6, column=3, sticky="nwse")
        tk.Button(self, text="Work", command=lambda: self.button_click("Work", 3)).grid(row=7, column=3, sticky="nwse")

        # self.work_btn = tk.Button(self, text="Work", command=lambda: self.button_click(
        #     "Work", 0)).grid(row=3, column=4, sticky="nwse")
        # self.work_btn = tk.Button(self, text="Work", command=lambda: self.button_click(
        #     "Work", 0)).grid(row=3, column=4, sticky="nwse")

        self.rest_btn = tk.Button(self, text="      Rest      ", command=lambda: self.button_click(
            "Rest")).grid(row=0, column=4, sticky="nwse", rowspan=2)
        # Equipment
        self.equipment_btn = tk.Button(self, text="Equipment",
                                       command=lambda: self.controller.frames["EquipmentView"].show_frame()) \
            .grid(row=0, column=2, sticky="nwse", padx=2, pady=2, rowspan=2)

        self.upgrade_work = tk.Button(self, text="Upgrade Work\n(100 gold)",
                                       command=lambda: self.upgrade_action("Work"))
        self.upgrade_work.grid(row=2, column=2, sticky="nwse", padx=2, pady=2, rowspan=2)

        self.upgrade_rest = tk.Button(self, text="Upgrade Rest\n(100 gold)",
                                       command=lambda: self.upgrade_action("Rest"))
        self.upgrade_rest.grid(row=2, column=4, sticky="nwse", padx=2, pady=2, rowspan=2)

        # Upgrade Buttons
        self.might_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train(0)) \
            .grid(row=4, column=2, sticky="nwse", padx=2, pady=2)
        self.cunning_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train(1)) \
            .grid(row=5, column=2, sticky="nwse", padx=2, pady=2)
        self.psyche_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train(2)) \
            .grid(row=6, column=2, sticky="nwse", padx=2, pady=2)
        self.lore_upgrade_btn = tk.Button(self, text="Train", command=lambda: self.train(3)) \
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

        self.challenge_btn = tk.Button(self, text="Test Challenge", command=lambda: self.do_challenge())
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
        self.messages = ErrorMessage(self)

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.elapsed = time.time()
        self.resting = False
        self.working = False
        self.in_adventure = False
        self.in_challenge = False

        self.active_work = None
        self.active_adventure = None
        self.active_challenge = None
        self.adventures = []

        self.__init_gui__()

        self.start()
        self.refresh()
        # self.set_challenges()

    def train(self, index):
        attr = ["Might", "Cunning", "Psyche", "Lore"]
        bohater = self.controller.hero
        succ, cost, next_cost, value = bohater.train(index)
        self.costs_labels[index].config(text="({})".format(next_cost))
        if succ:
            self.messages.add_message("Training successful\nYou gain {} {}.\n-{} {} exp.".format(
                large_number_format(value), attr[index], cost, attr[index]
            ), succ=True)
        else:
            self.messages.add_message("You don't have\nenough exp.")

    def generate_adventures(self, level):
        try:
            level = int(level)
            if level <= 0:
                return
        except ValueError:
            return

        self.adventures = []
        stats = []
        for i in range(4):
            stats.append(self.controller.hero.active[i].val)

        pattern = "{} - {}\n{} | {} | {} | {}"
        for i in range(3):
            self.adventures.append(adventure.Adventure([level for i in range(4)]))
            cost = self.adventures[i].get_total_costs()
            for j in range(4):
                cost[j] = large_number_format(cost[j])
            self.adventures_btns[i]['text'] = pattern.format(self.adventures[i].name,
                                                             self.adventures[i].get_remaining_challenges(),
                                                             *cost)

    def button_click(self, name, btn_id=-1):

        if name == "Work":
            if not self.resting and not self.working:
                self.active_work = action.Work(self.controller.hero, btn_id)

                self.working = True
                self.status_label['text'] = 'Working'

            if self.resting:
                self.messages.add_message("You can't Work\nwhile resting.")
            if self.in_challenge:
                self.messages.add_message("You can't Work\nwhile in challenge.")

        elif name == "Rest":
            if not self.working and not self.in_challenge:
                self.resting = not self.resting
                if self.resting:
                    self.status_label['text'] = 'Resting'
                else:
                    if self.in_adventure:
                        self.status_label['text'] = 'In Adventure'
                    else:
                        self.status_label['text'] = 'Idle'
            if self.working:
                self.messages.add_message("You can't Rest\nwhile working.")
            if self.in_challenge:
                self.messages.add_message("You can't Rest\nwhile in challenge.")

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

        self.active_adventure = self.adventures[id]
        self.set_next_challenge(True)
        # Set Text

    def adv_end(self):
        # Show Adventures
        self.adventure_entry.grid()
        self.adventure_label.grid()
        self.adventure_generate_btn.grid()
        for i in range(3):
            self.adventures_btns[i].grid()

        # Hide Challenge
        self.challenge_label.grid_remove()
        self.challenge_rem_label.grid_remove()
        self.challenge_btn.grid_remove()
        self.challenge_progressbar.grid_remove()

        self.active_challenge = None
        self.active_adventure = None
        self.in_challenge = False
        self.in_adventure = False

        self.generate_adventures(1)

    def set_next_challenge(self, start=False):
        if not start:
            self.active_adventure.challenge_index += 1

        self.challenge_rem_label['text'] = "Remaining Challenges: {}".format(
            self.active_adventure.get_remaining_challenges())

        if self.active_adventure.challenge_index + 1 > len(self.active_adventure.challenges):
            self.claim_reward(self.active_adventure)
            self.adv_end()
            return

        challenge = self.active_adventure.challenges[self.active_adventure.challenge_index]

        cost = challenge.get_cost()
        for i in range(4):
            cost[i] = large_number_format(cost[i])
        chall_time = large_number_format(challenge.get_time(self.controller.hero))
        self.challenge_btn['text'] = "{}\ncost: {}|{}|{}|{}\ntime: {}".format(challenge.name, *cost, chall_time)
        self.challenge_progressbar['value'] = 0

    def do_challenge(self):
        if self.active_challenge is not None or self.in_challenge:
            return

        if self.working:
            self.messages.add_message("You cant't start\n challenge while\nworking.")
            return

        if self.resting:
            self.messages.add_message("You cant't start\n challenge while\nresting.")
            return

        bohater = self.controller.hero

        challenge = self.active_adventure.challenges[self.active_adventure.challenge_index]
        if challenge.can_hero_start(bohater):
            self.in_challenge = True
            self.status_label['text'] = 'In Challenge'
            self.challenge_progressbar['maximum'] = int(challenge.progress_maximum)
            self.active_challenge = challenge
        else:
            self.messages.add_message("You don't have\n enough attributes\nto start this challenge.")

    def claim_reward(self, quest):
        bohater = self.controller.hero

        text = "{} completed\nexp: ({}, {}, {}, {})\nGold: {}"
        exps = []
        for i in range(4):
            bohater.active_exp[i].val += quest.reward.waluta.exp[i]
            exps.append(large_number_format(quest.reward.waluta.exp[i]))

        bohater.riches += quest.reward.waluta.riches
        bohater.treasures += quest.reward.waluta.treasures
        self.messages.add_message(text.format(quest.__class__.__name__, *exps,
                                              large_number_format(quest.reward.waluta.riches)), succ=True)

        for item in quest.reward.getItems():
            self.messages.add_message("You found Item\n{}\n{}".format(item.type, item.name), succ=True)
            bohater.eq.addItem(item)

    def upgrade_action(self, action_name):
        bohater = self.controller.hero
        if action_name == "Work":
            succ, cost, next_cost, level = action.Work(bohater).upgrade(bohater)
            print(action.Work.level)
            if succ:
                self.upgrade_work.config(text="Upgrade Work\n({} gold)".format(next_cost))
        elif action_name == "Rest":
            succ, cost, next_cost, level = action.Rest().upgrade(bohater)
            if succ:
                self.upgrade_rest.config(text="Upgrade Rest\n({} gold)".format(next_cost))

        if succ:
            self.messages.add_message("{} upgraded\nto level {}.\n-{} gold.".format(action_name, level, cost), succ=True)
        else:
            self.messages.add_message("You need {} gold\nto upgrade {}.".format(cost, action_name))

    def start(self):
        # self.stamina_prbar['maximum'] = self.controller.hero.passive[0].max
        # self.health_prbar['maximum'] = self.controller.hero.passive[1].max
        # self.ploy_prbar['maximum'] = self.controller.hero.passive[2].max
        # self.spirit_prbar['maximum'] = self.controller.hero.passive[3].max
        # self.clarity_prbar['maximum'] = self.controller.hero.passive[4].max

        self.generate_adventures(1)

    def refresh(self):
        """Uaktualnij dane na stronie"""
        self.after(33, self.refresh)  # 30 fpsow

        d_time = time.time() - self.elapsed
        self.elapsed = time.time()

        self.messages.update(d_time)
        if self.resting:
            rest = action.Rest()
            if rest.update(self.controller.hero, d_time):
                self.button_click("Rest")
                self.messages.add_message("Rest completed.", succ=True)
        if self.working:
            ret = self.active_work.update(self.controller.hero, d_time, self.active_adventure);
            if ret != 0:
                self.active_work = None
                self.working = False
                if ret == 1:
                    self.messages.add_message("Work Ended", succ=True)
                else:
                    self.messages.add_message("Not enough stamina for end work.")

        if self.in_challenge:
            if not self.working and not self.resting:
                if self.in_challenge:
                    if self.active_challenge.update(self.controller.hero, d_time):
                        self.claim_reward(self.active_challenge)
                        self.in_challenge = False
                        self.active_challenge = None
                        self.status_label['text'] = 'In Adventure'
                        self.set_next_challenge()
                    else:
                        self.challenge_progressbar['value'] = int(self.active_challenge.progress_current)

        # update text
        self.gold_value['text'] = large_number_format(self.controller.hero.riches.val)
        self.treasures_value['text'] = large_number_format(self.controller.hero.treasures.val)

        for i in range(4):
            self.active[i]['text'] = "{} ({})".format(large_number_format(self.controller.hero.active[i].val),
                                                      large_number_format(self.controller.hero.active_exp[i].val))

        for i in range(5):
            self.passive[i]['text'] = large_number_format(self.controller.hero.passive[i].val)
            # self.passive_bars[i]['value'] = self.controller.hero.passive[i].val

    def reset(self):
        """Zresetuj stronę do stanu początkowego"""
        pass


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
        self.elapsed = time.time()
        self.messages = ErrorMessage(self)

        self.item_string = "{}\n{}\nReq: {}M {}C {}P {}L\n+{}M +{}C +{}P +{}L"  # Name / slot/ Might / Cunning / Psyche / lore
        self.items_btns = []

        attr_names = attr_names = ["Might:", "Cunning:", "Psyche:", "Lore:"]
        self.hero_attr_names = [tk.Label(self, bg=('#ccfffc' if i % 2 else '#ccfccc'), borderwidth=2, relief="groove",
                                         text=attr_names[i]) for i in range(4)]
        self.hero_attr_values = [tk.Label(self, bg=("#ccfffc" if i % 2 else "#ccfccc"), borderwidth=2, relief="groove",
                                          ) for i in range(4)]

        slot_names = ["Weapon:", "Helmet:", "Armor:", "Ring:"]
        self.hero_items_names = [tk.Label(self, bg=('#ccfffc' if i % 2 else '#ccfccc'), borderwidth=2, relief="groove",
                                          text=slot_names[i]) for i in range(4)]
        self.hero_items_equipped = [
            tk.Label(self, bg=("#ccfffc" if i % 2 else "#ccfccc"), borderwidth=2, relief="groove",
                     text='None') for i in range(4)]

        for i, label in enumerate(self.hero_attr_names):
            label.grid(row=i, column=0, sticky="nwse")

        for i, label in enumerate(self.hero_attr_values):
            label.grid(row=i, column=1, sticky="nwse")

        for i, label in enumerate(self.hero_items_names):
            label.grid(row=5 + i, column=0, sticky="nwse")

        for i, label in enumerate(self.hero_items_equipped):
            label.grid(row=5 + i, column=1, sticky="nwse")

        tk.Button(self, text="Back", font=controller.main_font,
                  command=lambda: controller.show_frame("GameView")).grid(
            row=9, column=0, columnspan=2, sticky="nwse", padx=20, pady=20)

        for x in range(10):
            self.rowconfigure(x, weight=1)
        for y in range(10):
            self.columnconfigure(y, weight=1)

        self.refresh()

    def refresh(self):
        self.after(33, self.refresh)  # 30 fpsow

        d_time = time.time() - self.elapsed
        self.elapsed = time.time()

        self.messages.update(d_time)

    def show_frame(self):
        self.controller.show_frame("EquipmentView")
        self.update_informations()

    def update_informations(self):
        # Update Stats
        for i, label in enumerate(self.hero_attr_values):
            label['text'] = large_number_format(self.controller.hero.active[i])

        # Update Items
        for i, label in enumerate(self.hero_items_equipped):
            item = self.controller.hero.set[i]
            text = 'None'
            if item:
                item_attr = [attr.val for attr in item.item_attr]
                text = self.item_string.format(item.name, item.type, *item.min_attr, *item_attr)
            label['text'] = text

        # Update bags
        # Delete old items
        for item_btns in self.items_btns:
            item_btns.destroy()

        for i, eq_item in enumerate(self.controller.hero.eq.all_items):
        # for i in range(5):
        #     eq_item = hero.Item("fNazwa przedmiotu", 'Weapon', minimum=[1, 1, 1, 1], m=5, c=6, p=7, l=8)

            item_attr = [attr.val for attr in eq_item.item_attr]
            text = self.item_string.format(eq_item.name, eq_item.type, *eq_item.min_attr, *item_attr)

            # button = tk.Button(self, text=text, command=lambda: self.equip_item(i))
            button = tk.Button(self, text=text)
            button.extra = i
            button.grid(row=i // 4, column=3 + i % 4)
            button.bind("<Button-1>", self.equip_item)
            button.bind("<Button-3>", self.sell_item)  # Button-3 => Right Mouse Button
            self.items_btns.append(button)

    def equip_item(self, event): # TODO MOZE RZUCIC WYJATEK
        item_id = event.widget.extra
        self.controller.hero.equip(item_id)
        self.update_informations()

    def sell_item(self, event):
        item_id = event.widget.extra
        info = self.controller.hero.sell(item_id)
        self.messages.add_message("You sold\n{}\nfor {} gold.".format(*info), succ=True)
        self.update_informations()


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
