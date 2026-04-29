import psycopg2
import json
from config import load_config

def get_connection():
    """ database.ini арқылы базаға қосылу """
    try:
        params = load_config()
        return psycopg2.connect(**params)
    except Exception as e:
        print(f"Қосылу қатесі: {e}")
        return None

# --- 1. ПАГИНАЦИЯ ЖӘНЕ БАРЛЫҚ МӘЛІМЕТТІ ШЫҒАРУ ---
def show_paginated():
    page = 0
    limit = 5
    while True:
        conn = get_connection()
        if not conn: break
        
        try:
            with conn.cursor() as cur:
                # SQL: contacts, groups және phones кестелерін біріктіріп, барлық деректі алу
                cur.execute("""
                    SELECT c.name, 
                           COALESCE(c.email, '---'), 
                           COALESCE(c.birthday::text, '---'), 
                           COALESCE(g.name, '---'), 
                           COALESCE(string_agg(ph.phone, ', '), 'Нөмір жоқ')
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones ph ON c.id = ph.contact_id
                    GROUP BY c.id, g.name
                    ORDER BY c.id
                    LIMIT %s OFFSET %s
                """, (limit, page * limit))
                
                rows = cur.fetchall()
                if not rows and page > 0:
                    print("\n--- Бұл соңғы бет ---")
                    page -= 1
                    continue
                
                print(f"\n{'='*110}")
                print(f"{'Бет: ' + str(page + 1):^110}")
                print(f"{'='*110}")
                print(f"{'Аты':<15} | {'Email':<20} | {'Туған күні':<12} | {'Тобы':<12} | {'Телефондар'}")
                print(f"{'-'*110}")
                
                for r in rows:
                    print(f"{str(r[0]):<15} | {str(r[1]):<20} | {str(r[2]):<12} | {str(r[3]):<12} | {r[4]}")
                print(f"{'='*110}")
                
            conn.close()
        except Exception as e:
            print(f"Деректерді шығару қатесі: {e}")
            break
            
        cmd = input("\n[n] Келесі, [p] Алдыңғы, [q] Мәзірге қайту: ").lower()
        if cmd == 'n': page += 1
        elif cmd == 'p' and page > 0: page -= 1
        elif cmd == 'q': break

# --- 2. ЭКСПОРТ (JSON-ға сақтау) ---
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
            print("\n[OK] Деректер contacts.json файлына сақталды!")
        conn.close()
    except Exception as e:
        print(f"Экспорт қатесі: {e}")

# --- 3. ИМПОРТ ЖӘНЕ ЖАҢАРТУ ---
def import_from_json():
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("\n[!] Импорттау үшін алдымен contacts.json файлы керек!")
        return

    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            for item in data:
                cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                exists = cur.fetchone()
                if exists:
                    ans = input(f"'{item['name']}' бар. Жаңарту керек пе? (y/n): ")
                    if ans.lower() == 'y':
                        cur.execute("UPDATE contacts SET email = %s, birthday = %s WHERE name = %s", 
                                    (item.get('email'), item.get('birthday'), item['name']))
                else:
                    cur.execute("INSERT INTO contacts (name, email, birthday) VALUES (%s, %s, %s)", 
                                (item['name'], item.get('email'), item.get('birthday')))
            conn.commit()
            print("\n[OK] Импорт сәтті аяқталды!")
        conn.close()
    except Exception as e:
        print(f"Импорт қатесі: {e}")

# --- 4. МӘЗІР ---
def main():
    while True:
        print("\n" + "="*30)
        print("   PHONEBOOK SYSTEM (SITE)")
        print("="*30)
        print("1. Тізімді көру (Pagination)")
        print("2. JSON-ға экспорт")
        print("3. JSON-нан импорт/жаңарту")
        print("4. Шығу")
        
        choice = input("\nТаңдауыңыз: ")
        
        if choice == '1': show_paginated()
        elif choice == '2': export_to_json()
        elif choice == '3': import_from_json()
        elif choice == '4': 
            print("Бағдарлама аяқталды. Сау болыңыз!")
            break
        else:
            print("Қате таңдау!")

if __name__ == "__main__":
    main()