from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
import gamestate
import boto3
import io
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/status')
def status():
    status = gamestate.get_server_status()
    response = app.response_class(
        response=json.dumps(status),
        status=200)

@app.route('/create')
def create():
    if request.method == 'POST':
        if 'username' not in request.args.keys() or 'sessionId' not in request.args.keys():
            return app.response_class("Missing param", 404)
        user = request.args['username']
        room = request.args['sessionId']

        if 'create' not in request.args.keys():
            err = gamestate.create_player_in_room(room, user)
        else:
            err = gamestate.create_room_with_player(room, user)
        code = 200 if err == '' else 404
        broadcast_gamestate(room)
        return app.response_class(err, code)

def broadcast_gamestate(room):
    st = gamestate.get_gamestate(room)
    if st == None:
        return
    msg = json.dumps(st)
    emit('gamestate', msg, to=room)

# @socketio.on('join_game')
# def join_game(data):
#     packet = json.loads(data)
#     error = gamestate.add_player(packet)
#     if error != '':
#         emit('error', error)
#         return
#     join_room(packet['room'])
#     broadcast_gamestate(packet['room'])

@socketio.on('leave_game')
def leave_game(data):
    packet = json.loads(data)
    gamestate.remove_player(packet)
    leave_room(packet['room'])
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

def download_images():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bababooi')
    # obj = bucket.Object('asdfasdfadsf')
    # fs = io.StringIO()
    # obj.download_fileobj(fs)

if __name__ == '__main__':
    download_images()
    socketio.run(app)
