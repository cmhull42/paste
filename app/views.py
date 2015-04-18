from app import app
from flask import request, session, g, redirect, url_for, \
abort, render_template, flash
from string import capwords as capitalize
@app.route('/')
def show_entries():
	cur = g.db.execute("select title, text from entries order by id desc")
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template("show_entries.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
	if not session.get("logged_in"):
		abort(401)
	g.db.execute("insert into entries (title, text) values (?, ?)",
		[request.form["title"], request.form["text"]])

	g.db.commit()
	flash("New entry was successfully posted")
	return redirect(url_for("show_entries"))

@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		if request.form["username"] == app.config["USERNAME"] \
		and request.form["password"] == app.config["PASSWORD"]:
			session["logged_in"] = True
			flash("You were logged in")
			return redirect(url_for("show_entries"))
		else:
			error = "Invalid login"
	return render_template("login.html", error=error)

@app.route("/logout")
def logout():
	session.pop("logged_in", None)
	flash("You were logged out")
	return redirect(url_for("show_entries"))

@app.route("/edit")
def edit():
	defaults = {"defaultMode": "python",
				"lineNumbers": "true",
				"supportedModes": ["javascript", "python", "ruby"],
				"capwords": capitalize}
	return render_template("edit.html", **defaults)
