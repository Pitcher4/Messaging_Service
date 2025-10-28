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
print(Fore.YELLOW + f"Server is listening on {IP}:{PORT}")

# accept a connection
conn, addr = server.accept()
print(Fore.CYAN + f"Connected by {addr}")

# main chat loop
while True:
    data = conn.recv(1024).decode()  # receive message from client
    if not data:
        print(Fore.RED + "Client disconnected.")
        break

    print(Fore.BLUE + "Client: " + data)  # show the client’s message

    # ask for server reply
    msg = input(Fore.GREEN + "You: ")  
    conn.send(msg.encode())  # send message to client
