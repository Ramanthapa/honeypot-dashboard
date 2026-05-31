"""
db_setup.py — Day 5
Creates the SQLite database and attacks table.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "honeypot.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            ip          TEXT    NOT NULL,
            port        INTEGER,
            trap_type   TEXT    NOT NULL,  -- 'SSH' or 'HTTP'
            username    TEXT,
            password    TEXT,
            extra       TEXT,              -- raw command / path / user agent
            threat      TEXT DEFAULT 'Low' -- Low / Medium / High / Critical
        )
    """)

    conn.commit()
    conn.close()
    print("[*] Database initialized — honeypot.db ready")


if __name__ == "__main__":
    init_db()