# Fitness Tracking App
A group project for IDATG2002 – Databases. A fitness tracking web application built with Streamlit, using SQLite as the database and Plotly for data visualization.

## Group Members
- Andreas Danielsen Fageraas
- Johannes Nupen Theigen
- Erik Thoreplass
- Rikard Svalbjørg

## About the Project
The app implements CRUD operations for Users and Health Metrics, and includes a visualization showing average health metric values grouped by activity level.

## How to Run
1. Clone the repository:
```bash
   git clone https://github.com/rikardsv/Fitness-Tracking-Assignment-4.git
   cd Fitness-Tracking-Assignment-4
```
2. Install dependencies:
```bash
   pip install streamlit plotly pandas
```
3. Run the app:
```bash
   streamlit run main.py
```

## Project Structure

```
│   .gitignore
│   databaseHelpers.py
│   fitness.db
│   main.py
│   pageFunctions.py
│   README.md
│   tableQueries.py
│   visualization.py
│
```