# Server.py
# Run: `python3 Server.py` to start the web Server

from flask import Flask, render_template, url_for, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import ConnectionRefusedError, Namespace

# Initialize flask and flask_socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key!'
socketio = SocketIO(app)

connected_clients = [] # store all currently connected clients

''' Frontend Page '''
@app.route('/')
def index():
    return render_template('home.html')


''' Socket Related '''    
@socketio.on('connect')
def handle_connect():
    print(f'***Client [{request.sid}] connected successfully***')
    connected_clients.append(request.sid)
    display_connecting_clients()
    emit('connect', {'clientId':request.sid})
    emit('client_list_update', {'clients':connected_clients}, broadcast=True)
    
    
@socketio.on('disconnect')
def handle_disconnect():
    print(f'***Client [{request.sid}] disconnected successfully***')
    connected_clients.remove(request.sid)
    display_connecting_clients()
    emit('client_list_update', {'clients':connected_clients}, broadcast=True)
    
    
@socketio.on('receive-message')
def handle_receive_message(data):
    print(f'***Received message from Client [{request.sid}]***')
    print(f'***Message: {data['msg']}***')
    

@socketio.on('join')
def handle_join(data):
    username = session['username']
    room = data['room']
    join_room(room)
    emit('response', username + ' has entered the room.', to=room)
    
    
@socketio.on('leave')
def handle_leave(data):
    username = session['username']
    room = data['room']
    leave_room(room)
    emit('response', username + ' has left the room.', to=room)


''' Helper Functions '''
def display_connecting_clients():
    print(f'***Current connecting Clients: {connected_clients}***')

 
''' Main '''
if __name__=='__main__':
    socketio.run(app, host='127.0.0.1', port=5001) # port cannot be 5000
    