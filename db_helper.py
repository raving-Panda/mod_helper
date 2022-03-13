#import mysql.connector
import sqlite3
import datetime
import calendar
import settings as env
import sys

from sqlite3 import Error


class DBhelper:
    def __init__(self):
        self.create_connection(env.DB_FILE)
    
    def create_connection(self,db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            self.conn = conn
        except Error as e:
            print(e)

    def get_messages(self):
        """ create a database connection to a SQLite database """
        timestamp=""
        with open("timestamp.xsb",'r') as f:
            timestamp=f.read()
        execStr = f"SELECT text,timestamp from messages where timestamp > {timestamp} ORDER BY timestamp;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(execStr)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(e)

    def set_timestamp(self,tstamp):
        with open('timestamp.xsb','w') as f:
            f.write(str(tstamp))
            
    def get_messages2(self,user):
        """ create a database connection to a SQLite database """
        execStr = "SELECT * from attachments;"
        try:
            self.conn.execute(execStr)
            self.conn.commit()
        except Error as e:
            print(e)

    #finally:
    #    if conn:
    #        conn.close()


if __name__ == '__main__':
    db = DBhelper("./sqlite3.db")
