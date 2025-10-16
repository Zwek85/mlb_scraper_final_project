import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

DB_FILE = 'mlb_history.db'

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM mlb_world_series_history", conn)
    conn.close()
    return df

def main():
    st.title("⚾ MLB World Series History Dashboard")

    df = load_data()

    # Ensure Year column exists and is numeric
    if 'Year' not in df.columns:
        st.error("Year column missing! Please check your data import.")
        return
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])

    # Sidebar filters
    st.sidebar.header("Filters")

    years = sorted(df['Year'].unique())
    year_range = st.sidebar.slider("Select Year Range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

    teams = sorted(set(df['Winner'].unique()) | set(df['Loser'].unique()))
    selected_team = st.sidebar.selectbox("Select Team (Winner or Loser)", ["All"] + teams)

    # Filter data by year range
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    if selected_team != "All":
        filtered_df = filtered_df[(filtered_df['Winner'] == selected_team) | (filtered_df['Loser'] == selected_team)]

    st.write(f"### Showing {len(filtered_df)} World Series entries between {year_range[0]} and {year_range[1]}")

    # Visualization 1: Count of World Series Wins by Team
    wins = filtered_df['Winner'].value_counts().reset_index()
    wins.columns = ['Team', 'Wins']

    chart1 = alt.Chart(wins).mark_bar().encode(
        x=alt.X('Wins:Q', title='Number of Wins'),
        y=alt.Y('Team:N', sort='-x', title='Team'),
        tooltip=['Team', 'Wins']
    ).properties(
        title='World Series Wins by Team'
    )
    st.altair_chart(chart1, use_container_width=True)

    # Visualization 2: Timeline of World Series Results
    timeline = filtered_df[['Year', 'Winner', 'Loser', 'Result']].sort_values('Year')

    timeline_chart = alt.Chart(timeline).mark_circle(size=100).encode(
        x='Year:O',
        y=alt.Y('Winner:N', title='Winner Team'),
        color='Loser:N',
        tooltip=['Year', 'Winner', 'Loser', 'Result']
    ).properties(
        title='World Series Winners and Losers Over the Years'
    )
    st.altair_chart(timeline_chart, use_container_width=True)

    # Visualization 3: Win/Loss Pie Chart for Selected Team
    if selected_team != "All":
        wins_count = len(filtered_df[filtered_df['Winner'] == selected_team])
        losses_count = len(filtered_df[filtered_df['Loser'] == selected_team])
        pie_data = pd.DataFrame({
            'Outcome': ['Wins', 'Losses'],
            'Count': [wins_count, losses_count]
        })
        pie_chart = alt.Chart(pie_data).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Outcome", type="nominal"),
            tooltip=['Outcome', 'Count']
        ).properties(
            title=f"Win/Loss Distribution for {selected_team}"
        )
        st.altair_chart(pie_chart, use_container_width=True)

if __name__ == "__main__":
    main()
