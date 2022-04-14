from flask import Blueprint, request, make_response
import json
from app.utils import reply, connect
import bcrypt

bp = Blueprint('auth', __name__)        

@bp.route("/", methods=["GET"])
def login():
    args = request.args
    username = args.get("username")

    (cur, conn) = connect()
    cur.execute("""
        SELECT pf.user_id, pf.pw_hash
        FROM Profile AS pf
        WHERE pf.username = %s
        ;
    """, (username,))
    user = cur.fetchone()

    pw = args.get("pw_hash")
    try:
        if not bcrypt.checkpw(pw.encode(), bytes(user["pw_hash"])):
            response = make_response("The account does not exist or your password was incorrect.", 401) 
            response.set_cookie("user_id", "")
            return response  
    except:
        response = make_response("Error", 500) 
        response.set_cookie("user_id", "")
        return response

    del user["pw_hash"]

    response = make_response(json.dumps(user, default=str), 200)
    response.set_cookie("user_id", str(user["user_id"]).encode())
    return response

@bp.route("/logout", methods=["GET"])
def logout():
    response = make_response(json.dumps(True, default=str), 200)
    response.set_cookie("user_id", "", expires=0)
    return response