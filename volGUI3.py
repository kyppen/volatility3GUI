import tkinter as tk
from tkinter import ttk, Menu, filedialog, simpledialog
import platform
import subprocess
import FileHandling
import textBoxNumbers
import command as cmd
import re


# import intro


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


# uses system specific file browser
def browse_files(command_list, path_entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
        add_filepath_to_command(file_path, command_list)


def get_selected_command(listbox, output_text, info, mid_text_field):
    print("get_selected_command()")
    for i in listbox.curselection():
        # print(f"index {i}")
        print(listbox.get(i))
        update_selected_from_history(listbox.get(i), mid_text_field)
        print(info[0])
        print(len(info))
        # print(info[1])
        output_text.text.delete(1.0, tk.END)
        output_text.text.insert(1.0, info[i].get_output())


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
    # for i in range(total_steps):
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
    global path_entry, selected_entry, cmd_var, flag_var, os_var, output_text, progress_bar, progress_label, os_entry, mid_text_field
    command_list = []
    command_list = reset_command_list(command_list)
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
    Bigpools_plugin.add_checkbutton(label="--kernel", variable=bigpools_kernel_var,
                                    command=lambda: add_to_command("bigpools", "--kernel", command_list))
    bigpools_tags_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="--tags", variable=bigpools_tags_var,
                                    command=lambda: add_to_command("bigpools", "--tags", command_list))
    bigpools_show_free_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="--show-free", variable=bigpools_show_free_var,
                                    command=lambda: add_to_command("bigpools", "--show-free", command_list))
    commands_menu.add_cascade(label="Bigpools", menu=Bigpools_plugin)

    # Cachedump_plugin
    Cachedump_plugin = Menu(commands_menu, tearoff=0)
    cachedump_kernel_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--kernel", variable=cachedump_kernel_var,
                                     command=lambda: add_to_command("cachedump", "--kernel", command_list))
    cachedump_hivelist_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--hivelist", variable=cachedump_hivelist_var,
                                     command=lambda: add_to_command("cachedump", "--hivelist", command_list))
    cachedump_lsadump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--lsadump", variable=cachedump_lsadump_var,
                                     command=lambda: add_to_command("cachedump", "--lsadump", command_list))
    cachedump_hashdump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="--hashdump", variable=cachedump_hashdump_var,
                                     command=lambda: add_to_command("cachedump", "--hashdump", command_list))
    commands_menu.add_cascade(label="Cachedump", menu=Cachedump_plugin)

    # Callbacks_plugin
    Callbacks_plugin = Menu(commands_menu, tearoff=0)
    callbacks_kernel_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="--kernel", variable=callbacks_kernel_var,
                                     command=lambda: add_to_command("callbacks", "--kernel", command_list))
    callbacks_ssdt_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="--ssdt", variable=callbacks_ssdt_var,
                                     command=lambda: add_to_command("callbacks", "--ssdt", command_list))
    commands_menu.add_cascade(label="Callbacks", menu=Callbacks_plugin)

    # Cmdline_plugin
    Cmdline_plugin = Menu(commands_menu, tearoff=0)
    cmdline_kernel_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--kernel", variable=cmdline_kernel_var,
                                   command=lambda: add_to_command("cmdline", "--kernel", command_list))
    cmdline_pslist_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--pslist", variable=cmdline_pslist_var,
                                   command=lambda: add_to_command("cmdline", "--pslist", command_list))
    cmdline_pid_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="--pid", variable=cmdline_pid_var,
                                   command=lambda: add_to_command("cmdline", "--pid", command_list))
    commands_menu.add_cascade(label="Cmdline", menu=Cmdline_plugin)

    # Crashinfo_plugin
    Crashinfo_plugin = Menu(commands_menu, tearoff=0)
    crashinfo_primary_var = tk.BooleanVar()
    Crashinfo_plugin.add_checkbutton(label="--primary", variable=crashinfo_primary_var,
                                     command=lambda: add_to_command("crashinfo", "--primary", command_list))
    commands_menu.add_cascade(label="Crashinfo", menu=Crashinfo_plugin)

    # Devicetree_plugin
    Devicetree_plugin = Menu(commands_menu, tearoff=0)
    devicetree_kernel_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="--kernel", variable=devicetree_kernel_var,
                                      command=lambda: add_to_command("devicetree", "--kernel", command_list))
    devicetree_driverscan_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="--driverscan", variable=devicetree_driverscan_var,
                                      command=lambda: add_to_command("devicetree", "--driverscan", command_list))
    commands_menu.add_cascade(label="Devicetree", menu=Devicetree_plugin)

    # Dlllist_plugin
    Dlllist_plugin = Menu(commands_menu, tearoff=0)
    dlllist_kernel_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--kernel", variable=dlllist_kernel_var,
                                   command=lambda: add_to_command("dlllist", "--kernel", command_list))
    dlllist_pslist_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--pslist", variable=dlllist_pslist_var,
                                   command=lambda: add_to_command("dlllist", "--pslist", command_list))
    dlllist_psscan_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--psscan", variable=dlllist_psscan_var,
                                   command=lambda: add_to_command("dlllist", "--psscan", command_list))
    dlllist_info_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--info", variable=dlllist_info_var,
                                   command=lambda: add_to_command("dlllist", "--info", command_list))
    dlllist_pid_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--pid", variable=dlllist_pid_var,
                                   command=lambda: add_to_command("dlllist", "--pid", command_list))
    dlllist_offset_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--offset", variable=dlllist_offset_var,
                                   command=lambda: add_to_command("dlllist", "--offset", command_list))
    dlllist_dump_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="--dump", variable=dlllist_dump_var,
                                   command=lambda: add_to_command("dlllist", "--dump", command_list))
    commands_menu.add_cascade(label="Dlllist", menu=Dlllist_plugin)

    # Driverirp_plugin
    Driverirp_plugin = Menu(commands_menu, tearoff=0)
    driverirp_kernel_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--kernel", variable=driverirp_kernel_var,
                                     command=lambda: add_to_command("driverirp", "--kernel", command_list))
    driverirp_ssdt_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--ssdt", variable=driverirp_ssdt_var,
                                     command=lambda: add_to_command("driverirp", "--ssdt", command_list))
    driverirp_driverscan_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="--driverscan", variable=driverirp_driverscan_var,
                                     command=lambda: add_to_command("driverirp", "--driverscan", command_list))
    commands_menu.add_cascade(label="Driverirp", menu=Driverirp_plugin)

    # Drivermodule_plugin
    Drivermodule_plugin = Menu(commands_menu, tearoff=0)
    drivermodule_kernel_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--kernel", variable=drivermodule_kernel_var,
                                        command=lambda: add_to_command("drivermodule", "--kernel", command_list))
    drivermodule_ssdt_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--ssdt", variable=drivermodule_ssdt_var,
                                        command=lambda: add_to_command("drivermodule", "--ssdt", command_list))
    drivermodule_driverscan_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="--driverscan", variable=drivermodule_driverscan_var,
                                        command=lambda: add_to_command("drivermodule", "--driverscan", command_list))
    commands_menu.add_cascade(label="Drivermodule", menu=Drivermodule_plugin)

    # Driverscan_plugin
    Driverscan_plugin = Menu(commands_menu, tearoff=0)
    driverscan_kernel_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="--kernel", variable=driverscan_kernel_var,
                                      command=lambda: add_to_command("driverscan", "--kernel", command_list))
    driverscan_poolscanner_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="--poolscanner", variable=driverscan_poolscanner_var,
                                      command=lambda: add_to_command("driverscan", "--poolscanner", command_list))
    commands_menu.add_cascade(label="Driverscan", menu=Driverscan_plugin)

    # Dumpfiles_plugin
    Dumpfiles_plugin = Menu(commands_menu, tearoff=0)
    dumpfiles_kernel_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--kernel", variable=dumpfiles_kernel_var,
                                     command=lambda: add_to_command("dumpfiles", "--kernel", command_list))
    dumpfiles_pid_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--pid", variable=dumpfiles_pid_var,
                                     command=lambda: add_to_command("dumpfiles", "--pid", command_list))
    dumpfiles_virtaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--virtaddr", variable=dumpfiles_virtaddr_var,
                                     command=lambda: add_to_command("dumpfiles", "--virtaddr", command_list))
    dumpfiles_physaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--physaddr", variable=dumpfiles_physaddr_var,
                                     command=lambda: add_to_command("dumpfiles", "--physaddr", command_list))
    dumpfiles_filter_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--filter", variable=dumpfiles_filter_var,
                                     command=lambda: add_to_command("dumpfiles", "--filter", command_list))
    dumpfiles_ignore_case_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--ignore-case", variable=dumpfiles_ignore_case_var,
                                     command=lambda: add_to_command("dumpfiles", "--ignore-case", command_list))
    dumpfiles_pslist_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--pslist", variable=dumpfiles_pslist_var,
                                     command=lambda: add_to_command("dumpfiles", "--pslist", command_list))
    dumpfiles_handles_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="--handles", variable=dumpfiles_handles_var,
                                     command=lambda: add_to_command("dumpfiles", "--handles", command_list))
    commands_menu.add_cascade(label="Dumpfiles", menu=Dumpfiles_plugin)

    # Envars_plugin
    Envars_plugin = Menu(commands_menu, tearoff=0)
    envars_kernel_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--kernel", variable=envars_kernel_var,
                                  command=lambda: add_to_command("envars", "--kernel", command_list))
    envars_pid_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--pid", variable=envars_pid_var,
                                  command=lambda: add_to_command("envars", "--pid", command_list))
    envars_silent_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--silent", variable=envars_silent_var,
                                  command=lambda: add_to_command("envars", "--silent", command_list))
    envars_pslist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--pslist", variable=envars_pslist_var,
                                  command=lambda: add_to_command("envars", "--pslist", command_list))
    envars_hivelist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="--hivelist", variable=envars_hivelist_var,
                                  command=lambda: add_to_command("envars", "--hivelist", command_list))
    commands_menu.add_cascade(label="Envars", menu=Envars_plugin)

    # Filescan_plugin
    Filescan_plugin = Menu(commands_menu, tearoff=0)
    filescan_kernel_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="--kernel", variable=filescan_kernel_var,
                                    command=lambda: add_to_command("filescan", "--kernel", command_list))
    filescan_poolscanner_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="--poolscanner", variable=filescan_poolscanner_var,
                                    command=lambda: add_to_command("filescan", "--poolscanner", command_list))
    commands_menu.add_cascade(label="Filescan", menu=Filescan_plugin)

    # Getservicesids_plugin
    Getservicesids_plugin = Menu(commands_menu, tearoff=0)
    getservicesids_kernel_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="--kernel", variable=getservicesids_kernel_var,
                                          command=lambda: add_to_command("getservicesids", "--kernel", command_list))
    getservicesids_hivelist_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="--hivelist", variable=getservicesids_hivelist_var,
                                          command=lambda: add_to_command("getservicesids", "--hivelist", command_list))
    commands_menu.add_cascade(label="Getservicesids", menu=Getservicesids_plugin)

    # Getsids_plugin
    Getsids_plugin = Menu(commands_menu, tearoff=0)
    getsids_kernel_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--kernel", variable=getsids_kernel_var,
                                   command=lambda: add_to_command("getsids", "--kernel", command_list))
    getsids_pid_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--pid", variable=getsids_pid_var,
                                   command=lambda: add_to_command("getsids", "--pid", command_list))
    getsids_pslist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--pslist", variable=getsids_pslist_var,
                                   command=lambda: add_to_command("getsids", "--pslist", command_list))
    getsids_hivelist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="--hivelist", variable=getsids_hivelist_var,
                                   command=lambda: add_to_command("getsids", "--hivelist", command_list))
    commands_menu.add_cascade(label="Getsids", menu=Getsids_plugin)

    # Handles_plugin
    Handles_plugin = Menu(commands_menu, tearoff=0)
    handles_kernel_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--kernel", variable=handles_kernel_var,
                                   command=lambda: add_to_command("handles", "--kernel", command_list))
    handles_pslist_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--pslist", variable=handles_pslist_var,
                                   command=lambda: add_to_command("handles", "--pslist", command_list))
    handles_psscan_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--psscan", variable=handles_psscan_var,
                                   command=lambda: add_to_command("handles", "--psscan", command_list))
    handles_pid_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--pid", variable=handles_pid_var,
                                   command=lambda: add_to_command("handles", "--pid", command_list))
    handles_offset_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="--offset", variable=handles_offset_var,
                                   command=lambda: add_to_command("handles", "--offset", command_list))
    commands_menu.add_cascade(label="Handles", menu=Handles_plugin)

    # Hashdump_plugin
    Hashdump_plugin = Menu(commands_menu, tearoff=0)
    hashdump_kernel_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="--kernel", variable=hashdump_kernel_var,
                                    command=lambda: add_to_command("hashdump", "--kernel", command_list))
    hashdump_hivelist_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="--hivelist", variable=hashdump_hivelist_var,
                                    command=lambda: add_to_command("hashdump", "--hivelist", command_list))
    commands_menu.add_cascade(label="Hashdump", menu=Hashdump_plugin)

    # Iat_plugin
    Iat_plugin = Menu(commands_menu, tearoff=0)
    iat_kernel_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--kernel", variable=iat_kernel_var,
                               command=lambda: add_to_command("iat", "--kernel", command_list))
    iat_pslist_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--pslist", variable=iat_pslist_var,
                               command=lambda: add_to_command("iat", "--pslist", command_list))
    iat_pid_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="--pid", variable=iat_pid_var,
                               command=lambda: add_to_command("iat", "--pid", command_list))
    commands_menu.add_cascade(label="Iat", menu=Iat_plugin)

    # Info_plugin
    Info_plugin = Menu(commands_menu, tearoff=0)
    info_kernel_var = tk.BooleanVar()
    Info_plugin.add_checkbutton(label="--kernel", variable=info_kernel_var,
                                command=lambda: add_to_command("info", "--kernel", command_list))
    commands_menu.add_cascade(label="Info", menu=Info_plugin)

    # Joblinks_plugin
    Joblinks_plugin = Menu(commands_menu, tearoff=0)
    joblinks_kernel_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--kernel", variable=joblinks_kernel_var,
                                    command=lambda: add_to_command("joblinks", "--kernel", command_list))
    joblinks_physical_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--physical", variable=joblinks_physical_var,
                                    command=lambda: add_to_command("joblinks", "--physical", command_list))
    joblinks_pslist_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="--pslist", variable=joblinks_pslist_var,
                                    command=lambda: add_to_command("joblinks", "--pslist", command_list))
    commands_menu.add_cascade(label="Joblinks", menu=Joblinks_plugin)

    # Ldrmodules_plugin
    Ldrmodules_plugin = Menu(commands_menu, tearoff=0)
    ldrmodules_kernel_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--kernel", variable=ldrmodules_kernel_var,
                                      command=lambda: add_to_command("ldrmodules", "--kernel", command_list))
    ldrmodules_pslist_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--pslist", variable=ldrmodules_pslist_var,
                                      command=lambda: add_to_command("ldrmodules", "--pslist", command_list))
    ldrmodules_vadinfo_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--vadinfo", variable=ldrmodules_vadinfo_var,
                                      command=lambda: add_to_command("ldrmodules", "--vadinfo", command_list))
    ldrmodules_pid_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="--pid", variable=ldrmodules_pid_var,
                                      command=lambda: add_to_command("ldrmodules", "--pid", command_list))
    commands_menu.add_cascade(label="Ldrmodules", menu=Ldrmodules_plugin)

    # Lsadump_plugin
    Lsadump_plugin = Menu(commands_menu, tearoff=0)
    lsadump_kernel_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--kernel", variable=lsadump_kernel_var,
                                   command=lambda: add_to_command("lsadump", "--kernel", command_list))
    lsadump_hashdump_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--hashdump", variable=lsadump_hashdump_var,
                                   command=lambda: add_to_command("lsadump", "--hashdump", command_list))
    lsadump_hivelist_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="--hivelist", variable=lsadump_hivelist_var,
                                   command=lambda: add_to_command("lsadump", "--hivelist", command_list))
    commands_menu.add_cascade(label="Lsadump", menu=Lsadump_plugin)

    # Malfind_plugin
    Malfind_plugin = Menu(commands_menu, tearoff=0)
    malfind_kernel_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--kernel", variable=malfind_kernel_var,
                                   command=lambda: add_to_command("malfind", "--kernel", command_list))
    malfind_pid_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--pid", variable=malfind_pid_var,
                                   command=lambda: add_to_command("malfind", "--pid", command_list))
    malfind_dump_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--dump", variable=malfind_dump_var,
                                   command=lambda: add_to_command("malfind", "--dump", command_list))
    malfind_pslist_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--pslist", variable=malfind_pslist_var,
                                   command=lambda: add_to_command("malfind", "--pslist", command_list))
    malfind_vadinfo_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="--vadinfo", variable=malfind_vadinfo_var,
                                   command=lambda: add_to_command("malfind", "--vadinfo", command_list))
    commands_menu.add_cascade(label="Malfind", menu=Malfind_plugin)

    # Mbrscan_plugin
    Mbrscan_plugin = Menu(commands_menu, tearoff=0)
    mbrscan_kernel_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="--kernel", variable=mbrscan_kernel_var,
                                   command=lambda: add_to_command("mbrscan", "--kernel", command_list))
    mbrscan_full_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="--full", variable=mbrscan_full_var,
                                   command=lambda: add_to_command("mbrscan", "--full", command_list))
    commands_menu.add_cascade(label="Mbrscan", menu=Mbrscan_plugin)

    # Memmap_plugin
    Memmap_plugin = Menu(commands_menu, tearoff=0)
    memmap_kernel_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--kernel", variable=memmap_kernel_var,
                                  command=lambda: add_to_command("memmap", "--kernel", command_list))
    memmap_pslist_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--pslist", variable=memmap_pslist_var,
                                  command=lambda: add_to_command("memmap", "--pslist", command_list))
    memmap_pid_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--pid", variable=memmap_pid_var,
                                  command=lambda: add_to_command("memmap", "--pid", command_list))
    memmap_dump_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="--dump", variable=memmap_dump_var,
                                  command=lambda: add_to_command("memmap", "--dump", command_list))
    commands_menu.add_cascade(label="Memmap", menu=Memmap_plugin)

    # Mftscan_plugin
    Mftscan_plugin = Menu(commands_menu, tearoff=0)
    mftscan_primary_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="--primary", variable=mftscan_primary_var,
                                   command=lambda: add_to_command("mftscan", "--primary", command_list))
    mftscan_yarascanner_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="--yarascanner", variable=mftscan_yarascanner_var,
                                   command=lambda: add_to_command("mftscan", "--yarascanner", command_list))
    commands_menu.add_cascade(label="Mftscan", menu=Mftscan_plugin)

    # Ads_plugin
    Ads_plugin = Menu(commands_menu, tearoff=0)
    ads_primary_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="--primary", variable=ads_primary_var,
                               command=lambda: add_to_command("ads", "--primary", command_list))
    ads_yarascanner_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="--yarascanner", variable=ads_yarascanner_var,
                               command=lambda: add_to_command("ads", "--yarascanner", command_list))
    commands_menu.add_cascade(label="Ads", menu=Ads_plugin)

    # Modscan_plugin
    Modscan_plugin = Menu(commands_menu, tearoff=0)
    modscan_kernel_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--kernel", variable=modscan_kernel_var,
                                   command=lambda: add_to_command("modscan", "--kernel", command_list))
    modscan_poolscanner_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--poolscanner", variable=modscan_poolscanner_var,
                                   command=lambda: add_to_command("modscan", "--poolscanner", command_list))
    modscan_pslist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--pslist", variable=modscan_pslist_var,
                                   command=lambda: add_to_command("modscan", "--pslist", command_list))
    modscan_dlllist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--dlllist", variable=modscan_dlllist_var,
                                   command=lambda: add_to_command("modscan", "--dlllist", command_list))
    modscan_dump_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="--dump", variable=modscan_dump_var,
                                   command=lambda: add_to_command("modscan", "--dump", command_list))
    commands_menu.add_cascade(label="Modscan", menu=Modscan_plugin)

    # Modules_plugin
    Modules_plugin = Menu(commands_menu, tearoff=0)
    modules_kernel_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--kernel", variable=modules_kernel_var,
                                   command=lambda: add_to_command("modules", "--kernel", command_list))
    modules_pslist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--pslist", variable=modules_pslist_var,
                                   command=lambda: add_to_command("modules", "--pslist", command_list))
    modules_dlllist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--dlllist", variable=modules_dlllist_var,
                                   command=lambda: add_to_command("modules", "--dlllist", command_list))
    modules_dump_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--dump", variable=modules_dump_var,
                                   command=lambda: add_to_command("modules", "--dump", command_list))
    modules_name_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="--name", variable=modules_name_var,
                                   command=lambda: add_to_command("modules", "--name", command_list))
    commands_menu.add_cascade(label="Modules", menu=Modules_plugin)

    # Mutantscan_plugin
    Mutantscan_plugin = Menu(commands_menu, tearoff=0)
    mutantscan_kernel_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="--kernel", variable=mutantscan_kernel_var,
                                      command=lambda: add_to_command("mutantscan", "--kernel", command_list))
    mutantscan_poolscanner_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="--poolscanner", variable=mutantscan_poolscanner_var,
                                      command=lambda: add_to_command("mutantscan", "--poolscanner", command_list))
    commands_menu.add_cascade(label="Mutantscan", menu=Mutantscan_plugin)

    # Netscan_plugin
    Netscan_plugin = Menu(commands_menu, tearoff=0)
    netscan_kernel_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--kernel", variable=netscan_kernel_var,
                                   command=lambda: add_to_command("netscan", "--kernel", command_list))
    netscan_poolscanner_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--poolscanner", variable=netscan_poolscanner_var,
                                   command=lambda: add_to_command("netscan", "--poolscanner", command_list))
    netscan_info_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--info", variable=netscan_info_var,
                                   command=lambda: add_to_command("netscan", "--info", command_list))
    netscan_verinfo_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--verinfo", variable=netscan_verinfo_var,
                                   command=lambda: add_to_command("netscan", "--verinfo", command_list))
    netscan_include_corrupt_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="--include-corrupt", variable=netscan_include_corrupt_var,
                                   command=lambda: add_to_command("netscan", "--include-corrupt", command_list))
    commands_menu.add_cascade(label="Netscan", menu=Netscan_plugin)

    # Netstat_plugin
    Netstat_plugin = Menu(commands_menu, tearoff=0)
    netstat_kernel_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--kernel", variable=netstat_kernel_var,
                                   command=lambda: add_to_command("netstat", "--kernel", command_list))
    netstat_netscan_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--netscan", variable=netstat_netscan_var,
                                   command=lambda: add_to_command("netstat", "--netscan", command_list))
    netstat_modules_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--modules", variable=netstat_modules_var,
                                   command=lambda: add_to_command("netstat", "--modules", command_list))
    netstat_pdbutil_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--pdbutil", variable=netstat_pdbutil_var,
                                   command=lambda: add_to_command("netstat", "--pdbutil", command_list))
    netstat_info_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--info", variable=netstat_info_var,
                                   command=lambda: add_to_command("netstat", "--info", command_list))
    netstat_verinfo_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--verinfo", variable=netstat_verinfo_var,
                                   command=lambda: add_to_command("netstat", "--verinfo", command_list))
    netstat_include_corrupt_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="--include-corrupt", variable=netstat_include_corrupt_var,
                                   command=lambda: add_to_command("netstat", "--include-corrupt", command_list))
    commands_menu.add_cascade(label="Netstat", menu=Netstat_plugin)

    # Poolscanner_plugin
    Poolscanner_plugin = Menu(commands_menu, tearoff=0)
    poolscanner_kernel_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="--kernel", variable=poolscanner_kernel_var,
                                       command=lambda: add_to_command("poolscanner", "--kernel", command_list))
    poolscanner_handles_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="--handles", variable=poolscanner_handles_var,
                                       command=lambda: add_to_command("poolscanner", "--handles", command_list))
    commands_menu.add_cascade(label="Poolscanner", menu=Poolscanner_plugin)

    # Privs_plugin
    Privs_plugin = Menu(commands_menu, tearoff=0)
    privs_kernel_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--kernel", variable=privs_kernel_var,
                                 command=lambda: add_to_command("privs", "--kernel", command_list))
    privs_pid_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--pid", variable=privs_pid_var,
                                 command=lambda: add_to_command("privs", "--pid", command_list))
    privs_pslist_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="--pslist", variable=privs_pslist_var,
                                 command=lambda: add_to_command("privs", "--pslist", command_list))
    commands_menu.add_cascade(label="Privs", menu=Privs_plugin)

    # Pslist_plugin
    Pslist_plugin = Menu(commands_menu, tearoff=0)
    pslist_kernel_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--kernel", variable=pslist_kernel_var,
                                  command=lambda: add_to_command("pslist", "--kernel", command_list))
    pslist_physical_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--physical", variable=pslist_physical_var,
                                  command=lambda: add_to_command("pslist", "--physical", command_list))
    pslist_pid_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--pid", variable=pslist_pid_var,
                                  command=lambda: add_to_command("pslist", "--pid", command_list))
    pslist_dump_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="--dump", variable=pslist_dump_var,
                                  command=lambda: add_to_command("pslist", "--dump", command_list))
    commands_menu.add_cascade(label="Pslist", menu=Pslist_plugin)

    # Psscan_plugin
    Psscan_plugin = Menu(commands_menu, tearoff=0)
    psscan_kernel_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--kernel", variable=psscan_kernel_var,
                                  command=lambda: add_to_command("psscan", "--kernel", command_list))
    psscan_pslist_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--pslist", variable=psscan_pslist_var,
                                  command=lambda: add_to_command("psscan", "--pslist", command_list))
    psscan_info_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--info", variable=psscan_info_var,
                                  command=lambda: add_to_command("psscan", "--info", command_list))
    psscan_pid_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--pid", variable=psscan_pid_var,
                                  command=lambda: add_to_command("psscan", "--pid", command_list))
    psscan_dump_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--dump", variable=psscan_dump_var,
                                  command=lambda: add_to_command("psscan", "--dump", command_list))
    psscan_physical_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="--physical", variable=psscan_physical_var,
                                  command=lambda: add_to_command("psscan", "--physical", command_list))
    commands_menu.add_cascade(label="Psscan", menu=Psscan_plugin)

    # Pstree_plugin
    Pstree_plugin = Menu(commands_menu, tearoff=0)
    pstree_kernel_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--kernel", variable=pstree_kernel_var,
                                  command=lambda: add_to_command("pstree", "--kernel", command_list))
    pstree_physical_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--physical", variable=pstree_physical_var,
                                  command=lambda: add_to_command("pstree", "--physical", command_list))
    pstree_pslist_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--pslist", variable=pstree_pslist_var,
                                  command=lambda: add_to_command("pstree", "--pslist", command_list))
    pstree_pid_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="--pid", variable=pstree_pid_var,
                                  command=lambda: add_to_command("pstree", "--pid", command_list))
    commands_menu.add_cascade(label="Pstree", menu=Pstree_plugin)

    # Sessions_plugin
    Sessions_plugin = Menu(commands_menu, tearoff=0)
    sessions_kernel_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--kernel", variable=sessions_kernel_var,
                                    command=lambda: add_to_command("sessions", "--kernel", command_list))
    sessions_pslist_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--pslist", variable=sessions_pslist_var,
                                    command=lambda: add_to_command("sessions", "--pslist", command_list))
    sessions_pid_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="--pid", variable=sessions_pid_var,
                                    command=lambda: add_to_command("sessions", "--pid", command_list))
    commands_menu.add_cascade(label="Sessions", menu=Sessions_plugin)

    # Skeleton_key_check_plugin
    Skeleton_key_check_plugin = Menu(commands_menu, tearoff=0)
    skeleton_key_check_kernel_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--kernel", variable=skeleton_key_check_kernel_var,
                                              command=lambda: add_to_command("skeleton_key_check", "--kernel",
                                                                             command_list))
    skeleton_key_check_pslist_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--pslist", variable=skeleton_key_check_pslist_var,
                                              command=lambda: add_to_command("skeleton_key_check", "--pslist",
                                                                             command_list))
    skeleton_key_check_vadinfo_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--vadinfo", variable=skeleton_key_check_vadinfo_var,
                                              command=lambda: add_to_command("skeleton_key_check", "--vadinfo",
                                                                             command_list))
    skeleton_key_check_pdbutil_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="--pdbutil", variable=skeleton_key_check_pdbutil_var,
                                              command=lambda: add_to_command("skeleton_key_check", "--pdbutil",
                                                                             command_list))
    commands_menu.add_cascade(label="Skeleton_key_check", menu=Skeleton_key_check_plugin)

    # Ssdt_plugin
    Ssdt_plugin = Menu(commands_menu, tearoff=0)
    ssdt_kernel_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="--kernel", variable=ssdt_kernel_var,
                                command=lambda: add_to_command("ssdt", "--kernel", command_list))
    ssdt_modules_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="--modules", variable=ssdt_modules_var,
                                command=lambda: add_to_command("ssdt", "--modules", command_list))
    commands_menu.add_cascade(label="Ssdt", menu=Ssdt_plugin)

    # Strings_plugin
    Strings_plugin = Menu(commands_menu, tearoff=0)
    strings_kernel_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--kernel", variable=strings_kernel_var,
                                   command=lambda: add_to_command("strings", "--kernel", command_list))
    strings_pslist_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--pslist", variable=strings_pslist_var,
                                   command=lambda: add_to_command("strings", "--pslist", command_list))
    strings_pid_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--pid", variable=strings_pid_var,
                                   command=lambda: add_to_command("strings", "--pid", command_list))
    strings_strings_file_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="--strings_file", variable=strings_strings_file_var,
                                   command=lambda: add_to_command("strings", "--strings_file", command_list))
    commands_menu.add_cascade(label="Strings", menu=Strings_plugin)

    # Svcscan_plugin
    Svcscan_plugin = Menu(commands_menu, tearoff=0)
    svcscan_kernel_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--kernel", variable=svcscan_kernel_var,
                                   command=lambda: add_to_command("svcscan", "--kernel", command_list))
    svcscan_pslist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--pslist", variable=svcscan_pslist_var,
                                   command=lambda: add_to_command("svcscan", "--pslist", command_list))
    svcscan_poolscanner_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--poolscanner", variable=svcscan_poolscanner_var,
                                   command=lambda: add_to_command("svcscan", "--poolscanner", command_list))
    svcscan_vadyarascan_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--vadyarascan", variable=svcscan_vadyarascan_var,
                                   command=lambda: add_to_command("svcscan", "--vadyarascan", command_list))
    svcscan_hivelist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="--hivelist", variable=svcscan_hivelist_var,
                                   command=lambda: add_to_command("svcscan", "--hivelist", command_list))
    commands_menu.add_cascade(label="Svcscan", menu=Svcscan_plugin)

    # Symlinkscan_plugin
    Symlinkscan_plugin = Menu(commands_menu, tearoff=0)
    symlinkscan_kernel_var = tk.BooleanVar()
    Symlinkscan_plugin.add_checkbutton(label="--kernel", variable=symlinkscan_kernel_var,
                                       command=lambda: add_to_command("symlinkscan", "--kernel", command_list))
    commands_menu.add_cascade(label="Symlinkscan", menu=Symlinkscan_plugin)

    # Thrdscan_plugin
    Thrdscan_plugin = Menu(commands_menu, tearoff=0)
    thrdscan_kernel_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="--kernel", variable=thrdscan_kernel_var,
                                    command=lambda: add_to_command("thrdscan", "--kernel", command_list))
    thrdscan_poolscanner_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="--poolscanner", variable=thrdscan_poolscanner_var,
                                    command=lambda: add_to_command("thrdscan", "--poolscanner", command_list))
    commands_menu.add_cascade(label="Thrdscan", menu=Thrdscan_plugin)

    # Passphrase_plugin
    Passphrase_plugin = Menu(commands_menu, tearoff=0)
    passphrase_modules_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="--modules", variable=passphrase_modules_var,
                                      command=lambda: add_to_command("passphrase", "--modules", command_list))
    passphrase_min_length_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="--min-length", variable=passphrase_min_length_var,
                                      command=lambda: add_to_command("passphrase", "--min-length", command_list))
    commands_menu.add_cascade(label="Passphrase", menu=Passphrase_plugin)

    # Vadinfo_plugin
    Vadinfo_plugin = Menu(commands_menu, tearoff=0)
    vadinfo_kernel_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--kernel", variable=vadinfo_kernel_var,
                                   command=lambda: add_to_command("vadinfo", "--kernel", command_list))
    vadinfo_address_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--address", variable=vadinfo_address_var,
                                   command=lambda: add_to_command("vadinfo", "--address", command_list))
    vadinfo_pid_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--pid", variable=vadinfo_pid_var,
                                   command=lambda: add_to_command("vadinfo", "--pid", command_list))
    vadinfo_pslist_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--pslist", variable=vadinfo_pslist_var,
                                   command=lambda: add_to_command("vadinfo", "--pslist", command_list))
    vadinfo_dump_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--dump", variable=vadinfo_dump_var,
                                   command=lambda: add_to_command("vadinfo", "--dump", command_list))
    vadinfo_maxsize_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="--maxsize", variable=vadinfo_maxsize_var,
                                   command=lambda: add_to_command("vadinfo", "--maxsize", command_list))
    commands_menu.add_cascade(label="Vadinfo", menu=Vadinfo_plugin)

    # Vadwalk_plugin
    Vadwalk_plugin = Menu(commands_menu, tearoff=0)
    vadwalk_kernel_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--kernel", variable=vadwalk_kernel_var,
                                   command=lambda: add_to_command("vadwalk", "--kernel", command_list))
    vadwalk_pslist_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--pslist", variable=vadwalk_pslist_var,
                                   command=lambda: add_to_command("vadwalk", "--pslist", command_list))
    vadwalk_vadinfo_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--vadinfo", variable=vadwalk_vadinfo_var,
                                   command=lambda: add_to_command("vadwalk", "--vadinfo", command_list))
    vadwalk_pid_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="--pid", variable=vadwalk_pid_var,
                                   command=lambda: add_to_command("vadwalk", "--pid", command_list))
    commands_menu.add_cascade(label="Vadwalk", menu=Vadwalk_plugin)

    # Vadyarascan_plugin
    Vadyarascan_plugin = Menu(commands_menu, tearoff=0)
    commands_menu.add_cascade(label="Vadyarascan", menu=Vadyarascan_plugin)

    # Verinfo_plugin
    Verinfo_plugin = Menu(commands_menu, tearoff=0)
    verinfo_kernel_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--kernel", variable=verinfo_kernel_var,
                                   command=lambda: add_to_command("verinfo", "--kernel", command_list))
    verinfo_pslist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--pslist", variable=verinfo_pslist_var,
                                   command=lambda: add_to_command("verinfo", "--pslist", command_list))
    verinfo_modules_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--modules", variable=verinfo_modules_var,
                                   command=lambda: add_to_command("verinfo", "--modules", command_list))
    verinfo_dlllist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--dlllist", variable=verinfo_dlllist_var,
                                   command=lambda: add_to_command("verinfo", "--dlllist", command_list))
    verinfo_extensive_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="--extensive", variable=verinfo_extensive_var,
                                   command=lambda: add_to_command("verinfo", "--extensive", command_list))
    commands_menu.add_cascade(label="Verinfo", menu=Verinfo_plugin)

    # Virtmap_plugin
    Virtmap_plugin = Menu(commands_menu, tearoff=0)
    virtmap_kernel_var = tk.BooleanVar()
    Virtmap_plugin.add_checkbutton(label="--kernel", variable=virtmap_kernel_var,
                                   command=lambda: add_to_command("virtmap", "--kernel", command_list))
    commands_menu.add_cascade(label="Virtmap", menu=Virtmap_plugin)

    # Hivelist_plugin
    Hivelist_plugin = Menu(commands_menu, tearoff=0)
    hivelist_kernel_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--kernel", variable=hivelist_kernel_var,
                                    command=lambda: add_to_command("hivelist", "--kernel", command_list))
    hivelist_filter_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--filter", variable=hivelist_filter_var,
                                    command=lambda: add_to_command("hivelist", "--filter", command_list))
    hivelist_hivescan_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--hivescan", variable=hivelist_hivescan_var,
                                    command=lambda: add_to_command("hivelist", "--hivescan", command_list))
    hivelist_dump_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="--dump", variable=hivelist_dump_var,
                                    command=lambda: add_to_command("hivelist", "--dump", command_list))
    commands_menu.add_cascade(label="Hivelist", menu=Hivelist_plugin)

    # Hivescan_plugin
    Hivescan_plugin = Menu(commands_menu, tearoff=0)
    hivescan_kernel_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--kernel", variable=hivescan_kernel_var,
                                    command=lambda: add_to_command("hivescan", "--kernel", command_list))
    hivescan_poolscanner_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--poolscanner", variable=hivescan_poolscanner_var,
                                    command=lambda: add_to_command("hivescan", "--poolscanner", command_list))
    hivescan_bigpools_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="--bigpools", variable=hivescan_bigpools_var,
                                    command=lambda: add_to_command("hivescan", "--bigpools", command_list))
    commands_menu.add_cascade(label="Hivescan", menu=Hivescan_plugin)

    # Printkey_plugin
    Printkey_plugin = Menu(commands_menu, tearoff=0)
    printkey_kernel_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--kernel", variable=printkey_kernel_var,
                                    command=lambda: add_to_command("printkey", "--kernel", command_list))
    printkey_hivelist_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--hivelist", variable=printkey_hivelist_var,
                                    command=lambda: add_to_command("printkey", "--hivelist", command_list))
    printkey_offset_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--offset", variable=printkey_offset_var,
                                    command=lambda: add_to_command("printkey", "--offset", command_list))
    printkey_key_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--key", variable=printkey_key_var,
                                    command=lambda: add_to_command("printkey", "--key", command_list))
    printkey_recurse_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="--recurse", variable=printkey_recurse_var,
                                    command=lambda: add_to_command("printkey", "--recurse", command_list))
    commands_menu.add_cascade(label="Printkey", menu=Printkey_plugin)

    # Userassist_plugin
    Userassist_plugin = Menu(commands_menu, tearoff=0)
    userassist_kernel_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--kernel", variable=userassist_kernel_var,
                                      command=lambda: add_to_command("userassist", "--kernel", command_list))
    userassist_offset_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--offset", variable=userassist_offset_var,
                                      command=lambda: add_to_command("userassist", "--offset", command_list))
    userassist_hivelist_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="--hivelist", variable=userassist_hivelist_var,
                                      command=lambda: add_to_command("userassist", "--hivelist", command_list))
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
    #print(f"Length of History[0] {len(History)}")
    #print(f"Length of History[1] {len(History)}")

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

    update_button = ttk.Button(frame_mid, text="Update", command=lambda: update_cmd(command_list))
    update_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    cancel_button = ttk.Button(frame_mid, text="Cancel")
    cancel_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    reset_button = ttk.Button(frame_mid, text="Reset", command=lambda: reset_and_update(command_list))
    reset_button.grid(row=0, column=4, padx=5, pady=5, sticky='w')

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
