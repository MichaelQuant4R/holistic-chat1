from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
import os
from datetime import datetime
import time
from flask_gravatar import Gravatar
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from werkzeug.security import (generate_password_hash, check_password_hash)

app = Flask(__name__)


csrf = CSRFProtect(app)


# file_path = os.path.abspath(os.getcwd()) + "\database.db"


app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://aergufyovfuljj:72574957842209fe91b903dfa4efdb4c1b474e0271223997e47bb18f52b0cec0@ec2-34-202-5-87.compute-1.amazonaws.com:5432/dfoeieiamkqqvc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '\xd2\xf6Km%\x14\xff&\xe0\x97\x05\xf1\xe1Zv\x82\x88\x00R?T*\x82\xb8D\n\xc3P[Di\x17\xb6\x05b\x1e2\xfc\xe7\xaf'


# socketio = SocketIO(app, manage_session = False, cors_allowed_origins="*")
# socketio = SocketIO(app, manage_session=False)
socketio = SocketIO(app, manage_session=False, cors_allowed_origin =['http://holistic-chat.herokuapp.com'])




gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None
                   )


db = SQLAlchemy(app)

migrate = Migrate(app, db)

with app.app_context():
    
    if db.engine.url.drivername == "sqlite":
        
        migrate.init_app(app, db, render_as_batch = True)
        
    else:
        
        migrate.init_app(app, db)
        

class User(db.Model, UserMixin):
    
    
    id = db.Column(db.Integer, primary_key = True)
    
    username = db.Column(db.String(40))
    email = db.Column(db.String(40), unique = True)
    password = db.Column(db.String(128))
    confirm_password = db.Column(db.String(20))
    online = db.Column(db.Boolean, default = False)
    login_count = db.Column(db.Integer, default = 0)
    sid = db.Column(db.String(50))
    timestamp = db.Column(db.String(40))
    
    is_admin = db.Column(db.Boolean, default = False)
    
    chat_room = db.Column(db.String(50))
    
    chats = db.relationship("Chat", backref="user", lazy="dynamic")
    role = db.relationship("AdminRole", backref="user", lazy="dynamic")
    
    room_dictionary = db.relationship("RoomDict", backref="user", lazy="dynamic")

    
    def __init__(self, username, email, password, confirm_password):
        
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirm_password = confirm_password
        self.online = False
        self.login_count = 0
        self.is_admin = False
        self.timestamp = time.strftime('%b-%d-%y %I:%M%p', time.localtime())
        self.chat_room = None
        self.sid = None
    
    def checking_password(self, check_password):
        
        return check_password_hash(self.password, check_password)
    
    def get_image(self):
        
        return gravatar(self.email)
    
    
    def logged_in(self):
        
        self.online = True
        self.login_count += 1
        db.session.commit()
        print("LOGGED IN!!!")
        
    def logged_out(self):
        
        self.online = False
        db.session.commit()
        print("LOGGED OUT!!!")
        
    
        
    def __repr__(self):
        
        return "<Users {}, {}>".format(*[self.id, self.username])
        
        
        
class Chat(db.Model):
        
        id = db.Column(db.Integer, primary_key = True)
        text = db.Column(db.Text)
        room = db.Column(db.String(50))
        user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        timestamp = db.Column(db.String(40))
        sid = db.Column(db.String(50))
        
        
        joined = db.relationship("Join", backref="chat", lazy="dynamic")
        left = db.relationship("Leave", backref="chat", lazy="dynamic")
        
        
        def __init__(self, text, room, sid, user_id):
            
            self.text = text
            self.room = room
            self.user_id = user_id
            self.sid = sid
            self.timestamp = time.strftime('%b-%d-%y %I:%M%p', time.localtime())
        
        def __repr__(self):
            
            return "<Chat {}, userID {}>".format(*[self.id, self.user_id])
        
        
class Join(db.Model):
        
        id = db.Column(db.Integer, primary_key = True)
        text = db.Column(db.Text)
        room = db.Column(db.String(50))
        sid = db.Column(db.String(50))
        chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
        timestamp = db.Column(db.String(40))
        
        def __init__(self, text, room, sid, chat_id):
            
            self.text = text
            self.room = room
            self.chat_id = chat_id
            self.timestamp = time.strftime('%b-%d-%y %I:%M%p', time.localtime())
        
        def __repr__(self):
            
            return "<Join {}, ChatID {}>".format(*[self.id, self.chat_id])
        
        
class Leave(db.Model):
    
        id = db.Column(db.Integer, primary_key = True)
        text = db.Column(db.Text)
        room = db.Column(db.String(50))
        sid = db.Column(db.String(50))
        chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
        timestamp = db.Column(db.String(40))
        
        def __init__(self, text, room, sid, chat_id):
            
            self.text = text
            self.room = room
            self.sid = sid
            self.chat_id = chat_id
            self.timestamp = time.strftime('%b-%d-%y %I:%M%p', time.localtime())
        
        def __repr__(self):
            
            return "<Leave {}, ChatID {}>".format(*[self.id, self.chat_id])
        
        
class AdminRole(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.String(40))
    role = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(40), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    
    rooms = db.relationship("CreateRoom", backref="admin_role", lazy="dynamic")
    
    def __init__(self, email, role, user_id):
        
        
        self.email = email
        self.role = role
        self.user_id = user_id
        self.timestamp = time.strftime("%b-%d-%y %I:%M%p", time.localtime())
        
    def __repr__(self):
        
        return "<CreateRoom {}, adminID {}, {}>".format(*[self.id, self.user_id, self.role])
        
        
        
        
        
        
        
        
class CreateRoom(db.Model):
    
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.String(40))
    room = db.Column(db.String(50), unique = True)
    
    admin_id = db.Column(db.Integer, db.ForeignKey("admin_role.id"))
    
    
    def __init__(self, room, admin_id):
        
        self.room = room
        self.admin_id = admin_id
        self.timestamp = time.strftime("%b-%d-%y %I:%M%p", time.localtime())
        
    def __repr__(self):
        
        return "<CreateRoom {}, adminID {}, {}>".format(*[self.id, self.admin_id, self.room])
        
        
        
        
        
        
class RoomDict(db.Model):
    
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.String(40))
    room = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    
    def __init__(self, room, user_id):
        
        self.room = room
        self.user_id = user_id
        self.timestamp = time.strftime("%b-%d-%y %I:%M%p", time.localtime())
        
    def __repr__(self):
        
        return "<RoomDict {}, userID {}, {}>".format(*[self.id, self.user_id, self.room])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        