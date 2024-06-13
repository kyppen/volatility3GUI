import tkinter as tk

def search_in_text_field(search_term, text_with_line_numbers):
    text_with_line_numbers.text.tag_remove('highlight', '1.0', tk.END)

    if search_term:
        idx = '1.0'
        while True:
            idx = text_with_line_numbers.text.search(search_term, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break

            end_idx = f"{idx}+{len(search_term)}c"

            text_with_line_numbers.text.tag_add('highlight', idx, end_idx)

            idx = end_idx

        text_with_line_numbers.text.tag_config('highlight', background='yellow', foreground='black')