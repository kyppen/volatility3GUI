import tkinter as tk

def search_in_text_field(search_term, text_with_line_numbers):
    # Clear previous tags
    text_with_line_numbers.text.tag_remove('highlight', '1.0', tk.END)

    if search_term:
        idx = '1.0'
        while True:
            # Search for the term starting from idx
            idx = text_with_line_numbers.text.search(search_term, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break

            # Get the end index of the search term
            end_idx = f"{idx}+{len(search_term)}c"

            # Highlight the found term
            text_with_line_numbers.text.tag_add('highlight', idx, end_idx)

            # Move the idx to the end of the found term
            idx = end_idx

        # Add a tag configuration for the highlight
        text_with_line_numbers.text.tag_config('highlight', background='yellow', foreground='black')