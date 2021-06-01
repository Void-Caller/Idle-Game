import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class Message:
    gradient_error = ["#ff0000", "#ff1c0a", "#ff2a14", "#ff351b", "#ff3e22",
                      "#ff4729", "#ff4e2f", "#ff5635", "#ff5c3c", "#ff6342",
                      "#ff6948", "#ff6f4e", "#ff7554", "#ff7b5a", "#ff8060",
                      "#ff8666", "#ff8b6c", "#ff9172", "#ff9678", "#ff9b7e",
                      "#ffa184", "#ffa68b", "#ffab91", "#ffb097", "#ffb59d",
                      "#ffbaa4", "#ffbfaa", "#ffc4b0", "#ffc9b7", "#ffcebd",
                      "#ffd3c4", "#ffd8ca", "#ffddd1", "#ffe2d7", "#ffe7de",
                      "#ffebe4", "#fff0eb", "#fff5f2", "#fffaf8", "#ffffff"]
    gradient_succs = ["#78ff61", "#7eff67", "#84ff6d", "#8aff73", "#90ff78",
                      "#96ff7e", "#9bff83", "#a0ff89", "#a5ff8e", "#aaff94",
                      "#afff99", "#b3ff9e", "#b8ffa3", "#bcffa9", "#c1ffae",
                      "#c5ffb3", "#c9ffb8", "#cdffbd", "#d2ffc2", "#d6ffc7",
                      "#daffcc", "#ddffd1", "#e1ffd6", "#e5ffdc", "#e9ffe1",
                      "#edffe6", "#f1ffeb", "#f4fff0", "#f8fff5", "#fbfffa",
                      "#ffffff"]

    def __init__(self, view, text, show_time, hide_time, succ):
        self.elapsed_time = 0.0
        self.show_time = show_time
        self.hide_time = hide_time
        self.gradient = self.gradient_succs if succ else self.gradient_error

        self.label = tk.Label(view, text=text, bg=self.gradient[0], borderwidth=2, relief="groove")

    def set_grid(self, row, column):
        self.label.grid(row=row * 2, column=column, sticky="nwse", rowspan=2)

    def update(self, d_time):
        self.elapsed_time += d_time
        if self.elapsed_time > (self.show_time + self.hide_time):
            self.label.destroy()
            return True

        if self.elapsed_time > self.show_time:
            index = int((self.elapsed_time - self.show_time) / self.hide_time * len(self.gradient))
            self.label.configure(bg=self.gradient[index])

        return False


class ErrorMessage:
    def __init__(self, view):
        self.view = view
        self.messages = []
        self.waiting_messages = []

    def add_message(self, text, show_time=3, hide_time=2, succ=False):
        if len(self.messages) < 5:
            self.messages.append(Message(self.view, text, show_time, hide_time, succ))

        for i, message in enumerate(self.messages):
            message.set_grid(row=i, column=6)

    def update(self, d_time):
        for i, message in enumerate(self.messages):
            if message.update(d_time):
                self.messages.pop(i)
