# app.py
# Run: `python3 app.py` to start the web server

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import ConnectionRefusedError, Namespace

'''
Introduction:
1. Receive message
2. Send message
3. Broadcast message
4. Rooms
5. Connection events
6. Class-based namespaces
7. Error handling
8. Debugging
'''

# -----------------------------------------------------------------------------
# Initialize flask and flask_socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key!'
socketio = SocketIO(app)


# -----------------------------------------------------------------------------
'''
<Receiving messages>
Messages are received by both parties as events.
On client side: Javascript callbacks are used.
On server side: register handlers for these events (similar to handle routes).
'''
@socketio.on('message')
def handle_print_message(msg): # msg is a string
    print('Server received message: ' + msg)
    
@socketio.on('json')
def handle_print_json(json): # json is a JSON object
    print('Server received json: ' + json)
    
@socketio.on('my event', namespace='/chat')
def handle_print_my_custom_event(json): # named event
    print('received json: ' + str(json))
    return 'one', 2


# -----------------------------------------------------------------------------
'''
<Sending messages>
'send()' is used for unnamed events; 'emit()' is used for named events.
'''
@socketio.on('message')
def handle_send_message(msg):
    send(msg)

@socketio.on('json')
def handle_send_json(json):
    send(json, json=True)

def ack():
    print('Message sent to client was received')

'''
With callbacks, JS client receives a callback function to invoke upon 
  receipt of the message. 
After the client invokes the callback function, the server invokes 
  the corresponding server-side callback. 
If the client-side callback is invoked with arguments, these are provided 
  as arguments to the server-side callback as well.
'''
@socketio.on('my event')
def handle_emit_my_custom_event(json): # named event
    emit('Response from server:', 
         ('apple', json), 
         namespace='/chat', 
         callback=ack)


# -----------------------------------------------------------------------------
'''
<Broadcast>
When a message is sent using broadcast, all clients connected to the namespace 
  receive it, including the sender. 
When namespaces are not used, the clients connected to the global namespace 
  receive the message. 
Note that callbacks are not invoked for broadcast messages.
'''
@socketio.on('my event')
def handle_emit_my_custom_event_broadcast(data):
    emit('Response from server:', data, broadcast=True)
    
'''
Server as the originator of the message:
This can be useful to send notifications to clients of events that originated 
  in the server, for example in a background thread. 
'broadcast=True' is assumed in socketio.emit() and socketio.send().
Note that socketio.send() and socketio.emit() are not the same functions 
  as the context-aware send() and emit().
'''
def originator_function():
    socketio.emit('Origin event', {'data': 42})


# -----------------------------------------------------------------------------
'''
<Rooms>
Rooms are where users receive messages from the room or rooms they are in, 
  but not from other rooms.
All clients are assigned a room when they connect, named with the session ID 
  of the connection, which can be obtained from request.sid. 
A given client can join any rooms, which can be given any names. 
When a client disconnects, it is removed from all the rooms it was in.
Since all clients are assigned a personal room, to address a message to 
  a single client, the session ID of the client can be used as the to argument.
'''
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    # the 'to' argument causes the message to be sent to all the clients 
    #   that are in the given room.
    send(username + ' has entered the room.', to=room) 
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


# -----------------------------------------------------------------------------
'''
<Connection events>
'''
@socketio.on('connect')
def test_connect(auth): # 'auth' is optional
    # can raise a ConnectionRefusedError() if the authenticate() function 
    #   (written on server side) does not pass.
    emit('Response from server', {'data': 'Connected'})
    
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected.')


# -----------------------------------------------------------------------------
'''
<Class-based namespaces>
Any events received by the server are dispatched to a method named as 
  the event name with the 'on_' prefix.
'''
# Create a class-based namespace with Namespace as a base class.
class MyCustomNamespace(Namespace):
    def on_connect(self):
        pass
    def on_disconnect(self):
        pass
    def on_my_event(self, data):
        emit('Response from server:', data)
        
socketio.on_namespace(MyCustomNamespace('/chat'))


# -----------------------------------------------------------------------------
'''
<Error handling>
'''
@socketio.on_error() # handles the default namespace
def error_handler(e): # 'e' is the exception object
    pass

@socketio.on_error('/chat') # handles the '/chat' namespace
def error_handler_chat(e):
    pass

# handles all namespaces without explicit error handler
@socketio.on_error_default
def default_error_handler(e):
    pass

# 'request.event' variable can be used to inspect the message and data args 
#   of the current request.
@socketio.on('my error event')
def on_my_event(data):
    raise RuntimeError()

@socketio.on_error_default
def default_error_handler2(e):
    print(request.event['message']) # 'my error event'
    print(request.event['args']) # (data, )
    
   
# ----------------------------------------------------------------------------- 
'''
<Debugging and Troubleshooting>
The server can be configured to output logs to the terminal with the following:
'''
socketio = SocketIO(logger=True, engineio_logger=True)


# -----------------------------------------------------------------------------
if __name__=='__main__':
    socketio.run(app) # run flask_socketio to start the SocketIO web server
    