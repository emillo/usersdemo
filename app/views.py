from flask import render_template, current_app, abort, request, redirect, url_for, flash
from forms import LoginForm, UserEditForm
from login import get_login
from flask_login import login_user, logout_user, current_user, login_required
from passlib.hash import pbkdf2_sha256 as hasher
import requests, json, settings


def api_url(path):
    return "http://localhost:9999" + path

def home_page():
    return render_template("home.html")

def users_page():

    db = current_app.config["db"]
    if request.method == "GET":
        response = requests.get(api_url('/users/'))
        users = response.json()
        return render_template("users.html",users=users)
    else:
        if not current_user.is_admin:
            abort(401)
        form_user_keys = request.form.getlist("user_keys")
        for form_user_key in form_user_keys:
            requests.delete(api_url('/users/{:d}'.format(int(form_user_key))))
        flash("%(num)d users deleted." % {"num": len(form_user_keys)})
        return redirect(url_for("users_page"))

def user_page(user_key):
    response = requests.get(api_url('/users/{:d}'.format(user_key)))
    if response.status_code == 404:
        abort(404)
    user = response.json()
    return render_template("user.html",user=user)

@login_required
def user_add_page():
    if not current_user.is_admin:
        abort(401)
    form = UserEditForm()
    if form.validate_on_submit():
        payload = {
            "ID": 0,
            "username": form.data['username'],
            "firstname": form.data['firstname'],
            "lastname" : form.data['lastname'],
            "email": form.data['email'],
            "password": form.data['password']
        }
        
        try:
            response = requests.post(api_url('/users/'), json=payload)
            user = response.json()
            user_key = user['ID']
        except:
            flash("Username already taken")
            return render_template("user-edit.html", form=form)

        return redirect(url_for("user_page", user_key=user_key))

    return render_template("user-edit.html", form=form)

@login_required
def user_edit_page(user_key):
    if not current_user.is_admin:
        abort(401)
    response = requests.get(api_url('/users/{:d}'.format(user_key)))
    user = response.json()
    print(user)
    form = UserEditForm()
    if form.validate_on_submit():
        payload = {
            "ID": user_key,
            "username": form.data["username"],
            "firstname": form.data["firstname"],
            "lastname": form.data["lastname"],
            "email": form.data["email"],
            "password": form.data["password"]
            }
        print(payload)
        try:
            response = requests.put(api_url('/users/{:d}'.format(user_key)), json=payload)
            user = response.json()
            user_key = user['ID']
        except:
            flash("Username already taken")
            return render_template("user-edit.html", form=form)
            
        return redirect(url_for("user_page", user_key=user_key))

    form.username.data = user['username']
    form.firstname.data = user['firstname']
    form.lastname.data = user['lastname']
    form.email.data = user['email']
    return render_template("user-edit.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_login(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have successfully logged in as " + username )
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home_page"))






























