import sqlite3

conn = sqlite3.connect("safeher.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")