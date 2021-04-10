from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

@socketio.on('test_event')
def handle_message(data):
	print(data)
	send("ack")

if __name__ == '__main__':
    socketio.run(app)
