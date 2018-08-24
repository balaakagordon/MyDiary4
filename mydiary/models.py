"""
Holds the app's classes and methods
"""
# -*- coding: utf-8 -*-


"""importing packages"""
from flask import Flask, jsonify
from mydiary import app_db


""" the diary app is modelled as an object with it's own \
parameters and methods """
class MyDiary:
    def __init__(self):
        self.user_entries = None


    def addUser(self, user_name, user_email, user_password):
        sql_check_fn = """SELECT * from users WHERE email = %s;"""
        app_db.cursor.execute(sql_check_fn, (user_email,))
        rows = app_db.cursor.fetchall()
        if rows == []:
            sql_insert_fn = """INSERT INTO users (name, email, password) VALUES(%s, %s, %s);"""
            app_db.cursor.execute(sql_insert_fn, (
                            user_name,
                            user_email,
                            user_password
                            ))
            app_db.conn.commit()
            message = "Registered Successfully!"
        else:
            message = "This user already exists!"
        return message

    def userLogin(self, login_email, login_password):
        """ login method requires a username and password and returns a user ID """
        sql_fn = """SELECT * from users WHERE email = %s AND password = %s;"""
        app_db.cursor.execute(sql_fn, (
                            login_email,
                            login_password
                            ))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Sorry, incorrect credentials"
            return message
        return rows[0][0]
    
    def userLogout(self, token, user_id):
        """ logout method adds current token to blacklist \
        table """
        sql_insert_fn = """INSERT INTO blacklist (token, user_id) VALUES(%s, %s);"""
        app_db.cursor.execute(sql_insert_fn, (
                            token,
                            user_id
                            ))
        app_db.conn.commit()
        return "Successfully logged out"
    
    def inBlacklist(self, token):
        """ Check blacklist for generated token """
        sql_check_fn = """SELECT * from blacklist WHERE token = %s;"""
        app_db.cursor.execute(sql_check_fn, (token,))
        rows = app_db.cursor.fetchall()
        if rows == []:
            return False
        return True

class Entries:
    """ Entry lists for each user are modelled as objects with \
    parameters and methods """

    def __init__(self):
        pass

    def addEntry(self, user_id_data, title_data, entry_data, now_time):
        """ once an entry's data is submitted the server checks whether it exists \
        Entries to be added to entrylist """
        sql_check_fn = """SELECT * from entries WHERE data = %s AND title = %s AND user_id = %s;"""
        app_db.cursor.execute(sql_check_fn, (
                            entry_data,
                            title_data,
                            user_id_data
                            ))
        rows = app_db.cursor.fetchall()
        if rows == []:
            sql_insert_fn = """INSERT INTO entries (user_id, title, data, date_modified) VALUES(%s, %s, %s, %s);"""
            app_db.cursor.execute(sql_insert_fn, (
                            user_id_data,
                            title_data,
                            entry_data,
                            now_time
                            ))
            app_db.conn.commit()
            message = "Entry added successfully"
        else:
            message = "Entry already exists"
        return message
        

    def modifyEntry(self, title_data, entry_data, edit_time, entry_id_data, user_id_data):
        """ edits diary entries """
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s;"""
        app_db.cursor.execute(sql_check_fn, (user_id_data, entry_id_data))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Entry not found"
        elif rows[0][4] != edit_time:
            message = "Sorry, cannot edit entries made before today"
        else:
            sql_update_fn = """UPDATE entries SET title = %s, data = %s, date_modified = %s WHERE user_id = %s AND entry_id = %s;"""
            app_db.cursor.execute(sql_update_fn, (
                            title_data,
                            entry_data,
                            edit_time,
                            user_id_data,
                            entry_id_data
                            ))
            message = "Entry edited"
            app_db.conn.commit()
        return message

    def getOneEntry(self, user_id, diary_entry_id):
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s;"""
        app_db.cursor.execute(sql_check_fn, (user_id, diary_entry_id))
        row = app_db.cursor.fetchall()
        if row == []:
            message = "The specified entry cannot be found"
            return message
        entry = {
            'entry_id': row[0][0], 
            'user_id': row[0][1], 
            'title': row[0][2],
            'data': row[0][3],
            'date': row[0][4]
            }
        return entry

    def getAllEntries(self, user_id_data):
        sql_check_fn = """SELECT * from entries WHERE user_id = %s;"""
        app_db.cursor.execute(sql_check_fn, [user_id_data])
        rows = app_db.cursor.fetchall()
        entry_list = []
        for row in rows:
            entry = { 
                'entry_id': row[0],
                'user_id': row[1],
                'title': row[2],
                'data': row[3],
                'date': row[4]
                }
            entry_list.append(entry)
        return entry_list[:]
    
    def deleteEntry(self, entry_id_data, user_id_data):
        """ this method deletes diary entries """
        sql_delete_fn = """DELETE from entries where user_id = %s AND entry_id = %s;"""
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s;"""
        print("models: entry: " + str(entry_id_data))
        print("models: user: " + str(user_id_data))
        app_db.cursor.execute(sql_check_fn, (user_id_data, entry_id_data))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Unable to delete. Entry does not exist"
        else:
            app_db.cursor.execute(sql_delete_fn, (user_id_data, entry_id_data))
            message = "Entry successfully deleted"
        return message
