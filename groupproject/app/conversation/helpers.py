
def get_conversations(cur, user_id):
    cur.execute("""
        SELECT cv.conversation_id, cv.name, cv.last_message
        FROM ConversationView AS cv
        JOIN ConversationUsers AS cu ON cv.conversation_id = cu.conversation_id
        WHERE cu.user_id = %s
        ;
    """, (user_id,))
    conversations = cur.fetchall()
    result = conversations

    print(conversations)
    for conversation in conversations:
        cur.execute("""
            SELECT pf.user_id, pf.username, pf.name, pf.birthday, cu.read_receipt
            FROM ConversationUsers AS cu
            JOIN Profile as pf ON cu.user_id = pf.user_id
            WHERE cu.conversation_id = %s
            ;
        """, (conversation["conversation_id"],))
        users = cur.fetchall()

        last_read_message = None
        for user in users:
            if user["user_id"] == user_id:
                last_read_message = user["read_receipt"]

        print(last_read_message)
        print(conversation["last_message"] )
        conversation["users"] = users
        conversation["unread"] = False
        if last_read_message is None or conversation["last_message"] is None or conversation["last_message"] > last_read_message:
                conversation["unread"] = True
        print(conversation["unread"])
        

    return conversations