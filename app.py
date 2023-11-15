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
	if request.method=="GET":
		return render_template("login.html")
	if request.method=="POST":
		username=request.form["username"]
		password=request.form["password"]
		if users.login(username, password):
			return redirect("/front_page")
		return render_template("error.html", message="Wrong username or password")

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

@app.route("/group", methods=["POST", "GET"])
def group():
	list=messages.get_list()
	return render_template("group_page.html", count=len(list), messages=list)

@app.route("/send", methods=["POST", "GET"])
def send():
	content=request.form["content"]
	if messages.send(content):
		return redirect("/front_page")
	return render_template("error.html", message="Error sending message")