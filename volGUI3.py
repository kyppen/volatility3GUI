import tkinter as tk
from tkinter import ttk, Menu, filedialog
import platform
import subprocess
import FileHandling
import textBoxNumbers
import command as cmd



def save_as(output_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output_text.text.get(1.0, tk.END))


def clear_path():
    path_entry.delete(0, tk.END)


def get_system():
    return platform.system()


def browse_files(current_command):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
        current_command.set_filepath(file_path)

def get_selected_command(listbox, output_text, info, mid_text_field):
    print("get_selected_command()")
    for i in listbox.curselection():
        print(f"index {i}")
        print(listbox.get(i))
        update_selected_from_history(listbox.get(i), mid_text_field)
        print(info[0])
        print(len(info))
        #print(info[1])
        output_text.text.delete(1.0, tk.END)
        output_text.text.insert(1.0, info[1][i])

def update_selected_from_history(command, mid_text_field):
    print("update_selected_from_history()")
    command.strip()
    mid_text_field.delete(0, tk.END)
    mid_text_field.insert(0, command)

def set_os(os_name, current_command):
    current_command.set_os(os_name)
    print(current_command.os)
    os_entry.delete(0, tk.END)
    os_entry.insert(0, os_name)

def set_pluginAndFlag(current_command, plugin, flag):
    current_command.set_plugin(plugin)
    current_command.set_flag(flag)
    print(current_command.plugin)
    print(current_command.flag)


def run_command(current_command, output_text, prevCommandList, mid_text_field):
    print("run_command()")
    #print("Selected_entry: " + selected_entry.get())
    try:
        # Example: subprocess.check_output(['vol.py', '-f', '/path/to/file', 'windows.pslist'])

        #test = ['volatility3/vol.py', '-f', "benji.raw", 'windows.pslist']
        #command_list = ['volatility3/vol.py', current_command.flag, current_command.filename, current_command.getOsAndPlugin()]
        #print("running command " + ' '.join(command_list))
        #fuckyou = "python3 /home/fam/volatility3/volatility3/vol.py -f benji.raw windows.psscan"

        #commandFromEntry = selected_entry.get().strip().split(" ")
        print(current_command.to_string())
        #fuckyoulist = fuckyou.strip().split(" ")
        commandlist = current_command.to_string().split(" ") #For linux machines calling python3
        #print("running command " + ' '.join(commandFromEntry))
        output = subprocess.check_output(commandlist, text=True)

        FileHandling.AppendCommandToHistory(current_command)
        FileHandling.AppendCommandAndOutput(current_command, output)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Insert the command output to the text widget
    output_text.text.delete(1.0, tk.END)  # Clear the current output
    output_text.text.insert(tk.END, output)  # Insert the new output
    output_text.update_line_numbers()
    mid_text_field.delete(0, tk.END)
    mid_text_field.insert(tk.END, current_command.to_string())
    FileHandling.update_history(prevCommandList)
    total_steps = 1
    for i in range(total_steps):
        progress_bar['value'] = (i + 1) * (100 / total_steps)
        #root.update_idletasks()


def create_gui():
    #intro.show_welcome_window()
    current_command = cmd.command()
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
    file_menu.add_command(label="Save as", command=lambda: save_as(text_with_line_numbers))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    help_menu.add_command(label="Tutorial")
    menu_bar.add_cascade(label="Help", menu=help_menu)

    os_menu = Menu(menu_bar, tearoff=0)
    os_menu.add_command(label="Windows", command=lambda: set_os("windows", current_command))
    os_menu.add_command(label="MacOS", command=lambda: set_os("MacOs", current_command))
    os_menu.add_command(label="Linux", command=lambda: set_os("linux", current_command))
    os_menu.add_command(label="RedStarOS", command=lambda: set_os("RedStarOS", current_command))
    os_menu.add_command(label="TempleOS", command=lambda: set_os("TempleOS", current_command))
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
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda :browse_files(current_command))
    browse_button.grid(row=0, column=2, padx=1, pady=0)
    clear_button = ttk.Button(path_frame, text="Clear", command=clear_path)
    clear_button.grid(row=0, column=3, padx=1, pady=0)

    # plugins & flags
    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(frame_center, tearoff=0)

    # dlllist_plugin
    dlllist_plugin = Menu(commands_menu, tearoff=0)
    dlllist_plugin.add_command(label="--pid", command=lambda :set_pluginAndFlag(current_command,"dlllist","--pid"))
    dlllist_plugin.add_command(label="--offset",command=lambda :set_pluginAndFlag(current_command,"dlllist","--offset"))
    dlllist_plugin.add_command(label="--profile",command=lambda :set_pluginAndFlag(current_command,"dlllist","--profile"))
    commands_menu.add_cascade(label="dlllist", menu=dlllist_plugin)

    # psscan_plugin
    psscan_plugin = Menu(commands_menu, tearoff=0)
    psscan_plugin.add_command(label="-f", command=lambda :set_pluginAndFlag(current_command,"psscan","-f"))
    commands_menu.add_cascade(label="psscan", menu=psscan_plugin)

    # pslist_plugin
    pslist_plugin = Menu(commands_menu, tearoff=0)
    pslist_plugin.add_command(label="-f", command=lambda :set_pluginAndFlag(current_command,"pslist","-f"))
    commands_menu.add_cascade(label="pslist", menu=pslist_plugin)

    # pstree_plugin
    pstree_plugin = Menu(commands_menu, tearoff=0)
    pstree_plugin.add_command(label="placeholder", command = lambda: set_pluginAndFlag(current_command, "pstree", "placeholder"))
    commands_menu.add_cascade(label="pstree", menu=pstree_plugin)

    commands_button = ttk.Menubutton(frame_center, text="Commands", menu=commands_menu,)
    commands_button.grid(row=1, column=0, columnspan=2, sticky='ew')

    prevCommandList = tk.Listbox(frame_right, width=60)
    prevCommandList.grid(row=0, column=0, sticky='nsew')

    command_scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=prevCommandList.yview)
    command_scrollbar.grid(row=0, column=1, sticky='ns')



    output_frame = ttk.Frame(frame_lower)
    output_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    text_with_line_numbers = textBoxNumbers.TextWithLineNumbers(output_frame)
    text_with_line_numbers.pack(expand=True, fill='both')

    prevCommandList.config(yscrollcommand=command_scrollbar.set)
    History = FileHandling.update_history(prevCommandList)
    print(f"Length of History {len(History)}")
    print(f"Length of History[0] {len(History[0])}")
    print(f"Length of History[1] {len(History[1])}")


    select_button = ttk.Button(frame_right, text="Get Selected Command", command=lambda :get_selected_command(prevCommandList, text_with_line_numbers, History, mid_text_field))
    select_button.grid(row=2, column=0, columnspan=2, pady=5)

    prevCommandList.pack()

    # Widgets in frame_mid
    mid_text_field = ttk.Entry(frame_mid, width=100)
    mid_text_field.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    mid_text_field.insert(0, "filename.txt / dlllist / --offset")
    prevCommandList.bind("<<ListboxSelect>>",
                         get_selected_command(prevCommandList, text_with_line_numbers, History, mid_text_field))

    run_button = ttk.Button(frame_mid, text="Run", command=lambda:run_command(current_command,text_with_line_numbers,prevCommandList, mid_text_field))
    run_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    reset_button = ttk.Button(frame_mid, text="Reset")
    reset_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    cancel_button = ttk.Button(frame_mid, text="Cancel")
    cancel_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

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
