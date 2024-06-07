# JONNY KODE
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk, ImageEnhance, ImageFont, ImageDraw, UnidentifiedImageError
import subprocess
import os
import ctypes


# Function to open a file dialog and allow the user to select a memory dump file
def open_file():
    file_path = filedialog.askopenfilename(title="Select Memory Dump File")
    if file_path:
        file_entry.delete(0, tk.END)  # Clear the entry widget
        file_entry.insert(0, file_path)  # Insert the selected file path


# Function to run Volatility with the selected memory dump file, OS profile, and plugin
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

    output_text.delete(1.0, tk.END)  # Clear the output text box
    output_text.insert(tk.END, f"Running Volatility 3 with plugin '{full_plugin}' on file '{file_path}'...\n\n")

    try:
        # Run the Volatility tool and capture the output
        result = subprocess.run(['volatility3/vol.py', '-f', file_path, full_plugin], capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)  # Display the output in the text box
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {e}")


# Function to toggle between different themes
def toggle_theme():
    global current_theme
    themes = [light_theme, dark_theme, dark_orange_theme]
    current_theme = (current_theme + 1) % len(themes)
    apply_theme(themes[current_theme])
    toggle_title_bar_dark_mode(current_theme == 1 or current_theme == 2)


# Function to apply the selected theme to the root window and its widgets
def apply_theme(theme):
    root.config(bg=theme['bg'])
    for widget in root.winfo_children():
        apply_widget_theme(widget, theme)


# Function to apply the selected theme to an individual widget
def apply_widget_theme(widget, theme):
    widget_type = widget.winfo_class()
    if widget_type in ("Frame", "Label", "Button", "OptionMenu"):
        widget.config(bg=theme['bg'], fg=theme['fg'])
    if widget_type == "Text":
        widget.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['insertbackground'])
    if widget_type == "Entry":
        widget.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['insertbackground'])
    for child in widget.winfo_children():
        apply_widget_theme(child, theme)


# Function to toggle dark mode for the title bar (Windows only)
def toggle_title_bar_dark_mode(enable):
    if os.name == 'nt':
        try:
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
            value = 2 if enable else 1
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(value)),
                                                       ctypes.sizeof(ctypes.c_int))
        except Exception as e:
            print(f"Error setting title bar theme: {e}")


# Function to create the main application window
def create_main_window():
    global root, file_entry, profile_var, plugin_var, output_text, light_theme, dark_theme, dark_orange_theme, current_theme

    root = tk.Tk()
    root.title("Volatility 3 GUI")
    root.geometry("800x600")  # Set the window size to match the welcome window

    current_theme = 0

    # Define the themes
    light_theme = {
        'bg': 'white',
        'fg': 'black',
        'insertbackground': 'black'
    }

    dark_theme = {
        'bg': 'black',
        'fg': 'white',
        'insertbackground': 'white'
    }

    dark_orange_theme = {
        'bg': '#FF8C00',
        'fg': 'black',
        'insertbackground': 'black'
    }

    apply_theme(light_theme)  # Set initial theme

    # File selection section
    file_frame = tk.Frame(root)
    file_frame.pack(pady=10)
    file_label = tk.Label(file_frame, text="Memory Dump File:")
    file_label.pack(side=tk.LEFT, padx=5)
    file_entry = tk.Entry(file_frame, width=50)
    file_entry.pack(side=tk.LEFT, padx=5)
    file_button = tk.Button(file_frame, text="Browse", command=open_file)
    file_button.pack(side=tk.LEFT, padx=5)

    # Profile selection section
    profile_frame = tk.Frame(root)
    profile_frame.pack(pady=10)
    profile_label = tk.Label(profile_frame, text="OS Profile:")
    profile_label.pack(side=tk.LEFT, padx=5)
    profile_var = tk.StringVar()
    profile_options = ['windows', 'linux', 'mac']
    profile_menu = tk.OptionMenu(profile_frame, profile_var, *profile_options)
    profile_menu.pack(side=tk.LEFT, padx=5)

    # Plugin selection section
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

    # Output text box for displaying the results
    output_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
    output_text.pack(pady=10)

    # Theme toggle button
    theme_toggle_button = tk.Button(root, text="Toggle Theme", command=toggle_theme)
    theme_toggle_button.pack(pady=10)

    root.mainloop()


# Function to create and display a welcome window with a fade effect
def show_welcome_window():
    def transition_to_main(event=None):
        welcome_root.destroy()
        #create_main_window()

    def fade_in_out(step=0, reverse=False):
        alpha = step / 50 if not reverse else 1 - step / 50
        faded_image = ImageEnhance.Brightness(bg_image).enhance(alpha)
        faded_photo = ImageTk.PhotoImage(faded_image)
        welcome_canvas.itemconfig(bg_image_id, image=faded_photo)
        welcome_canvas.image = faded_photo  # Keep a reference to avoid garbage collection

        if step < 50 and not reverse:
            welcome_root.after(20, fade_in_out, step + 1, False)
        elif step > 0 and reverse:
            welcome_root.after(20, fade_in_out, step - 1, True)
        else:
            welcome_root.after(20, fade_in_out, 0, not reverse)  # Repeat the fading

    def animate_dots(step=0):
        dot_text = "." * ((step % 4) + 1)  # Create the dot animation with 4 dots
        welcome_canvas.itemconfig(dot_id, text=dot_text)
        welcome_root.after(500, animate_dots, step + 1)

    welcome_root = tk.Tk()
    welcome_root.title("Tsukyomi Program")
    welcome_root.geometry("800x600")  # Set the window size to match the main window

    # Create a canvas to layer the background image and the text
    welcome_canvas = tk.Canvas(welcome_root, width=800, height=600)
    welcome_canvas.pack(fill="both", expand=True)

    try:
        # Load and resize the background image
        image_path = r"images\intro.webp"  # Use the correct path to your image
        bg_image = Image.open(image_path).convert("RGBA")
        bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create an image item on the canvas
        bg_image_id = welcome_canvas.create_image(0, 0, anchor="nw", image=bg_photo)

        # Load the Naruto font
        font_path = r"font\intro_font.ttf"
        if not os.path.isfile(font_path):
            raise OSError(f"Font file not found: {font_path}")

        naruto_font = ImageFont.truetype(font_path, 48)

        # Create an image with text using the custom font
        text_image = Image.new("RGBA", (800, 600), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_image)
        draw.text((300, 250), "TSUKYOMI", font=naruto_font, fill="white")
        draw.text((300, 320), "Forensics & Analysis", font=ImageFont.truetype("arial.ttf", 24), fill="white")
        text_photo = ImageTk.PhotoImage(text_image)

        # Create a text item on the canvas
        text_id = welcome_canvas.create_image(0, 0, anchor="nw", image=text_photo)
        welcome_canvas.text_photo = text_photo  # Keep a reference to avoid garbage collection

        # Create dot text on the canvas
        dot_id = welcome_canvas.create_text(400, 380, text="", font=("Arial", 43), fill="white")

        welcome_root.after(500, fade_in_out)  # Start the fade effect after a brief delay
        welcome_root.after(500, animate_dots)  # Start the dot animation
        welcome_root.bind("<Button-1>", transition_to_main)  # Skip intro screen on click
        welcome_root.after(5000, transition_to_main)  # Automatically transition to main window after a brief delay
        welcome_root.mainloop()

    except UnidentifiedImageError as e:
        messagebox.showerror("Error", f"An error occurred with the image: {e}")
    except OSError as e:
        messagebox.showerror("Error", f"An error occurred with the font: {e}")


# Start the welcome window event loop
#show_welcome_window()