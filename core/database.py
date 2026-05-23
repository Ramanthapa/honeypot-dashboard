import sqlite3
from datetime import datetime

DB_PATH = 'logs/attacks.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip_address TEXT,
            port INTEGER,
            attack_type TEXT,
            username TEXT,
            password TEXT,
            raw_data TEXT,
            threat_level TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("[DB] Database ready")

def log_attack(ip, port, attack_type, username='', password='', raw_data='', threat_level='LOW'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attacks
        (timestamp, ip_address, port, attack_type, username, password, raw_data, threat_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (str(datetime.now()), ip, port, attack_type, username, password, raw_data, threat_level))
    conn.commit()
    conn.close()

def get_all_attacks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attacks ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    stats = {}
    cursor.execute('SELECT COUNT(*) FROM attacks')
    stats['total'] = cursor.fetchone()[0]
    cursor.execute('SELECT attack_type, COUNT(*) FROM attacks GROUP BY attack_type')
    stats['by_type'] = cursor.fetchall()
    cursor.execute('SELECT ip_address, COUNT(*) as cnt FROM attacks GROUP BY ip_address ORDER BY cnt DESC LIMIT 5')
    stats['top_ips'] = cursor.fetchall()
    conn.close()
    return stats