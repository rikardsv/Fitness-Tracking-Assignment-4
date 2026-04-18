import sqlite3
import hashlib
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Join it with the filename to get an absolute path
DB_NAME = os.path.join(BASE_DIR, "fitness.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")


#Database helpers
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_tables():
    """Create tables by executing the DDL in schema.sql."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


# Default data
DEFAULT_PASSWORD = "password123"

DEFAULT_USERS = [
    # (Name, Email, Gender, CurrentWeight, Height, ActivityLevel)
    ("Per",    "per@gmail.com",    "Male",   70.0, 180.0, "Moderate"),
    ("Peter",  "peter@gmail.com",  "Male",   65.0, 176.0, "Low"),
    ("Anna",   "anna@gmail.com",   "Female", 60.0, 171.0, "High"),
    ("Anders", "anders@gmail.com", "Male",   80.0, 185.0, "High"),
    ("Maria",  "maria@gmail.com",  "Female", 58.0, 165.0, "Moderate"),
    ("Lars",   "lars@gmail.com",   "Male",   90.0, 182.0, "Low"),
    ("Ingrid", "ingrid@gmail.com", "Female", 65.0, 170.0, "High"),
    ("Ole",    "ole@gmail.com",    "Male",   75.0, 178.0, "Moderate"),
]


DEFAULT_METRICS = {
    "per@gmail.com":    [("Weight", 70.0), ("BMI", 21.6), ("Body Fat", 18.0),
                         ("Heart Rate", 68), ("Calories", 2400), ("Steps", 6000)],
    "peter@gmail.com":  [("Weight", 65.0), ("BMI", 21.0), ("Body Fat", 22.0),
                         ("Heart Rate", 74), ("Calories", 2100), ("Steps", 4000)],
    "anna@gmail.com":   [("Weight", 60.0), ("BMI", 20.5), ("Body Fat", 19.0),
                         ("Heart Rate", 62), ("Calories", 2300), ("Steps", 10000)],
    "anders@gmail.com": [("Weight", 80.0), ("BMI", 23.4), ("Body Fat", 15.0),
                         ("Heart Rate", 60), ("Calories", 2800), ("Steps", 15000)],
    "maria@gmail.com":  [("Weight", 58.0), ("BMI", 21.3), ("Body Fat", 24.0),
                         ("Heart Rate", 70), ("Calories", 2000), ("Steps", 7500)],
    "lars@gmail.com":   [("Weight", 90.0), ("BMI", 27.2), ("Body Fat", 28.0),
                         ("Heart Rate", 78), ("Calories", 2500), ("Steps", 3500)],
    "ingrid@gmail.com": [("Weight", 65.0), ("BMI", 22.5), ("Body Fat", 20.0),
                         ("Heart Rate", 64), ("Calories", 2200), ("Steps", 12000)],
    "ole@gmail.com":    [("Weight", 75.0), ("BMI", 23.7), ("Body Fat", 19.0),
                         ("Heart Rate", 66), ("Calories", 2450), ("Steps", 8000)],
}


def seed_default_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM User")
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            return  # Database already populated — do nothing.

        password_hash = hash_password(DEFAULT_PASSWORD)

        # Insert users and remember their generated IDs by email.
        email_to_id = {}
        for name, email, gender, weight, height, activity in DEFAULT_USERS:
            cursor.execute("""
                INSERT INTO User
                    (Name, PasswordHash, Email, Gender, CurrentWeight, Height, ActivityLevel)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, password_hash, email, gender, weight, height, activity))
            email_to_id[email] = cursor.lastrowid

        # Insert health metrics, linking to the correct UserID via email lookup.
        for email, metrics in DEFAULT_METRICS.items():
            user_id = email_to_id.get(email)
            if user_id is None:
                continue
            for metric_type, metric_value in metrics:
                cursor.execute("""
                    INSERT INTO HealthMetric (UserID, MetricType, MetricValue)
                    VALUES (?, ?, ?)
                """, (user_id, metric_type, metric_value))

        conn.commit()
    finally:
        conn.close()