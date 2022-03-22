from flask import jsonify
import psycopg2
import psycopg2.extras

# connection string is stored outside repo to avoid checking in sensitive info 
connectionPath = "connection.txt"

def reply(response):
    res = jsonify(response)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

def connect():
    with open(connectionPath) as connectionFile:
        db = connectionFile.readline()

    schema = "schema.sql"
    conn = psycopg2.connect(db)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return (cur, conn)