import socket
from colorama import Fore, Back

from dot_animation import Dot_Animation

IP = input("Enter IP: ").lower()
PORT = 50501

if IP == "all":
    IP = "0.0.0.0"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket

server.bind((IP, PORT)) # binds socket to IP and port

server.listen(1) # listens for connections
print(f"{Fore.BLACK}{Back.GREEN}Server is listening on {IP}:{PORT}")

# accept a connection
conn, addr = server.accept()
print(f"{Fore.BLACK}{Back.GREEN}Connected on {addr}")

# main chat loop
while True:
    msg_client = conn.recv(1024).decode()  # receive message from client
    if not msg_client:
        print(Fore.RED + "Client disconnected.")
        break

    print(Fore.BLUE + "Client: " + msg_client)  # show the client’s message

    # ask for server reply
    msg_server = input(Fore.GREEN + "You: ")  
    conn.send(msg_server.encode())  # send message to client
