import requests
import pprint

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


URL = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/cab824f7-2aa0-4e9e-8a62-c5e5576fcba7?subscription-key=aa9e664eab614b01b8308665d9decdaf&staging=true&verbose=true&timezoneOffset=0&q="

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    r = requests.get(URL+message['msg'])
    print(message['msg'])
    print(r.status_code)
    print(r.json())

    print(pprint.pformat(r.json()))

    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)

    emit('message', {'msg': "Server Response" + ':' + pprint.pformat(str(r.json()), indent=4)}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

