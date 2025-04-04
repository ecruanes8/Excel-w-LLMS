from csv_to_sqlite import CSVtoSQLite
from llm_implementation import build_llm_prompt, ask_llm

def main(): 
    db = CSVtoSQLite("default.db")
    print("📊 Welcome to Excel AI but the better version!")
    print("Type 'help' to see available commands.\n")


    try:
        while True: 
            command = input(">> ").strip().lower()
            if command == "help":
                print(""" 
                    Available Commands: 
                    - load: load a CSV file and create a table in SQL
                    - ask: ask in plain english, ai generates SQL 
                    - tables: List all tables in database 
                    - query: Run SQL query
                    - exit: Exit the assistant
                    - switch: switch databases
                """)

            elif command == "ask":
                if db is None:
                    print("Load a database first using the [load] or [switch] command.")
                    continue
                try: 
                    print("Available tables:")
                    tables = db.query("SELECT name FROM sqlite_master WHERE type='table';")['name']
                    for t in tables:
                        print(f" - {t}")
                    table = input("Which table do you want to query? ").strip()
                    schema = db.get_existing_schema(table)
                    user_request = input("Ask your question:\n>>> ")
                    prompt = build_llm_prompt(user_request, schema)
                    sql = ask_llm(prompt)
                except Exception as e:
                    print("❌ Error generating or running SQL. Check error_log.txt.")
                    import logging
                    logging.error("LLM Ask Error", exc_info=True)

            elif command== "load": 
                csv_path = input("Enter CSV file path: ").strip()
                table_name = input("Enter table name: ").strip() 
                
                try: 
                    db.load_csv(csv_path)
                    if db.table_exists(table_name): 
                        table_name = db.handle_conflict(table_name)
                    if table_name: 
                        db.infer_and_create_table(table_name)
                        db.insert_to_sql(table_name) 
                except Exception as e: 
                    print("Error loading CSV. See error_log.txt")
                    import logging
                    logging.error("CSV Load Error",exc_info=True)
            elif command == "switch":
                db_path = input("Enter path to SQLite DB file: ").strip()

                # Close current connection if any
                if db:
                    db.close()

                # Reconnect to the new database
                db = CSVtoSQLite(db_path)
                print(f"Switched to database: {db_path}")
            
            elif command== "tables": 
                try: 
                    result = db.query("SELECT name FROM sqlite_master WHERE type = 'table';")
                    print("Tables: ")
                    for name in result ['name']: 
                        print(f" -{name}")
                except Exception as e: 
                    print("Error in listing all tables")

            elif command == "query":
                    sql = input("Enter SQL query:\n>>> ")
                    try:
                        result = db.query(sql)
                        print(result)
                    except Exception as e:
                        print("❌ Query failed. See error_log.txt.")
                        import logging
                        logging.error("Query Error", exc_info=True)

            elif command == "exit":
                print("👋 Goodbye!")
                break

            else:
                print("⚠️ Unknown command. Type 'help' to see options.")

    finally:
        db.close()

if __name__ == "__main__":
    main()