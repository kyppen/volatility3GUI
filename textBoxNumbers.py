import tkinter as tk
from tkinter import ttk

class TextWithLineNumbers(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create the Text and line number widgets
        self.text = tk.Text(self, wrap='word', height=30, width=200)
        self.line_numbers = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='lightgrey', state='disabled')

        # Pack the widgets
        self.line_numbers.grid(row=0, column=0, sticky='ns')
        self.text.grid(row=0, column=1, sticky='nsew')

        # Configure grid to make text expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.sync_scroll)

        # Bind events to update the line numbers
        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.sync_scroll)
        self.text.bind('<Button-1>', self.sync_scroll)
        self.text.bind('<ButtonRelease-1>', self.sync_scroll)
        self.text.bind('<Configure>', self.sync_scroll)

        # Initialize line numbers
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        '''Update the line numbers in the widget'''
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')

        line_count = int(self.text.index('end').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count))

        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

    def sync_scroll(self, *args):
        '''Synchronize the scrolling of line numbers with the text widget'''
        self.line_numbers.yview_moveto(self.text.yview()[0])
        self.scrollbar.set(*self.text.yview())
