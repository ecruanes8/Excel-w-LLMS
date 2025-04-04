import pandas as pd
import sqlite3
import logging

logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

class CSVtoSQLite:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.df = None
    
    #function to load csv, input is csv path 
    def load_csv(self, csv_path):
        self.df = pd.read_csv(csv_path)
        print(f"Loaded CSV: {csv_path}")
        return self.df
    
    #converting pandas type to sql type 
    def map_dtype_to_sql(self, dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            return "REAL"
        elif pd.api.types.is_bool_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return "TEXT"
        else:
            return "TEXT"
    
    #gets column names and creates table with columns if doesn't already exist 
    def infer_and_create_table(self, table_name):
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        columns = [
            f'"{col}" {self.map_dtype_to_sql(dtype)}'
            for col, dtype in self.df.dtypes.items()
        ]
        create_stmt = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(columns)});'
        self.cursor.execute(create_stmt)
        self.conn.commit()
        print(f"Table '{table_name}' created with inferred schema.")
    
    #to_sql function to insert into database table 
    def insert_to_sql(self, table_name, if_exists='append'):
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        try:
            self.df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
            print(f"Data inserted into '{table_name}'.")
        except Exception as e:
            logging.error(f"Failed to insert into table '{table_name}'", exc_info=True)
            print(f"❌ Error inserting into table '{table_name}'. Logged to error_log.txt")
    
    #check is table exists
    def table_exists(self, table_name):
        self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        return self.cursor.fetchone() is not None
    
    #returns structure of table (each row)
    def get_existing_schema(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        schema = self.cursor.fetchall()

        schema_prompt = f"Table {table_name}:\n"
        for col in schema:
            schema_prompt += f"  - {col[1]} ({col[2]})\n"

        return schema_prompt.strip()

        
    #if table already exists, gives option to user to overwrite, rename or skip 
    def handle_conflict(self, table_name):
        print(f"\n⚠️ Table '{table_name}' already exists.")
        schema = self.get_existing_schema(table_name)
        print("Existing schema:")
        for col in schema:
            print(f" - {col[1]} ({col[2]})")

        print("\nOptions: [O]verwrite  [R]ename  [S]kip")
        choice = input("Choose an option: ").strip().upper()

        if choice == "O":
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
            print(f"Table '{table_name}' overwritten.")
            return table_name

        elif choice == "R":
            new_name = input("Enter new table name: ").strip()
            print(f"Using table name: '{new_name}'")
            return new_name

        elif choice == "S":
            print("Skipping import.")
            return None

        else:
            print("Invalid option. Skipping.")
            return None
    
    #to query into existing table 
    def query(self, sql_query):
        return pd.read_sql(sql_query, self.conn)
    
    #to close connection
    def close(self):
        self.conn.close()
