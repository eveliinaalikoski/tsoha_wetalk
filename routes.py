from app import app
import users, messages, groups
from flask import render_template, request, redirect
from db import db
from flask import session

@app.route("/")
def index():
	group_list=groups.get_groups()
	return render_template("index.html", group_list=group_list)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method=="GET":
		return render_template("login.html")
	if request.method=="POST":
		name=request.form["name"]
		password=request.form["password"]
		if users.login(name, password):
			return redirect("/")
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
					return redirect("/")
		if not register:
			return render_template("error.html", message="The username is already taken")
		return render_template("error.html", message="Registeration failed")

@app.route("/create_group", methods=["POST", "GET"])
def create_group():
	if request.method=="GET":
		return render_template("create_group.html")
	if request.method=="POST":
		group_name=request.form["group_name"]
		create=groups.create_group(group_name)
		if create:
			return redirect("/")
		return render_template("error.html", message="Creating group failed")
        
# @app.route("/delete_group/<group_id>/")
# def delete_group(group_id):
# 	# admins can delete groups 
# 	# same for messages!
	

@app.route("/join/<group_id>/", methods=["POST", "GET"])
def join(group_id):
	group_name=groups.get_group_name(group_id)
	add=groups.add_to_group(group_id, session["user_id"])
	if add:
		return render_template("join.html", 
						 group_name=group_name,
						 group_id=group_id)
	return render_template("error.html", message="Couldn't join group")

@app.route("/group_page/<group_id>/", methods=["POST", "GET"])
def group_page(group_id):
	group_name=groups.get_group_name(group_id)
	list=messages.get_list(group_id)
	member=groups.is_member(session["user_id"], group_id)
	admin=groups.is_admin(session["user_id"], group_id)
	return render_template("group_page.html", 
						count=len(list), 
						messages=list, 
						group_name=group_name, 
						group_id=group_id, 
						member=member,
						admin=admin)

@app.route("/send/<group_id>/", methods=["POST", "GET"])
def send(group_id):
	if request.method=="GET":
		group_name=groups.get_group_name(group_id)
		return render_template("send.html", 
						 group_name=group_name, 
						 group_id=group_id)
	message=request.form["message"]
	user_id=session["user_id"]
	group_name=groups.get_group_name(group_id)
	#conv.id=
	message=request.form["message"]
	if messages.send(user_id, group_id, message):
		return redirect("/group_page/" + group_id + "/")
	return render_template("error.html", message="Error sending message")

@app.route("/delete_message/<message_id>/")
def delete_message(message_id):
	group_id=messages.group_id(message_id)
	delete=messages.delete(message_id)
	if delete:
		return redirect("/group_page/" + group_id + "/")
	return render_template("error.html", message="Error deleting message")

@app.route("/delete_group/<group_id>/")
def delete_group(group_id):
	delete=groups.delete(group_id)
	if delete:
		return redirect("/")
	return render_template("error.html", message="Error deleting group")

@app.route("/profile", methods=["POST", "GET"])
def profile():
	# add logout
    return render_template("profile.html")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/profile")