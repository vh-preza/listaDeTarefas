import sqlite3
import json
from flask import Flask, render_template, request, session, redirect, flash
from helpers import hash_password, verify_password

app = Flask(__name__)

with open("./static/config.json") as file:
    config = json.load(file)

app.secret_key = config.get("secret_key")

connection = sqlite3.connect("./static/users.db", check_same_thread=False)
db = connection.cursor()

db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, activity TEXT NOT NULL, username TEXT NOT NULL, is_checked INTEGER NOT NULL, FOREIGN KEY (username) REFERENCES users (username))")
db.execute("CREATE INDEX IF NOT EXISTS index_username ON items (username)")

@app.route("/")
def index():
    if "username" not in session:
        return render_template("login.html")
    
    items = db.execute("SELECT id, activity, is_checked FROM items WHERE username = ?", (session["username"],)).fetchall()
    
    return render_template("index.html", items=items)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="Username and Password fields cannot be empty.")
        
        try:
            result = db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()

            if result:
                hashed_password = result[0]
            else:
                return render_template("login.html", error="Username does not exist.")

            if not verify_password(password, hashed_password):
                return render_template("login.html", error="Password is incorrect.")
            
            session["username"] = username
        except:
            return render_template("login.html", error="An error occurred, try again.")
        
        return redirect("/")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return render_template("register.html", error="Username and Password fields cannot be empty.")

        if password != confirmation:
            return render_template("register.html", error="Password must match its confirmation.")
        
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
            session["username"] = username
        except:
            return render_template("register.html", error="An error occurred, try again.")

        return redirect("/")
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        task = request.form.get("task")

        if not task:
            flash("Cannot add empty task field")
            return redirect("/")
        
        try:
            db.execute("INSERT INTO items (activity, username, is_checked) VALUES (?, ?, 0)", (task, session["username"]))
        except:
            flash("An error occurred while trying to add the task, try again")

    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        data = request.get_json()

        if not data:
            flash("Unable to get data")
            return redirect("/")

        if "text" in data:
            text = data.get("text")
            if not text:
                flash("Text field cannot be empty")
                return redirect("/")
            
            try:
                db.execute("UPDATE items SET activity = ? WHERE id = ?", (text, id))
            except:
                flash("An error occurred while trying to update the task, try again")
        else:
            checked = data.get("checked")
            
            try:
                db.execute("UPDATE items SET is_checked = ? WHERE id = ?", (checked, id))
            except:
                flash("An error occurred while trying to update the task, try again")
    
    return redirect("/")

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        try:
            db.execute("DELETE FROM items WHERE id = ? AND username = ?", (id, session["username"]))
        except:
            flash("An error occurred while trying to delete the task, try again")
        
    return redirect("/")