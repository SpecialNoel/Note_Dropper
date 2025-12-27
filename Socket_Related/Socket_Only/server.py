import socket
from threading import Thread

# Tutorial from https://thepythoncode.com/article/make-a-chat-room-application-in-python

# Create a TCP socket for server
def create_server_socket(SERVER_HOST, SERVER_PORT):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make the 
    serverSocket.bind((SERVER_HOST, SERVER_PORT))
    return serverSocket

def handle_a_client(conn, address, clientSockets):
    while True:
        try:
            msg = conn.recv(1024)
        except Exception as e:
            conn.close()
            clientSockets.remove(conn)
            print(f'Error: {e}. Removed {address} from client sockets')
        else:
            for socket in clientSockets:
                socket.send(msg)

def accept_a_connection(serverSocket, clientSockets):
    (conn, address) = serverSocket.accept()
    print(f'Accepted connection request from Client[{address}].')
    
    clientSockets.add(conn)
    
    # Start a new thread that handles this client only
    t = Thread(target=handle_a_client, args=(conn,address,clientSockets,))
    t.daemon = True # Make the thread daemon so it ends whenever the main thread ends
    t.start()
        
if __name__=='__main__':
    MAX_CLIENT_COUNT = 1
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    serverSocket = create_server_socket(SERVER_HOST, SERVER_PORT)
    
    clientSockets = set()
    
    serverSocket.listen(MAX_CLIENT_COUNT)
    print(f'Server socket[{SERVER_HOST}: {SERVER_PORT}] started listening. MAX {MAX_CLIENT_COUNT} Clients')
    
    while True:
        accept_a_connection(serverSocket, clientSockets)
        if not len(clientSockets): 
            print('No more Client connected to the channel. Channel closed.')
            break
    
    serverSocket.close()
    print('Server socket closed')
    