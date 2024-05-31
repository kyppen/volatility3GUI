import tkinter as tk
from tkinter import ttk, Menu, filedialog
import command
import subprocess
import textBoxNumbers





def save_as(output_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("memory", ""), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(output_text.get(1.0, tk.END))

def browse_files(current_command, path_entry ):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
    print((file_path))
    current_command.set_filepath(path_entry.get())
def resize(item):
    size = item.width/10
    return size
def set_flag(current_command, flag):
    current_command.set_flag(flag)
    print(f"set_flag() to {flag}")

def set_command(current_command, command):
    current_command.set_plugin(command)
    print(f"set_plugin to {command} ")


def update_selected(current_command, selected_entry):
    print("update_selected")
    ##TODO add different systems
    selected_text = selected_entry
    selected_entry.delete(0, tk.END)
    current_command.printString()
    selected_entry.insert(0, current_command.to_string())
    print(current_command.to_string())
    print(selected_text)

def run_command(current_command, output_text):
    try:
        # Example: subprocess.check_output(['vol.py', '-f', '/path/to/file', 'windows.pslist'])

        #test = ['volatility3/vol.py', '-f', "benji.raw", 'windows.pslist']
        #command_list = ['volatility3/vol.py', current_command.flag, current_command.filename, current_command.getOsAndPlugin()]
        #print("running command " + ' '.join(command_list))
        #commandlist = current_command.getWindowsCommandList() #For windows machines {Untested2}
        commandlist = current_command.getLinuxCommandList() #For linux machines calling python3
        f = open("output.txt", "w")  # this creates the file

        print("running command " + ' '.join(commandlist))
        output = subprocess.check_output(commandlist, text=True)
        subprocess.run("ls", stdout=f)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Insert the command output to the text widget
    output_text.text.delete("1.0", tk.END)  # Clear the current output
    output_text.text.insert(tk.END, output)  # Insert the new output
    output_text.update_line_numbers()


def mainScreen(OS, root):

    current_command = command.command()
    output_text = tk.StringVar()
    root.geometry("600x400")
    def show_selected():
        print(selected_option.get())

    print("mainScreen")
    print(OS)
    root.title(OS)
    current_command.set_os(OS)
    root.geometry("600x400")
    menu_bar = Menu(root)
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
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
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
    command_menu.add_command(label="pscan", command=lambda:current_command.set_flag_button(plugin_button, "psscan"))
    plugin_button.grid(row=3, column=0, columnspan=2, sticky="ew")

    # Save and Reset buttons
    run_button = ttk.Button(left_frame, text="Run", command=lambda: run_command(current_command,text_with_line_numbers))
    run_button.grid(row=4, column=0, pady=5)
    reset_button = ttk.Button(left_frame, text="Reset")
    reset_button.grid(row=5, column=0, pady=5)

    # Text field to display the current file path
    path_frame = ttk.Frame(root)
    path_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')
    path_label = ttk.Label(path_frame, text="File Path:")
    path_label.grid(row=0, column=0, sticky='w')
    path_entry = ttk.Entry(path_frame, width=50)
    path_entry.grid(row=0, column=1, sticky='ew')
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda: browse_files(current_command,path_entry))
    browse_button.grid(row=0, column=2, padx=5)


    # Text field to display selected commands and flags
    selected_frame = ttk.Frame(root)
    selected_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
    selected_label = ttk.Label(selected_frame, text="Selected:")
    selected_label.grid(row=0, column=0, sticky='w')
    selected_entry = ttk.Entry(selected_frame, width=100)
    selected_entry.grid(row=0, column=1, sticky='ew')
    update_button = ttk.Button(selected_frame, text="Update command", command=lambda :update_selected(current_command, selected_entry))

    update_button.grid(row=0, column=2, padx=5)

    output_frame = ttk.Frame(root)
    output_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    text_with_line_numbers = textBoxNumbers.TextWithLineNumbers(output_frame)
    text_with_line_numbers.grid(row=0, column=0, sticky='nsew')
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
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(1, weight=1)

    #button = ttk.Button(top_frame, text="Show Selected", command=show_selected)
    #button.grid(row=1, column=0, padx=10, pady=10, sticky="nw")



