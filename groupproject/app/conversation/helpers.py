
def get_conversations(cur, user_id):
    cur.execute("""
        SELECT co.conversation_id, co.name
        FROM Conversation AS co
        JOIN ConversationUsers AS cu ON co.conversation_id = cu.conversation_id
        WHERE cu.user_id = %s
        ;
    """, (user_id,))
    conversations = cur.fetchall()
    result = conversations

    for conversation in conversations:
        cur.execute("""
            SELECT pf.user_id, pf.username, pf.name, pf.birthday
            FROM ConversationUsers AS cu
            JOIN Profile as pf ON cu.user_id = pf.user_id
            WHERE cu.conversation_id = %s AND cu.user_id <> %s
            ;
        """, (conversation["conversation_id"], user_id))
        users = cur.fetchall()
        conversation["users"] = users

    return conversations