import socket # handles sending and receiving data
from colorama import Fore, Back # to colour text
import subprocess # to run other scripts
import logging # to log errors
from encryption import Encryption

IP = input(f"{Fore.YELLOW}Enter IP address: {Fore.RESET}") # IP adress for WiFi
PORT = 50501 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket

while True:
    try:
        # connects to server
        client.connect((IP, PORT))
        print(f"{Fore.YELLOW}Broadcasting message on {IP}:{PORT}{Fore.RESET}") # TODO add dot animation here

        # sends public key to server
        client.send(Encryption().public_key_pem)

        # receives public key from server
        server_public_key_pem = client.recv(2048)
        Encryption().load_peer_public_key(server_public_key_pem)

        # creates a random AES session key and send it (encrypted)
        encrypted_session_key = Encryption().encrypt_for_peer(Encryption().session_key)
        client.send(encrypted_session_key)

        print(f"{Fore.GREEN}Secure session established.{Fore.RESET}\n")

        # starts chat loop
        while True:
            msg = input(f"{Fore.BLUE}You: ") # users message they are sending
            encrypted_msg = Encryption().encrypt_message(msg)
            client.send(encrypted_msg.encode()) # sends message by encoding message into binary first

            encrypted_msg_in = client.recv(4096).decode() # decodes the message out of bin (does not decrypt)
            msg_in = Encryption().decrypt_message(encrypted_msg_in) # decrypts message
            print(Fore.WHITE + msg_in) # outputs decrypted message in

# error handling
    # handle invalid IP address error
    except OSError as e:
        open("errors.txt", "a").write(str(e) + "\n") # opens/creates error log, appends error to file, automatically closes file

        print(f"{Fore.RED}{Back.RESET}Invalid IP address {Fore.GREEN}HINT: Check your IP address by running 'ipconfig' in your terminal.{Fore.RESET}")

        # asks user if they want to see advanced error code
        error = input(f"{Fore.YELLOW}Do you want to see the advanced error code? (y/n): {Fore.RESET}").lower()
        if error == "y":
            print(f"{Fore.RED}Error code: {e}{Fore.RESET}")
    
        # ask user if they want to exit or restart
        exit = input(f"{Fore.YELLOW}Do you want to exit? (y/n): {Fore.RESET}").lower()
        if exit == "y":
            break
        else:
            subprocess.run(["python", "main.py"])
    
    except Exception as e:
        open("errors.txt", "a").write(str(e) + "\n") # opens/creates error log, appends error to file, automatically closes file

        print(f"{Fore.RED}An unexpected error occurred: {e}{Fore.RESET}")

        # ask user if they want to exit or restart
        exit = input(f"{Fore.YELLOW}Do you want to exit? (y/n): {Fore.RESET}").lower()
        if exit == "y":
            break
        else:
            subprocess.run(["python", "main.py"])