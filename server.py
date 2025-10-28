import socket
from colorama import Fore, Back
from dot_animation import Dot_Animation
import threading # threading module to run dot animation in a separate thread

IP = input("Enter IP: ").lower()
PORT = 50501

if IP == "all":
    IP = "0.0.0.0"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket
server.bind((IP, PORT)) # binds socket to IP and port

# start listening for connections
server.listen(1) # listens for connections
break_loop = [False]
# start dot animation in a separate thread
animation_thread = threading.Thread(target=Dot_Animation, args=("Waiting for connection", break_loop))
animation_thread.start()  # start the dot animation

# accept a connection
conn, addr = server.accept()

# stop the dot animation
break_loop[0] = True
animation_thread.join()

print(f"{Fore.BLACK}{Back.GREEN}Connected on {addr}")

# main chat loop
while True:
    msg_client = conn.recv(1024).decode() # receive message from client
    if not msg_client:
        print(Fore.RED + "Client disconnected.")
        break

    print(Fore.BLUE + "Client: " + msg_client) # show the client’s message

    # ask for server reply
    msg_server = input(Fore.GREEN + "You: ")  
    conn.send(msg_server.encode()) # send message to client
