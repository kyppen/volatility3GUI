import tkinter as tk
from tkinter import ttk, Menu, filedialog
import platform
import subprocess
import FileHandling
import textBoxNumbers
import command as cmd
import re


def save_as(output_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output_text.text.get(1.0, tk.END))


# empties the path_entry field
def clear_path(path_entry):
    path_entry.delete(0, tk.END)


# returns the name of host os
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
        #print(f"index {i}")
        print(listbox.get(i))
        update_selected_from_history(listbox.get(i), mid_text_field)
        print(info[0])
        print(len(info))
        # print(info[1])
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


def get_os():
    return os_entry.get()


# runs command with subproccess and returns result in text form
def run_command_capture_output(cmd_list):
def set_pluginAndFlag(current_command, plugin, flag):
    current_command.set_plugin(plugin)
    current_command.set_flag(flag)
    print(current_command.plugin)
    print(current_command.flag)


def run_command(current_command, output_text, prevCommandList, mid_text_field):
    print("run_command()")
    # print("Selected_entry: " + selected_entry.get())
    try:
        # Example: subprocess.check_output(['vol.py', '-f', '/path/to/file', 'windows.pslist'])

        # test = ['volatility3/vol.py', '-f', "benji.raw", 'windows.pslist']
        # command_list = ['volatility3/vol.py', current_command.flag, current_command.filename, current_command.getOsAndPlugin()]
        # print("running command " + ' '.join(command_list))
        # fuckyou = "python3 /home/fam/volatility3/volatility3/vol.py -f benji.raw windows.psscan"

        # commandFromEntry = selected_entry.get().strip().split(" ")
        print(current_command.to_string())
        # fuckyoulist = fuckyou.strip().split(" ")
        commandlist = current_command.to_string().split(" ")  # For linux machines calling python3
        # print("running command " + ' '.join(commandFromEntry))
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
    #for i in range(total_steps):
       # progress_bar['value'] = (i + 1) * (100 / total_steps)
        # root.update_idletasks()


# adds plugin and flag to command list
# if plugin is already in list then only adds flag
def add_to_command(plugin, flag, cmd_list):
    if (get_os() + '.' + plugin) in cmd_list:
        cmd_list.append(flag)
        add_userinput_to_command(flag, cmd_list)
    else:
        cmd_list.append(get_os() + '.' + plugin)
        cmd_list.append(flag)
        add_userinput_to_command(flag, cmd_list)
    return cmd_list


def sanitize_input(input):
    # Use regex to sanitize for a-z, A-Z, 0-9 and -
    sanitized = re.sub(r'[^a-zA-Z0-9-]', '', input)
    return sanitized


def check_if_flag_takes_input(flag):
    flags_with_input = ['--pid', '--offset']
    if flag in flags_with_input:
        root = tk.Tk()
        root.withdraw()
        user_input = simpledialog.askstring("Input Required", f"Please enter a value for {flag}:")
        root.destroy()
        return sanitize_input(user_input)
    return None


# adds the userinput to the index after the flag it belongs to in the list
def add_userinput_to_command(flag, cmd_list):
    if flag in cmd_list:
        user_input = check_if_flag_takes_input(flag)
        if user_input is not None:
            if type(user_input) is list:
                flag_index = cmd_list.index('-f')
                cmd_list.insert(flag_index + 2, user_input[0])
                cmd_list.insert(flag_index + 3, user_input[1])
            else:
                flag_index = cmd_list.index(flag)
                cmd_list.insert(flag_index + 1, user_input)

        else:
            print(f"flag '{flag}' does not take input")
    else:
        print(f"Flag '{flag}' not found in cmd_list")

    return cmd_list


# resets the command list
def reset_command_list(cmd_list, file_path):
    cmd_list.clear()
    if get_system() == "Windows":
        cmd_list.append("python")
        cmd_list.append("path/to/vol.py")
    else:
        cmd_list.append("python3")

    cmd_list.append("-f")
    return cmd_list


def update_cmd(command_list):
    # Join the command list into a single string
    command_str = ' '.join(command_list)
    # Update the mid_text_field with the new command string
    mid_text_field.delete(0, tk.END)
    mid_text_field.insert(0, command_str)


def reset_and_update(cmd_list):
    reset_command_list(cmd_list)
    update_cmd(cmd_list)


def create_gui():
   # intro.show_welcome_window()
    current_command = cmd.command()
    global path_entry, selected_entry, cmd_var, flag_var, os_var, output_text, progress_bar, progress_label, os_entry
    command_list = []
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
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda: browse_files(current_command))
    browse_button.grid(row=0, column=2, padx=1, pady=0)
    clear_button = ttk.Button(path_frame, text="Clear", command=clear_path)
    clear_button.grid(row=0, column=3, padx=1, pady=0)

    # plugins & flags
    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(frame_center, tearoff=0)

    # Bigpools_plugin
    Bigpools_plugin = Menu(commands_menu, tearoff=0)
    bigpools_kernel_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="--kernel", variable=bigpools_kernel_var, command=lambda: set_pluginAndFlag(current_command, "bigpools", "--kernel"))
    bigpools_tags_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="--tags", variable=bigpools_tags_var, command=lambda: set_pluginAndFlag(current_command, "bigpools", "--tags"))
    bigpools_show_free_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="--show-free", variable=bigpools_show_free_var, command=lambda: set_pluginAndFlag(current_command, "bigpools", "--show-free"))
    commands_menu.add_cascade(label="Bigpools", menu=Bigpools_plugin)

    # Cachedump_plugin
    Cachedump_plugin = Menu(commands_menu, tearoff=0)
    cachedump_kernel_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--kernel", variable=cachedump_kernel_var, command=lambda: set_pluginAndFlag(current_command, "cachedump", "--kernel"))
    cachedump_hivelist_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--hivelist", variable=cachedump_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "cachedump", "--hivelist"))
    cachedump_lsadump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--lsadump", variable=cachedump_lsadump_var, command=lambda: set_pluginAndFlag(current_command, "cachedump", "--lsadump"))
    cachedump_hashdump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--hashdump", variable=cachedump_hashdump_var, command=lambda: set_pluginAndFlag(current_command, "cachedump", "--hashdump"))
    commands_menu.add_cascade(label="Cachedump", menu=Cachedump_plugin)

    # Callbacks_plugin
    Callbacks_plugin = Menu(commands_menu, tearoff=0)
    callbacks_kernel_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="--kernel", variable=callbacks_kernel_var, command=lambda: set_pluginAndFlag(current_command, "callbacks", "--kernel"))
    callbacks_ssdt_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="--ssdt", variable=callbacks_ssdt_var, command=lambda: set_pluginAndFlag(current_command, "callbacks", "--ssdt"))
    commands_menu.add_cascade(label="Callbacks", menu=Callbacks_plugin)

    # Cmdline_plugin
    Cmdline_plugin = Menu(commands_menu, tearoff=0)
    cmdline_kernel_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--kernel", variable=cmdline_kernel_var, command=lambda: set_pluginAndFlag(current_command, "cmdline", "--kernel"))
    cmdline_pslist_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--pslist", variable=cmdline_pslist_var, command=lambda: set_pluginAndFlag(current_command, "cmdline", "--pslist"))
    cmdline_pid_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--pid", variable=cmdline_pid_var, command=lambda: set_pluginAndFlag(current_command, "cmdline", "--pid"))
    commands_menu.add_cascade(label="Cmdline", menu=Cmdline_plugin)

    # Crashinfo_plugin
    Crashinfo_plugin = Menu(commands_menu, tearoff=0)
    crashinfo_primary_var = tk.BooleanVar()
    Crashinfo_plugin.add_checkbutton(label="--primary", variable=crashinfo_primary_var, command=lambda: set_pluginAndFlag(current_command, "crashinfo", "--primary"))
    commands_menu.add_cascade(label="Crashinfo", menu=Crashinfo_plugin)

    # Devicetree_plugin
    Devicetree_plugin = Menu(commands_menu, tearoff=0)
    devicetree_kernel_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="--kernel", variable=devicetree_kernel_var, command=lambda: set_pluginAndFlag(current_command, "devicetree", "--kernel"))
    devicetree_driverscan_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="--driverscan", variable=devicetree_driverscan_var, command=lambda: set_pluginAndFlag(current_command, "devicetree", "--driverscan"))
    commands_menu.add_cascade(label="Devicetree", menu=Devicetree_plugin)

    # Dlllist_plugin
    Dlllist_plugin = Menu(commands_menu, tearoff=0)
    dlllist_kernel_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--kernel", variable=dlllist_kernel_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--kernel"))
    dlllist_pslist_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--pslist", variable=dlllist_pslist_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--pslist"))
    dlllist_psscan_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--psscan", variable=dlllist_psscan_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--psscan"))
    dlllist_info_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--info", variable=dlllist_info_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--info"))
    dlllist_pid_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--pid", variable=dlllist_pid_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--pid"))
    dlllist_offset_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--offset", variable=dlllist_offset_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--offset"))
    dlllist_dump_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--dump", variable=dlllist_dump_var, command=lambda: set_pluginAndFlag(current_command, "dlllist", "--dump"))
    commands_menu.add_cascade(label="Dlllist", menu=Dlllist_plugin)

    # Driverirp_plugin
    Driverirp_plugin = Menu(commands_menu, tearoff=0)
    driverirp_kernel_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--kernel", variable=driverirp_kernel_var, command=lambda: set_pluginAndFlag(current_command, "driverirp", "--kernel"))
    driverirp_ssdt_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--ssdt", variable=driverirp_ssdt_var, command=lambda: set_pluginAndFlag(current_command, "driverirp", "--ssdt"))
    driverirp_driverscan_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--driverscan", variable=driverirp_driverscan_var, command=lambda: set_pluginAndFlag(current_command, "driverirp", "--driverscan"))
    commands_menu.add_cascade(label="Driverirp", menu=Driverirp_plugin)

    # Drivermodule_plugin
    Drivermodule_plugin = Menu(commands_menu, tearoff=0)
    drivermodule_kernel_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--kernel", variable=drivermodule_kernel_var, command=lambda: set_pluginAndFlag(current_command, "drivermodule", "--kernel"))
    drivermodule_ssdt_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--ssdt", variable=drivermodule_ssdt_var, command=lambda: set_pluginAndFlag(current_command, "drivermodule", "--ssdt"))
    drivermodule_driverscan_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--driverscan", variable=drivermodule_driverscan_var, command=lambda: set_pluginAndFlag(current_command, "drivermodule", "--driverscan"))
    commands_menu.add_cascade(label="Drivermodule", menu=Drivermodule_plugin)

    # Driverscan_plugin
    Driverscan_plugin = Menu(commands_menu, tearoff=0)
    driverscan_kernel_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="--kernel", variable=driverscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "driverscan", "--kernel"))
    driverscan_poolscanner_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="--poolscanner", variable=driverscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "driverscan", "--poolscanner"))
    commands_menu.add_cascade(label="Driverscan", menu=Driverscan_plugin)

    # Dumpfiles_plugin
    Dumpfiles_plugin = Menu(commands_menu, tearoff=0)
    dumpfiles_kernel_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--kernel", variable=dumpfiles_kernel_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--kernel"))
    dumpfiles_pid_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--pid", variable=dumpfiles_pid_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--pid"))
    dumpfiles_virtaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--virtaddr", variable=dumpfiles_virtaddr_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--virtaddr"))
    dumpfiles_physaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--physaddr", variable=dumpfiles_physaddr_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--physaddr"))
    dumpfiles_filter_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--filter", variable=dumpfiles_filter_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--filter"))
    dumpfiles_ignore_case_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--ignore-case", variable=dumpfiles_ignore_case_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--ignore-case"))
    dumpfiles_pslist_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--pslist", variable=dumpfiles_pslist_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--pslist"))
    dumpfiles_handles_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--handles", variable=dumpfiles_handles_var, command=lambda: set_pluginAndFlag(current_command, "dumpfiles", "--handles"))
    commands_menu.add_cascade(label="Dumpfiles", menu=Dumpfiles_plugin)

    # Envars_plugin
    Envars_plugin = Menu(commands_menu, tearoff=0)
    envars_kernel_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--kernel", variable=envars_kernel_var, command=lambda: set_pluginAndFlag(current_command, "envars", "--kernel"))
    envars_pid_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--pid", variable=envars_pid_var, command=lambda: set_pluginAndFlag(current_command, "envars", "--pid"))
    envars_silent_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--silent", variable=envars_silent_var, command=lambda: set_pluginAndFlag(current_command, "envars", "--silent"))
    envars_pslist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--pslist", variable=envars_pslist_var, command=lambda: set_pluginAndFlag(current_command, "envars", "--pslist"))
    envars_hivelist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--hivelist", variable=envars_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "envars", "--hivelist"))
    commands_menu.add_cascade(label="Envars", menu=Envars_plugin)

    # Filescan_plugin
    Filescan_plugin = Menu(commands_menu, tearoff=0)
    filescan_kernel_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="--kernel", variable=filescan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "filescan", "--kernel"))
    filescan_poolscanner_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="--poolscanner", variable=filescan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "filescan", "--poolscanner"))
    commands_menu.add_cascade(label="Filescan", menu=Filescan_plugin)

    # Getservicesids_plugin
    Getservicesids_plugin = Menu(commands_menu, tearoff=0)
    getservicesids_kernel_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="--kernel", variable=getservicesids_kernel_var, command=lambda: set_pluginAndFlag(current_command, "getservicesids", "--kernel"))
    getservicesids_hivelist_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="--hivelist", variable=getservicesids_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "getservicesids", "--hivelist"))
    commands_menu.add_cascade(label="Getservicesids", menu=Getservicesids_plugin)

    # Getsids_plugin
    Getsids_plugin = Menu(commands_menu, tearoff=0)
    getsids_kernel_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--kernel", variable=getsids_kernel_var, command=lambda: set_pluginAndFlag(current_command, "getsids", "--kernel"))
    getsids_pid_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--pid", variable=getsids_pid_var, command=lambda: set_pluginAndFlag(current_command, "getsids", "--pid"))
    getsids_pslist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--pslist", variable=getsids_pslist_var, command=lambda: set_pluginAndFlag(current_command, "getsids", "--pslist"))
    getsids_hivelist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--hivelist", variable=getsids_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "getsids", "--hivelist"))
    commands_menu.add_cascade(label="Getsids", menu=Getsids_plugin)

    # Handles_plugin
    Handles_plugin = Menu(commands_menu, tearoff=0)
    handles_kernel_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--kernel", variable=handles_kernel_var, command=lambda: set_pluginAndFlag(current_command, "handles", "--kernel"))
    handles_pslist_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--pslist", variable=handles_pslist_var, command=lambda: set_pluginAndFlag(current_command, "handles", "--pslist"))
    handles_psscan_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--psscan", variable=handles_psscan_var, command=lambda: set_pluginAndFlag(current_command, "handles", "--psscan"))
    handles_pid_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--pid", variable=handles_pid_var, command=lambda: set_pluginAndFlag(current_command, "handles", "--pid"))
    handles_offset_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--offset", variable=handles_offset_var, command=lambda: set_pluginAndFlag(current_command, "handles", "--offset"))
    commands_menu.add_cascade(label="Handles", menu=Handles_plugin)

    # Hashdump_plugin
    Hashdump_plugin = Menu(commands_menu, tearoff=0)
    hashdump_kernel_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="--kernel", variable=hashdump_kernel_var, command=lambda: set_pluginAndFlag(current_command, "hashdump", "--kernel"))
    hashdump_hivelist_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="--hivelist", variable=hashdump_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "hashdump", "--hivelist"))
    commands_menu.add_cascade(label="Hashdump", menu=Hashdump_plugin)

    # Iat_plugin
    Iat_plugin = Menu(commands_menu, tearoff=0)
    iat_kernel_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--kernel", variable=iat_kernel_var, command=lambda: set_pluginAndFlag(current_command, "iat", "--kernel"))
    iat_pslist_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--pslist", variable=iat_pslist_var, command=lambda: set_pluginAndFlag(current_command, "iat", "--pslist"))
    iat_pid_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--pid", variable=iat_pid_var, command=lambda: set_pluginAndFlag(current_command, "iat", "--pid"))
    commands_menu.add_cascade(label="Iat", menu=Iat_plugin)

    # Info_plugin
    Info_plugin = Menu(commands_menu, tearoff=0)
    info_kernel_var = tk.BooleanVar()
    Info_plugin.add_checkbutton(label="--kernel", variable=info_kernel_var, command=lambda: set_pluginAndFlag(current_command, "info", "--kernel"))
    commands_menu.add_cascade(label="Info", menu=Info_plugin)

    # Joblinks_plugin
    Joblinks_plugin = Menu(commands_menu, tearoff=0)
    joblinks_kernel_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--kernel", variable=joblinks_kernel_var, command=lambda: set_pluginAndFlag(current_command, "joblinks", "--kernel"))
    joblinks_physical_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--physical", variable=joblinks_physical_var, command=lambda: set_pluginAndFlag(current_command, "joblinks", "--physical"))
    joblinks_pslist_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--pslist", variable=joblinks_pslist_var, command=lambda: set_pluginAndFlag(current_command, "joblinks", "--pslist"))
    commands_menu.add_cascade(label="Joblinks", menu=Joblinks_plugin)

    # Ldrmodules_plugin
    Ldrmodules_plugin = Menu(commands_menu, tearoff=0)
    ldrmodules_kernel_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--kernel", variable=ldrmodules_kernel_var, command=lambda: set_pluginAndFlag(current_command, "ldrmodules", "--kernel"))
    ldrmodules_pslist_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--pslist", variable=ldrmodules_pslist_var, command=lambda: set_pluginAndFlag(current_command, "ldrmodules", "--pslist"))
    ldrmodules_vadinfo_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--vadinfo", variable=ldrmodules_vadinfo_var, command=lambda: set_pluginAndFlag(current_command, "ldrmodules", "--vadinfo"))
    ldrmodules_pid_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--pid", variable=ldrmodules_pid_var, command=lambda: set_pluginAndFlag(current_command, "ldrmodules", "--pid"))
    commands_menu.add_cascade(label="Ldrmodules", menu=Ldrmodules_plugin)

    # Lsadump_plugin
    Lsadump_plugin = Menu(commands_menu, tearoff=0)
    lsadump_kernel_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--kernel", variable=lsadump_kernel_var, command=lambda: set_pluginAndFlag(current_command, "lsadump", "--kernel"))
    lsadump_hashdump_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--hashdump", variable=lsadump_hashdump_var, command=lambda: set_pluginAndFlag(current_command, "lsadump", "--hashdump"))
    lsadump_hivelist_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--hivelist", variable=lsadump_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "lsadump", "--hivelist"))
    commands_menu.add_cascade(label="Lsadump", menu=Lsadump_plugin)

    # Malfind_plugin
    Malfind_plugin = Menu(commands_menu, tearoff=0)
    malfind_kernel_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--kernel", variable=malfind_kernel_var, command=lambda: set_pluginAndFlag(current_command, "malfind", "--kernel"))
    malfind_pid_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--pid", variable=malfind_pid_var, command=lambda: set_pluginAndFlag(current_command, "malfind", "--pid"))
    malfind_dump_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--dump", variable=malfind_dump_var, command=lambda: set_pluginAndFlag(current_command, "malfind", "--dump"))
    malfind_pslist_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--pslist", variable=malfind_pslist_var, command=lambda: set_pluginAndFlag(current_command, "malfind", "--pslist"))
    malfind_vadinfo_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--vadinfo", variable=malfind_vadinfo_var, command=lambda: set_pluginAndFlag(current_command, "malfind", "--vadinfo"))
    commands_menu.add_cascade(label="Malfind", menu=Malfind_plugin)

    # Mbrscan_plugin
    Mbrscan_plugin = Menu(commands_menu, tearoff=0)
    mbrscan_kernel_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="--kernel", variable=mbrscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "mbrscan", "--kernel"))
    mbrscan_full_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="--full", variable=mbrscan_full_var, command=lambda: set_pluginAndFlag(current_command, "mbrscan", "--full"))
    commands_menu.add_cascade(label="Mbrscan", menu=Mbrscan_plugin)

    # Memmap_plugin
    Memmap_plugin = Menu(commands_menu, tearoff=0)
    memmap_kernel_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--kernel", variable=memmap_kernel_var, command=lambda: set_pluginAndFlag(current_command, "memmap", "--kernel"))
    memmap_pslist_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--pslist", variable=memmap_pslist_var, command=lambda: set_pluginAndFlag(current_command, "memmap", "--pslist"))
    memmap_pid_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--pid", variable=memmap_pid_var, command=lambda: set_pluginAndFlag(current_command, "memmap", "--pid"))
    memmap_dump_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--dump", variable=memmap_dump_var, command=lambda: set_pluginAndFlag(current_command, "memmap", "--dump"))
    commands_menu.add_cascade(label="Memmap", menu=Memmap_plugin)

    # Mftscan_plugin
    Mftscan_plugin = Menu(commands_menu, tearoff=0)
    mftscan_primary_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="--primary", variable=mftscan_primary_var, command=lambda: set_pluginAndFlag(current_command, "mftscan", "--primary"))
    mftscan_yarascanner_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="--yarascanner", variable=mftscan_yarascanner_var, command=lambda: set_pluginAndFlag(current_command, "mftscan", "--yarascanner"))
    commands_menu.add_cascade(label="Mftscan", menu=Mftscan_plugin)

    # Ads_plugin
    Ads_plugin = Menu(commands_menu, tearoff=0)
    ads_primary_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="--primary", variable=ads_primary_var, command=lambda: set_pluginAndFlag(current_command, "ads", "--primary"))
    ads_yarascanner_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="--yarascanner", variable=ads_yarascanner_var, command=lambda: set_pluginAndFlag(current_command, "ads", "--yarascanner"))
    commands_menu.add_cascade(label="Ads", menu=Ads_plugin)

    # Modscan_plugin
    Modscan_plugin = Menu(commands_menu, tearoff=0)
    modscan_kernel_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--kernel", variable=modscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "modscan", "--kernel"))
    modscan_poolscanner_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--poolscanner", variable=modscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "modscan", "--poolscanner"))
    modscan_pslist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--pslist", variable=modscan_pslist_var, command=lambda: set_pluginAndFlag(current_command, "modscan", "--pslist"))
    modscan_dlllist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--dlllist", variable=modscan_dlllist_var, command=lambda: set_pluginAndFlag(current_command, "modscan", "--dlllist"))
    modscan_dump_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--dump", variable=modscan_dump_var, command=lambda: set_pluginAndFlag(current_command, "modscan", "--dump"))
    commands_menu.add_cascade(label="Modscan", menu=Modscan_plugin)

    # Modules_plugin
    Modules_plugin = Menu(commands_menu, tearoff=0)
    modules_kernel_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--kernel", variable=modules_kernel_var, command=lambda: set_pluginAndFlag(current_command, "modules", "--kernel"))
    modules_pslist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--pslist", variable=modules_pslist_var, command=lambda: set_pluginAndFlag(current_command, "modules", "--pslist"))
    modules_dlllist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--dlllist", variable=modules_dlllist_var, command=lambda: set_pluginAndFlag(current_command, "modules", "--dlllist"))
    modules_dump_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--dump", variable=modules_dump_var, command=lambda: set_pluginAndFlag(current_command, "modules", "--dump"))
    modules_name_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--name", variable=modules_name_var, command=lambda: set_pluginAndFlag(current_command, "modules", "--name"))
    commands_menu.add_cascade(label="Modules", menu=Modules_plugin)

    # Mutantscan_plugin
    Mutantscan_plugin = Menu(commands_menu, tearoff=0)
    mutantscan_kernel_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="--kernel", variable=mutantscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "mutantscan", "--kernel"))
    mutantscan_poolscanner_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="--poolscanner", variable=mutantscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "mutantscan", "--poolscanner"))
    commands_menu.add_cascade(label="Mutantscan", menu=Mutantscan_plugin)

    # Netscan_plugin
    Netscan_plugin = Menu(commands_menu, tearoff=0)
    netscan_kernel_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--kernel", variable=netscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "netscan", "--kernel"))
    netscan_poolscanner_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--poolscanner", variable=netscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "netscan", "--poolscanner"))
    netscan_info_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--info", variable=netscan_info_var, command=lambda: set_pluginAndFlag(current_command, "netscan", "--info"))
    netscan_verinfo_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--verinfo", variable=netscan_verinfo_var, command=lambda: set_pluginAndFlag(current_command, "netscan", "--verinfo"))
    netscan_include_corrupt_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--include-corrupt", variable=netscan_include_corrupt_var, command=lambda: set_pluginAndFlag(current_command, "netscan", "--include-corrupt"))
    commands_menu.add_cascade(label="Netscan", menu=Netscan_plugin)

    # Netstat_plugin
    Netstat_plugin = Menu(commands_menu, tearoff=0)
    netstat_kernel_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--kernel", variable=netstat_kernel_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--kernel"))
    netstat_netscan_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--netscan", variable=netstat_netscan_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--netscan"))
    netstat_modules_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--modules", variable=netstat_modules_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--modules"))
    netstat_pdbutil_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--pdbutil", variable=netstat_pdbutil_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--pdbutil"))
    netstat_info_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--info", variable=netstat_info_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--info"))
    netstat_verinfo_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--verinfo", variable=netstat_verinfo_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--verinfo"))
    netstat_include_corrupt_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--include-corrupt", variable=netstat_include_corrupt_var, command=lambda: set_pluginAndFlag(current_command, "netstat", "--include-corrupt"))
    commands_menu.add_cascade(label="Netstat", menu=Netstat_plugin)

    # Poolscanner_plugin
    Poolscanner_plugin = Menu(commands_menu, tearoff=0)
    poolscanner_kernel_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="--kernel", variable=poolscanner_kernel_var, command=lambda: set_pluginAndFlag(current_command, "poolscanner", "--kernel"))
    poolscanner_handles_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="--handles", variable=poolscanner_handles_var, command=lambda: set_pluginAndFlag(current_command, "poolscanner", "--handles"))
    commands_menu.add_cascade(label="Poolscanner", menu=Poolscanner_plugin)

    # Privs_plugin
    Privs_plugin = Menu(commands_menu, tearoff=0)
    privs_kernel_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--kernel", variable=privs_kernel_var, command=lambda: set_pluginAndFlag(current_command, "privs", "--kernel"))
    privs_pid_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--pid", variable=privs_pid_var, command=lambda: set_pluginAndFlag(current_command, "privs", "--pid"))
    privs_pslist_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--pslist", variable=privs_pslist_var, command=lambda: set_pluginAndFlag(current_command, "privs", "--pslist"))
    commands_menu.add_cascade(label="Privs", menu=Privs_plugin)

    # Pslist_plugin
    Pslist_plugin = Menu(commands_menu, tearoff=0)
    pslist_kernel_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--kernel", variable=pslist_kernel_var, command=lambda: set_pluginAndFlag(current_command, "pslist", "--kernel"))
    pslist_physical_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--physical", variable=pslist_physical_var, command=lambda: set_pluginAndFlag(current_command, "pslist", "--physical"))
    pslist_pid_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--pid", variable=pslist_pid_var, command=lambda: set_pluginAndFlag(current_command, "pslist", "--pid"))
    pslist_dump_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--dump", variable=pslist_dump_var, command=lambda: set_pluginAndFlag(current_command, "pslist", "--dump"))
    commands_menu.add_cascade(label="Pslist", menu=Pslist_plugin)

    # Psscan_plugin
    Psscan_plugin = Menu(commands_menu, tearoff=0)
    psscan_kernel_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--kernel", variable=psscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--kernel"))
    psscan_pslist_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--pslist", variable=psscan_pslist_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--pslist"))
    psscan_info_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--info", variable=psscan_info_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--info"))
    psscan_pid_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--pid", variable=psscan_pid_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--pid"))
    psscan_dump_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--dump", variable=psscan_dump_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--dump"))
    psscan_physical_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--physical", variable=psscan_physical_var, command=lambda: set_pluginAndFlag(current_command, "psscan", "--physical"))
    commands_menu.add_cascade(label="Psscan", menu=Psscan_plugin)

    # Pstree_plugin
    Pstree_plugin = Menu(commands_menu, tearoff=0)
    pstree_kernel_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--kernel", variable=pstree_kernel_var, command=lambda: set_pluginAndFlag(current_command, "pstree", "--kernel"))
    pstree_physical_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--physical", variable=pstree_physical_var, command=lambda: set_pluginAndFlag(current_command, "pstree", "--physical"))
    pstree_pslist_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--pslist", variable=pstree_pslist_var, command=lambda: set_pluginAndFlag(current_command, "pstree", "--pslist"))
    pstree_pid_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--pid", variable=pstree_pid_var, command=lambda: set_pluginAndFlag(current_command, "pstree", "--pid"))
    commands_menu.add_cascade(label="Pstree", menu=Pstree_plugin)

    # Sessions_plugin
    Sessions_plugin = Menu(commands_menu, tearoff=0)
    sessions_kernel_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--kernel", variable=sessions_kernel_var, command=lambda: set_pluginAndFlag(current_command, "sessions", "--kernel"))
    sessions_pslist_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--pslist", variable=sessions_pslist_var, command=lambda: set_pluginAndFlag(current_command, "sessions", "--pslist"))
    sessions_pid_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--pid", variable=sessions_pid_var, command=lambda: set_pluginAndFlag(current_command, "sessions", "--pid"))
    commands_menu.add_cascade(label="Sessions", menu=Sessions_plugin)

    # Skeleton_key_check_plugin
    Skeleton_key_check_plugin = Menu(commands_menu, tearoff=0)
    skeleton_key_check_kernel_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--kernel", variable=skeleton_key_check_kernel_var, command=lambda: set_pluginAndFlag(current_command, "skeleton_key_check", "--kernel"))
    skeleton_key_check_pslist_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--pslist", variable=skeleton_key_check_pslist_var, command=lambda: set_pluginAndFlag(current_command, "skeleton_key_check", "--pslist"))
    skeleton_key_check_vadinfo_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--vadinfo", variable=skeleton_key_check_vadinfo_var, command=lambda: set_pluginAndFlag(current_command, "skeleton_key_check", "--vadinfo"))
    skeleton_key_check_pdbutil_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--pdbutil", variable=skeleton_key_check_pdbutil_var, command=lambda: set_pluginAndFlag(current_command, "skeleton_key_check", "--pdbutil"))
    commands_menu.add_cascade(label="Skeleton_key_check", menu=Skeleton_key_check_plugin)

    # Ssdt_plugin
    Ssdt_plugin = Menu(commands_menu, tearoff=0)
    ssdt_kernel_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="--kernel", variable=ssdt_kernel_var, command=lambda: set_pluginAndFlag(current_command, "ssdt", "--kernel"))
    ssdt_modules_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="--modules", variable=ssdt_modules_var, command=lambda: set_pluginAndFlag(current_command, "ssdt", "--modules"))
    commands_menu.add_cascade(label="Ssdt", menu=Ssdt_plugin)

    # Strings_plugin
    Strings_plugin = Menu(commands_menu, tearoff=0)
    strings_kernel_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--kernel", variable=strings_kernel_var, command=lambda: set_pluginAndFlag(current_command, "strings", "--kernel"))
    strings_pslist_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--pslist", variable=strings_pslist_var, command=lambda: set_pluginAndFlag(current_command, "strings", "--pslist"))
    strings_pid_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--pid", variable=strings_pid_var, command=lambda: set_pluginAndFlag(current_command, "strings", "--pid"))
    strings_strings_file_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--strings_file", variable=strings_strings_file_var, command=lambda: set_pluginAndFlag(current_command, "strings", "--strings_file"))
    commands_menu.add_cascade(label="Strings", menu=Strings_plugin)

    # Svcscan_plugin
    Svcscan_plugin = Menu(commands_menu, tearoff=0)
    svcscan_kernel_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--kernel", variable=svcscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "svcscan", "--kernel"))
    svcscan_pslist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--pslist", variable=svcscan_pslist_var, command=lambda: set_pluginAndFlag(current_command, "svcscan", "--pslist"))
    svcscan_poolscanner_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--poolscanner", variable=svcscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "svcscan", "--poolscanner"))
    svcscan_vadyarascan_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--vadyarascan", variable=svcscan_vadyarascan_var, command=lambda: set_pluginAndFlag(current_command, "svcscan", "--vadyarascan"))
    svcscan_hivelist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--hivelist", variable=svcscan_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "svcscan", "--hivelist"))
    commands_menu.add_cascade(label="Svcscan", menu=Svcscan_plugin)

    # Symlinkscan_plugin
    Symlinkscan_plugin = Menu(commands_menu, tearoff=0)
    symlinkscan_kernel_var = tk.BooleanVar()
    Symlinkscan_plugin.add_checkbutton(label="--kernel", variable=symlinkscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "symlinkscan", "--kernel"))
    commands_menu.add_cascade(label="Symlinkscan", menu=Symlinkscan_plugin)

    # Thrdscan_plugin
    Thrdscan_plugin = Menu(commands_menu, tearoff=0)
    thrdscan_kernel_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="--kernel", variable=thrdscan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "thrdscan", "--kernel"))
    thrdscan_poolscanner_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="--poolscanner", variable=thrdscan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "thrdscan", "--poolscanner"))
    commands_menu.add_cascade(label="Thrdscan", menu=Thrdscan_plugin)

    # Passphrase_plugin
    Passphrase_plugin = Menu(commands_menu, tearoff=0)
    passphrase_modules_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="--modules", variable=passphrase_modules_var, command=lambda: set_pluginAndFlag(current_command, "passphrase", "--modules"))
    passphrase_min_length_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="--min-length", variable=passphrase_min_length_var, command=lambda: set_pluginAndFlag(current_command, "passphrase", "--min-length"))
    commands_menu.add_cascade(label="Passphrase", menu=Passphrase_plugin)

    # Vadinfo_plugin
    Vadinfo_plugin = Menu(commands_menu, tearoff=0)
    vadinfo_kernel_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--kernel", variable=vadinfo_kernel_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--kernel"))
    vadinfo_address_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--address", variable=vadinfo_address_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--address"))
    vadinfo_pid_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--pid", variable=vadinfo_pid_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--pid"))
    vadinfo_pslist_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--pslist", variable=vadinfo_pslist_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--pslist"))
    vadinfo_dump_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--dump", variable=vadinfo_dump_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--dump"))
    vadinfo_maxsize_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--maxsize", variable=vadinfo_maxsize_var, command=lambda: set_pluginAndFlag(current_command, "vadinfo", "--maxsize"))
    commands_menu.add_cascade(label="Vadinfo", menu=Vadinfo_plugin)

    # Vadwalk_plugin
    Vadwalk_plugin = Menu(commands_menu, tearoff=0)
    vadwalk_kernel_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--kernel", variable=vadwalk_kernel_var, command=lambda: set_pluginAndFlag(current_command, "vadwalk", "--kernel"))
    vadwalk_pslist_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--pslist", variable=vadwalk_pslist_var, command=lambda: set_pluginAndFlag(current_command, "vadwalk", "--pslist"))
    vadwalk_vadinfo_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--vadinfo", variable=vadwalk_vadinfo_var, command=lambda: set_pluginAndFlag(current_command, "vadwalk", "--vadinfo"))
    vadwalk_pid_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--pid", variable=vadwalk_pid_var, command=lambda: set_pluginAndFlag(current_command, "vadwalk", "--pid"))
    commands_menu.add_cascade(label="Vadwalk", menu=Vadwalk_plugin)

    # Vadyarascan_plugin
    Vadyarascan_plugin = Menu(commands_menu, tearoff=0)
    commands_menu.add_cascade(label="Vadyarascan", menu=Vadyarascan_plugin)

    # Verinfo_plugin
    Verinfo_plugin = Menu(commands_menu, tearoff=0)
    verinfo_kernel_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--kernel", variable=verinfo_kernel_var, command=lambda: set_pluginAndFlag(current_command, "verinfo", "--kernel"))
    verinfo_pslist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--pslist", variable=verinfo_pslist_var, command=lambda: set_pluginAndFlag(current_command, "verinfo", "--pslist"))
    verinfo_modules_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--modules", variable=verinfo_modules_var, command=lambda: set_pluginAndFlag(current_command, "verinfo", "--modules"))
    verinfo_dlllist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--dlllist", variable=verinfo_dlllist_var, command=lambda: set_pluginAndFlag(current_command, "verinfo", "--dlllist"))
    verinfo_extensive_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--extensive", variable=verinfo_extensive_var, command=lambda: set_pluginAndFlag(current_command, "verinfo", "--extensive"))
    commands_menu.add_cascade(label="Verinfo", menu=Verinfo_plugin)

    # Virtmap_plugin
    Virtmap_plugin = Menu(commands_menu, tearoff=0)
    virtmap_kernel_var = tk.BooleanVar()
    Virtmap_plugin.add_checkbutton(label="--kernel", variable=virtmap_kernel_var, command=lambda: set_pluginAndFlag(current_command, "virtmap", "--kernel"))
    commands_menu.add_cascade(label="Virtmap", menu=Virtmap_plugin)

    # Hivelist_plugin
    Hivelist_plugin = Menu(commands_menu, tearoff=0)
    hivelist_kernel_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--kernel", variable=hivelist_kernel_var, command=lambda: set_pluginAndFlag(current_command, "hivelist", "--kernel"))
    hivelist_filter_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--filter", variable=hivelist_filter_var, command=lambda: set_pluginAndFlag(current_command, "hivelist", "--filter"))
    hivelist_hivescan_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--hivescan", variable=hivelist_hivescan_var, command=lambda: set_pluginAndFlag(current_command, "hivelist", "--hivescan"))
    hivelist_dump_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--dump", variable=hivelist_dump_var, command=lambda: set_pluginAndFlag(current_command, "hivelist", "--dump"))
    commands_menu.add_cascade(label="Hivelist", menu=Hivelist_plugin)

    # Hivescan_plugin
    Hivescan_plugin = Menu(commands_menu, tearoff=0)
    hivescan_kernel_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--kernel", variable=hivescan_kernel_var, command=lambda: set_pluginAndFlag(current_command, "hivescan", "--kernel"))
    hivescan_poolscanner_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--poolscanner", variable=hivescan_poolscanner_var, command=lambda: set_pluginAndFlag(current_command, "hivescan", "--poolscanner"))
    hivescan_bigpools_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--bigpools", variable=hivescan_bigpools_var, command=lambda: set_pluginAndFlag(current_command, "hivescan", "--bigpools"))
    commands_menu.add_cascade(label="Hivescan", menu=Hivescan_plugin)

    # Printkey_plugin
    Printkey_plugin = Menu(commands_menu, tearoff=0)
    printkey_kernel_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--kernel", variable=printkey_kernel_var, command=lambda: set_pluginAndFlag(current_command, "printkey", "--kernel"))
    printkey_hivelist_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--hivelist", variable=printkey_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "printkey", "--hivelist"))
    printkey_offset_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--offset", variable=printkey_offset_var, command=lambda: set_pluginAndFlag(current_command, "printkey", "--offset"))
    printkey_key_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--key", variable=printkey_key_var, command=lambda: set_pluginAndFlag(current_command, "printkey", "--key"))
    printkey_recurse_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--recurse", variable=printkey_recurse_var, command=lambda: set_pluginAndFlag(current_command, "printkey", "--recurse"))
    commands_menu.add_cascade(label="Printkey", menu=Printkey_plugin)

    # Userassist_plugin
    Userassist_plugin = Menu(commands_menu, tearoff=0)
    userassist_kernel_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--kernel", variable=userassist_kernel_var, command=lambda: set_pluginAndFlag(current_command, "userassist", "--kernel"))
    userassist_offset_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--offset", variable=userassist_offset_var, command=lambda: set_pluginAndFlag(current_command, "userassist", "--offset"))
    userassist_hivelist_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--hivelist", variable=userassist_hivelist_var, command=lambda: set_pluginAndFlag(current_command, "userassist", "--hivelist"))
    commands_menu.add_cascade(label="Userassist", menu=Userassist_plugin)



    commands_button = ttk.Menubutton(frame_center, text="Commands", menu=commands_menu, )
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

    select_button = ttk.Button(frame_right, text="Get Selected Command",
                               command=lambda: get_selected_command(prevCommandList, text_with_line_numbers, History,
                                                                    mid_text_field))
    select_button.grid(row=2, column=0, columnspan=2, pady=5)

    prevCommandList.pack()

    # Widgets in frame_mid
    mid_text_field = ttk.Entry(frame_mid, width=100)
    mid_text_field.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    mid_text_field.insert(0, "filename.txt / dlllist / --offset")
    prevCommandList.bind("<<ListboxSelect>>",
                         get_selected_command(prevCommandList, text_with_line_numbers, History, mid_text_field))

    run_button = ttk.Button(frame_mid, text="Run",
                            command=lambda: run_command(current_command, text_with_line_numbers, prevCommandList,
                                                        mid_text_field))
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
