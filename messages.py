from db import db
from flask import session, request, abort
from sqlalchemy.sql import text

def get_list(group_id):
    sql = text("""SELECT U.name, M.message, M.sent_at 
               FROM users U, messages M, groups G 
               WHERE M.group_id=G.id 
               AND U.id=M.user_id 
               ORDER BY M.id""")
    result = db.session.execute(sql, {"G.id":group_id}).fetchall()
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