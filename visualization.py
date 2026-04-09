import pandas as pd
import streamlit as st
import plotly.express as px
import databaseHelpers as dh

# -------------------------
# Page function: Visualization
# -------------------------
def visualization_page():
    st.subheader("Health Metrics by Activity Level")

    metric_types = get_metric_types()

    if not metric_types:
        st.info("No health metric data available yet.")
        return

    selected_metric = st.selectbox("Choose a health metric", metric_types)
    df = fetch_metric_by_activity_level(selected_metric)

    if df.empty:
        st.info("No visualization data found for the selected metric.")
        return

    fig = px.bar(
        df,
        x="ActivityLevel",
        y="AvgMetricValue",
        text="AvgMetricValue",
        hover_data=["UserCount"],
        title=f"Average latest {selected_metric} by activity level"
    )

    st.plotly_chart(fig, use_container_width=True)

    highest = df.iloc[0]
    lowest = df.iloc[-1]

    st.caption(
        f"This chart shows the average latest recorded {selected_metric.lower()} "
        f"for users grouped by activity level. The highest average value is in "
        f"'{highest['ActivityLevel']}' with {highest['AvgMetricValue']}, while the "
        f"lowest is in '{lowest['ActivityLevel']}' with {lowest['AvgMetricValue']}. "
        f"The result is based on the latest measurement per user for the selected metric."
    )

    st.markdown("**Underlying SQL logic:** JOIN + subquery + aggregation")
    st.code("""
SELECT
    u.ActivityLevel,
    hm.MetricType,
    ROUND(AVG(hm.MetricValue), 2) AS AvgMetricValue,
    COUNT(*) AS UserCount
FROM User u
JOIN HealthMetric hm
    ON u.UserID = hm.UserID
JOIN (
    SELECT UserID, MetricType, MAX(HealthMetricID) AS LatestMetricID
    FROM HealthMetric
    GROUP BY UserID, MetricType
) latest
    ON hm.HealthMetricID = latest.LatestMetricID
WHERE hm.MetricType = ?
  AND u.ActivityLevel IS NOT NULL
  AND TRIM(u.ActivityLevel) <> ''
GROUP BY u.ActivityLevel, hm.MetricType
ORDER BY AvgMetricValue DESC
""", language="sql")


# -------------------------
# Visualization queries
# -------------------------
def get_metric_types():
    conn = dh.get_connection()
    df = pd.read_sql_query("""
        SELECT DISTINCT MetricType
        FROM HealthMetric
        WHERE MetricType IS NOT NULL AND TRIM(MetricType) <> ''
        ORDER BY MetricType
    """, conn)
    conn.close()
    return df["MetricType"].tolist()


def fetch_metric_by_activity_level(metric_type):
    conn = dh.get_connection()
    query = """
    SELECT
        u.ActivityLevel,
        hm.MetricType,
        ROUND(AVG(hm.MetricValue), 2) AS AvgMetricValue,
        COUNT(*) AS UserCount
    FROM User u
    JOIN HealthMetric hm
        ON u.UserID = hm.UserID
    JOIN (
        SELECT UserID, MetricType, MAX(HealthMetricID) AS LatestMetricID
        FROM HealthMetric
        GROUP BY UserID, MetricType
    ) latest
        ON hm.HealthMetricID = latest.LatestMetricID
    WHERE hm.MetricType = ?
      AND u.ActivityLevel IS NOT NULL
      AND TRIM(u.ActivityLevel) <> ''
    GROUP BY u.ActivityLevel, hm.MetricType
    ORDER BY AvgMetricValue DESC
    """
    df = pd.read_sql_query(query, conn, params=(metric_type,))
    conn.close()
    return df

