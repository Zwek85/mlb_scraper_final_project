import os
import sqlite3
import pandas as pd

# Folder where your CSV files are stored
DATA_FOLDER = './'

# Name of the SQLite database
DB_FILE = 'mlb_history.db'


def infer_and_convert_dtypes(df):
    """Convert columns to appropriate data types if possible."""
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass  # Leave as string if conversion fails
    return df


def import_csv_to_sqlite(db_file, csv_file, table_name):
    print(f"\n📥 Importing: {csv_file} as table `{table_name}`")
    try:
        # 🔧 Force correct column names regardless of CSV header content
        df = pd.read_csv(
            csv_file,
            header=None,
            names=["Year", "Winner", "Loser", "Result"]
        )

        print(f"🔎 Columns detected: {list(df.columns)}")
        print(f"📊 Original shape: {df.shape}")

        # Drop duplicate rows
        df = df.drop_duplicates()

        # Drop rows that are entirely empty
        df = df.dropna(how='all')

        # Convert to correct dtypes
        df = infer_and_convert_dtypes(df)

        print(f"Cleaned shape: {df.shape}")

        # Write to SQLite database
        with sqlite3.connect(db_file) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"Successfully imported `{table_name}`")

    except pd.errors.EmptyDataError:
        print(f"Skipping {csv_file}: File is empty.")
    except Exception as e:
        print(f"Error importing {csv_file}: {e}")


def main():
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found to import.")
        return

    # Import each CSV as a table
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        csv_path = os.path.join(DATA_FOLDER, csv_file)
        import_csv_to_sqlite(DB_FILE, csv_path, table_name)

    print("\nAll valid CSVs imported successfully!")


if __name__ == '__main__':
    main()
