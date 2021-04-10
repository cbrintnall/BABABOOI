from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
import gamestate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def broadcast_gamestate(room):
    st = gamestate.get_gamestate(room)
    msg = json.dumps(st)
    emit('gamestate', msg, to=room)

@app.route('/can_create_new_game')
def can_create_new_game():
    if gamestate.can_create_new_game():
        return "yes"
    return "no"

@socketio.on('join_game')
def join_game(data):
    packet = json.loads(data)
    error = gamestate.add_player(packet)
    if error != '':
        emit('error', error)
        return
    join_room(packet['room'])
    broadcast_gamestate(packet['room'])

@socketio.on('leave_game')
def leave_game(data):
    packet = json.loads(data)
    game_still_exists = gamestate.remove_player(packet)
    leave_room(packet['room'])
    if game_still_exists:
        broadcast_gamestate(packet['room'])

@socketio.on('choose_game')
def choose_game(data):
    packet = json.loads(data)
    err = gamestate.change_mode(packet)
    if err != '':
        emit('error', error)
        return
    broadcast_gamestate(packet['room'])

@socketio.on('start_game')
def start_game(data):
    packet = json.loads(data)
    err = gamestate.start_game(packet)
    if err != '':
        emit('error', error)
        return
    broadcast_gamestate(packet['room'])

@socketio.on('submit_image')
def submit_image(data):
    pass

@socketio.on('submit_text')
def submit_text(data):
    pass

if __name__ == '__main__':
    socketio.run(app)
