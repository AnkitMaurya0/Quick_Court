import sqlite3

DB_NAME = "quickcourt.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.close()
    print(f"Database '{DB_NAME}' created from schema.sql")

if __name__ == "__main__":
    init_db()
