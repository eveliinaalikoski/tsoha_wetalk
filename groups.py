def create_group(group_name):
   try:
        sql="INSERT INTO groups (group_name) VALUES (:group_name)"
        db.session.execute(sql, {"group_name":group_name})
        db.session.commit()
        return True
    except:
        return False

def add_to_group(group_name, username):
    pass