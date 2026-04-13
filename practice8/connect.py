import psycopg2
from config import load_config

def connect():
    """ PostgreSQL дерекқорына қосылу """
    config = load_config()
    try:
        # Конфигурация арқылы қосылу
        with psycopg2.connect(**config) as conn:
            print('Дерекқорға сәтті қосылдық!')
            with conn.cursor() as cur:
                # Базаның нұсқасын тексеру (жай тексеріс үшін)
                cur.execute('SELECT version()')
                db_version = cur.fetchone()
                print(f'PostgreSQL нұсқасы: {db_version}')
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Қате: {error}")

if __name__ == '__main__':
    connect()
    