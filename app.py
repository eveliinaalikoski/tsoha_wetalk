from os import getenv
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///alev"
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db=SQLAlchemy(app)

@app.route("/")
def index():
	return render_template("index.html", message="Welcome!")

@app.route("/login", methods=["POST"])
def login():
	# username=request.form["username"]
	# sql="INSERT INTO users (username, password) VALUES (:username, NOW()) RETURNING id"
	# db.session.execute(sql, {"username":username})
	# db.session.commit()
	return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
	return render_template("register.html")
	
@app.route("/front_page", methods=["POST", "GET"])
def front_page():
	username="testi" #request.form["username"]
	groups=["1", "2", "3"] #db.session.execute(text("SELECT group_name FROM groups"))
	return render_template("front_page.html",
						username=username,
						groups=groups)

@app.route("/join", methods=["POST", "GET"])
def join():
	group="test"
	return render_template("/join.html", group=group)