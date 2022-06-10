import socket
import threading
# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            # message = client.recv(1024)
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('QUIT'):
                name_to_quit = msg.decode('ascii')[4:]
                quit_user(name_to_quit)
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        write_thread=threading.Thread(target=write)
        write_thread.start()

def quit_user(name):
    print("check"+name)
    if name in nicknames:
        print('enter in quit_user')
        name_index= nicknames.index(name)
        client_to_quit=clients[name_index]
        clients.remove(client_to_quit)
        client_to_quit.send('You have left chat'.encode('ascii'))
        client_to_quit.send("0".encode('ascii'))
        client_to_quit.close()
        nicknames.remove(name)
        broadcast(f'{name} has left the chat'.encode('ascii'))

def write():
    while True:
        message=input("")
        msg=f"server: {message}"
        broadcast(msg.encode("ascii"))   
print("server is listening...")
receive()