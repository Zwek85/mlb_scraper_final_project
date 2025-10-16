import sqlite3
import pandas as pd

DB_FILE = 'mlb_history.db'  # Your SQLite database file

def run_query():
    conn = sqlite3.connect(DB_FILE)
    print(f"Connected to database: {DB_FILE}\n")
    print("Enter your SQL query below. Type 'exit' or 'quit' to leave.\n")

    while True:
        query = input("SQL> ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Exiting...")
            break
        if not query:
            continue

        try:
            df = pd.read_sql_query(query, conn)
            if df.empty:
                print("No results found.\n")
            else:
                print(df.to_string(index=False))
                print(f"\nRows returned: {len(df)}\n")

        except Exception as e:
            print(f"❌ Error: {e}\n")

    conn.close()

if __name__ == "__main__":
    run_query()
