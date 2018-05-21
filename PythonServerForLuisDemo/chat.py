#!/bin/env python
from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':

    print("Connect to this chat server using http://127.0.0.1:5000")
    socketio.run(app)
