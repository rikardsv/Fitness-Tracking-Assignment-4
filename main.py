import streamlit as st
import pageFunctions as pf
import databaseHelpers as dh
import visualization as v

DB_NAME = "fitness.db"

# Main app
def main():
    st.set_page_config(page_title="Fitness App", layout="wide")
    dh.create_tables()
    dh.seed_default_data()

    st.title("Fitness Tracker App")
    st.write("CRUD for User and HealthMetric, plus a Plotly visualization.")

    section = st.sidebar.radio(
        "Choose section",
        ["Users", "Health Metrics", "Visualization"]
    )

    if section == "Users":
        pages = {
            "Read Users": pf.read_users_page,
            "Create User": pf.create_user_page,
            "Update User": pf.update_user_page,
            "Delete User": pf.delete_user_page,
        }
    elif section == "Health Metrics":
        pages = {
            "Read Health Metrics": pf.read_health_metrics_page,
            "Create Health Metric": pf.create_health_metric_page,
            "Update Health Metric": pf.update_health_metric_page,
            "Delete Health Metric": pf.delete_health_metric_page,
        }
    else:
        pages = {
            "Show Visualization": v.visualization_page
        }

    selected_page = st.sidebar.selectbox("Choose action", list(pages.keys()))
    pages[selected_page]()


if __name__ == "__main__":
    main()