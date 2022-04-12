#!/usr/bin/python

from flask import Flask
from flask_cors import CORS

# cd groupproject/app
# export FLASK_APP=app
# python3 -m flask run

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"*": {"origins": ["http://localhost:3000", "http://192.168.1.19:3000"]}})

    with app.app_context():
        from profile import bp as profile_bp
        from conversation import bp as conversation_bp
        from auth import bp as auth_bp
        from friend import bp as friend_bp

        app.register_blueprint(profile_bp, url_prefix='/profile')
        app.register_blueprint(conversation_bp, url_prefix='/conversation')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(friend_bp, url_prefix='/friend')

    return app

app = create_app()