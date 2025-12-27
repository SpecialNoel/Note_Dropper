# Client.py

# Run the program with command: python3 Client.py
# Make sure to run the server program (Server.py) first before running the client program

import socket
from datetime import datetime
from threading import Thread

'''
Current Issues:
1. Client needs to stop the daemon thread it created gracefully. See this website for more detail: https://superfastpython.com/stop-daemon-thread/.
2. Need to limit the max and min length of username. After that, adjust the name format with printf based on the max length.
'''

# Keep listening for messages broadcasted to this client
def listen_for_messages(clientSocket):
    while True:
        message = clientSocket.recv(1024)
        print('\n' + message.decode())

    return

if __name__ == '__main__': 
    # Server's IP address and port number
    # If the server is not on this same machine, use the private IP address
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000

    # Token that will be used to separate the client name & message
    separator_token = '<SEP>'

    # Initialize TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    print(f'[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...')
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    print('[+] Connected.')

    # Prompt the client for a name with user keyboard input
    name = input('Enter your name: ')

    # Make a thread that listens for messages broadcasted to this client and print them
    t = Thread(target=listen_for_messages, args=(clientSocket,))
    
    # Make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    
    # Start the thread
    t.start()

    # Keep 'staying' in the chatroom until the client breaks with input 'q' or key-combination [Ctrl+c]
    while True:
        # Input message we want to send to the server
        print('\nType a message to send to the chatroom, or')
        print('Type q to disconnect')
        message = input()
        
        # A hard-code way to exit the program
        if message.lower() == 'q':
            print('\nDisconnected from the chatroom')
            break
        
        # Add the datetime and name of the sender to the message
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        message = f'[{date_now}] {name}{separator_token}{message}'
        
        # Send the message to server
        clientSocket.send(message.encode())

    # Close the socket
    clientSocket.close()
    
    exit(0)
