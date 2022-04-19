from flask import Blueprint, request, make_response
import json
from app.utils import reply, connect
import friend.helpers as helpers

bp = Blueprint('friend', __name__)        

# @bp.route("/friender", methods=["GET"])
# def get_friender():
#     cookie_user = request.cookies.get("user_id")
#     (cur, conn) = connect()
#     cur.execute("""
#         SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
#         FROM Friend AS fr
#         JOIN Profile AS pf ON pf.user_id = fr.friendee_id
#         WHERE fr.friender_id = %s
#         ;
#     """, (cookie_user,))
#     friends = cur.fetchall()

#     return make_response(json.dumps(friends, default=str))

@bp.route("", methods=["GET"])
def get_friends():
    cookie_user = request.cookies.get("user_id")
    (cur, conn) = connect()
    friends = helpers.get_my_friends(cur, cookie_user)

    return make_response(json.dumps(friends, default=str))

@bp.route("/pending/in", methods=["GET"])
def get_pending_incoming():
    cookie_user = request.cookies.get("user_id")
    (cur, conn) = connect()
    friends = helpers.get_my_friends(cur, cookie_user, 0)
    cur.execute("""
        SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friender_id
        WHERE fr.friendee_id = %s AND is_accepted = 0
        ;
    """, (cookie_user,))
    friends = cur.fetchall()

    return make_response(json.dumps(friends, default=str))

@bp.route("/pending/out", methods=["GET"])
def get_pending_outgoing():
    cookie_user = request.cookies.get("user_id")
    (cur, conn) = connect()
    cur.execute("""
        SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friendee_id
        WHERE fr.friender_id = %s AND is_accepted = 0
        ;
    """, (cookie_user, ))
    friends = cur.fetchall()

    return make_response(json.dumps(friends, default=str))

@bp.route("/befriend/<username>", methods=["POST"])
def befriend_user(username):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()

    cur.execute("""
        SELECT user_id
        FROM Profile
        WHERE username = %s
    """, (username,))
    me = cur.fetchone()
    if me is not None and me["user_id"] == cookie_user:
        return make_response("You cannot befriend yourself.", 400)
    try:
        friends = helpers.get_my_friends(cur, cookie_user, 0)
        for friend in friends:
            if friend["username"] == username:
                return accept_request(friend["user_id"])

        cur.execute("""
            INSERT INTO Friend VALUES (%s, (
                SELECT pf.user_id
                FROM Profile AS pf
                WHERE pf.username = '%s'
                LIMIT 1
            ), 0)
            ;
        """, (cookie_user, username))
        
        conn.commit()

        return reply(True)
    except:
        return make_response("The provided username does not exist, or you are already friends.", 400)

@bp.route("/accept/<user_id>", methods=["GET"])
def accept_request(user_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        UPDATE Friend as fr
        SET is_accepted = 1
        WHERE fr.friendee_id = %s AND fr.friender_id = %s
        ;
    """, (cookie_user, user_id))
    conn.commit()

    return reply(True)

@bp.route("/defriend/<user_id>", methods=["DELETE"])
def defriend_user(user_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        DELETE FROM Friend
        WHERE friender_id = %s AND friendee_id = %s
        ;
    """, (cookie_user, user_id))
    cur.execute("""
        DELETE FROM Friend
        WHERE friendee_id = %s AND friender_id = %s
        ;
    """, (cookie_user, user_id))
    conn.commit()

    return reply(True)
