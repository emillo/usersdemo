import sqlite3 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from user import User

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_user(self, user):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Users 
            (username, firstname, lastname, 
            email, password) VALUES (?,?,?,?,?)"""
            try:
                cursor.execute(query, (user['username'], user['firstname'],
                                       user['lastname'], user['email'],
                                       hasher.hash(user['password'])))
            except dbapi2.IntegrityError as e:
                raise Exception(e)
            connection.commit()
            user_key = cursor.lastrowid
        return self.get_user(user_key)

    def delete_user(self,user_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Users WHERE (ID = ?)"
            cursor.execute(query,(user_key,))
            connection.commit()

    def get_user(self,user_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT ID, username, firstname, lastname, 
            email, password FROM Users WHERE (ID = ?)"""
            cursor.execute(query,(user_key,))
            ID, username, firstname, lastname,email, password = cursor.fetchone()
        return User(ID, username,firstname,lastname,email,password)


    def update_user(self, user_key, user):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query ="""UPDATE Users SET username = ?, firstname = ?, 
            lastname =?, email = ?, password = ?  WHERE (ID = ?)"""
            try:
                cursor.execute(query,(user['username'], user['firstname'],
                                      user['lastname'], user['email'],
                                      hasher.hash(user['password']), user_key,))
            except dbapi2.IntegrityError as e:
                raise Exception(e)
            
            connection.commit()
        return self.get_user(user_key)

    def get_users(self):
        users = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT ID, username, firstname, lastname, 
            email, password FROM Users ORDER BY ID"""
            cursor.execute(query)
            for user_key, username, firstname, lastname, email, password in cursor:
                users.append(User(user_key, username, firstname,
                                             lastname, email, password))
        return users
    
    def get_password(self,username):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT password FROM Users WHERE username = ?"
            cursor.execute(query, (username,))
            password = cursor.fetchone()[0]
        return password












