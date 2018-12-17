from flask import Flask, abort
from flask_restplus import Api, Resource, fields
from database import Database
import os

currentpath = os.path.realpath(".")
db = Database(os.path.join(currentpath, "Users.db"))

app = Flask(__name__)
app.config.from_object("settings")

api = Api(app, version="1.0", title="Users API Demo",
          description="A simple API for managing users")
ns = api.namespace("users", description="Users operations")

user = api.model("User", {
    "ID": fields.Integer,
    "username": fields.String,
    "firstname": fields.String,
    "lastname": fields.String,
    "email": fields.String,
    "password": fields.String
})


class UserDAO(object):
    def __init__(self):
        self.users = []

    def list_users(self):
        self.users = db.get_users()
        return self.users

    def get(self, id):
        try:
            user = db.get_user(id)
        except:
            return abort(404, "User {} not found".format(id))
        return user

    def add_user(self, newuser):
        try:
            user = db.add_user(newuser)
        except:
            return abort(409, "Username already taken")
        return user

    def delete_user(self, id):
        try:
            db.get_user(id)
        except:
            return abort(404, "User {} not found".format(id))
        db.delete_user(id)

    def update_user(self, id, user):
        try:
            return db.update_user(id, user)
        except:
            return abort(404, "User {} not found".format(id))


DAO = UserDAO()


@ns.route("/")
@ns.doc("UserList")
class UserList(Resource):
    """GET shows a list of all users and you can add new users with POST"""

    @ns.doc("list_users")
    @ns.marshal_with(user)
    def get(self):
        """List all users"""
        return DAO.list_users()

    @ns.doc("add_user")
    @ns.expect(user)
    @ns.response(409, "Username already taken")
    @ns.marshal_with(user, code=201)
    def post(self):
        """Create a new user"""
        return DAO.add_user(api.payload), 201


@ns.route("/<int:id>")
@ns.response(404, "User not found")
@ns.param("id", "The user identifier")
class User(Resource):
    """Shows a single user and lets you update and delete it."""

    @ns.doc("get_user")
    @ns.marshal_with(user)
    def get(self, id):
        """Fetch a single user by ID"""
        return DAO.get(id)

    @ns.doc("delete_user")
    @ns.response(204, "User deleted")
    def delete(self, id):
        """Delete a user by ID"""
        DAO.delete_user(id)
        return "", 204

    @ns.doc("update_user")
    @ns.param("id", "The user identifier")
    @ns.expect(user)
    @ns.marshal_with(user)
    def put(self, id):
        """Update an user by ID"""
        return DAO.update_user(id, api.payload), 201


if __name__ == "__main__":
    port = app.config.get("BACKEND_PORT", 9999)
    app.run(host="0.0.0.0", port=port, debug=True)
