# JONNY KODE
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFont, ImageDraw, UnidentifiedImageError
import os





# Function to create and display a welcome window with a fade effect
def show_welcome_window():
    def transition_to_main(event=None):
        welcome_root.destroy()

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
    welcome_root.title("Tsukuyomi Program")
    welcome_root.geometry("800x600")  # Set the window size to match the main window

    # Create a canvas to layer the background image and the text
    welcome_canvas = tk.Canvas(welcome_root, width=800, height=600)
    welcome_canvas.pack(fill="both", expand=True)

    try:
        # Load and resize the background image
        image_path = os.path.join('images', 'intro.webp')  # Use the correct path to your image
        bg_image = Image.open(image_path).convert("RGBA")
        bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create an image item on the canvas
        bg_image_id = welcome_canvas.create_image(0, 0, anchor="nw", image=bg_photo)

        # Load the Naruto font
        font_path = os.path.join('font', 'intro_font.ttf')
        if not os.path.isfile(font_path):
            raise OSError(f"Font file not found: {font_path}")

        naruto_font = ImageFont.truetype(font_path, 48)

        # Create an image with text using the custom font
        text_image = Image.new("RGBA", (800, 600), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_image)
        draw.text((300, 250), "TSUKUYOMI", font=naruto_font, fill="white")
        arial_font = os.path.join('font', 'arial.ttf')
        draw.text((300, 320), "Forensics & Analysis", font=ImageFont.truetype(arial_font, 24), fill="white")
        text_photo = ImageTk.PhotoImage(text_image)

        # Create a text item on the canvas
        text_id = welcome_canvas.create_image(0, 0, anchor="nw", image=text_photo)
        welcome_canvas.text_photo = text_photo  # Keep a reference to avoid garbage collection

        # Create dot text on the canvas
        dot_id = welcome_canvas.create_text(400, 380, text="", font=(arial_font, 43), fill="white")
        print("fade_in_out")
        welcome_root.after(500, fade_in_out)  # Start the fade effect after a brief delay
        print("animate_dots")
        welcome_root.after(500, animate_dots)  # Start the dot animation
        welcome_root.bind("<Button-1>", transition_to_main)  # Skip intro screen on click
        welcome_root.after(5000, transition_to_main)  # Automatically transition to main window after a brief delay
        welcome_root.mainloop()

    except UnidentifiedImageError as e:
        messagebox.showerror("Error", f"An error occurred with the image: {e}")
    except OSError as e:
        messagebox.showerror("Error", f"An error occurred with the font: {e}")

