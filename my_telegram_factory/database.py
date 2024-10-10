import sqlite3

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('bots.db')
    cursor = conn.cursor()
    # إنشاء جدول البوتات إذا لم يكن موجودًا
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_bot_to_db(token):
    """إضافة توكن البوت إلى قاعدة البيانات."""
    conn = sqlite3.connect('bots.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bots (token) VALUES (?)", (token,))
        conn.commit()
    except sqlite3.IntegrityError:
        print("هذا التوكن موجود بالفعل.")
    finally:
        conn.close()

def remove_bot_from_db(token):
    """حذف توكن البوت من قاعدة البيانات."""
    conn = sqlite3.connect('bots.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bots WHERE token = ?", (token,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_bots_from_db():
    """استرجاع قائمة البوتات من قاعدة البيانات."""
    conn = sqlite3.connect('bots.db')
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM bots")
    bots = [row[0] for row in cursor.fetchall()]
    conn.close()
    return bots
