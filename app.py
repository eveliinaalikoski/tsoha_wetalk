from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///alev"
db=SQLAlchemy(app)

@app.route("/")
def index():
	return render_template("index.html", message="Welcome!")

@app.route("/login", methods=["POST"])
def login():
	return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
	return render_template("register.html")
	
@app.route("/front_page", methods=["POST", "GET"])
def front_page():
	username=request.form["username"]
	return render_template("front_page.html", username=username)
