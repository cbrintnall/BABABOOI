from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS
from model_interactions import preload, load_data_local
import json, io, random, string, os
from PIL import Image
import gamestate

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config.from_object(f'settings.{os.environ.get("CONFIG", "DevConfig")}')
socketio = SocketIO(app, cors_allowed_origins="*")

try:
    preload()
except Exception as e:
    print(f"Exception preloading: {e}, this won't stop app start, we'll try a local load instead")
    load_data_local()

@app.route('/status', methods=['GET'])
def status():
    status = gamestate.get_server_status()
    st = json.dumps(status)
    return app.response_class(response=st, status=200)

@app.route('/create', methods=['POST'])
def create():
    print(request.args)
    if 'username' not in request.args or 'sessionId' not in request.args:
        return app.response_class(response="Missing param", status=400)
    user = request.args['username']
    room = request.args['sessionId']

    if 'create' not in request.args:
        err = gamestate.create_player_in_room(room, user)
    else:
        err = gamestate.create_room_with_player(room, user)
    print(err)
    code = 200 if err == '' else 400
    return app.response_class(response=err, status=code)

def broadcast_gamestate(room):
    st = gamestate.get_gamestate(room)
    if st == None:
        return
    msg = json.dumps(st)
    emit('gamestate', msg, to=room)

@socketio.on('handshake')
def handshake(data):
    packet = json.loads(data)
    join_room(packet['room'])
    broadcast_gamestate(packet['room'])

@socketio.on('leave_game')
def leave_game(data):
    packet = json.loads(data)
    gamestate.remove_player(packet)
    leave_room(packet['room'])
    broadcast_gamestate(packet['room'])

@socketio.on('choose_game')
def choose_game(data):
    packet = json.loads(data)
    err = gamestate.choose_game(packet)
    if err != '':
        emit('error', err)
        return
    broadcast_gamestate(packet['room'])

@socketio.on('start_game')
def start_game(data):
    packet = json.loads(data)
    err = gamestate.start_game(packet)
    if err != '':
        emit('error', err)
        return
    broadcast_gamestate(packet['room'])

    # Hacky patch to assure newRound=False for every other call
    room = packet['room']
    game = gamestate.games[room]
    if game.gameType == 'bababooi':
        game.gameSpecificData['newRound'] = False

@socketio.on('is_round_over')
def is_round_over(data):
    packet = json.loads(data)
    room = packet['room']
    if gamestate.is_round_over(room):
        gamestate.bababooi_end_round2(gamestate.games[room])
        broadcast_gamestate(room)

@socketio.on('start_next_round')
def start_next_round(data):
    packet = json.loads(data)
    gamestate.bababooi_start_next_round(packet)

@socketio.on('submit_image')
def submit_image(data):
    packet = json.loads(data)
    gamestate.submit_image(packet)

@socketio.on('submit_text')
def submit_text(data):
    packet = json.loads(data)
    err = gamestate.submit_text(packet)
    if err != '':
        emit('error', err)
        return
    broadcast_gamestate(packet['room'])

if __name__ == '__main__':
    socketio.run(app)
