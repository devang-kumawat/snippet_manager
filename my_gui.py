import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("code_saver.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS codes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 code TEXT NOT NULL,
                 tags TEXT)''')  # Added title and tags
    conn.commit()
    conn.close()

init_db()

root = tk.Tk()
root.title("Code Saver")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

submitted_code = []  # Now stores tuples (title, code, tags)

def save_code():
    title = title_input.get().strip()
    code = code_input.get("1.0", tk.END).strip()
    tags = tags_input.get().strip()
    if title and code:
        conn = sqlite3.connect("code_saver.db")
        c = conn.cursor()
        c.execute("INSERT INTO codes (title, code, tags) VALUES (?, ?, ?)", (title, code, tags))
        conn.commit()
        conn.close()
        submitted_code.append((title, code, tags))
        update_code_list()
        title_input.delete(0, tk.END)
        code_input.delete("1.0", tk.END)
        tags_input.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning!", "Title and code are required!")

def update_code_list():
    code_list.delete(0, tk.END)
    for i, (title, code, tags) in enumerate(submitted_code, 1):
        preview = f"{title}: {code.splitlines()[0][:40]}..." if len(code.splitlines()[0]) > 40 else f"{title}: {code.splitlines()[0]}"
        code_list.insert(tk.END, f"{i}: {preview}")

def show_full_code(event):
    selection = code_list.curselection()
    if selection:
        index = selection[0]
        title, code, tags = submitted_code[index]
        code_display.config(state="normal")
        code_display.delete("1.0", tk.END)
        code_display.insert(tk.END, f"Title: {title}\nTags: {tags}\n\n{code}")
        code_display.config(state="disabled")

def load_codes():
    conn = sqlite3.connect("code_saver.db")
    c = conn.cursor()
    c.execute("SELECT title, code, tags FROM codes")
    rows = c.fetchall()
    conn.close()
    submitted_code.clear()
    for row in rows:
        submitted_code.append(row)
    update_code_list()

# Frames
left_frame = tk.Frame(root, bg="#f0f0f0")
left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, anchor=tk.N)

right_frame = tk.Frame(root, bg="#f0f0f0")
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True, anchor=tk.N)

# Left frame: Input and List
header = tk.Label(left_frame, text="Submit Your Code: ", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
header.pack(pady=(0, 10))

tk.Label(left_frame, text="Title:", font=("Arial", 12), bg="#f0f0f0", fg="#555555").pack(pady=(0, 5))
title_input = tk.Entry(left_frame, width=50, font=("Arial", 11))
title_input.pack(pady=5)

input_label = tk.Label(left_frame, text="Enter Code Below:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
input_label.pack(pady=(0, 5))
code_input = scrolledtext.ScrolledText(left_frame, width=50, height=10, font=("Consolas", 11), bg="#ffffff", fg="#000000", borderwidth=2, relief="groove")
code_input.pack(pady=10)

tk.Label(left_frame, text="Tags (comma-separated):", font=("Arial", 12), bg="#f0f0f0", fg="#555555").pack(pady=(0, 5))
tags_input = tk.Entry(left_frame, width=50, font=("Arial", 11))
tags_input.pack(pady=5)

save_button = tk.Button(left_frame, text="Save Code", command=save_code, font=("Arial", 11), bg="#4CAF50", fg="white", activebackground="#45a049", borderwidth=2, relief="raised")
save_button.pack(pady=10)

list_label = tk.Label(left_frame, text="Saved Codes:", font=("Arial", 11), bg="#f0f0f0", fg="#555555")
list_label.pack(pady=(0, 5))
code_list = tk.Listbox(left_frame, width=50, height=15, font=("Arial", 11), bg="#ffffff", fg="#333333", borderwidth=2, relief="groove")
code_list.pack(pady=10, fill=tk.BOTH, expand=True)
code_list.bind("<<ListboxSelect>>", show_full_code)

# Right frame: Preview (using grid)
spacer = tk.Label(right_frame, text="", bg="#f0f0f0")
spacer.grid(row=0, column=0, pady=(0, 25))

display_label = tk.Label(right_frame, text="Selected Code Preview:", font=("Arial", 12), bg="#f0f0f0", fg="#555555")
display_label.grid(row=1, column=0, pady=(0, 5), sticky="w")

code_display = scrolledtext.ScrolledText(right_frame, width=50, height=25, font=("Consolas", 11), bg="#e0e0e0", fg="#000000", borderwidth=2, relief="groove")
code_display.grid(row=2, column=0, pady=10, sticky="nsew")
code_display.config(state="disabled")

right_frame.grid_rowconfigure(2, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Load existing codes
load_codes()

root.mainloop()