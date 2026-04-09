import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="sekow102", 
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )

    cursor = connection.cursor()

    # 1. Кесте құру
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            age INT
        );
    ''')

    # 2. МӘЛІМЕТ ҚОСУ (INSERT)
    # Өзіңнің атыңды немесе басқа есімді жазып көр
    user_name = "Serikzhan"
    user_age = 20
    
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (user_name, user_age))
    
    # Өзгерісті сақтау (МАҢЫЗДЫ!)
    connection.commit()
    print(f"Базаға {user_name} сәтті қосылды!")

    # 3. МӘЛІМЕТТІ ОҚУ (SELECT)
    cursor.execute("SELECT id, name, age FROM users;")
    rows = cursor.fetchall()

    print("\nБАЗАДАҒЫ БАРЛЫҚ ПАЙДАЛАНУШЫЛАР:")
    print("-" * 40)
    for row in rows:
        print(f"ID: {row[0]} | Аты: {row[1]} | Жасы: {row[2]}")
    print("-" * 40)

except Exception as error:
    print("Қате шықты:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Байланыс жабылды.")