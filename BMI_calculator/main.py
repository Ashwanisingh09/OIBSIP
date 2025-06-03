import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite Database
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight REAL,
    height_cm REAL,
    bmi REAL,
    category TEXT
)
""")
conn.commit()

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            messagebox.showerror("Invalid Input", "Please enter positive numbers only.")
            return

        height_m = height_cm / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"

        result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        # Insert into database
        cursor.execute("INSERT INTO bmi_records (weight, height_cm, bmi, category) VALUES (?, ?, ?, ?)",
                       (weight, height_cm, bmi, category))
        conn.commit()

        messagebox.showinfo("Success", "BMI Recorded Successfully!")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Function to show history records
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")

    tree = ttk.Treeview(history_window, columns=("Weight", "Height (cm)", "BMI", "Category"), show="headings")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height (cm)", text="Height (cm)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")
    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT weight, height_cm, bmi, category FROM bmi_records")
    records = cursor.fetchall()
    for record in records:
        tree.insert("", "end", values=record)

# Function to plot BMI trend graph
def plot_graph():
    cursor.execute("SELECT id, bmi FROM bmi_records")
    data = cursor.fetchall()

    if not data:
        messagebox.showerror("No Data", "No data available to plot.")
        return

    ids, bmis = zip(*data)

    plt.figure(figsize=(8, 4))
    plt.plot(ids, bmis, marker='o', color='green')
    plt.title("BMI Trend Over Time")
    plt.xlabel("Record ID")
    plt.ylabel("BMI Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main GUI Window
root = tk.Tk()
root.title("BMI Calculator (Advanced)")
root.geometry("360x320")

# GUI Widgets
tk.Label(root, text="Enter your weight (kg):", font=("Arial", 11)).pack(pady=5)
weight_entry = tk.Entry(root, font=("Arial", 11))
weight_entry.pack()

tk.Label(root, text="Enter your height (cm):", font=("Arial", 11)).pack(pady=5)
height_entry = tk.Entry(root, font=("Arial", 11))
height_entry.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi, bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=10)
tk.Button(root, text="Show History", command=show_history, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=5)
tk.Button(root, text="Plot BMI Graph", command=plot_graph, bg="#FF9800", fg="white", font=("Arial", 11)).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run the application
root.mainloop()

# Close DB connection on exit
conn.close()
