import sqlite3
import json

class Storage:
    def __init__(self, path='tfr.db'):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS samples (
                timestamp REAL,
                cpu REAL,
                mem REAL,
                disk_read INTEGER,
                disk_write INTEGER,
                net_sent INTEGER,
                net_recv INTEGER,
                proc_count INTEGER,
                top_cpu TEXT,
                top_mem TEXT
            )
        ''')
        self.conn.commit()

    def insert(self, data):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['timestamp'],
            data['cpu_total'],
            data['mem_total'],
            data['disk_read'],
            data['disk_write'],
            data['net_sent'],
            data['net_recv'],
            data['proc_count'],
            json.dumps(data['top_cpu']),
            json.dumps(data['top_mem'])
        ))
        self.conn.commit()
