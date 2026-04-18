import sqlite3
import pandas as pd
import streamlit as st
import tableQueries as tq


# Page functions: User
def read_users_page():
    st.subheader("All Users")
    df = tq.fetch_users()

    if df.empty:
        st.info("No users found.")
        return

    display_df = df.drop(columns=["PasswordHash"])
    st.dataframe(display_df, use_container_width=True)


def create_user_page():
    st.subheader("Create User")

    with st.form("create_user_form", clear_on_submit=True):
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
        current_weight = st.number_input("Current Weight (kg)", min_value=0.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=0.0, step=0.1)
        activity_level = st.selectbox("Activity Level", ["", "Low", "Moderate", "High"])

        submitted = st.form_submit_button("Add User")

        if submitted:
            if not name.strip() or not password.strip() or not email.strip():
                st.error("Name, password and email are required.")
                return

            try:
                tq.insert_user(
                    name=name.strip(),
                    password=password,
                    email=email.strip(),
                    gender=gender if gender else None,
                    current_weight=current_weight if current_weight > 0 else None,
                    height=height if height > 0 else None,
                    activity_level=activity_level if activity_level else None
                )
                st.success("User added successfully.")
            except sqlite3.IntegrityError:
                st.error("That email already exists. Please use another email.")


def update_user_page():
    st.subheader("Update User")
    users = tq.fetch_users()

    if users.empty:
        st.info("No users found.")
        return

    user_options = {
        f"{row['UserID']} - {row['Name']}": row["UserID"]
        for _, row in users.iterrows()
    }

    selected_label = st.selectbox("Choose user", list(user_options.keys()))
    selected_user_id = user_options[selected_label]
    selected_user = users[users["UserID"] == selected_user_id].iloc[0]

    gender_options = ["", "Male", "Female", "Other"]
    activity_options = ["", "Low", "Moderate", "High"]

    current_gender = selected_user["Gender"] if pd.notna(selected_user["Gender"]) else ""
    current_activity = selected_user["ActivityLevel"] if pd.notna(selected_user["ActivityLevel"]) else ""

    with st.form("update_user_form"):
        name = st.text_input("Name", value=selected_user["Name"])
        email = st.text_input("Email", value=selected_user["Email"])
        new_password = st.text_input("New Password (leave blank to keep current)", type="password")
        gender = st.selectbox(
            "Gender",
            gender_options,
            index=gender_options.index(current_gender) if current_gender in gender_options else 0
        )
        current_weight = st.number_input(
            "Current Weight (kg)",
            min_value=0.0,
            value=float(selected_user["CurrentWeight"]) if pd.notna(selected_user["CurrentWeight"]) else 0.0,
            step=0.1
        )
        height = st.number_input(
            "Height (cm)",
            min_value=0.0,
            value=float(selected_user["Height"]) if pd.notna(selected_user["Height"]) else 0.0,
            step=0.1
        )
        activity_level = st.selectbox(
            "Activity Level",
            activity_options,
            index=activity_options.index(current_activity) if current_activity in activity_options else 0
        )

        submitted = st.form_submit_button("Update User")

        if submitted:
            if not name.strip() or not email.strip():
                st.error("Name and email are required.")
                return

            try:
                tq.update_user(
                    user_id=selected_user_id,
                    name=name.strip(),
                    email=email.strip(),
                    gender=gender if gender else None,
                    current_weight=current_weight if current_weight > 0 else None,
                    height=height if height > 0 else None,
                    activity_level=activity_level if activity_level else None,
                    new_password=new_password.strip() if new_password.strip() else None
                )
                st.success("User updated successfully.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("That email already exists. Please use another email.")


def delete_user_page():
    st.subheader("Delete User")
    users = tq.fetch_users()

    if users.empty:
        st.info("No users found.")
        return

    user_options = {
        f"{row['UserID']} - {row['Name']}": row["UserID"]
        for _, row in users.iterrows()
    }

    selected_label = st.selectbox("Choose user to delete", list(user_options.keys()))
    selected_user_id = user_options[selected_label]

    st.warning("Deleting a user will also delete related health metrics because of ON DELETE CASCADE.")

    if st.button("Delete User"):
        tq.delete_user(selected_user_id)
        st.success("User deleted successfully.")
        st.rerun()


# Page functions: HealthMetric
def read_health_metrics_page():
    st.subheader("All Health Metrics")
    df = tq.fetch_health_metrics()

    if df.empty:
        st.info("No health metrics found.")
        return

    st.dataframe(df, use_container_width=True)


def create_health_metric_page():
    st.subheader("Create Health Metric")
    users = tq.fetch_users()

    if users.empty:
        st.warning("You must create a user first.")
        return

    user_options = {
        f"{row['UserID']} - {row['Name']}": row["UserID"]
        for _, row in users.iterrows()
    }

    metric_types = ["Weight", "BMI", "Body Fat", "Heart Rate", "Calories", "Steps"]

    with st.form("create_health_metric_form", clear_on_submit=True):
        selected_label = st.selectbox("User", list(user_options.keys()))
        user_id = user_options[selected_label]
        metric_type = st.selectbox("Metric Type", metric_types)
        metric_value = st.number_input("Metric Value", step=0.1)

        submitted = st.form_submit_button("Add Health Metric")

        if submitted:
            tq.insert_health_metric(user_id, metric_type, metric_value)
            st.success("Health metric added successfully.")


def update_health_metric_page():
    st.subheader("Update Health Metric")
    metrics = tq.fetch_health_metrics()
    users = tq.fetch_users()

    if metrics.empty:
        st.info("No health metrics found.")
        return

    user_options = {
        f"{row['UserID']} - {row['Name']}": row["UserID"]
        for _, row in users.iterrows()
    }
    user_id_to_label = {v: k for k, v in user_options.items()}

    metric_types = ["Weight", "BMI", "Body Fat", "Heart Rate", "Calories", "Steps"]

    metric_options = {
        f"{row['HealthMetricID']} - {row['Name']} - {row['MetricType']} ({row['MetricValue']})": row["HealthMetricID"]
        for _, row in metrics.iterrows()
    }

    selected_metric_label = st.selectbox("Choose metric", list(metric_options.keys()))
    selected_metric_id = metric_options[selected_metric_label]
    selected_metric = metrics[metrics["HealthMetricID"] == selected_metric_id].iloc[0]

    with st.form("update_health_metric_form"):
        selected_user_label = st.selectbox(
            "User",
            list(user_options.keys()),
            index=list(user_options.keys()).index(user_id_to_label[selected_metric["UserID"]])
        )
        user_id = user_options[selected_user_label]

        metric_type = st.selectbox(
            "Metric Type",
            metric_types,
            index=metric_types.index(selected_metric["MetricType"]) if selected_metric["MetricType"] in metric_types else 0
        )

        metric_value = st.number_input(
            "Metric Value",
            value=float(selected_metric["MetricValue"]),
            step=0.1
        )

        submitted = st.form_submit_button("Update Health Metric")

        if submitted:
            tq.update_health_metric(selected_metric_id, user_id, metric_type, metric_value)
            st.success("Health metric updated successfully.")
            st.rerun()


def delete_health_metric_page():
    st.subheader("Delete Health Metric")
    metrics = tq.fetch_health_metrics()

    if metrics.empty:
        st.info("No health metrics found.")
        return

    metric_options = {
        f"{row['HealthMetricID']} - {row['Name']} - {row['MetricType']} ({row['MetricValue']})": row["HealthMetricID"]
        for _, row in metrics.iterrows()
    }

    selected_metric_label = st.selectbox("Choose metric to delete", list(metric_options.keys()))
    selected_metric_id = metric_options[selected_metric_label]

    if st.button("Delete Health Metric"):
        tq.delete_health_metric(selected_metric_id)
        st.success("Health metric deleted successfully.")
        st.rerun()
