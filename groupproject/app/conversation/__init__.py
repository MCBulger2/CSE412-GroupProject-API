from flask import Blueprint, request, make_response
import json
from app.utils import reply, connect
import conversation.helpers as helpers

bp = Blueprint('conversation', __name__)

@bp.route("/all", methods=["GET"])
def get_conversations():
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    conversations = helpers.get_conversations(cur, cookie_user)
    return reply(conversations)
    
@bp.route("/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    try:
        cookie_user = int(request.cookies.get("user_id"))
        print(cookie_user)
        (cur, conn) = connect()
        cur.execute("""
            SELECT *
            FROM Conversation AS co
            WHERE co.conversation_id = %s
            ;
        """ %(conversation_id))
        conversation = cur.fetchone()

        cur.execute("""
            SELECT pf.user_id, pf.username, pf.name, pf.birthday, pf.profile_picture
            FROM Conversation AS co
            JOIN ConversationUsers AS cu ON co.conversation_id = cu.conversation_id
            JOIN Profile AS pf ON cu.user_id = pf.user_id
            WHERE co.conversation_id = %s
            ;
        """ %(conversation_id))
        conversation_users = cur.fetchall()
        conversation["users"] = conversation_users

        if all(cookie_user != user["user_id"] for user in conversation_users):
            return make_response(json.dumps("You do not have access to view this conversation."), 401)

        cur.execute("""
            SELECT cm.message_id, cm.content, cm.timestamp, cm.sender_id, pf.username, pf.name
            FROM Conversation AS co
            JOIN ConversationMessage AS cm ON co.conversation_id = cm.conversation_id
            JOIN Profile AS pf ON cm.sender_id = pf.user_id
            WHERE co.conversation_id = %s
            ORDER BY cm.timestamp
            ;
        """, (conversation_id,))
        conversation_messages = cur.fetchall()
        conversation["messages"] = conversation_messages

        return json.dumps(conversation, default=str)
    except:
        return make_response(json.dumps("This conversation does not exist."), 404)
        

@bp.route("", methods=["POST"])
def create_conversation():
    cookie_user = int(request.cookies.get("user_id"))
    name = request.json["name"]
    users = request.json["users"]
    (cur, conn) = connect()
    cur.execute("""
        INSERT INTO Conversation (name)
        VALUES (%s)
        RETURNING conversation_id
        ;
    """, (name,))
    res = cur.fetchone()
    conversation_id = res["conversation_id"]
    print(conversation_id)

    if (cookie_user in users):
        return make_response("Error", 400)

    for user_id in users + [cookie_user]:
        print(user_id)
        print(conversation_id)
        cur.execute("""
            INSERT INTO ConversationUsers (conversation_id, user_id)
            VALUES (%s, %s)
        """, (conversation_id, user_id))

    conn.commit()

    return make_response(res)

@bp.route("", methods=["PUT"])
def update_conversation_name():
    data = request.json
    conversation_id = data["conversation_id"]
    name = data["name"]
    (cur, conn) = connect()

    cur.execute("""
        UPDATE Conversation
        SET name = %s
        WHERE conversation_id = %s
    """, (name, conversation_id))
    conn.commit()

    return make_response(json.dumps(True))

@bp.route("/<conversation_id>/adduser/<user_id>", methods=["POST"])
def add_user_to_conversation(conversation_id, user_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        INSERT INTO ConversationUsers
        VALUES (%s, %s)
    """, (conversation_id, user_id))
    conn.commit()

    return make_response(json.dumps(True))

@bp.route("/<conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    cookie_user = int(request.cookies.get("user_id"))
    (cur, conn) = connect()
    cur.execute("""
        DELETE FROM Conversation
        WHERE conversation_id IN (
            SELECT conversation_id
            FROM ConversationUsers AS cu
            WHERE cu.user_id = %s AND cu.conversation_id = %s
        )
    """, (cookie_user, conversation_id))
    conn.commit()

    return reply(True)

@bp.route("/send", methods=["POST"])
def send_message():
    cookie_user = int(request.cookies.get("user_id"))
    conversation_id = request.json["conversation_id"]
    content = request.json["content"]
    (cur, conn) = connect()

    conversations = helpers.get_conversations(cur, cookie_user)
    if not any(conversation_id == conversation["conversation_id"] for conversation in conversations):
        return make_response("The conversation does not exist, or you are not allowed to send a message in this conversation.", 401)
    
    cur.execute("""
        INSERT INTO ConversationMessage (isfeedmessage, content, sender_id, conversation_id)
        VALUES (0, %s, %s, %s)
        RETURNING message_id
        ;
    """, (content, cookie_user, conversation_id))
    message_id = cur.fetchone()
    conn.commit()

    return make_response(message_id)

