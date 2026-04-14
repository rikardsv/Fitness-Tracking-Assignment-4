import sqlite3
import hashlib
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Join it with the filename to get an absolute path
DB_NAME = os.path.join(BASE_DIR, "fitness.db")


# -------------------------
# Database helpers
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        PasswordHash TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Gender TEXT,
        CurrentWeight REAL,
        Height REAL,
        ActivityLevel TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS HealthMetric (
        HealthMetricID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        MetricType TEXT NOT NULL,
        MetricValue REAL NOT NULL,
        FOREIGN KEY (UserID) REFERENCES User(UserID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """)

    conn.commit()
    conn.close()
