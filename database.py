import sqlite3

def init_db():
    conn = sqlite3.connect('reputation.db')
    cursor = conn.cursor()
    
    # Jobs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        customer_contact TEXT NOT NULL,
        job_type TEXT,
        status TEXT DEFAULT 'completed',
        feedback TEXT,
        sentiment TEXT,
        notified_owner INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()

def add_job(name, contact, job_type):
    conn = sqlite3.connect('reputation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (customer_name, customer_contact, job_type) VALUES (?, ?, ?)',
                   (name, contact, job_type))
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return job_id

def update_feedback(job_id, feedback, sentiment):
    conn = sqlite3.connect('reputation.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET feedback = ?, sentiment = ? WHERE id = ?',
                   (feedback, sentiment, job_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
