import cv2
import sqlite3
from datetime import datetime

db = sqlite3.connect("attendance.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT,
    date TEXT,
    time TEXT
)
""")

camera = cv2.VideoCapture(0)

face = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        name = "Student"
        now = datetime.now()

        cursor.execute(
            "INSERT INTO attendance VALUES (?, ?, ?)",
            (name, now.date(), now.strftime("%H:%M:%S"))
        )
        db.commit()

        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
db.close()
