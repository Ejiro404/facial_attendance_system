import tkinter as tk
from tkinter import ttk
from database.db import connect


def open_records():
    window = tk.Toplevel()
    window.title("Attendance Records Dashboard")
    window.geometry("950x550")
    window.config(bg="#0f172a")

    # Search input
    search_var = tk.StringVar()

    tk.Label(
        window,
        text="Search Records (Name / Matric / Status / Date)",
        bg="#0f172a",
        fg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=10)

    search_entry = tk.Entry(window, textvariable=search_var, width=50)
    search_entry.pack(pady=5)

    # Table
    tree = ttk.Treeview(
        window,
        columns=("Name", "Matric", "Date", "Status"),
        show="headings"
    )

    tree.heading("Name", text="Student Name")
    tree.heading("Matric", text="Matric Number")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")

    tree.column("Name", width=220)
    tree.column("Matric", width=160)
    tree.column("Date", width=180)
    tree.column("Status", width=120)

    tree.pack(fill="both", expand=True, pady=15)

    # Load data from DB
    def load_data(filter_text=""):
        tree.delete(*tree.get_children())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.full_name, s.matric_no, a.id, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            if filter_text.lower() in str(row).lower():
                tree.insert("", "end", values=row)

    # Live search (no button needed)
    def on_search(*args):
        load_data(search_var.get())

    search_var.trace("w", on_search)

    # Refresh function
    def refresh():
        search_var.set("")
        load_data()

    # Button panel
    btn_frame = tk.Frame(window, bg="#0f172a")
    btn_frame.pack(pady=5)

    tk.Button(
        btn_frame,
        text="Refresh",
        command=refresh,
        width=15
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        btn_frame,
        text="Clear Search",
        command=lambda: search_var.set(""),
        width=15
    ).grid(row=0, column=1, padx=10)

    load_data()