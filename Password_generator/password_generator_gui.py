import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# Function to check clipboard tool availability
def check_clipboard_tool():
    try:
        pyperclip.paste()
        return True
    except pyperclip.PyperclipException:
        return False

# Function to update password strength indicator
def update_strength_label(password):
    length = len(password)
    strength = ""
    color = "black"

    if length < 6:
        strength = "Weak"
        color = "#FF4C4C"
    elif 6 <= length < 10:
        strength = "Medium"
        color = "#FFA500"
    else:
        strength = "Strong"
        color = "#4CAF50"

    strength_label.config(text=f"Strength: {strength}", fg=color)

# Password generator function
def generate_password():
    length = length_var.get()
    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4")
        return

    char_pool = ""

    if upper_var.get():
        char_pool += string.ascii_uppercase
    if lower_var.get():
        char_pool += string.ascii_lowercase
    if number_var.get():
        char_pool += string.digits
    if symbol_var.get():
        # Safe symbols set (avoids encoding/display issues)
        safe_punctuation = "!#$%&()*+,-./:;<=>?@[]^_{|}~"
        char_pool += safe_punctuation

    if not char_pool:
        messagebox.showerror("Error", "Please select at least one character type!")
        return

    password = ''.join(random.choice(char_pool) for _ in range(length))
    
    # Debug: print to terminal
    print("Generated Password:", password)

    password_var.set(password)
    update_strength_label(password)

# Copy to clipboard function
def copy_password():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Warning", "No password to copy!")
        return

    if check_clipboard_tool():
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Clipboard Error", "No clipboard mechanism found on your system. Install xclip or xsel.")

# GUI setup
root = tk.Tk()
root.title("🔐 Advanced Password Generator")
root.geometry("500x440")
root.config(bg="#2C3E50")

title = tk.Label(root, text="🔒 Password Generator", font=("Helvetica", 22, "bold"), bg="#2C3E50", fg="#ECF0F1")
title.pack(pady=15)

main_frame = tk.Frame(root, bg="#34495E", bd=2, relief="ridge")
main_frame.pack(padx=20, pady=10, fill="both")

# Password Length
tk.Label(main_frame, text="Password Length:", bg="#34495E", fg="#ECF0F1", font=("Helvetica", 13)).grid(row=0, column=0, sticky="w", padx=10, pady=8)
length_var = tk.IntVar(value=12)
tk.Entry(main_frame, textvariable=length_var, width=5, font=("Helvetica", 12)).grid(row=0, column=1, padx=5)

# Character Options
upper_var = tk.BooleanVar()
lower_var = tk.BooleanVar()
number_var = tk.BooleanVar()
symbol_var = tk.BooleanVar()

tk.Checkbutton(main_frame, text="Uppercase (A-Z)", variable=upper_var, bg="#34495E", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", padx=10)
tk.Checkbutton(main_frame, text="Lowercase (a-z)", variable=lower_var, bg="#34495E", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", padx=10)
tk.Checkbutton(main_frame, text="Numbers (0-9)", variable=number_var, bg="#34495E", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w", padx=10)
tk.Checkbutton(main_frame, text="Symbols (!@#$...)", variable=symbol_var, bg="#34495E", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w", padx=10)

# Password Display
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, font=("Consolas", 18), width=30, justify="center", bd=3, relief="ridge")
password_entry.pack(pady=20)

# Strength Label
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1")
strength_label.pack()

# Buttons Frame
btn_frame = tk.Frame(root, bg="#2C3E50")
btn_frame.pack(pady=10)

generate_btn = tk.Button(btn_frame, text="Generate Password", command=generate_password, bg="#27AE60", fg="white", font=("Helvetica", 13), width=20, bd=0, activebackground="#2ECC71")
generate_btn.grid(row=0, column=0, padx=10)

copy_btn = tk.Button(btn_frame, text="Copy to Clipboard", command=copy_password, bg="#2980B9", fg="white", font=("Helvetica", 13), width=20, bd=0, activebackground="#3498DB")
copy_btn.grid(row=0, column=1, padx=10)

# Footer
footer = tk.Label(root, text="💾 Created by Ashwani Singh", font=("Helvetica", 11), bg="#2C3E50", fg="#BDC3C7")
footer.pack(pady=5)

root.mainloop()
