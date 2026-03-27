import psycopg2
import csv
from config import load_config
def connect():
    config = load_config()
    return psycopg2.connect(**config)
conn=connect()
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20)
);
""")
conn.commit()
def insert_console():
    first_name=input("First name: ")
    last_name=input("Last name: ")
    phone=input("Phone: ")
    cur.execute(
        "INSERT INTO phonebook(first_name, last_name, phone) VALUES (%s, %s, %s)",
        (first_name, last_name, phone)
    )
    conn.commit()
    print('Inserted')
def insert_csv(file):
    with open(file, 'r') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s,%s,%s)",
                row
            )
    conn.commit()
    print("CSV uploaded")
def update():
    name=input("Name to update: ")
    new_phone=input("New phone: ")
    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE first_name=%s",
        (new_phone, name)
    )
    conn.commit()
    print("Updated")
def query():
    print('1-ALL')
    print("2-By name")
    print("3-By phone pattern")
    c=input("Choose: ")
    if c=='1':
        cur.execute("SELECT * FROM phonebook")
    elif c=='2':
        name=input("Name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name=%s", (name,))
    elif c=="3":
        pattern=input("Pattern: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (pattern,))
    for row in cur.fetchall():
        print(row)

def delete():
    print("1-By name")
    print("2-By phone")
    c = input("Choose: ")
    if c == "1":
        name = input("Name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    elif c == "2":
        phone = input("Phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    print("Deleted")
while True:
    print("\nMENU")
    print("1 Insert console")
    print("2 Insert CSV")
    print("3 Update")
    print("4 Query")
    print("5 Delete")
    print("0 Exit")
    choice =input(">> ")
    if choice== "1":
        insert_console()
    elif choice == "2":
        insert_csv("phonebook.csv")
    elif choice=="3":
        update()
    elif choice=="4":
        query()
    elif choice== "5":
        delete()
    elif choice=="0":
        break
cur.close()
conn.close()