#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import socket
import threading
import pyaudio


ADDRESS = "127.0.0.1"
PORT = 9808


def tryConnect() -> socket.socket:
    print("Trying to connect to the server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ADDRESS, PORT))
    except Exception as e:
        print("Connect Failed!")
        sys.exit()
    else:
        return client


def showInfo():
    """显示LOGO
    """
    print("\033[1;36m   ______\033[1;32m____                  \033[1;36m__\033[0m")
    print("\033[1;36m  / ____\033[1;32m/ __ \\\033[1;33m__  __\033[1;31m___\033[1;35m  _____\033[1;36m/ /_\033[1;32m____  \033[1;33m_____\033[0m")
    print("\033[1;36m / /   \033[1;32m/ / / \033[1;33m/ / / \033[1;31m/ _ \\\033[1;35m/ ___\033[1;36m/ __\033[1;32m/ __ \\\033[1;33m/ ___/\033[0m")
    print("\033[1;36m/ /___\033[1;32m/ /_/ \033[1;33m/ /_/ \033[1;31m/  __\033[1;35m(__  )\033[1;36m /_\033[1;32m/ /_/ \033[1;33m/ /\033[0m")
    print("\033[1;36m\\____/\033[1;32m\\___\\_\033[1;33m\\__,_/\033[1;31m\\___/\033[1;35m____/\033[1;36m\\__/\033[1;32m\\____\033[1;33m/_/\033[0m")
    print()
    print("This is a Audio Chatting Room by cquestor.\n")
    print("I assume that you are willing to comply with the program's provisions \nwhen you open it. Please protect your privacy and respect others'. I \nwill not pay you for any loss caused by this program.\n")
    print("Now you can just enjoy it.\n")


def preChoice() -> int:
    print("1. Create a new chatting room.")
    print("2. Join a exist chatting room.")
    while True:
        selection = input("\033[1;36mPlease give me your choice: \033[0;m")
        if selection != "1" and selection != "2":
            print(
                "\n\033[1;31mInvalid selection! Just give me 1 or 2!\033[0;m\n")
        else:
            break
    return int(selection)


def receive_server_data(client: socket.socket, playing_stream: pyaudio.Stream):
    while True:
        try:
            data = client.recv(1024)
            playing_stream.write(data)
        except:
            pass


def send_data_to_server(client: socket.socket, recording_stream: pyaudio.Stream):
    print("\n\033[1;32mYou can speak now!\033[0m\n")
    while True:
        try:
            data = recording_stream.read(1024)
            client.sendall(data)
        except:
            pass


def main():
    client = tryConnect()
    showInfo()
    selection = preChoice()
    if selection == 1:
        room_name = input("\033[1;36mPlease give the room a name: \033[0;m")
        client.send(f"create {room_name}".encode("utf-8"))
        data = client.recv(1024).decode('utf-8')
        if data == "error":
            print("\n\033[1;31mCreate Failed!\033[0;m\n")
            sys.exit()
        elif data == "success":
            print(
                f"\n\033[1;32mCreate success! Your room name is: {room_name}\033[0m\n")
            p = pyaudio.PyAudio()
            playing_stream = p.open(
                format=pyaudio.paInt16, channels=1, rate=20000, output=True, frames_per_buffer=1024)
            recording_stream = p.open(
                format=pyaudio.paInt16, channels=1, rate=20000, input=True, frames_per_buffer=1024)
            threading.Thread(target=receive_server_data,
                             args=(client, playing_stream,)).start()
            send_data_to_server(client, recording_stream)
        else:
            print(f"\n\033[1;31m{data}\033[0;m\n")
            sys.exit()
    if selection == 2:
        room_name = input("Please give the room's name: ")
        client.send(f"join {room_name}".encode("utf-8"))
        data = client.recv(1024).decode('utf-8')
        if data == "error":
            print(f"\n\033[1;31mRoom [{room_name}] is not exist!\033[0;m\n")
            sys.exit()
        elif data == "success":
            print(
                f"\n\033[1;32mJoin success! Your room name is: {room_name}\033[0m\n")
            p = pyaudio.PyAudio()
            playing_stream = p.open(
                format=pyaudio.paInt16, channels=1, rate=20000, output=True, frames_per_buffer=1024)
            recording_stream = p.open(
                format=pyaudio.paInt16, channels=1, rate=20000, input=True, frames_per_buffer=1024)
            threading.Thread(target=receive_server_data,
                             args=(client, playing_stream,)).start()
            send_data_to_server(client, recording_stream)


if __name__ == '__main__':
    main()
