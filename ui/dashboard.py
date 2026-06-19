import tkinter as tk
from tkinter import messagebox

from face.register import register_student
from face.recognizer import run_recognition
from attendance.export import export_attendance
from ui.records_view import open_records


def run_app():
    root = tk.Tk()
    root.title("Facial Attendance System")
    root.geometry("850x520")
    root.config(bg="#0f172a")

    # Header
    header = tk.Frame(root, bg="#0f172a")
    header.pack(pady=20)

    tk.Label(
        header,
        text="Facial Recognition Attendance System",
        font=("Helvetica", 20, "bold"),
        fg="#ffffff",
        bg="#0f172a"
    ).pack()

    tk.Label(
        header,
        text="Automated Student Attendance Using Computer Vision (LBPH)",
        font=("Helvetica", 11),
        fg="#94a3b8",
        bg="#0f172a"
    ).pack()

    # Main container
    container = tk.Frame(root, bg="#0f172a")
    container.pack(pady=30)

    btn_style = {
        "width": 30,
        "height": 2,
        "font": ("Helvetica", 11, "bold"),
        "bd": 0,
        "cursor": "hand2"
    }

    def styled_button(master, text, command, color):
        return tk.Button(
            master,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground="#1e293b",
            **btn_style
        )

    # Actions
    styled_button(
        container,
        "Register Student",
        register_popup,
        "#2563eb"
    ).pack(pady=8)

    styled_button(
        container,
        "Start Attendance",
        run_recognition,
        "#16a34a"
    ).pack(pady=8)

    styled_button(
        container,
        "Export Attendance Report",
        export_attendance,
        "#f59e0b"
    ).pack(pady=8)

    styled_button(
        container,
        "View Records",
        open_records,
        "#64748b"
    ).pack(pady=8)

    # Footer
    tk.Label(
        root,
        text="Final Year Project • Computer Vision • LBPH Algorithm",
        font=("Helvetica", 9),
        fg="#64748b",
        bg="#0f172a"
    ).pack(side="bottom", pady=10)

    root.mainloop()


def register_popup():
    popup = tk.Toplevel()
    popup.title("Student Registration")
    popup.geometry("320x220")
    popup.config(bg="#0f172a")

    tk.Label(popup, text="Matric Number", bg="#0f172a", fg="white").pack(pady=(15, 5))
    matric_entry = tk.Entry(popup, width=30)
    matric_entry.pack()

    tk.Label(popup, text="Full Name", bg="#0f172a", fg="white").pack(pady=(10, 5))
    name_entry = tk.Entry(popup, width=30)
    name_entry.pack()

    def submit():
        matric_no = matric_entry.get().strip()
        full_name = name_entry.get().strip()

        if matric_no and full_name:
            register_student(matric_no, full_name)
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    tk.Button(
        popup,
        text="Start Camera Capture",
        command=submit,
        bg="#2563eb",
        fg="white",
        width=25,
        height=2
    ).pack(pady=20)