import subprocess

menu = input("Menu:\n1. Start conversation\n2. Connect to a conversation\nChoose an option (1 or 2): ")

if menu == "1":
    subprocess.run(["python", "server.py"])
elif menu == "2":
    subprocess.run(["python", "client.py"])