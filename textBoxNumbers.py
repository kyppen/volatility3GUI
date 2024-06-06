import tkinter as tk
from tkinter import ttk

class TextWithLineNumbers(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create the Text and line number widgets
        self.text = tk.Text(self, wrap='word', height=30, width=200, undo=True)
        self.line_numbers = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='lightgrey', state='disabled')

        # Pack the widgets
        self.line_numbers.grid(row=0, column=0, sticky='ns')
        self.text.grid(row=0, column=1, sticky='nsew')

        # Configure grid to make text expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.on_scrollbar)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.on_text_scroll)

        # Bind events to update the line numbers
        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.on_mouse_wheel)
        self.text.bind('<Button-1>', self.sync_scroll)
        self.text.bind('<ButtonRelease-1>', self.sync_scroll)
        self.text.bind('<Configure>', self.sync_scroll)

        # Disable scrolling on the line number widget
        self.line_numbers.bind('<MouseWheel>', lambda e: 'break')
        self.line_numbers.bind('<Button-4>', lambda e: 'break')
        self.line_numbers.bind('<Button-5>', lambda e: 'break')

        # Initialize line numbers
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        '''Update the line numbers in the widget'''
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')

        line_count = int(self.text.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

    def sync_scroll(self, *args):
        '''Synchronize the scrolling of line numbers with the text widget'''
        self.line_numbers.yview_moveto(self.text.yview()[0])

    def on_scrollbar(self, *args):
        '''Handle scrollbar movement'''
        self.text.yview(*args)
        self.sync_scroll()

    def on_text_scroll(self, *args):
        '''Handle text widget scrolling'''
        self.sync_scroll()
        self.scrollbar.set(*args)

    def on_mouse_wheel(self, event):
        '''Handle mouse wheel movement'''
        self.text.yview_scroll(int(-1*(event.delta/120)), 'units')
        self.sync_scroll()
        return 'break'