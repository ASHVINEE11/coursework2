import pandas as pd
import os
from sqlalchemy import create_engine

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """

    # TODO: Check if CSV file exists
    if os.path.exists(csv_path):
        print(f"The file {csv_path} exists.")
    else:
        print(f"The file {csv_path} does not exists.")
        return 0

    # TODO: Read CSV using pandas.read_csv()
    df = pd.read_csv(csv_path)
    print (df.head())
    
    # TODO: Use df.to_sql() to insert data
    df.to_sql(
        name=table_name, 
        con=conn, 
        if_exists='replace', 
        index=False
    )
  # Parameters: name=table_name, con=conn, if_exists='append', index=False

    # TODO: Print success message and return row count
    print(f"{len(df)} row was loaded into '{table_name}' successfully!")
    return len(df)




if __name__ == "__main__":
    # Base folder
    base_folder = r"C:\Users\ashvi\OneDrive - Middlesex University\Desktop\CW2 CST1510\CW2_M01070954_CST1510\DATA"

    # Database file
    db_file = "intelligence_platform.db"
    db_path = os.path.join(base_folder, db_file)

    # Create database connection
    conn = create_engine(f"sqlite:///{db_path}")

    # Load Cyber Incidents 
    cyber_csv = os.path.join(base_folder, "cyber_incidents_csv.csv")
    load_csv_to_table(conn, cyber_csv, "cyber_incidents")

    # Load IT Ticketss
    tickets_csv = os.path.join(base_folder, "it_tickets(1).csv")
    load_csv_to_table(conn, tickets_csv, "it_tickets")
