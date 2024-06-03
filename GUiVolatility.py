# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:33:10 2024

@author: benji
"""

import tkinter as tk
import subprocess
import openfile


# Function to run a Volatility command and display output
def run_volatility_command(command):
    # Run the Volatility command as a subprocess
    try:
        print("trying to run ")
        # Example: subprocess.check_output(['vol.py', '-f', '/path/to/file', 'windows.pslist'])
        output = subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    # Insert the command output to the text widget
    output_text.delete("1.0", tk.END)  # Clear the current output
    output_text.insert(tk.END, output)  # Insert the new output

# Create the main window
root = tk.Tk()
root.title("Volatility GUI")

# Create a frame for the buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.LEFT, padx=10, pady=10)

# Create a white empty space (text widget) on the right
output_text = tk.Text(root, bg="white")
output_text.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Add buttons to the frame, each with a command to execute
button4 = tk.Button(frame_buttons, text="open file",
                    command=lambda: openfile.browse_files)

testttt = ['python3 volatility3/vol.py', '-f', 'MSEDGEWIN10-20231107-184623.raw', 'windows.pstree']
button1 = tk.Button(frame_buttons, text="Command 1",
                    command=lambda: run_volatility_command(testttt))
button1.pack(fill=tk.X)
button2 = tk.Button(frame_buttons, text="Command 2",
                    command=lambda: run_volatility_command('volatility3/vol.py -f “/path/to/file” windows.psscan'))
button2.pack(fill=tk.X)

button3 = tk.Button(frame_buttons, text="Command 3",
                    command=lambda: run_volatility_command('volatility3/vol.py -f “/path/to/file” windows.pstree'))
button3.pack(fill=tk.X)

# Start the GUI event loop
root.mainloop()


