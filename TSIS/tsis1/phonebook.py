import psycopg2
import json
from config import load_config  # config.py файлынан функцияны шақыру

def get_connection():
    """ Конфигурацияны жүктеп, базаға қосылу """
    try:
        params = load_config() # database.ini-ден мәліметтерді оқиды
        return psycopg2.connect(**params)
    except Exception as e:
        print(f"Базаға қосылу қатесі: {e}")
        return None

# --- 1. PAGINATION (БЕТТЕРМЕН КӨРУ) ---
def show_paginated():
    page = 0
    limit = 5
    while True:
        conn = get_connection()
        if not conn: break
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.name, c.email, g.name 
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY c.id
                    LIMIT %s OFFSET %s
                """, (limit, page * limit))
                
                rows = cur.fetchall()
                if not rows and page > 0:
                    print("\n--- Соңғы бетке жеттіңіз ---")
                    page -= 1
                    continue
                
                print(f"\n--- Бет {page + 1} ---")
                for r in rows:
                    print(f"Аты: {r[0]:<15} | Email: {str(r[1]):<20} | Тобы: {r[2]}")
            conn.close()
        except Exception as e:
            print(f"Қате шықты: {e}")
            break
            
        cmd = input("\n[n] Келесі, [p] Алдыңғы, [q] Мәзірге қайту: ").lower()
        if cmd == 'n': page += 1
        elif cmd == 'p' and page > 0: page -= 1
        elif cmd == 'q': break

# --- 2. EXPORT TO JSON ---
def export_to_json():
    conn = get_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, c.birthday, g.name, array_agg(ph.phone)
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones ph ON c.id = ph.contact_id
                GROUP BY c.id, g.name
            """)
            rows = cur.fetchall()
            data = []
            for r in rows:
                data.append({
                    "name": r[0],
                    "email": r[1],
                    "birthday": str(r[2]) if r[2] else None,
                    "group": r[3],
                    "phones": r[4] if r[4][0] is not None else []
                })
            
            with open("contacts.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("\n[OK] Деректер 'contacts.json' файлына сақталды!")
        conn.close()
    except Exception as e:
        print(f"Экспорт кезінде қате: {e}")

# --- 3. IMPORT FROM JSON ---
def import_from_json():
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("\n[!] 'contacts.json' файлы табылмады.")
        return

    conn = get_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            for item in data:
                cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                exists = cur.fetchone()
                
                if exists:
                    ans = input(f"'{item['name']}' базада бар. Жаңарту керек пе? (y/n): ")
                    if ans.lower() == 'y':
                        cur.execute("""
                            UPDATE contacts SET email = %s, birthday = %s 
                            WHERE name = %s
                        """, (item.get('email'), item.get('birthday'), item['name']))
                else:
                    cur.execute("INSERT INTO contacts (name, email, birthday) VALUES (%s, %s, %s)", 
                                (item['name'], item.get('email'), item.get('birthday')))
            conn.commit()
            print("\n[OK] Импорт сәтті аяқталды!")
        conn.close()
    except Exception as e:
        print(f"Импорт кезінде қате: {e}")

# --- 4. НЕГІЗГІ МӘЗІР ---
def main():
    while True:
        print("\n======= PHONEBOOK MENU =======")
        print("1. Контактілерді көру (Pagination)")
        print("2. JSON-ға экспорттау")
        print("3. JSON-нан импорттау")
        print("4. Шығу")
        
        choice = input("\nТаңдауыңыз: ")
        
        if choice == '1':
            show_paginated()
        elif choice == '2':
            export_to_json()
        elif choice == '3':
            import_from_json()
        elif choice == '4':
            print("Сау болыңыз!")
            break
        else:
            print("Қате таңдау, қайталап көріңіз.")

if __name__ == "__main__":
    main()