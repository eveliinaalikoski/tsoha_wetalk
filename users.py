from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request, abort
from db import db
from sqlalchemy.sql import text

def login(name, password):
    sql=text("SELECT id, password FROM users WHERE name=:name")
    result=db.session.execute(sql, {"name":name})
    user=result.fetchone()
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
        sql=text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def get_users(user_id):
    sql=text("SELECT id, name FROM users WHERE id<>:user_id;")
    users=db.session.execute(sql, {"user_id":user_id})
    return users.fetchall()

def get_name(user_id):
    sql=text("SELECT name FROM users WHERE id=:id")
    user=db.session.execute(sql, {"id":user_id}).fetchone()
    if user:
        return user[0]
    return False


def check_csrf():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)