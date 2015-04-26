from app import app
from flask import request, session, g, redirect, url_for, \
abort, render_template, flash
from string import capwords as capitalize
from app import hashids
import json
from datetime import datetime

@app.route('/')
def show_entries():
	defaults = {"language": "python",
				"linenumbers": "true",
				"supportedModes": app.config["SUPPORTED_MODES"],
				"pasteText": "",
				"readOnly": "false",
				"capwords": capitalize}
	return render_template("edit.html", **defaults)

@app.route("/add", methods=["POST"])
def add_entry():
	title = request.form["title"] if "title" in request.form else None
	text = request.form["text"]
	linenumbers = "true" if "linenumbers" in request.form else "false"
	language = request.form["language"]
	author = request.form["author"] if "author" in request.form else None
	options = json.dumps({"linenumbers": linenumbers, "language": language})
	print(title)
	g.db.execute("insert into entries(title, text, options, created_at, author) values (?, ?, ?, ?, ?)",
					title, text, options, datetime.now(), author)
	lastid = g.db.execute("select @@IDENTITY").fetchone()[0]
	hashUrl = hashids.encode(lastid)
	g.db.execute("update entries set urlHash=? where id=?", hashUrl, lastid)
	g.db.commit()

	return redirect(url_for("show_entry", pasteid=hashUrl))

@app.route("/<pasteid>")
def show_entry(pasteid):
	row = g.db.execute("select COALESCE(title, 'Untitled') as title, text, options, created_at, COALESCE(author, 'Anonymous') as author from entries where urlHash=?", pasteid).fetchone()
	if row is None:
		abort(404)
	options = { "title": row.title, "pasteValue": row.text,
				"createdAt": row.created_at.isoformat(), "author": row.author,
				"readOnly": "true", "supportedModes": app.config["SUPPORTED_MODES"],
				"capwords": capitalize}
	storedOptions = json.loads(row.options)
	storedOptions.update(options)
	return render_template("show.html", **storedOptions)
