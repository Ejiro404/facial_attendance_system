import cv2
import numpy as np
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db import connect


TRAINER_PATH = "trainer/trainer.yml"
STABLE_FRAMES = 5


def get_student_name(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM students WHERE id=?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Unknown"


def create_session():
    conn = connect()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")
    start_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute(
        "INSERT INTO sessions (date, start_time) VALUES (?, ?)",
        (date, start_time)
    )

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return session_id


def mark_attendance(session_id, student_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM attendance
        WHERE student_id=? AND session_id=?
    """, (student_id, session_id))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO attendance (student_id, session_id, status)
            VALUES (?, ?, 'Present')
        """, (student_id, session_id))

    conn.commit()
    conn.close()


def run_recognition():
    if not os.path.exists(TRAINER_PATH):
        print("Model not found. Train first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    session_id = create_session()
    marked_students = set()
    stability_counter = {}

    print(f"Attendance session started: {session_id}")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        best_match = None
        best_conf = 999

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            student_id, confidence = recognizer.predict(face)

            if confidence < best_conf:
                best_conf = confidence
                best_match = (student_id, confidence, (x, y, w, h))

        if best_match:
            student_id, confidence, (x, y, w, h) = best_match

            # stability tracking
            if confidence < 70:
                stability_counter[student_id] = stability_counter.get(student_id, 0) + 1
            else:
                stability_counter[student_id] = 0

            name = get_student_name(student_id)

            # only mark after stable detection
            if stability_counter[student_id] >= STABLE_FRAMES:

                if student_id not in marked_students:
                    mark_attendance(session_id, student_id)
                    marked_students.add(student_id)

                    print(f"{name} marked present")

                label = f"{name} - Present"
                color = (0, 255, 0)

            else:
                label = f"{name} - Verifying..."
                color = (0, 255, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    print("Session ended")