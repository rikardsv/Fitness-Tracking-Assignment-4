CREATE TABLE IF NOT EXISTS User (
    UserID         INTEGER PRIMARY KEY AUTOINCREMENT,
    Name           TEXT    NOT NULL,
    PasswordHash   TEXT    NOT NULL,
    Email          TEXT    NOT NULL UNIQUE,
    Gender         TEXT,
    CurrentWeight  REAL,
    Height         REAL,
    ActivityLevel  TEXT
);

CREATE TABLE IF NOT EXISTS HealthMetric (
    HealthMetricID  INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID          INTEGER NOT NULL,
    MetricType      TEXT    NOT NULL,
    MetricValue     REAL    NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);