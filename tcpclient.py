import socket
import threading
import time
# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                if message=="0":
                    print("quiting ....")
                    time.sleep(2)
                    quit()

                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        if message[len(nickname)+2:].startswith('/'):
            if message[len(nickname)+2:].startswith('/quit'):
                client.send(f'QUIT{message[len(nickname)+2+6:]}'.encode('ascii'))
        else:
            client.send(message.encode('ascii'))
        

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()