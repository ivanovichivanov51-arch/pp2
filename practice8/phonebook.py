import psycopg2
from config import load_config

def add_or_update_contact(user_name, user_phone):
    """3.2.2: Процедураны шақыру (Upsert)"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (user_name, user_phone))
            conn.commit()
            print(f"Дайын! {user_name} базаға сақталды/жаңартылды.")
    except Exception as e:
        print(f"Қосу қатесі: {e}")

def search_contact(pattern):
    """3.2.1: Функцияны шақыру (Search)"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
                results = cur.fetchall()
                if results:
                    print(f"\n'{pattern}' бойынша табылғандар:")
                    for row in results:
                        print(f"Аты: {row[0]}, Телефоны: {row[1]}")
                else:
                    print(f"\n'{pattern}' бойынша ештеңе табылмады.")
    except Exception as e:
        print(f"Іздеу қатесі: {e}")

def delete_contact(search_param):
    """3.2.5: Контактіні жою"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (search_param,))
            conn.commit()
            print(f"Контакт жойылды балапан: {search_param}")
    except Exception as e:
        print(f"Жою қатесі: {e}")

def get_paged_contacts(page_number, page_size=2):
    """3.2.3: Беттерге бөліп шығару"""
    config = load_config()
    offset = (page_number - 1) * page_size
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (page_size, offset))
                results = cur.fetchall()
                if results:
                    print(f"\n--- {page_number}-бет ---")
                    for row in results:
                        print(f"{row[0]}: {row[1]}")
                else:
                    print("\nБұл бетте дерек жоқ.")
    except Exception as e:
        print(f"Беттеу қатесі: {e}")

# НЕГІЗГІ МӘЗІР (Бұл бөлім файлда ТЕК БІР РЕТ болуы керек)
if __name__ == "__main__":
    while True:
        print("\n--- Телефон кітапшасы ---")
        print("1. Контакт қосу/жаңарту")
        print("2. Іздеу")
        print("3. Жою")
        print("4. Беттер бойынша көру (Pagination)")
        print("0. Шығу")
        
        choice = input("\nне керек балапан: ")
        
        if choice == "1":
            name = input("Есімді енгізеғой балапан: ")
            phone = input("Телефонды енгізіңізеғой балапан: ")
            add_or_update_contact(name, phone)
            
        elif choice == "2":
            pattern = input("Кімді немесе қандай нөмірді іздейміз балапан?: ")
            search_contact(pattern)
            
        elif choice == "3":
            param = input("Жойылатын контактінің атын немесе нөмірін жазағой балапан: ")
            delete_contact(param)
            
        elif choice == "4":
            try:
                page = int(input("Қай бетті ашамыз балапан? (1, 2, 3...): "))
                get_paged_contacts(page)
            except ValueError:
                print("Тек сандарды балапан!")
                
        elif choice == "0":
            print("Бағдарлама аяқталды балапан. аманшылықта!")
            break
            
        else:
            print("Қате таңдау! 0-ден 4-ке дейінгі санды таңда балапан")