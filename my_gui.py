import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("code_saver.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS codes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 code TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

root = tk.Tk()
root.title("Code Saver")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

submitted_code = []

def save_code():
    code = code_input.get("1.0", tk.END).strip()
    if code:
        conn = sqlite3.connect("code_saver.db")
        c = conn.cursor()
        c.execute("INSERT INTO codes (code) VALUES (?)", (code,))
        conn.commit()
        conn.close()
        submitted_code.append(code)
        update_code_list()
        code_input.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Warning!", "No input provided")

def update_code_list():
    code_list.delete(0, tk.END)
    for i, code in enumerate(submitted_code, 1):
        preview = code.splitlines()[0][:50] + "..." if len(code.splitlines()[0]) > 50 else code.splitlines()[0]
        code_list.insert(tk.END, f"{i}: {preview}")

def show_full_code(event):
    selection = code_list.curselection()
    if selection:
        index = selection[0]
        full_code = submitted_code[index]
        code_display.config(state="normal")
        code_display.delete("1.0", tk.END)
        code_display.insert(tk.END, full_code)
        code_display.config(state="disabled")

def load_codes():
    conn = sqlite3.connect("code_saver.db")
    c = conn.cursor()
    c.execute("SELECT code FROM codes")
    rows = c.fetchall()
    conn.close()
    submitted_code.clear()
    for row in rows:
        submitted_code.append(row[0])
    update_code_list()

# Create two frames for side-by-side layout
left_frame = tk.Frame(root, bg="#f0f0f0")
left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, anchor=tk.N)

right_frame = tk.Frame(root, bg="#f0f0f0")
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True, anchor=tk.N)

# Left frame: Input and List (using pack)
header = tk.Label(left_frame, text="Submit Your Code: ", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
header.pack(pady=(0, 10))

input_label = tk.Label(left_frame, text="Enter Code Below:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
input_label.pack(pady=(0, 5))

code_input = scrolledtext.ScrolledText(left_frame, width=50, height=10, font=("Consolas", 11), bg="#ffffff", fg="#000000", borderwidth=2, relief="groove")
code_input.pack(pady=10)

save_button = tk.Button(left_frame, text="Save Code", command=save_code, font=("Arial", 11), bg="#4CAF50", fg="white", activebackground="#45a049", borderwidth=2, relief="raised")
save_button.pack(pady=10)

list_label = tk.Label(left_frame, text="Saved Codes:", font=("Arial", 11), bg="#f0f0f0", fg="#555555")
list_label.pack(pady=(0, 5))

code_list = tk.Listbox(left_frame, width=50, height=20, font=("Arial", 11), bg="#ffffff", fg="#333333", borderwidth=2, relief="groove")
code_list.pack(pady=10, fill=tk.BOTH, expand=True)
code_list.bind("<<ListboxSelect>>", show_full_code)

# Right frame: Preview (using grid consistently)
spacer = tk.Label(right_frame, text="", bg="#f0f0f0")
spacer.grid(row=0, column=0, pady=(0, 25))  # Spacer to align with header

display_label = tk.Label(right_frame, text="Selected Code Preview:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
display_label.grid(row=1, column=0, pady=(0, 5), sticky="w")  # Changed column to 0 for consistency

code_display = scrolledtext.ScrolledText(right_frame, width=50, height=30, font=("Consolas", 11), bg="#e0e0e0", fg="#000000", borderwidth=2, relief="groove")
code_display.grid(row=2, column=0, pady=10, sticky="nsew")
code_display.config(state="disabled")

# Configure grid to allow expansion
right_frame.grid_rowconfigure(2, weight=1)  # Row 2 (code_display) expands vertically
right_frame.grid_columnconfigure(0, weight=1)  # Column 0 expands horizontally

# Load existing codes
load_codes()

# Start the application
root.mainloop()