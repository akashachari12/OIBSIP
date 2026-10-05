import tkinter as tk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


window = tk.Tk()
window.title("BMI Calculator")
window.geometry("700x900")
window.resizable(False, False)

bmi_history = []

# Create database
connection = sqlite3.connect("bmi_history.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT
    )
""")

connection.commit()

# Add date column if it does not exist
try:
    cursor.execute(
        "ALTER TABLE bmi_records ADD COLUMN date_time TEXT"
    )
    connection.commit()
except sqlite3.OperationalError:
    pass


# ---------------- CALCULATE FUNCTION ----------------

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            result_label.config(
                text="Please enter positive values."
            )
            return

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"

        # Show result
        if category == "Underweight":
            result_color = "orange"
        elif category == "Normal weight":
            result_color = "green"
        elif category == "Overweight":
            result_color = "orange"
        else:
            result_color = "red"

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        # Save in temporary history
        bmi_history.append(
            f"BMI: {bmi:.2f} - {category}"
        )

        # Get current date and time
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        # Save result in database
        cursor.execute(
            """
            INSERT INTO bmi_records
            (weight, height, bmi, category, date_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (weight, height, bmi, category, date_time)
        )

        connection.commit()

    except ValueError:
        result_label.config(
            text="Please enter numbers only."
        )


# ---------------- CLEAR FUNCTION ----------------

def clear_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")


def show_history():
    cursor.execute(
        """
        SELECT weight, height, bmi, category, date_time
        FROM bmi_records
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("500x500")

    title_label = tk.Label(
        window,
        text="BMI Calculator",
        font=("Arial", 24, "bold")
    )  
    title_label.pack(pady=20)

    if not records:
        empty_label = tk.Label(
            history_window,
            text="No BMI records found.",
            font=("Arial", 12)
        )
        empty_label.pack(pady=20)
        return

    for record in records:
        weight, height, bmi, category, date_time = record

        history_label = tk.Label(
            history_window,
            text=(
                f"Weight: {weight} kg\n"
                f"Height: {height} m\n"
                f"BMI: {bmi:.2f}\n"
                f"Category: {category}\n"
                f"Date: {date_time}\n"
                "-----------------------------"
            ),
            font=("Arial", 11),
            justify="left"
        )

        history_label.pack(
            anchor="w",
            padx=20,
            pady=8
        )
        
def clear_history():
    cursor.execute("DELETE FROM bmi_records")
    connection.commit()

    bmi_history.clear()

    result_label.config(text="BMI history cleared!")

    history_title = tk.Label(
        history_window,
        text="BMI HISTORY",
        font=("Arial", 20, "bold")
    )
    history_title.pack(pady=20)

    # Get records from database
    cursor.execute(
    "SELECT weight, height, bmi, category, date_time FROM bmi_records"
)

    records = cursor.fetchall()

    if records:
        for record in records:
            weight, height, bmi, category, date_time = record

            history_label = tk.Label(
                history_window,
                text=f"Weight: {weight} kg | "
     f"Height: {height} m\n"
     f"BMI: {bmi:.2f} | Category: {category}\n"
     f"Date: {date_time}",
                font=("Arial", 11),
                pady=8
            )
            history_label.pack()

    else:
        history_label = tk.Label(
            history_window,
            text="No BMI records found.",
            font=("Arial", 12)
        )
        history_label.pack(pady=20)

def show_graph():
    cursor.execute(
        """
        SELECT bmi, date_time
        FROM bmi_records
        WHERE date_time IS NOT NULL
        ORDER BY id
        """
    )

    records = cursor.fetchall()

    if not records:
        result_label.config(
            text="No BMI records available for graph."
        )
        return

    bmi_values = [record[0] for record in records]
    dates = [record[1] for record in records]

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(1, len(bmi_values) + 1),
        bmi_values,
        marker="o"
    )

    plt.xlabel("BMI Record")
    plt.ylabel("BMI")
    plt.title("BMI History")

    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ---------------- WEIGHT ----------------

weight_label = tk.Label(
    window,
    text="Weight (kg)",
    font=("Arial", 13)
)
weight_label.pack()

weight_entry = tk.Entry(
    window,
    font=("Arial", 14),
    width=20
)
weight_entry.pack(pady=8)

weight_label = tk.Label(
    window,
    text="Enter Weight (kg)",
    font=("Arial", 12, "bold")
)
weight_label.pack(pady=5)


# ---------------- HEIGHT ----------------

height_label = tk.Label(
    window,
    text="Height (meters)",
    font=("Arial", 13)
)
height_label.pack()

height_entry = tk.Entry(
    window,
    font=("Arial", 14),
    width=20
)
height_entry.pack(pady=8)

height_label = tk.Label(
    window,
    text="Enter Height (m)",
    font=("Arial", 12, "bold")
)
height_label.pack(pady=5)


# ---------------- BUTTONS ----------------

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    width=20,
    command=calculate_bmi
)
calculate_button.pack(pady=10)


clear_button = tk.Button(
    window,
    text="Clear",
    font=("Arial", 11),
    width=20,
    command=clear_fields
)
clear_button.pack(pady=5)

graph_button = tk.Button(
    window,
    text="Show BMI Graph",
    command=show_graph
)
graph_button.pack()

history_button = tk.Button(
    window,
    text="View History",
    font=("Arial", 12),
    width=18,
    command=show_history
)
history_button.pack(pady=10)

clear_button = tk.Button(
    window,
    text="Clear History",
    command=clear_history
)
clear_button.pack()


# ---------------- RESULT ----------------

result_label = tk.Label(
    window,
    text="",
    font=("Arial", 15, "bold")
)
result_label.pack(pady=30)

bmi_range_label = tk.Label(
    window,
    text=(
        "BMI Range:\n"
        "Below 18.5  → Underweight\n"
        "18.5 - 24.9 → Normal weight\n"
        "25.0 - 29.9 → Overweight\n"
        "30.0 or above → Obesity"
    ),
    font=("Arial", 11),
    justify="left"
)

bmi_range_label.pack(pady=10)


window.mainloop()