import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS idx_attendance_unique 
ON attendance(student_id, session_id)
""")

conn.commit()
conn.close()

print("DB fixed successfully")