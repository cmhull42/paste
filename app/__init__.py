import sqlite3
from flask import Flask, g
from contextlib import closing
from hashids import Hashids
import string, pyodbc

app = Flask(__name__)
app.config.from_object("config")
hashids = Hashids(app.config["SALT"], 7, string.ascii_letters+string.digits)
from app import views

def connect_db():
	connectionString = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(
							app.config["DRIVER"],
							app.config["DB_SERVER"],
							app.config["DATABASE"],
							app.config["USERNAME"],
							app.config["PASSWORD"])
	return pyodbc.connect(connectionString)

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource("schema.sql", mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
