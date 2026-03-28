import tkinter as tk
# Base Tkinter module.
# We use this for:
# - tk.Tk()        -> the main window
# - tk.Text        -> multiline text boxes
# - tk.END         -> "end of text" marker when reading/deleting text

from tkinter import ttk, messagebox
# ttk gives the themed widgets:
# - ttk.Frame
# - ttk.Label
# - ttk.Button
#
# messagebox gives popup dialogs like error messages.


def parse_number_lines(widget, label):
    """
    Read all lines from a Text widget and convert them into a list of floats.

    Parameters
    ----------
    widget : tk.Text
        The multiline input box we want to read from.
    label : str
        A human-readable name like 'Column 1' or 'Column 2'.
        This is used only to produce better error messages.

    Returns
    -------
    list[float]
        A list of numeric values extracted from the widget.

    Behavior
    --------
    - Blank lines are ignored.
    - Any non-blank line must be a valid number.
    - If a line is invalid, a ValueError is raised.
    """

    raw_text = widget.get("1.0", tk.END)
    # Read the entire contents of the Text widget.
    #
    # In Tkinter Text widgets, positions are written as "line.character":
    #   "1.0" means line 1, character 0
    #
    # tk.END means "go all the way to the end".

    lines = raw_text.splitlines()
    # Break the full text into a Python list of separate lines.

    values = []
    # This will store the successfully parsed numbers.

    for line_index, line in enumerate(lines, start=1):
        # Loop through the lines one by one.
        #
        # enumerate(..., start=1) means:
        # - first line gets number 1
        # - second line gets number 2
        # etc.
        #
        # That is useful for user-facing error messages.

        text = line.strip()
        # Remove leading/trailing spaces.
        #
        # Example:
        # "   322.17   " -> "322.17"

        if text == "":
            continue
        # Ignore blank lines completely.
        #
        # This is important because it lets the user leave
        # empty lines in the input without breaking the app.

        try:
            values.append(float(text))
            # Convert the cleaned line to a float and store it.
            #
            # Examples:
            # "5"      -> 5.0
            # "4.87"   -> 4.87
            # "-1.65"  -> -1.65

        except ValueError:
            # float(text) failed, so the line is not a valid number.
            # We raise our own clearer error message.

            raise ValueError(
                f"{label}, line {line_index}: '{text}' is not a valid number."
            )

    return values
    # After all lines are processed, return the final numeric list.


def show_output(left_list, right_list):
    """
    Display the two resulting lists in the output text box.
    """

    output_text.config(state="normal")
    # The output box is normally disabled so the user cannot type in it.
    # To update it from code, we temporarily enable it.

    output_text.delete("1.0", tk.END)
    # Remove any previous output.

    output_text.insert(tk.END, f"{left_list}\n\n{right_list}")
    # Insert the two lists as text.
    #
    # Example:
    # [322.17, 314.41, 323.12]
    #
    # [0.05, 4.87, 7.74]

    output_text.config(state="disabled")
    # Lock the output box again so it behaves like a display field.


def convert_lists():
    """
    Main action function.
    This runs when the user clicks the Convert button.
    """

    try:
        left_list = parse_number_lines(left_input, "Column 1")
        right_list = parse_number_lines(right_input, "Column 2")
        # Read and parse both input boxes.

    except ValueError as exc:
        # If either parse fails, show a popup error and stop.

        messagebox.showerror("Invalid input", str(exc))
        return

    if len(left_list) != len(right_list):
        # The two inputs must contain the same number of valid numeric lines.
        # Otherwise there is no clear 1-to-1 correspondence between rows.

        messagebox.showerror(
            "Length mismatch",
            f"Column 1 has {len(left_list)} values, while Column 2 has {len(right_list)} values.\n\n"
            "Please make sure both columns contain the same number of numeric lines."
        )
        return

    show_output(left_list, right_list)
    # If parsing succeeds and lengths match, show the result.


def clear_all():
    """
    Clear both input boxes and the output box.
    """

    left_input.delete("1.0", tk.END)
    # Remove all text from the left input box.

    right_input.delete("1.0", tk.END)
    # Remove all text from the right input box.

    output_text.config(state="normal")
    # Temporarily unlock the output box.

    output_text.delete("1.0", tk.END)
    # Clear the output area.

    output_text.config(state="disabled")
    # Lock the output box again.


# -------------------------
# Build the main window
# -------------------------

root = tk.Tk()
# Create the main application window.

root.title("Two-List Converter")
# Set the text shown in the title bar.

root.geometry("760x520")
# Set the initial window size:
# width = 760 pixels
# height = 520 pixels

root.minsize(680, 420)
# Prevent the window from being shrunk below this size.
# This helps avoid ugly or cramped layouts.


# -------------------------
# Main container frame
# -------------------------

main = ttk.Frame(root, padding=16)
# Create a frame inside the root window.
# padding=16 adds internal spacing so widgets are not glued to the edges.

main.pack(fill="both", expand=True)
# Put the frame into the root window.
#
# fill="both" means it can expand horizontally and vertically.
# expand=True means it should take extra available space.


# -------------------------
# Intro text
# -------------------------

intro_label = ttk.Label(
    main,
    text="Enter one number per line in each input box. Blank lines are ignored."
)
# Create an explanatory label at the top.

intro_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
# Place the label using grid layout.
#
# row=0, column=0        -> top-left position in the grid
# columnspan=2           -> stretch across both columns
# sticky="w"             -> align left ("west")
# pady=(0, 12)           -> 0 px above, 12 px below


# -------------------------
# Labels for the two input boxes
# -------------------------

left_label = ttk.Label(main, text="Column 1 / List 1 input")
left_label.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))

right_label = ttk.Label(main, text="Column 2 / List 2 input")
right_label.grid(row=1, column=1, sticky="w", pady=(0, 6))

# These labels sit directly above the two input fields.


# -------------------------
# Main input widgets
# -------------------------

left_input = tk.Text(main, wrap="none", width=24)
# Create the left multiline text box.
#
# We use tk.Text, not ttk.Entry, because Entry is only single-line.
#
# wrap="none" means lines do not wrap automatically.
# width=24 is an approximate width in text characters.

left_input.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
# Place it in row 2, column 0.
#
# sticky="nsew" means the widget should stretch in all directions
# if the cell grows:
# n = north
# s = south
# e = east
# w = west

right_input = tk.Text(main, wrap="none", width=24)
# Create the right multiline text box.

right_input.grid(row=2, column=1, sticky="nsew")
# Place it beside the left input box.


# -------------------------
# Button row
# -------------------------

button_frame = ttk.Frame(main)
# Small sub-frame just for the buttons.

button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 12))
# Place the button frame under both input boxes.

convert_button = ttk.Button(button_frame, text="Convert", command=convert_lists)
# Create the Convert button.
#
# command=convert_lists means:
# when clicked, run the convert_lists() function.

convert_button.pack(side="left", fill="x", expand=True, padx=(0, 6))
# Pack it inside the button_frame from the left side.

clear_button = ttk.Button(button_frame, text="Clear", command=clear_all)
# Create the Clear button.

clear_button.pack(side="left", fill="x", expand=True)
# Pack it beside the Convert button.

# Note:
# Using pack() here is fine because this is a different parent container
# from the one using grid().
#
# main uses grid() for its children.
# button_frame uses pack() for its children.
#
# That is allowed.
#
# What you should avoid is mixing pack() and grid() inside the SAME parent.


# -------------------------
# Output section
# -------------------------

output_label = ttk.Label(main, text="Output")
output_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 6))
# Label above the output box.

output_text = tk.Text(main, height=8, wrap="word")
# Create the output text box.
#
# height=8 means about 8 lines tall initially.
# wrap="word" means long text wraps at word boundaries.

output_text.grid(row=5, column=0, columnspan=2, sticky="nsew")
# Place the output box beneath the output label.

output_text.config(state="disabled")
# Make the output box read-only from the user's perspective.


# -------------------------
# Resizing behavior
# -------------------------

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
# Allow both columns to expand equally when the window is resized.

main.rowconfigure(2, weight=1)
# Let the row containing the two input boxes expand vertically.

main.rowconfigure(5, weight=1)
# Let the output row expand vertically too.

# These lines are what make the text areas grow nicely when the window grows.


# -------------------------
# Start the app
# -------------------------

root.mainloop()
# Start Tkinter's event loop.
#
# This keeps the window alive and waiting for user actions:
# - typing
# - clicking buttons
# - resizing the window
# - closing the app
#
# Without mainloop(), the program would create the widgets and then exit.