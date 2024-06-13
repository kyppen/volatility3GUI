import tkinter as tk
from tkinter import ttk
import random
import utils



class TextWithLineNumbers(tk.Frame):
    #adds index to the left of output field
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.text = tk.Text(self, wrap='word', height=30, width=200, undo=True)
        self.line_numbers = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                   state='disabled')

        self.line_numbers.grid(row=0, column=0, sticky='ns')
        self.text.grid(row=0, column=1, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.scrollbar = ttk.Scrollbar(self, command=self.on_scrollbar)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.on_text_scroll)
        self.line_numbers.config()

        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.on_mouse_wheel)
        self.text.bind('<Button-1>', self.sync_scroll)
        self.text.bind('<ButtonRelease-1>', self.sync_scroll)
        self.text.bind('<Configure>', self.sync_scroll)

        self.line_numbers.bind('<MouseWheel>', lambda e: 'break')
        self.line_numbers.bind('<Button-4>', lambda e: 'break')
        self.line_numbers.bind('<Button-5>', lambda e: 'break')

        self.update_line_numbers()


    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')

        line_count = int(self.text.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

    def sync_scroll(self, *args):
        self.line_numbers.yview_moveto(self.text.yview()[0])

    def on_scrollbar(self, *args):
        self.text.yview(*args)
        self.sync_scroll()

    def set_ui_color(self):
        hex_color = utils.generate_hex_color()
        print(hex_color)
        contrast_color = utils.yiq_contrast_color(hex_color)
        self.text.config(background=hex_color)
        self.text.config(fg=contrast_color)
        print(contrast_color)

        hex_color2 = utils.generate_hex_color()
        contrast_color2 = utils.yiq_contrast_color(hex_color2)
        self.line_numbers.config(background=hex_color2, fg=contrast_color2)
    def set_ui_color_white(self):
        self.text.config(fg="#000000",background="#d0d3d4")
        self.line_numbers.config(fg="#000000",background="#d0d3d4")
    def set_ui_dark_color(self):
        self.text.config(fg="#FFFFFF", background="#3e3e42")
        self.line_numbers.config(fg="#FFFFFF", background="#3e3e42")
    def on_text_scroll(self, *args):
        self.sync_scroll()
        self.scrollbar.set(*args)

    def on_mouse_wheel(self, event):
        self.text.yview_scroll(int(-1*(event.delta/120)), 'units')
        self.sync_scroll()
        return 'break'