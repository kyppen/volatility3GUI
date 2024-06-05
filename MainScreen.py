import datetime
import tkinter as tk
from tkinter import ttk, Menu, filedialog, Scrollbar
import command
import subprocess
import textBoxNumbers
import FileHandling
import os
import platform

import utils


def save_as(output_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("memory", ""), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(output_text.get(1.0, tk.END))

def browse_files(current_command, path_entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
    print((file_path))
    current_command.set_filepath(path_entry.get())
def resize(item):
    size = item.width/10
    return size
def selectFromHistory(event):
    print("SelectFromHistory()")
    event.get()
def set_command(current_command, command):
    current_command.set_plugin(command)
    print(f"set_plugin to {command} ")

def get_selected_command(listbox, selected_entry, output_text, info):
    for i in listbox.curselection():
        print(f"index {i}")
        print(listbox.get(i))
        update_selected_from_history(listbox.get(i), selected_entry)
        print(info[0])
        print(len(info))
        #print(info[1])
        output_text.text.delete(1.0, tk.END)
        output_text.text.insert(1.0, info[1][i])


def update_selected_from_history(command, selected_entry):
    print("update_selected_from_history()")
    command.strip()
    selected_entry.delete(0, tk.END)
    selected_entry.insert(0, command)


def update_selected(current_command, selected_entry):
    print("update_selected")
    ##TODO add different systems
    selected_text = selected_entry
    selected_entry.delete(0, tk.END)
    current_command.printString()
    selected_entry.insert(0, current_command.to_string(utils.detect_os()))
    #print(current_command.to_string())


def run_command(current_command, output_text, selected_entry, prevCommandList):
    print("run_command()")
    print("Selected_entry: " + selected_entry.get())
    try:
        # Example: subprocess.check_output(['vol.py', '-f', '/path/to/file', 'windows.pslist'])

        #test = ['volatility3/vol.py', '-f', "benji.raw", 'windows.pslist']
        #command_list = ['volatility3/vol.py', current_command.flag, current_command.filename, current_command.getOsAndPlugin()]
        #print("running command " + ' '.join(command_list))
        #fuckyou = "python3 /home/fam/volatility3/volatility3/vol.py -f benji.raw windows.psscan"
        commandFromEntry = selected_entry.get().strip().split(" ")
        #fuckyoulist = fuckyou.strip().split(" ")
        #commandlist = current_command.getLinuxCommandList() #For linux machines calling python3
        print("running command " + ' '.join(commandFromEntry))

        output = subprocess.check_output(commandFromEntry, text=True)

        FileHandling.AppendCommandToHistory(selected_entry)
        FileHandling.AppendCommandAndOutput(current_command, output, selected_entry)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Insert the command output to the text widget
    output_text.text.delete("1.0", tk.END)  # Clear the current output
    output_text.text.insert(tk.END, output)  # Insert the new output
    output_text.update_line_numbers()
    #FileHandling.update_history(prevCommandList)


def mainScreen(OS, root):

    current_command = command.command()
    #History[0] is a list of previous commands
    #History[1] is a list of previous outputs
    #they should match 1:1
    output_text = tk.StringVar()
    root.geometry("600x400")
    print("mainScreen")
    print(OS)
    root.title(OS)
    current_command.set_os(OS)
    menu_bar = Menu(root)

    ##Top bar
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Export to")
    file_menu.add_command(label="Save as", command=lambda: save_as(output_text))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    help_menu.add_command(label="Tutorial")
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    top_frame = tk.Frame(root)

    selected_option = tk.StringVar()
    ## WF MAC: AC:80:0A:A3:C0:96
    top_frame = tk.Frame(root)
    top_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

    # Create the dropdown menu
    left_frame = ttk.Frame(root)
    left_frame.grid(row=0, column=0,rowspan=3, padx=10, pady=10, sticky='nw')
    os_menu = Menu(left_frame, tearoff=0)

    ##OS button this button's text is the currently selected OS
    os_button = ttk.Menubutton(top_frame, text=OS, menu=os_menu)

    #These makes the buttons for the OS select dropdown
    os_menu.add_command(label="Windows", command=lambda: current_command.set_os_button(os_button,"windows"))
    os_menu.add_command(label="OSX", command=lambda: current_command.set_os_button(os_button,"OSX"))
    os_menu.add_command(label="Linux", command=lambda: current_command.set_os_button(os_button,"Linux"))
    os_button.grid(row=4, column=0, columnspan=2, sticky='nw')


    ##Command Menu
    flag_menu = Menu(left_frame, tearoff=0)
    flag_button = ttk.Menubutton(left_frame, text="flags", menu=flag_menu)
    flag_menu.add_command(label="-f", command=lambda: current_command.set_flag_button(flag_button, "-f"))
    flag_menu.add_command(label="-g", command=lambda: current_command.set_flag_button(flag_button, "-g"))
    flag_menu.add_command(label="-h", command=lambda: current_command.set_flag_button(flag_button, "-h"))
    flag_menu.add_command(label="-pid", command=lambda: current_command.set_flag_button(flag_button, "-pid"))
    flag_menu.add_command(label="-wololo", command=lambda: current_command.set_flag_button(flag_button, "-wololo"))
    flag_menu.add_command(label="-kill", command=lambda: current_command.set_flag_button(flag_button, "-kill"))
    flag_button.grid(row=2, column=0, columnspan=2, sticky='ew')

    command_menu = Menu(left_frame, tearoff=0)
    plugin_button = ttk.Menubutton(left_frame, text="Command", menu=command_menu)
    command_menu.add_command(label="pslist", command=lambda:current_command.set_plugin_button(plugin_button, "pslist"))
    command_menu.add_command(label="pstree", command=lambda:current_command.set_plugin_button(plugin_button, "pstree"))
    command_menu.add_command(label="psxview", command=lambda:current_command.set_plugin_button(plugin_button, "psxview"))
    command_menu.add_command(label="psscan", command=lambda:current_command.set_plugin_button(plugin_button, "psscan"))
    plugin_button.grid(row=3, column=0, columnspan=2, sticky="ew")

    # Text field to display selected commands and flags
    selected_frame = ttk.Frame(root)
    selected_frame.grid(row=0, column=0, columnspan=2, padx=40, pady=50, sticky='n')
    selected_label = ttk.Label(selected_frame, text="Selected:")
    selected_label.grid(row=0, column=0, sticky='w')
    selected_entry = ttk.Entry(selected_frame, width=100)
    selected_entry.grid(row=0, column=1, sticky='ew')
    update_button = ttk.Button(selected_frame, text="Update command", command=lambda :update_selected(current_command, selected_entry))
    
    update_button.grid(row=0, column=2, padx=5)

    # Save and Reset buttons
    run_button = ttk.Button(left_frame, text="Run", command=lambda: run_command(current_command,text_with_line_numbers, selected_entry, prevCommandList))
    run_button.grid(row=4, column=0, pady=5)
    reset_button = ttk.Button(left_frame, text="Reset")
    reset_button.grid(row=4, column=1, pady=5)

    # Frame for command list
    command_frame = ttk.Frame(left_frame)
    command_frame.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')
    command_label = ttk.Label(command_frame, text="Previous Commands")
    command_label.grid(row=0, column=0, padx=5, pady=5)
    #command_list = tk.Listbox(command_frame)
    #command_list.grid(row=1, column=0, sticky='nsew')

    output_frame = ttk.Frame(root)
    output_frame.grid(row=2, column=0, columnspan=2, padx=300, pady=20, sticky='nsew')
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    text_with_line_numbers = textBoxNumbers.TextWithLineNumbers(output_frame)
    text_with_line_numbers.grid(row=0, column=0, sticky='nsew')

    command_frame.grid_rowconfigure(1, weight=1)
    command_frame.grid_columnconfigure(0, weight=1)
    #def get_selected_command(listbox, selected_entry, output_text, info):
    select_button = ttk.Button(command_frame, text="Get Selected Command", command=lambda :get_selected_command(prevCommandList, selected_entry, text_with_line_numbers, History))
    select_button.grid(row=2, column=0, columnspan=2, pady=5)

    command_scrollbar = ttk.Scrollbar(command_frame)
    command_scrollbar.grid(row=1, column=1, sticky='ns')


    prevCommandList = tk.Listbox(command_frame, yscrollcommand=command_scrollbar.set)
    prevCommandList.grid(row=1, column=0, sticky='nsew')
    History = FileHandling.update_history(prevCommandList)
    print(f"Length of History {len(History)}")
    print(f"Length of History[0] {len(History[0])}")
    print(f"Length of History[1] {len(History[1])}")
#def get_selected_command(listbox, selected_entry, output_text, info):
    prevCommandList.bind("<<ListboxSelect>>", get_selected_command(prevCommandList, selected_entry, text_with_line_numbers, History))



    # Text field to display the current file path
    path_frame = ttk.Frame(root)
    path_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')
    path_label = ttk.Label(path_frame, text="File Path:")
    path_label.grid(row=0, column=0, sticky='w')
    path_entry = ttk.Entry(path_frame, width=50)
    path_entry.grid(row=0, column=1, sticky='ew')
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda: browse_files(current_command,path_entry))
    browse_button.grid(row=0, column=2, padx=5)



    # Adjust the left frame's row configurations for proper alignment
    left_frame.grid_rowconfigure(5, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    #log_frame = ttk.Frame(root)
    #left_frame.grid(row=0, column=1, padx=0, pady=10, sticky="ws")
    #log_with_line_number = textBoxNumbers.TextWithLineNumbers(left_frame)
    #log_with_line_number.grid(row=0, column=2, sticky="ns")
    """
    ##Output
    output_frame = ttk.Frame(root)
    output_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='n')
    ##Change width here to change width, should be changed so its dynamic
    output_text = tk.Text(output_frame, wrap='word', height=30, width=200)
    output_text.grid(row=0, column=0, sticky='nsew')
    output_scroll = ttk.Scrollbar(output_frame, command=output_text.yview)
    output_scroll.grid(row=0, column=1, sticky='ns')
    output_text.config(yscrollcommand=output_scroll.set)
    """

    #button = ttk.Button(top_frame, text="Show Selected", command=show_selected)
    #button.grid(row=1, column=0, padx=10, pady=10, sticky="nw")



