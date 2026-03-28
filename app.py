import tkinter as tk
from tkinter import ttk, messagebox


ROW_COUNT = 20


def collect_rows():
    left_list = []
    right_list = []

    for row_index, (left_entry, right_entry) in enumerate(row_entries, start=1):
        left_text = left_entry.get().strip()
        right_text = right_entry.get().strip()

        # Ignore completely blank rows
        if left_text == "" and right_text == "":
            continue

        # Reject half-filled rows
        if left_text == "" or right_text == "":
            raise ValueError(f"Row {row_index}: both cells must be filled or both left blank.")

        try:
            left_value = float(left_text)
            right_value = float(right_text)
        except ValueError:
            raise ValueError(f"Row {row_index}: both values must be valid numbers.")

        left_list.append(left_value)
        right_list.append(right_value)

    return left_list, right_list


def show_output(left_list, right_list):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"{left_list}\n{right_list}")
    output_text.config(state="disabled")


def convert_rows(event=None):
    try:
        left_list, right_list = collect_rows()
    except ValueError as exc:
        messagebox.showerror("Invalid input", str(exc))
        return

    show_output(left_list, right_list)


def clear_all():
    for left_entry, right_entry in row_entries:
        left_entry.delete(0, tk.END)
        right_entry.delete(0, tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")


root = tk.Tk()
root.title("Two-Column Converter")
root.geometry("460x760")
root.minsize(420, 700)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

intro_label = ttk.Label(
    main,
    text="Enter up to 20 rows of numeric data. Blank rows are ignored.",
)
intro_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

header_row_label = ttk.Label(main, text="#")
header_row_label.grid(row=1, column=0, sticky="w", padx=(0, 8))

header_left_label = ttk.Label(main, text="Column 1")
header_left_label.grid(row=1, column=1, sticky="w", padx=(0, 8))

header_right_label = ttk.Label(main, text="Column 2")
header_right_label.grid(row=1, column=2, sticky="w")

row_entries = []

for i in range(ROW_COUNT):
    row_number = ttk.Label(main, text=str(i + 1))
    row_number.grid(row=i + 2, column=0, sticky="w", padx=(0, 8), pady=2)

    left_entry = ttk.Entry(main, width=16)
    left_entry.grid(row=i + 2, column=1, sticky="ew", padx=(0, 8), pady=2)

    right_entry = ttk.Entry(main, width=16)
    right_entry.grid(row=i + 2, column=2, sticky="ew", pady=2)

    row_entries.append((left_entry, right_entry))

button_frame = ttk.Frame(main)
button_frame.grid(row=ROW_COUNT + 2, column=0, columnspan=3, sticky="ew", pady=(14, 12))

convert_button = ttk.Button(button_frame, text="Convert", command=convert_rows)
convert_button.pack(side="left", fill="x", expand=True, padx=(0, 6))

clear_button = ttk.Button(button_frame, text="Clear", command=clear_all)
clear_button.pack(side="left", fill="x", expand=True)

output_label = ttk.Label(main, text="Output")
output_label.grid(row=ROW_COUNT + 3, column=0, columnspan=3, sticky="w", pady=(0, 6))

output_text = tk.Text(main, height=8, wrap="word")
output_text.grid(row=ROW_COUNT + 4, column=0, columnspan=3, sticky="nsew")
output_text.config(state="disabled")

main.columnconfigure(1, weight=1)
main.columnconfigure(2, weight=1)
main.rowconfigure(ROW_COUNT + 4, weight=1)

root.bind("<Return>", convert_rows)

root.mainloop()
