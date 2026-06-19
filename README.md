**Facial Recognition Attendance System (LBPH OpenCV)**

**Project Overview**

This is an automated attendance system built using Python and OpenCV. It uses facial recognition to identify students and mark attendance in real time through a webcam. The system replaces manual attendance tracking with an image-based recognition pipeline powered by the LBPH algorithm.

It is designed for classroom environments and small to medium-sized student groups. The system supports student registration, dataset creation, model training, real-time recognition, attendance logging, and data export.


**Key Features**

Student registration through webcam image capture
Face detection and recognition using OpenCV LBPH algorithm
Real-time attendance marking using webcam input
SQLite database for storing student and attendance records
Export attendance data to CSV or Excel format
Simple desktop interface using Tkinter
Prevents duplicate attendance marking within a session
Fully offline system once installed


**Tech Stack**

Python 3.x
OpenCV
NumPy
Pandas
SQLite3
Tkinter
OpenPyXL


**System Workflow**

Student Registration
Face image capture via webcam
Dataset storage on local machine

Model Training
LBPH algorithm trains on captured images
Generates trained model file

Face Recognition
Live webcam feed detects faces
System compares faces with trained model

Attendance Marking
Recognized students are marked present
Stored in SQLite database

Export
Attendance records exported to Excel or CSV


**Project Structure**

Facial-Attendance-System
face (face detection and recognition logic)
attendance (attendance processing and export functions)
trainer (model training scripts)
data (stored face images)
dashboard.py (main application interface)
main.py (entry point if applicable)
trainer.yml (trained LBPH model)
requirements.txt
README.md



**How to Run**

Clone repository
git clone https://github.com/yourusername/facial-attendance-system.git
cd facial-attendance-system

Install dependencies
pip install -r requirements.txt

Run application
python main.py



**How It Works**

The system first registers students by capturing multiple face images. These images are stored locally and used to train the LBPH model. Once training is complete, the webcam is activated for real-time recognition. When a face is detected and matched, the system automatically logs attendance in the database.


**Limitations**

Performance depends on lighting conditions
Accuracy decreases with low-quality training data
Not optimized for large-scale public surveillance
Requires consistent camera positioning for best results


**Future Improvements**

Web-based version using Flask or Django
Cloud database integration
Deep learning-based recognition model upgrade
Mobile attendance application
Real-time analytics dashboard for administrators



**Author**

This project was developed as an academic final-year computer vision system focused on automating attendance using facial recognition.


**License**

For academic and educational use only. Commercial use requires permission.
