from db import db
from flask import session, request, abort
from sqlalchemy.sql import text

def get_convs(user_id):
    sql=text("""SELECT id FROM conversations 
             WHERE user_id1=:user_id 
             OR user_id2=:user_id""")
    convs=db.session.execute(sql, {"user_id":user_id})
    return convs.fetchall()

def create(user_id1, user_id2):
    try:
        sql=text("""INSERT INTO conversations (user_id1, user_id2) 
                 VALUES (:user_id1, :user_id2)""")
        db.session.execute(sql, {"user_id1":user_id1, "user_id2":user_id2})
        db.session.commit()
        return True
    except:
        return False

def get_conv_id(user_id1, user_id2):
    sql=text("""SELECT id FROM conversations 
             WHERE (user_id1=:user_id1 AND user_id2=:user_id2) 
             OR (user_id1=:user_id2 AND user_id2=:user_id1)""")
    id=db.session.execute(sql, {"user_id1":user_id1, "user_id2":user_id2}).fetchone()
    if id:
        return id[0]
    return False

def get_users(conv_id):
    sql=text("""SELECT user_id1, user_id2 
             FROM conversations
             WHERE id=:conv_id""")
    users=db.session.execute(sql, {"conv_id":conv_id}).fetchone()
    print("users", users)
    if users:
        return users
    return False

def get_messages(conv_id):
    sql=text("""SELECT U.name, M.message, M.sent_at, M.id
             FROM messages M, users U, conversations C
             WHERE C.id=:cid
             AND M.conv_id=C.id
             AND U.id=M.user_id
             ORDER BY M.id""")
    list=db.session.execute(sql, {"cid":conv_id}).fetchall()
    return list

def send(user_id, conv_id, message):
    try:
        sql=text("""INSERT INTO messages 
                 (user_id, conv_id, message, sent_at) 
                 VALUES 
                 (:user_id, :conv_id, :message, NOW())""")
        db.session.execute(sql, {"user_id":user_id, "conv_id":conv_id, "message":message})
        db.session.commit()
        return True
    except:
        return False