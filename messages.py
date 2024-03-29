from db import db
from flask import session, request, abort
from sqlalchemy.sql import text

def get_list(group_id):
    sql = text("""SELECT U.name, M.message, M.sent_at, M.id
               FROM users U, messages M, groups G 
               WHERE G.id=:gid
               AND M.group_id=G.id 
               AND U.id=M.user_id 
               ORDER BY M.id""")
    result = db.session.execute(sql, {"gid":group_id}).fetchall()
    return result

def send(user_id, group_id, message):
    try:
        sql=text("""INSERT INTO messages 
                 (user_id, group_id, message, sent_at) 
                 VALUES 
                 (:user_id, :group_id, :message, NOW())""")
        db.session.execute(sql, {"user_id":user_id, "group_id":group_id, "message":message})
        db.session.commit()
        return True
    except:
        return False

def delete(message_id):
    try:
        sql=text("DELETE FROM messages WHERE id=:message_id")
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()
        return True
    except:
        return False

def group_id(message_id):
    sql = text("SELECT group_id FROM messages WHERE id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    return str(result[0])