import tkinter as tk
from tkinter import ttk, Menu, filedialog
import platform
import subprocess
import FileHandling
import textBoxNumbers
import command as cmd
import intro


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


def create_gui():
    intro.show_welcome_window()
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
    browse_button = ttk.Button(path_frame, text="Browse", command=lambda: browse_files(current_command))
    browse_button.grid(row=0, column=2, padx=1, pady=0)
    clear_button = ttk.Button(path_frame, text="Clear", command=clear_path)
    clear_button.grid(row=0, column=3, padx=1, pady=0)

    # plugins & flags
    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(frame_center, tearoff=0)
    # BigPools_plugin
    BigPools_plugin = Menu(commands_menu, tearoff=0)
    BigPools_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "BigPools", "kernel"))
    BigPools_plugin.add_command(label="tags", command=lambda: set_pluginAndFlag(current_command, "BigPools", "tags"))
    BigPools_plugin.add_command(label="show-free", command=lambda: set_pluginAndFlag(current_command, "BigPools", "show-free"))
    commands_menu.add_cascade(label="BigPools", menu=BigPools_plugin)

    # Cachedump_plugin
    Cachedump_plugin = Menu(commands_menu, tearoff=0)
    Cachedump_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Cachedump", "kernel"))
    Cachedump_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "Cachedump", "hivelist"))
    Cachedump_plugin.add_command(label="lsadump", command=lambda: set_pluginAndFlag(current_command, "Cachedump", "lsadump"))
    Cachedump_plugin.add_command(label="hashdump", command=lambda: set_pluginAndFlag(current_command, "Cachedump", "hashdump"))
    commands_menu.add_cascade(label="Cachedump", menu=Cachedump_plugin)

    # Callbacks_plugin
    Callbacks_plugin = Menu(commands_menu, tearoff=0)
    Callbacks_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Callbacks", "kernel"))
    Callbacks_plugin.add_command(label="ssdt", command=lambda: set_pluginAndFlag(current_command, "Callbacks", "ssdt"))
    commands_menu.add_cascade(label="Callbacks", menu=Callbacks_plugin)

    # CmdLine_plugin
    CmdLine_plugin = Menu(commands_menu, tearoff=0)
    CmdLine_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "CmdLine", "kernel"))
    CmdLine_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "CmdLine", "pslist"))
    CmdLine_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "CmdLine", "pid"))
    commands_menu.add_cascade(label="CmdLine", menu=CmdLine_plugin)

    # Crashinfo_plugin
    Crashinfo_plugin = Menu(commands_menu, tearoff=0)
    Crashinfo_plugin.add_command(label="primary", command=lambda: set_pluginAndFlag(current_command, "Crashinfo", "primary"))
    commands_menu.add_cascade(label="Crashinfo", menu=Crashinfo_plugin)

    # DeviceTree_plugin
    DeviceTree_plugin = Menu(commands_menu, tearoff=0)
    DeviceTree_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DeviceTree", "kernel"))
    DeviceTree_plugin.add_command(label="driverscan", command=lambda: set_pluginAndFlag(current_command, "DeviceTree", "driverscan"))
    commands_menu.add_cascade(label="DeviceTree", menu=DeviceTree_plugin)

    # DllList_plugin
    DllList_plugin = Menu(commands_menu, tearoff=0)
    DllList_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DllList", "kernel"))
    DllList_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "DllList", "pslist"))
    DllList_plugin.add_command(label="psscan", command=lambda: set_pluginAndFlag(current_command, "DllList", "psscan"))
    DllList_plugin.add_command(label="info", command=lambda: set_pluginAndFlag(current_command, "DllList", "info"))
    DllList_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "DllList", "pid"))
    DllList_plugin.add_command(label="offset", command=lambda: set_pluginAndFlag(current_command, "DllList", "offset"))
    DllList_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "DllList", "dump"))
    commands_menu.add_cascade(label="DllList", menu=DllList_plugin)

    # DriverIrp_plugin
    DriverIrp_plugin = Menu(commands_menu, tearoff=0)
    DriverIrp_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DriverIrp", "kernel"))
    DriverIrp_plugin.add_command(label="ssdt", command=lambda: set_pluginAndFlag(current_command, "DriverIrp", "ssdt"))
    DriverIrp_plugin.add_command(label="driverscan", command=lambda: set_pluginAndFlag(current_command, "DriverIrp", "driverscan"))
    commands_menu.add_cascade(label="DriverIrp", menu=DriverIrp_plugin)

    # DriverModule_plugin
    DriverModule_plugin = Menu(commands_menu, tearoff=0)
    DriverModule_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DriverModule", "kernel"))
    DriverModule_plugin.add_command(label="ssdt", command=lambda: set_pluginAndFlag(current_command, "DriverModule", "ssdt"))
    DriverModule_plugin.add_command(label="driverscan", command=lambda: set_pluginAndFlag(current_command, "DriverModule", "driverscan"))
    commands_menu.add_cascade(label="DriverModule", menu=DriverModule_plugin)

    # DriverScan_plugin
    DriverScan_plugin = Menu(commands_menu, tearoff=0)
    DriverScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DriverScan", "kernel"))
    DriverScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "DriverScan", "poolscanner"))
    commands_menu.add_cascade(label="DriverScan", menu=DriverScan_plugin)

    # DumpFiles_plugin
    DumpFiles_plugin = Menu(commands_menu, tearoff=0)
    DumpFiles_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "kernel"))
    DumpFiles_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "pid"))
    DumpFiles_plugin.add_command(label="virtaddr", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "virtaddr"))
    DumpFiles_plugin.add_command(label="physaddr", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "physaddr"))
    DumpFiles_plugin.add_command(label="filter", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "filter"))
    DumpFiles_plugin.add_command(label="ignore-case", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "ignore-case"))
    DumpFiles_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "pslist"))
    DumpFiles_plugin.add_command(label="handles", command=lambda: set_pluginAndFlag(current_command, "DumpFiles", "handles"))
    commands_menu.add_cascade(label="DumpFiles", menu=DumpFiles_plugin)

    # Envars_plugin
    Envars_plugin = Menu(commands_menu, tearoff=0)
    Envars_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Envars", "kernel"))
    Envars_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Envars", "pid"))
    Envars_plugin.add_command(label="silent", command=lambda: set_pluginAndFlag(current_command, "Envars", "silent"))
    Envars_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Envars", "pslist"))
    Envars_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "Envars", "hivelist"))
    commands_menu.add_cascade(label="Envars", menu=Envars_plugin)

    # FileScan_plugin
    FileScan_plugin = Menu(commands_menu, tearoff=0)
    FileScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "FileScan", "kernel"))
    FileScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "FileScan", "poolscanner"))
    commands_menu.add_cascade(label="FileScan", menu=FileScan_plugin)

    # GetServiceSIDs_plugin
    GetServiceSIDs_plugin = Menu(commands_menu, tearoff=0)
    GetServiceSIDs_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "GetServiceSIDs", "kernel"))
    GetServiceSIDs_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "GetServiceSIDs", "hivelist"))
    commands_menu.add_cascade(label="GetServiceSIDs", menu=GetServiceSIDs_plugin)

    # GetSIDs_plugin
    GetSIDs_plugin = Menu(commands_menu, tearoff=0)
    GetSIDs_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "GetSIDs", "kernel"))
    GetSIDs_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "GetSIDs", "pid"))
    GetSIDs_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "GetSIDs", "pslist"))
    GetSIDs_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "GetSIDs", "hivelist"))
    commands_menu.add_cascade(label="GetSIDs", menu=GetSIDs_plugin)

    # Handles_plugin
    Handles_plugin = Menu(commands_menu, tearoff=0)
    Handles_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Handles", "kernel"))
    Handles_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Handles", "pslist"))
    Handles_plugin.add_command(label="psscan", command=lambda: set_pluginAndFlag(current_command, "Handles", "psscan"))
    Handles_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Handles", "pid"))
    Handles_plugin.add_command(label="offset", command=lambda: set_pluginAndFlag(current_command, "Handles", "offset"))
    commands_menu.add_cascade(label="Handles", menu=Handles_plugin)

    # Hashdump_plugin
    Hashdump_plugin = Menu(commands_menu, tearoff=0)
    Hashdump_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Hashdump", "kernel"))
    Hashdump_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "Hashdump", "hivelist"))
    commands_menu.add_cascade(label="Hashdump", menu=Hashdump_plugin)

    # IAT_plugin
    IAT_plugin = Menu(commands_menu, tearoff=0)
    IAT_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "IAT", "kernel"))
    IAT_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "IAT", "pslist"))
    IAT_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "IAT", "pid"))
    commands_menu.add_cascade(label="IAT", menu=IAT_plugin)

    # Info_plugin
    Info_plugin = Menu(commands_menu, tearoff=0)
    Info_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Info", "kernel"))
    commands_menu.add_cascade(label="Info", menu=Info_plugin)

    # JobLinks_plugin
    JobLinks_plugin = Menu(commands_menu, tearoff=0)
    JobLinks_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "JobLinks", "kernel"))
    JobLinks_plugin.add_command(label="physical", command=lambda: set_pluginAndFlag(current_command, "JobLinks", "physical"))
    JobLinks_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "JobLinks", "pslist"))
    commands_menu.add_cascade(label="JobLinks", menu=JobLinks_plugin)

    # LdrModules_plugin
    LdrModules_plugin = Menu(commands_menu, tearoff=0)
    LdrModules_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "LdrModules", "kernel"))
    LdrModules_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "LdrModules", "pslist"))
    LdrModules_plugin.add_command(label="vadinfo", command=lambda: set_pluginAndFlag(current_command, "LdrModules", "vadinfo"))
    LdrModules_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "LdrModules", "pid"))
    commands_menu.add_cascade(label="LdrModules", menu=LdrModules_plugin)

    # Lsadump_plugin
    Lsadump_plugin = Menu(commands_menu, tearoff=0)
    Lsadump_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Lsadump", "kernel"))
    Lsadump_plugin.add_command(label="hashdump", command=lambda: set_pluginAndFlag(current_command, "Lsadump", "hashdump"))
    Lsadump_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "Lsadump", "hivelist"))
    commands_menu.add_cascade(label="Lsadump", menu=Lsadump_plugin)

    # Malfind_plugin
    Malfind_plugin = Menu(commands_menu, tearoff=0)
    Malfind_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Malfind", "kernel"))
    Malfind_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Malfind", "pid"))
    Malfind_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "Malfind", "dump"))
    Malfind_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Malfind", "pslist"))
    Malfind_plugin.add_command(label="vadinfo", command=lambda: set_pluginAndFlag(current_command, "Malfind", "vadinfo"))
    commands_menu.add_cascade(label="Malfind", menu=Malfind_plugin)

    # MBRScan_plugin
    MBRScan_plugin = Menu(commands_menu, tearoff=0)
    MBRScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "MBRScan", "kernel"))
    MBRScan_plugin.add_command(label="full", command=lambda: set_pluginAndFlag(current_command, "MBRScan", "full"))
    commands_menu.add_cascade(label="MBRScan", menu=MBRScan_plugin)

    # Memmap_plugin
    Memmap_plugin = Menu(commands_menu, tearoff=0)
    Memmap_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Memmap", "kernel"))
    Memmap_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Memmap", "pslist"))
    Memmap_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Memmap", "pid"))
    Memmap_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "Memmap", "dump"))
    commands_menu.add_cascade(label="Memmap", menu=Memmap_plugin)

    # MFTScan_plugin
    MFTScan_plugin = Menu(commands_menu, tearoff=0)
    MFTScan_plugin.add_command(label="primary", command=lambda: set_pluginAndFlag(current_command, "MFTScan", "primary"))
    MFTScan_plugin.add_command(label="yarascanner", command=lambda: set_pluginAndFlag(current_command, "MFTScan", "yarascanner"))
    commands_menu.add_cascade(label="MFTScan", menu=MFTScan_plugin)

    # ADS_plugin
    ADS_plugin = Menu(commands_menu, tearoff=0)
    ADS_plugin.add_command(label="primary", command=lambda: set_pluginAndFlag(current_command, "ADS", "primary"))
    ADS_plugin.add_command(label="yarascanner", command=lambda: set_pluginAndFlag(current_command, "ADS", "yarascanner"))
    commands_menu.add_cascade(label="ADS", menu=ADS_plugin)

    # ModScan_plugin
    ModScan_plugin = Menu(commands_menu, tearoff=0)
    ModScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "ModScan", "kernel"))
    ModScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "ModScan", "poolscanner"))
    ModScan_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "ModScan", "pslist"))
    ModScan_plugin.add_command(label="dlllist", command=lambda: set_pluginAndFlag(current_command, "ModScan", "dlllist"))
    ModScan_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "ModScan", "dump"))
    commands_menu.add_cascade(label="ModScan", menu=ModScan_plugin)

    # Modules_plugin
    Modules_plugin = Menu(commands_menu, tearoff=0)
    Modules_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Modules", "kernel"))
    Modules_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Modules", "pslist"))
    Modules_plugin.add_command(label="dlllist", command=lambda: set_pluginAndFlag(current_command, "Modules", "dlllist"))
    Modules_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "Modules", "dump"))
    Modules_plugin.add_command(label="name", command=lambda: set_pluginAndFlag(current_command, "Modules", "name"))
    commands_menu.add_cascade(label="Modules", menu=Modules_plugin)

    # MutantScan_plugin
    MutantScan_plugin = Menu(commands_menu, tearoff=0)
    MutantScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "MutantScan", "kernel"))
    MutantScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "MutantScan", "poolscanner"))
    commands_menu.add_cascade(label="MutantScan", menu=MutantScan_plugin)

    # NetScan_plugin
    NetScan_plugin = Menu(commands_menu, tearoff=0)
    NetScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "NetScan", "kernel"))
    NetScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "NetScan", "poolscanner"))
    NetScan_plugin.add_command(label="info", command=lambda: set_pluginAndFlag(current_command, "NetScan", "info"))
    NetScan_plugin.add_command(label="verinfo", command=lambda: set_pluginAndFlag(current_command, "NetScan", "verinfo"))
    NetScan_plugin.add_command(label="include-corrupt", command=lambda: set_pluginAndFlag(current_command, "NetScan", "include-corrupt"))
    commands_menu.add_cascade(label="NetScan", menu=NetScan_plugin)

    # NetStat_plugin
    NetStat_plugin = Menu(commands_menu, tearoff=0)
    NetStat_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "NetStat", "kernel"))
    NetStat_plugin.add_command(label="netscan", command=lambda: set_pluginAndFlag(current_command, "NetStat", "netscan"))
    NetStat_plugin.add_command(label="modules", command=lambda: set_pluginAndFlag(current_command, "NetStat", "modules"))
    NetStat_plugin.add_command(label="pdbutil", command=lambda: set_pluginAndFlag(current_command, "NetStat", "pdbutil"))
    NetStat_plugin.add_command(label="info", command=lambda: set_pluginAndFlag(current_command, "NetStat", "info"))
    NetStat_plugin.add_command(label="verinfo", command=lambda: set_pluginAndFlag(current_command, "NetStat", "verinfo"))
    NetStat_plugin.add_command(label="include-corrupt", command=lambda: set_pluginAndFlag(current_command, "NetStat", "include-corrupt"))
    commands_menu.add_cascade(label="NetStat", menu=NetStat_plugin)

    # PoolScanner_plugin
    PoolScanner_plugin = Menu(commands_menu, tearoff=0)
    PoolScanner_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "PoolScanner", "kernel"))
    PoolScanner_plugin.add_command(label="handles", command=lambda: set_pluginAndFlag(current_command, "PoolScanner", "handles"))
    commands_menu.add_cascade(label="PoolScanner", menu=PoolScanner_plugin)

    # Privs_plugin
    Privs_plugin = Menu(commands_menu, tearoff=0)
    Privs_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Privs", "kernel"))
    Privs_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Privs", "pid"))
    Privs_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Privs", "pslist"))
    commands_menu.add_cascade(label="Privs", menu=Privs_plugin)

    # PsList_plugin
    PsList_plugin = Menu(commands_menu, tearoff=0)
    PsList_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "PsList", "kernel"))
    PsList_plugin.add_command(label="physical", command=lambda: set_pluginAndFlag(current_command, "PsList", "physical"))
    PsList_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "PsList", "pid"))
    PsList_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "PsList", "dump"))
    commands_menu.add_cascade(label="PsList", menu=PsList_plugin)

    # PsScan_plugin
    PsScan_plugin = Menu(commands_menu, tearoff=0)
    PsScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "PsScan", "kernel"))
    PsScan_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "PsScan", "pslist"))
    PsScan_plugin.add_command(label="info", command=lambda: set_pluginAndFlag(current_command, "PsScan", "info"))
    PsScan_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "PsScan", "pid"))
    PsScan_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "PsScan", "dump"))
    PsScan_plugin.add_command(label="physical", command=lambda: set_pluginAndFlag(current_command, "PsScan", "physical"))
    commands_menu.add_cascade(label="PsScan", menu=PsScan_plugin)

    # PsTree_plugin
    PsTree_plugin = Menu(commands_menu, tearoff=0)
    PsTree_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "PsTree", "kernel"))
    PsTree_plugin.add_command(label="physical", command=lambda: set_pluginAndFlag(current_command, "PsTree", "physical"))
    PsTree_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "PsTree", "pslist"))
    PsTree_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "PsTree", "pid"))
    commands_menu.add_cascade(label="PsTree", menu=PsTree_plugin)

    # Sessions_plugin
    Sessions_plugin = Menu(commands_menu, tearoff=0)
    Sessions_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Sessions", "kernel"))
    Sessions_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Sessions", "pslist"))
    Sessions_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Sessions", "pid"))
    commands_menu.add_cascade(label="Sessions", menu=Sessions_plugin)

    # Skeleton_Key_Check_plugin
    Skeleton_Key_Check_plugin = Menu(commands_menu, tearoff=0)
    Skeleton_Key_Check_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Skeleton_Key_Check", "kernel"))
    Skeleton_Key_Check_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Skeleton_Key_Check", "pslist"))
    Skeleton_Key_Check_plugin.add_command(label="vadinfo", command=lambda: set_pluginAndFlag(current_command, "Skeleton_Key_Check", "vadinfo"))
    Skeleton_Key_Check_plugin.add_command(label="pdbutil", command=lambda: set_pluginAndFlag(current_command, "Skeleton_Key_Check", "pdbutil"))
    commands_menu.add_cascade(label="Skeleton_Key_Check", menu=Skeleton_Key_Check_plugin)

    # SSDT_plugin
    SSDT_plugin = Menu(commands_menu, tearoff=0)
    SSDT_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "SSDT", "kernel"))
    SSDT_plugin.add_command(label="modules", command=lambda: set_pluginAndFlag(current_command, "SSDT", "modules"))
    commands_menu.add_cascade(label="SSDT", menu=SSDT_plugin)

    # Strings_plugin
    Strings_plugin = Menu(commands_menu, tearoff=0)
    Strings_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "Strings", "kernel"))
    Strings_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "Strings", "pslist"))
    Strings_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "Strings", "pid"))
    Strings_plugin.add_command(label="strings_file", command=lambda: set_pluginAndFlag(current_command, "Strings", "strings_file"))
    commands_menu.add_cascade(label="Strings", menu=Strings_plugin)

    # SvcScan_plugin
    SvcScan_plugin = Menu(commands_menu, tearoff=0)
    SvcScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "SvcScan", "kernel"))
    SvcScan_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "SvcScan", "pslist"))
    SvcScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "SvcScan", "poolscanner"))
    SvcScan_plugin.add_command(label="vadyarascan", command=lambda: set_pluginAndFlag(current_command, "SvcScan", "vadyarascan"))
    SvcScan_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "SvcScan", "hivelist"))
    commands_menu.add_cascade(label="SvcScan", menu=SvcScan_plugin)

    # SymlinkScan_plugin
    SymlinkScan_plugin = Menu(commands_menu, tearoff=0)
    SymlinkScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "SymlinkScan", "kernel"))
    commands_menu.add_cascade(label="SymlinkScan", menu=SymlinkScan_plugin)

    # ThrdScan_plugin
    ThrdScan_plugin = Menu(commands_menu, tearoff=0)
    ThrdScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "ThrdScan", "kernel"))
    ThrdScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "ThrdScan", "poolscanner"))
    commands_menu.add_cascade(label="ThrdScan", menu=ThrdScan_plugin)

    # Passphrase_plugin
    Passphrase_plugin = Menu(commands_menu, tearoff=0)
    Passphrase_plugin.add_command(label="modules", command=lambda: set_pluginAndFlag(current_command, "Passphrase", "modules"))
    Passphrase_plugin.add_command(label="min-length", command=lambda: set_pluginAndFlag(current_command, "Passphrase", "min-length"))
    commands_menu.add_cascade(label="Passphrase", menu=Passphrase_plugin)

    # VadInfo_plugin
    VadInfo_plugin = Menu(commands_menu, tearoff=0)
    VadInfo_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "kernel"))
    VadInfo_plugin.add_command(label="address", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "address"))
    VadInfo_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "pid"))
    VadInfo_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "pslist"))
    VadInfo_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "dump"))
    VadInfo_plugin.add_command(label="maxsize", command=lambda: set_pluginAndFlag(current_command, "VadInfo", "maxsize"))
    commands_menu.add_cascade(label="VadInfo", menu=VadInfo_plugin)

    # VadWalk_plugin
    VadWalk_plugin = Menu(commands_menu, tearoff=0)
    VadWalk_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "VadWalk", "kernel"))
    VadWalk_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "VadWalk", "pslist"))
    VadWalk_plugin.add_command(label="vadinfo", command=lambda: set_pluginAndFlag(current_command, "VadWalk", "vadinfo"))
    VadWalk_plugin.add_command(label="pid", command=lambda: set_pluginAndFlag(current_command, "VadWalk", "pid"))
    commands_menu.add_cascade(label="VadWalk", menu=VadWalk_plugin)

    # VadYaraScan_plugin
    VadYaraScan_plugin = Menu(commands_menu, tearoff=0)
    commands_menu.add_cascade(label="VadYaraScan", menu=VadYaraScan_plugin)

    # VerInfo_plugin
    VerInfo_plugin = Menu(commands_menu, tearoff=0)
    VerInfo_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "VerInfo", "kernel"))
    VerInfo_plugin.add_command(label="pslist", command=lambda: set_pluginAndFlag(current_command, "VerInfo", "pslist"))
    VerInfo_plugin.add_command(label="modules", command=lambda: set_pluginAndFlag(current_command, "VerInfo", "modules"))
    VerInfo_plugin.add_command(label="dlllist", command=lambda: set_pluginAndFlag(current_command, "VerInfo", "dlllist"))
    VerInfo_plugin.add_command(label="extensive", command=lambda: set_pluginAndFlag(current_command, "VerInfo", "extensive"))
    commands_menu.add_cascade(label="VerInfo", menu=VerInfo_plugin)

    # VirtMap_plugin
    VirtMap_plugin = Menu(commands_menu, tearoff=0)
    VirtMap_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "VirtMap", "kernel"))
    commands_menu.add_cascade(label="VirtMap", menu=VirtMap_plugin)

    # HiveList_plugin
    HiveList_plugin = Menu(commands_menu, tearoff=0)
    HiveList_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "HiveList", "kernel"))
    HiveList_plugin.add_command(label="filter", command=lambda: set_pluginAndFlag(current_command, "HiveList", "filter"))
    HiveList_plugin.add_command(label="hivescan", command=lambda: set_pluginAndFlag(current_command, "HiveList", "hivescan"))
    HiveList_plugin.add_command(label="dump", command=lambda: set_pluginAndFlag(current_command, "HiveList", "dump"))
    commands_menu.add_cascade(label="HiveList", menu=HiveList_plugin)

    # HiveScan_plugin
    HiveScan_plugin = Menu(commands_menu, tearoff=0)
    HiveScan_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "HiveScan", "kernel"))
    HiveScan_plugin.add_command(label="poolscanner", command=lambda: set_pluginAndFlag(current_command, "HiveScan", "poolscanner"))
    HiveScan_plugin.add_command(label="bigpools", command=lambda: set_pluginAndFlag(current_command, "HiveScan", "bigpools"))
    commands_menu.add_cascade(label="HiveScan", menu=HiveScan_plugin)

    # PrintKey_plugin
    PrintKey_plugin = Menu(commands_menu, tearoff=0)
    PrintKey_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "PrintKey", "kernel"))
    PrintKey_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "PrintKey", "hivelist"))
    PrintKey_plugin.add_command(label="offset", command=lambda: set_pluginAndFlag(current_command, "PrintKey", "offset"))
    PrintKey_plugin.add_command(label="key", command=lambda: set_pluginAndFlag(current_command, "PrintKey", "key"))
    PrintKey_plugin.add_command(label="recurse", command=lambda: set_pluginAndFlag(current_command, "PrintKey", "recurse"))
    commands_menu.add_cascade(label="PrintKey", menu=PrintKey_plugin)

    # UserAssist_plugin
    UserAssist_plugin = Menu(commands_menu, tearoff=0)
    UserAssist_plugin.add_command(label="kernel", command=lambda: set_pluginAndFlag(current_command, "UserAssist", "kernel"))
    UserAssist_plugin.add_command(label="offset", command=lambda: set_pluginAndFlag(current_command, "UserAssist", "offset"))
    UserAssist_plugin.add_command(label="hivelist", command=lambda: set_pluginAndFlag(current_command, "UserAssist", "hivelist"))
    commands_menu.add_cascade(label="UserAssist", menu=UserAssist_plugin)

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
