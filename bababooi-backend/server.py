from flask import Flask, render_template
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

@socketio.on('join_game')
def join_game(data):
    join_packet = json.loads(data)
    player_exists = gamestate.add_player(join_packet)
    if player_exists:
        emit('error', 'Player already exists!')
        return
    join_room(join_packet['room'])
    broadcast_players(join_packet['room'])

@socketio.on('leave_game')
def leave_game(data):
    leave_packet = json.loads(data)
    game_still_exists = gamestate.remove_player(leave_packet)
    leave_room(leave_packet['room'])
    print("Game_still_exist:", game_still_exists)
    if game_still_exists:
        broadcast_players(leave_packet['room'])

@socketio.on('start_game')
def start_game(data):
    pass

if __name__ == '__main__':
    socketio.run(app)
