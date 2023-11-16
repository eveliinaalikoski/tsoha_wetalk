from app import app
import users, messages
from flask import render_template, request, redirect

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
	username=request.form["username"]
	groups=db.session.execute(text("SELECT group_name FROM groups"))
	return render_template("front_page.html",
						username=username,
						groups=groups)

@app.route("/create_group", methods=["POST", "GET"])
def create_group():
    if request.method=="GET":
        return render_template("create_group.html")
    if request.method=="POST":
        group_name=request.form["group_name"]
        create=groups.create_group(group_name):
        if create:
            return redirect("/front_page")
        return render_template("error.html", message="Creating group failed")
        
@app.route("/join/{{ group }}", methods=["POST", "GET"])
def join(group):
	return render_template("/join.html", group=group)

@app.route("/group_page", methods=["POST", "GET"])
def group_page():
	if request.method=="GET":
		group_name="test"
		list=["1","2","3","4"] # messages.get_list()
		return render_template("group_page.html", count=len(list), messages=list, group_name=group_name)
	if request.method=="POST":
		return redirect("/group_page")

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method=="GET":
		return render_template("send.html")
	if request.method=="POST":
		content=request.form["content"]
		if messages.send(content):
			return render_template("group_page.html")
		return render_template("error.html", message="Error sending message")