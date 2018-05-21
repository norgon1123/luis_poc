from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET'])
def index():
    """Login form to enter a room."""
    name = "Example User"
    room = "Microsoft Luis"
    session.setdefault("name", name)
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


