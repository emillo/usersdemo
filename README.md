# Users Demo
A simple demo of an api for managing a user database

The database is sqlite

Both the api and the frontend are implemented using flask.
                                                                                
## Requirements

First of all we need a sqlite database:
```bash
# in a debian like distro
sudo apt install sqlite3

# create the database in the app dir (also create the admin user with password '12345')
cd app/
sqlite3 Users.db < users.sql
```

Then we need some python libraries: we can install them in a virtual python environment:

```bash
# install pyvenv and pip
# in a debian-like distro
sudo apt install python3-venv python3-pip

#create the virtual env
pyvenv .

# activate the virtual environment
source bin/activate

# install the dependencies with pip
pip install flask flask_restplus flask_login flask_wtf requests passlib sqlite3
```

