import tkinter as tk
from tkinter import ttk, messagebox


def parse_number_lines(widget, label):
    raw_text = widget.get('1.0', tk.END)
    lines = raw_text.splitlines()

    values = []
    for line_index, line in enumerate(lines, start=1):
        text = line.strip()
        if text == '':
            continue
        try:
            values.append(float(text))
        except ValueError:
            raise ValueError(f"{label}, line {line_index}: '{text}' is not a valid number.")

    return values


def show_output(left_list, right_list):
    output_text.config(state='normal')
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"{left_list}\n\n{right_list}")
    output_text.config(state='disabled')


def convert_lists(event=None):
    try:
        left_list = parse_number_lines(left_input, 'Column 1')
        right_list = parse_number_lines(right_input, 'Column 2')
    except ValueError as exc:
        messagebox.showerror('Invalid input', str(exc))
        return

    if len(left_list) != len(right_list):
        messagebox.showerror(
            'Length mismatch',
            f'Column 1 has {len(left_list)} values, while Column 2 has {len(right_list)} values.\n\n'
            'Please make sure both columns contain the same number of numeric lines.'
        )
        return

    show_output(left_list, right_list)


def clear_all():
    left_input.delete('1.0', tk.END)
    right_input.delete('1.0', tk.END)
    output_text.config(state='normal')
    output_text.delete('1.0', tk.END)
    output_text.config(state='disabled')


root = tk.Tk()
root.title('Two-List Converter')
root.geometry('760x520')
root.minsize(680, 420)

main = ttk.Frame(root, padding=16)
main.pack(fill='both', expand=True)

intro_label = ttk.Label(
    main,
    text='Enter one number per line in each input box. Blank lines are ignored.'
)
intro_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 12))

left_label = ttk.Label(main, text='Column 1 / List 1 input')
left_label.grid(row=1, column=0, sticky='w', padx=(0, 8), pady=(0, 6))

right_label = ttk.Label(main, text='Column 2 / List 2 input')
right_label.grid(row=1, column=1, sticky='w', pady=(0, 6))

left_input = tk.Text(main, wrap='none', width=24)
left_input.grid(row=2, column=0, sticky='nsew', padx=(0, 8))

right_input = tk.Text(main, wrap='none', width=24)
right_input.grid(row=2, column=1, sticky='nsew')

button_frame = ttk.Frame(main)
button_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(12, 12))

convert_button = ttk.Button(button_frame, text='Convert', command=convert_lists)
convert_button.pack(side='left', fill='x', expand=True, padx=(0, 6))

clear_button = ttk.Button(button_frame, text='Clear', command=clear_all)
clear_button.pack(side='left', fill='x', expand=True)

output_label = ttk.Label(main, text='Output')
output_label.grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 6))

output_text = tk.Text(main, height=8, wrap='word')
output_text.grid(row=5, column=0, columnspan=2, sticky='nsew')
output_text.config(state='disabled')

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
main.rowconfigure(2, weight=1)
main.rowconfigure(5, weight=1)


root.mainloop()
