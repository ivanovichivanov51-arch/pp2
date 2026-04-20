import psycopg2
from config import load_config

def connect():
    """ PostgreSQL базасына қосылу """
    config = load_config()
    try:
        #  кодыңдағыдай қосылу, бірақ параметрлер config-тен алынады
        conn = psycopg2.connect(**config)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Қосылу қатесі:", error)
        return None