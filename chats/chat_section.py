from flask import (Blueprint, render_template, redirect, url_for, request, jsonify, flash)
from flask_login import (current_user, login_required)
from models import (db, app, socketio, User, Chat, Join, Leave, RoomDict)
from flask_socketio import (emit, send, join_room, leave_room, disconnect,
                            close_room)
import time
from config import  domain, rooms_dict

app_chat = Blueprint("chat_section", __name__, template_folder = "templates_chat",
#                      url_prefix="/holistic_chat",
                     static_folder = "static_chats",
                     static_url_path = "/static_chats")

# rooms_dict = {'Python': {},
#  'Javascript': {},
#  'CSS': {},
#  'HTML': {},
#  'C#': {},
#  'Java': {},
#  'C++': {},
#  'GDScript': {},
#  'Blender': {}}



@app_chat.route("/chat_room/<string:room>", methods = ["GET", "POST"])
@login_required
def chat_room(room):
    
    chats = Chat.query.filter_by(room = room).all()

    
    
    check_room_dict = RoomDict.query.filter_by(user_id = current_user.id).first()
    
    
    if check_room_dict is not None:

        if check_room_dict.room != room:


            flash("You're already in a chat room", "info")
            return redirect(url_for("chat_section.chat_room", room = check_room_dict.room))


    
    return render_template("chat_room.html", title = "chat room",
                           room = room,
                           chats = chats, 
                           domain = domain)
                           

@socketio.on("message")
def handleMessage(msg):
    
    print("MESSAGES RECEIVED!!!!")
    print(msg)
    print(current_user.id)
    text = msg["message"]
    room = msg["room"]
    user = current_user
    sid = rooms_dict[room][user.id]["sid"]
    
    join_room(room)
    
    chatting = Chat(text, room, sid, user.id)
    db.session.add(chatting)
    db.session.commit()
    
    chat = Chat.query.filter_by(user_id = user.id).filter_by(text = text).filter_by(room = room)\
    .filter_by(sid = sid).all()[-1]
    
    user_info = {"user_id": user.id, "username": current_user.username,
             "message": text, "image": current_user.get_image(), "room": room,
            "chat_id": chat.id,
            "timestamp": chat.timestamp,
             "room": room}
    
    send(user_info, broadcast = True, room = room)
    
    
    
    
@socketio.on('join')
def on_join(data):
    
    print("JOINED ROOM!")
    print(data)
    
    # Chat(text, room, user_id)
    # CreateRoom(room, admin_id)
    # Leave(text, room, chat_id)
    # Join(text, room, chat_id)
    
    
    username = data["username"]
    room =  data["room"]
    user_id = data["user_id"]
    
    join_room(room)
    
    current_user.chat_room = room
    db.session.commit()
    
    user = current_user
    
    sid = request.sid
    
    print("REQUEST SID", sid)
    
    
    text = current_user.username.title() + " has joined the " + current_user.chat_room + " room."
    
    chatting = Chat(text, room, sid, user.id)
    db.session.add(chatting)
    db.session.commit()
    
    
    check_user_in_room = RoomDict.query.filter_by(user_id = user.id).filter_by(room = room).first()
    
    if check_user_in_room is  None:
        adding_user = RoomDict(room, user.id)
        db.session.add(adding_user)
        db.session.commit()
    
    
    
    
    chat = Chat.query.filter_by(room = room).filter_by(user_id = user.id).filter_by(text = text)\
    .filter_by(sid = sid).all()[-1]
    joined = Join(text, room, sid, chat.id)
    db.session.add(joined)
    db.session.commit()
    
    user_room = room
    
    rooms_dict[user_room][user.id] = {"user_id": user.id, "username": user.username, "image": user.get_image(), "room": user_room,
                                     "sid": sid}
    
    
    print("ROOMS DICT", rooms_dict)
    
    emit("msg", {"msg": text,
                 "users_dict": rooms_dict, "sid": sid}, broadcast = True, room = room)

    
    
@socketio.on('leave')
def on_leave(data):

    print("LEAVE ROOM!")
    print(data)
    
    
    username = data['username']
    room = data['room']
    leave_room(room)
    user_id = data["user_id"]
    sid = rooms_dict[room][user_id]["sid"]
    
    
    rooms_dict[room].pop(user_id)
    
    
    user = current_user
    
    
    removing_user = RoomDict.query.filter_by(room = room).filter_by(user_id = user.id).first()
    db.session.delete(removing_user)
    db.session.commit()
    
    # Chat(text, room, user_id)
    # CreateRoom(room, admin_id)
    # Leave(text, room, chat_id)
    # Join(text, room, chat_id)
    
    text = username.title() + " has left the room"
    chatting = Chat(text, room, sid, user.id)
    db.session.add(chatting)
    db.session.commit()
    
    chat = Chat.query.filter_by(user_id = user.id).filter_by(room = room).filter_by(sid = sid).all()[-1]
    
    left = Leave(text, room, sid, chat.id)
    db.session.add(left)
    db.session.commit()
    
    print(rooms_dict)
    
    
    emit("leave", {"left":text, "users_dict":rooms_dict, "room":room}, broadcast=True, room = room)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    