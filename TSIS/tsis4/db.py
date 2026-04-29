# db.py
import psycopg2
from config import DB_CONFIG

def get_connection():
    """Дерекқорға байланыс орнату"""
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id       SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id            SERIAL PRIMARY KEY,
            player_id     INTEGER REFERENCES players(id),
            score         INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at     TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_player(username):
    """Ойыншыны табу немесе жаңа жасау, id қайтару"""
    conn = get_connection()
    cur = conn.cursor()
    # Бар ма — тексеру
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        player_id = row[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return player_id

def save_game_session(player_id, score, level_reached):
    """Ойын нәтижесін сақтау"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level_reached))
    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard():
    """Top 10 нәтиже — username, score, level, күні"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached,
               gs.played_at::date
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_personal_best(player_id):
    """Ойыншының ең жоғары ұпайы"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(score) FROM game_sessions
        WHERE player_id = %s
    """, (player_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row[0] else 0