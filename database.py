import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            score INTEGER,
            reason TEXT,
            url TEXT UNIQUE,
            date_found TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def job_exists(url):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM jobs WHERE url = ?", (url,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def save_job(title, company, score, reason, url):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    date_found = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cursor.execute("""
        INSERT OR IGNORE INTO jobs (title, company, score, reason, url, date_found)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, company, score, reason, url, date_found))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")