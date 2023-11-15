
def get_list():
    sql = "SELECT M.message, U.username, M.sent_at FROM messages M, users U" \
        "WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()
