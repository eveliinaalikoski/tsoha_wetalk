from db import db
from flask import session, request, abort
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT M.message, U.username, M.sent_at FROM messages M, users U" \
        "WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    print(result.fetchall())
    return result.fetchall()

def send(user_id, group_id, content):
    try:
        sql=text("INSERT INTO messages (user_id, group_id, content, sent_at) VALUES (:content, :user_id, NOW())")
        db.session.execute(sql, {"user_id":user_id, "group_id":group_id, "content":content})
        db.session.commit()
        return True
    except:
        return False