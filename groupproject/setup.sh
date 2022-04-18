# Stop postgresql and delete the existing database
pg_ctl -D ~/cse412groupproject stop
rm -rf ~/cse412groupproject

# Set parameters and initialize new database
export PGPORT=$1
export PGHOST=/tmp
initdb ~/cse412groupproject
pg_ctl -D ~/cse412groupproject -o '-k /tmp' start
createdb cse412groupproject

#  Create the database schema using DDL

psql -U $USER -d cse412groupproject -c "CREATE TABLE Profile (
	user_id SERIAL PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	name TEXT,
	birthday DATE,
	profile_picture BYTEA,
	pw_hash BYTEA NOT NULL
);"
psql -U $USER -d cse412groupproject -c "CREATE TABLE Conversation (
	conversation_id SERIAL PRIMARY KEY,
	name TEXT
);"
psql -U $USER -d cse412groupproject -c "CREATE TABLE ConversationMessage (
	message_id SERIAL PRIMARY KEY,
	content TEXT,
	timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
	isFeedMessage INT NOT NULL DEFAULT 0,
	sender_id INT NOT NULL REFERENCES Profile (user_id) ON DELETE CASCADE,
	conversation_id INT REFERENCES Conversation(conversation_id) ON DELETE CASCADE
);"
psql -U $USER -d cse412groupproject -c "CREATE TABLE ConversationUsers (
	conversation_id INT NOT NULL REFERENCES Conversation ON DELETE CASCADE,
	user_id INT NOT NULL REFERENCES Profile ON DELETE CASCADE,
    read_receipt INT REFERENCES ConversationMessage,
	PRIMARY KEY (conversation_id, user_id)
);"
psql -U $USER -d cse412groupproject -c "CREATE TABLE Friend (
	friender_id INT NOT NULL REFERENCES Profile (user_id) ON DELETE CASCADE,
	friendee_id INT NOT NULL REFERENCES Profile (user_id) ON DELETE CASCADE,
    is_accepted INT NOT NULL DEFAULT 0,
	PRIMARY KEY (friender_id, friendee_id)
);"

psql -U $USER -d cse412groupproject -c "CREATE VIEW ConversationView AS (
    SELECT c.conversation_id, c.name, lt.message_id AS last_message
    FROM Conversation AS c
    FULL OUTER JOIN (
        SELECT cm.conversation_id, MAX(cm.timestamp) as timestamp, MAX(cm.message_id) as message_id
        FROM ConversationMessage AS cm
        GROUP BY cm.conversation_id
    ) AS lt ON lt.conversation_id = c.conversation_id
    ORDER BY lt.timestamp DESC
);"

# Insert synthetic data into the database

psql -U $USER -d cse412groupproject -c "INSERT INTO Profile (username, name, birthday, pw_hash) VALUES 
    ('jdoe', 'John Doe', '2000-11-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('jfletcher', 'Julie Fletcher', '1957-05-22', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('philgil', 'Phil Gilbreath', '1997-06-06', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('_chapa_', 'Gerardo Chapa', '1937-04-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('jcollins', 'Justin Collins', '1963-12-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('valgal', 'Valeria Kester', '2003-02-26', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('joegreene', 'Joseph Greene', '1951-07-26', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('thesanches', 'Louise Sanches', '1951-04-08', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('edgar', 'Edgar Looney', '1961-09-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('valenzuela', 'Hal Valenzuela', '1975-02-10', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('leelee', 'Lee Velasquez', '2002-02-08', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('bbbarker', 'Christina Barker', '1960-05-29', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('ngallo', 'Nicole Gallo', '2000-01-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('spivey', 'Clara Spivey', '1999-02-20', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('hazel', 'Hazel Abney', '1976-10-14', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('leclair_calvin', 'Calvin Leclair', '1983-01-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('blanch', 'Blanch Cox', '1980-03-19', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('mperry', 'Marlene Perry', '1976-10-14', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('phy', 'Phyllis Smyth', '2003-01-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('karen', 'Karen Wilson', '1988-09-08', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('jeff', 'Jeffrey Griggs', '1976-10-14', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('rocco', 'Rocco Brown', '2000-01-01', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('herb', 'Herbert Hall', '1970-12-12', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('larrydaley', 'Larray Daley', '1976-10-14', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('rbrack', 'Robert Brackman', '1990-05-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('julie_m', 'Julie Maltby', '2001-02-20', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('joan', 'Joan Reynolds', '1990-05-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('lucylucy', 'Lucile Park', '1991-06-20', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('lll', 'Laura Fritch', '1998-04-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO'),
    ('cynthia', 'Cynthia Miller', '1981-05-30', '\$2a\$12\$hFEMEP9h5to0FOx..2Vbnu/p3Thq5T9bnUGpr3dc6Vq7woLUXSkXO')
;"

# Friendships
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (1, 2, 1), (2, 1, 1), (1, 3, 1), (3, 1, 1), (2, 3, 1), (3, 2, 1);"      # First 3 users are all friends with each other
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (4, 1, 1), (5, 1, 1), (4, 5, 1), (5, 4, 1);"                      # 4 and 5 are friends with 1 but not vice versa, and friends with each other
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (6, 2, 1), (2, 6, 1), (6, 3, 1), (4, 6, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (7, 6, 1), (6, 7, 1), (7, 5, 1), (5, 7, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (8, 9, 1), (8, 10, 1), (8, 11, 1), (8, 12, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (9, 8, 1), (9, 10, 1), (9, 11, 1), (9, 12, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (10, 11, 1), (10, 8, 1), (10, 9, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (11, 10, 1), (11, 8, 1), (11, 9, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (12, 10, 1), (12, 8, 1), (12, 9, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (30, 29, 1), (29, 30, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (29, 28, 1), (28, 29, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (28, 27, 1), (27, 28, 1);"
psql -U $USER -d cse412groupproject -c "INSERT INTO Friend VALUES (27, 26, 1), (26, 27, 1);"


# Create conversations
psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Group Convo 1');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (1, 1), (1, 2), (1, 3);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('Hello, World!', 1, 1),
    ('Hello, back!', 2, 1),
    ('Same here, hello', 3, 1),
    ('Lets have a very interesting conversation', 1, 1),
    ('indeed', 3, 1),
    ('yes', 2, 1)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 1');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (2, 1), (2, 2);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('No comfort do written conduct at prevent manners on.', 2, 2),
    ('Alone visit use these smart rooms ham. No waiting in on enjoyed placing it inquiry.', 1, 2),
    ('No comfort do written conduct at prevent manners on.', 2, 2),
    ('By in no ecstatic wondered disposal my speaking. Direct wholly valley or uneasy it at really.', 1, 2)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 2');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (3, 7), (2, 5);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('ts sometimes her behaviour are contented. ', 5, 3),
    ('Her companions instrument set estimating sex remarkably solicitude motionless.', 7, 3),
    ('Remain lively hardly needed at do by. ', 7, 3)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 3');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (4, 2), (4, 4);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('This is a private conversation between us', 2, 4),
    ('Sounds good, its just us then', 4, 4)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 4');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (5, 8), (5, 7);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('Same an quit most an. Admitting an mr disposing sportsmen.', 8, 5),
    ('New the her nor case that lady paid read. Invitation friendship travelling eat everything the out two. Shy you who scarcely expenses debating hastened resolved. Always polite moment on is warmth spirit it to hearts. Downs those still witty an balls so chief so. Moment an little remain no up lively no. Way brought may off our regular country towards adapted cheered. ', 7, 5),
    ('Placing assured be', 8, 5),
    ('Far shed each high read are men over day. Afraid we praise', 8, 5),
    ('By an outlived insisted procured improved am. ', 8, 5)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 5');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (6, 30), (6, 29);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('This is a private conversation between us', 30, 6),
    ('Sounds good, its just us then', 29, 6)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 6');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (7, 29), (7, 28);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('This is a private conversation between us', 29, 7),
    ('Sounds good, its just us then', 28, 7)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Group Convo 2');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (8, 9), (8, 10), (8, 11);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('message1', 8, 8),
    ('message2', 9, 8),
    ('message2', 10, 8)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 7');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (9, 27), (9, 26);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('This is a private conversation between us', 27, 7),
    ('Sounds good, its just us then', 26, 7)
;"

psql -U $USER -d cse412groupproject -c "INSERT INTO Conversation (name) VALUES ('Normal Convo 8');"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationUsers VALUES (10, 26), (10, 25);"
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, conversation_id) VALUES 
    ('This is a private conversation between us', 26, 7),
    ('Sounds good, its just us then', 25, 7)
;"

# Social Feed Messages
psql -U $USER -d cse412groupproject -c "INSERT INTO ConversationMessage (content, sender_id, isfeedmessage) VALUES
    ('This is my first feed message', 1, 1),
    ('I like this messaging service!', 2, 1),
    ('[Insert Political Hot Take]', 3, 1),
    ('asd;alkjsdf;lkajsd;flk', 7, 1),
    ('random message', 6, 1),
    ('just testing out this service', 5, 1),
    ('another message being sent out to all of my friends <3', 1, 1),
    ('another message being sent out to all of my friends <3', 1, 1),
    ('hellllllllo', 6, 1),
    ('wayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy longer message', 30, 1),
    ('shorter message', 29, 1),
    ('asdfasdfasdfasdfasdfasdfasdfasdfasdfasdf random typing to get a much longer message than some of the other messages in the database', 28, 1),
    ('tesingtestingtesting', 27, 1)
;"

# Finally, open a psql command prompt
psql -p $1 -U $USER cse412groupproject
