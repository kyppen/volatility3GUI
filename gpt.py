import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def open_file():
    file_path = filedialog.askopenfilename(title="Select Memory Dump File")
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def run_volatility():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a memory dump file.")
        return
    
    profile = profile_var.get()
    if not profile:
        messagebox.showerror("Error", "Please select an OS profile.")
        return

    plugin = plugin_var.get()
    if not plugin:
        messagebox.showerror("Error", "Please select a Volatility 3 plugin.")
        return

    full_plugin = f"{profile}.{plugin}"
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Running Volatility 3 with plugin '{full_plugin}' on file '{file_path}'...\n\n")
    
    try:
        result = subprocess.run(['volatility3/vol.py', '-f', file_path, full_plugin], capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Volatility 3 GUI")

# File selection
file_frame = tk.Frame(root)
file_frame.pack(pady=10)
file_label = tk.Label(file_frame, text="Memory Dump File:")
file_label.pack(side=tk.LEFT, padx=5)
file_entry = tk.Entry(file_frame, width=50)
file_entry.pack(side=tk.LEFT, padx=5)
file_button = tk.Button(file_frame, text="Browse", command=open_file)
file_button.pack(side=tk.LEFT, padx=5)

# Profile selection
profile_frame = tk.Frame(root)
profile_frame.pack(pady=10)
profile_label = tk.Label(profile_frame, text="OS Profile:")
profile_label.pack(side=tk.LEFT, padx=5)
profile_var = tk.StringVar()
profile_options = ['windows', 'linux', 'mac']
profile_menu = tk.OptionMenu(profile_frame, profile_var, *profile_options)
profile_menu.pack(side=tk.LEFT, padx=5)

# Plugin selection
plugin_frame = tk.Frame(root)
plugin_frame.pack(pady=10)
plugin_label = tk.Label(plugin_frame, text="Volatility 3 Plugin:")
plugin_label.pack(side=tk.LEFT, padx=5)
plugin_var = tk.StringVar()
plugin_options = ['pslist', 'pstree', 'dlllist', 'filescan', 'cmdline', 'netscan']
plugin_menu = tk.OptionMenu(plugin_frame, plugin_var, *plugin_options)
plugin_menu.pack(side=tk.LEFT, padx=5)

# Run button
run_button = tk.Button(root, text="Run", command=run_volatility)
run_button.pack(pady=10)

# Output text box
output_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
output_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
