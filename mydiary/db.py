#!/usr/bin/python

import psycopg2


class MyDiaryDatabase:
    """This defines the database connection and holds methods for creating and deleting tables"""

    def __init__(self, db_name):
        self.mydb = 'dbi88r8l9ebmvl'

        try:
            self.conn = psycopg2.connect(dbname=self.mydb, user='sodgzedklqgcec', host='ec2-54-227-241-179.compute-1.amazonaws.com', password='8e8928519826655653cf3f4c5a32efcc71a3ae97bcfe021faa0cea9246c27c19', port='5432')
            self.cursor = self.conn.cursor()
        
        # self.mydb = 'mydiarydb'

        # try:
        #     self.conn = psycopg2.connect(dbname=self.mydb, user='postgres', host='localhost', password='postgres', port='5432')
        #     self.cursor = self.conn.cursor()

        except Exception as e:
            print("Unable to connect. Check dbname, user or password inputs.")
            print(e)

    def new_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                    (user_id SERIAL NOT NULL PRIMARY KEY, 
                    name VARCHAR(150) NOT NULL, 
                    email VARCHAR(150) NOT NULL, 
                    password VARCHAR(150) NOT NULL,
                    registered VARCHAR(10) NOT NULL,
                    lastUsed VARCHAR(10) NOT NULL,
                    deletedEntries INTEGER,
                    currentEntries INTEGER,
                    allEntries INTEGER,
                    notifications BOOLEAN);""")
        self.conn.commit()

    def new_entries_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS entries 
                    (entry_id SERIAL NOT NULL PRIMARY KEY, 
                    user_id INTEGER NOT NULL, 
                    title VARCHAR(150) NOT NULL, 
                    data VARCHAR(5000) NOT NULL, 
                    date_modified VARCHAR(10) NOT NULL);""")
        self.conn.commit()
    
    def new_blacklist(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist 
                    (token VARCHAR(500) NOT NULL,
                    user_id INTEGER NOT NULL);""")
        self.conn.commit()

    def drop_entries_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS entries;""")
        self.conn.commit()

    def drop_users_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users;""")
        self.conn.commit()

    def check_table(self,table_name):
        sql_check_fn = """SELECT * from %s;"""
        self.cursor.execute(sql_check_fn, (table_name,))
        rows = self.cursor.fetchall()
        return rows