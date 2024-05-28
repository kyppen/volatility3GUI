import tkinter as tk
from tkinter import ttk, Menu



def mainScreen(OS, root):
    print("mainScreen")
    print(OS)
    root.title(OS)
    root.title("Dropdown Menu Example")
    root.geometry("300x200")

    left_frame = tk.Frame(root)

    selected_option = tk.StringVar()

    left_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    os_menu = Menu(left_frame, tearoff=0)
    os_menu.add_command(label="Windows", command=lambda:selected_option.set("Windows"))
    os_menu.add_command(label="OSX", command=lambda:selected_option.set("OSX"))
    os_menu.add_command(label="Linux", command=lambda:selected_option.set("Linux"))
    os_button = ttk.Menubutton(left_frame, text="OS", menu=os_menu)
    os_button.grid(row=0, column=0, columnspan=2, sticky="ne")




    # Create a button to trigger the display of the selected option
    ##button = ttk.Button(root, text="Show Selected", command=show_selected)
    ##button.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

