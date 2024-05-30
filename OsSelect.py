
import tkinter as tk
import MainScreen

def SelectScreen():
    print("SelectScreen function()")
    ##button_frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def windows_button(system, frame, root):
    print("windows")
    clear_frame(frame)
    MainScreen.mainScreen("windows", root)

def OSX_button(system, frame, root):
    print("OSX")
    clear_frame(frame)
    MainScreen.mainScreen("OSX", root)

def Linux_button(system, frame, root):
    print("Linux")
    clear_frame(frame)
    MainScreen.mainScreen("Linux", root )



root = tk.Tk()
root.title("Centralized Buttons")

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=10, pady=10)

# Create buttons with colors and commands
button1 = tk.Button(button_frame, text="Windows", bg="white", fg="black", command= lambda:windows_button("Windows", button_frame, root))
button2 = tk.Button(button_frame, text="OSX", bg="white", fg="black", command= lambda:OSX_button("OSX", button_frame, root))
button3 = tk.Button(button_frame, text="Linux", bg="white", fg="black", command= lambda:Linux_button("Linux", button_frame, root))

# Use grid to place buttons within the frame
button1.grid(row=0, column=0, padx=10, pady=10)
button2.grid(row=0, column=1, padx=10, pady=10)
button3.grid(row=0, column=2, padx=10, pady=10)

# Center the button frame in the main window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
button_frame.grid(row=0, column=0, padx=10, pady=10)

# Run the application
root.mainloop()
