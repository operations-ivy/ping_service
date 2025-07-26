import sqlite3

class SQLStorage:
    @staticmethod
    def connect(db_name):
        return sqlite3.connect(":memory:" if db_name == ":memory:" else db_name)

    @staticmethod
    def create_table(conn):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ping_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                min_rtt REAL,
                avg_rtt REAL,
                max_rtt REAL,
                packet_loss REAL,
                error TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    @staticmethod
    def insert_result(conn, result):
        cursor = conn.cursor()
        if result['min_rtt']:
            cursor.execute("""
                INSERT INTO ping_results (host, success, min_rtt, avg_rtt, max_rtt, packet_loss)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (result['host'], result['success'], result['min_rtt'], result['avg_rtt'], result['max_rtt'], result['packet_loss']))
            conn.commit()
        else:
            cursor.execute("""
                INSERT INTO ping_results (host, success, error)
                VALUES (?, ?, ?)
            """, (result['host'], result['success'], result.get('error', '')))
            conn.commit()

    @staticmethod
    def fetch_last_5_results(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ping_results
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        return cursor.fetchall()