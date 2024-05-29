import tkinter as tk
from tkinter import filedialog
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


def browse_file():
    # Open file dialog and update the command with the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("Memory dump files", "*.raw"), ("All files", "*.*")])
    if file_path:  # Update the command only if a file is selected
        volatility_command[3] = file_path  # Update the file path in the command
        file_label.config(text=f"File: {file_path}")  # Update the label with the file name


# Set up the GUI
def create_gui():
    global path_entry, output_text, volatility_command, file_label

    root = tk.Tk()
    root.title("Volatility GUI")
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side=tk.LEFT, padx=10, pady=10)

    output_text = tk.Text(root, bg="white")
    output_text.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    # Initial Volatility command setup
    volatility_command = ['python', 'volatility3-develop\\vol.py', '-f', '', 'windows.pslist']

    # Browse file button
    browse_button = tk.Button(frame_buttons, text="Browse File", command=browse_file)
    browse_button.pack(fill=tk.X)

    file_label = tk.Label(frame_buttons, text="No file selected")
    file_label.pack(fill=tk.X)

    # Command button
    button_command = tk.Button(frame_buttons, text="Run Volatility Command",
                               command=lambda: run_volatility_command(volatility_command))
    button_command.pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
