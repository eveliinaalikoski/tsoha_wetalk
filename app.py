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

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method=="GET":
		return render_template("login.html")
	if request.method=="POST":
		username=request.form["username"]
		password=request.form["password"]
		if users.login(username, password):
			return redirect("/front_page")
		return render_template("error.html", message="Wrong username or password")

@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method=="GET":
		return render_template("register.html")
	if request.method=="POST":
		username=request.form["username"]
		password1=request.form["password1"]
		password2=request.form["password2"]
		if password1!=password2:
			return render_template("error.html", message="Passwords differ")
		if users.register(username, password1):
			return redirect("/front_page")
		return render_template("error.html", message="Registeration failed")
	
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

@app.route("/group_page", methods=["POST", "GET"])
def group():
	group_name="test"
	list=messages.get_list()
	return render_template("group_page.html", count=len(list), messages=list, group_name=group_name)

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method=="GET":
		return render_template("send.html")
	if request.method=="POST":
		content=request.form["content"]
		if messages.send(content):
			return redirect("/group_page")
		return render_template("error.html", message="Error sending message")