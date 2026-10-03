"""Flag students who may need a mentor.

Rule used in this project:
- attendance below 75, or
- average of subject marks below 40.
"""

import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "students.csv"
ATTENDANCE_LIMIT = 75
AVERAGE_LIMIT = 40


def load_students(path=DATA_PATH):
    students = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            marks = [float(row["math"]), float(row["physics"]), float(row["python"])]
            average = sum(marks) / len(marks)
            attendance = float(row["attendance"])
            reasons = []
            if attendance < ATTENDANCE_LIMIT:
                reasons.append(f"attendance {attendance:.0f}% is below {ATTENDANCE_LIMIT}%")
            if average < AVERAGE_LIMIT:
                reasons.append(f"average {average:.1f} is below {AVERAGE_LIMIT}")
            students.append(
                {
                    "name": row["name"],
                    "attendance": attendance,
                    "math": marks[0],
                    "physics": marks[1],
                    "python": marks[2],
                    "average": round(average, 1),
                    "at_risk": bool(reasons),
                    "reasons": reasons,
                }
            )
    return students


def summary(students):
    total = len(students)
    at_risk = sum(1 for student in students if student["at_risk"])
    class_average = sum(student["average"] for student in students) / total if total else 0
    return {
        "total": total,
        "at_risk": at_risk,
        "safe": total - at_risk,
        "class_average": round(class_average, 1),
    }
