import cv2
import os
import numpy as np
from database.db import connect

# Dataset storage location for captured face images
DATASET_PATH = "data/images"

# Ensure base dataset directory exists
os.makedirs(DATASET_PATH, exist_ok=True)


def register_student(matric_no, full_name):
    conn = connect()
    cursor = conn.cursor()

    # Insert student record into database
    cursor.execute(
        "INSERT INTO students (matric_no, full_name) VALUES (?, ?)",
        (matric_no, full_name)
    )

    student_id = cursor.lastrowid
    conn.commit()

    # Create dedicated folder for each student
    student_folder = os.path.join(DATASET_PATH, str(student_id))
    os.makedirs(student_folder, exist_ok=True)

    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    count = 0
    max_images = 20
    min_images = 15

    print("Camera initialized. Position face in front of camera.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Camera feed not available.")
            break

        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Capture only first detected face per frame
        if len(faces) > 0:
            (x, y, w, h) = faces[0]

            count += 1

            # Crop face region
            face_img = gray[y:y+h, x:x+w]

            # Save captured face image
            img_path = f"{student_folder}/{count}.jpg"
            cv2.imwrite(img_path, face_img)

            # Draw detection box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Progress feedback
            cv2.putText(
                frame,
                f"Capturing Samples: {count}/{max_images}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Student Registration", frame)

        # Manual stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture manually stopped.")
            break

        # Auto stop when enough samples are collected
        if count >= max_images:
            print("Maximum image samples reached.")
            break

    cam.release()
    cv2.destroyAllWindows()

    # Validate dataset quality before accepting registration
    if count < min_images:
        print(f"Registration failed: only {count} samples captured (minimum required: {min_images})")
        return

    print(f"Student {full_name} registered successfully with {count} samples")