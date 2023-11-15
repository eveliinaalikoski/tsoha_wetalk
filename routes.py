from app import app
from flask import Flask
from flask import render_template, request, redirect
from sqlalchemy.sql import text
from db import db

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
	groups=db.session.execute(text("SELECT group_name FROM groups"))
	return render_template("front_page.html",
						username=username,
						groups=groups)
