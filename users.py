from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request, abort
from db import db
from sqlalchemy.sql import text

def login(name, password):
    print("täällä")
    sql=text("SELECT id, password FROM users WHERE name=:name")
    result=db.session.execute(sql, {"name":name})
    user=result.fetchone()
    print(user)
    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False
    session["user_id"]=user[0]
    session["name"]=name
    return True

def user_id():
    return session.get("name", 0)

def logout():
    del session["user_id"]
    del session["name"]

def register(name, password):
    hash_value=generate_password_hash(password)
    try:
        print("täs")
        sql=text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        print("me")
        return True
    except:
        return False

def check_csrf():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)