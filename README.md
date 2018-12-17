# Users Demo
A simple demo of an api for managing a user database

Both the api and the frontend are implemented using [flask](http://flask.pocoo.org/).

The database is a file based sqlite db; the file [users.sql](app/users.sql) contains the db schema and the creation of the first user 'admin' with password '12345'. The admin user has the privilege to add, delete and edit users.

The frontend webapp is running on http port 8080 and the backend api runs on http port 9999

The responsive UI is implemented with [bulma](https://bulma.io)
                                                                                
## Requirements

First of all we need a sqlite database:
```bash
# in a debian-based distro
sudo apt install sqlite3

# create the database in the app dir (also creates the admin user with password '12345')
cd app/
sqlite3 Users.db < users.sql
```

Then we need some python libraries: we can install them in a virtual python environment:

```bash
# up one level to the root of the checkout
cd ..

# install pyvenv and pip
# in a debian-based distro
sudo apt install python3-venv python3-pip

#create the virtual env
pyvenv .

# activate the virtual environment
source bin/activate

# install the dependencies with pip
pip install -r requirements.txt
```

## Running the demo

```bash
# go to the app dir
cd app/

# launch the backend api
python backend.py &

# launch the frontend webapp
python frontend.py &
```

now you can point your browser to http://localhost:8080 for the webapp frontend and explore the api on http://localhost:9999

the entry point for using the api is http://localhost:9999/users
