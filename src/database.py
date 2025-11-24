import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="logistech.db"):
        self.db_name = db_name
        # Connect to SQLite database
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.create_tables()
        except sqlite3.Error as err:
            print(f"Error connecting to database: {err}")
            raise

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Bin Configuration Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bins (
                bin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                capacity INTEGER NOT NULL,
                location_code TEXT NOT NULL
            )
        ''')

        # Shipment Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipment_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_id TEXT,
                bin_id INTEGER,
                timestamp TEXT,
                status TEXT
            )
        ''')
        
        self.conn.commit()
        cursor.close()

    def load_bins(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT bin_id, capacity, location_code FROM bins')
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def log_shipment(self, tracking_id, bin_id, status):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        # SQLite uses ? as placeholder
        cursor.execute('''
            INSERT INTO shipment_logs (tracking_id, bin_id, timestamp, status)
            VALUES (?, ?, ?, ?)
        ''', (tracking_id, bin_id, timestamp, status))
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()
