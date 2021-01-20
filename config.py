# rooms_dict = {"Python": {}, "Javascript":{},"Java":{}, "C#":{}, "CSS":{}, "C++": {},
#              "GDScript": {}, "Blender": {}}

from models import CreateRoom

rooms = CreateRoom.query.all()

rooms_dict = {rooms[i].room: {} for i in range(len(rooms))}
rooms_dict

# domain = "https://holistic-chat.herokuapp.com"
domain = "http://127.0.0.1:5000"