import tkinter as tk
from tkinter import ttk
import utils

class TextWithLineNumbers(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.text = tk.Text(self, wrap='word', height=30, width=1, undo=True)
        self.line_numbers_left = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                    state='disabled')
        self.line_numbers_right = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                    state='disabled')
        self.text.grid(row=0, column=1, sticky='nsew')
        self.line_numbers_right.grid(row=0, column=0, sticky='ns')
        self.line_numbers_left.grid(row=0, column=4, sticky='ns')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.scrollbar = ttk.Scrollbar(self, command=self.on_scrollbar)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.on_text_scroll)

        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.on_mouse_wheel)
        self.text.bind('<Button-1>', self.sync_scroll)
        self.text.bind('<ButtonRelease-1>', self.sync_scroll)
        self.text.bind('<Configure>', self.sync_scroll)

        self.line_numbers_right.bind('<MouseWheel>', lambda e: 'break')
        self.line_numbers_right.bind('<Button-4>', lambda e: 'break')
        self.line_numbers_right.bind('<Button-5>', lambda e: 'break')
        self.line_numbers_left.bind('<MouseWheel>', lambda e: 'break')
        self.line_numbers_left.bind('<Button-4>', lambda e: 'break')
        self.line_numbers_left.bind('<Button-5>', lambda e: 'break')

        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers_right.config(state='normal')
        self.line_numbers_right.delete('1.0', 'end')

        self.line_numbers_left.config(state='normal')
        self.line_numbers_left.delete('1.0', 'end')

        line_count = int(self.text.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers_right.insert('1.0', line_numbers_string)
        self.line_numbers_right.config(state='disabled')
        self.line_numbers_left.insert('1.0', line_numbers_string)
        self.line_numbers_left.config(state='disabled')

    def sync_scroll(self, *args):
        self.line_numbers_right.yview_moveto(self.text.yview()[0])
        self.line_numbers_left.yview_moveto(self.text.yview()[0])

    def on_scrollbar(self, *args):
        self.text.yview(*args)
        self.sync_scroll()

    def set_ui_color(self):
        hex_color = utils.generate_hex_color()
        contrast_color = utils.yiq_contrast_color(hex_color)
        self.text.config(background=hex_color, fg=contrast_color)

        hex_color2 = utils.generate_hex_color()
        contrast_color2 = utils.yiq_contrast_color(hex_color2)
        self.line_numbers_right.config(background=hex_color2, fg=contrast_color2)
        self.line_numbers_left.config(background=hex_color2, fg=contrast_color2)

    def set_ui_color_white(self):
        self.text.config(fg="#000000", background="#fff")
        self.line_numbers_right.config(fg="#000000", background="#d3d3d3")
        self.line_numbers_left.config(fg="#000000", background="#d3d3d3")

    def set_ui_dark_color(self):
        self.text.config(fg="#FFFFFF", background="#3e3e42")
        self.line_numbers_right.config(fg="#FFFFFF", background="#3e3e42")
        self.line_numbers_left.config(fg="#FFFFFF", background="#3e3e42")


    def on_text_scroll(self, *args):
        self.sync_scroll()
        self.scrollbar.set(*args)

    def on_mouse_wheel(self, event):
        self.text.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        self.sync_scroll()
        return 'break'