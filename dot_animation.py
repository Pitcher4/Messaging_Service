from colorama import Fore, Back
import sys
import time
DOT_SPEED = 0.4

def Dot_Animation(title, break_loop):
    while not break_loop[0]: # break loop is a list to allow mutability
        for i in range(4): # i: 0, 1, 2, 3
            sys.stdout.write(f"{Fore.BLACK}{Back.GREEN}\r{title}{'.' * i}{' ' * (3 - i)}") # prints "." i times and replaces spaces in front of it with " ". eg. .| | , .|.| , .|.|.,
            sys.stdout.flush()
            time.sleep(DOT_SPEED)
        if break_loop[0]:
            break
