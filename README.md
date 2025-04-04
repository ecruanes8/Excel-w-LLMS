The purpose of this project is to create an Excel AI assistant by implementing an LLM and setting up databases by uploading CSV files to SQL. 

Modulation of Excel w/ LLMS: 
  excel_ai_assistant/               ← Your project folder
   - main.py                      ← CLI entry point
   - csv_creator.py               ← CSV creator for examples
   - csv_to_sqlite.py             ← CSV-to-SQLite class (DB logic)
   - llm_implementation.py        ← LLM prompt building and API call
   - students.csv                 ← Example CS
   - error_log.txt                ← Logged errors


To run the program: 
  python main.py

This will then prompt you to either enter 'help' for commands available then you can: 
  --> load csv files
  --> switch databases
  --> list all available tables
  --> ask using an LLM
  --> make a SQL query
  --> exit the program. 
