import socket
from colorama import Fore, Back
from dot_animation import Dot_Animation
import threading # threading module to run dot animation in a separate thread

IP = input(f"{Fore.YELLOW}Enter IP: {Fore.RESET}").lower()
PORT = 50501

if IP == "all":
    IP = "0.0.0.0"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket
server.bind((IP, PORT)) # binds socket to IP and port

# start listening for connections
server.listen(3) # listens for connections
break_loop = [False]
# start dot animation in a separate thread
animation_thread = threading.Thread(target=Dot_Animation, args=("Waiting for connection", break_loop))
animation_thread.start()  # start the dot animation

# accept a connection
conn, addr = server.accept()

# stop the dot animation
break_loop[0] = True
animation_thread.join()

print(f"{Fore.YELLOW}Connected on {addr}{Fore.RESET}")

# main chat loop
while True:
    try:
        msg_client = conn.recv(1024).decode() # receive message from client
        if not msg_client:
            print(f"{Fore.RED}Client disconnected.{Fore.RESET}")
            break

        print(f"{Fore.WHITE}Client: {msg_client}{Fore.RESET}") # show the client’s message

        # ask for server reply
        msg_server = input(f"{Fore.BLUE}You: {Fore.RESET}")  
        conn.send(msg_server.encode()) # send message to client

    except Exception as e:
        open("errors.txt", "a").write(str(e) + "\n") # log error

        print(f"{Fore.RED}An unexpected error occurred: {e}{Fore.RESET}")
        break

        exit = input(f"{Fore.YELLOW}Do you want to exit? (y/n): {Fore.RESET}").lower()
        if exit == "y":
            break
        else:
            subprocess.run(["python", "main.py"])