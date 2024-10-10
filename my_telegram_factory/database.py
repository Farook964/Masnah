import sqlite3
import os

db_file = "bots.db"

def init_db():
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                bot_token TEXT,
                session_name TEXT
            )
        ''')
        conn.commit()
        conn.close()
