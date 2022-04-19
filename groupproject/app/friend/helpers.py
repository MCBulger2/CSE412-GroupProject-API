def get_my_friends(cur, cookie_user, is_accepted = 1):
    cur.execute("""
        (SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friender_id
        WHERE fr.friendee_id = %s AND is_accepted = %s)
        UNION
        (SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friendee_id
        WHERE fr.friender_id = %s AND is_accepted = %s)
        ;
    """, (cookie_user, is_accepted, cookie_user, is_accepted))
    friends = cur.fetchall()
    return friends