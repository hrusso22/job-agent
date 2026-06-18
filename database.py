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
            date_found TEXT,
            date_posted TEXT
        )
    """)
    
    # Add date_posted column if it doesn't exist yet
    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN date_posted TEXT")
    except:
        pass
    
    conn.commit()
    conn.close()

def job_exists(url):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_job(title, company, score, reason, url, date_posted=None):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    date_found = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cursor.execute("""
        INSERT OR IGNORE INTO jobs (title, company, score, reason, url, date_found, date_posted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, company, score, reason, url, date_found, date_posted))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")