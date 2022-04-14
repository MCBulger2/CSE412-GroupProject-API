from flask import Blueprint, request, make_response
import json
from app.utils import reply, connect
import friend.helpers as helpers

bp = Blueprint('friend', __name__)        

@bp.route("/friender", methods=["GET"])
def get_friender():
    cookie_user = request.cookies.get("user_id")
    (cur, conn) = connect()
    cur.execute("""
        SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
        FROM Friend AS fr
        JOIN Profile AS pf ON pf.user_id = fr.friendee_id
        WHERE fr.friender_id = %s
        ;
    """, (cookie_user,))
    friends = cur.fetchall()

    return make_response(json.dumps(friends, default=str))

@bp.route("/friendee", methods=["GET"])
def get_friendee():
    cookie_user = request.cookies.get("user_id")
    (cur, conn) = connect()
    friends = helpers.get_my_friends(cur, cookie_user)

    return make_response(json.dumps(friends, default=str))

@bp.route("/befriend/<username>", methods=["POST"])
def befriend_user(username):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        INSERT INTO Friend VALUES (%s, (
            SELECT pf.user_id
            FROM Profile AS pf
            WHERE pf.username = '%s'
            LIMIT 1
        ))
        ;
    """ %(cookie_user, username))
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
    conn.commit()

    return reply(True)
