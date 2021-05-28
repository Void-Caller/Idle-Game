import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
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
        for F in (MenuView, GameView, GameEndView, LoginView, RegisterView):
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
    def __init__(self, parent, controller):
        """Konstruktor dla GameView.
        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.entry_label_font = tkfont.Font(
        #    family='Helvetica', size=12, weight='bold')

        #  Pomocniczne zmienne
        self.stamina = float(5)
        #
        self.game_font = tkfont.Font(
            family='Helvetica', size=10, weight="bold")

        some_lb = tk.Label(self, text='Game', font=controller.main_font)

        tk.Label(self, text='Riches', bg='#ccfffc').grid(row=0, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Gold:', anchor='w', font=self.game_font).grid(row=1, column=0, sticky="nwse")
        self.gold_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.gold_value.grid(row=1, column=1, sticky="nwse")

        tk.Label(self, text='Treasures:', anchor='w', font=self.game_font).grid(row=2, column=0, sticky="nwse")
        self.treasures_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.treasures_value.grid(row=2, column=1, sticky="nwse")

        # Atrybuty
        tk.Label(self, text='Active', bg='#ccfffc').grid(row=3, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Might:', anchor='w', font=self.game_font).grid(row=4, column=0, sticky="nwse")
        self.might_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.might_value.grid(row=4, column=1, sticky="nwse")
        tk.Label(self, text='Cunning:', anchor='w', font=self.game_font).grid(row=5, column=0, sticky="nwse")
        self.cunning_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.cunning_value.grid(row=5, column=1, sticky="nwse")
        tk.Label(self, text='Psyche:', anchor='w', font=self.game_font).grid(row=6, column=0, sticky="nwse")
        self.psyche_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.psyche_value.grid(row=6, column=1, sticky="nwse")
        tk.Label(self, text='Lore:', anchor='w', font=self.game_font).grid(row=7, column=0, sticky="nwse")
        self.lore_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.lore_value.grid(row=7, column=1, sticky="nwse")

        # Atrybuty
        tk.Label(self, text='Passive', bg='#ccfffc').grid(row=9, column=0, sticky="nwse", columnspan=2)

        tk.Label(self, text='Stamina:', anchor='w', font=self.game_font).grid(row=10, column=0, sticky="nwse")
        self.stamina_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.stamina_value.grid(row=10, column=1, sticky="nwse")
        tk.Label(self, text='Health:', anchor='w', font=self.game_font).grid(row=11, column=0, sticky="nwse")
        self.health_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.health_value.grid(row=11, column=1, sticky="nwse")
        tk.Label(self, text='Ploy:', anchor='w', font=self.game_font).grid(row=12, column=0, sticky="nwse")
        self.ploy_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.ploy_value.grid(row=12, column=1, sticky="nwse")
        tk.Label(self, text='Spirit:', anchor='w', font=self.game_font).grid(row=13, column=0, sticky="nwse")
        self.spirit_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.spirit_value.grid(row=13, column=1, sticky="nwse")
        tk.Label(self, text='Clarity:', anchor='w', font=self.game_font).grid(row=14, column=0, sticky="nwse")
        self.clarity_value = tk.Label(self, text="0", font=self.game_font, anchor='e')
        self.clarity_value.grid(row=14, column=1, sticky="nwse")

        # self.treasures_value['text'] = large_number_format('99955479574157')
        # error_lb['text']

        tk.Label(self, text='Stamina', bg='#ccfffc').grid(row=0, column=5, sticky="nwse", columnspan=2)
        self.stamina_prbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.stamina_prbar.grid(row=1, column=5, sticky="ew")

        tk.Label(self, text='Health', bg='#ccfffc').grid(row=2, column=5, sticky="nwse", columnspan=2)
        self.health_prbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.health_prbar.grid(row=3, column=5, sticky="ew")

        tk.Label(self, text='Ploy', bg='#ccfffc').grid(row=4, column=5, sticky="nwse", columnspan=2)
        self.ploy_prbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.ploy_prbar.grid(row=5, column=5, sticky="ew")

        tk.Label(self, text='Spirit', bg='#ccfffc').grid(row=6, column=5, sticky="nwse", columnspan=2)
        self.spirit_prbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.spirit_prbar.grid(row=7, column=5, sticky="ew")

        tk.Label(self, text='Clarity', bg='#ccfffc').grid(row=8, column=5, sticky="nwse", columnspan=2)
        self.clarity_prbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')  # variable=?
        self.clarity_prbar.grid(row=9, column=5, sticky="ew")

        activity_names = ["Work", "Rest", "Adventure", "Challenge"]
        self.activity_btns = []
        for i in range(len(activity_names)):
            b = tk.Button(self, text=activity_names[i])
            self.activity_btns.append(b)

        cols = 3
        rows = len(self.activity_btns) // cols + (len(self.activity_btns) % cols > 0)
        for i in range(len(self.activity_btns)):
            c = i % cols + 2
            r = i // cols
            self.activity_btns[i].grid(
                row=r, column=c, sticky="nwse", padx=2, pady=2)

        # some_lb.grid(row=0, column=0)

        for x in range(20):
            self.rowconfigure(x, weight=1)
        for y in range(10):
            self.columnconfigure(y, weight=1)
        self.start()
        self.refresh()

    def start(self):
        self.stamina_prbar['maximum'] = self.controller.hero.stamina.max
        self.health_prbar['maximum'] = self.controller.hero.health.max
        self.ploy_prbar['maximum'] = self.controller.hero.ploy.max
        self.spirit_prbar['maximum'] = self.controller.hero.spirit.max
        self.clarity_prbar['maximum'] = self.controller.hero.clarity.max


    def refresh(self):
        """Uaktualnij dane na stronie"""
        self.after(33, self.refresh)  # 30 fpsow
        # rest = action.Rest([1, 1, 1, 1])
        # rest.regeneration(self.controller.hero)

        # update text
        self.stamina_value['text'] = str(self.controller.hero.stamina.val)
        self.health_value['text'] = str(self.controller.hero.health.val)
        self.ploy_value['text'] = str(self.controller.hero.ploy.val)
        self.spirit_value['text'] = str(self.controller.hero.spirit.val)
        self.clarity_value['text'] = str(self.controller.hero.clarity.val)
        # update progress bar
        self.stamina_prbar['value'] = float(self.controller.hero.stamina.val)
        self.health_prbar['value'] = float(self.controller.hero.health.val)
        self.ploy_prbar['value'] = float(self.controller.hero.ploy.val)
        self.spirit_prbar['value'] = float(self.controller.hero.spirit.val)
        self.clarity_prbar['value'] = float(self.controller.hero.clarity.val)

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
        password_lb = tk.Label(self, text='Password', font=controller.main_font)

        login_entry = tk.Entry(self, text='Username', font=controller.main_font)
        password_entry = tk.Entry(self, text='Password', font=controller.main_font, show="*")

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
        password_lb = tk.Label(self, text='Password', font=controller.main_font)
        email_lb = tk.Label(self, text='Email', font=controller.main_font)

        login_entry = tk.Entry(self, text='Username', font=controller.main_font, )
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


def login(view, controller, username, password):
    cl = Client().get_instance()
    return_value = cl.login(username, password)
    error_lb = tk.Label(view, text='Invalid username or password', font=controller.main_font)
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


def switch_to_game(view, controller):
    view.reset()
    controller.show_frame("GameView")


def large_number_format(number):
    def _round(num, div, let=''):
        return str(round(num / div, 2)) + let

    number = int(str(number))  # z decimal do string do int

    letters = ['K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oct', 'Non', 'Dec', 'Und', 'Duo']
    i = len(letters) - 1
    f = 999_999_999_999_999_999_999_999_999_999_999_999_999
    div = 1_000_000_000_000_000_000_000_000_000_000_000_000_000
    while i >= 0:
        if number > f:
            return _round(number, div, letters[i])
        f, div, i = f // 1000, div // 1000, i - 1

    return number


def main():
    # app = Application(game)
    app = Application()
    app.geometry("800x500")

    app.mainloop()


if __name__ == "__main__":
    main()
