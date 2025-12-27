# Server.py

# Run the program with command: python3 Server.py

# Tutorial from https://thepythoncode.com/article/make-a-chat-room-application-in-python

import socket
from threading import Thread

'''
Current Issues:
1. Server cannot be found by devices other than its same device. Need to update SERVER_HOST to Server device's private IP address.
2. Potential improvement: Do some printing in the Server terminal:
    a. print out the username with the address for each newly joined Client.
    b. print out a line stating which Client has joined or leaved the chatroom.
    c. print out the current chatroom (with pairs of username and address) whenever a Client joins or leaves.
3. Add a feature where the Server handles multiple chatrooms at the same time.
   Client can create a new room or join an existing room via a unique valid room code.
4. Make this application compatible to other devices, such as iOS.
'''

# Keep listening for a message from the conn socket
# Whenever a message is received, broadcast it to all other connected clients
def listen_for_client(conn):
    global clientSockets
    
    while True:
        try:
            # Keep listening for a message from conn socket
            msg = conn.recv(1024)
        except Exception as e:
            # Client is no longer connected, remove it from the set
            print(f'[!] Error: {e}')
            clientSockets.remove(conn)
        else:
            # Replace the <SEP> token with ': ' for formatting
            msgStr = msg.decode()
            msgStr = msgStr.replace(separatorToken, ': ')

        # Broadcast the message to all connected clients
        for client_socket in clientSockets:
            client_socket.send(msgStr.encode())
    
    return
       
# Main     
if __name__ == '__main__':
    # Server's IP address and port number
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    
    # Token that will be used to separate the client name & message
    separatorToken = '<SEP>'

    # Initialize a set of all connected (unique) client's sockets
    clientSockets = set()
    
    # Create a TCP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Make the port as reusable port
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the address we specified
    serverSocket.bind((SERVER_HOST, SERVER_PORT))
    
    # Listen for upcoming connections (up to 5 clients at the same time)
    serverSocket.listen(5)
    print(f'[*] Server started listening as {SERVER_HOST}:{SERVER_PORT}')

    while True:
        # Keep listening for new connections all the time
        conn, addr = serverSocket.accept()
        print(f'[+] {addr} connected.')
        
        # Add the new connected client to connected sockets set
        clientSockets.add(conn)
        
        # Start a new thread that listens for each client's messages
        t = Thread(target=listen_for_client, args=(conn,))

        # Make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        
        # Start the thread
        t.start()

    # Close client sockets
    for conn in clientSockets:
        conn.close()
        
    # Close server socket
    serverSocket.close()
    
    exit(0)

