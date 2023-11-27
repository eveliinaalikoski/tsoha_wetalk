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
				if users.login(name, password1):
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
		group_name=request.form["group_name"]
		create=groups.create_group(group_name)
		if create:
			return redirect("/front_page")
		return render_template("error.html", message="Creating group failed")
        
@app.route("/join", methods=["POST", "GET"])
def join():
	group=request.form["group_name"]
	group=groups.get_group(group)
	add=groups.add_to_group(group, session["user_id"])
	if add:
		return render_template("join.html", group=group)
	return render_template("error.html", message="Couldn't join group")

@app.route("/group_page/<group_id>/", methods=["POST", "GET"])
def group_page(group_id):
	group_name=groups.get_group_name(group_id)
	list=messages.get_list(group_id)
	return render_template("group_page.html", 
						count=len(list), 
						messages=list, 
						group_name=group_name, 
						group_id=group_id)

@app.route("/send/<group_id>/", methods=["POST", "GET"])
def send(group_id):
	if request.method=="GET":
		group_name=groups.get_group_name(group_id)
		return render_template("send.html", group_name=group_name)
	if request.method=="POST":
		user_id=session["user_id"]
		group_name=groups.get_group_name(group_id)
		#conv.id=
		message=request.form["message"]
		if messages.send(user_id, group_id, message):
			return redirect("/sent")
		return render_template("error.html", message="Error sending message")

@app.route("/sent", methods=["POST", "GET"])
def sent():
	message=request.form["message"]
	return render_template("sent.html", message=message)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")