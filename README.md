# MLB World Series Dashboard

An interactive Streamlit app to explore MLB World Series winners. 
The dashboard include 3 visualizations: 
Visualization 1: Count of World Series Wins by Team
Visualization 2: Timeline of World Series Results
Visualization 3: Win/Loss Pie Chart for Selected Team

## Features

- Interactive year filter (dropdown)
- Data visualization using Altair
- Data cleaning and import using Pandas & SQLite
- Fully reproducible environment

dashboard screeshot: 
<img width="1399" height="893" alt="Screenshot 2025-10-15 at 10 10 54 PM" src="https://github.com/user-attachments/assets/69d11c37-efc9-48cc-ae4f-a2a07c5019b7" />

## Setup Instructions

1. Clone the repo
3. Install dependencies:
   -pip install -r requirements.txt
4.Import data
-make sure that mlb_world_series_history.csv is created in the project folder and run:
python3 import_csv.py
This will create mlb_history.db with a table named mlb_world_series_history

5. Run the streamlit app:
streamlit run app.py
The app will launch in your browser at http://localhost:8506.
