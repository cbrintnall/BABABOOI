from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
import gamestate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def broadcast_players(room):
    players = gamestate.get_players(room)
    msg = {}
    msg['room'] = room
    msg['players'] = players
    msg_str = json.dumps(msg)
    emit('players', msg_str, to=room)

def broadcast_gamestate(room):
    emit('gamestate', "asdf", to=room)

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
    broadcast_players(packet['room'])

@socketio.on('leave_game')
def leave_game(data):
    packet = json.loads(data)
    game_still_exists = gamestate.remove_player(packet)
    leave_room(packet['room'])
    if game_still_exists:
        broadcast_players(packet['room'])

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
    pass

if __name__ == '__main__':
    socketio.run(app)
