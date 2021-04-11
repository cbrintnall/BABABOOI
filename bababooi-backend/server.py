from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS
import json, io, random, string, boto3, os
from PIL import Image
import gamestate

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
preload()

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

@socketio.on('submit_image')
def submit_image(data):
    pass

@socketio.on('submit_text')
def submit_text(data):
    packet = json.loads(data)
    err = gamestate.submit_image(json)
    if err != '':
        emit('error', err)
        return
    broadcast_gamestate(packet['room'])

def preload():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bababooi')

    # Load bababooi data

    # TODO: Remove this cache for prod
    if not os.path.isfile('cached_bababooi.txt'):
        info = bucket.Object('games/adv_draw/info.json')
        gamestate.bababooi_data['info'] = json.loads(info.get()['Body'].read())
        gamestate.bababooi_data['img'] = {}
        for class_name in gamestate.bababooi_data['info']['class_names']:
            filename = 'games/adv_draw/' + class_name + '.ndjson'
            imgs = bucket.Object(filename)
            gamestate.bababooi_data['img'][class_name] = []
            imgFileStr = imgs.get()['Body'].read()
            for line in imgFileStr.splitlines():
                gamestate.bababooi_data['img'][class_name].append(json.loads(line))
        with open('cached_bababooi.txt', 'w') as fp:
            fp.write(json.dumps(gamestate.bababooi_data))
    else:
        with open('cached_bababooi.txt', 'r') as fp:
            gamestate.bababooi_data = json.loads(fp.read())
    # print(gamestate.bababooi_data['info'])
    # print(gamestate.bababooi_data['img']['tennis_racquet'])

    # images = [Image.new('L', (256, 256)) for _ in range(4)]
    # for i, image in enumerate(images):
    #     image_bytes = io.BytesIO()
    #     image.save(image_bytes, 'png')
    #     images[i] = base64.b64encode(image_bytes.getvalue()).decode('ascii')

    # json = requests.post('http://127.0.0.1:5000/predict', json=images)
    # print(json.content)

if __name__ == '__main__':
    socketio.run(app)
