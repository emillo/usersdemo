from flask import Flask, render_template
from flask_login import LoginManager
import views
from database import Database
from user import User
from login import get_login
import os

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_login(user_id)

def not_authorized(e):
    return render_template('401.html'), 401

def not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    
    app.add_url_rule("/",
                     view_func=views.home_page)
    app.add_url_rule("/users",
                     view_func=views.users_page, methods=["GET","POST"])
    app.add_url_rule("/users/<int:user_key>",
                     view_func=views.user_page)
    app.add_url_rule("/new-user",
                     view_func=views.user_add_page, methods=["GET","POST"])
    app.add_url_rule("/users/<int:user_key>/edit",
                     view_func=views.user_edit_page, methods=["GET","POST"])
    app.add_url_rule("/login",
                     view_func=views.login_page, methods=["GET","POST"])
    app.add_url_rule("/logout",
                     view_func=views.logout_page)

    lm.init_app(app)
    lm.login_view = "login_page"

    app.register_error_handler(401, not_authorized)
    app.register_error_handler(404, not_found)
    return app

if __name__ == "__main__":
    currentpath = os.path.realpath(".")
    db = Database(os.path.join(currentpath, "Users.db"))
    app = create_app()
    app.config["db"] = db
    port = app.config.get("FRONTEND_PORT", 8080)
    app.run(host="0.0.0.0", port=port)












