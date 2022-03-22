
def get_conversations(cur, user_id):
    cur.execute("""
        SELECT co.conversation_id, co.name
        FROM Conversation AS co
        JOIN ConversationUsers AS cu ON co.conversation_id = cu.conversation_id
        WHERE cu.user_id = %s
        ;
    """, (user_id,))
    conversations = cur.fetchall()
    return conversations