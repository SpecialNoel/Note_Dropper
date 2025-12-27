# FlaskChat
An attempt on the tutorial of building a chat application with Flask and Flask-SocketIO.

## Reference
[The FlaskChat tutorial](https://thepythoncode.com/article/how-to-build-a-chat-app-in-python-using-flask-and-flasksocketio) is published on The Python Code, by author Menard Maranan. All rights go to the original author.

## Execution
Follow these steps to run the FlaskChat program.
### 1. Setup
a) In terminal, use command ```cd FlaskChat``` to change the current folder to FlaskChat.

b) Use command ```python -m venv flask_chat_venv``` to create a [_virtual environment_](https://docs.python.org/3/library/venv.html) in the current folder.

c) Use command ```source flask_chat_venv/bin/activate``` to activate the virtual environment for Linux/MacOS. 

Use command ```\flask_chat_venv\Scripts\activate``` to activate for Windows.

You will notice the prefix **'(flask_chat_venv)'** being added to each of your terminal command lines, upon successful activation.

To deactivate the virtual environment, use command ```deactivate```.

d) Install **Flask** and **Flask-SocketIO** using command ```pip install flask-socketio```.

##

### 2. Run the server program
a) In terminal, use command ```python3 main.py``` to start the server program.

Use key-combination ```[Ctrl+c]``` in the same terminal to terminate the server program.

##

### 3. Run the client program
a) Open a browser of choice.

b) Type in the URL ```http://127.0.0.1:5000/``` to the browser to open the home page.

c) In home page, type in _username_ and click the 'Create Room' button to create and enter a chat room.

OR,

Type in _username_ and _chat room code_, then click the 'Join' button to join an existing chat room.

d) In room page, type a message and click the 'Send' button to send the message to the current chat room.

e) Click the 'Leave the Chat' button to leave the chat room and return to the home page. 
