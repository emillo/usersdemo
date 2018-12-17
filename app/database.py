import sqlite3 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from user import User


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_user(self, user):
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = """INSERT INTO Users
            (username, firstname, lastname,
            email, password) VALUES (?,?,?,?,?)"""
            try:
                cur.execute(query, (user['username'], user['firstname'],
                                    user['lastname'], user['email'],
                                    hasher.hash(user['password'])))
            except dbapi2.IntegrityError as e:
                raise Exception(e)
            connection.commit()
            user_key = cur.lastrowid
        return self.get_user(user_key)

    def delete_user(self, user_key):
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = "DELETE FROM Users WHERE (ID = ?)"
            cur.execute(query, (user_key,))
            connection.commit()

    def get_user(self, user_key):
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = """SELECT ID, username, firstname, lastname,
            email, password FROM Users WHERE (ID = ?)"""
            cur.execute(query, (user_key,))
            ID, username, firstname, lastname, email, password = cur.fetchone()
        return User(ID, username, firstname, lastname, email, password)

    def update_user(self, user_key, user):
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = """UPDATE Users SET username = ?, firstname = ?,
            lastname =?, email = ?, password = ?  WHERE (ID = ?)"""
            try:
                cur.execute(query, (user["username"], user["firstname"],
                                    user["lastname"], user["email"],
                                    hasher.hash(user["password"]),
                                    user_key,))
            except dbapi2.IntegrityError as e:
                raise Exception(e)

            connection.commit()
        return self.get_user(user_key)

    def get_users(self):
        users = []
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = """SELECT ID, username, firstname, lastname,
            email, password FROM Users ORDER BY ID"""
            cur.execute(query)
            for id, username, firstname, lastname, email, password in cur:
                users.append(User(id, username, firstname,
                                  lastname, email, password))
        return users

    def get_password(self, username):
        with dbapi2.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = "SELECT password FROM Users WHERE username = ?"
            cur.execute(query, (username,))
            password = cur.fetchone()[0]
        return password
