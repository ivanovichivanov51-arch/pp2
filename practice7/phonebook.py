import psycopg2
import csv
from connect import connect

# 1. Кесте құру функциясы
def create_table():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Кесте дайын.")

# 2. Қолмен жаңа контакт қосу
def insert_contact(name, phone):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print(f"Сәтті қосылды: {name}")
        cursor.close()
        conn.close()

# 3. CSV файлдан автоматты түрде жүктеу (Тапсырма 3.2.2)
def insert_from_csv(file_path):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # row[0] - аты, row[1] - телефоны
                    cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))
            conn.commit()
            print("CSV-ден мәліметтер жүктелді!")
        except Exception as e:
            print(f"Файл оқуда қате: {e}")
        finally:
            cursor.close()
            conn.close()

# 4. Нөмірді өзгерту (Update)
def update_contact(name, new_phone):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET phone = %s WHERE name = %s", (new_phone, name))
        conn.commit()
        print(f"{name} нөмірі жаңартылды.")
        cursor.close()
        conn.close()

# 5. Контактіні өшіру (Delete)
def delete_contact(name):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE name = %s", (name,))
        conn.commit()
        print(f"{name} базадан өшірілді.")
        cursor.close()
        conn.close()

# --- НЕГІЗГІ МӘЗІР ---
if __name__ == '__main__':
    create_table() # Бағдарлама іске қосылғанда кестені тексереді
    
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Жаңа контакт қосу")
        print("2. CSV файлдан жүктеу")
        print("3. Нөмірді өзгерту")
        print("4. Контактіні өшіру")
        print("0. Шығу")
        
        choice = input("\nТаңдаңыз: ")
        
        if choice == '1':
            name = input("Аты: ")
            phone = input("Телефон: ")
            insert_contact(name, phone)
        elif choice == '2':
            insert_from_csv('contacts.csv')
        elif choice == '3':
            name = input("Кімнің нөмірін өзгертеміз?: ")
            new_phone = input("Жаңа нөмір: ")
            update_contact(name, new_phone)
        elif choice == '4':
            name = input("Кімді өшіреміз?: ")
            delete_contact(name)
        elif choice == '0':
            print("Сау болыңыз!")
            break
        else:
            print("Қате таңдау!")