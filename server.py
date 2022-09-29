#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import threading


ADDRESS = "0.0.0.0"
PORT = 9808

ROOMS = {}


def accept_clients(server: socket.socket):
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr,)).start()


def handle_client(client: socket.socket, addr: str):
    current_room = ""
    while True:
        try:
            data = client.recv(1024)

            # 连接断开
            if data == b'':
                removeMember(current_room, client)

            if data.startswith('create'.encode('utf-8')):
                msg_str = data.decode('utf-8')
                try:
                    _, room_name = msg_str.split()
                    if room_name in ROOMS.keys():
                        client.send(
                            "This room name is already in use!".encode('utf-8'))
                    else:
                        current_room = room_name
                        ROOMS[current_room] = [client]
                        client.send("success".encode('utf-8'))
                except Exception:
                    client.send("error".encode('utf-8'))

            elif data.startswith('join'.encode('utf-8')):
                msg_str = data.decode('utf-8')
                _, room_name = msg_str.split()
                if not room_name in ROOMS.keys():
                    client.send("error".encode('utf-8'))
                else:
                    current_room = room_name
                    ROOMS[current_room].append(client)
                    client.send("success".encode('utf-8'))

            elif current_room != "":
                for each in ROOMS[current_room]:
                    if client != each:
                        try:
                            client.send(data)
                        except:
                            pass

        except socket.error:
            removeMember(current_room, client)


def removeMember(room_name: str, client: socket.socket):
    try:
        room: list[socket.socket] = ROOMS.get(room_name)
        room.remove(client)
        if len(room) < 1:
            ROOMS.pop(room_name)
    except Exception:
        pass
    finally:
        client.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.listen(64)
    print(f"\033[1;32mListening at: {ADDRESS}\033[0m")
    print(f"\033[1;32mServer port: {PORT}\033[0m")
    accept_clients(server)


if __name__ == '__main__':
    main()
