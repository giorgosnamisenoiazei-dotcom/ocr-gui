import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ====================== EXPIRATION SETTINGS ======================
# Change this line every time you make a new build
EXPIRATION_STR = "2026-03-29T13:24:36+02:00"   # ← 2 hours from now (as of your current time)

# Parse the expiration time
try:
    EXPIRATION_DATE = datetime.datetime.fromisoformat(EXPIRATION_STR)
except ValueError:
    # Fallback in case of formatting issue
    EXPIRATION_DATE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
# =================================================================

def is_expired():
    now = datetime.datetime.now(datetime.timezone.utc)      # Always compare in UTC
    expiration_utc = EXPIRATION_DATE.astimezone(datetime.timezone.utc)
    
    if now > expiration_utc:
        return True
    return False

def get_remaining_time():
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration_utc = EXPIRATION_DATE.astimezone(datetime.timezone.utc)
    remaining = expiration_utc - now
    
    if remaining.total_seconds() <= 0:
        return 0
    
    hours = int(remaining.total_seconds() // 3600)
    minutes = int((remaining.total_seconds() % 3600) // 60)
    return f"{hours}h {minutes:02d}m"

# ====================== MAIN APPLICATION ======================
if is_expired():
    messagebox.showerror(
        "Version Expired",
        "This version of the application has expired.\n\n"
        "Please download a newer version."
    )
    exit()   # Close immediately

# App starts normally
root = tk.Tk()
root.title(f"Adder GUI - Expires in {get_remaining_time()}")
root.geometry("340x280")
root.minsize(340, 280)

main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

entry_a = ttk.Entry(main, width=25)
entry_b = ttk.Entry(main, width=25)
result_var = tk.StringVar(value="")

ttk.Label(main, text="First number:").grid(row=0, column=0, sticky="w", pady=(0, 5))
entry_a.grid(row=1, column=0, sticky="ew", pady=(0, 15))

ttk.Label(main, text="Second number:").grid(row=2, column=0, sticky="w", pady=(0, 5))
entry_b.grid(row=3, column=0, sticky="ew", pady=(0, 15))

ttk.Button(main, text="Add", command=lambda: add_numbers()).grid(row=4, column=0, sticky="ew", pady=(0, 15))

ttk.Label(main, text="Result:").grid(row=5, column=0, sticky="w", pady=(0, 5))
result_entry = ttk.Entry(main, textvariable=result_var, state="readonly", width=25)
result_entry.grid(row=6, column=0, sticky="ew")

main.columnconfigure(0, weight=1)

def add_numbers(event=None):
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        result_var.set(str(a + b))
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers in both fields.")

root.bind("<Return>", add_numbers)

root.mainloop()
