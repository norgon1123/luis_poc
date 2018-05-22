import requests
import pprint
import webbrowser

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


URL = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/02de9d9b-9f9b-41d6-b9d3-b4f0cc47afbb?subscription-key=063bc462e0cc4895914493f4da7c157f&verbose=true&timezoneOffset=0&q="
loggedIn = False
waitForBPName = False
waitForFileName = False
bpName = ''
fileName = ''

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    if not loggedIn:
        emit('message', {'msg': 'Luis: Hello! What is your name?'}, room=room)
    else:
        emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    global loggedIn
    global waitForFileName
    global waitForBPName

    if not loggedIn:
        login(message)
        loggedIn = True
        emit('message', {'msg': 'Luis: Welcome ' + session.get('name') + '!'})
        emit('message', {'msg': 'Luis: What can I help you with?'})
    elif waitForBPName:
        #launch BP here
        launchBP(message['msg'])
        waitForBPName = False
        #waitForBPName = False
    elif waitForFileName:
        openNotepad(message['msg'])
        waitForFileName = False
    elif not waitForBPName and not waitForFileName:
        res = postMessage(message)
        if 'BP' in res:
            askForBpName('Status' in res)
        elif 'Notepad' in res:
            askForFileName();

def launchBP(bpName):
    #call api
    emit('message', {'msg': 'Luis: Launching BP with name ' + bpName + ' and UUID ' + '1234'})

def askForFileName():
    emit('message', {'msg': 'Luis: What would you like to call your new file?'})
    global waitForFileName
    waitForFileName = True

def openNotepad(fileName):
    import subprocess as sp
    programName = "/Applications/Atom.app/Contents/MacOS/Atom"
    sp.Popen([programName, fileName.split(",")[0] + '.txt'])

def login(message):
    session['name'] = message['msg']

def postMessage(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    r = requests.get(URL+message['msg'])
    print(message['msg'])
    print(r.status_code)
    print(r.json())

    print(pprint.pformat(r.json()))

    room = session.get('room')
    emit('message', {'msg': session.get('name') + ': ' + message['msg']}, room=room)

    #emit('message', {'msg': "Server Response" + ':' + pprint.pformat(str(r.json()['intents'][0]['intent']), indent=4)}, room=room)

    return r.json()['intents'][0]['intent']

def askForBpName(forStatus) :
    if forStatus:
        emit('message', {'msg': 'Luis: What is the name of the BP you would like to check?'})
    else:
        emit('message', {'msg': 'Luis: What is the name of the BP you would like to launch?'})
    global waitForBPName
    waitForBPName = True

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
