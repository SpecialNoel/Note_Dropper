import socket
from datetime import datetime
from threading import Thread

# python3 Client.py

def create_client_socket(SERVER_HOST, SERVER_PORT):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    clientSocket.connect((SERVER_HOST, SERVER_PORT)) 
    return clientSocket

def recv_msg_from_channel(clientSocket):
    while True:
        msg = clientSocket.recv(1024)
        print('\n' + msg.decode())
    
def get_and_send_user_input_msg(clientSocket, clientName):
    def send_msg_to_channel(clientSocket, clientName, msg):
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = f'[{date_now} {clientName}:{msg}]'
        clientSocket.send(msg.encode())
    
    while True:
        msg = input()
        if msg.lower() == 'q':
            print('\nDisconnected from the chatroom')
            break
        send_msg_to_channel(clientSocket, clientName, msg)

if __name__ == '__main__':
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    
    clientSocket = create_client_socket(SERVER_HOST, SERVER_PORT)
    clientName = input('Enter your username: ')
    
    t = Thread(target=recv_msg_from_channel, args=(clientSocket,))
    t.daemon = True
    t.start()

    print('\nType a message to send to the channel, or\nType q to disconnect')
    t2 = Thread(target=get_and_send_user_input_msg, args=(clientSocket,clientName,))
    t2.daemon = True
    t2.start()

    clientSocket.close()
    print('Client socket closed')