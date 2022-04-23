from flask import Blueprint, make_response, request
import json
from app.utils import reply, connect
import bcrypt
import base64
import app.friend.helpers as friend_helpers

bp = Blueprint('profile', __name__)

@bp.route("/<user_id>", methods=["GET"])
def get_profile(user_id):
    (cur, conn) = connect()
    cur.execute("""
        SELECT pf.user_id, pf.username, pf.name, pf.birthday
        FROM Profile as pf
        WHERE pf.user_id = %s
        ;
    """, (int(user_id),))
    profile = cur.fetchone()
    # if profile["profile_picture"] is not None:
    #     profile["profile_picture"] = base64.b64encode(profile["profile_picture"]).decode()

    return json.dumps(profile, default=str)

@bp.route("/<user_id>/picture", methods=["GET"])
def get_profile_picture(user_id):
    try:
        (cur, conn) = connect()
        cur.execute("""
            SELECT pf.profile_picture, pf.is_jpeg
            FROM Profile as pf
            WHERE pf.user_id = %s
            ;
        """, (int(user_id),))
        profile = cur.fetchone()
        if profile["profile_picture"] is not None:
            profile["profile_picture"] = profile["profile_picture"].tobytes()

        response = make_response(profile["profile_picture"])
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename=f'{user_id}.png')
        if profile["is_jpeg"] == 1:
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set(
                'Content-Disposition', 'attachment', filename=f'{user_id}.jpeg')
        return response
    except:
        return make_response("Profile picture does not exist.", 404)
        

@bp.route("", methods=["POST"])
def create_profile():
    data = request.json
    pw = data["pw_hash"]
    is_jpeg = data["isJpeg"]

    profile_picture = None
    pf = None
    try:
        pf = data["profile_picture"]
        profile_picture = base64.b64decode(pf)
    except:
        pf = None
        profile_picture = None

    
    hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    (cur, conn) = connect()

    try:    
        cur.execute("""
            INSERT INTO Profile (username, name, pw_hash, is_jpeg, profile_picture)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
            ;
        """, (data["username"], data["name"], hashed_pw, 1 if is_jpeg else 0, profile_picture))
        user_id = cur.fetchone()
        conn.commit()
        return reply(user_id)
    except:
        return make_response("Username is already taken.", 400)

@bp.route("", methods=["PUT"])
def update_profile():
    cookie_user = int(request.cookies.get("user_id"))
    data = request.json
    username = data["username"]
    name = data["name"]
    birthday = data["birthday"]
    is_jpeg = data["isJpeg"]
    
    (cur, conn) = connect()
    profile_picture = None
    pf = None
    try:
        pf = data["profile_picture"]
        if pf == "keep":
            cur.execute("""
                UPDATE Profile
                SET username = %s, name = %s, birthday = %s
                WHERE user_id = %s
            """, (username, name, birthday, cookie_user))
            conn.commit()
            return reply(True)
        profile_picture = base64.b64decode(pf)
    except:
        pf = None
        profile_picture = None

    (cur, conn) = connect()
    cur.execute("""
        UPDATE Profile
        SET username = %s, name = %s, birthday = %s, profile_picture = %s, is_jpeg = %s
        WHERE user_id = %s
    """, (username, name, birthday, profile_picture, 1 if is_jpeg else 0, cookie_user))
    conn.commit()
    
    return reply(True)

@bp.route("/password", methods=["PUT"])
def update_password():
    cookie_user = int(request.cookies.get("user_id"))
    data = request.json
    password = data["password"]
    newPassword = data["newPassword"]
    (cur, conn) = connect()
    cur.execute("""
        SELECT pf.pw_hash
        FROM Profile as pf
        WHERE pf.user_id = %s
        ;
    """, (int(cookie_user),))
    profile = cur.fetchone()

    if not bcrypt.checkpw(password.encode(), bytes(profile["pw_hash"])):
        return make_response("The password you entered does not match your current password.", 401)

    hashed_pw = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())
    print(hashed_pw)
    cur.execute("""
        UPDATE Profile
        SET pw_hash = %s
        WHERE user_id = %s
    """, (hashed_pw, cookie_user))
    conn.commit()
    
    return reply(True)

@bp.route("", methods=["DELETE"])
def delete_profile():
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        DELETE FROM Profile
        WHERE user_id = %s
    """, (cookie_user,))
    conn.commit()

    return reply(True)

@bp.route("/<user_id>/feed", methods=["GET"])
def get_profile_feed(user_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        SELECT friender_id, friendee_id
        FROM Friend
        WHERE (friender_id = %s AND friendee_id = %s) OR (friendee_id = %s AND friender_id = %s)
        ;
    """, (user_id, cookie_user, user_id, cookie_user))
    friendship = cur.fetchone()
    if cookie_user != int(user_id) and friendship is None:
        return make_response("You are not authorized to view this user's feed.", 401)

    cur.execute("""
        SELECT message_id, sender_id, pf.username, pf.name, content, timestamp
        FROM ConversationMessage as cm
        JOIN Profile AS pf ON pf.user_id = cm.sender_id
        WHERE cm.isfeedmessage = 1 AND cm.sender_id = %s
        ;
    """, (int(user_id),))
    feed = cur.fetchall()

    return json.dumps(feed, default=str)

@bp.route("/feed/all", methods=["GET"])
def get_all_friend_feeds():
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()

    cur.execute("""
        (SELECT message_id, sender_id, pf.username, pf.name, content, timestamp
        FROM ConversationMessage as cm
        JOIN Profile AS pf ON pf.user_id = cm.sender_id
        WHERE cm.isfeedmessage = 1 AND cm.sender_id IN (
            SELECT friender_id
            FROM Friend
            WHERE friendee_id = %s
        ))
        UNION
        (SELECT message_id, sender_id, pf.username, pf.name, content, timestamp
        FROM ConversationMessage as cm
        JOIN Profile AS pf ON pf.user_id = cm.sender_id
        WHERE cm.isfeedmessage = 1 AND cm.sender_id IN (
            SELECT friendee_id
            FROM Friend
            WHERE friender_id = %s
        ))
        ORDER BY timestamp
    """, (cookie_user,))
    messages = cur.fetchall()

    return make_response(json.dumps(messages, default=str))

@bp.route("/feed/post", methods=["POST"])
def post_to_feed():
    cookie_user = int(request.cookies.get("user_id"))
    content = request.json["content"]
    (cur, conn) = connect()

    cur.execute("""
        INSERT INTO ConversationMessage (isfeedmessage, sender_id, content)
        VALUES (1, %s, %s)
        RETURNING message_id
    """, (cookie_user, content))
    message_id = cur.fetchall()
    conn.commit()

    return make_response(json.dumps(message_id, default=str))

@bp.route("/feed/<message_id>", methods=["DELETE"])
def delete_feed_message(message_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()

    cur.execute("""
        DELETE FROM ConversationMessage
        WHERE message_id = %s AND isFeedMessage = 1 AND sender_id = %s
    """, (int(message_id), cookie_user))
    rowcount = cur.rowcount
    if rowcount == 0:
        return make_response("There was an error deleting the indicated message. Either it does not exist, or you are not authorized to delete it.", 401)

    conn.commit()

    return reply(True)
