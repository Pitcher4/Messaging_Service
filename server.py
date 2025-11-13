import socket
from colorama import Fore, Back
from dot_animation import Dot_Animation
import threading # threading module to run dot animation in a separate thread
from encryption import Encryption
import subprocess

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

# receives public key from client
client_public_key_pem = conn.recv(2048)
Encryption().load_peer_public_key(client_public_key_pem)

# sends servers public ket
conn.send(Encryption().public_key_pem)

# receives private key
encrypted_session_key = conn.recv(4096)
Encryption().session_key = Encryption().decrypt(encrypted_session_key)  # Decrypt AES key with private RSA key

print(f"{Fore.GREEN}Secure session established with client.{Fore.RESET}\n")


# main chat loop
while True:
    try:
        # receiving message
        encrypted_msg_client = conn.recv(4096).decode() # receive encrypted message from client
        if not msg_client:
            print(f"{Fore.RED}Client disconnected.{Fore.RESET}")
            break

        msg_client = Encryption().decrypt_message(encrypted_msg_client) # decrypted message from client
        print(f"{Fore.WHITE}Client: {msg_client}{Fore.RESET}") # show the client’s message

        # sending message
        msg_server = input(f"{Fore.BLUE}You: {Fore.RESET}")
        encrypted_msg_server = Encryption().encrypt_message(msg_server)
        conn.send(msg_server.encode()) # send message to client

    except Exception as e:
        open("errors.txt", "a").write(str(e) + "\n") # log error

        print(f"{Fore.RED}An unexpected error occurred: {e}{Fore.RESET}")

        exit = input(f"{Fore.YELLOW}Do you want to exit? (y/n): {Fore.RESET}").lower()
        if exit == "y":
            break
        else:
            subprocess.run(["python", "main.py"])