import pandas as pd
import databaseHelpers as dh


def fetch_users():
    conn = dh.get_connection()
    df = pd.read_sql_query("SELECT * FROM User ORDER BY UserID", conn)
    conn.close()
    return df


def insert_user(name, password, email, gender, current_weight, height, activity_level):
    conn = dh.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO User (Name, PasswordHash, Email, Gender, CurrentWeight, Height, ActivityLevel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        dh.hash_password(password),
        email,
        gender,
        current_weight,
        height,
        activity_level
    ))
    conn.commit()
    conn.close()


def update_user(user_id, name, email, gender, current_weight, height, activity_level, new_password=None):
    conn = dh.get_connection()
    cursor = conn.cursor()

    if new_password:
        cursor.execute("""
            UPDATE User
            SET Name = ?, Email = ?, Gender = ?, CurrentWeight = ?, Height = ?, ActivityLevel = ?, PasswordHash = ?
            WHERE UserID = ?
        """, (
            name,
            email,
            gender,
            current_weight,
            height,
            activity_level,
            dh.hash_password(new_password),
            user_id
        ))
    else:
        cursor.execute("""
            UPDATE User
            SET Name = ?, Email = ?, Gender = ?, CurrentWeight = ?, Height = ?, ActivityLevel = ?
            WHERE UserID = ?
        """, (
            name,
            email,
            gender,
            current_weight,
            height,
            activity_level,
            user_id
        ))

    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = dh.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE UserID = ?", (user_id,))
    conn.commit()
    conn.close()

def fetch_health_metrics():
    conn = dh.get_connection()
    query = """
    SELECT
        hm.HealthMetricID,
        hm.UserID,
        u.Name,
        u.ActivityLevel,
        hm.MetricType,
        hm.MetricValue
    FROM HealthMetric hm
    JOIN User u ON hm.UserID = u.UserID
    ORDER BY hm.HealthMetricID
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def insert_health_metric(user_id, metric_type, metric_value):
    conn = dh.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO HealthMetric (UserID, MetricType, MetricValue)
        VALUES (?, ?, ?)
    """, (user_id, metric_type, metric_value))
    conn.commit()
    conn.close()


def update_health_metric(metric_id, user_id, metric_type, metric_value):
    conn = dh.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE HealthMetric
        SET UserID = ?, MetricType = ?, MetricValue = ?
        WHERE HealthMetricID = ?
    """, (user_id, metric_type, metric_value, metric_id))
    conn.commit()
    conn.close()

def delete_health_metric(metric_id):
    conn = dh.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM HealthMetric WHERE HealthMetricID = ?", (metric_id,))
    conn.commit()
    conn.close()

