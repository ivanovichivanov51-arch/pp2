import psycopg2
from config import load_config

def connect():
    """ PostgreSQL серверіне қосылу """
    conn = None
    try:
        # Конфигурацияны жүктеу
        params = load_config()

        # Қосылу
        print('PostgreSQL деректер қорына қосылуда...')
        conn = psycopg2.connect(**params)
        
        # Курсор құру
        cur = conn.cursor()
        
        # PostgreSQL нұсқасын тексеру
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f'Сәтті қосылды! База нұсқасы: {db_version}')
        
        # Жабу
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Қате шықты: {error}")
    finally:
        if conn is not None:
            conn.close()
            print('Байланыс жабылды.')

if __name__ == '__main__':
    connect()