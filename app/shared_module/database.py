from time import sleep
from datetime import datetime
from threading import Lock
import sqlite3 
from .helpers import json2dict, str2hex
from .singleton import Singleton

class SQLITE(metaclass=Singleton):

    __internalLock = Lock()
    __conn = None

    def __init__(self, db_file = None, tableName = []):
        with self.__internalLock:
            if db_file is None:
                self.__conn = sqlite3.connect(':memory:', check_same_thread = False)
            else:
                self.__conn = sqlite3.connect(db_file, check_same_thread = False)

            for name in tableName:
                self._create_table_if_not_exist(name)

    def insert(self, table, value):
        with self.__internalLock:
            self._create_table_if_not_exist(table)
            cursor = self.__conn.cursor()
            cursor.execute('INSERT INTO {} (value) VALUES ({})'.format(table, value))
            self.__conn.commit()

    def get_values(self, table, startDate = None, endDate = None):
        with self.__internalLock:
            ans = list()
            if self._table_exist(table):
                cursor = self.__conn.cursor()
                cursor.execute('SELECT value, date_created from {}'.format(table))
                temp = cursor.fetchall()

                for data in temp:
                    ans.append((
                        float(data[0]), 
                        datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
                        ))
                self.__conn.commit()
            return ans

    def get_last_value(self, table):
        with self.__internalLock:
            ans = list()
            if self._table_exist(table):
                cursor = self.__conn.cursor()
 
                cursor.execute(''' 
                    SELECT value, date_created FROM {} 
                    ORDER BY date_created DESC LIMIT 1 
                    '''.format(table))
                data = cursor.fetchone()
                if not data is None:
                    ans = [float(data[0]), 
                    datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')]
                self.__conn.commit()
            return ans

    def _create_table_if_not_exist(self, table):
        cursor = self.__conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            date_created DATETIME DEFAULT (datetime('now','localtime')) 
            )                        
        '''.format(table))
        self.__conn.commit()

    def _table_exist(self, table):
        cursor = self.__conn.cursor()

        cursor.execute('''
            SELECT count(name) FROM sqlite_master 
            WHERE type=\'table\' AND name=\'{}\' 
            '''.format(table))

        ans = cursor.fetchone()[0]==1
        self.__conn.commit()
        return bool(ans)            

    def get_table_name(self):
        with self.__internalLock:
            cursor = self.__conn.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type =\'table\' AND name NOT LIKE \'sqlite_%\'')
            ans = [temp[0] for temp in cursor]
            self.__conn.commit()
            return ans


