# core/database.py
import sqlite3


class StorageManager:
    def __init__(self, db_name="messenger.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # Таблица настроек
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY, value TEXT)''')
        # Таблица сообщений
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sender TEXT,
            text TEXT,
            status TEXT)''')
        self.conn.commit()

    def save_setting(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        res = self.cursor.fetchone()
        return res[0] if res else ""

    def add_message(self, timestamp, sender, text, status):
        self.cursor.execute("INSERT INTO messages (timestamp, sender, text, status) VALUES (?, ?, ?, ?)",
                            (timestamp, sender, text, status))
        self.conn.commit()

    def get_all_messages(self):
        self.cursor.execute("SELECT timestamp, sender, text, status FROM messages")
        return self.cursor.fetchall()