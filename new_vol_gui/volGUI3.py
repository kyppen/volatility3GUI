import tkinter as tk
from tkinter import ttk, Menu, filedialog
import platform

import textBoxNumbers


def save_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output_text.get(1.0, tk.END))


def clear_path():
    path_entry.delete(0, tk.END)


def get_system():
    return platform.system()


def browse_files():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)


def set_os(os_name):
    os_entry.delete(0, tk.END)
    os_entry.insert(0, os_name)


def create_gui():
    global path_entry, selected_entry, cmd_var, flag_var, os_var, output_text, progress_bar, progress_label, os_entry
    # Create the main window
    root = tk.Tk()
    root.title("Volatility 3")
    root.configure(bg="#f2f2e9")

    # menubar frame
    menubar_frame = ttk.Frame(root, height=30)
    menubar_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
    menubar_frame.grid_propagate(False)

    # Create a container frame inside the menubar_frame
    menubar_container = ttk.Frame(menubar_frame)
    menubar_container.grid(row=0, column=0, sticky='ew')

    # Configure the container frame to expand
    menubar_container.grid_columnconfigure(0, weight=1)
    menubar_container.grid_columnconfigure(1, weight=0)

    # Text field to display the current OS
    os_entry = ttk.Entry(menubar_container, width=20)
    os_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

    # menubar
    menu_bar = Menu(menubar_container)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Export to")
    file_menu.add_command(label="Save as", command=lambda: save_as())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    help_menu.add_command(label="Tutorial")
    menu_bar.add_cascade(label="Help", menu=help_menu)

    os_menu = Menu(menu_bar, tearoff=0)
    os_menu.add_command(label="Windows", command=lambda: set_os("Windows"))
    os_menu.add_command(label="MacOS", command=lambda: set_os("MacOS"))
    os_menu.add_command(label="Linux", command=lambda: set_os("Linux"))
    os_menu.add_command(label="RedStarOS", command=lambda: set_os("RedStarOS"))
    os_menu.add_command(label="TempleOS", command=lambda: set_os("TempleOS"))
    menu_bar.add_cascade(label="OS", menu=os_menu)

    root.config(menu=menu_bar)

    # window size
    root.minsize(1200, 400)

    # root window grid layout
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)

    # frames
    frame_left = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_center = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_right = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_mid = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_lower = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)

    # frame placement
    frame_left.grid(row=1, column=0, sticky="nsew")
    frame_center.grid(row=1, column=1, sticky="nsew")
    frame_right.grid(row=1, column=2, sticky="nsew")
    frame_mid.grid(row=2, column=0, columnspan=3, sticky="nsew")
    frame_lower.grid(row=3, column=0, columnspan=3, sticky="nsew")

    # Force frames to keep their size
    frame_left.grid_propagate(False)
    frame_center.grid_propagate(False)
    frame_right.grid_propagate(False)
    frame_mid.grid_propagate(False)

    # Configure grid for frame_right to make Listbox and Scrollbar fill the frame
    frame_right.grid_rowconfigure(0, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_columnconfigure(1, weight=0)

    # Set the size of the top frames
    frame_left.config(width=200, height=100)
    frame_center.config(width=200, height=100)
    frame_right.config(width=200, height=100)
    frame_mid.config(height=50)

    # Ensure frame_mid's height remains locked
    frame_mid.grid(row=2, column=0, columnspan=3, sticky="nsew")

    # row & column weights for frames
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=5)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)

    # Text field to display the current file path
    path_frame = ttk.Frame(frame_left, padding="1 1 1 1", style='TFrame')
    path_frame.grid(row=0, column=1, padx=1, pady=1, sticky='ew')
    path_label = ttk.Label(path_frame, text="File Path:")
    path_label.grid(row=0, column=0, sticky='w')
    path_entry = ttk.Entry(path_frame, width=20)
    path_entry.grid(row=0, column=1, sticky='ew')
    browse_button = ttk.Button(path_frame, text="Browse", command=browse_files)
    browse_button.grid(row=0, column=2, padx=1, pady=0)
    clear_button = ttk.Button(path_frame, text="Clear", command=clear_path)
    clear_button.grid(row=0, column=3, padx=1, pady=0)

    # plugins & flags
    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(frame_center, tearoff=0)

    # dlllist_plugin
    dlllist_plugin = Menu(commands_menu, tearoff=0)
    dlllist_plugin.add_command(label="--pid")
    dlllist_plugin.add_command(label="--offset")
    dlllist_plugin.add_command(label="--profile")
    commands_menu.add_cascade(label="dlllist", menu=dlllist_plugin)

    # psscan_plugin
    psscan_plugin = Menu(commands_menu, tearoff=0)
    psscan_plugin.add_command(label="--profile")
    commands_menu.add_cascade(label="psscan", menu=psscan_plugin)

    # pslist_plugin
    pslist_plugin = Menu(commands_menu, tearoff=0)
    pslist_plugin.add_command(label="-P")
    commands_menu.add_cascade(label="pslist", menu=pslist_plugin)

    # pstree_plugin
    pstree_plugin = Menu(commands_menu, tearoff=0)
    commands_menu.add_cascade(label="pstree", menu=pstree_plugin)

    commands_button = ttk.Menubutton(frame_center, text="Commands", menu=commands_menu)
    commands_button.grid(row=1, column=0, columnspan=2, sticky='ew')

    # def get_selected_command(listbox, selected_entry, output_text, info):
    select_button = ttk.Button(frame_right, text="Get Selected Command")

    prevCommandList = tk.Listbox(frame_right)
    prevCommandList.grid(row=0, column=0, sticky='nsew')

    command_scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=prevCommandList.yview)
    command_scrollbar.grid(row=0, column=1, sticky='ns')

    prevCommandList.config(yscrollcommand=command_scrollbar.set)

    for i in range(0, 15):
        prevCommandList.insert(i, f"cmd:{i} wololo")

    output_frame = ttk.Frame(frame_lower)
    output_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    text_with_line_numbers = textBoxNumbers.TextWithLineNumbers(output_frame)
    text_with_line_numbers.pack(expand=True, fill='both')

    prevCommandList.pack()

    # Widgets in frame_mid
    mid_text_field = ttk.Entry(frame_mid, width=30)
    mid_text_field.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    mid_text_field.insert(0, "filename.txt / dlllist / --offset")

    mid_button1 = ttk.Button(frame_mid, text="Run")
    mid_button1.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    mid_button2 = ttk.Button(frame_mid, text="Reset")
    mid_button2.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    mid_button3 = ttk.Button(frame_mid, text="Cancel")
    mid_button3.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    progress_bar = ttk.Progressbar(frame_mid, orient="horizontal", mode="determinate", maximum=100)
    progress_bar.grid(row=0, column=4, padx=3, pady=3, sticky='ew')

    # Configure grid weights for frame_mid
    frame_mid.grid_columnconfigure(0, weight=1)
    frame_mid.grid_columnconfigure(1, weight=0)
    frame_mid.grid_columnconfigure(2, weight=0)
    frame_mid.grid_columnconfigure(3, weight=0)
    frame_mid.grid_columnconfigure(4, weight=2)
    frame_mid.grid_columnconfigure(5, weight=0)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
