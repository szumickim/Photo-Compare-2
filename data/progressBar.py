from tkinter import ttk
import tkinter as tk


class ClsProgress():
    def __init__(self, master, pack=True, row=0, column=0):
        # root window
        self.root = master

        # progressbar
        self.bar = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=250
        )
        self.bar.pack()

    def window_always_on_top(self):
        self.root.attributes('-topmost', True)

    def add_counter(self):
        self.counter_label_text = tk.StringVar()
        self.counter_label = tk.Label(self.root, textvariable=self.counter_label_text)
        self.counter_label.pack()

    def change_counter_label_text(self, text):
        self.counter_label_text.set(text)
        self.counter_label.pack()

    def progress(self, percent_of_progress):
        if self.bar['value'] < 100:
            self.bar['value'] = percent_of_progress
            self.root.update()

    def kill_bar(self):
        self.root.destroy()

