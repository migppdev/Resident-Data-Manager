import sqlite3 as sql
import pandas as pd


conn = sql.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Residents(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        age INTEGER,
        registration_date TEXT
    )
""")

def add_resident_db(full_name, age, registration_date):
    cursor.execute("INSERT INTO Residents VALUES (null, ?, ?, ?)", (full_name, age, registration_date,))
    conn.commit()

def search_resident_db(query):
    cursor.execute("SELECT full_name FROM Residents WHERE full_name LIKE ?", (f'%{query}%',))
    results = cursor.fetchall()
    return results

def get_residents():
    cursor.execute("SELECT full_name FROM Residents")
    results = cursor.fetchall()
    return results

def delete_resident(full_name):
    cursor.execute("DELETE FROM Residents WHERE full_name = ?", (full_name,))
    conn.commit()

def get_data(full_name):
    cursor.execute("SELECT * FROM Residents WHERE full_name = ?", (full_name,))
    data = cursor.fetchall()
    return data[0]

def update_data_db(new_full_name, new_age, new_date, old_full_name):
    cursor.execute("UPDATE Residents SET full_name = ?, age = ?, registration_date = ? WHERE full_name = ?", (new_full_name, new_age, new_date, old_full_name))
    conn.commit()

def import_excel_db(file_path):
    # Read the Excel file and store the data in a DataFrame
    df = pd.read_excel(file_path)

    # Ignore first rows
    df = df.iloc[0:]

    # Iterate over the DataFrame rows and execute the INSERT queries
    for row in df.itertuples(index=False):
        cursor.execute('INSERT INTO Residents VALUES (null, ?, ?, ?)', row)


def export_excel_db(file_path):
    cursor.execute("SELECT full_name, age, registration_date FROM Residents")
    results = cursor.fetchall()
    
    # Create a DataFrame with the query results
    df = pd.DataFrame(results, columns=['Name', 'Age', 'Registration Date'])
    
    # Export the DataFrame to an Excel file
    df.to_excel(file_path, index=False)
    
    
def delete_all_db():
    cursor.execute("DELETE FROM Residents;")
    conn.commit()

def close_db():
    conn.close()