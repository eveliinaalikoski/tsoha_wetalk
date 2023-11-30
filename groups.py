from flask import session, request, abort
from db import db
from sqlalchemy.sql import text

def get_group_name(group_id):
    sql=text("SELECT group_name FROM groups WHERE id=:id")
    result=db.session.execute(sql, {"id":group_id}).fetchone()
    if result:
        return result[0]
    return False

def get_group_id(group_name):
    sql=text("SELECT id FROM groups WHERE group_name=:group_name")
    result=db.session.execute(sql, {"group_name":group_name}).fetchone()
    if result:
        return result[0]
    return False

def create_group(group_name):
   try:
        sql=text("INSERT INTO groups (group_name) VALUES (:group_name)")
        db.session.execute(sql, {"group_name":group_name})
        db.session.commit()
        add=add_to_group(group_name, session["user_id"])
        admin=add_admin(group_name, session["user_id"])
        if add and admin:
            return True
   except:
        return False

def get_groups():
    groups=db.session.execute(text("SELECT id, group_name FROM groups;"))
    return groups.fetchall()

def add_to_group(group_name, user_id):
    try:
        group_id=get_group_id(group_name)
        sql=text("INSERT INTO users_groups (group_id, user_id) VALUES (:group_id, :user_id);")
        db.session.execute(sql, {"group_id":group_id, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def add_admin(group_name, user_id):
    try:
        group_id=get_group_id(group_name)
        sql=text("INSERT INTO admins (user_id, group_id) VALUES (:user_id, :group_id);")
        db.session.execute(sql, {"user_id":user_id, "group_id":group_id})
        db.session.commit()
        return True
    except:
        return False

def is_admin(user_id, group_id):
    sql=text("SELECT user_id FROM admins WHERE group_id=:group_id")
    admin=db.session.execute(sql, {"group_id":group_id}).fetchone()
    if admin and admin[0]==user_id:
        return True
    return False

def is_member(user_id, group_id):
    sql=text("SELECT user_id FROM users_groups WHERE group_id=:group_id")
    members=db.session.execute(sql, {"group_id":group_id}).fetchall()
    if members:
        list=[]
        for i in members:
            list.append(i[0])
    else:
        return False
    if user_id in list:
        return True
    return False