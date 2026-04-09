import psycopg2
from config import load_config

def connect():
    """ PostgreSQL деректер қорына қосылу """
    conn = None
    try:
        # Конфигурацияны database.ini файлынан оқу
        params = load_config()

        # Серверге қосылу
        print('PostgreSQL деректер қорына қосылудамыз...')
        conn = psycopg2.connect(**params)
		
        # Курсор жасау
        cur = conn.cursor()
        
        # Нұсқасын тексеру
        cur.execute('SELECT version()')
        db_version = cur.fetchone()

        print(f'Қосылу сәтті аяқталды! \nнуска: {db_version}')
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Қате шықты: {error}")
    finally:
        if conn is not None:
            conn.close()
            print('Байланыс жабылды.')

if __name__ == '__main__':
    connect()