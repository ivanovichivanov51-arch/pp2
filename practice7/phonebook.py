import psycopg2
from connect import connect

def create_table():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(20)
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()

def insert_contact(name, phone):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print(f"{name} қосылды!")
        cursor.close()
        conn.close()
