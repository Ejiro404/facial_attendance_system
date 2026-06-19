import cv2
import os
import numpy as np
import sys
from PIL import Image

# Ensure project root is available for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db import connect


DATASET_PATH = "data/images"
TRAINER_PATH = "trainer/trainer.yml"


def train_model():
    # Initialize LBPH face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load Haar Cascade classifier for face detection validation
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = []
    ids = []

    conn = connect()
    cursor = conn.cursor()

    # Retrieve all registered students
    cursor.execute("SELECT id FROM students")
    students = cursor.fetchall()

    for student in students:
        student_id = student[0]

        student_folder = os.path.join(DATASET_PATH, str(student_id))

        if not os.path.exists(student_folder):
            continue

        image_files = os.listdir(student_folder)

        for img_file in image_files:
            img_path = os.path.join(student_folder, img_file)

            try:
                # Load image and convert to grayscale
                img = Image.open(img_path).convert("L")
                img_numpy = np.array(img, "uint8")

                # Validate face region before training
                detected_faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in detected_faces:
                    faces.append(img_numpy[y:y+h, x:x+w])
                    ids.append(student_id)

            except Exception:
                # Skip unreadable or corrupted images
                print(f"Invalid image skipped: {img_path}")

    # Ensure training data exists
    if len(faces) == 0:
        print("No valid training data found")
        return

    print("Training LBPH model...")

    # Train recognizer using dataset
    recognizer.train(faces, np.array(ids))

    # Ensure trainer directory exists
    os.makedirs("trainer", exist_ok=True)

    # Save trained model
    recognizer.save(TRAINER_PATH)

    print(f"Model training completed. Saved at {TRAINER_PATH}")


if __name__ == "__main__":
    train_model()