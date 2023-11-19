from app import app
import users, messages, groups
from flask import render_template, request, redirect
from db import db
from flask import session

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
		register=users.register(name, password1)
		if register:
				if login(name, password1):
					print("jep")
					return redirect("/front_page")
		if not register:
			return render_template("error.html", message="The username is taken")
		return render_template("error.html", message="Registeration failed")


@app.route("/front_page", methods=["POST", "GET"])
def front_page():
	group_list=groups.get_groups()
	return render_template("front_page.html", group_list=group_list)

@app.route("/create_group", methods=["POST", "GET"])
def create_group():
	if request.method=="GET":
		return render_template("create_group.html")
	if request.method=="POST":
		print("w")
		group_name=request.form["group_name"]
		create=groups.create_group(group_name)
		if create:
			return redirect("/front_page")
		return render_template("error.html", message="Creating group failed")
        
@app.route("/join", methods=["POST", "GET"])
def join():
	group=request.form["group_name"]
	print(group)
	group=groups.get_group(group)
	print(group)
	user_id=session["user_id"]
	print(1, user_id)
	add=groups.add_to_group(group, user_id)
	print(add)
	if add:
		return render_template("join.html", group=group)
	return render_template("error.html", message="Couldn't join group")

@app.route("/group_page", methods=["POST", "GET"])
def group_page():
	group_name=session["group"]
	print(group_name)
	group_id=groups.get_group_id(group_name)
	list=messages.get_list(group_id)
	return render_template("group_page.html", count=len(list), messages=list, group_name=group_name)

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method=="GET":
		return render_template("send.html")
	if request.method=="POST":
		user_id=session["user_id"]
		# conv.id=
		group_id=groups.get_group_id(session["group"])
		message=request.form["message"]
		if messages.send(user_id, group_id, message):
			return render_template("sent.html", group_name=session["group"])
		return render_template("error.html", message="Error sending message")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")