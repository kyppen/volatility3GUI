import tkinter as tk
import subprocess

system = ""

def clear_frame(button_grid):
   for widgets in button_grid.winfo_children():
      widgets.destroy()

def windows_click(button_grid):
    print("Windows")
    clear_frame(button_grid)
    system = "Windows"


def OSX_click(button_grid):
    print("OSX")
    clear_frame(button_grid)
    system = "OSX"
    
def Linux_click(button_grid):
    print("Linux")
    clear_frame(button_grid)
    system = "Linux"
    

def Main_window():
    OSButton = tk.Frame(root)
    button1 = tk.Button(OSButton, text=system, bg="red", fg="black")
    button1.pack(side=tk.LEFT, padx=10, pady=10)


def Placeholder():
    print("Placeholder() called")
    BUTTON_WIDTH = 20
    BUTTON_HEIGHT = 10
    BUTTON_COLOR = "red"
    BUTTON_TEXT_COLOR = "white"


    root.geometry("500x500")
    button_grid = tk.Frame(root)
    button_grid.grid(row=0, column=0, padx=10, pady=10)


    Windows = tk.Button(button_grid, text="Windows", bg = BUTTON_COLOR, command= lambda:windows_click(button_grid))
    OSX = tk.Button(button_grid, text="OSX", bg = BUTTON_COLOR, command= lambda: OSX_click(button_grid))
    Linux = tk.Button(button_grid, text="Linux", bg = BUTTON_COLOR, command= lambda: Linux_click(button_grid))

    Windows.grid(row=0, column=0, padx=10, pady=10)
    OSX.grid(row=0, column=1, padx=10, pady=10)
    Linux.grid(row=0, column=2, padx=10, pady=10)
    
    Windows.config(height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
    OSX.config(height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
    Linux.config(height=BUTTON_HEIGHT, width=BUTTON_WIDTH)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    button_grid.grid(row=0, column=0, padx=10, pady=10)

    root.mainloop()

    
root = tk.Tk()
root.title("Select Os")
button_grid = tk.Frame(root)
button_grid.grid(row=0, column=0, padx=10, pady=10)
