import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name=None):
        if db_name is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_name = os.path.join(base_dir, "../database/warehouse.db")
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Bin Configuration Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bins (
                bin_id INTEGER PRIMARY KEY,
                capacity INTEGER NOT NULL,
                location_code TEXT NOT NULL
            )
        ''')

        # Shipment Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipment_logs (
                tracking_id TEXT,
                bin_id INTEGER,
                timestamp DATETIME,
                status TEXT
            )
        ''')
        
        self.conn.commit()

    def load_bins(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT bin_id, capacity, location_code FROM bins')
        return cursor.fetchall()

    def log_shipment(self, tracking_id, bin_id, status):
        cursor = self.conn.cursor()
        timestamp = datetime.now()
        cursor.execute('''
            INSERT INTO shipment_logs (tracking_id, bin_id, timestamp, status)
            VALUES (?, ?, ?, ?)
        ''', (tracking_id, bin_id, timestamp, status))
        self.conn.commit()

    def close(self):
        self.conn.close()
