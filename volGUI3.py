import tkinter as tk
from tkinter import ttk, Menu, filedialog, simpledialog
import platform
import subprocess
import FileHandling
import textBoxNumbers
import command as cmd
import re


# uses system specific save functionality
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


# uses system specific file browser
def browse_files(command_list, path_entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
        add_filepath_to_command(file_path, command_list)


def dump_path():
    file_path = filedialog.askdirectory()
    if file_path:
        return file_path
    else:
        return None


#
def get_selected_command(listbox, output_text, info, mid_text_field):
    print("get_selected_command()")
    for i in listbox.curselection():
        print(listbox.get(i))
        update_selected_from_history(listbox.get(i), mid_text_field)
        output_text.text.delete(1.0, tk.END)
        output_text.text.insert(1.0, info[1][i])


#
def update_selected_from_history(command, mid_text_field):
    print("update_selected_from_history()")
    command.strip()
    mid_text_field.delete(0, tk.END)
    mid_text_field.insert(0, command)


#
def set_os(os_name, os_entry, current_command):
    current_command.set_os(os_name)
    print(current_command.os)
    os_entry.delete(0, tk.END)
    os_entry.insert(0, os_name)


# returns the value of the os_entry field
def get_os(os_entry):
    return os_entry.get()


# runs command with subproccess and returns result in text form
def run_command_capture_output(cmd_list):
    try:
        print(f"Running command: {' '.join(cmd_list)}")
        result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"Command output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        return e.output


# calls on run_command_capture_output and writes return value to mid_text_field
def run_command(command_list, output_text, prevCommandList):
    print("run_command()")
    clear_output(output_text)

    # command_str_list = command_list.to_string().split(" ")
    output = run_command_capture_output(command_list)

    output_text.text.delete(1.0, tk.END)
    output_text.text.insert(tk.END, output)
    output_text.update_line_numbers()
    FileHandling.update_history(prevCommandList)


def clear_output(output_text):
    output_text.text.delete(1.0, tk.END)
    output_text.update_line_numbers()


# adds plugin and flag to command list
def add_to_command(plugin, flag, cmd_list, os_entry):
    os_name = get_os(os_entry)
    if (os_name + '.' + plugin) in cmd_list:
        if flag != "":
            cmd_list.append(flag)
            add_userinput_to_command(flag, cmd_list)
    else:
        cmd_list.append(os_name + '.' + plugin)

        if flag != "":
            cmd_list.append(flag)
            add_userinput_to_command(flag, cmd_list)

    return cmd_list


# adds the filepath to the command list
def add_filepath_to_command(filepath, cmd_list):
    if filepath not in cmd_list:
        flag_index = cmd_list.index('-f')
        cmd_list.insert(flag_index + 1, filepath)
    else:
        print("file already in use")
    return cmd_list


# sanitizes the userinput for a-z, A-Z, 0-9 and -
def sanitize_input(input):
    sanitized = re.sub(r'[^a-zA-Z0-9-]', '', input)
    return sanitized


# checks if a flag takes an input and then prompts the user for it
def check_if_flag_takes_input(flag):
    flags_with_input = ['--pid', '--offset', '--dump']
    if flag in flags_with_input:
        if flag == '--dump':
            print("found --dump")
            path = dump_path()
            return_val = ['-o', path]
            return return_val

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
        cmd_list.append("/home/bolle/Documents/volatility3/vol.py")
    else:
        cmd_list.append("python3")
        cmd_list.append("/home/bolle/Documents/volatility3/vol.py")

    cmd_list.append("-f")
    cmd_list.append(file_path)
    return cmd_list


# updates the command field to the current command
def update_cmd(command_list, mid_text_field):
    command_str = ' '.join(command_list)
    mid_text_field.delete(0, tk.END)
    mid_text_field.insert(0, command_str)


# calls on update_cmd and reset_command_list
def reset_and_update(cmd_list, mid_text_field):
    path_index = cmd_list.index('-f')
    file_path = cmd_list[path_index + 1]
    reset_command_list(cmd_list, file_path)
    update_cmd(cmd_list, mid_text_field)
    return cmd_list


# builds the GUI
def create_gui():
    current_command = cmd.command()
    command_list = []
    command_list = reset_command_list(command_list, "")

    root = tk.Tk()
    root.title("Volatility 3")
    root.configure(bg="#f2f2e9")

    menubar_frame = ttk.Frame(root, height=30)
    menubar_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
    menubar_frame.grid_propagate(False)

    menubar_container = ttk.Frame(menubar_frame)
    menubar_container.grid(row=0, column=0, sticky='ew')
    menubar_container.grid_columnconfigure(0, weight=1)
    menubar_container.grid_columnconfigure(1, weight=0)

    os_entry = ttk.Entry(menubar_container, width=20)
    os_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

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
    os_menu.add_command(label="Windows", command=lambda: set_os("windows", os_entry, current_command))
    os_menu.add_command(label="MacOS", command=lambda: set_os("MacOs", os_entry, current_command))
    os_menu.add_command(label="Linux", command=lambda: set_os("linux", os_entry, current_command))
    os_menu.add_command(label="RedStarOS", command=lambda: set_os("RedStarOS", os_entry, current_command))
    os_menu.add_command(label="TempleOS", command=lambda: set_os("TempleOS", os_entry, current_command))
    menu_bar.add_cascade(label="OS", menu=os_menu)

    root.config(menu=menu_bar)
    root.minsize(1200, 400)

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)

    frame_left = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_center = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_right = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_mid = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame_lower = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)

    frame_left.grid(row=1, column=0, sticky="nsew")
    frame_center.grid(row=1, column=1, sticky="nsew")
    frame_right.grid(row=1, column=2, sticky="nsew")
    frame_mid.grid(row=2, column=0, columnspan=3, sticky="nsew")
    frame_lower.grid(row=3, column=0, columnspan=3, sticky="nsew")

    frame_left.grid_propagate(False)
    frame_center.grid_propagate(False)
    frame_right.grid_propagate(False)
    frame_mid.grid_propagate(False)

    frame_right.grid_rowconfigure(0, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_columnconfigure(1, weight=0)

    frame_left.config(width=200, height=100)
    frame_center.config(width=200, height=100)
    frame_right.config(width=200, height=100)
    frame_mid.config(height=50)

    frame_mid.grid(row=2, column=0, columnspan=3, sticky="nsew")

    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=5)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)

    path_frame = ttk.Frame(frame_left, padding="1 1 1 1", style='TFrame')
    path_frame.grid(row=0, column=1, padx=1, pady=1, sticky='ew')
    path_label = ttk.Label(path_frame, text="File Path:")
    path_label.grid(row=0, column=0, sticky='w')
    path_entry = ttk.Entry(path_frame, width=20)
    path_entry.grid(row=0, column=1, sticky='ew')
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda: browse_files(command_list, path_entry))
    browse_button.grid(row=0, column=2, padx=1, pady=0)
    clear_button = ttk.Button(path_frame, text="Clear", command=lambda: clear_path(path_entry))
    clear_button.grid(row=0, column=3, padx=1, pady=0)

    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(frame_center, tearoff=0)
    # Bigpools_plugin
    Bigpools_plugin = Menu(commands_menu, tearoff=0)
    bigpools_kernel_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="-kernel", variable=bigpools_kernel_var,
                                    command=lambda: add_to_command("bigpools", "-kernel", command_list, os_entry))
    bigpools_tags_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="-tags", variable=bigpools_tags_var,
                                    command=lambda: add_to_command("bigpools", "-tags", command_list, os_entry))
    bigpools_show_free_var = tk.BooleanVar()
    Bigpools_plugin.add_checkbutton(label="-show-free", variable=bigpools_show_free_var,
                                    command=lambda: add_to_command("bigpools", "-show-free", command_list, os_entry))
    commands_menu.add_cascade(label="Bigpools", menu=Bigpools_plugin)

    # Cachedump_plugin
    Cachedump_plugin = Menu(commands_menu, tearoff=0)
    cachedump_kernel_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="-kernel", variable=cachedump_kernel_var,
                                     command=lambda: add_to_command("cachedump", "-kernel", command_list, os_entry))
    cachedump_hivelist_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="-hivelist", variable=cachedump_hivelist_var,
                                     command=lambda: add_to_command("cachedump", "-hivelist", command_list, os_entry))
    cachedump_lsadump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="-lsadump", variable=cachedump_lsadump_var,
                                     command=lambda: add_to_command("cachedump", "-lsadump", command_list, os_entry))
    cachedump_hashdump_var = tk.BooleanVar()
    Cachedump_plugin.add_checkbutton(label="-hashdump", variable=cachedump_hashdump_var,
                                     command=lambda: add_to_command("cachedump", "-hashdump", command_list, os_entry))
    commands_menu.add_cascade(label="Cachedump", menu=Cachedump_plugin)

    # Callbacks_plugin
    Callbacks_plugin = Menu(commands_menu, tearoff=0)
    callbacks_kernel_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="-kernel", variable=callbacks_kernel_var,
                                     command=lambda: add_to_command("callbacks", "-kernel", command_list, os_entry))
    callbacks_ssdt_var = tk.BooleanVar()
    Callbacks_plugin.add_checkbutton(label="-ssdt", variable=callbacks_ssdt_var,
                                     command=lambda: add_to_command("callbacks", "-ssdt", command_list, os_entry))
    commands_menu.add_cascade(label="Callbacks", menu=Callbacks_plugin)

    # Cmdline_plugin
    Cmdline_plugin = Menu(commands_menu, tearoff=0)
    cmdline_kernel_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="-kernel", variable=cmdline_kernel_var,
                                   command=lambda: add_to_command("cmdline", "-kernel", command_list, os_entry))
    cmdline_pslist_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="-pslist", variable=cmdline_pslist_var,
                                   command=lambda: add_to_command("cmdline", "-pslist", command_list, os_entry))
    cmdline_pid_var = tk.BooleanVar()
    Cmdline_plugin.add_checkbutton(label="-pid", variable=cmdline_pid_var,
                                   command=lambda: add_to_command("cmdline", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Cmdline", menu=Cmdline_plugin)

    # Crashinfo_plugin
    Crashinfo_plugin = Menu(commands_menu, tearoff=0)
    crashinfo_primary_var = tk.BooleanVar()
    Crashinfo_plugin.add_checkbutton(label="-primary", variable=crashinfo_primary_var,
                                     command=lambda: add_to_command("crashinfo", "-primary", command_list, os_entry))
    commands_menu.add_cascade(label="Crashinfo", menu=Crashinfo_plugin)

    # Devicetree_plugin
    Devicetree_plugin = Menu(commands_menu, tearoff=0)
    devicetree_kernel_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="-kernel", variable=devicetree_kernel_var,
                                      command=lambda: add_to_command("devicetree", "-kernel", command_list, os_entry))
    devicetree_driverscan_var = tk.BooleanVar()
    Devicetree_plugin.add_checkbutton(label="-driverscan", variable=devicetree_driverscan_var,
                                      command=lambda: add_to_command("devicetree", "-driverscan", command_list,
                                                                     os_entry))
    commands_menu.add_cascade(label="Devicetree", menu=Devicetree_plugin)

    # Dlllist_plugin
    Dlllist_plugin = Menu(commands_menu, tearoff=0)
    dlllist_kernel_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-kernel", variable=dlllist_kernel_var,
                                   command=lambda: add_to_command("dlllist", "-kernel", command_list, os_entry))
    dlllist_pslist_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-pslist", variable=dlllist_pslist_var,
                                   command=lambda: add_to_command("dlllist", "-pslist", command_list, os_entry))
    dlllist_psscan_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-psscan", variable=dlllist_psscan_var,
                                   command=lambda: add_to_command("dlllist", "-psscan", command_list, os_entry))
    dlllist_info_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-info", variable=dlllist_info_var,
                                   command=lambda: add_to_command("dlllist", "-info", command_list, os_entry))
    dlllist_pid_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-pid", variable=dlllist_pid_var,
                                   command=lambda: add_to_command("dlllist", "--pid", command_list, os_entry))
    dlllist_offset_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-offset", variable=dlllist_offset_var,
                                   command=lambda: add_to_command("dlllist", "-offset", command_list, os_entry))
    dlllist_dump_var = tk.BooleanVar()
    Dlllist_plugin.add_checkbutton(label="-dump", variable=dlllist_dump_var,
                                   command=lambda: add_to_command("dlllist", "--dump", command_list, os_entry))
    commands_menu.add_cascade(label="Dlllist", menu=Dlllist_plugin)

    # Driverirp_plugin
    Driverirp_plugin = Menu(commands_menu, tearoff=0)
    driverirp_kernel_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="-kernel", variable=driverirp_kernel_var,
                                     command=lambda: add_to_command("driverirp", "-kernel", command_list, os_entry))
    driverirp_ssdt_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="-ssdt", variable=driverirp_ssdt_var,
                                     command=lambda: add_to_command("driverirp", "-ssdt", command_list, os_entry))
    driverirp_driverscan_var = tk.BooleanVar()
    Driverirp_plugin.add_checkbutton(label="-driverscan", variable=driverirp_driverscan_var,
                                     command=lambda: add_to_command("driverirp", "-driverscan", command_list, os_entry))
    commands_menu.add_cascade(label="Driverirp", menu=Driverirp_plugin)

    # Drivermodule_plugin
    Drivermodule_plugin = Menu(commands_menu, tearoff=0)
    drivermodule_kernel_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="-kernel", variable=drivermodule_kernel_var,
                                        command=lambda: add_to_command("drivermodule", "-kernel", command_list,
                                                                       os_entry))
    drivermodule_ssdt_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="-ssdt", variable=drivermodule_ssdt_var,
                                        command=lambda: add_to_command("drivermodule", "-ssdt", command_list, os_entry))
    drivermodule_driverscan_var = tk.BooleanVar()
    Drivermodule_plugin.add_checkbutton(label="-driverscan", variable=drivermodule_driverscan_var,
                                        command=lambda: add_to_command("drivermodule", "-driverscan", command_list,
                                                                       os_entry))
    commands_menu.add_cascade(label="Drivermodule", menu=Drivermodule_plugin)

    # Driverscan_plugin
    Driverscan_plugin = Menu(commands_menu, tearoff=0)
    driverscan_kernel_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="-kernel", variable=driverscan_kernel_var,
                                      command=lambda: add_to_command("driverscan", "-kernel", command_list, os_entry))
    driverscan_poolscanner_var = tk.BooleanVar()
    Driverscan_plugin.add_checkbutton(label="-poolscanner", variable=driverscan_poolscanner_var,
                                      command=lambda: add_to_command("driverscan", "-poolscanner", command_list,
                                                                     os_entry))
    commands_menu.add_cascade(label="Driverscan", menu=Driverscan_plugin)

    # Dumpfiles_plugin
    Dumpfiles_plugin = Menu(commands_menu, tearoff=0)
    dumpfiles_kernel_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-kernel", variable=dumpfiles_kernel_var,
                                     command=lambda: add_to_command("dumpfiles", "-kernel", command_list, os_entry))
    dumpfiles_pid_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-pid", variable=dumpfiles_pid_var,
                                     command=lambda: add_to_command("dumpfiles", "--pid", command_list, os_entry))
    dumpfiles_virtaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-virtaddr", variable=dumpfiles_virtaddr_var,
                                     command=lambda: add_to_command("dumpfiles", "-virtaddr", command_list, os_entry))
    dumpfiles_physaddr_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-physaddr", variable=dumpfiles_physaddr_var,
                                     command=lambda: add_to_command("dumpfiles", "-physaddr", command_list, os_entry))
    dumpfiles_filter_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-filter", variable=dumpfiles_filter_var,
                                     command=lambda: add_to_command("dumpfiles", "-filter", command_list, os_entry))
    dumpfiles_ignore_case_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-ignore-case", variable=dumpfiles_ignore_case_var,
                                     command=lambda: add_to_command("dumpfiles", "-ignore-case", command_list,
                                                                    os_entry))
    dumpfiles_pslist_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-pslist", variable=dumpfiles_pslist_var,
                                     command=lambda: add_to_command("dumpfiles", "-pslist", command_list, os_entry))
    dumpfiles_handles_var = tk.BooleanVar()
    Dumpfiles_plugin.add_checkbutton(label="-handles", variable=dumpfiles_handles_var,
                                     command=lambda: add_to_command("dumpfiles", "-handles", command_list, os_entry))
    commands_menu.add_cascade(label="Dumpfiles", menu=Dumpfiles_plugin)

    # Envars_plugin
    Envars_plugin = Menu(commands_menu, tearoff=0)
    envars_kernel_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="-kernel", variable=envars_kernel_var,
                                  command=lambda: add_to_command("envars", "-kernel", command_list, os_entry))
    envars_pid_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="-pid", variable=envars_pid_var,
                                  command=lambda: add_to_command("envars", "--pid", command_list, os_entry))
    envars_silent_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="-silent", variable=envars_silent_var,
                                  command=lambda: add_to_command("envars", "-silent", command_list, os_entry))
    envars_pslist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="-pslist", variable=envars_pslist_var,
                                  command=lambda: add_to_command("envars", "-pslist", command_list, os_entry))
    envars_hivelist_var = tk.BooleanVar()
    Envars_plugin.add_checkbutton(label="-hivelist", variable=envars_hivelist_var,
                                  command=lambda: add_to_command("envars", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Envars", menu=Envars_plugin)

    # Filescan_plugin
    Filescan_plugin = Menu(commands_menu, tearoff=0)
    filescan_kernel_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="-kernel", variable=filescan_kernel_var,
                                    command=lambda: add_to_command("filescan", "-kernel", command_list, os_entry))
    filescan_poolscanner_var = tk.BooleanVar()
    Filescan_plugin.add_checkbutton(label="-poolscanner", variable=filescan_poolscanner_var,
                                    command=lambda: add_to_command("filescan", "-poolscanner", command_list, os_entry))
    commands_menu.add_cascade(label="Filescan", menu=Filescan_plugin)

    # Getservicesids_plugin
    Getservicesids_plugin = Menu(commands_menu, tearoff=0)
    getservicesids_kernel_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="-kernel", variable=getservicesids_kernel_var,
                                          command=lambda: add_to_command("getservicesids", "-kernel", command_list,
                                                                         os_entry))
    getservicesids_hivelist_var = tk.BooleanVar()
    Getservicesids_plugin.add_checkbutton(label="-hivelist", variable=getservicesids_hivelist_var,
                                          command=lambda: add_to_command("getservicesids", "-hivelist", command_list,
                                                                         os_entry))
    commands_menu.add_cascade(label="Getservicesids", menu=Getservicesids_plugin)

    # Getsids_plugin
    Getsids_plugin = Menu(commands_menu, tearoff=0)
    getsids_kernel_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="-kernel", variable=getsids_kernel_var,
                                   command=lambda: add_to_command("getsids", "-kernel", command_list, os_entry))
    getsids_pid_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="-pid", variable=getsids_pid_var,
                                   command=lambda: add_to_command("getsids", "--pid", command_list, os_entry))
    getsids_pslist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="-pslist", variable=getsids_pslist_var,
                                   command=lambda: add_to_command("getsids", "-pslist", command_list, os_entry))
    getsids_hivelist_var = tk.BooleanVar()
    Getsids_plugin.add_checkbutton(label="-hivelist", variable=getsids_hivelist_var,
                                   command=lambda: add_to_command("getsids", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Getsids", menu=Getsids_plugin)

    # Handles_plugin
    Handles_plugin = Menu(commands_menu, tearoff=0)
    handles_kernel_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="-kernel", variable=handles_kernel_var,
                                   command=lambda: add_to_command("handles", "-kernel", command_list, os_entry))
    handles_pslist_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="-pslist", variable=handles_pslist_var,
                                   command=lambda: add_to_command("handles", "-pslist", command_list, os_entry))
    handles_psscan_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="-psscan", variable=handles_psscan_var,
                                   command=lambda: add_to_command("handles", "-psscan", command_list, os_entry))
    handles_pid_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="-pid", variable=handles_pid_var,
                                   command=lambda: add_to_command("handles", "--pid", command_list, os_entry))
    handles_offset_var = tk.BooleanVar()
    Handles_plugin.add_checkbutton(label="-offset", variable=handles_offset_var,
                                   command=lambda: add_to_command("handles", "-offset", command_list, os_entry))
    commands_menu.add_cascade(label="Handles", menu=Handles_plugin)

    # Hashdump_plugin
    Hashdump_plugin = Menu(commands_menu, tearoff=0)
    hashdump_kernel_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="-kernel", variable=hashdump_kernel_var,
                                    command=lambda: add_to_command("hashdump", "-kernel", command_list, os_entry))
    hashdump_hivelist_var = tk.BooleanVar()
    Hashdump_plugin.add_checkbutton(label="-hivelist", variable=hashdump_hivelist_var,
                                    command=lambda: add_to_command("hashdump", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Hashdump", menu=Hashdump_plugin)

    # Iat_plugin
    Iat_plugin = Menu(commands_menu, tearoff=0)
    iat_kernel_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="-kernel", variable=iat_kernel_var,
                               command=lambda: add_to_command("iat", "-kernel", command_list, os_entry))
    iat_pslist_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="-pslist", variable=iat_pslist_var,
                               command=lambda: add_to_command("iat", "-pslist", command_list, os_entry))
    iat_pid_var = tk.BooleanVar()
    Iat_plugin.add_checkbutton(label="-pid", variable=iat_pid_var,
                               command=lambda: add_to_command("iat", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Iat", menu=Iat_plugin)

    # Info_plugin
    Info_plugin = Menu(commands_menu, tearoff=0)
    info_kernel_var = tk.BooleanVar()
    Info_plugin.add_checkbutton(label="-kernel", variable=info_kernel_var,
                                command=lambda: add_to_command("info", "-kernel", command_list, os_entry))
    commands_menu.add_cascade(label="Info", menu=Info_plugin)

    # Joblinks_plugin
    Joblinks_plugin = Menu(commands_menu, tearoff=0)
    joblinks_kernel_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="-kernel", variable=joblinks_kernel_var,
                                    command=lambda: add_to_command("joblinks", "-kernel", command_list, os_entry))
    joblinks_physical_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="-physical", variable=joblinks_physical_var,
                                    command=lambda: add_to_command("joblinks", "-physical", command_list, os_entry))
    joblinks_pslist_var = tk.BooleanVar()
    Joblinks_plugin.add_checkbutton(label="-pslist", variable=joblinks_pslist_var,
                                    command=lambda: add_to_command("joblinks", "-pslist", command_list, os_entry))
    commands_menu.add_cascade(label="Joblinks", menu=Joblinks_plugin)

    # Ldrmodules_plugin
    Ldrmodules_plugin = Menu(commands_menu, tearoff=0)
    ldrmodules_kernel_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="-kernel", variable=ldrmodules_kernel_var,
                                      command=lambda: add_to_command("ldrmodules", "-kernel", command_list, os_entry))
    ldrmodules_pslist_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="-pslist", variable=ldrmodules_pslist_var,
                                      command=lambda: add_to_command("ldrmodules", "-pslist", command_list, os_entry))
    ldrmodules_vadinfo_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="-vadinfo", variable=ldrmodules_vadinfo_var,
                                      command=lambda: add_to_command("ldrmodules", "-vadinfo", command_list, os_entry))
    ldrmodules_pid_var = tk.BooleanVar()
    Ldrmodules_plugin.add_checkbutton(label="-pid", variable=ldrmodules_pid_var,
                                      command=lambda: add_to_command("ldrmodules", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Ldrmodules", menu=Ldrmodules_plugin)

    # Lsadump_plugin
    Lsadump_plugin = Menu(commands_menu, tearoff=0)
    lsadump_kernel_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="-kernel", variable=lsadump_kernel_var,
                                   command=lambda: add_to_command("lsadump", "-kernel", command_list, os_entry))
    lsadump_hashdump_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="-hashdump", variable=lsadump_hashdump_var,
                                   command=lambda: add_to_command("lsadump", "-hashdump", command_list, os_entry))
    lsadump_hivelist_var = tk.BooleanVar()
    Lsadump_plugin.add_checkbutton(label="-hivelist", variable=lsadump_hivelist_var,
                                   command=lambda: add_to_command("lsadump", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Lsadump", menu=Lsadump_plugin)

    # Malfind_plugin
    Malfind_plugin = Menu(commands_menu, tearoff=0)
    malfind_kernel_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="-kernel", variable=malfind_kernel_var,
                                   command=lambda: add_to_command("malfind", "-kernel", command_list, os_entry))
    malfind_pid_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="-pid", variable=malfind_pid_var,
                                   command=lambda: add_to_command("malfind", "--pid", command_list, os_entry))
    malfind_dump_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="-dump", variable=malfind_dump_var,
                                   command=lambda: add_to_command("malfind", "--dump", command_list, os_entry))
    malfind_pslist_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="-pslist", variable=malfind_pslist_var,
                                   command=lambda: add_to_command("malfind", "-pslist", command_list, os_entry))
    malfind_vadinfo_var = tk.BooleanVar()
    Malfind_plugin.add_checkbutton(label="-vadinfo", variable=malfind_vadinfo_var,
                                   command=lambda: add_to_command("malfind", "-vadinfo", command_list, os_entry))
    commands_menu.add_cascade(label="Malfind", menu=Malfind_plugin)

    # Mbrscan_plugin
    Mbrscan_plugin = Menu(commands_menu, tearoff=0)
    mbrscan_kernel_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="-kernel", variable=mbrscan_kernel_var,
                                   command=lambda: add_to_command("mbrscan", "-kernel", command_list, os_entry))
    mbrscan_full_var = tk.BooleanVar()
    Mbrscan_plugin.add_checkbutton(label="-full", variable=mbrscan_full_var,
                                   command=lambda: add_to_command("mbrscan", "-full", command_list, os_entry))
    commands_menu.add_cascade(label="Mbrscan", menu=Mbrscan_plugin)

    # Memmap_plugin
    Memmap_plugin = Menu(commands_menu, tearoff=0)
    memmap_kernel_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="-kernel", variable=memmap_kernel_var,
                                  command=lambda: add_to_command("memmap", "-kernel", command_list, os_entry))
    memmap_pslist_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="-pslist", variable=memmap_pslist_var,
                                  command=lambda: add_to_command("memmap", "-pslist", command_list, os_entry))
    memmap_pid_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="-pid", variable=memmap_pid_var,
                                  command=lambda: add_to_command("memmap", "--pid", command_list, os_entry))
    memmap_dump_var = tk.BooleanVar()
    Memmap_plugin.add_checkbutton(label="-dump", variable=memmap_dump_var,
                                  command=lambda: add_to_command("memmap", "--dump", command_list, os_entry))
    commands_menu.add_cascade(label="Memmap", menu=Memmap_plugin)

    # Mftscan_plugin
    Mftscan_plugin = Menu(commands_menu, tearoff=0)
    mftscan_primary_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="-primary", variable=mftscan_primary_var,
                                   command=lambda: add_to_command("mftscan", "-primary", command_list, os_entry))
    mftscan_yarascanner_var = tk.BooleanVar()
    Mftscan_plugin.add_checkbutton(label="-yarascanner", variable=mftscan_yarascanner_var,
                                   command=lambda: add_to_command("mftscan", "-yarascanner", command_list, os_entry))
    commands_menu.add_cascade(label="Mftscan", menu=Mftscan_plugin)

    # Ads_plugin
    Ads_plugin = Menu(commands_menu, tearoff=0)
    ads_primary_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="-primary", variable=ads_primary_var,
                               command=lambda: add_to_command("ads", "-primary", command_list, os_entry))
    ads_yarascanner_var = tk.BooleanVar()
    Ads_plugin.add_checkbutton(label="-yarascanner", variable=ads_yarascanner_var,
                               command=lambda: add_to_command("ads", "-yarascanner", command_list, os_entry))
    commands_menu.add_cascade(label="Ads", menu=Ads_plugin)

    # Modscan_plugin
    Modscan_plugin = Menu(commands_menu, tearoff=0)
    modscan_kernel_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="-kernel", variable=modscan_kernel_var,
                                   command=lambda: add_to_command("modscan", "-kernel", command_list, os_entry))
    modscan_poolscanner_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="-poolscanner", variable=modscan_poolscanner_var,
                                   command=lambda: add_to_command("modscan", "-poolscanner", command_list, os_entry))
    modscan_pslist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="-pslist", variable=modscan_pslist_var,
                                   command=lambda: add_to_command("modscan", "-pslist", command_list, os_entry))
    modscan_dlllist_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="-dlllist", variable=modscan_dlllist_var,
                                   command=lambda: add_to_command("modscan", "-dlllist", command_list, os_entry))
    modscan_dump_var = tk.BooleanVar()
    Modscan_plugin.add_checkbutton(label="-dump", variable=modscan_dump_var,
                                   command=lambda: add_to_command("modscan", "--dump", command_list, os_entry))
    commands_menu.add_cascade(label="Modscan", menu=Modscan_plugin)

    # Modules_plugin
    Modules_plugin = Menu(commands_menu, tearoff=0)
    modules_kernel_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="-kernel", variable=modules_kernel_var,
                                   command=lambda: add_to_command("modules", "-kernel", command_list, os_entry))
    modules_pslist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="-pslist", variable=modules_pslist_var,
                                   command=lambda: add_to_command("modules", "-pslist", command_list, os_entry))
    modules_dlllist_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="-dlllist", variable=modules_dlllist_var,
                                   command=lambda: add_to_command("modules", "-dlllist", command_list, os_entry))
    modules_dump_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="-dump", variable=modules_dump_var,
                                   command=lambda: add_to_command("modules", "--dump", command_list, os_entry))
    modules_name_var = tk.BooleanVar()
    Modules_plugin.add_checkbutton(label="-name", variable=modules_name_var,
                                   command=lambda: add_to_command("modules", "-name", command_list, os_entry))
    commands_menu.add_cascade(label="Modules", menu=Modules_plugin)

    # Mutantscan_plugin
    Mutantscan_plugin = Menu(commands_menu, tearoff=0)
    mutantscan_kernel_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="-kernel", variable=mutantscan_kernel_var,
                                      command=lambda: add_to_command("mutantscan", "-kernel", command_list, os_entry))
    mutantscan_poolscanner_var = tk.BooleanVar()
    Mutantscan_plugin.add_checkbutton(label="-poolscanner", variable=mutantscan_poolscanner_var,
                                      command=lambda: add_to_command("mutantscan", "-poolscanner", command_list,
                                                                     os_entry))
    commands_menu.add_cascade(label="Mutantscan", menu=Mutantscan_plugin)

    # Netscan_plugin
    Netscan_plugin = Menu(commands_menu, tearoff=0)
    netscan_kernel_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="-kernel", variable=netscan_kernel_var,
                                   command=lambda: add_to_command("netscan", "-kernel", command_list, os_entry))
    netscan_poolscanner_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="-poolscanner", variable=netscan_poolscanner_var,
                                   command=lambda: add_to_command("netscan", "-poolscanner", command_list, os_entry))
    netscan_info_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="-info", variable=netscan_info_var,
                                   command=lambda: add_to_command("netscan", "-info", command_list, os_entry))
    netscan_verinfo_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="-verinfo", variable=netscan_verinfo_var,
                                   command=lambda: add_to_command("netscan", "-verinfo", command_list, os_entry))
    netscan_include_corrupt_var = tk.BooleanVar()
    Netscan_plugin.add_checkbutton(label="-include-corrupt", variable=netscan_include_corrupt_var,
                                   command=lambda: add_to_command("netscan", "-include-corrupt", command_list,
                                                                  os_entry))
    commands_menu.add_cascade(label="Netscan", menu=Netscan_plugin)

    # Netstat_plugin
    Netstat_plugin = Menu(commands_menu, tearoff=0)
    netstat_kernel_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-kernel", variable=netstat_kernel_var,
                                   command=lambda: add_to_command("netstat", "-kernel", command_list, os_entry))
    netstat_netscan_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-netscan", variable=netstat_netscan_var,
                                   command=lambda: add_to_command("netstat", "-netscan", command_list, os_entry))
    netstat_modules_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-modules", variable=netstat_modules_var,
                                   command=lambda: add_to_command("netstat", "-modules", command_list, os_entry))
    netstat_pdbutil_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-pdbutil", variable=netstat_pdbutil_var,
                                   command=lambda: add_to_command("netstat", "-pdbutil", command_list, os_entry))
    netstat_info_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-info", variable=netstat_info_var,
                                   command=lambda: add_to_command("netstat", "-info", command_list, os_entry))
    netstat_verinfo_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-verinfo", variable=netstat_verinfo_var,
                                   command=lambda: add_to_command("netstat", "-verinfo", command_list, os_entry))
    netstat_include_corrupt_var = tk.BooleanVar()
    Netstat_plugin.add_checkbutton(label="-include-corrupt", variable=netstat_include_corrupt_var,
                                   command=lambda: add_to_command("netstat", "-include-corrupt", command_list,
                                                                  os_entry))
    commands_menu.add_cascade(label="Netstat", menu=Netstat_plugin)

    # Poolscanner_plugin
    Poolscanner_plugin = Menu(commands_menu, tearoff=0)
    poolscanner_kernel_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="-kernel", variable=poolscanner_kernel_var,
                                       command=lambda: add_to_command("poolscanner", "-kernel", command_list, os_entry))
    poolscanner_handles_var = tk.BooleanVar()
    Poolscanner_plugin.add_checkbutton(label="-handles", variable=poolscanner_handles_var,
                                       command=lambda: add_to_command("poolscanner", "-handles", command_list,
                                                                      os_entry))
    commands_menu.add_cascade(label="Poolscanner", menu=Poolscanner_plugin)

    # Privs_plugin
    Privs_plugin = Menu(commands_menu, tearoff=0)
    privs_kernel_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="-kernel", variable=privs_kernel_var,
                                 command=lambda: add_to_command("privs", "-kernel", command_list, os_entry))
    privs_pid_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="-pid", variable=privs_pid_var,
                                 command=lambda: add_to_command("privs", "--pid", command_list, os_entry))
    privs_pslist_var = tk.BooleanVar()
    Privs_plugin.add_checkbutton(label="-pslist", variable=privs_pslist_var,
                                 command=lambda: add_to_command("privs", "-pslist", command_list, os_entry))
    commands_menu.add_cascade(label="Privs", menu=Privs_plugin)

    # Pslist_plugin
    Pslist_plugin = Menu(commands_menu, tearoff=0)
    pslist_kernel_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="no flag", variable=pslist_kernel_var,
                                  command=lambda: add_to_command("pslist", "", command_list, os_entry))
    pslist_kernel_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="-kernel", variable=pslist_kernel_var,
                                  command=lambda: add_to_command("pslist", "-kernel", command_list, os_entry))
    pslist_physical_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="-physical", variable=pslist_physical_var,
                                  command=lambda: add_to_command("pslist", "-physical", command_list, os_entry))
    pslist_pid_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="-pid", variable=pslist_pid_var,
                                  command=lambda: add_to_command("pslist", "--pid", command_list, os_entry))
    pslist_dump_var = tk.BooleanVar()
    Pslist_plugin.add_checkbutton(label="-dump", variable=pslist_dump_var,
                                  command=lambda: add_to_command("pslist", "--dump", command_list, os_entry))
    commands_menu.add_cascade(label="Pslist", menu=Pslist_plugin)

    # Psscan_plugin
    Psscan_plugin = Menu(commands_menu, tearoff=0)
    psscan_kernel_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="no flag", variable=psscan_kernel_var,
                                  command=lambda: add_to_command("psscan", "", command_list, os_entry))
    psscan_kernel_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-kernel", variable=psscan_kernel_var,
                                  command=lambda: add_to_command("psscan", "-kernel", command_list, os_entry))
    psscan_pslist_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-pslist", variable=psscan_pslist_var,
                                  command=lambda: add_to_command("psscan", "-pslist", command_list, os_entry))
    psscan_info_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-info", variable=psscan_info_var,
                                  command=lambda: add_to_command("psscan", "-info", command_list, os_entry))
    psscan_pid_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-pid", variable=psscan_pid_var,
                                  command=lambda: add_to_command("psscan", "--pid", command_list, os_entry))
    psscan_dump_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-dump", variable=psscan_dump_var,
                                  command=lambda: add_to_command("psscan", "--dump", command_list, os_entry))
    psscan_physical_var = tk.BooleanVar()
    Psscan_plugin.add_checkbutton(label="-physical", variable=psscan_physical_var,
                                  command=lambda: add_to_command("psscan", "-physical", command_list, os_entry))
    commands_menu.add_cascade(label="Psscan", menu=Psscan_plugin)

    # Pstree_plugin
    Pstree_plugin = Menu(commands_menu, tearoff=0)
    pstree_kernel_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="-kernel", variable=pstree_kernel_var,
                                  command=lambda: add_to_command("pstree", "-kernel", command_list, os_entry))
    pstree_physical_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="-physical", variable=pstree_physical_var,
                                  command=lambda: add_to_command("pstree", "-physical", command_list, os_entry))
    pstree_pslist_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="-pslist", variable=pstree_pslist_var,
                                  command=lambda: add_to_command("pstree", "-pslist", command_list, os_entry))
    pstree_pid_var = tk.BooleanVar()
    Pstree_plugin.add_checkbutton(label="-pid", variable=pstree_pid_var,
                                  command=lambda: add_to_command("pstree", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Pstree", menu=Pstree_plugin)

    # Sessions_plugin
    Sessions_plugin = Menu(commands_menu, tearoff=0)
    sessions_kernel_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="-kernel", variable=sessions_kernel_var,
                                    command=lambda: add_to_command("sessions", "-kernel", command_list, os_entry))
    sessions_pslist_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="-pslist", variable=sessions_pslist_var,
                                    command=lambda: add_to_command("sessions", "-pslist", command_list, os_entry))
    sessions_pid_var = tk.BooleanVar()
    Sessions_plugin.add_checkbutton(label="-pid", variable=sessions_pid_var,
                                    command=lambda: add_to_command("sessions", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Sessions", menu=Sessions_plugin)

    # Skeleton_key_check_plugin
    Skeleton_key_check_plugin = Menu(commands_menu, tearoff=0)
    skeleton_key_check_kernel_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="-kernel", variable=skeleton_key_check_kernel_var,
                                              command=lambda: add_to_command("skeleton_key_check", "-kernel",
                                                                             command_list, os_entry))
    skeleton_key_check_pslist_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="-pslist", variable=skeleton_key_check_pslist_var,
                                              command=lambda: add_to_command("skeleton_key_check", "-pslist",
                                                                             command_list, os_entry))
    skeleton_key_check_vadinfo_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="-vadinfo", variable=skeleton_key_check_vadinfo_var,
                                              command=lambda: add_to_command("skeleton_key_check", "-vadinfo",
                                                                             command_list, os_entry))
    skeleton_key_check_pdbutil_var = tk.BooleanVar()
    Skeleton_key_check_plugin.add_checkbutton(label="-pdbutil", variable=skeleton_key_check_pdbutil_var,
                                              command=lambda: add_to_command("skeleton_key_check", "-pdbutil",
                                                                             command_list, os_entry))
    commands_menu.add_cascade(label="Skeleton_key_check", menu=Skeleton_key_check_plugin)

    # Ssdt_plugin
    Ssdt_plugin = Menu(commands_menu, tearoff=0)
    ssdt_kernel_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="-kernel", variable=ssdt_kernel_var,
                                command=lambda: add_to_command("ssdt", "-kernel", command_list, os_entry))
    ssdt_modules_var = tk.BooleanVar()
    Ssdt_plugin.add_checkbutton(label="-modules", variable=ssdt_modules_var,
                                command=lambda: add_to_command("ssdt", "-modules", command_list, os_entry))
    commands_menu.add_cascade(label="Ssdt", menu=Ssdt_plugin)

    # Strings_plugin
    Strings_plugin = Menu(commands_menu, tearoff=0)
    strings_kernel_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="-kernel", variable=strings_kernel_var,
                                   command=lambda: add_to_command("strings", "-kernel", command_list, os_entry))
    strings_pslist_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="-pslist", variable=strings_pslist_var,
                                   command=lambda: add_to_command("strings", "-pslist", command_list, os_entry))
    strings_pid_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="-pid", variable=strings_pid_var,
                                   command=lambda: add_to_command("strings", "--pid", command_list, os_entry))
    strings_strings_file_var = tk.BooleanVar()
    Strings_plugin.add_checkbutton(label="-strings_file", variable=strings_strings_file_var,
                                   command=lambda: add_to_command("strings", "-strings_file", command_list, os_entry))
    commands_menu.add_cascade(label="Strings", menu=Strings_plugin)

    # Svcscan_plugin
    Svcscan_plugin = Menu(commands_menu, tearoff=0)
    svcscan_kernel_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="-kernel", variable=svcscan_kernel_var,
                                   command=lambda: add_to_command("svcscan", "-kernel", command_list, os_entry))
    svcscan_pslist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="-pslist", variable=svcscan_pslist_var,
                                   command=lambda: add_to_command("svcscan", "-pslist", command_list, os_entry))
    svcscan_poolscanner_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="-poolscanner", variable=svcscan_poolscanner_var,
                                   command=lambda: add_to_command("svcscan", "-poolscanner", command_list, os_entry))
    svcscan_vadyarascan_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="-vadyarascan", variable=svcscan_vadyarascan_var,
                                   command=lambda: add_to_command("svcscan", "-vadyarascan", command_list, os_entry))
    svcscan_hivelist_var = tk.BooleanVar()
    Svcscan_plugin.add_checkbutton(label="-hivelist", variable=svcscan_hivelist_var,
                                   command=lambda: add_to_command("svcscan", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Svcscan", menu=Svcscan_plugin)

    # Symlinkscan_plugin
    Symlinkscan_plugin = Menu(commands_menu, tearoff=0)
    symlinkscan_kernel_var = tk.BooleanVar()
    Symlinkscan_plugin.add_checkbutton(label="-kernel", variable=symlinkscan_kernel_var,
                                       command=lambda: add_to_command("symlinkscan", "-kernel", command_list, os_entry))
    commands_menu.add_cascade(label="Symlinkscan", menu=Symlinkscan_plugin)

    # Thrdscan_plugin
    Thrdscan_plugin = Menu(commands_menu, tearoff=0)
    thrdscan_kernel_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="-kernel", variable=thrdscan_kernel_var,
                                    command=lambda: add_to_command("thrdscan", "-kernel", command_list, os_entry))
    thrdscan_poolscanner_var = tk.BooleanVar()
    Thrdscan_plugin.add_checkbutton(label="-poolscanner", variable=thrdscan_poolscanner_var,
                                    command=lambda: add_to_command("thrdscan", "-poolscanner", command_list, os_entry))
    commands_menu.add_cascade(label="Thrdscan", menu=Thrdscan_plugin)

    # Passphrase_plugin
    Passphrase_plugin = Menu(commands_menu, tearoff=0)
    passphrase_modules_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="-modules", variable=passphrase_modules_var,
                                      command=lambda: add_to_command("passphrase", "-modules", command_list, os_entry))
    passphrase_min_length_var = tk.BooleanVar()
    Passphrase_plugin.add_checkbutton(label="-min-length", variable=passphrase_min_length_var,
                                      command=lambda: add_to_command("passphrase", "-min-length", command_list,
                                                                     os_entry))
    commands_menu.add_cascade(label="Passphrase", menu=Passphrase_plugin)

    # Vadinfo_plugin
    Vadinfo_plugin = Menu(commands_menu, tearoff=0)
    vadinfo_kernel_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-kernel", variable=vadinfo_kernel_var,
                                   command=lambda: add_to_command("vadinfo", "-kernel", command_list, os_entry))
    vadinfo_address_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-address", variable=vadinfo_address_var,
                                   command=lambda: add_to_command("vadinfo", "-address", command_list, os_entry))
    vadinfo_pid_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-pid", variable=vadinfo_pid_var,
                                   command=lambda: add_to_command("vadinfo", "--pid", command_list, os_entry))
    vadinfo_pslist_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-pslist", variable=vadinfo_pslist_var,
                                   command=lambda: add_to_command("vadinfo", "-pslist", command_list, os_entry))
    vadinfo_dump_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-dump", variable=vadinfo_dump_var,
                                   command=lambda: add_to_command("vadinfo", "--dump", command_list, os_entry))
    vadinfo_maxsize_var = tk.BooleanVar()
    Vadinfo_plugin.add_checkbutton(label="-maxsize", variable=vadinfo_maxsize_var,
                                   command=lambda: add_to_command("vadinfo", "-maxsize", command_list, os_entry))
    commands_menu.add_cascade(label="Vadinfo", menu=Vadinfo_plugin)

    # Vadwalk_plugin
    Vadwalk_plugin = Menu(commands_menu, tearoff=0)
    vadwalk_kernel_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="-kernel", variable=vadwalk_kernel_var,
                                   command=lambda: add_to_command("vadwalk", "-kernel", command_list, os_entry))
    vadwalk_pslist_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="-pslist", variable=vadwalk_pslist_var,
                                   command=lambda: add_to_command("vadwalk", "-pslist", command_list, os_entry))
    vadwalk_vadinfo_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="-vadinfo", variable=vadwalk_vadinfo_var,
                                   command=lambda: add_to_command("vadwalk", "-vadinfo", command_list, os_entry))
    vadwalk_pid_var = tk.BooleanVar()
    Vadwalk_plugin.add_checkbutton(label="-pid", variable=vadwalk_pid_var,
                                   command=lambda: add_to_command("vadwalk", "--pid", command_list, os_entry))
    commands_menu.add_cascade(label="Vadwalk", menu=Vadwalk_plugin)

    # Vadyarascan_plugin
    Vadyarascan_plugin = Menu(commands_menu, tearoff=0)
    commands_menu.add_cascade(label="Vadyarascan", menu=Vadyarascan_plugin)

    # Verinfo_plugin
    Verinfo_plugin = Menu(commands_menu, tearoff=0)
    verinfo_kernel_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="-kernel", variable=verinfo_kernel_var,
                                   command=lambda: add_to_command("verinfo", "-kernel", command_list, os_entry))
    verinfo_pslist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="-pslist", variable=verinfo_pslist_var,
                                   command=lambda: add_to_command("verinfo", "-pslist", command_list, os_entry))
    verinfo_modules_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="-modules", variable=verinfo_modules_var,
                                   command=lambda: add_to_command("verinfo", "-modules", command_list, os_entry))
    verinfo_dlllist_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="-dlllist", variable=verinfo_dlllist_var,
                                   command=lambda: add_to_command("verinfo", "-dlllist", command_list, os_entry))
    verinfo_extensive_var = tk.BooleanVar()
    Verinfo_plugin.add_checkbutton(label="-extensive", variable=verinfo_extensive_var,
                                   command=lambda: add_to_command("verinfo", "-extensive", command_list, os_entry))
    commands_menu.add_cascade(label="Verinfo", menu=Verinfo_plugin)

    # Virtmap_plugin
    Virtmap_plugin = Menu(commands_menu, tearoff=0)
    virtmap_kernel_var = tk.BooleanVar()
    Virtmap_plugin.add_checkbutton(label="-kernel", variable=virtmap_kernel_var,
                                   command=lambda: add_to_command("virtmap", "-kernel", command_list, os_entry))
    commands_menu.add_cascade(label="Virtmap", menu=Virtmap_plugin)

    # Hivelist_plugin
    Hivelist_plugin = Menu(commands_menu, tearoff=0)
    hivelist_kernel_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="-kernel", variable=hivelist_kernel_var,
                                    command=lambda: add_to_command("hivelist", "-kernel", command_list, os_entry))
    hivelist_filter_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="-filter", variable=hivelist_filter_var,
                                    command=lambda: add_to_command("hivelist", "-filter", command_list, os_entry))
    hivelist_hivescan_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="-hivescan", variable=hivelist_hivescan_var,
                                    command=lambda: add_to_command("hivelist", "-hivescan", command_list, os_entry))
    hivelist_dump_var = tk.BooleanVar()
    Hivelist_plugin.add_checkbutton(label="-dump", variable=hivelist_dump_var,
                                    command=lambda: add_to_command("hivelist", "--dump", command_list, os_entry))
    commands_menu.add_cascade(label="Hivelist", menu=Hivelist_plugin)

    # Hivescan_plugin
    Hivescan_plugin = Menu(commands_menu, tearoff=0)
    hivescan_kernel_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="-kernel", variable=hivescan_kernel_var,
                                    command=lambda: add_to_command("hivescan", "-kernel", command_list, os_entry))
    hivescan_poolscanner_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="-poolscanner", variable=hivescan_poolscanner_var,
                                    command=lambda: add_to_command("hivescan", "-poolscanner", command_list, os_entry))
    hivescan_bigpools_var = tk.BooleanVar()
    Hivescan_plugin.add_checkbutton(label="-bigpools", variable=hivescan_bigpools_var,
                                    command=lambda: add_to_command("hivescan", "-bigpools", command_list, os_entry))
    commands_menu.add_cascade(label="Hivescan", menu=Hivescan_plugin)

    # Printkey_plugin
    Printkey_plugin = Menu(commands_menu, tearoff=0)
    printkey_kernel_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="-kernel", variable=printkey_kernel_var,
                                    command=lambda: add_to_command("printkey", "-kernel", command_list, os_entry))
    printkey_hivelist_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="-hivelist", variable=printkey_hivelist_var,
                                    command=lambda: add_to_command("printkey", "-hivelist", command_list, os_entry))
    printkey_offset_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="-offset", variable=printkey_offset_var,
                                    command=lambda: add_to_command("printkey", "-offset", command_list, os_entry))
    printkey_key_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="-key", variable=printkey_key_var,
                                    command=lambda: add_to_command("printkey", "-key", command_list, os_entry))
    printkey_recurse_var = tk.BooleanVar()
    Printkey_plugin.add_checkbutton(label="-recurse", variable=printkey_recurse_var,
                                    command=lambda: add_to_command("printkey", "-recurse", command_list, os_entry))
    commands_menu.add_cascade(label="Printkey", menu=Printkey_plugin)

    # Userassist_plugin
    Userassist_plugin = Menu(commands_menu, tearoff=0)
    userassist_kernel_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="-kernel", variable=userassist_kernel_var,
                                      command=lambda: add_to_command("userassist", "-kernel", command_list, os_entry))
    userassist_offset_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="-offset", variable=userassist_offset_var,
                                      command=lambda: add_to_command("userassist", "-offset", command_list, os_entry))
    userassist_hivelist_var = tk.BooleanVar()
    Userassist_plugin.add_checkbutton(label="-hivelist", variable=userassist_hivelist_var,
                                      command=lambda: add_to_command("userassist", "-hivelist", command_list, os_entry))
    commands_menu.add_cascade(label="Userassist", menu=Userassist_plugin)

    commands_button = ttk.Menubutton(frame_center, text="Commands", menu=commands_menu)
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

    mid_text_field = ttk.Entry(frame_mid, width=100)
    mid_text_field.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    mid_text_field.insert(0, "filename.txt / dlllist / -offset")
    prevCommandList.bind("<<ListboxSelect>>",
                         get_selected_command(prevCommandList, text_with_line_numbers, History, mid_text_field))

    run_button = ttk.Button(frame_mid, text="Run",
                            command=lambda: run_command(command_list, text_with_line_numbers, prevCommandList))
    run_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    update_button = ttk.Button(frame_mid, text="Update", command=lambda: update_cmd(command_list, mid_text_field))
    update_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    cancel_button = ttk.Button(frame_mid, text="Cancel")
    cancel_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    reset_button = ttk.Button(frame_mid, text="Reset", command=lambda: reset_and_update(command_list, mid_text_field))
    reset_button.grid(row=0, column=4, padx=5, pady=5, sticky='w')

    frame_mid.grid_columnconfigure(0, weight=1)
    frame_mid.grid_columnconfigure(1, weight=0)
    frame_mid.grid_columnconfigure(2, weight=0)
    frame_mid.grid_columnconfigure(3, weight=0)
    frame_mid.grid_columnconfigure(4, weight=2)
    frame_mid.grid_columnconfigure(5, weight=0)

    reset_and_update(command_list, mid_text_field)
    root.mainloop()


if __name__ == "__main__":
    create_gui()
