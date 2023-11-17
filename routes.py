from app import app
import users, messages
from flask import render_template, request, redirect
from flask import session
import db
from sqlalchemy.sql import text

@app.route("/")
def index():
	return render_template("index.html", message="Welcome!")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method=="GET":
		return render_template("login.html")
	if request.method=="POST":
		name=request.form["name"]
		password=request.form["password"]
		if users.login(name, password):
			return redirect("/front_page")
		return render_template("error.html", message="Wrong name or password")

@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method=="GET":
		return render_template("register.html")
	if request.method=="POST":
		name=request.form["name"]
		password1=request.form["password1"]
		password2=request.form["password2"]
		if len(name)<2 or len(name)>20:
			return render_template("error.html", message="Username has to be 2-20 characters")
		if password1!=password2:
			return render_template("error.html", message="Passwords differ")
		if users.register(name, password1):
			if users.login(name, password1):
				return redirect("/front_page")
		return render_template("error.html", message="Registeration failed")


@app.route("/front_page", methods=["POST", "GET"])
def front_page():
    groups=db.db.session.execute(text("SELECT group_name FROM groups"))
    if request.method=="GET":
        return render_template("front_page.html", groups=groups)
    if request.method=="POST":
        return render_template("front_page.html", groups=groups)

@app.route("/create_group", methods=["POST", "GET"])
def create_group():
    if request.method=="GET":
        return render_template("create_group.html")
    if request.method=="POST":
        group_name=request.form["group_name"]
        create=groups.create_group(group_name)
        if create_group(group_name):
            return redirect("/front_page")
        return render_template("error.html", message="Creating group failed")
        
@app.route("/join/{{ group }}", methods=["POST", "GET"])
def join(group):
	#get
	return render_template("/join.html", group=group)

@app.route("/group_page", methods=["POST", "GET"])
def group_page():
	if request.method=="GET":
		group_name=request.form["group"]
		list=messages.get_list()
		return render_template("group_page.html", count=len(list), messages=list, group_name=group_name)
	if request.method=="POST":
		return redirect("/group_page")

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method=="GET":
		return render_template("send.html")
	if request.method=="POST":
		content=request.form["content"]
		group_name=request.form["group"]
		if messages.send(content):
			return render_template("group_page.html", group_name=group_name)
		return render_template("error.html", message="Error sending message")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")