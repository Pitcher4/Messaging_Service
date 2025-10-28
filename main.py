import subprocess
from colorama import Fore, Back

print(f"{Fore.BLACK}{Back.GREEN}Menu:\n1. Connect to a conversation\n2. Start a conversation\nChoose an option (1 or 2): ")
menu = input(f"{Fore.RESET}{Back.RESET}\n")

if menu == "1":
    subprocess.run(["python", "server.py"])
elif menu == "2":
    subprocess.run(["python", "client.py"])