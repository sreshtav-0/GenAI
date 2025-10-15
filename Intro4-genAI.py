# SQLIte3 
# CRUD-> Create Read Update Delete
import sqlite3

# Create a database and the Table
def create_table():
    connection = sqlite3.connect("myDatabase.db") 

    cursor = connection.cursor() 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  
    age INTEGER NOT NULL,   
    email TEXT UNIQUE NOT NULL                
    )
""")
    connection.commit()
    connection.close()
    print("Database and Table successfully created")

# Inserting the Data 
def insert_data(name, age, email):
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
INSERT INTO users (name, age, email) 
VALUES (?, ?, ?)
""", (name, age, email))
        connection.commit() 
        print("Data inserted successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    create_table()
    #insert_data("Morty Sanchez", 13, "sci_fiventures@gmail.com")