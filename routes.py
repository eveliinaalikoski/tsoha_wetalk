from app import app
import users, messages, groups, convs
from db import db
from flask import render_template, request, redirect
from flask import session

@app.route("/")
def index():
	group_list=groups.get_groups()
	user=users.user_id()
	user_list=users.get_users(user)
	conv_list=convs.get_convs(user)
	return render_template("index.html", 
						group_list=group_list,
						user_list=user_list,
						conv_list=conv_list)

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

@app.route("/group_list")
def group_list():
	group_list=groups.get_groups()
	return render_template("groups.html", group_list=group_list)

@app.route("/chat_list")
def chat_list():
	if not session["user_id"]:
		return render_template("error.html", message="You have to be signed in to see your chats")
	conv_list=convs.get_convs(session["user_id"])
	return render_template("chats.html", conv_list=conv_list)

@app.route("/user_list")
def user_list():
	user_list=users.get_users(users.user_id())
	return render_template("users.html", user_list=user_list)

@app.route("/create_group", methods=["POST", "GET"])
def create_group():
	if request.method=="GET":
		return render_template("create_group.html")
	if request.method=="POST":
		group_name=request.form["group_name"]
		if len(group_name)<2 or len(group_name)>20:
			return render_template("error.html", message="Groupname has to be 2-20 characters")
		create=groups.create_group(group_name)
		if create:
			return redirect("/")
		return render_template("error.html", message="Creating group failed")

@app.route("/join/<group_id>/", methods=["POST", "GET"])
def join(group_id):
	group_name=groups.get_group_name(group_id)
	add=groups.add_to_group(group_name, session["user_id"])
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

@app.route("/group_send/<group_id>/", methods=["POST", "GET"])
def group_send(group_id):
	member=groups.is_member(session["user_id"], group_id)
	if not member:
		return render_template("error.html", message="You are not a member of this group")
	if request.method=="GET":
		group_name=groups.get_group_name(group_id)
		return render_template("group_send.html", 
						 group_name=group_name, 
						 group_id=group_id)
	message=request.form["message"]
	if len(message)<2 or len(message)>200:
		return render_template("error.html", message="Message must be 2-200 characters long")
	user_id=session["user_id"]
	group_name=groups.get_group_name(group_id)
	if messages.send(user_id, group_id, message):
		return redirect("/group_page/" + group_id + "/")
	return render_template("error.html", message="Error sending message")

@app.route("/group_users/<group_id>/")
def group_users(group_id):
	member=groups.is_member(session["user_id"], group_id)
	user_list=users.get_users(session["user_id"])
	group_name=groups.get_group_name(group_id)
	return render_template("group_users.html",
						group_id=group_id, 
						member=member,
						user_list=user_list,
						group_name=group_name)

@app.route("/create_conv/<user_id>/")
def create_conv(user_id):
	if convs.get_conv_id(session["user_id"], user_id) is not False:
		return render_template("error.html", message="""You already have a chat 
						 with this user""")
	create=convs.create(session["user_id"], user_id)
	conv_id=convs.get_conv_id(session["user_id"], user_id)
	if create:
		return redirect("/conv/" + str(conv_id) + "/")
	return render_template("error.html", message="Couldn't create conversation")

@app.route("/conv/<conv_id>/")
def conv(conv_id):
	conv_users=convs.get_users(conv_id)
	if conv_users[0]==session["user_id"]:
		user=users.get_name(conv_users[1])
	elif conv_users[1]==session["user_id"]:
		user=users.get_name(conv_users[0])
	else:
		return render_template("error.html", message="You are not a member of this chat")
	messages=convs.get_messages(conv_id)
	return render_template("conv.html", 
						conv_id=conv_id,
						user=user, 
						messages=messages,
						count=len(messages))

@app.route("/user_send/<conv_id>/", methods=["POST", "GET"])
def user_send(conv_id):
	if request.method=="GET":
		conv_users=convs.get_users(conv_id)
		if conv_users[0]==session["user_id"]:
			user=users.get_name(conv_users[1])
			user_id=conv_users[1]
		else:
			user=users.get_name(conv_users[0])
			user_id=conv_users[0]
		return render_template("user_send.html",
						 user=user,
						 user_id=user_id,
						 conv_id=conv_id)
	message=request.form["message"]
	if len(message)<2 or len(message)>200:
		return render_template("error.html", message="Message must be 2-200 characters long")
	if convs.send(session["user_id"], conv_id, message):
		return redirect("/conv/" + conv_id + "/")
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
	delete=groups.delete_group(group_id)
	if delete:
		return redirect("/")
	return render_template("error.html", message="Error deleting a group")	

@app.route("/user/<user_id>/")
def user(user_id):
	name=users.get_name(user_id)
	conv_id=convs.get_conv_id(session["user_id"], user_id)
	group_list=groups.get_group_by_user(user_id)
	return render_template("user.html", 
						user_id=user_id,
						name=name,
						conv_id=conv_id,
						group_list=group_list)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/profile")