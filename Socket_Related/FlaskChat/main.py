# main.py

# Run the program with command: python3 main.py
# Enter the URL in a broswer to open the home page: http://127.0.0.1:5000/

# Tutorial: https://thepythoncode.com/article/how-to-build-a-chat-app-in-python-using-flask-and-flasksocketio

from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
import random
import string

# Create a Flask instance
app = Flask(__name__)

# Setup the secret key to protect user session data
# It does not protect other sensitive things like user passwords
# Every time the application is restarted, users will be logged out like a cookie reset
app.config['SECRET_KEY'] = 'bkfawliaril2lhr2(@U(((#HGL((*&^%&^&**!)($@TDHWLDHIdwiuafuiqh2r9lwge99*&HWA))))))'

# Create a SocketIO instance with app
socketio = SocketIO(app)

# Used to store each individual room created
rooms = {}

# Generate a random room id that is unique among existing ids
def generate_room_code(length: int, existing_codes: list[str]) -> str:
    # Keep generating the randomized id until it is unique from previously generated ones
    while True:
        # string.ascii_letters consists of [a-zA-Z]
        # code_chars will be a string iterable with size of 'length'
        code_chars = [random.choice(string.ascii_letters) for _ in range(length)]
        # code will be the string containing the same content as code_chars with the same order
        code = ''.join(code_chars)
        # The id is unique from previously generated ones, return it
        if code not in existing_codes:
            return code


# -------------------------------- Routes --------------------------------
'''
Definition: A route is a function that defines how the server responds to a request from a client
           which is usually associated with a URL path (i.e. /chat, /about, etc.). A route can
           return a response to the client, such as an HTML page, a JSON object, or a status code.
'''     

# Home route (/): The homepage and landing page of the application.
# In the homepage, the user can enter their name, and either create a chat room, or join one with a room id.
# Handle requests to this route with the GET and POST HTTP methods.
@app.route('/', methods=['GET', 'POST'])
def home():
    # Reset session
    '''
    Definition: A session is used to store information related to a user, across different requests, 
               as they interact with a web app. We need a session since HTTP is a stateless protocol.
    '''
    session.clear()
    
    # Received a HTTP POST method
    if request.method == 'POST':
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)
        
        # The user forgets to provide their username
        if not name:
            return render_template('home.html', error='Name is required', code=code)
    
        # If the user wants to create a chat room, create it with a random id and added it to rooms
        if create != False:
            room_code = generate_room_code(6, list(rooms.keys()))
            # Each room consists of a 'members' object used to store the number of users in the room,
            # and the messages exchanged between users in that room.
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room
            
        if join != False:
            # The user wants to join a chat room, but forgets to provide the room id
            if not code:
                return render_template('home.html', error="Please enter a room code to enter a chat room", name=name)

            # The user has typed in an invalid room id
            if code not in rooms:
                return render_template('home.html', error="Room code invalid", name=name)
            
            # Assign the code to room_code for later session initiation
            room_code = code
        
        # Initiate a new session with room_code and name
        session['room'] = room_code
        session['name'] = name
        
        # Redirect the user to the room template
        return redirect(url_for('room')) 
    else:
        # Generate the home page and display it to the user
        return render_template('home.html')
    
    
# Room route (/room): Where the chat room is served. Where users can send/receive messages
#                     from other users present in the same room.
# This route only accepts the GET HTTP request
@app.route('/room')
def room():
    # Obtain the username and room from the current session
    name = session.get('name')
    room = session.get('room')
    
    # Redirect the user to the home page if the username or room does not exist,
    # or the room cannot be found in rooms
    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))

    # Obtain the messages currently going on from the current room
    messages = rooms[room]['messages']
    
    # Generate the room page and display it to the user
    return render_template('room.html', room=room, user=name, messages=messages)


# -------------------------------- SocketIO Event Handlers --------------------------------

# Connect: Handle the event when a client connects to the server
@socketio.on('connect')
def handle_connect():
    # Obtain the username and room from the current session
    name = session.get('name')
    room = session.get('room')
    
    # Do not proceed further if either the username or the room does not exist
    if name is None or room is None:
        return
    
    # If the room cannot be found in rooms
    if room not in rooms:
        # Leave the room using the leave_room() method from flask_socketio
        leave_room(room)
    
    # Join the room using the join_room() method from flask_socketio
    join_room(room)
    
    # Send the room-entering message to the current room using the send() method from flask_socketio
    message = {
        'sender': '',
        'message': f'{name} has entered the chat'
    }
    send(message=message, to=room)
    
    # Increment the number of users in that room
    rooms[room]['members'] += 1
    return

# Message: Handle the event when either the client ro server sendes a message to each other
@socketio.on('message')
def handle_message(payload):
    # Obtain the username and room from the current session
    name = session.get('name')
    room = session.get('room')
    
    # Do not proceed further if the room cannot be found in rooms
    if room not in rooms:
        return
    
    # Send the message to the current room
    message = {
        'sender': name,
        'message': payload['message']
    }
    send(message=message, to=room)
    
    # Append this message to 'messages', the collection of message, in the current room
    rooms[room]['messages'].append(message)
    
    return

# Disconnect: Handle the event when the user leaves the room
@socketio.on('disconnect')
def handle_disconnect():
    # Obtain the username and room from the current session
    name = session.get('name')
    room = session.get('room')
    
    # Leave the room using the leave_room() method from flask_socketio
    leave_room(room)
    
    if room in rooms:
        # Decrement the number of members in that room
        rooms[room]['members'] -= 1
        
        # Delete the room from rooms if no memeber is in the room anymore
        if rooms[room]['members'] <= 0:
            del rooms[room]
        
        # Send the leave notification message to the current room
        message = {
            'sender': '',
            'message': f'{name} has left the chat'
        }
        send(message=message, to=room)
        
    return
        
# Main
if __name__ == '__main__':
    # We run the SocketIO instance instead of the Flask instance (app)
    socketio.run(app, debug=True)
