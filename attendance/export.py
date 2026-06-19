import pandas as pd
from database.db import connect


def export_attendance():
    conn = connect()

    query = """
    SELECT s.full_name, s.matric_no, a.timestamp, a.status
    FROM attendance a
    JOIN students s ON a.student_id = s.id
    """

    df = pd.read_sql_query(query, conn)

    file_name = "attendance_report.xlsx"
    df.to_excel(file_name, index=False)

    conn.close()

    print(f"Attendance exported to {file_name}")