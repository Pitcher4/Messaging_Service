import socket # handles sending and receiving data
from colorama import Fore, Back # to colour text

IP = input("Enter IP address: ") # IP adress for WiFi
PORT = 50501 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket

client.connect((IP, PORT))
print(f"{Fore.BLACK}{Back.GREEN}Broadcasting message on {IP}:{PORT}")

while True:
    msg = input(Fore.GREEN + "You: ") # users message they are sending
    client.send(msg.encode()) # sends message by encoding message into binary first

    data = client.recv(1024).decode() # decodes the message and stores it
    print(Fore.BLUE + data) # outputs the data