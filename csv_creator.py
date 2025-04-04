# csv_creator.py
import pandas as pd
#example csv 
def create_csv():
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [20, 21, 22],
        "grade": ["A", "B", "A"]
    }
    df = pd.DataFrame(data)
    df.to_csv("students.csv", index=False)
    print("students.csv created.")
