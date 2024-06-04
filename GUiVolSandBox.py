import tkinter as tk
from tkinter import ttk, Menu, filedialog
import subprocess


def run_volatility_command(command):
    try:
        # Correct command execution with subprocess.run
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        output = result.stdout  # Capture stdout as output
    except subprocess.CalledProcessError as e:
        output = e.output  # Capture error output if command fails

    # Clear current output and insert new output to the text widget
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state="disabled")


def run_command(command_text):
    cmd_history = open("logs/command-logs.txt", "a+", encoding='utf-8')
    cmd_history.write(command_text + "\n")
    cmd_history.close()


def browse_file():
    # Open file dialog and update the command with the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("Memory dump files", "*.raw"), ("All files", "*.*")])
    if file_path:  # Update the command only if a file is selected
        volatility_command[3] = file_path  # Update the file path in the command
        file_label.config(text=f"File: {file_path}")  # Update the label with the file name


# Set up the GUI
def create_gui():
    global path_entry, selected_entry, cmd_var, flag_var, os_var, output_text, volatility_command, file_label

    root = tk.Tk()
    root.title("Volatility GUI")
    frame_buttons = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
    frame_buttons.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    left_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    output_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
    output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
    output_text = tk.Text(output_frame, wrap='word', height=15)
    output_text.grid(row=0, column=0, sticky='nsew')
    output_scroll = ttk.Scrollbar(output_frame, command=output_text.yview)
    output_scroll.grid(row=0, column=1, sticky='ns')
    output_text.config(yscrollcommand=output_scroll.set)

    # Initial Volatility command setup

    # Browse file button
    browse_button = ttk.Button(left_frame, text="Browse File", command=browse_file)
    browse_button.grid(row=3, column=0, pady=5)
    run_button = ttk.Button(left_frame, text="Run", command=lambda: run_volatility_command(create_gui()))
    run_button.grid(row=3, column=0, pady=5)
    file_label = ttk.Label(frame_buttons, text="No file selected")

    # Commands menu
    cmd_var = tk.StringVar()
    flag_var = tk.StringVar()
    commands_menu = Menu(left_frame, tearoff=0)

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

    commands_button = ttk.Menubutton(left_frame, text="Commands", menu=commands_menu)
    commands_button.grid(row=1, column=0, columnspan=2, sticky='ew')

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=10)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=10)

    frame_buttons.grid_rowconfigure(1, weight=1)
    frame_buttons.grid_columnconfigure(0, weight=1)
    frame_buttons.grid_columnconfigure(1, weight=1)

    output_frame.grid_rowconfigure(0, weight=1)
    output_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
