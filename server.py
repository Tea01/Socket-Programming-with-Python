import socket
import threading

HEADER = 64
#pick the port and the server than the socket
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) #address
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

#allowa us to open up this device to other connections
                     #the family name | streaming data through the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) #we have bound the socket with the address

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)    #until the client doesnt send a msg to connect it wont connect
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  #we will wait to this line here for a new connection to the server. when the new connection occures we will store the address of that connection and a object.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
print("[STARTING] server is starting...")
start()