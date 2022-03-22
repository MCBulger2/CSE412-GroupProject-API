def get_my_friends(cur, cookie_user):
    cur.execute("""
        SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friender_id
        WHERE fr.friendee_id = %s
        ;
    """, (cookie_user,))
    friends = cur.fetchall()
    return friends