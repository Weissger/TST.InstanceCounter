import sqlite3
import collections
import functools


class InstanceCountStore(object):
    def __init__(self, sqlite_path):
        self.__connection = sqlite3.connect(sqlite_path, timeout=10)
        self.__connection.execute("""
            CREATE TABLE IF NOT EXISTS instance_counts (type, instance_count INT, PRIMARY KEY(type))
            """)
        self.__connection.commit()

    def store_instance_count(self, in_type, count):
        cur = self.__connection.cursor()
        cur.execute("""
            INSERT INTO instance_counts VALUES (?, ?)
          """, [in_type, count])
        cur.close()

    def get_instance_count(self, in_type):
        cur = self.__connection.cursor()
        cur.execute("""
            SELECT instance_count FROM instance_counts WHERE type=?
          """, [in_type])
        res = cur.fetchone()
        cur.close()
        return res[0]
